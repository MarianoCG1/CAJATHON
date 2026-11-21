"""Auditoría de dificultad de los datos sintéticos de NEG-02 (herramienta de planificación).

La verdad de terreno de NEG-02 son reglas deterministas sobre la información completa. Por eso
detectar oportunidades con información completa es trivial *por construcción*. La pregunta útil es
cuánto se pierde cuando la Caja solo ve (A) sus propios datos o (B) lo que el cliente consintió.

Escenarios (mismas reglas, distinto nivel de visibilidad; ingreso estimado, no el real latente):
  A  solo datos de la Caja (E00)
  B  Caja + entidades con consentimiento VIGENTE a la Caja (finalidad OFERTA_PRODUCTOS), por alcance
  C  información completa observable (todas las entidades), con ingreso estimado

NO es el motor de oportunidades del reto: solo mide el techo y el piso del dataset.

Uso:
    python scripts/auditoria/auditar_neg02.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "retos" / "NEG-02" / "datos" / "sintetico"
CAJA = "E00"
# Umbrales: los mismos supuestos que usa el generador para definir la verdad.
RATIO_SOBRE, CONSOL_N, CONSOL_SALDO, CONSOL_TEA, CONSOL_RATIO = 0.50, 2, 4000.0, 40.0, 0.15
CAP_CREC, CAP_RATIO, AHORRO_SALDO, AHORRO_TEA, DOM_SHARE, ABONOS_MIN = 0.15, 0.35, 8000.0, 2.5, 0.30, 800.0
CREDITOS = ("CREDITO_MYPE", "CREDITO_CONSUMO", "CREDITO_CONSOLIDACION", "TARJETA_CREDITO")
RIESGO = ("DEFICIENTE", "DUDOSO", "PERDIDA")
MYPE = ("MYPE_COMERCIO", "MYPE_SERVICIOS", "MYPE_AGRO")
TIPOS = ["CONSOLIDACION_DEUDA", "CAPITAL_TRABAJO_MYPE", "CAPTACION_AHORRO", "DOMICILIACION_INGRESOS", "RESTRICCION_SOBREENDEUDAMIENTO"]


def cargar(datos: Path = DATOS) -> dict:
    return {
        "cli": pd.read_csv(datos / "clientes.csv"),
        "pro": pd.read_csv(datos / "productos_cliente.csv"),
        "tx": pd.read_csv(datos / "transacciones.csv", parse_dates=["fecha"]),
        "con": pd.read_csv(datos / "consentimientos.csv"),
        "alc": pd.read_csv(datos / "consentimiento_alcances.csv"),
        "ver": pd.read_csv(datos / "verdad" / "verdad_oportunidades.csv"),
    }


def _permisos(d: dict) -> pd.DataFrame:
    """(cliente, entidad_fuente, alcance) con consentimiento VIGENTE para la Caja y finalidad de oferta."""
    c = d["con"]
    c = c[(c["estado"] == "VIGENTE") & (c["entidad_receptora_id"] == CAJA) & (c["finalidad"] == "OFERTA_PRODUCTOS")]
    return c.merge(d["alc"], on="consentimiento_id")[["cliente_id", "entidad_fuente_id", "alcance"]].drop_duplicates()


def _visibles(d: dict, escenario: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    pro, tx = d["pro"].copy(), d["tx"].copy()
    if escenario == "C":
        return pro, tx
    if escenario == "A":
        return pro[pro["entidad_id"] == CAJA].copy(), tx[tx["entidad_id"] == CAJA].copy()
    perm = _permisos(d)
    # B: se ve todo lo de la Caja; lo externo, solo por alcance
    ext = pro[pro["entidad_id"] != CAJA].copy()
    for alc, cols in (("PRODUCTOS", ["categoria", "estado"]), ("SALDOS", ["saldo_actual_pen", "monto_original_pen"]),
                      ("CONDICIONES", ["tasa_ea_pct", "cuota_mensual_pen", "calificacion", "dias_atraso"])):
        p = perm[perm["alcance"] == alc][["cliente_id", "entidad_fuente_id"]].assign(_ok=True)
        ext = ext.merge(p, left_on=["cliente_id", "entidad_id"], right_on=["cliente_id", "entidad_fuente_id"], how="left").drop(columns="entidad_fuente_id")
        ext.loc[ext["_ok"].isna(), cols] = np.nan
        ext = ext.drop(columns="_ok")
    pt = perm[perm["alcance"] == "TRANSACCIONES"][["cliente_id", "entidad_fuente_id"]].assign(_ok=True)
    txe = tx[tx["entidad_id"] != CAJA].merge(pt, left_on=["cliente_id", "entidad_id"], right_on=["cliente_id", "entidad_fuente_id"], how="left")
    txe = txe[txe["_ok"].notna()].drop(columns=["entidad_fuente_id", "_ok"])
    # categoría desconocida (sin PRODUCTOS) se descarta: no se sabe qué producto es
    ext = ext[ext["categoria"].notna()]
    return pd.concat([pro[pro["entidad_id"] == CAJA], ext]), pd.concat([tx[tx["entidad_id"] == CAJA], txe])


def reglas(d: dict, escenario: str) -> pd.DataFrame:
    cli = d["cli"].set_index("cliente_id")
    pro, tx = _visibles(d, escenario)
    act = pro[pro["estado"].fillna("ACTIVO") != "CANCELADO"]
    cred = act[act["categoria"].isin(CREDITOS)]
    ext_c = cred[cred["entidad_id"] != CAJA]
    ab = tx[tx["tipo"].str.startswith("ABONO")]
    meses = 6.0
    s = pd.DataFrame(index=cli.index)
    s["abonos_prom"] = ab.groupby("cliente_id")["monto_pen"].sum().reindex(s.index).fillna(0) / meses
    # ingreso estimado: lo declarado a la Caja; si no hay, el flujo de abonos visible
    s["ingreso"] = cli["ingreso_declarado_caja_pen"].where(cli["ingreso_declarado_caja_pen"] > 0)
    s["ingreso"] = s["ingreso"].fillna(s["abonos_prom"].replace(0, np.nan))
    s["cuota"] = cred.groupby("cliente_id")["cuota_mensual_pen"].sum().reindex(s.index).fillna(0)
    s["ratio"] = s["cuota"] / s["ingreso"]
    riesgo = cred[cred["calificacion"].isin(RIESGO)].groupby("cliente_id").size().reindex(s.index).fillna(0) > 0
    s["n_ext"] = ext_c.groupby("cliente_id").size().reindex(s.index).fillna(0)
    s["saldo_ext"] = ext_c.groupby("cliente_id")["saldo_actual_pen"].sum().reindex(s.index).fillna(0)
    s["tea_ext"] = ext_c.groupby("cliente_id")["tasa_ea_pct"].max().reindex(s.index).fillna(0)
    aho = act[(act["categoria"] == "CUENTA_AHORRO") & (act["entidad_id"] != CAJA) & (act["tasa_ea_pct"] <= AHORRO_TEA)]
    s["ahorro_ext"] = aho.groupby("cliente_id")["saldo_actual_pen"].sum().reindex(s.index).fillna(0)
    mitad = pd.Timestamp("2026-08-01")
    i = ab[ab["fecha"] < mitad].groupby("cliente_id")["monto_pen"].sum().reindex(s.index)
    f = ab[ab["fecha"] >= mitad].groupby("cliente_id")["monto_pen"].sum().reindex(s.index)
    s["crec"] = (f / i - 1).where(i > 0)
    tot = ab.groupby("cliente_id")["monto_pen"].sum().reindex(s.index)
    caja = ab[ab["entidad_id"] == CAJA].groupby("cliente_id")["monto_pen"].sum().reindex(s.index).fillna(0)
    s["share_caja"] = (caja / tot).where(tot > 0)
    restr = (s["ratio"] > RATIO_SOBRE) | riesgo
    flujo = s["abonos_prom"] >= ABONOS_MIN
    es_caja = cli["es_cliente_caja"].astype(bool)
    out = pd.DataFrame({
        "CONSOLIDACION_DEUDA": (~restr) & (s["n_ext"] >= CONSOL_N) & (s["saldo_ext"] >= CONSOL_SALDO) & (s["tea_ext"] >= CONSOL_TEA) & (s["ratio"] >= CONSOL_RATIO),
        "CAPITAL_TRABAJO_MYPE": (~restr) & cli["segmento"].isin(MYPE) & flujo & (s["crec"].fillna(-1) >= CAP_CREC) & (s["ratio"].fillna(0) < CAP_RATIO),
        "CAPTACION_AHORRO": s["ahorro_ext"] >= AHORRO_SALDO,
        "DOMICILIACION_INGRESOS": es_caja & flujo & (s["share_caja"].fillna(1) < DOM_SHARE),
        "RESTRICCION_SOBREENDEUDAMIENTO": restr,
    })
    return out.astype(int)


def auditar(datos: Path = DATOS) -> pd.DataFrame:
    d = cargar(datos)
    ver = d["ver"].pivot(index="cliente_id", columns="tipo_oportunidad", values="existe")
    filas = []
    for esc in ("A", "B", "C"):
        pred = reglas(d, esc).reindex(ver.index).fillna(0)
        for t in TIPOS:
            y, p = ver[t].astype(bool), pred[t].astype(bool)
            tp = int((y & p).sum())
            filas.append({"escenario": esc, "tipo": t, "existen": int(y.sum()),
                          "recall": tp / max(1, int(y.sum())), "precision": tp / max(1, int(p.sum())) if p.sum() else float("nan")})
    return pd.DataFrame(filas)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    r = auditar()
    print(r.pivot(index="tipo", columns="escenario", values="recall").round(2).to_string())
    print()
    print(r.pivot(index="tipo", columns="escenario", values="precision").round(2).to_string())
    print()
    print("recall global:", {e: round(float((g.recall * g.existen).sum() / g.existen.sum()), 3) for e, g in r.groupby("escenario")})
