"""Pruebas del generador de datos sintéticos RIE-01.

Ejecutar:  python -m pytest retos/RIE-01/datos -q
Prueban propiedades del DATASET (integridad, rangos, reproducibilidad, ausencia de datos personales,
embudo exposición ≠ pérdida, mapa informativo pero imperfecto). No prueban ningún modelo de exposición.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

RUTA_GENERADOR = Path(__file__).resolve().parent / "generar.py"
_spec = importlib.util.spec_from_file_location("rie01_generar", RUTA_GENERADOR)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

SEMILLA = 123
N = 3000


@pytest.fixture(scope="module")
def t():
    return gen.generar_todo(seed=SEMILLA, n_clientes=N)


# ---------------------------------------------------------------- reproducibilidad
def test_misma_semilla_mismos_datos(t):
    otra = gen.generar_todo(seed=SEMILLA, n_clientes=N)
    assert t.keys() == otra.keys()
    for k in t:
        pd.testing.assert_frame_equal(t[k], otra[k], check_exact=True)


def test_semilla_distinta_cambia_los_datos(t):
    otra = gen.generar_todo(seed=SEMILLA + 1, n_clientes=N)
    assert not t["clientes"]["lat"].equals(otra["clientes"]["lat"])
    assert not t["impacto_backtest"]["afectado"].equals(otra["impacto_backtest"]["afectado"])


def test_escritura_csv_es_reproducible(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    for d in (a, b):
        assert gen.main(["--seed", "5", "--n-clientes", "800", "--out", str(d)]) == 0
    ma = json.loads((a / "manifest.json").read_text(encoding="utf-8"))
    mb = json.loads((b / "manifest.json").read_text(encoding="utf-8"))
    assert ma["archivos"] == mb["archivos"]
    for rel in gen.ARCHIVOS.values():
        assert (a / rel).exists()
    assert (a / "LEEME.md").exists()


def test_n_clientes_minimo():
    with pytest.raises(ValueError):
        gen.generar_todo(n_clientes=10)


# ---------------------------------------------------------------- esquema e integridad
COLUMNAS_CLAVE = {
    "clientes": ["cliente_id", "agencia_id", "distrito_id", "sector_id", "lat", "lon", "actividad_id",
                 "fecha_alta", "antiguedad_meses", "ingreso_mensual_soles"],
    "creditos": ["credito_id", "cliente_id", "producto", "monto_desembolsado_soles", "saldo_soles",
                 "dias_atraso", "calificacion", "estado"],
    "mapa_amenaza": ["distrito_id", "tipo_amenaza", "indice", "categoria", "resolucion"],
    "impacto_backtest": ["evento_id", "cliente_id", "afectado", "incumple_30d", "saldo_en_mora_soles"],
    "impacto_historico": ["evento_id", "cliente_id", "afectado", "incumple_30d"],
}


@pytest.mark.parametrize("tabla,cols", COLUMNAS_CLAVE.items())
def test_columnas_clave_sin_nulos(t, tabla, cols):
    df = t[tabla]
    for c in cols:
        assert c in df.columns, f"{tabla}.{c}"
        assert df[c].notna().all(), f"nulos en {tabla}.{c}"


def test_ids_unicos(t):
    assert t["clientes"]["cliente_id"].is_unique
    assert t["creditos"]["credito_id"].is_unique
    assert t["sectores"]["sector_id"].is_unique
    assert t["distritos"]["distrito_id"].is_unique


def test_claves_foraneas(t):
    cli = set(t["clientes"]["cliente_id"])
    assert set(t["creditos"]["cliente_id"]) <= cli
    assert cli <= set(t["creditos"]["cliente_id"]), "todo cliente tiene al menos un crédito"
    assert set(t["clientes"]["sector_id"]) <= set(t["sectores"]["sector_id"])
    assert set(t["clientes"]["distrito_id"]) <= set(t["distritos"]["distrito_id"])
    assert set(t["clientes"]["agencia_id"]) <= set(t["agencias"]["agencia_id"])
    assert set(t["clientes"]["actividad_id"]) <= set(t["actividades"]["actividad_id"])
    assert set(t["sectores"]["distrito_id"]) <= set(t["distritos"]["distrito_id"])
    assert set(t["impacto_backtest"]["cliente_id"]) <= cli
    assert set(t["impacto_historico"]["cliente_id"]) <= cli
    assert set(t["impacto_backtest"]["evento_id"]) == set(t["eventos_backtest"]["evento_id"])
    assert set(t["impacto_historico"]["evento_id"]) <= set(t["eventos_historicos"]["evento_id"])
    assert set(t["eventos_backtest"]["escenario_id"]) <= set(t["escenarios"]["escenario_id"])
    s = t["sectores"].merge(t["clientes"][["sector_id", "distrito_id"]], on="sector_id", suffixes=("_s", "_c"))
    assert (s["distrito_id_s"] == s["distrito_id_c"]).all(), "el sector del cliente está en su distrito"


def test_cobertura_del_mapa(t):
    n_d = len(t["distritos"])
    assert len(t["mapa_amenaza"]) == n_d * len(gen.TIPOS_AMENAZA)
    assert set(t["mapa_amenaza"]["tipo_amenaza"]) == set(gen.TIPOS_AMENAZA)
    assert len(t["verdad_amenaza_sector"]) == len(t["sectores"]) * len(gen.TIPOS_AMENAZA)


def test_cada_amenaza_tiene_las_cuatro_categorias(t):
    cats = t["mapa_amenaza"].groupby("tipo_amenaza")["categoria"].agg(lambda s: set(s))
    for tipo, c in cats.items():
        assert c == {"bajo", "medio", "alto", "muy_alto"}, tipo


# ---------------------------------------------------------------- rangos y plausibilidad
def test_coordenadas_en_el_norte_del_peru(t):
    for tabla in ("clientes", "sectores", "distritos", "agencias"):
        df = t[tabla]
        assert df["lat"].between(-10.0, -3.0).all(), tabla
        assert df["lon"].between(-82.0, -77.5).all(), tabla


def test_creditos_coherentes(t):
    c = t["creditos"]
    assert (c["monto_desembolsado_soles"] >= 500).all() and (c["monto_desembolsado_soles"] <= 80_000).all()
    assert (c["saldo_soles"] > 0).all()
    assert (c["saldo_soles"] <= c["monto_desembolsado_soles"] + 0.01).all()
    assert (c["cuota_mensual_soles"] > 0).all()
    assert c["plazo_meses"].between(6, 36).all()
    assert c["tea_pct"].between(20, 60).all()
    assert (c["dias_atraso"] >= 0).all()
    assert set(c["producto"]) <= {"capital_trabajo", "activo_fijo", "agropecuario"}
    assert set(c["calificacion"]) <= {"normal", "cpp", "deficiente", "dudoso", "perdida"}
    vencidos = c["estado"] == "vencido"
    assert (c.loc[vencidos, "dias_atraso"] > 30).all()
    assert (c.loc[~vencidos, "dias_atraso"] <= 30).all()


def test_cartera_sintetica_con_mora_moderada(t):
    mora = (t["creditos"]["dias_atraso"] > 30).mean()
    assert 0.02 < mora < 0.10, "mora sintética plausible (no representa a la Caja)"
    assert 1.0 <= len(t["creditos"]) / len(t["clientes"]) <= 1.3


def test_antiguedad_y_fechas(t):
    cl = t["clientes"]
    cr = t["creditos"].merge(cl[["cliente_id", "fecha_alta"]], on="cliente_id")
    assert (pd.to_datetime(cr["fecha_desembolso"]) >= pd.to_datetime(cr["fecha_alta"]) - pd.Timedelta(days=31)).all()
    assert (pd.to_datetime(cl["fecha_alta"]) <= pd.Timestamp(gen.FECHA_CORTE_POR_DEFECTO)).all()
    assert (cl["antiguedad_meses"] >= 1).all()


def test_carga_financiera_razonable(t):
    cuota = t["creditos"].groupby("cliente_id")["cuota_mensual_soles"].sum()
    ing = t["clientes"].set_index("cliente_id")["ingreso_mensual_soles"]
    carga = (cuota / ing.reindex(cuota.index))
    assert carga.quantile(0.99) <= 0.75  # casos extremos posibles al recortar el ingreso a [600, 15 000]
    assert 0.08 < carga.median() < 0.35


def test_indices_en_rango(t):
    assert t["mapa_amenaza"]["indice"].between(0, 1).all()
    assert t["verdad_amenaza_sector"]["susceptibilidad_real"].between(0, 1).all()
    imp = t["impacto_backtest"]
    assert imp["intensidad_local_real"].between(0, 1).all()
    assert imp["caida_ingreso_pct"].between(0, 0.9).all()
    assert set(imp["afectado"]) <= {0, 1} and set(imp["incumple_30d"]) <= {0, 1}
    assert imp["dias_atraso_max_90d"].between(0, 90).all()


def test_mezcla_de_actividades_sensibles(t):
    cl = t["clientes"].merge(t["actividades"], on="actividad_id")
    share = cl["es_sensible_clima"].mean()
    assert 0.20 < share < 0.60, "ni todo ni nada es sensible al clima"
    por_perfil = cl.merge(t["distritos"][["distrito_id", "perfil"]], on="distrito_id").groupby("perfil")["es_sensible_clima"].mean()
    assert por_perfil["agricola_costa"] > por_perfil["urbano"] + 0.2
    assert set(t["actividades"]["rubro"]) >= {"agropecuario", "comercio", "servicios", "pesca"}


def test_distribucion_geografica(t):
    cl = t["clientes"].merge(t["distritos"][["distrito_id", "departamento", "zona"]], on="distrito_id")
    assert (cl["departamento"] == "La Libertad").mean() > 0.55
    assert cl["departamento"].nunique() >= 4
    assert set(cl["zona"]) == set(gen.ZONAS)
    assert cl["distrito_id"].nunique() >= 40


def test_montos_en_soles_y_sin_extremos(t):
    assert t["creditos"]["saldo_soles"].median() < 8_000
    assert t["clientes"]["ingreso_mensual_soles"].between(600, 15_000).all()


def test_capacidad_de_agencias(t):
    a = t["agencias"]
    assert (a["n_gestores"] >= 2).all()
    assert (a["capacidad_visitas_semana"] == a["n_gestores"] * 12).all()


def test_acciones_exigen_aprobacion_humana(t):
    ac = t["acciones_preventivas"]
    assert (ac["requiere_aprobacion_humana"] == 1).all()
    assert (ac["efectividad_min"] < ac["efectividad_max"]).all()
    assert (ac["efectividad_max"] <= 1).all()
    assert (ac["origen_parametros"] == "supuesto_generador").all()


# ---------------------------------------------------------------- sin datos personales ni red
PROHIBIDAS = re.compile(r"nombre_cliente|apellido|dni|documento|telefono|celular|correo|email|direccion|domicilio|genero|sexo", re.I)


def test_sin_columnas_de_datos_personales(t):
    for tabla, df in t.items():
        malas = [c for c in df.columns if PROHIBIDAS.search(c)]
        assert not malas, f"{tabla}: {malas}"


def test_ids_sinteticos_no_ordenados_por_distrito(t):
    cl = t["clientes"].sort_values("cliente_id")
    assert re.fullmatch(r"C\d{6}", cl["cliente_id"].iloc[0])
    primeros = cl.head(200)["distrito_id"].nunique()
    assert primeros > 15, "los ids están barajados, no agrupados por distrito"


def test_el_generador_no_usa_red():
    codigo = RUTA_GENERADOR.read_text(encoding="utf-8")
    assert not re.search(r"^\s*(import|from)\s+(requests|urllib|socket|http|ftplib|smtplib|aiohttp|httpx)\b",
                         codigo, re.M)


# ---------------------------------------------------------------- historia, backtest y verdad oculta
def test_historico_menos_severo_que_backtest(t):
    assert t["eventos_backtest"]["severidad_realizada"].max() > t["eventos_historicos"]["severidad_realizada"].max() + 0.1


def test_backtest_difiere_del_escenario_ex_ante(t):
    e = t["eventos_backtest"]
    assert (e["severidad_realizada"] != e["severidad_nominal"]).all(), "incertidumbre de escenario presente"


def test_eventos_historicos_son_anteriores_al_corte_y_backtest_posteriores(t):
    corte = pd.Timestamp(gen.FECHA_CORTE_POR_DEFECTO)
    assert (pd.to_datetime(t["eventos_historicos"]["fecha_inicio"]) < corte).all()
    assert (pd.to_datetime(t["eventos_backtest"]["fecha_inicio_simulada"]) > corte).all()


def test_historico_solo_incluye_clientes_ya_existentes(t):
    alta = t["clientes"].set_index("cliente_id")["fecha_alta"]
    h = t["impacto_historico"].merge(t["eventos_historicos"][["evento_id", "fecha_inicio"]], on="evento_id")
    h["alta"] = alta.reindex(h["cliente_id"]).to_numpy()
    assert (pd.to_datetime(h["alta"]) <= pd.to_datetime(h["fecha_inicio"])).all()


def test_impacto_historico_no_filtra_verdad_oculta(t):
    assert "intensidad_local_real" not in t["impacto_historico"].columns
    assert "saldo_en_mora_soles" not in t["impacto_historico"].columns


def test_saldo_en_mora_consistente(t):
    imp = t["impacto_backtest"]
    assert (imp.loc[imp["incumple_30d"] == 0, "saldo_en_mora_soles"] == 0).all()
    assert (imp.loc[imp["incumple_30d"] == 1, "saldo_en_mora_soles"] > 0).all()


def test_todos_los_clientes_en_cada_evento_de_backtest(t):
    por_evento = t["impacto_backtest"].groupby("evento_id").size()
    assert (por_evento == len(t["clientes"])).all()


def test_mas_severidad_mas_afectacion(t):
    e = t["eventos_backtest"].set_index("evento_id")
    imp = t["impacto_backtest"].groupby("evento_id")["afectado"].mean()
    for tipo in gen.TIPOS_AMENAZA:
        sub = e[e["tipo_amenaza"] == tipo]
        if len(sub) >= 2:
            a, b = sub["severidad_realizada"].idxmin(), sub["severidad_realizada"].idxmax()
            assert imp[b] > imp[a], tipo


def test_exposicion_no_es_perdida(t):
    """El embudo se estrecha: no todo expuesto resulta afectado y no todo afectado entra en mora."""
    d = gen.diagnostico_embudo(t)
    assert (d["p_afectado_si_expuesto"] < 0.6).all()
    assert (d["p_mora_si_expuesto"] < d["p_afectado_si_expuesto"]).all()
    assert (d["p_mora_si_expuesto"] > 0).all()
    assert (d["pct_saldo_expuesto"].between(0.05, 0.60)).all()


def test_mapa_visible_es_informativo_pero_imperfecto(t):
    """Correlación positiva con la afectación real por distrito, sin ser perfecta (hay que ir más fino)."""
    mapa = t["mapa_amenaza"]
    cli = t["clientes"][["cliente_id", "distrito_id"]]
    corrs = []
    for ev in t["eventos_backtest"].itertuples(index=False):
        d = t["impacto_backtest"].query("evento_id == @ev.evento_id").merge(cli, on="cliente_id")
        tasa = d.groupby("distrito_id")["afectado"].mean()
        idx = mapa[mapa["tipo_amenaza"] == ev.tipo_amenaza].set_index("distrito_id")["indice"].reindex(tasa.index)
        corrs.append(np.corrcoef(idx, tasa)[0, 1])
    medio = float(np.mean(corrs))
    assert 0.35 < medio < 0.97, medio


def test_hay_perdida_fuera_del_mapa_distrital(t):
    """Parte de la mora ocurre en distritos no marcados como alto/muy alto: el mapa grueso no basta."""
    d = gen.diagnostico_embudo(t)
    frac = d["saldo_en_mora_no_expuesto_soles"] / d["saldo_en_mora_total_soles"]
    assert (frac > 0.15).all()


def test_el_colchon_financiero_protege(t):
    cl = t["clientes"].set_index("cliente_id")
    imp = t["impacto_backtest"].merge(cl[["tiene_ingreso_secundario", "tiene_seguro", "meses_reserva"]],
                                      left_on="cliente_id", right_index=True)
    imp["colchon"] = imp["tiene_ingreso_secundario"] + imp["tiene_seguro"] + (imp["meses_reserva"] >= 2).astype(int)
    alta_expo = imp[imp["intensidad_local_real"] > imp["intensidad_local_real"].quantile(0.8)]
    con = alta_expo[alta_expo["colchon"] >= 2]["afectado"].mean()
    sin = alta_expo[alta_expo["colchon"] == 0]["afectado"].mean()
    assert con < sin


def test_verdad_sector_difiere_del_mapa(t):
    """El mapa distrital no reproduce la verdad por sector (hay varianza intra-distrito)."""
    v = t["verdad_amenaza_sector"].merge(t["sectores"][["sector_id", "distrito_id"]], on="sector_id")
    sd_intra = v.groupby(["distrito_id", "tipo_amenaza"])["susceptibilidad_real"].std().mean()
    assert sd_intra > 0.10
