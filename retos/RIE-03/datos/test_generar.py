"""Pruebas del generador sintético de RIE-03.

Verifican: reproducibilidad, esquema, integridad referencial, ausencia de fugas del futuro,
que el deterioro gradual realmente precede al atraso, que existen fluctuaciones normales que
imitan al deterioro (para medir falsos positivos), y que las variables sensibles no se
correlacionan con el resultado (para auditar sesgos del modelo que se construya después).

Ejecutar:  python -m pytest retos/RIE-03/datos -q
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Carga explícita por ruta para convivir con los demás `test_generar.py` del repo.
_spec = importlib.util.spec_from_file_location("rie03_generar", Path(__file__).resolve().parent / "generar.py")
g = importlib.util.module_from_spec(_spec)
sys.modules["rie03_generar"] = g  # los dataclass necesitan el módulo registrado
_spec.loader.exec_module(g)

N_GRANDE = 2500


@pytest.fixture(scope="module")
def t():
    return g.generar(g.Config(n_clientes=N_GRANDE))


@pytest.fixture(scope="module")
def cfg_grande():
    return g.Config(n_clientes=N_GRANDE)


# ------------------------------------------------------------------ reproducibilidad
def test_misma_semilla_mismos_datos():
    a = g.generar(g.Config(n_clientes=300, semilla=11))
    b = g.generar(g.Config(n_clientes=300, semilla=11))
    assert a.keys() == b.keys()
    for k in a:
        pd.testing.assert_frame_equal(a[k], b[k])


def test_distinta_semilla_distintos_datos():
    a = g.generar(g.Config(n_clientes=300, semilla=11))
    b = g.generar(g.Config(n_clientes=300, semilla=12))
    assert not a["cuotas"].equals(b["cuotas"])
    assert not a["senales_mensuales"].equals(b["senales_mensuales"])


def test_csv_identicos_byte_a_byte(tmp_path):
    cfg = g.Config(n_clientes=200, semilla=5)
    m1 = g.escribir(g.generar(cfg), cfg, tmp_path / "a")
    m2 = g.escribir(g.generar(cfg), cfg, tmp_path / "b")
    assert m1["sha256_csv"] == m2["sha256_csv"]
    assert set(m1["sha256_csv"]) >= {f"{k}.csv" for k in g.DICCIONARIO}


def test_cli_escribe_todo(tmp_path):
    assert g.main(["--n-clientes", "150", "--semilla", "3", "--salida", str(tmp_path)]) == 0
    for nombre in list(g.DICCIONARIO) + ["diccionario"]:
        assert (tmp_path / f"{nombre}.csv").stat().st_size > 0
    meta = json.loads((tmp_path / "metadata.json").read_text(encoding="utf-8"))
    assert meta["semilla"] == 3 and meta["n_clientes"] == 150
    assert "efecto de intervención" in " ".join(meta["supuestos_clave"]).lower() or "intervención" in " ".join(
        meta["supuestos_clave"]
    )


# ------------------------------------------------------------------ esquema e integridad
def test_columnas_coinciden_con_diccionario(t):
    for tabla, cols in g.DICCIONARIO.items():
        assert list(t[tabla].columns) == [c[0] for c in cols], tabla


def test_claves_unicas_y_foraneas(t):
    assert t["clientes"]["cliente_id"].is_unique
    assert t["creditos"]["credito_id"].is_unique
    assert t["verdad_terreno"]["credito_id"].is_unique
    assert not t["cuotas"].duplicated(["credito_id", "nro_cuota"]).any()
    assert not t["saldos_mensuales"].duplicated(["credito_id", "periodo"]).any()
    assert not t["senales_mensuales"].duplicated(["credito_id", "periodo"]).any()
    cre = set(t["creditos"]["credito_id"])
    for tabla in ("cuotas", "saldos_mensuales", "senales_mensuales", "gestiones", "verdad_terreno"):
        assert set(t[tabla]["credito_id"]) <= cre, tabla
    assert set(t["creditos"]["cliente_id"]) == set(t["clientes"]["cliente_id"])
    assert set(t["clientes"]["agencia_id"]) <= set(t["agencias"]["agencia_id"])
    assert set(t["clientes"]["analista_id"]) <= set(t["analistas"]["analista_id"])


def test_saldos_y_senales_alineados(t):
    a = t["saldos_mensuales"][["credito_id", "periodo"]].reset_index(drop=True)
    b = t["senales_mensuales"][["credito_id", "periodo"]].reset_index(drop=True)
    pd.testing.assert_frame_equal(a, b)


def test_sin_datos_personales(t):
    assert t["clientes"]["cliente_id"].str.fullmatch(r"CLI-\d{5}").all()
    assert t["creditos"]["credito_id"].str.fullmatch(r"CRE-\d{5}").all()
    assert t["analistas"]["analista_id"].str.fullmatch(r"ANA-\d{3}").all()
    prohibidas = re.compile(r"dni|telefono|celular|correo|email|direccion|apellido", re.I)
    for tabla, df in t.items():
        assert not [c for c in df.columns if prohibidas.search(c)], tabla
    assert t["agencias"]["nombre"].str.startswith("Sintética").all()


def test_rangos_plausibles(t):
    c = t["creditos"]
    assert c["monto_desembolsado"].between(800, 80000).all()
    assert c["plazo_meses"].isin(g.PLAZOS).all()
    assert c["tea"].between(0.20, 0.70).all()
    assert c["dia_vencimiento"].between(1, 28).all()
    assert 0.10 < c["cuota_ingreso_origen"].median() < 0.45
    assert c["cuota_ingreso_origen"].between(0.05, 0.60).all()
    assert set(t["clientes"]["sector"]) <= set(g.SECTORES)
    assert set(t["clientes"]["zona"]) == set(g.ZONAS)


# ------------------------------------------------------------------ sin fugas del futuro
def test_ninguna_fecha_supera_el_corte_final(t, cfg_grande):
    fin = cfg_grande.fin
    assert fin == pd.Timestamp("2026-10-31")
    q = t["cuotas"]
    assert q["fecha_vencimiento"].max() <= fin
    assert q["fecha_primer_pago"].dropna().max() <= fin
    assert q["fecha_cancelacion"].dropna().max() <= fin
    assert t["saldos_mensuales"]["fecha_corte"].max() <= fin
    assert t["senales_mensuales"]["fecha_corte"].max() <= fin
    assert t["gestiones"]["fecha"].max() <= fin
    v = t["verdad_terreno"]
    assert v["fecha_primer_atraso_30d"].dropna().max() <= fin


def test_pagos_coherentes(t):
    q = t["cuotas"]
    pagadas = q.dropna(subset=["fecha_cancelacion"])
    assert (pagadas["fecha_cancelacion"] >= pagadas["fecha_vencimiento"]).sum() >= (
        pagadas["dias_atraso_cancelacion"] == 0
    ).sum()
    esperado = (pagadas["fecha_cancelacion"] - pagadas["fecha_vencimiento"]).dt.days.clip(lower=0)
    assert (pagadas["dias_atraso_cancelacion"].astype(int) == esperado).all()
    con_primer = q.dropna(subset=["fecha_primer_pago", "fecha_cancelacion"])
    assert (con_primer["fecha_primer_pago"] <= con_primer["fecha_cancelacion"]).all()
    assert (q["monto_primer_pago"].dropna() <= q["monto_cuota"].loc[q["monto_primer_pago"].notna()] + 1e-6).all()
    assert q["dias_atraso_cancelacion"].dropna().ge(0).all()
    assert (q["dias_atraso_cancelacion"].isna() == q["fecha_cancelacion"].isna()).all()


def test_cancelaciones_en_orden(t):
    q = t["cuotas"].sort_values(["credito_id", "nro_cuota"])
    pagadas = q.dropna(subset=["fecha_cancelacion"])
    dif = pagadas.groupby("credito_id")["fecha_cancelacion"].diff().dropna()
    assert (dif >= pd.Timedelta(0)).all()


def test_dias_atraso_de_saldos_coinciden_con_cuotas(t):
    corte = pd.Timestamp("2025-12-31")
    s = t["saldos_mensuales"]
    s = s[s["fecha_corte"] == corte].set_index("credito_id")
    q = t["cuotas"]
    q = q[(q["fecha_vencimiento"] <= corte)]
    impaga = q[q["fecha_cancelacion"].isna() | (q["fecha_cancelacion"] > corte)]
    esperado = (corte - impaga.groupby("credito_id")["fecha_vencimiento"].min()).dt.days
    esperado = esperado.reindex(s.index).fillna(0).astype(int)
    assert (s["dias_atraso_corte"] == esperado).mean() > 0.995
    # calificación coherente con los tramos
    d = s["dias_atraso_corte"]
    assert (s.loc[d <= 8, "calificacion"] == "normal").all()
    assert (s.loc[(d > 8) & (d <= 30), "calificacion"] == "cpp").all()
    assert (s.loc[d > 120, "calificacion"] == "perdida").all()


def test_saldo_capital_no_crece(t):
    s = t["saldos_mensuales"].sort_values(["credito_id", "periodo"])
    dif = s.groupby("credito_id")["saldo_capital"].diff().dropna()
    assert (dif <= 1e-6).all()
    assert (s["saldo_capital"] > 0).all()
    assert (s["saldo_vencido"] >= 0).all()


def test_gestiones_son_reactivas(t):
    gs = t["gestiones"]
    assert set(gs["dias_atraso_al_gestionar"]) <= {5, 15, 30}
    assert set(gs["resultado"]) <= {"contactado_promesa_pago", "contactado_sin_compromiso", "no_contesta"}
    assert gs["gestion_id"].is_unique
    # nunca se gestiona antes del vencimiento + 5 días
    m = gs.merge(t["cuotas"][["credito_id", "fecha_vencimiento", "fecha_cancelacion"]], on="credito_id")
    m = m[(m["fecha"] - m["fecha_vencimiento"]).dt.days == m["dias_atraso_al_gestionar"]]
    assert len(m) >= len(gs)  # cada gestión corresponde a una cuota vencida


# ------------------------------------------------------------------ propiedades de las trayectorias
def test_mezcla_de_trayectorias(t, cfg_grande):
    real = t["verdad_terreno"]["trayectoria"].value_counts(normalize=True)
    for k, p in cfg_grande.mezcla.items():
        assert abs(real[k] - p) < 0.005, k


def test_prevalencia_global_plausible(t):
    v = t["verdad_terreno"]
    p30 = v["fecha_primer_atraso_30d"].notna().mean()
    p8 = v["fecha_primer_atraso_8d"].notna().mean()
    assert 0.04 < p30 < 0.14
    assert p30 < p8 < 0.30


def test_resultado_por_tipo_de_trayectoria(t):
    v = t["verdad_terreno"]
    p30 = v.groupby("trayectoria")["fecha_primer_atraso_30d"].apply(lambda x: x.notna().mean())
    p8 = v.groupby("trayectoria")["fecha_primer_atraso_8d"].apply(lambda x: x.notna().mean())
    assert p30["estable"] < 0.01
    assert p30["pagador_tardio"] < 0.01 and p8["pagador_tardio"] > 0.4  # trampa para reglas de «días de atraso»
    assert p30["deterioro_gradual"] > 0.6
    assert p30["shock_abrupto"] > 0.8
    assert 0.0 < p30["fluctuante"] < 0.10  # casi siempre se recupera: son los falsos positivos potenciales


def test_deterioro_gradual_anticipa_el_atraso(t):
    v = t["verdad_terreno"]
    gr = v[(v["trayectoria"] == "deterioro_gradual")].dropna(subset=["fecha_primer_atraso_8d"]).copy()
    gr["inicio"] = pd.to_datetime(gr["mes_inicio_deterioro"] + "-01")
    lead = (gr["fecha_primer_atraso_8d"] - gr["inicio"]).dt.days
    assert (lead > 0).mean() > 0.95  # alguna fluctuación normal previa puede dar un atraso aislado antes del inicio
    assert lead.median() >= 60  # hay ventana real para actuar antes del atraso
    sh = v[(v["trayectoria"] == "shock_abrupto")].dropna(subset=["fecha_primer_atraso_8d"]).copy()
    sh["inicio"] = pd.to_datetime(sh["mes_inicio_deterioro"] + "-01")
    lead_sh = (sh["fecha_primer_atraso_8d"] - sh["inicio"]).dt.days
    assert lead_sh.median() < lead.median()  # el shock da menos aviso que el deterioro gradual
    # solo gradual y shock tienen mes de inicio
    assert v.loc[~v["trayectoria"].isin(["deterioro_gradual", "shock_abrupto"]), "mes_inicio_deterioro"].isna().all()


def _ratio_abonos(t, ids, ventana=3):
    s = t["senales_mensuales"][t["senales_mensuales"]["credito_id"].isin(ids)].dropna(subset=["abonos_cuenta_mes"])
    s = s.sort_values(["credito_id", "periodo"])
    out = []
    for _, grp in s.groupby("credito_id"):
        a = grp["abonos_cuenta_mes"].to_numpy()
        if a.size >= 2 * ventana + 2:
            out.append(a[-ventana:].mean() / a[:ventana].mean())
    return np.array(out)


def test_senales_de_deterioro_caen_en_gradual_y_no_en_estable(t):
    v = t["verdad_terreno"]
    gr = v[(v["trayectoria"] == "deterioro_gradual") & v["fecha_primer_atraso_8d"].notna()]["credito_id"]
    es = v[v["trayectoria"] == "estable"]["credito_id"]
    r_gr, r_es = _ratio_abonos(t, set(gr)), _ratio_abonos(t, set(es))
    assert r_gr.size > 20 and r_es.size > 200
    assert np.median(r_gr) < 0.8
    assert np.median(r_es) > 0.85


def test_fluctuaciones_normales_imitan_caidas_pero_se_recuperan(t):
    """Los 'fluctuantes' tienen caídas transitorias de ingreso (falsos positivos potenciales)."""
    v = t["verdad_terreno"].set_index("credito_id")
    s = t["senales_mensuales"].dropna(subset=["abonos_cuenta_mes"]).copy()
    s["tray"] = s["credito_id"].map(v["trayectoria"])
    s = s[s["tray"].isin(["estable", "fluctuante"])]
    med = s.groupby("credito_id")["abonos_cuenta_mes"].transform("median")
    s["caida"] = s["abonos_cuenta_mes"] < 0.75 * med
    por_cliente = s.groupby("credito_id").agg(caida=("caida", "any"), tray=("tray", "first"))
    tasa = por_cliente.groupby("tray")["caida"].mean()
    assert tasa["fluctuante"] > tasa["estable"] + 0.08
    # la gran mayoría de las caídas de fluctuantes NO termina en atraso > 30 días
    fl = v[v["trayectoria"] == "fluctuante"]
    con_caida = por_cliente[(por_cliente.tray == "fluctuante") & por_cliente.caida].index
    assert fl.loc[fl.index.intersection(con_caida), "fecha_primer_atraso_30d"].isna().mean() > 0.9


def test_precursores_de_deuda_externa_y_consultas(t):
    v = t["verdad_terreno"].set_index("credito_id")
    s = t["senales_mensuales"].copy()
    s["tray"] = s["credito_id"].map(v["trayectoria"])
    s = s[s["tray"].isin(["estable", "deterioro_gradual"])]
    cons = s.groupby("tray")["consultas_otras_entidades_mes"].mean()
    assert cons["deterioro_gradual"] > cons["estable"] * 1.5


def test_datos_faltantes_controlados(t):
    cli = t["clientes"].set_index("cliente_id")
    s = t["senales_mensuales"].copy()
    s["cuenta"] = s["cliente_id"].map(cli["tiene_cuenta_ahorros"])
    assert s.loc[s["cuenta"] == 0, "abonos_cuenta_mes"].isna().all()
    falt = s.loc[s["cuenta"] == 1, "abonos_cuenta_mes"].isna().mean()
    assert 0.005 < falt < 0.04
    assert (s["n_operaciones_cuenta_mes"].dropna() >= 0).all()
    assert (s["deuda_otras_entidades"] >= 0).all()


# ------------------------------------------------------------------ sesgos (auditoría)
def test_variables_sensibles_independientes_del_resultado(t):
    v = t["verdad_terreno"].merge(t["clientes"], on="cliente_id")
    v["evento"] = v["fecha_primer_atraso_30d"].notna()
    por_sexo = v.groupby("sexo")["evento"].mean()
    assert abs(por_sexo["F"] - por_sexo["M"]) < 0.04
    por_edad = v.groupby("rango_edad")["evento"].mean()
    assert por_edad.max() - por_edad.min() < 0.08
    # el canal de contacto tampoco determina el deterioro
    por_canal = v.groupby("canal_preferido")["evento"].mean()
    assert por_canal.max() - por_canal.min() < 0.08
