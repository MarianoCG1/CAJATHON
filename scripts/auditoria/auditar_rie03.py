"""Auditoría de trivialidad de los datos sintéticos de RIE-03 (herramienta de planificación).

Pregunta: ¿se puede predecir el atraso > 30 d en los próximos 60 d con una regla simple
o con una sola variable? Si sí, el backtest del reto no demostraría nada.

NO es el modelo del reto ni se reutiliza en la solución: solo mide la dificultad del dataset.
Etiqueta, corte y población se definen aquí, solo con información disponible al corte.

Uso:
    python scripts/auditoria/auditar_rie03.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "retos" / "RIE-03" / "datos" / "sintetico"
HORIZONTE_DIAS = 60


def construir(datos: Path = DATOS) -> pd.DataFrame:
    s = pd.read_csv(datos / "saldos_mensuales.csv", parse_dates=["fecha_corte"])
    g = pd.read_csv(datos / "senales_mensuales.csv")
    cr = pd.read_csv(datos / "creditos.csv", usecols=["credito_id", "cuota_ingreso_origen", "monto_desembolsado", "plazo_meses"])
    cl = pd.read_csv(datos / "clientes.csv", usecols=["cliente_id", "antiguedad_cliente_meses", "n_creditos_previos", "tiene_billetera_digital"])
    v = pd.read_csv(datos / "verdad_terreno.csv", parse_dates=["fecha_primer_atraso_30d"])
    df = s.merge(g.drop(columns=["fecha_corte"]), on=["credito_id", "periodo"]).merge(cr, on="credito_id")
    df = df.merge(cl, on="cliente_id").merge(v[["credito_id", "trayectoria", "fecha_primer_atraso_30d"]], on="credito_id")
    df = df.sort_values(["credito_id", "periodo"]).reset_index(drop=True)
    gb = df.groupby("credito_id")
    # historia de señales (solo pasado)
    for col in ["abonos_cuenta_mes", "n_operaciones_cuenta_mes", "saldo_promedio_cuenta_mes", "cobros_digitales_mes"]:
        media3 = gb[col].transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean())
        df[f"{col}_rel3"] = df[col] / media3.replace(0, np.nan)
    df["consultas_3m"] = gb["consultas_otras_entidades_mes"].transform(lambda x: x.rolling(3, min_periods=1).sum())
    df["deuda_otras_delta3"] = df["deuda_otras_entidades"] - gb["deuda_otras_entidades"].shift(3)
    df["atraso_max_3m"] = gb["dias_atraso_corte"].transform(lambda x: x.rolling(3, min_periods=1).max())
    df["atraso_prev"] = gb["dias_atraso_corte"].shift(1)
    # etiqueta: primer atraso > 30 d dentro de los próximos 60 d, sin haberlo tenido antes
    f30 = df["fecha_primer_atraso_30d"]
    df["y"] = ((f30 > df["fecha_corte"]) & (f30 <= df["fecha_corte"] + pd.Timedelta(days=HORIZONTE_DIAS))).astype(int)
    df["ya_30d"] = (f30.notna() & (f30 <= df["fecha_corte"]))
    return df


FEATURES = [
    "dias_atraso_corte", "atraso_max_3m", "atraso_prev", "saldo_vencido",
    "abonos_cuenta_mes_rel3", "n_operaciones_cuenta_mes_rel3", "saldo_promedio_cuenta_mes_rel3",
    "cobros_digitales_mes_rel3", "consultas_3m", "deuda_otras_delta3", "n_entidades_con_deuda",
    "cuota_ingreso_origen", "antiguedad_cliente_meses", "n_creditos_previos",
]


def _prec_at(y, score, frac=0.10):
    k = max(1, int(len(y) * frac))
    idx = np.argsort(-np.asarray(score))[:k]
    return float(np.asarray(y)[idx].mean())


def auditar(datos: Path = DATOS) -> dict:
    df = construir(datos)
    # población: sin atraso > 30 d previo y con horizonte observado completo
    df = df[~df["ya_30d"]]
    df = df[df["fecha_corte"] <= pd.Timestamp("2026-08-31")]
    entreno = df[df["fecha_corte"] <= "2025-06-30"]
    prueba = df[(df["fecha_corte"] >= "2026-01-31")]  # hueco de purga ≥ horizonte
    # regla simple: ya tiene algún atraso hoy (0 d = sin señal)
    out = {"n_prueba": int(len(prueba)), "prevalencia_prueba": float(prueba["y"].mean())}
    out["regla_atraso_actual_auc"] = float(roc_auc_score(prueba["y"], prueba["dias_atraso_corte"]))
    out["regla_atraso_actual_prec_top10"] = _prec_at(prueba["y"], prueba["dias_atraso_corte"])
    # mejor variable individual
    mejores = {}
    for c in FEATURES:
        x = prueba[c].fillna(prueba[c].median())
        a = roc_auc_score(prueba["y"], x)
        mejores[c] = max(a, 1 - a)
    out["auc_por_variable"] = dict(sorted(mejores.items(), key=lambda kv: -kv[1]))
    # modelo lineal y de árboles con todas las variables
    Xe, Xp = entreno[FEATURES].fillna(0), prueba[FEATURES].fillna(0)
    lr = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500)).fit(Xe, entreno["y"])
    gbm = HistGradientBoostingClassifier(max_iter=150, random_state=0).fit(Xe, entreno["y"])
    for nombre, m in (("logistica", lr), ("arboles", gbm)):
        p = m.predict_proba(Xp)[:, 1]
        out[f"{nombre}_auc"] = float(roc_auc_score(prueba["y"], p))
        out[f"{nombre}_prec_top10"] = _prec_at(prueba["y"], p)
    # solo señales de alerta temprana (sin mirar el atraso actual): ¿hay anticipación real?
    solo = [c for c in FEATURES if "atraso" not in c and c != "saldo_vencido"]
    g2 = HistGradientBoostingClassifier(max_iter=150, random_state=0).fit(entreno[solo].fillna(0), entreno["y"])
    p2 = g2.predict_proba(prueba[solo].fillna(0))[:, 1]
    out["arboles_sin_atraso_auc"] = float(roc_auc_score(prueba["y"], p2))
    out["arboles_sin_atraso_prec_top10"] = _prec_at(prueba["y"], p2)
    # restringido a quienes hoy están al día (el caso que importa: anticipar antes del atraso)
    aldia = prueba["dias_atraso_corte"] <= 0
    out["n_al_dia"] = int(aldia.sum())
    out["prevalencia_al_dia"] = float(prueba.loc[aldia, "y"].mean())
    pa = gbm.predict_proba(Xp[aldia.values])[:, 1]
    out["arboles_al_dia_auc"] = float(roc_auc_score(prueba.loc[aldia, "y"], pa))
    out["arboles_al_dia_prec_top10"] = _prec_at(prueba.loc[aldia, "y"], pa)
    pb = g2.predict_proba(prueba.loc[aldia, solo].fillna(0))[:, 1]
    out["arboles_sin_atraso_al_dia_auc"] = float(roc_auc_score(prueba.loc[aldia, "y"], pb))
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = auditar()
    for k, v in r.items():
        if isinstance(v, dict):
            print(k)
            for kk, vv in list(v.items())[:8]:
                print(f"   {kk:34s} {vv:.3f}")
        else:
            print(f"{k:34s} {v:.3f}" if isinstance(v, float) else f"{k:34s} {v}")
