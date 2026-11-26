#!/usr/bin/env python
"""Territorio sintético para COM-01 «Encontrar oportunidades donde otros no ven clientes».

Genera zonas comerciales FICTICIAS (con nombres de distritos reales de La Libertad como
referencia geográfica), sus señales públicas simuladas (con huecos), un historial de visitas
comerciales sesgado hacia donde la entidad ya tiene clientes, y la «verdad de terreno»
oculta, que solo sirve para evaluar.

No hay personas, negocios, documentos ni contactos: la unidad es la zona.
Reproducible: misma semilla y escenario => mismas tablas. Solo numpy y pandas.

Es una herramienta de datos preexistente. NO contiene el planificador, el agente, la API ni la
interfaz, que se construyen en la fase presencial.

Uso:
    python retos/COM-01/datos/generar.py [--escenario oculto] [--semilla 20261203]
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA_DEFECTO = 20261203

# distrito, tipo, peso en número de zonas  (nombres geográficos reales; zonas FICTICIAS)
DISTRITOS = [
    ("Trujillo", "urbana", 14), ("El Porvenir", "urbana", 10), ("La Esperanza", "urbana", 10),
    ("Víctor Larco Herrera", "urbana", 6), ("Florencia de Mora", "urbana", 5),
    ("Huanchaco", "periurbana", 6), ("Moche", "periurbana", 5), ("Laredo", "periurbana", 5),
    ("Chepén", "periurbana", 8), ("Pacasmayo", "periurbana", 6), ("Guadalupe", "periurbana", 5),
    ("Casa Grande", "rural", 6), ("Chocope", "rural", 4), ("Virú", "rural", 8),
    ("Chao", "rural", 6), ("Huamachuco", "rural", 8), ("Otuzco", "rural", 5),
    ("Santiago de Chuco", "rural", 3),
]

# Escenarios (supuestos). Cambian cuánto se parece el potencial real a lo que ya se ve.
#   peso_presencia: cuánto se concentra la cartera actual donde el potencial real es alto.
#   peso_latente:   cuánto del potencial depende de algo que ninguna fuente pública muestra.
ESCENARIOS = {
    "oculto": {"peso_presencia": 0.15, "peso_latente": 0.6},
    "conocido": {"peso_presencia": 1.60, "peso_latente": 0.6},
    "datos_pobres": {"peso_presencia": 0.15, "peso_latente": 1.8},
}


@dataclass(frozen=True)
class Config:
    escenario: str = "oculto"
    semilla: int = SEMILLA_DEFECTO
    visitas_historicas: int = 3000
    conversion_media: float = 0.08  # clientes nuevos por visita en una zona sin saturar (supuesto)


def _z(x: np.ndarray) -> np.ndarray:
    return (x - np.nanmean(x)) / (np.nanstd(x) + 1e-9)


def _sigmoide(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def generar(cfg: Config = Config()) -> dict[str, pd.DataFrame]:
    if cfg.escenario not in ESCENARIOS:
        raise ValueError(f"escenario desconocido: {cfg.escenario}")
    par = ESCENARIOS[cfg.escenario]
    rng = np.random.default_rng(cfg.semilla)

    filas = [(d, t) for d, t, n in DISTRITOS for _ in range(n)]
    n = len(filas)
    distrito = np.array([f[0] for f in filas])
    tipo = np.array([f[1] for f in filas])
    urb, per = tipo == "urbana", tipo == "periurbana"

    negocios = np.round(rng.lognormal(np.log(np.select([urb, per], [320, 190], 110)), 0.45)).astype(int)
    actividad = np.clip(rng.beta(2.5, 2.5, n) + np.select([urb, per], [0.08, 0.02], -0.06), 0.02, 0.98)
    cobertura = rng.gamma(2.5, np.select([urb, per], [1.4, 0.9], 0.45))  # puntos financieros por 100 negocios
    digital = np.clip(rng.beta(2, 3, n) + np.select([urb, per], [0.15, 0.0], -0.18), 0.01, 0.95)
    distancia = rng.gamma(2.0, np.select([urb, per], [0.9, 2.5], 8.0))  # km a la agencia más cercana
    latente = rng.normal(0, 1, n)  # confianza, informalidad, competencia real: nadie lo publica

    senal = (
        0.55 * _z(actividad) - 0.55 * _z(cobertura) - 0.15 * _z(distancia)
        + par["peso_latente"] * latente
    )
    # se calibra el intercepto para que la conversión media sea la configurada
    lo, hi = -10.0, 5.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if _sigmoide(mid + senal).mean() < cfg.conversion_media else (lo, mid)
    p_real = _sigmoide(lo + senal)
    prospectos = np.maximum(np.round(negocios * rng.uniform(0.15, 0.40, n)), 10).astype(int)

    # cartera actual: más densa cerca de agencias y en zonas urbanas; según el escenario,
    # se concentra más o menos donde el potencial real es alto
    atractivo = (
        0.9 * _z(negocios.astype(float)) - 0.9 * _z(distancia) + 0.4 * _z(cobertura)
        + par["peso_presencia"] * _z(np.log(p_real))
    )
    peso = np.exp(atractivo - atractivo.max())
    clientes = rng.poisson(peso / peso.sum() * 9000)

    # señales públicas con huecos: la zona sin presencia digital se ve menos, no vale menos
    p_hueco = np.clip(0.55 - digital, 0.03, 0.5)
    digital_obs = np.where(rng.random(n) < p_hueco, np.nan, np.round(digital + rng.normal(0, 0.05, n), 3))
    zonas = pd.DataFrame({
        "zona_id": [f"Z-{i + 1:03d}" for i in range(n)],
        "distrito": distrito,
        "tipo": tipo,
        "negocios_estimados": np.round(negocios * rng.lognormal(0, 0.20, n)).astype(int),
        "actividad_comercial": np.round(np.clip(actividad + rng.normal(0, 0.10, n), 0, 1), 3),
        "puntos_financieros_x100neg": np.round(np.maximum(cobertura * rng.lognormal(0, 0.25, n), 0), 2),
        "presencia_digital": digital_obs,
        "km_agencia": np.round(distancia, 1),
        "clientes_actuales": clientes,
    })

    # historial de visitas: se visitó sobre todo donde ya hay clientes (sesgo de costumbre)
    p_visita = (clientes + 1.0) ** 1.2
    p_visita /= p_visita.sum()
    visitas = rng.multinomial(cfg.visitas_historicas, p_visita)
    historial = pd.DataFrame({
        "zona_id": zonas["zona_id"],
        "visitas": visitas,
        "clientes_nuevos": rng.binomial(visitas, p_real),
    })

    verdad = pd.DataFrame({
        "zona_id": zonas["zona_id"],
        "conversion_real": p_real,
        "prospectos_disponibles": prospectos,
    })
    return {"zonas": zonas, "historial": historial, "verdad": verdad}


def main() -> None:
    ap = argparse.ArgumentParser(description="Genera el territorio sintético de COM-01.")
    ap.add_argument("--escenario", choices=sorted(ESCENARIOS), default="oculto")
    ap.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    ap.add_argument("--salida", default=str(Path(__file__).parent / "sintetico"))
    args = ap.parse_args()
    tablas = generar(Config(escenario=args.escenario, semilla=args.semilla))
    destino = Path(args.salida)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, df in tablas.items():
        df.to_csv(destino / f"{nombre}.csv", index=False)
        print(f"{nombre}: {len(df)} filas")


if __name__ == "__main__":
    main()
