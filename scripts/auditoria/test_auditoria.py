"""Pruebas de las auditorías de dificultad de datos.

Dejan constancia de que los datasets sintéticos no son triviales: si alguien cambia un generador
y una regla simple pasa a resolver el backtest, estas pruebas lo avisan. Se omiten si los datos
no están generados (`python retos/<ID>/datos/generar.py`).
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import auditar_neg02 as neg02
import auditar_rie01 as rie01
import auditar_rie03 as rie03

sin_rie03 = pytest.mark.skipif(not (rie03.DATOS / "verdad_terreno.csv").exists(), reason="faltan datos de RIE-03")
sin_neg02 = pytest.mark.skipif(not (neg02.DATOS / "verdad" / "verdad_oportunidades.csv").exists(), reason="faltan datos de NEG-02")
sin_rie01 = pytest.mark.skipif(not (rie01.DATOS / "backtest" / "impacto_backtest.csv").exists(), reason="faltan datos de RIE-01")


@sin_rie03
def test_rie03_ninguna_variable_ni_la_regla_de_atraso_resuelven_el_problema():
    r = rie03.auditar()
    assert max(r["auc_por_variable"].values()) < 0.92
    assert r["regla_atraso_actual_auc"] < 0.90
    # hay señal real entre quienes hoy están al día (el caso que importa) y no es perfecta
    assert 0.70 < r["arboles_al_dia_auc"] < 0.97
    # las señales de alerta temprana aportan sobre mirar solo el atraso
    assert r["arboles_sin_atraso_auc"] > r["regla_atraso_actual_auc"] + 0.05


@sin_neg02
def test_neg02_el_consentimiento_limita_lo_que_se_puede_detectar():
    r = neg02.auditar()
    rec = {e: float((g.recall * g.existen).sum() / g.existen.sum()) for e, g in r.groupby("escenario")}
    assert rec["A"] < 0.30  # solo con datos de la Caja se detecta poco
    assert rec["A"] < rec["B"] < rec["C"]
    assert rec["C"] > 0.85  # con información completa las reglas casi lo resuelven: por construcción


@sin_rie01
def test_rie01_una_formula_de_pocos_factores_no_alcanza_para_ganar():
    r = rie01.auditar()
    assert r["auc_reglas"]["amenaza × sensibilidad × intensidad"] < 0.80
    cap = r["captura_incumplimiento_con_2_semanas_de_visitas"]
    assert cap["regla f_3"] > cap["azar"] * 1.5  # hay señal para priorizar
    assert cap["arboles"] >= cap["regla f_3"] - 0.01
