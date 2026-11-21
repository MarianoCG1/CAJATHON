"""Auditoría de trivialidad de los datos sintéticos de RIE-01 (herramienta de planificación).

Pregunta: ¿una fórmula de pocos factores observables (amenaza del distrito × sensibilidad de la
actividad × intensidad del escenario) ya predice casi todo el incumplimiento? Si sí, el backtest
no distinguiría una solución buena de una trivial.

Se entrena solo con `impacto_historico` y se mide en `backtest/` (verdad oculta). No es el modelo
de exposición del reto: solo mide la dificultad del dataset.

Uso:
    python scripts/auditoria/auditar_rie01.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "retos" / "RIE-01" / "datos" / "sintetico"
CAPACIDAD_SEMANAL = 492  # visitas/semana de todas las agencias (agencias.csv)


def _base(d: Path) -> dict:
    cli = pd.read_csv(d / "clientes.csv")
    cred = pd.read_csv(d / "creditos.csv")
    agg = cred.groupby("cliente_id").agg(saldo=("saldo_soles", "sum"), cuota=("cuota_mensual_soles", "sum"),
                                         atraso=("dias_atraso", "max")).reset_index()
    cli = cli.merge(agg, on="cliente_id", how="left").fillna({"saldo": 0, "cuota": 0, "atraso": 0})
    cli = cli.merge(pd.read_csv(d / "sectores.csv")[["sector_id", "dist_cauce_km", "pendiente_pct", "altitud_m"]], on="sector_id", how="left")
    cli = cli.merge(pd.read_csv(d / "distritos.csv")[["distrito_id", "zona"]], on="distrito_id", how="left")
    cli = cli.merge(pd.read_csv(d / "actividades.csv"), on="actividad_id", how="left")
    cli["ratio_cuota"] = cli["cuota"] / cli["ingreso_mensual_soles"].replace(0, np.nan)
    return {"cli": cli, "mapa": pd.read_csv(d / "mapa_amenaza.csv"),
            "hist_ev": pd.read_csv(d / "eventos_historicos.csv"), "hist": pd.read_csv(d / "impacto_historico.csv"),
            "bt_ev": pd.read_csv(d / "backtest" / "eventos_backtest.csv"), "bt": pd.read_csv(d / "backtest" / "impacto_backtest.csv"),
            "esc": pd.read_csv(d / "escenarios.csv")}


def _filas(b: dict, eventos: pd.DataFrame, impacto: pd.DataFrame, nominal: bool) -> pd.DataFrame:
    """Une cliente × evento con las variables conocidas ANTES del evento."""
    cli, mapa = b["cli"], b["mapa"]
    ev = eventos.copy()
    if nominal:  # backtest: se usa la intensidad nominal del escenario, no la realizada
        e = b["esc"].set_index("escenario_id")
        for z in ("costa", "sierra", "selva_alta"):
            ev[f"intensidad_{z}"] = ev["escenario_id"].map(e[f"intensidad_{z}"])
    df = impacto[["evento_id", "cliente_id", "incumple_30d", "afectado"]].merge(ev[["evento_id", "tipo_amenaza", "intensidad_costa", "intensidad_sierra", "intensidad_selva_alta"]], on="evento_id")
    df = df.merge(cli, on="cliente_id", how="left")
    df = df.merge(mapa[["distrito_id", "tipo_amenaza", "indice"]], on=["distrito_id", "tipo_amenaza"], how="left")
    df["intensidad_zona"] = np.select([df["zona"] == "costa", df["zona"] == "sierra"],
                                      [df["intensidad_costa"], df["intensidad_sierra"]], df["intensidad_selva_alta"])
    sens = {"lluvia_intensa": "sens_lluvia_intensa", "inundacion": "sens_inundacion", "sequia": "sens_sequia"}
    df["sensibilidad"] = [r[sens[t]] for r, t in zip(df[list(sens.values())].to_dict("records"), df["tipo_amenaza"])]
    df["f_amenaza"] = df["indice"]
    df["f_2"] = df["indice"] * df["sensibilidad"]
    df["f_3"] = df["f_2"] * df["intensidad_zona"]
    df["tipo_cod"] = df["tipo_amenaza"].astype("category").cat.codes
    return df


FEATURES = ["indice", "sensibilidad", "intensidad_zona", "f_3", "meses_reserva", "tiene_seguro", "tiene_ingreso_secundario",
            "antiguedad_meses", "ingreso_mensual_soles", "saldo", "ratio_cuota", "atraso", "dist_cauce_km", "pendiente_pct",
            "altitud_m", "tipo_cod"]


def _capt(df: pd.DataFrame, score: np.ndarray, k: int) -> float:
    """Fracción de los incumplimientos del evento que caen entre los k clientes mejor puntuados."""
    idx = np.argsort(-score)[:k]
    return float(df["incumple_30d"].values[idx].sum() / max(1, df["incumple_30d"].sum()))


def auditar(datos: Path = DATOS) -> dict:
    b = _base(datos)
    ent = _filas(b, b["hist_ev"], b["hist"], nominal=False)
    pru = _filas(b, b["bt_ev"], b["bt"], nominal=True)
    out = {"n_prueba": int(len(pru)), "prevalencia_incumple": float(pru["incumple_30d"].mean())}
    aucs = {}
    for nombre, col in (("solo amenaza del distrito", "f_amenaza"), ("amenaza × sensibilidad", "f_2"), ("amenaza × sensibilidad × intensidad", "f_3"),
                        ("solo meses de reserva (invertido)", "meses_reserva")):
        x = pru[col].fillna(pru[col].median())
        a = roc_auc_score(pru["incumple_30d"], x)
        aucs[nombre] = a if col != "meses_reserva" else 1 - a
    out["auc_reglas"] = aucs
    m = HistGradientBoostingClassifier(max_iter=200, random_state=0).fit(ent[FEATURES], ent["incumple_30d"])
    pru["p"] = m.predict_proba(pru[FEATURES])[:, 1]
    out["auc_arboles"] = float(roc_auc_score(pru["incumple_30d"], pru["p"]))
    # captura con capacidad de 2 semanas de visitas (≈ 8 % de la cartera) por evento
    k = 2 * CAPACIDAD_SEMANAL
    caps = {"azar": [], "regla f_3": [], "arboles": [], "orden perfecto": []}
    rng = np.random.default_rng(0)
    for _, g in pru.groupby("evento_id"):
        caps["azar"].append(_capt(g, rng.random(len(g)), k))
        caps["regla f_3"].append(_capt(g, g["f_3"].fillna(0).values, k))
        caps["arboles"].append(_capt(g, g["p"].values, k))
        caps["orden perfecto"].append(_capt(g, g["incumple_30d"].values + rng.random(len(g)) * 1e-6, k))
    out["captura_incumplimiento_con_2_semanas_de_visitas"] = {n: float(np.mean(v)) for n, v in caps.items()}
    # techo: fórmula con la susceptibilidad REAL del sector (verdad oculta, solo para medir el margen)
    v = pd.read_csv(datos / "backtest" / "verdad_amenaza_sector.csv")
    pru = pru.merge(v, on=["sector_id", "tipo_amenaza"], how="left")
    pru["f_oraculo"] = pru["susceptibilidad_real"] * pru["sensibilidad"] * pru["intensidad_zona"]
    out["auc_oraculo_susceptibilidad_real"] = float(roc_auc_score(pru["incumple_30d"], pru["f_oraculo"].fillna(0)))
    out["captura_oraculo_2_semanas"] = float(np.mean([_capt(g, g["f_oraculo"].fillna(0).values, k) for _, g in pru.groupby("evento_id")]))
    # concentración: ¿pocos distritos explican todo?
    top = pru.groupby("distrito_id")["incumple_30d"].sum().sort_values(ascending=False)
    out["share_incumple_en_top5_distritos"] = float(top.head(5).sum() / top.sum())
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = auditar()
    for k, v in r.items():
        if isinstance(v, dict):
            print(k)
            for kk, vv in v.items():
                print(f"   {kk:40s} {vv:.3f}")
        else:
            print(f"{k:50s} {v:.3f}" if isinstance(v, float) else f"{k:50s} {v}")
