"""Pruebas del generador de datos sintéticos RIE-02.

Verifican integridad, reproducibilidad, ausencia de fugas hacia el detector, que cada patrón
inyectado tenga la forma que dice el diccionario de datos y que los señuelos legítimos
efectivamente engañen a una regla simple (si no engañaran, no medirían falsos positivos).

Ejecutar: python -m pytest retos/RIE-02/datos -q
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

_RUTA = Path(__file__).with_name("generar.py")
_spec = importlib.util.spec_from_file_location("rie02_generar", _RUTA)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

ENTRADA = ("personas", "negocios", "direcciones", "telefonos", "dispositivos", "solicitudes",
           "referencias", "agencias")


@pytest.fixture(scope="module")
def d():
    return gen.generar(semilla=2026, escala=1.0)


@pytest.fixture(scope="module")
def chico():
    return gen.generar(semilla=7, escala=0.2)


# ---------- helpers ----------
def _fk_ok(hijo: pd.Series, padre: pd.Series, permitir_vacio: bool = False) -> bool:
    valores = hijo[hijo != ""] if permitir_vacio else hijo
    return bool(valores.isin(set(padre)).all())


def _tokens(d, sids: list[str]) -> dict[str, set[tuple[str, str]]]:
    """Entidades por solicitud: personas, teléfonos, dispositivos y direcciones."""
    s = d["solicitudes"].set_index("solicitud_id").loc[sids]
    neg = d["negocios"].set_index("negocio_id")["direccion_id"]
    refs = d["referencias"]
    refs = refs[refs["solicitud_id"].isin(sids)]
    t: dict[str, set] = {sid: set() for sid in sids}
    for sid, fila in s.iterrows():
        t[sid].add(("p", fila["solicitante_id"]))
        t[sid].add(("t", fila["telefono_id"]))
        t[sid].add(("d", fila["direccion_domicilio_id"]))
        t[sid].add(("d", neg[fila["negocio_id"]]))
        if fila["dispositivo_id"]:
            t[sid].add(("v", fila["dispositivo_id"]))
    for _, f in refs.iterrows():
        t[f["solicitud_id"]].add(("p", f["persona_referencia_id"]))
        t[f["solicitud_id"]].add(("t", f["telefono_referencia_id"]))
    return t


def _componentes(tokens: dict[str, set]) -> int:
    padre = {k: k for k in tokens}

    def raiz(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    por_token: dict = defaultdict(list)
    for sid, ts in tokens.items():
        for tk in ts:
            por_token[tk].append(sid)
    for sids in por_token.values():
        for otro in sids[1:]:
            padre[raiz(otro)] = raiz(sids[0])
    return len({raiz(k) for k in tokens})


def _sids(d, red_id: str) -> list[str]:
    et = d["etiquetas_solicitudes"]
    return et.loc[et["red_id"] == red_id, "solicitud_id"].tolist()


def _redes(d, patron: str) -> list[str]:
    r = d["redes_verdad"]
    return r.loc[r["patron"] == patron, "red_id"].tolist()


# ---------- integridad ----------
def test_ids_unicos_y_llaves_foraneas(d):
    for tabla, col in (("personas", "persona_id"), ("negocios", "negocio_id"),
                       ("direcciones", "direccion_id"), ("telefonos", "telefono_id"),
                       ("dispositivos", "dispositivo_id"), ("solicitudes", "solicitud_id"),
                       ("referencias", "referencia_id"), ("redes_verdad", "red_id")):
        assert d[tabla][col].is_unique, f"{tabla}.{col} con duplicados"
    s, n, r, e = d["solicitudes"], d["negocios"], d["referencias"], d["etiquetas_solicitudes"]
    assert _fk_ok(s["solicitante_id"], d["personas"]["persona_id"])
    assert _fk_ok(s["negocio_id"], n["negocio_id"])
    assert _fk_ok(s["telefono_id"], d["telefonos"]["telefono_id"])
    assert _fk_ok(s["dispositivo_id"], d["dispositivos"]["dispositivo_id"], permitir_vacio=True)
    assert _fk_ok(s["direccion_domicilio_id"], d["direcciones"]["direccion_id"])
    assert _fk_ok(s["agencia_id"], d["agencias"]["agencia_id"])
    assert _fk_ok(n["propietario_id"], d["personas"]["persona_id"])
    assert _fk_ok(n["direccion_id"], d["direcciones"]["direccion_id"])
    assert _fk_ok(r["solicitud_id"], s["solicitud_id"])
    assert _fk_ok(r["persona_referencia_id"], d["personas"]["persona_id"])
    assert _fk_ok(r["telefono_referencia_id"], d["telefonos"]["telefono_id"])
    assert set(e["solicitud_id"]) == set(s["solicitud_id"]) and e["solicitud_id"].is_unique
    assert _fk_ok(e.loc[e["red_id"] != "", "red_id"], d["redes_verdad"]["red_id"])


def test_sin_huerfanos(d):
    s, n, r = d["solicitudes"], d["negocios"], d["referencias"]
    usadas_personas = set(s["solicitante_id"]) | set(r["persona_referencia_id"])
    assert set(d["personas"]["persona_id"]) == usadas_personas
    assert set(n["negocio_id"]) == set(s["negocio_id"])
    assert set(d["telefonos"]["telefono_id"]) == set(s["telefono_id"]) | set(r["telefono_referencia_id"])
    assert set(d["dispositivos"]["dispositivo_id"]) == set(s.loc[s["dispositivo_id"] != "", "dispositivo_id"])
    assert set(d["direcciones"]["direccion_id"]) == (
        set(s["direccion_domicilio_id"]) | set(n["direccion_id"]))


def test_referencias_dos_o_mas_por_solicitud(d):
    por = d["referencias"].groupby("solicitud_id").size()
    assert len(por) == len(d["solicitudes"])
    assert por.min() >= 1 and por.max() <= 3


def test_la_persona_de_referencia_no_es_la_solicitante(d):
    m = d["referencias"].merge(d["solicitudes"][["solicitud_id", "solicitante_id"]], on="solicitud_id")
    assert (m["persona_referencia_id"] != m["solicitante_id"]).all()


# ---------- ficticio y plausible ----------
def test_documentos_y_telefonos_claramente_ficticios(d):
    assert d["personas"]["documento_ficticio"].str.fullmatch(r"FIC-\d{8}").all()
    assert d["telefonos"]["numero_ficticio"].str.fullmatch(r"FIC-\d{9}").all()
    assert d["personas"]["documento_ficticio"].is_unique
    assert d["telefonos"]["numero_ficticio"].is_unique
    assert d["dispositivos"]["huella_ficticia"].is_unique


def test_valores_plausibles(d):
    s = d["solicitudes"]
    assert s["monto_solicitado_pen"].between(1000, 80000).all()
    assert s["ingreso_mensual_declarado_pen"].ge(800).all()
    assert s["plazo_meses"].isin({6, 9, 12, 18, 24, 36}).all()
    f = pd.to_datetime(s["fecha_solicitud"])
    assert f.min() >= pd.Timestamp(gen.FECHA_INICIO)
    assert f.max() <= pd.Timestamp(date(2026, 10, 2))
    assert (f.dt.weekday != 6).all(), "no debe haber solicitudes en domingo"
    assert set(d["personas"]["distrito_residencia"]) <= set(d["agencias"]["distrito"])
    assert d["personas"]["edad_anios"].between(22, 62).all()
    assert d["direcciones"]["hogares_esperados"].ge(1).all()


def test_las_tablas_de_entrada_no_traen_etiquetas(d):
    prohibidas = ("etiqueta", "fraude", "red_id", "rol", "particion", "senuelo", "patron")
    for tabla in ENTRADA:
        for col in d[tabla].columns:
            assert not any(p in col for p in prohibidas), f"{tabla}.{col} filtra la verdad"


def test_orden_de_ids_no_delata_las_redes(d):
    """Los ids están barajados: los miembros de una red no son contiguos."""
    for rid in d["redes_verdad"].query("clase == 'fraude'")["red_id"]:
        sids = sorted(int(x[1:]) for x in _sids(d, rid))
        assert sids[-1] - sids[0] > 3 * len(sids), f"{rid} con solicitud_id casi contiguos"
        pers = sorted(int(x[1:]) for x in d["solicitudes"].set_index("solicitud_id")
                      .loc[[f"S{i:06d}" for i in sids], "solicitante_id"])
        assert pers[-1] - pers[0] > 5 * len(pers), f"{rid} con persona_id casi contiguos"


# ---------- reproducibilidad ----------
def _huella(carpeta: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(carpeta.glob("*"))}


def test_mismo_resultado_con_misma_semilla(tmp_path):
    a, b, c = tmp_path / "a", tmp_path / "b", tmp_path / "c"
    gen.escribir(gen.generar(11, 0.2), a, 11, 0.2)
    gen.escribir(gen.generar(11, 0.2), b, 11, 0.2)
    gen.escribir(gen.generar(12, 0.2), c, 12, 0.2)
    assert _huella(a) == _huella(b), "misma semilla debe dar archivos idénticos"
    assert _huella(a)["solicitudes.csv"] != _huella(c)["solicitudes.csv"]


def test_escritura_de_archivos_y_manifest(tmp_path):
    info = gen.escribir(gen.generar(5, 0.2), tmp_path, 5, 0.2)
    esperados = {f"{t}.csv" for t in ENTRADA} | {"redes_verdad.csv", "etiquetas_solicitudes.csv",
                                                  "manifest.json"}
    assert esperados <= {p.name for p in tmp_path.iterdir()}
    leido = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert leido == json.loads(json.dumps(info))
    assert leido["semilla"] == 5 and leido["escala"] == 0.2
    df = pd.read_csv(tmp_path / "solicitudes.csv", dtype=str, keep_default_na=False)
    assert len(df) == leido["filas"]["solicitudes"]


def test_main_cli(tmp_path, capsys):
    assert gen.main(["--semilla", "3", "--escala", "0.1", "--salida", str(tmp_path / "out")]) == 0
    assert (tmp_path / "out" / "solicitudes.csv").exists()
    assert "RIE-02" in capsys.readouterr().out


def test_escala_chica_conserva_todos_los_patrones(chico):
    redes = chico["redes_verdad"]
    assert set(gen.PATRONES_FRAUDE) <= set(redes["patron"])
    assert set(gen.PATRONES_SENUELO) <= set(redes["patron"])
    assert len(chico["solicitudes"]) < len(gen.generar(7, 1.0)["solicitudes"])


# ---------- volúmenes y verdad de terreno ----------
def test_volumenes_por_defecto(d):
    n = len(d["solicitudes"])
    assert 3500 <= n <= 5000
    et = d["etiquetas_solicitudes"]
    tasa_fraude = (et["etiqueta"] == "fraude").mean()
    assert 0.03 <= tasa_fraude <= 0.08
    assert (et["etiqueta"] == "legitima_senuelo").sum() >= 500
    redes = d["redes_verdad"]
    assert set(gen.PATRONES_FRAUDE) == set(redes.loc[redes["clase"] == "fraude", "patron"])
    assert set(gen.PATRONES_SENUELO) == set(redes.loc[redes["clase"] == "legitima_senuelo", "patron"])
    assert (redes.query("clase == 'fraude'").groupby("patron").size() >= 6).all()


def test_etiquetas_coherentes_con_redes(d):
    et, redes = d["etiquetas_solicitudes"], d["redes_verdad"]
    assert (et.loc[et["etiqueta"] == "normal", "red_id"] == "").all()
    assert (et.loc[et["etiqueta"] != "normal", "red_id"] != "").all()
    clase = redes.set_index("red_id")["clase"]
    for etiqueta, esperado in (("fraude", "fraude"), ("legitima_senuelo", "legitima_senuelo")):
        sub = et[et["etiqueta"] == etiqueta]
        assert (sub["red_id"].map(clase) == esperado).all()
    cuenta = et[et["red_id"] != ""].groupby("red_id").size()
    assert (redes.set_index("red_id")["n_solicitudes"] == cuenta.reindex(redes["red_id"]).values).all()
    assert et["particion"].isin({"dev", "eval"}).all()
    # Cada solicitud de una red hereda la partición de la red.
    p_red = redes.set_index("red_id")["particion"]
    con_red = et[et["red_id"] != ""]
    assert (con_red["particion"] == con_red["red_id"].map(p_red)).all()


def test_particion_dev_eval_en_cada_patron(d):
    tabla = d["redes_verdad"].groupby(["patron", "particion"]).size().unstack(fill_value=0)
    assert (tabla["dev"] >= 1).all() and (tabla["eval"] >= 1).all()


def test_dificultades_cubiertas_en_fraude(d):
    f = d["redes_verdad"].query("clase == 'fraude'")
    assert set(f["dificultad"]) == {"baja", "media", "alta"}


def test_cada_red_es_conexa_en_el_grafo(d):
    """Toda red (fraude o señuelo) forma un componente conexo vía entidades compartidas."""
    for rid in d["redes_verdad"]["red_id"]:
        sids = _sids(d, rid)
        if len(sids) > 1:
            assert _componentes(_tokens(d, sids)) == 1, f"{rid} no es conexa"


# ---------- forma de cada patrón ----------
def test_anillo_forma_un_ciclo_de_referencias(d):
    r, s = d["referencias"], d["solicitudes"].set_index("solicitud_id")
    for rid in _redes(d, "anillo"):
        sids = _sids(d, rid)
        miembros = {s.loc[x, "solicitante_id"]: x for x in sids}
        sig: dict[str, str] = {}
        for _, f in r[r["solicitud_id"].isin(sids)].iterrows():
            if f["persona_referencia_id"] in miembros:
                sig[s.loc[f["solicitud_id"], "solicitante_id"]] = f["persona_referencia_id"]
        assert set(sig) == set(miembros), "cada miembro avala a otro miembro"
        actual, visitados = next(iter(miembros)), set()
        while actual not in visitados:
            visitados.add(actual)
            actual = sig[actual]
        assert visitados == set(miembros), "las referencias recorren a todos los miembros en un ciclo"


def test_estrella_todos_citan_al_mismo_contacto(d):
    r = d["referencias"]
    et = d["etiquetas_solicitudes"]
    for rid in _redes(d, "estrella"):
        sub = et[(et["red_id"] == rid) & (et["rol"] == "testaferro")]["solicitud_id"]
        rr = r[r["solicitud_id"].isin(sub)]
        top = rr["persona_referencia_id"].value_counts()
        assert top.iloc[0] == len(sub), "un mismo contacto avala a todos los testaferros"
        tel = rr.loc[rr["persona_referencia_id"] == top.index[0], "telefono_referencia_id"]
        assert tel.nunique() == 1
        assert len(sub) >= 6


def test_dispositivo_compartido_misma_huella_identidades_distintas(d):
    s = d["solicitudes"].set_index("solicitud_id")
    for rid in _redes(d, "dispositivo_compartido"):
        f = s.loc[_sids(d, rid)]
        assert f["dispositivo_id"].nunique() == 1 and f["dispositivo_id"].iloc[0] != ""
        assert f["solicitante_id"].nunique() == len(f)
        assert f["telefono_id"].nunique() == len(f)
        fechas = pd.to_datetime(f["fecha_solicitud"])
        assert (fechas.max() - fechas.min()).days <= 50


def test_dispositivo_compartido_estructura_montos_en_dificultad_baja(d):
    s = d["solicitudes"].set_index("solicitud_id")
    redes = d["redes_verdad"].query("patron == 'dispositivo_compartido' and dificultad == 'baja'")
    for rid in redes["red_id"]:
        m = s.loc[_sids(d, rid), "monto_solicitado_pen"]
        assert m.between(0.9 * gen.UMBRAL_REVISION_PEN, gen.UMBRAL_REVISION_PEN).all()


def test_direccion_fantasma_muchos_solicitantes_un_inmueble(d):
    s = d["solicitudes"].set_index("solicitud_id")
    neg = d["negocios"].set_index("negocio_id")["direccion_id"]
    tipo = d["direcciones"].set_index("direccion_id")
    for rid in _redes(d, "direccion_fantasma"):
        f = s.loc[_sids(d, rid)]
        doms = f["direccion_domicilio_id"].value_counts()
        locs = f["negocio_id"].map(neg).value_counts()
        mejor = doms if doms.iloc[0] >= locs.iloc[0] else locs
        assert mejor.iloc[0] == len(f), "todos comparten el mismo inmueble"
        assert f["solicitante_id"].nunique() == len(f) >= 4
        capacidad = tipo.loc[mejor.index[0], "hogares_esperados"]
        assert capacidad == 1 or tipo.loc[mejor.index[0], "tipo_inmueble"] == "oficina_compartida"


def test_evasiva_debil_ningun_vinculo_aislado_pasa_de_dos(d):
    for rid in _redes(d, "evasiva_debil"):
        tk = _tokens(d, _sids(d, rid))
        por_token: dict = defaultdict(set)
        for sid, ts in tk.items():
            for t in ts:
                por_token[t].add(sid)
        compartidos = {t: v for t, v in por_token.items() if len(v) > 1}
        assert max(len(v) for v in compartidos.values()) <= 2
        tipos = {t[0] for t in compartidos}
        assert len(compartidos) >= 3 and len(tipos) >= 2
        assert _componentes(tk) == 1


# ---------- señuelos ----------
def test_familia_comparte_domicilio_y_apellido(d):
    s = d["solicitudes"].set_index("solicitud_id")
    p = d["personas"].set_index("persona_id")
    comparten = total = 0
    for rid in _redes(d, "familia"):
        f = s.loc[_sids(d, rid)]
        assert f["direccion_domicilio_id"].nunique() == 1
        assert len(f) >= 2
        if p.loc[f["solicitante_id"], "apellido_paterno"].nunique() == 1:
            comparten += 1
        total += 1
    # La mayoría comparte apellido; las familias «extendidas» (cuñados, compadres) no.
    assert 0.55 <= comparten / total < 1.0


def test_mercado_direccion_compartida_y_referencias_entre_vecinos(d):
    s = d["solicitudes"].set_index("solicitud_id")
    neg = d["negocios"].set_index("negocio_id")["direccion_id"]
    dirs = d["direcciones"].set_index("direccion_id")
    for rid in _redes(d, "mercado"):
        f = s.loc[_sids(d, rid)]
        locs = f["negocio_id"].map(neg)
        assert locs.nunique() == 1
        assert dirs.loc[locs.iloc[0], "tipo_inmueble"] == "puesto_mercado"
        assert len(f) >= 8


def test_tableta_de_agencia_es_un_dispositivo_de_tipo_tableta(d):
    s = d["solicitudes"].set_index("solicitud_id")
    disp = d["dispositivos"].set_index("dispositivo_id")
    for rid in _redes(d, "tableta_agencia"):
        f = s.loc[_sids(d, rid)]
        assert f["dispositivo_id"].nunique() == 1
        assert disp.loc[f["dispositivo_id"].iloc[0], "tipo_dispositivo"] == "tableta_agencia"
        assert (f["canal"] == "promotor_tableta").all()
        assert f["solicitante_id"].nunique() >= 3


def test_gestor_contador_mismo_contacto_con_negocios_antiguos(d):
    r, s = d["referencias"], d["solicitudes"].set_index("solicitud_id")
    neg = d["negocios"].set_index("negocio_id")
    for rid in _redes(d, "gestor_contador"):
        sids = _sids(d, rid)
        rr = r[(r["solicitud_id"].isin(sids)) & (r["relacion"] == "asesor_contable")]
        assert rr["persona_referencia_id"].nunique() == 1 and len(rr) == len(sids)
        assert neg.loc[s.loc[sids, "negocio_id"], "antiguedad_meses"].min() >= 18


def test_coincidencia_casual_son_dos_con_un_unico_dato_compartido(d):
    for rid in _redes(d, "coincidencia_casual"):
        sids = _sids(d, rid)
        assert len(sids) == 2
        a, b = _tokens(d, sids).values()
        comunes = a & b
        tipos = sorted(t[0] for t in comunes)
        # Un dato compartido; si es una persona de referencia, comparte también su propio teléfono.
        assert len(comunes) == 1 or tipos == ["p", "t"], f"{rid}: comparte {comunes}"
        fechas = pd.to_datetime(d["solicitudes"].set_index("solicitud_id").loc[sids, "fecha_solicitud"])
        assert (fechas.max() - fechas.min()).days >= 55


def test_reincidencia_legitima_misma_persona_misma_etiqueta_normal(d):
    s = d["solicitudes"]
    repetidas = s["solicitante_id"].value_counts()
    repetidas = repetidas[repetidas > 1].index
    assert 100 <= len(repetidas) <= 300
    et = d["etiquetas_solicitudes"].set_index("solicitud_id")
    sub = s[s["solicitante_id"].isin(repetidas)]
    # Quien repite no es fraude: renueva con sus propios datos (≥ 90 días).
    assert (et.loc[sub["solicitud_id"], "etiqueta"] != "fraude").all()
    for pid, g in sub.groupby("solicitante_id"):
        fechas = pd.to_datetime(g["fecha_solicitud"])
        if g["telefono_id"].nunique() == 1:
            assert (fechas.max() - fechas.min()).days >= 60


# ---------- los señuelos deben engañar a las reglas simples ----------
def _regla_simple(d, minimo: int) -> pd.Series:
    """Marca la solicitud cuyo teléfono, dispositivo o inmueble lo usan >= `minimo` personas distintas."""
    s = d["solicitudes"].copy()
    neg = d["negocios"].set_index("negocio_id")["direccion_id"]
    s["local_id"] = s["negocio_id"].map(neg)
    marca = pd.Series(False, index=s.index)
    for col in ("telefono_id", "dispositivo_id", "direccion_domicilio_id", "local_id"):
        x = s[s[col] != ""] if col == "dispositivo_id" else s
        personas = x.groupby(col)["solicitante_id"].transform("nunique")
        marca.loc[x.index[personas >= minimo]] = True
    return pd.Series(marca.values, index=s["solicitud_id"])


def _verdad(d, marca: pd.Series) -> tuple[pd.Series, pd.Series]:
    et = d["etiquetas_solicitudes"].set_index("solicitud_id")
    return et["etiqueta"].reindex(marca.index), et["red_id"].reindex(marca.index)


def test_regla_simple_cualquier_coincidencia_tiene_muchos_falsos_positivos(d):
    marca = _regla_simple(d, minimo=2)
    et, _ = _verdad(d, marca)
    marcadas = et[marca]
    precision = (marcadas == "fraude").mean()
    assert precision < 0.35, f"los señuelos deben bajar la precisión de la regla simple ({precision:.2f})"
    assert (marcadas == "legitima_senuelo").sum() >= 100
    recall = (marcadas == "fraude").sum() / (et == "fraude").sum()
    assert 0.3 <= recall <= 1.0


def test_regla_simple_de_tres_o_mas_se_pierde_el_fraude_encadenado_y_aun_asi_falla(d):
    marca = _regla_simple(d, minimo=3)
    et, red = _verdad(d, marca)
    patron = d["redes_verdad"].set_index("red_id")["patron"]
    fraude_oculto = red[(et == "fraude") & ~marca].map(patron)
    assert {"evasiva_debil", "anillo"} <= set(fraude_oculto), "el grafo debe aportar sobre la regla"
    marcadas = et[marca]
    assert (marcadas == "legitima_senuelo").sum() >= 50, "los señuelos también engañan a esta regla"
    assert (marcadas == "fraude").sum() < (et == "fraude").sum()


# ---------- honestidad del dataset: el backtest no debe ser trivial ----------
def _componentes_con_ventana(d) -> list[tuple[list[str], int]]:
    """Regla ingenua de CONTROL (no es el detector): componentes conexos por entidad compartida,
    con su tamaño y su ventana en días. Sirve solo para comprobar que el dataset no se resuelve
    con una regla de dos parámetros (tamaño mínimo y ventana máxima)."""
    sids = d["solicitudes"]["solicitud_id"].tolist()
    tokens = _tokens(d, sids)
    padre = {k: k for k in sids}

    def raiz(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    por_token: dict = defaultdict(list)
    for sid, ts in tokens.items():
        for tk in ts:
            por_token[tk].append(sid)
    for v in por_token.values():
        for o in v[1:]:
            padre[raiz(o)] = raiz(v[0])
    comp: dict = {}
    for sid in sids:
        comp.setdefault(raiz(sid), []).append(sid)
    fechas = pd.to_datetime(d["solicitudes"].set_index("solicitud_id")["fecha_solicitud"])
    return [(m, int((fechas.loc[m].max() - fechas.loc[m].min()).days)) for m in comp.values()]


def _regla_componente_rafaga(componentes, sids: list[str], minimo: int, ventana: int) -> pd.Series:
    marcadas = {s for m, dias in componentes if len(m) >= minimo and dias <= ventana for s in m}
    return pd.Series([s in marcadas for s in sids], index=sids)


def _f1(d, marca: pd.Series) -> tuple[float, float, float]:
    et = d["etiquetas_solicitudes"].set_index("solicitud_id")["etiqueta"].reindex(marca.index)
    tp = int((marca & (et == "fraude")).sum())
    prec = tp / max(1, int(marca.sum()))
    rec = tp / int((et == "fraude").sum())
    return prec, rec, 0.0 if tp == 0 else 2 * prec * rec / (prec + rec)


def test_ninguna_regla_de_un_solo_vinculo_es_buena(d):
    for minimo in (2, 3, 4):
        _, _, f1 = _f1(d, _regla_simple(d, minimo))
        assert f1 < 0.4, f"regla de coincidencia con minimo={minimo} demasiado buena (F1={f1:.2f})"


def test_regla_ingenua_de_componente_y_rafaga_no_llega_a_la_perfeccion(d):
    comps = _componentes_con_ventana(d)
    sids = d["solicitudes"]["solicitud_id"].tolist()
    mejor = 0.0
    for minimo in (3, 4, 5):
        for ventana in (14, 30, 60, 90):
            mejor = max(mejor, _f1(d, _regla_componente_rafaga(comps, sids, minimo, ventana))[2])
    assert mejor < 0.7, f"el dataset es demasiado fácil: una regla de 2 parámetros logra F1={mejor:.2f}"
    assert mejor > 0.3, "la regla de control debería ver algo; si no, el dataset no tiene señal"


def test_los_senuelos_tambien_llegan_en_rafaga(d):
    r = d["redes_verdad"]
    s = r[(r["clase"] == "legitima_senuelo") & r["patron"].isin(
        ["familia", "mercado", "asociacion_gremial", "gestor_contador"]) & (r["n_solicitudes"] >= 3)]
    dias = (pd.to_datetime(s["fecha_fin"]) - pd.to_datetime(s["fecha_inicio"])).dt.days
    assert (dias <= 30).mean() >= 0.2, "debe haber señuelos concentrados en pocos días"
    assert (dias > 90).mean() >= 0.2, "y señuelos repartidos en meses"


def test_el_fraude_dificil_se_diluye_en_el_tiempo(d):
    r = d["redes_verdad"].query("clase == 'fraude'").copy()
    r["dias"] = (pd.to_datetime(r["fecha_fin"]) - pd.to_datetime(r["fecha_inicio"])).dt.days
    por = r.groupby("dificultad")["dias"].median()
    assert por["alta"] > por["baja"], "la dificultad alta debe tener ventanas más largas"
    assert (r.loc[r["dificultad"] == "alta", "dias"] > 30).any()


def test_los_perfiles_de_fraude_y_senuelo_se_traslapan(d):
    s = d["solicitudes"].merge(d["etiquetas_solicitudes"], on="solicitud_id").merge(
        d["personas"], left_on="solicitante_id", right_on="persona_id")
    nuevo = s["meses_como_cliente"] == 0
    frac_fraude = nuevo[s["etiqueta"] == "fraude"].mean()
    frac_senuelo = nuevo[s["rol"].isin(["miembro_hogar", "comerciante_mercado", "socio_gremial",
                                        "cliente_de_gestor"])].mean()
    assert 0.5 <= frac_fraude <= 0.85, "no todo el fraude es cliente nuevo"
    assert frac_senuelo >= 0.1, "algunos señuelos son clientes nuevos"


def _regla_informada(d, maxgrado: int = 12, minimo: int = 4, ventana: int = 90, nuevos: float = 0.4):
    """Control con conocimiento de dominio (no es el detector): ignora tabletas de agencia y
    puestos de mercado, descarta entidades con demasiados usuarios y exige ráfaga y perfil nuevo."""
    sids = d["solicitudes"]["solicitud_id"].tolist()
    ss = d["solicitudes"].set_index("solicitud_id")
    per = d["personas"].set_index("persona_id")
    tablet = set(d["dispositivos"].loc[d["dispositivos"]["tipo_dispositivo"] == "tableta_agencia",
                                       "dispositivo_id"])
    mercado = set(d["direcciones"].loc[d["direcciones"]["tipo_inmueble"] == "puesto_mercado",
                                       "direccion_id"])
    padre = {k: k for k in sids}

    def raiz(a):
        while padre[a] != a:
            padre[a] = padre[padre[a]]
            a = padre[a]
        return a

    por_token: dict = defaultdict(list)
    for sid, ts in _tokens(d, sids).items():
        for tk in ts:
            if (tk[0] == "v" and tk[1] in tablet) or (tk[0] == "d" and tk[1] in mercado):
                continue
            por_token[tk].append(sid)
    for v in por_token.values():
        v = list(dict.fromkeys(v))
        if 1 < len(v) <= maxgrado:
            for o in v[1:]:
                padre[raiz(o)] = raiz(v[0])
    comp: dict = {}
    for sid in sids:
        comp.setdefault(raiz(sid), []).append(sid)
    fechas = pd.to_datetime(ss["fecha_solicitud"])
    marcadas = set()
    for m in comp.values():
        if len(m) < minimo:
            continue
        f = fechas.loc[m]
        frac_nuevos = (per.loc[ss.loc[m, "solicitante_id"], "meses_como_cliente"] == 0).mean()
        if (f.max() - f.min()).days <= ventana and frac_nuevos >= nuevos:
            marcadas.update(m)
    return pd.Series([s in marcadas for s in sids], index=sids)


def test_una_regla_con_conocimiento_de_dominio_rinde_bien_pero_no_es_perfecta(d):
    """El dataset tiene señal (se puede resolver con criterio) pero no es trivial (ni 100 %)."""
    prec, rec, f1 = _f1(d, _regla_informada(d))
    assert f1 > 0.6, f"debe haber señal recuperable (F1={f1:.2f})"
    assert f1 < 0.97 and rec < 0.99, f"demasiado fácil: P={prec:.2f} R={rec:.2f}"
    comps = _componentes_con_ventana(d)
    sids = d["solicitudes"]["solicitud_id"].tolist()
    ingenua = max(_f1(d, _regla_componente_rafaga(comps, sids, m, v))[2] for m in (3, 4, 5)
                  for v in (14, 30, 60, 90))
    assert f1 - ingenua > 0.2, "el conocimiento de dominio debe aportar bastante sobre la regla ingenua"
