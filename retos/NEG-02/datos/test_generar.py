"""Pruebas del generador de datos sintéticos NEG-02.

Ejecutar: python -m pytest retos/NEG-02/datos -q
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Se carga por ruta con un nombre único para no chocar con otros `generar.py` del repo.
_RUTA = Path(__file__).with_name("generar.py")
_spec = importlib.util.spec_from_file_location("neg02_generar", _RUTA)
g = importlib.util.module_from_spec(_spec)
sys.modules["neg02_generar"] = g
_spec.loader.exec_module(g)

N = 500
SEMILLA = 12345


@pytest.fixture(scope="module")
def t() -> dict[str, pd.DataFrame]:
    return g.generar(n_clientes=N, semilla=SEMILLA)


# ---------------------------------------------------------------- reproducibilidad
def _hash_df(df: pd.DataFrame) -> str:
    return hashlib.sha256(df.to_csv(index=False, lineterminator="\n").encode("utf-8")).hexdigest()


def test_misma_semilla_mismas_tablas(t):
    otra = g.generar(n_clientes=N, semilla=SEMILLA)
    for nombre in t:
        assert _hash_df(t[nombre]) == _hash_df(otra[nombre]), nombre


def test_semilla_distinta_cambia_los_datos(t):
    otra = g.generar(n_clientes=N, semilla=SEMILLA + 1)
    assert _hash_df(t["productos_cliente"]) != _hash_df(otra["productos_cliente"])
    assert _hash_df(t["consentimientos"]) != _hash_df(otra["consentimientos"])


def test_parametros_invalidos():
    with pytest.raises(ValueError):
        g.generar(n_clientes=5)
    with pytest.raises(ValueError):
        g.generar(n_clientes=50, meses=1)
    with pytest.raises(ValueError):
        g.generar(n_clientes=50, tasa_consentimiento=1.5)


# ---------------------------------------------------------------- esquema
def _tipo_ok(serie: pd.Series, tipo: str) -> bool:
    if tipo == "str":
        return serie.dropna().map(lambda x: isinstance(x, str)).all()
    if tipo == "bool":
        return pd.api.types.is_bool_dtype(serie)
    if tipo == "int":
        return pd.api.types.is_integer_dtype(serie)
    if tipo == "float":
        return pd.api.types.is_float_dtype(serie) or pd.api.types.is_integer_dtype(serie)
    if tipo == "date":
        return pd.api.types.is_datetime64_any_dtype(serie)
    raise AssertionError(tipo)


def test_esquema_coincide_con_la_especificacion(t):
    assert set(t) == set(g.COLUMNAS) == set(g.ARCHIVOS)
    for nombre, cols in g.COLUMNAS.items():
        df = t[nombre]
        assert list(df.columns) == [c[0] for c in cols], nombre
        for col, tipo, _ in cols:
            assert _tipo_ok(df[col], tipo), f"{nombre}.{col} no es {tipo}"


def test_claves_primarias_unicas_y_sin_nulos(t):
    claves = {
        "entidades": ["entidad_id"], "catalogo_productos": ["producto_id"], "clientes": ["cliente_id"],
        "productos_cliente": ["producto_cliente_id"], "transacciones": ["tx_id"],
        "consentimientos": ["consentimiento_id"], "consentimiento_alcances": ["consentimiento_id", "alcance"],
        "consentimiento_eventos": ["evento_id"], "alcances_campos": ["alcance", "tabla", "columna"],
        "verdad_cliente": ["cliente_id"], "verdad_oportunidades": ["cliente_id", "tipo_oportunidad"],
    }
    for nombre, pk in claves.items():
        df = t[nombre]
        assert df[pk].notna().all().all(), nombre
        assert not df.duplicated(pk).any(), nombre


def test_integridad_referencial(t):
    ent = set(t["entidades"]["entidad_id"])
    cli = set(t["clientes"]["cliente_id"])
    prod_cat = set(t["catalogo_productos"]["producto_id"])
    pc = t["productos_cliente"]
    assert set(pc["cliente_id"]) <= cli
    assert set(pc["entidad_id"]) <= ent
    assert set(pc["producto_id"]) <= prod_cat
    cat = t["catalogo_productos"].set_index("producto_id")["entidad_id"]
    assert (pc["producto_id"].map(cat) == pc["entidad_id"]).all()
    tx = t["transacciones"]
    assert set(tx["cliente_id"]) <= cli
    assert set(tx["producto_cliente_id"]) <= set(pc["producto_cliente_id"])
    dueno = pc.set_index("producto_cliente_id")[["cliente_id", "entidad_id"]]
    j = tx.join(dueno, on="producto_cliente_id", rsuffix="_p")
    assert (j["cliente_id"] == j["cliente_id_p"]).all() and (j["entidad_id"] == j["entidad_id_p"]).all()
    c = t["consentimientos"]
    assert set(c["cliente_id"]) <= cli
    assert set(c["entidad_receptora_id"]) <= ent and set(c["entidad_fuente_id"]) <= ent
    assert set(t["consentimiento_alcances"]["consentimiento_id"]) <= set(c["consentimiento_id"])
    assert set(t["consentimiento_eventos"]["consentimiento_id"]) <= set(c["consentimiento_id"])
    assert set(t["verdad_cliente"]["cliente_id"]) == cli


# ---------------------------------------------------------------- ecosistema multientidad
def test_al_menos_tres_entidades_fuente_con_clientes(t):
    ent = t["entidades"]
    fuentes = ent[ent["rol_sandbox"] == "FUENTE"]
    assert len(fuentes) >= 3
    assert (ent["rol_sandbox"] == "RECEPTORA").sum() == 1
    activos = t["productos_cliente"]
    for e in fuentes["entidad_id"]:
        assert (activos["entidad_id"] == e).any(), e


def test_clientes_con_productos_en_varias_entidades(t):
    activos = t["productos_cliente"].query("estado != 'CANCELADO'")
    n_ent = activos.groupby("cliente_id")["entidad_id"].nunique().reindex(t["clientes"]["cliente_id"]).fillna(0)
    assert (n_ent >= 1).all(), "todo cliente debe tener al menos un producto"
    assert (n_ent >= 2).mean() >= 0.40
    assert (n_ent >= 3).mean() >= 0.10
    prospectos = t["clientes"].query("not es_cliente_caja")
    assert 0.25 <= len(prospectos) / N <= 0.55
    caja = activos.query("entidad_id == 'E00'")["cliente_id"]
    assert set(t["clientes"].query("es_cliente_caja")["cliente_id"]) <= set(caja), "todo cliente de la Caja tiene un producto allí"
    assert not set(prospectos["cliente_id"]) & set(caja)


def test_entidades_ficticias(t):
    ent = t["entidades"]
    assert ent["ficticia"].all()
    assert t["catalogo_productos"]["es_supuesto"].all()
    for nombre in ent.query("entidad_id != 'E00'")["nombre"]:
        assert nombre.endswith("Demo"), nombre
    reales = ["BCP", "BBVA", "Interbank", "Scotiabank", "Mibanco", "Agrobanco", "Yape", "Plin", "Cajamarca", "Piura"]
    texto = " ".join(ent["nombre"]) + " " + " ".join(t["catalogo_productos"]["nombre"])
    for r in reales:
        assert r.lower() not in texto.lower(), r


# ---------------------------------------------------------------- productos
def test_creditos_coherentes_con_el_catalogo(t):
    pc = t["productos_cliente"].merge(t["catalogo_productos"], on="producto_id", suffixes=("", "_cat"))
    cred = pc[pc["categoria"].isin(g.CATEGORIAS_CREDITO)]
    assert len(cred) > 500
    assert (cred["monto_original_pen"] >= cred["monto_min_pen"] - 1e-6).all()
    assert (cred["monto_original_pen"] <= cred["monto_max_pen"] + 1e-6).all()
    assert (cred["tasa_ea_pct"] >= cred["tea_min_pct"] - 1e-6).all()
    assert (cred["tasa_ea_pct"] <= cred["tea_max_pct"] + 1e-6).all()
    assert (cred["saldo_actual_pen"] <= cred["monto_original_pen"] + 0.01).all()
    assert (cred["saldo_actual_pen"] >= 0).all()
    todos = pc[pc["categoria"].isin(["CUENTA_AHORRO", "DEPOSITO_PLAZO", "BILLETERA_DIGITAL"])]
    assert (todos["tasa_ea_pct"] >= todos["tea_min_pct"] - 1e-6).all()
    assert (todos["tasa_ea_pct"] <= todos["tea_max_pct"] + 1e-6).all()


def test_cuota_de_prestamos_es_la_anualidad(t):
    pc = t["productos_cliente"]
    prest = pc[pc["categoria"].isin(["CREDITO_MYPE", "CREDITO_CONSUMO", "CREDITO_CONSOLIDACION"])
               & (pc["estado"] != "CANCELADO")]
    assert len(prest) > 300
    for fila in prest.head(200).itertuples():
        factor, _ = g._factor_cuota(fila.tasa_ea_pct, int(fila.plazo_meses))
        assert fila.cuota_mensual_pen == pytest.approx(fila.monto_original_pen * factor, rel=0.002, abs=0.02)


def test_atraso_estado_y_calificacion_son_consistentes(t):
    pc = t["productos_cliente"]
    cred = pc[pc["categoria"].isin(g.CATEGORIAS_CREDITO) & (pc["estado"] != "CANCELADO")]
    assert (cred["calificacion"] == cred["dias_atraso"].map(g.calificacion_por_dias)).all()
    assert ((cred["dias_atraso"] > 8) == (cred["estado"] == "MORA")).all()
    assert (cred["dias_atraso"] > 8).any(), "debe haber algo de mora"
    assert (pc[~pc["categoria"].isin(g.CATEGORIAS_CREDITO)]["dias_atraso"] == 0).all()
    canc = pc[pc["estado"] == "CANCELADO"]
    assert len(canc) > 0
    assert (canc["saldo_actual_pen"] == 0).all() and canc["fecha_cierre"].notna().all()
    assert (canc["fecha_cierre"] > canc["fecha_apertura"]).all()
    assert (pc["fecha_apertura"] <= pd.Timestamp(g.FECHA_CORTE)).all()


@pytest.mark.parametrize("dias,esperada", [(0, "NORMAL"), (8, "NORMAL"), (9, "CPP"), (30, "CPP"), (31, "DEFICIENTE"),
                                           (60, "DEFICIENTE"), (61, "DUDOSO"), (120, "DUDOSO"), (121, "PERDIDA")])
def test_tramos_de_calificacion(dias, esperada):
    assert g.calificacion_por_dias(dias) == esperada


# ---------------------------------------------------------------- transacciones
def test_transacciones_validas(t):
    tx = t["transacciones"]
    assert len(tx) > 20000
    assert (tx["monto_pen"] > 0).all()
    assert tx["fecha"].max() <= pd.Timestamp(g.FECHA_CORTE)
    assert tx["fecha"].min() >= pd.Timestamp(2026, 5, 1)
    assert (tx.loc[tx["tipo"].str.startswith("ABONO"), "sentido"] == "CREDITO").all()
    assert (tx.loc[~tx["tipo"].str.startswith("ABONO"), "sentido"] == "DEBITO").all()
    pc = t["productos_cliente"].set_index("producto_cliente_id")
    cuotas = tx[tx["tipo"] == "PAGO_CUOTA"]
    assert pc.loc[cuotas["producto_cliente_id"], "categoria"].isin(g.CATEGORIAS_CREDITO).all()
    abonos = tx[tx["tipo"].str.startswith("ABONO")]
    assert pc.loc[abonos["producto_cliente_id"], "categoria"].isin(g.CATEGORIAS_TRANSACCIONALES).all()
    assert tx["tx_id"].is_monotonic_increasing


def test_hay_clientes_sin_flujo_observable_y_con_flujo_en_varias_entidades(t):
    tx = t["transacciones"]
    ab = tx[tx["tipo"].str.startswith("ABONO")]
    con_flujo = ab["cliente_id"].nunique()
    assert 0.70 * N <= con_flujo < N, "debe haber un grupo sin cuenta (economía en efectivo)"
    multi = ab.groupby("cliente_id")["entidad_id"].nunique()
    assert (multi >= 2).sum() > 0.05 * N


def test_crecimiento_de_abonos_distingue_al_arquetipo(t):
    v = t["verdad_cliente"]
    con = v[v["arquetipo_crecimiento"]]["crecimiento_abonos"].dropna()
    sin = v[~v["arquetipo_crecimiento"]]["crecimiento_abonos"].dropna()
    assert len(con) > 20
    assert con.mean() > 0.20
    assert sin.mean() < 0.05
    assert (sin >= g.CAPITAL_CRECIMIENTO_MIN).mean() < 0.05, "la estacionalidad no debe parecer crecimiento"


# ---------------------------------------------------------------- consentimientos
def test_consentimientos_vigencia_y_estado(t):
    c = t["consentimientos"]
    assert set(c["estado"]) == {"VIGENTE", "VENCIDO", "REVOCADO"}
    assert ((c["fecha_vencimiento"] - c["fecha_otorgado"]).dt.days == c["plazo_dias"]).all()
    assert set(c["plazo_dias"]) <= {90, 180, 365} and set(c["historia_meses"]) <= {3, 6, 12}
    assert (c["fecha_otorgado"] <= pd.Timestamp(g.FECHA_CORTE)).all()
    rev = c[c["fecha_revocado"].notna()]
    assert len(rev) > 0
    assert (rev["fecha_revocado"] > rev["fecha_otorgado"]).all()
    assert (rev["fecha_revocado"] <= rev["fecha_vencimiento"]).all()
    assert (rev["fecha_revocado"] <= pd.Timestamp(g.FECHA_CORTE)).all()
    esperado = [g.estado_consentimiento(r, v) for r, v in zip(c["fecha_revocado"], c["fecha_vencimiento"])]
    assert list(c["estado"]) == esperado
    vig = c[c["estado"] == "VIGENTE"]
    assert (vig["fecha_vencimiento"] >= pd.Timestamp(g.FECHA_CORTE)).all() and vig["fecha_revocado"].isna().all()
    assert set(c["finalidad"]) == set(g.FINALIDADES)


def test_estado_en_el_borde_de_vencimiento():
    corte = pd.Timestamp(g.FECHA_CORTE)
    assert g.estado_consentimiento(None, corte) == "VIGENTE"
    assert g.estado_consentimiento(None, corte - pd.Timedelta(days=1)) == "VENCIDO"
    assert g.estado_consentimiento(corte - pd.Timedelta(days=5), corte + pd.Timedelta(days=30)) == "REVOCADO"
    assert g.estado_consentimiento(pd.NaT, corte + pd.Timedelta(days=30)) == "VIGENTE"


def test_alcances_validos_y_siempre_incluyen_productos(t):
    al = t["consentimiento_alcances"]
    assert set(al["alcance"]) == set(g.ALCANCES)
    por = al.groupby("consentimiento_id")["alcance"].apply(set)
    assert set(por.index) == set(t["consentimientos"]["consentimiento_id"])
    assert por.map(lambda s: "PRODUCTOS" in s).all()
    assert por.map(len).nunique() > 2, "debe haber alcances de distinto tamaño"


def test_los_alcances_cubren_todas_las_columnas_de_datos(t):
    ac = t["alcances_campos"]
    for tabla in ("productos_cliente", "transacciones"):
        cubiertas = list(ac.loc[ac["tabla"] == tabla, "columna"])
        assert len(cubiertas) == len(set(cubiertas)), "una columna en un solo alcance"
        esperado = set(t[tabla].columns) - set(g.COLUMNAS_CLAVE[tabla])
        assert set(cubiertas) == esperado, tabla
    assert set(ac["alcance"]) == set(g.ALCANCES)


def test_consentimientos_son_coherentes_con_los_productos(t):
    c, pc = t["consentimientos"], t["productos_cliente"]
    assert (c["entidad_receptora_id"] != c["entidad_fuente_id"]).all()
    tiene = set(zip(pc["cliente_id"], pc["entidad_id"]))
    assert all((a, b) in tiene for a, b in zip(c["cliente_id"], c["entidad_fuente_id"])), \
        "solo se consiente compartir datos de entidades donde el cliente tiene productos"
    a_caja = c[c["entidad_receptora_id"] == "E00"]
    assert len(a_caja) > 0 and (a_caja["entidad_fuente_id"] != "E00").all()
    terceros = c[c["entidad_receptora_id"] != "E00"]
    assert len(terceros) > 0, "deben existir consentimientos a otros receptores (no valen para la Caja)"
    prospectos = set(t["clientes"].query("not es_cliente_caja")["cliente_id"])
    assert set(a_caja["cliente_id"]) & prospectos, "los prospectos también pueden consentir a la Caja"


def test_renovaciones(t):
    c = t["consentimientos"].set_index("consentimiento_id")
    ren = c[c["renueva_a"].notna()]
    assert len(ren) > 0
    for kid, r in ren.iterrows():
        previo = c.loc[r["renueva_a"]]
        assert (previo["cliente_id"], previo["entidad_fuente_id"], previo["entidad_receptora_id"]) == \
               (r["cliente_id"], r["entidad_fuente_id"], r["entidad_receptora_id"])
        assert r["fecha_otorgado"] >= previo["fecha_vencimiento"]
        assert previo["estado"] == "VENCIDO"


def test_eventos_de_auditoria(t):
    c = t["consentimientos"].set_index("consentimiento_id")
    ev = t["consentimiento_eventos"]
    assert ev["fecha"].is_monotonic_increasing
    assert set(ev["tipo"]) == {"OTORGADO", "REVOCADO", "VENCIDO"}
    por = ev.groupby("consentimiento_id")["tipo"].apply(list)
    for kid, r in c.iterrows():
        tipos = por[kid]
        assert tipos.count("OTORGADO") == 1
        assert ("REVOCADO" in tipos) == (r["estado"] == "REVOCADO")
        assert ("VENCIDO" in tipos) == (r["estado"] == "VENCIDO")


def test_tasa_de_consentimiento_es_un_parametro():
    n = 150
    sin = g.generar(n_clientes=n, semilla=SEMILLA, tasa_consentimiento=0.0)["consentimientos"]
    todo = g.generar(n_clientes=n, semilla=SEMILLA, tasa_consentimiento=1.0)["consentimientos"]
    base = g.generar(n_clientes=n, semilla=SEMILLA)["consentimientos"]
    assert (sin["entidad_receptora_id"] == "E00").sum() == 0
    a, b, c = (len(x[x["entidad_receptora_id"] == "E00"]) for x in (sin, base, todo))
    assert a < b < c


# ---------------------------------------------------------------- verdad de terreno
def test_prevalencias_de_oportunidades_son_plausibles(t):
    vo = t["verdad_oportunidades"]
    assert set(vo["tipo_oportunidad"]) == set(g.TIPOS_OPORTUNIDAD)
    assert len(vo) == N * len(g.TIPOS_OPORTUNIDAD)
    assert set(vo["existe"]) == {0, 1}
    prev = vo.groupby("tipo_oportunidad")["existe"].mean()
    for tipo, p in prev.items():
        assert 0.03 <= p <= 0.25, (tipo, p)


def test_verdad_se_puede_recalcular_de_forma_independiente(t):
    pc, tx, v, vo = t["productos_cliente"], t["transacciones"], t["verdad_cliente"].set_index("cliente_id"), t["verdad_oportunidades"]
    ingreso = v["ingreso_mensual_real_pen"]
    verdad = {tp: dict(zip(gr["cliente_id"], gr["existe"])) for tp, gr in vo.groupby("tipo_oportunidad")}
    activos = pc[pc["estado"] != "CANCELADO"]
    por_cli = {k: gr for k, gr in activos.groupby("cliente_id")}
    abonos = tx[tx["tipo"].str.startswith("ABONO")]
    ab_cli = {k: gr for k, gr in abonos.groupby("cliente_id")}
    es_caja = t["clientes"].set_index("cliente_id")["es_cliente_caja"]
    for cid in t["clientes"]["cliente_id"]:
        gr = por_cli.get(cid, activos.iloc[0:0])
        cred = gr[gr["categoria"].isin(g.CATEGORIAS_CREDITO)]
        ratio = cred["cuota_mensual_pen"].sum() / ingreso[cid]
        restr = ratio > g.UMBRAL_RATIO_SOBREENDEUDAMIENTO or cred["calificacion"].isin(g.CALIFICACIONES_RIESGO).any()
        assert verdad["RESTRICCION_SOBREENDEUDAMIENTO"][cid] == int(restr), cid
        aho = gr[(gr["categoria"] == "CUENTA_AHORRO") & (gr["entidad_id"] != "E00") & (gr["tasa_ea_pct"] <= g.AHORRO_TEA_MAX)]
        assert verdad["CAPTACION_AHORRO"][cid] == int(aho["saldo_actual_pen"].sum() >= g.AHORRO_SALDO_MIN), cid
        ext = cred[cred["entidad_id"] != "E00"]
        consol = (not restr and len(ext) >= g.CONSOL_MIN_CREDITOS_EXTERNOS
                  and ext["saldo_actual_pen"].sum() >= g.CONSOL_MIN_SALDO_EXTERNO
                  and (len(ext) > 0 and ext["tasa_ea_pct"].max() >= g.CONSOL_TEA_MIN)
                  and ratio >= g.CONSOL_RATIO_MIN)
        assert verdad["CONSOLIDACION_DEUDA"][cid] == int(consol), cid
        ab = ab_cli.get(cid)
        if ab is None:
            assert verdad["DOMICILIACION_INGRESOS"][cid] == 0 and verdad["CAPITAL_TRABAJO_MYPE"][cid] == 0
            continue
        prom = ab["monto_pen"].sum() / 6
        share = ab.loc[ab["entidad_id"] == "E00", "monto_pen"].sum() / ab["monto_pen"].sum()
        dom = bool(es_caja[cid]) and prom >= g.ABONOS_PROMEDIO_MIN and share < g.DOM_SHARE_MAX
        assert verdad["DOMICILIACION_INGRESOS"][cid] == int(dom), cid


def test_sobreendeudados_tienen_mayor_carga_y_casos_dificiles(t):
    v = t["verdad_cliente"]
    sob = v[v["arquetipo_sobreendeudado"]]
    nor = v[~v["arquetipo_sobreendeudado"]]
    assert len(sob) > 15
    assert sob["ratio_cuota_ingreso"].mean() > 2 * nor["ratio_cuota_ingreso"].mean()
    assert (sob["ratio_cuota_ingreso"] > g.UMBRAL_RATIO_SOBREENDEUDAMIENTO).mean() >= 0.60
    # deuda cara dispersa que NO debe recibir oferta de consolidación (casos difíciles para el agente)
    m = v.merge(t["verdad_oportunidades"].pivot(index="cliente_id", columns="tipo_oportunidad", values="existe"),
                left_on="cliente_id", right_index=True)
    dificiles = m[m["arquetipo_deuda_cara_dispersa"] & (m["CONSOLIDACION_DEUDA"] == 0)]
    positivos = m[m["CONSOLIDACION_DEUDA"] == 1]
    assert len(dificiles) > 5 and len(positivos) > 20


def test_carpeta_verdad_separada(t):
    assert g.ARCHIVOS["verdad_cliente"].startswith("verdad/")
    assert g.ARCHIVOS["verdad_oportunidades"].startswith("verdad/")
    for nombre, ruta in g.ARCHIVOS.items():
        assert nombre.startswith("verdad") == ruta.startswith("verdad/")
    publicas = [c for n in t if not n.startswith("verdad") for c in t[n].columns]
    assert "ingreso_mensual_real_pen" not in publicas, "el ingreso real es latente y no debe filtrarse"


# ---------------------------------------------------------------- sin datos personales
def test_sin_datos_personales(t):
    prohibidas = {"nombre_completo", "apellido", "dni", "documento", "telefono", "celular", "correo", "email",
                  "direccion", "ruc", "sexo", "genero"}
    for nombre, df in t.items():
        assert not prohibidas & {c.lower() for c in df.columns}, nombre
    dni = re.compile(r"\b\d{8}\b|\b9\d{8}\b|@")
    for nombre, df in t.items():
        for col in df.select_dtypes(include="object").columns:
            muestras = df[col].dropna().astype(str)
            assert not muestras.str.contains(dni).any(), f"{nombre}.{col} parece contener un dato personal"
    assert (t["clientes"]["cliente_id"].str.fullmatch(r"C\d{6}")).all()


def test_montos_y_geografia_plausibles(t):
    cli = t["clientes"]
    assert set(cli["segmento"]) == set(g.SEGMENTOS)
    assert cli["provincia"].nunique() >= 4 and cli["distrito"].nunique() >= 8
    ing = t["verdad_cliente"]["ingreso_mensual_real_pen"]
    assert ing.min() >= 1130 and ing.max() <= 30000
    assert 1800 <= ing.median() <= 3200
    decl = cli.loc[cli["es_cliente_caja"], "ingreso_declarado_caja_pen"]
    assert decl.notna().all() and cli.loc[~cli["es_cliente_caja"], "ingreso_declarado_caja_pen"].isna().all()
    assert cli.loc[cli["es_cliente_caja"], "fecha_alta_caja"].notna().all()
    assert cli.loc[~cli["es_cliente_caja"], "fecha_alta_caja"].isna().all()


# ---------------------------------------------------------------- escritura
def test_escribir_genera_archivos_manifest_y_es_reproducible(tmp_path):
    tablas = g.generar(n_clientes=60, semilla=7)
    m1 = g.escribir(tablas, tmp_path / "a", semilla=7, meses=6)
    m2 = g.escribir(g.generar(n_clientes=60, semilla=7), tmp_path / "b", semilla=7, meses=6)
    assert m1 == m2, "mismos parámetros => mismos bytes"
    for rel, info in m1["archivos"].items():
        ruta = tmp_path / "a" / rel
        assert ruta.exists()
        assert hashlib.sha256(ruta.read_bytes()).hexdigest() == info["sha256"]
        assert len(pd.read_csv(ruta)) == info["filas"]
    assert set(m1["archivos"]) == set(g.ARCHIVOS.values())
    leido = json.loads((tmp_path / "a" / "manifest.json").read_text(encoding="utf-8"))
    assert leido["semilla"] == 7 and leido["n_clientes"] == 60 and leido["fecha_corte"] == "2026-10-31"
    assert "sintéticos" in leido["aviso"]
    diccionario = (tmp_path / "a" / "diccionario_datos.md").read_text(encoding="utf-8")
    for ruta in g.ARCHIVOS.values():
        assert ruta in diccionario


def test_csv_se_lee_de_vuelta_con_los_mismos_valores(tmp_path):
    tablas = g.generar(n_clientes=60, semilla=3)
    g.escribir(tablas, tmp_path, semilla=3, meses=6)
    cons = pd.read_csv(tmp_path / "consentimientos.csv", parse_dates=["fecha_otorgado", "fecha_vencimiento", "fecha_revocado"])
    assert list(cons["estado"]) == list(tablas["consentimientos"]["estado"])
    assert (cons["fecha_otorgado"] == tablas["consentimientos"]["fecha_otorgado"]).all()
    pc = pd.read_csv(tmp_path / "productos_cliente.csv")
    assert pc["saldo_actual_pen"].sum() == pytest.approx(tablas["productos_cliente"]["saldo_actual_pen"].sum())


def test_ventana_de_meses_configurable():
    tablas = g.generar(n_clientes=60, semilla=3, meses=3)
    tx = tablas["transacciones"]
    assert tx["fecha"].min() >= pd.Timestamp(2026, 8, 1) and tx["fecha"].max() <= pd.Timestamp(date(2026, 10, 31))
    assert tablas["verdad_cliente"]["crecimiento_abonos"].notna().any()
