#!/usr/bin/env python
"""Auditoría de COM-01: ¿aporta algo aprender de las visitas, o basta un ranking?

Experimento mínimo sobre el territorio sintético (retos/COM-01/datos/generar.py). Compara,
con el mismo presupuesto de visitas y el mismo historial:

  habitual : se visita donde ya hay clientes (costumbre y referidos, simplificado).
  ranking  : un puntaje fijo por zona (modelo con datos públicos + historial); se recorren
             las mejores zonas sin volver a aprender.
  aprende  : parte del mismo puntaje, actualiza lo que sabe tras cada semana (muestreo de
             Thompson) y reserva una cuota para las zonas de las que menos se sabe.
  mixto    : complemento, no reemplazo: cada semana reparte las salidas entre la costumbre
             (habitual) y el descubrimiento (aprende) según lo que va rindiendo cada una,
             con un mínimo del 20 % para cada fuente.
  techo    : conoce la verdad de terreno (inalcanzable; sirve de referencia).

No es la solución: no planifica rutas, no tiene agente, API ni interfaz, y no se reutiliza
en el evento. Sirve para saber si el problema es trivial y en qué condiciones el enfoque
NO gana. Los resultados dependen de los supuestos del generador.

Uso: python scripts/auditoria/auditar_com01.py [--semillas 100]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

RAIZ = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("generar_com01", RAIZ / "retos/COM-01/datos/generar.py")
gen = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = gen
_spec.loader.exec_module(gen)

SEMANAS = 12
SALIDAS_POR_SEMANA = 15  # salidas de campo a una zona (supuesto)
VISITAS_POR_SALIDA = 10  # (supuesto)
CUOTA_EXPLORAR = 0.2
FUERZA_PREVIA = 30.0  # cuántas visitas «vale» el puntaje inicial


def puntaje_inicial(zonas: pd.DataFrame, historial: pd.DataFrame) -> np.ndarray:
    """Conversión estimada por zona con datos públicos y el historial (sesgado) de visitas."""
    X = pd.DataFrame({
        "negocios": np.log1p(zonas["negocios_estimados"]),
        "actividad": zonas["actividad_comercial"],
        "cobertura": zonas["puntos_financieros_x100neg"],
        "digital": zonas["presencia_digital"].fillna(zonas["presencia_digital"].median()),
        "sin_dato_digital": zonas["presencia_digital"].isna().astype(float),
        "km": zonas["km_agencia"],
    })
    X = (X - X.mean()) / (X.std() + 1e-9)
    exitos = historial["clientes_nuevos"].to_numpy()
    fallos = historial["visitas"].to_numpy() - exitos
    Xx = np.vstack([X.to_numpy(), X.to_numpy()])
    y = np.r_[np.ones(len(X)), np.zeros(len(X))]
    w = np.r_[exitos, fallos].astype(float)
    m = LogisticRegression(C=1.0, max_iter=2000).fit(Xx[w > 0], y[w > 0], sample_weight=w[w > 0])
    return m.predict_proba(X.to_numpy())[:, 1]


def simular(tablas: dict, politica: str, rng: np.random.Generator) -> dict:
    zonas, historial, verdad = tablas["zonas"], tablas["historial"], tablas["verdad"]
    n = len(zonas)
    p = verdad["conversion_real"].to_numpy()
    pool = verdad["prospectos_disponibles"].to_numpy().astype(float)
    clientes = zonas["clientes_actuales"].to_numpy().astype(float)
    score = puntaje_inicial(zonas, historial)

    # posterior Beta: puntaje inicial como creencia previa + historial de la propia zona
    alfa = score * FUERZA_PREVIA + historial["clientes_nuevos"].to_numpy()
    beta = (1 - score) * FUERZA_PREVIA + (historial["visitas"] - historial["clientes_nuevos"]).to_numpy()

    quedan = pool.copy()
    visitas = np.zeros(n)
    total = 0
    habitual_p = (clientes + 1.0) ** 1.2
    habitual_p /= habitual_p.sum()
    mejores = np.argsort(-score)[: SALIDAS_POR_SEMANA * 3]  # el ranking rota entre sus 45 mejores
    cursor = 0

    rinde = {"habitual": [1.0, 1.0], "aprende": [1.0, 1.0]}  # [nuevos+1, sin resultado+1]

    def elegir_aprende(k: int) -> np.ndarray:
        n_explorar = int(round(k * CUOTA_EXPLORAR))
        muestra = rng.beta(alfa, beta) * (quedan / pool)
        elegidas = list(np.argsort(-muestra)[: k - n_explorar])
        # cuota para lo que menos se conoce (menos visitas acumuladas), al azar entre empates
        orden = np.lexsort((rng.random(n), historial["visitas"].to_numpy() + visitas))
        elegidas += [z for z in orden if z not in elegidas][:n_explorar]
        return np.array(elegidas, dtype=int)

    for _ in range(SEMANAS):
        origen = None
        if politica == "mixto":
            minimo = int(round(SALIDAS_POR_SEMANA * 0.2))
            tasas = {f: rng.beta(*rinde[f], size=SALIDAS_POR_SEMANA) for f in rinde}
            n_hab = int((tasas["habitual"] > tasas["aprende"]).sum())
            n_hab = int(np.clip(n_hab, minimo, SALIDAS_POR_SEMANA - minimo))
            desc = elegir_aprende(SALIDAS_POR_SEMANA - n_hab)
            peso = habitual_p.copy()
            peso[desc] = 0
            hab = rng.choice(n, n_hab, replace=False, p=peso / peso.sum())
            elegidas = np.r_[hab, desc]
            origen = ["habitual"] * n_hab + ["aprende"] * len(desc)
        elif politica == "habitual":
            elegidas = rng.choice(n, SALIDAS_POR_SEMANA, replace=False, p=habitual_p)
        elif politica == "ranking":
            elegidas = mejores[(cursor + np.arange(SALIDAS_POR_SEMANA)) % len(mejores)]
            cursor += SALIDAS_POR_SEMANA
        elif politica == "techo":
            elegidas = np.argsort(-p * quedan / pool)[:SALIDAS_POR_SEMANA]
        elif politica == "aprende":
            elegidas = elegir_aprende(SALIDAS_POR_SEMANA)
        else:
            raise ValueError(politica)

        for i, z in enumerate(elegidas):
            prob = p[z] * quedan[z] / pool[z]  # la zona se agota al visitarla
            nuevos = rng.binomial(VISITAS_POR_SALIDA, prob)
            quedan[z] = max(quedan[z] - nuevos, 0)
            visitas[z] += VISITAS_POR_SALIDA
            alfa[z] += nuevos
            beta[z] += VISITAS_POR_SALIDA - nuevos
            total += nuevos
            if origen is not None:
                rinde[origen[i]][0] += nuevos
                rinde[origen[i]][1] += VISITAS_POR_SALIDA - nuevos

    # zonas «ocultas»: alto potencial real y poca cartera actual
    ocultas = (p >= np.quantile(p, 0.75)) & (clientes <= np.median(clientes))
    poco_digital = zonas["presencia_digital"].isna().to_numpy() | (zonas["presencia_digital"].to_numpy() < 0.25)
    return {
        "clientes_x100_visitas": 100 * total / visitas.sum(),
        "ocultas_visitadas": float((visitas[ocultas] > 0).mean()) if ocultas.any() else np.nan,
        "visitas_poca_senal_digital": float(visitas[poco_digital].sum() / visitas.sum()),
    }


def auditar(escenario: str, semillas: int, visitas_historicas: int = 3000) -> pd.DataFrame:
    filas = []
    for s in range(semillas):
        tablas = gen.generar(gen.Config(escenario=escenario, semilla=1000 + s, visitas_historicas=visitas_historicas))
        for politica in ("habitual", "ranking", "aprende", "mixto", "techo"):
            r = simular(tablas, politica, np.random.default_rng(50_000 + s))
            filas.append({"semilla": s, "politica": politica, **r})
    return pd.DataFrame(filas)


def resumen(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("politica")[["clientes_x100_visitas", "ocultas_visitadas", "visitas_poca_senal_digital"]].median()


VARIACIONES = [
    ("base", {}), ("salidas 8", {"SALIDAS_POR_SEMANA": 8}), ("salidas 25", {"SALIDAS_POR_SEMANA": 25}),
    ("5 visitas por salida", {"VISITAS_POR_SALIDA": 5}), ("4 semanas", {"SEMANAS": 4}), ("26 semanas", {"SEMANAS": 26}),
    ("exploración 10 %", {"CUOTA_EXPLORAR": 0.1}), ("exploración 40 %", {"CUOTA_EXPLORAR": 0.4}),
    ("previa 10", {"FUERZA_PREVIA": 10.0}), ("previa 100", {"FUERZA_PREVIA": 100.0}),
    ("historial 500", {"historial": 500}), ("historial 12000", {"historial": 12000}),
]


def sensibilidad(semillas: int) -> pd.DataFrame:
    """Peor caso de cada estrategia (frente a la mejor de las cuatro) al cambiar un parámetro."""
    estrategias = ["habitual", "ranking", "aprende", "mixto"]
    originales = {k: globals()[k] for k in ("SALIDAS_POR_SEMANA", "VISITAS_POR_SALIDA", "SEMANAS", "CUOTA_EXPLORAR", "FUERZA_PREVIA")}
    filas = []
    for nombre, cambio in VARIACIONES:
        globals().update({**originales, **{k: v for k, v in cambio.items() if k != "historial"}})
        peor = dict.fromkeys(estrategias, 1.0)
        for escenario in gen.ESCENARIOS:
            med = auditar(escenario, semillas, cambio.get("historial", 3000)).groupby("politica")["clientes_x100_visitas"].median()
            for e in estrategias:
                peor[e] = min(peor[e], med[e] / med[estrategias].max())
        filas.append({"variacion": nombre, **peor})
    globals().update(originales)
    return pd.DataFrame(filas).set_index("variacion")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--semillas", type=int, default=100)
    ap.add_argument("--sensibilidad", action="store_true", help="peor caso al variar parámetros")
    args = ap.parse_args()
    if args.sensibilidad:
        print((100 * sensibilidad(min(args.semillas, 60))).round(0).to_string())
        return
    for escenario in gen.ESCENARIOS:
        df = auditar(escenario, args.semillas)
        tabla = df.pivot(index="semilla", columns="politica", values="clientes_x100_visitas")
        print(f"\n== escenario: {escenario} ({args.semillas} semillas, medianas) ==")
        print(resumen(df).loc[["habitual", "ranking", "aprende", "mixto", "techo"]].round(3).to_string())
        for propia, rival in [("aprende", "habitual"), ("aprende", "ranking"),
                              ("mixto", "habitual"), ("mixto", "ranking")]:
            dif = tabla[propia] - tabla[rival]
            print(f"{propia} vs {rival}: gana en {100 * (dif > 0).mean():.0f}% de semillas; "
                  f"diferencia mediana {dif.median():+.2f} clientes x100 visitas "
                  f"(p10 {dif.quantile(0.1):+.2f}, p90 {dif.quantile(0.9):+.2f})")


if __name__ == "__main__":
    main()
