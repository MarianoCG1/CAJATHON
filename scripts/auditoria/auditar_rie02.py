"""Auditoría de trivialidad de los datos sintéticos de RIE-02 (herramienta de planificación).

Pregunta: ¿una regla simple de coincidencias (teléfono, dispositivo, dirección, referencias) detecta
las redes de fraude sin disparar sobre los señuelos legítimos (familias, mercados, tabletas de agencia,
gremios, gestores)? Si sí, el backtest no distinguiría una solución buena de una trivial.

Se evalúa a nivel de solicitud contra `etiquetas_solicitudes.csv` (fraude / legítima_señuelo / normal) y
a nivel de red contra `redes_verdad.csv`. No es el detector del reto.

Uso:
    python scripts/auditoria/auditar_rie02.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "retos" / "RIE-02" / "datos" / "sintetico"


def construir(datos: Path = DATOS) -> pd.DataFrame:
    s = pd.read_csv(datos / "solicitudes.csv", parse_dates=["fecha_solicitud"])
    e = pd.read_csv(datos / "etiquetas_solicitudes.csv")
    neg = pd.read_csv(datos / "negocios.csv")[["negocio_id", "direccion_id"]].rename(columns={"direccion_id": "direccion_negocio_id"})
    ref = pd.read_csv(datos / "referencias.csv")
    df = s.merge(e, on="solicitud_id").merge(neg, on="negocio_id", how="left")
    # vínculos por recurso: cuántas OTRAS solicitudes comparten el valor
    for col in ("telefono_id", "dispositivo_id", "direccion_domicilio_id", "direccion_negocio_id"):
        df[f"comp_{col}"] = df.groupby(col)["solicitud_id"].transform("count") - 1
    # referencias: el mismo teléfono de referencia aparece en otras solicitudes
    ref_tel = ref.groupby("telefono_referencia_id")["solicitud_id"].nunique()
    ref = ref.assign(n=ref["telefono_referencia_id"].map(ref_tel) - 1)
    df["comp_referencia"] = df["solicitud_id"].map(ref.groupby("solicitud_id")["n"].max()).fillna(0)
    # referencia a un solicitante de otra solicitud (cadena de referencias)
    sol_persona = s.set_index("solicitante_id")["solicitud_id"]
    ref["ref_es_solicitante"] = ref["persona_referencia_id"].isin(sol_persona.index).astype(int)
    df["ref_a_solicitante"] = df["solicitud_id"].map(ref.groupby("solicitud_id")["ref_es_solicitante"].max()).fillna(0)
    cols = ["comp_telefono_id", "comp_dispositivo_id", "comp_direccion_domicilio_id", "comp_direccion_negocio_id", "comp_referencia"]
    df["n_tipos"] = (df[cols] > 0).sum(axis=1)
    df["es_fraude"] = (df["etiqueta"] == "fraude").astype(int)
    df["es_senuelo"] = (df["etiqueta"] == "legitima_senuelo").astype(int)
    return df


def _medidas(df: pd.DataFrame, flag: pd.Series) -> dict:
    fr, se, no = df["es_fraude"] == 1, df["es_senuelo"] == 1, df["etiqueta"] == "normal"
    tp = int((flag & fr).sum())
    return {"recall_fraude": tp / max(1, int(fr.sum())),
            "precision": tp / max(1, int(flag.sum())),
            "senuelos_marcados": float((flag & se).sum() / max(1, int(se.sum()))),
            "normales_marcadas": float((flag & no).sum() / max(1, int(no.sum()))),
            "n_marcadas": int(flag.sum())}


def auditar(datos: Path = DATOS) -> dict:
    df = construir(datos)
    ev = df[df["particion"] == "eval"]
    reglas = {
        "R1 comparte algún recurso": ev["n_tipos"] >= 1,
        "R2 comparte teléfono": ev["comp_telefono_id"] > 0,
        "R3 comparte dispositivo": ev["comp_dispositivo_id"] > 0,
        "R4 comparte dos o más tipos de recurso": ev["n_tipos"] >= 2,
        "R5 dos tipos y referencia a otro solicitante": (ev["n_tipos"] >= 2) & (ev["ref_a_solicitante"] > 0),
    }
    out = {"n_eval": int(len(ev)), "fraude_eval": int(ev["es_fraude"].sum()), "senuelos_eval": int(ev["es_senuelo"].sum()),
           "reglas": {k: _medidas(ev, v) for k, v in reglas.items()}}
    # a nivel de red: ¿cuántas redes de fraude (por dificultad) tienen al menos una solicitud marcada por R4?
    redes = pd.read_csv(datos / "redes_verdad.csv")
    r4 = ev[reglas["R4 comparte dos o más tipos de recurso"]]
    por_red = ev[ev["es_fraude"] == 1].assign(m=lambda d: d.index.isin(r4.index)).groupby("red_id")["m"].mean()
    redes = redes[(redes["clase"] == "fraude") & (redes["particion"] == "eval")].merge(por_red.rename("share_marcada"), left_on="red_id", right_index=True, how="left")
    out["fraude_por_dificultad"] = redes.groupby("dificultad")["share_marcada"].mean().round(3).to_dict()
    return out


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = auditar()
    print({k: v for k, v in r.items() if k not in ("reglas",)})
    for k, v in r["reglas"].items():
        print(f"{k:48s} recall {v['recall_fraude']:.2f}  precisión {v['precision']:.2f}  señuelos {v['senuelos_marcados']:.2f}  normales {v['normales_marcadas']:.2f}  n={v['n_marcadas']}")
