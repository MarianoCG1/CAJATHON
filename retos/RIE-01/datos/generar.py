#!/usr/bin/env python
"""Generador de datos SINTÉTICOS para el desafío RIE-01 «Microfinanzas resilientes al clima».

Qué hace
--------
Produce, en CSV y con semilla fija, un mundo sintético plausible para una caja municipal del
norte del Perú: distritos y sectores, un mapa de amenaza *visible* (con error), clientes MYPE con
actividad económica sensible o no al clima, créditos en S/, escenarios climáticos, eventos
históricos (para calibrar) y eventos de backtest con su «verdad» oculta (para medir el KPI).

Qué NO hace
-----------
No construye el modelo de exposición, los escenarios operativos, el mapa ni el agente: eso es la
funcionalidad crítica y se desarrolla en el evento presencial. Solo genera datos y un diagnóstico
de calidad del propio dataset (embudo exposición → afectación → mora).

Reglas del proyecto que cumple
------------------------------
* Sin datos reales ni personales: no hay nombres, documentos ni domicilios. Los ids son
  secuenciales y barajados; las coordenadas de clientes son un punto aleatorio alrededor del
  centroide de un sector.
* Sin red: solo usa pandas/numpy y la biblioteca estándar, y no abre conexiones.
* Reproducible: misma semilla y mismos parámetros dan los mismos bytes en los CSV (con la misma
  versión de pandas/numpy).
* Los nombres de distritos son reales (geografía pública) pero sus coordenadas son aproximadas y
  todo lo demás es inventado. La huella de agencias es sintética, no la red real de la Caja.

Uso
---
    python retos/RIE-01/datos/generar.py                      # 12 000 clientes → retos/RIE-01/datos/sintetico/
    python retos/RIE-01/datos/generar.py --n-clientes 50000 --seed 7 --out retos/RIE-01/datos/sintetico

Todo parámetro del «mundo» (sensibilidades, efectividad de acciones, severidades) es un SUPUESTO
DEL GENERADOR, no un dato de la Caja ni una estimación de impacto real.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

VERSION_GENERADOR = "1.0"
SEED_POR_DEFECTO = 20261203
N_CLIENTES_POR_DEFECTO = 12_000
FECHA_CORTE_POR_DEFECTO = "2026-10-31"
SALIDA_POR_DEFECTO = Path(__file__).resolve().parent / "sintetico"

TIPOS_AMENAZA = ["lluvia_intensa", "inundacion", "sequia"]
ZONAS = ["costa", "sierra", "selva_alta"]
TIPOS_SECTOR = ["ribera_cauce", "llanura_urbana", "campina_regada", "ladera_secano"]
SEVERIDADES = {"leve": 0.30, "moderada": 0.55, "severa": 0.85}
SD_SEVERIDAD = {"leve": 0.10, "moderada": 0.12, "severa": 0.15}

# Archivos de salida (clave lógica → ruta relativa). Lo de backtest/ es «verdad» y no se usa para entrenar.
ARCHIVOS = {
    "agencias": "agencias.csv",
    "distritos": "distritos.csv",
    "sectores": "sectores.csv",
    "mapa_amenaza": "mapa_amenaza.csv",
    "actividades": "actividades.csv",
    "clientes": "clientes.csv",
    "creditos": "creditos.csv",
    "escenarios": "escenarios.csv",
    "eventos_historicos": "eventos_historicos.csv",
    "impacto_historico": "impacto_historico.csv",
    "acciones_preventivas": "acciones_preventivas.csv",
    "eventos_backtest": "backtest/eventos_backtest.csv",
    "impacto_backtest": "backtest/impacto_backtest.csv",
    "verdad_amenaza_sector": "backtest/verdad_amenaza_sector.csv",
}

# --------------------------------------------------------------------------------------
# Geografía (nombres reales, coordenadas aproximadas ±5 km, valores de peso inventados)
# (nombre, provincia, departamento, lat, lon, altitud_m, zona, perfil, peso_relativo)
# La huella es sintética: pesa más La Libertad. [POR CONFIRMAR] la huella real con la Caja.
# --------------------------------------------------------------------------------------
DISTRITOS = [
    ("Trujillo", "Trujillo", "La Libertad", -8.112, -79.029, 34, "costa", "urbano", 14.0),
    ("El Porvenir", "Trujillo", "La Libertad", -8.075, -79.000, 60, "costa", "urbano", 9.0),
    ("La Esperanza", "Trujillo", "La Libertad", -8.078, -79.042, 70, "costa", "urbano", 10.0),
    ("Florencia de Mora", "Trujillo", "La Libertad", -8.083, -79.020, 50, "costa", "urbano", 3.0),
    ("Víctor Larco Herrera", "Trujillo", "La Libertad", -8.137, -79.056, 12, "costa", "urbano", 5.0),
    ("Huanchaco", "Trujillo", "La Libertad", -8.078, -79.122, 5, "costa", "pesquero_turistico", 4.0),
    ("Moche", "Trujillo", "La Libertad", -8.170, -79.010, 20, "costa", "agricola_costa", 3.0),
    ("Laredo", "Trujillo", "La Libertad", -8.083, -78.959, 100, "costa", "agricola_costa", 3.0),
    ("Salaverry", "Trujillo", "La Libertad", -8.224, -78.980, 5, "costa", "pesquero_turistico", 2.0),
    ("Chicama", "Ascope", "La Libertad", -7.845, -79.147, 160, "costa", "agricola_costa", 2.0),
    ("Paiján", "Ascope", "La Libertad", -7.730, -79.300, 40, "costa", "agricola_costa", 3.0),
    ("Casa Grande", "Ascope", "La Libertad", -7.745, -79.185, 150, "costa", "agricola_costa", 3.0),
    ("Chocope", "Ascope", "La Libertad", -7.790, -79.225, 100, "costa", "agricola_costa", 2.0),
    ("Santiago de Cao", "Ascope", "La Libertad", -7.960, -79.230, 15, "costa", "agricola_costa", 1.5),
    ("Rázuri", "Ascope", "La Libertad", -7.700, -79.440, 10, "costa", "pesquero_turistico", 1.0),
    ("Ascope", "Ascope", "La Libertad", -7.715, -79.110, 280, "costa", "agricola_costa", 1.0),
    ("Chepén", "Chepén", "La Libertad", -7.225, -79.430, 130, "costa", "agricola_costa", 4.0),
    ("Guadalupe", "Pacasmayo", "La Libertad", -7.250, -79.480, 100, "costa", "agricola_costa", 3.0),
    ("San Pedro de Lloc", "Pacasmayo", "La Libertad", -7.425, -79.510, 40, "costa", "agricola_costa", 2.5),
    ("Pacasmayo", "Pacasmayo", "La Libertad", -7.400, -79.570, 5, "costa", "pesquero_turistico", 2.0),
    ("Virú", "Virú", "La Libertad", -8.415, -78.750, 90, "costa", "agricola_costa", 3.0),
    ("Chao", "Virú", "La Libertad", -8.540, -78.680, 80, "costa", "agricola_costa", 2.0),
    ("Guadalupito", "Virú", "La Libertad", -8.950, -78.620, 30, "costa", "agricola_costa", 1.0),
    ("Huamachuco", "Sánchez Carrión", "La Libertad", -7.820, -78.050, 3180, "sierra", "sierra", 3.0),
    ("Otuzco", "Otuzco", "La Libertad", -7.900, -78.570, 2640, "sierra", "sierra", 2.0),
    ("Cascas", "Gran Chimú", "La Libertad", -7.480, -78.820, 1280, "sierra", "sierra", 1.5),
    ("Santiago de Chuco", "Santiago de Chuco", "La Libertad", -8.140, -78.180, 3120, "sierra", "sierra", 1.5),
    ("Chiclayo", "Chiclayo", "Lambayeque", -6.771, -79.840, 30, "costa", "urbano", 7.0),
    ("Lambayeque", "Lambayeque", "Lambayeque", -6.700, -79.906, 20, "costa", "agricola_costa", 3.0),
    ("Ferreñafe", "Ferreñafe", "Lambayeque", -6.640, -79.790, 50, "costa", "agricola_costa", 2.0),
    ("Motupe", "Lambayeque", "Lambayeque", -6.150, -79.720, 190, "costa", "agricola_costa", 1.5),
    ("Olmos", "Lambayeque", "Lambayeque", -5.990, -79.760, 150, "costa", "agricola_costa", 1.5),
    ("Piura", "Piura", "Piura", -5.195, -80.632, 30, "costa", "urbano", 6.0),
    ("Castilla", "Piura", "Piura", -5.200, -80.620, 30, "costa", "urbano", 3.0),
    ("Catacaos", "Piura", "Piura", -5.270, -80.680, 25, "costa", "agricola_costa", 2.0),
    ("Sullana", "Sullana", "Piura", -4.903, -80.686, 60, "costa", "urbano", 4.0),
    ("Paita", "Paita", "Piura", -5.090, -81.110, 5, "costa", "pesquero_turistico", 2.0),
    ("Sechura", "Sechura", "Piura", -5.557, -80.822, 10, "costa", "pesquero_turistico", 1.5),
    ("Chulucanas", "Morropón", "Piura", -5.095, -80.163, 95, "costa", "agricola_costa", 2.0),
    ("Chimbote", "Santa", "Áncash", -9.085, -78.578, 5, "costa", "urbano", 3.0),
    ("Nuevo Chimbote", "Santa", "Áncash", -9.120, -78.520, 20, "costa", "urbano", 2.5),
    ("Casma", "Casma", "Áncash", -9.470, -78.310, 20, "costa", "agricola_costa", 1.0),
    ("Cajamarca", "Cajamarca", "Cajamarca", -7.157, -78.510, 2750, "sierra", "sierra", 3.0),
    ("Jaén", "Jaén", "Cajamarca", -5.708, -78.808, 730, "selva_alta", "selva_alta", 2.5),
]

# Agencias sintéticas (nombre de ciudad → distrito donde se ubican). No es la red real de la Caja.
AGENCIAS = [
    "Trujillo", "El Porvenir", "La Esperanza", "Chepén", "Pacasmayo", "Casa Grande", "Virú",
    "Huamachuco", "Chiclayo", "Piura", "Chimbote", "Cajamarca", "Jaén",
]

# Peso de cada tipo de sector por perfil de distrito (ribera, llanura, campiña, ladera).
PESO_SECTOR = {
    "urbano": [0.15, 0.55, 0.15, 0.15],
    "agricola_costa": [0.20, 0.20, 0.50, 0.10],
    "sierra": [0.10, 0.20, 0.25, 0.45],
    "selva_alta": [0.20, 0.20, 0.40, 0.20],
    "pesquero_turistico": [0.20, 0.50, 0.10, 0.20],
}

# Susceptibilidad latente base por tipo de amenaza y tipo de sector (supuesto del generador).
HAZARD_BASE = {
    "inundacion": [0.80, 0.35, 0.45, 0.08],
    "lluvia_intensa": [0.55, 0.50, 0.35, 0.65],
    "sequia": [0.15, 0.10, 0.35, 0.80],
}
# Cómo se reparte una amenaza/evento por zona geográfica (supuesto del generador).
PATRON_ZONA = {
    "lluvia_intensa": {"costa": 1.0, "sierra": 0.8, "selva_alta": 0.7},
    "inundacion": {"costa": 1.0, "sierra": 0.5, "selva_alta": 0.8},
    "sequia": {"costa": 0.6, "sierra": 1.0, "selva_alta": 0.5},
}

# (id, nombre, rubro, sens_lluvia, sens_inundacion, sens_sequia, ticket_mediano_soles,
#  factor_ingreso, p_seguro) — sensibilidades y tickets son supuestos del generador.
ACTIVIDADES = [
    ("A01", "Cultivo de arroz", "agropecuario", 0.50, 0.85, 0.90, 9000, 0.75, 0.10),
    ("A02", "Cultivo de frutales", "agropecuario", 0.50, 0.70, 0.75, 12000, 0.95, 0.10),
    ("A03", "Cultivo de caña y cultivos transitorios", "agropecuario", 0.40, 0.70, 0.85, 8000, 0.70, 0.10),
    ("A04", "Hortalizas y pan llevar", "agropecuario", 0.55, 0.75, 0.80, 4000, 0.60, 0.10),
    ("A05", "Crianza de animales menores y aves", "agropecuario", 0.40, 0.60, 0.50, 5000, 0.70, 0.10),
    ("A06", "Pesca artesanal y acuicultura", "pesca", 0.60, 0.30, 0.10, 7000, 0.90, 0.03),
    ("A07", "Comercio minorista (bodega, abarrotes)", "comercio", 0.30, 0.45, 0.15, 6000, 1.00, 0.03),
    ("A08", "Mercado y comercio ambulante", "comercio", 0.50, 0.55, 0.20, 5000, 0.85, 0.03),
    ("A09", "Restaurante y servicios de comida", "servicios", 0.35, 0.40, 0.20, 8000, 1.10, 0.03),
    ("A10", "Transporte (mototaxi, carga ligera)", "transporte", 0.50, 0.40, 0.10, 9000, 1.05, 0.03),
    ("A11", "Taller y manufactura ligera", "manufactura", 0.30, 0.40, 0.20, 12000, 1.20, 0.03),
    ("A12", "Construcción menor y materiales", "construccion", 0.55, 0.35, 0.10, 11000, 1.15, 0.03),
    ("A13", "Hospedaje y turismo", "turismo", 0.40, 0.35, 0.35, 14000, 1.30, 0.03),
    ("A14", "Servicios personales y profesionales", "servicios", 0.15, 0.20, 0.05, 6000, 1.00, 0.03),
]
PESO_ACTIVIDAD = {
    "urbano": [0.01, 0.01, 0.01, 0.02, 0.02, 0.01, 0.24, 0.14, 0.10, 0.09, 0.12, 0.06, 0.03, 0.15],
    "agricola_costa": [0.18, 0.14, 0.10, 0.07, 0.06, 0.01, 0.10, 0.04, 0.04, 0.06, 0.05, 0.04, 0.01, 0.05],
    "sierra": [0.02, 0.05, 0.18, 0.20, 0.15, 0.00, 0.12, 0.06, 0.04, 0.05, 0.04, 0.04, 0.01, 0.04],
    "selva_alta": [0.20, 0.10, 0.12, 0.10, 0.06, 0.00, 0.10, 0.04, 0.04, 0.06, 0.04, 0.04, 0.02, 0.04],
    "pesquero_turistico": [0.01, 0.02, 0.01, 0.02, 0.03, 0.22, 0.16, 0.08, 0.14, 0.07, 0.05, 0.04, 0.12, 0.03],
}

# Eventos históricos (calibración): (id, tipo, fecha, severidad). Fechas ficticias; no replican
# episodios reales. La severidad máxima histórica es MENOR que la de algunos eventos de backtest
# a propósito, para probar extrapolación.
EVENTOS_HISTORICOS = [
    ("EH01", "lluvia_intensa", "2018-02-12", 0.35),
    ("EH02", "inundacion", "2018-12-08", 0.45),
    ("EH03", "inundacion", "2019-03-20", 0.55),
    ("EH04", "sequia", "2020-03-14", 0.40),
    ("EH05", "lluvia_intensa", "2020-10-02", 0.50),
    ("EH06", "inundacion", "2021-02-25", 0.30),
    ("EH07", "sequia", "2022-03-18", 0.55),
    ("EH08", "lluvia_intensa", "2023-02-12", 0.40),
    ("EH09", "inundacion", "2024-02-05", 0.50),
    ("EH10", "sequia", "2025-03-22", 0.35),
]
# Eventos de backtest: (id, escenario_ex_ante, fecha_simulada). Fechas posteriores al corte.
EVENTOS_BACKTEST = [
    ("EB01", "ES02", "2027-02-10"),  # lluvia moderada
    ("EB02", "ES06", "2027-03-05"),  # inundación severa
    ("EB03", "ES09", "2027-02-20"),  # sequía severa
    ("EB04", "ES05", "2027-03-15"),  # inundación moderada
    ("EB05", "ES03", "2027-01-25"),  # lluvia severa
    ("EB06", "ES07", "2027-02-28"),  # sequía leve
]

# Catálogo de acciones preventivas. Costos y efectividades son PARÁMETROS DE SIMULACIÓN
# (supuesto del generador), no política de la Caja: [POR CONFIRMAR] con el owner qué acciones
# existen y cuánto cuestan. La efectividad es una reducción relativa de P(mora | afectado).
ACCIONES = [
    ("AC01", "alerta_temprana", "comunicacion", "Mensaje anticipado al cliente con recomendaciones del escenario", 0.5, 0.02, 0.08, "todos"),
    ("AC02", "visita_preventiva", "visita", "Visita del gestor para evaluar el negocio antes del evento", 30.0, 0.10, 0.25, "todos"),
    ("AC03", "reprogramacion_preventiva", "condicion_credito", "Periodo de gracia de 1 a 2 cuotas, con aprobación humana", 8.0, 0.25, 0.50, "todos"),
    ("AC04", "ampliacion_de_plazo", "condicion_credito", "Reducción de cuota ampliando el plazo, con aprobación humana", 15.0, 0.20, 0.40, "todos"),
    ("AC05", "capital_de_reposicion", "producto", "Línea corta para reponer insumos o activos tras el evento", 20.0, 0.15, 0.35, "todos"),
    ("AC06", "derivacion_a_microseguro", "producto", "Oferta de microseguro. [POR CONFIRMAR] si la Caja lo ofrece", 5.0, 0.10, 0.30, "agropecuario"),
    ("AC07", "asesoria_continuidad", "comunicacion", "Orientación breve de continuidad del negocio", 12.0, 0.03, 0.10, "todos"),
]


# --------------------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------------------
def _sigmoide(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _haversine_km(lat1, lon1, lat2, lon2):
    """Distancia en km; admite arreglos con broadcasting."""
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = p2 - p1
    dl = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * r * np.arcsin(np.sqrt(a))


def _categoria_amenaza(indice: np.ndarray) -> np.ndarray:
    """Categorías por cuantiles dentro de cada amenaza (40 % bajo, 30 % medio, 20 % alto, 10 % muy alto)."""
    q40, q70, q90 = np.quantile(indice, [0.40, 0.70, 0.90])
    return np.select([indice < q40, indice < q70, indice < q90], ["bajo", "medio", "alto"],
                     default="muy_alto")


def _calificacion(dias: np.ndarray) -> np.ndarray:
    """Simplificación de la clasificación por días de atraso para micro y pequeña empresa."""
    return np.select(
        [dias <= 8, dias <= 30, dias <= 60, dias <= 120],
        ["normal", "cpp", "deficiente", "dudoso"],
        default="perdida",
    )


def _rngs(seed: int) -> Dict[str, np.random.Generator]:
    nombres = ["sectores", "hazard", "mapa", "clientes", "creditos", "eventos"]
    hijos = np.random.SeedSequence(seed).spawn(len(nombres))
    return {n: np.random.default_rng(h) for n, h in zip(nombres, hijos)}


def _rng_evento(seed: int, clave: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, 7919, clave]))


# --------------------------------------------------------------------------------------
# Tablas de referencia
# --------------------------------------------------------------------------------------
def generar_distritos() -> pd.DataFrame:
    filas = []
    for i, (nom, prov, dep, lat, lon, alt, zona, perfil, peso) in enumerate(DISTRITOS, start=1):
        filas.append((f"D{i:02d}", nom, prov, dep, lat, lon, alt, zona, perfil, peso))
    return pd.DataFrame(
        filas,
        columns=["distrito_id", "distrito", "provincia", "departamento", "lat", "lon",
                 "altitud_m", "zona", "perfil", "peso_relativo"],
    )


def generar_actividades() -> pd.DataFrame:
    df = pd.DataFrame(
        ACTIVIDADES,
        columns=["actividad_id", "actividad", "rubro", "sens_lluvia_intensa", "sens_inundacion",
                 "sens_sequia", "ticket_mediano_soles", "factor_ingreso", "prob_seguro"],
    )
    sens = df[["sens_lluvia_intensa", "sens_inundacion", "sens_sequia"]].max(axis=1)
    df["es_sensible_clima"] = (sens >= 0.60).astype(int)
    return df


def generar_sectores(distritos: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    filas = []
    for d in distritos.itertuples(index=False):
        for k, tipo in enumerate(TIPOS_SECTOR):
            delta_alt = [-8, 0, 6, 120 if d.zona == "costa" else 250][k]
            sd_off = 0.03 if k == 3 else 0.015
            dist_cauce = [rng.uniform(0.02, 0.4), rng.uniform(0.5, 3.0),
                          rng.uniform(0.3, 2.0), rng.uniform(1.0, 6.0)][k]
            pendiente = [rng.uniform(0.5, 4), rng.uniform(0, 3), rng.uniform(1, 5), rng.uniform(15, 45)][k]
            filas.append((
                f"{d.distrito_id}-{'RULC'[k]}", d.distrito_id, tipo,
                d.lat + rng.normal(0, sd_off), d.lon + rng.normal(0, sd_off),
                max(0.0, d.altitud_m + delta_alt + rng.normal(0, 5)),
                dist_cauce, pendiente, PESO_SECTOR[d.perfil][k],
            ))
    df = pd.DataFrame(
        filas,
        columns=["sector_id", "distrito_id", "tipo_sector", "lat", "lon", "altitud_m",
                 "dist_cauce_km", "pendiente_pct", "peso_area"],
    )
    return df


def generar_verdad_amenaza(sectores: pd.DataFrame, distritos: pd.DataFrame,
                           rng: np.random.Generator) -> pd.DataFrame:
    """Susceptibilidad latente por sector y amenaza. Es la VERDAD; el mapa visible la aproxima mal."""
    zona = sectores.merge(distritos[["distrito_id", "zona"]], on="distrito_id")["zona"].to_numpy()
    idx_tipo = sectores["tipo_sector"].map({t: i for i, t in enumerate(TIPOS_SECTOR)}).to_numpy()
    out = []
    pos_dist = {d: i for i, d in enumerate(distritos["distrito_id"])}
    i_dist = sectores["distrito_id"].map(pos_dist).to_numpy()
    for tipo in TIPOS_AMENAZA:
        base = np.array(HAZARD_BASE[tipo])[idx_tipo]
        mod = np.array([PATRON_ZONA[tipo][z] for z in zona])
        # factor de distrito (cuenca, drenaje, red de riego): hace que unos distritos sean más críticos
        f_dist = rng.lognormal(0.0, 0.35, size=len(distritos))[i_dist]
        h = base * mod * f_dist * rng.lognormal(0.0, 0.2, size=len(sectores))
        if tipo == "inundacion":
            h = h * (0.5 + 0.5 * np.exp(-sectores["dist_cauce_km"].to_numpy() / 1.5))
        out.append(pd.DataFrame({
            "sector_id": sectores["sector_id"], "tipo_amenaza": tipo,
            "susceptibilidad_real": np.clip(h, 0.0, 1.0),
        }))
    return pd.concat(out, ignore_index=True)


def generar_mapa_amenaza(sectores: pd.DataFrame, verdad: pd.DataFrame, rng: np.random.Generator,
                         error_estandar: float = 0.07) -> pd.DataFrame:
    """Mapa visible a nivel de distrito: promedio ponderado de la verdad + error. Resolución gruesa."""
    m = verdad.merge(sectores[["sector_id", "distrito_id", "peso_area"]], on="sector_id")
    m["ponderado"] = m["susceptibilidad_real"] * m["peso_area"]
    g = m.groupby(["distrito_id", "tipo_amenaza"], sort=True).agg(
        s=("ponderado", "sum"), w=("peso_area", "sum")).reset_index()
    g["indice"] = np.clip(g["s"] / g["w"] + rng.normal(0, error_estandar, size=len(g)), 0.0, 1.0)
    g["categoria"] = ""
    for tipo in TIPOS_AMENAZA:
        sel = g["tipo_amenaza"] == tipo
        g.loc[sel, "categoria"] = _categoria_amenaza(g.loc[sel, "indice"].to_numpy())
    g["error_estandar"] = error_estandar
    g["resolucion"] = "distrito"
    g["fuente"] = "sintetico_v1"
    return g[["distrito_id", "tipo_amenaza", "indice", "categoria", "error_estandar",
              "resolucion", "fuente"]]


def generar_escenarios() -> pd.DataFrame:
    filas = []
    duraciones = {"lluvia_intensa": (3, 4, 6), "inundacion": (2, 3, 5), "sequia": (12, 20, 32)}
    nombres = {"lluvia_intensa": "Lluvias intensas", "inundacion": "Inundación", "sequia": "Sequía"}
    n = 1
    for tipo in TIPOS_AMENAZA:
        for j, (sev, val) in enumerate(SEVERIDADES.items()):
            patron = PATRON_ZONA[tipo]
            filas.append((
                f"ES{n:02d}", f"{nombres[tipo]} {sev}", tipo, sev, val, SD_SEVERIDAD[sev],
                round(min(1.0, val * patron["costa"]), 4),
                round(min(1.0, val * patron["sierra"]), 4),
                round(min(1.0, val * patron["selva_alta"]), 4),
                duraciones[tipo][j],
                f"Escenario hipotético de {nombres[tipo].lower()} {sev} (parámetros del generador)",
            ))
            n += 1
    return pd.DataFrame(filas, columns=[
        "escenario_id", "nombre", "tipo_amenaza", "severidad", "severidad_nominal",
        "sd_severidad", "intensidad_costa", "intensidad_sierra", "intensidad_selva_alta",
        "duracion_semanas", "descripcion"])


def generar_acciones() -> pd.DataFrame:
    df = pd.DataFrame(ACCIONES, columns=[
        "accion_id", "accion", "tipo", "descripcion", "costo_unitario_soles",
        "efectividad_min", "efectividad_max", "aplica_rubros"])
    df["requiere_aprobacion_humana"] = 1
    df["origen_parametros"] = "supuesto_generador"
    return df


# --------------------------------------------------------------------------------------
# Clientes y créditos
# --------------------------------------------------------------------------------------
def generar_agencias_y_clientes(n_clientes: int, distritos: pd.DataFrame, sectores: pd.DataFrame,
                                actividades: pd.DataFrame, fecha_corte: pd.Timestamp,
                                rng: np.random.Generator):
    # 1) distrito por cliente
    pesos = distritos["peso_relativo"].to_numpy(dtype=float)
    pesos = pesos / pesos.sum()
    idx_dist = rng.choice(len(distritos), size=n_clientes, p=pesos)
    # 2) sector y actividad según el perfil del distrito
    perfil = distritos["perfil"].to_numpy()[idx_dist]
    sec_por_dist = {d: g.reset_index(drop=True) for d, g in sectores.groupby("distrito_id", sort=False)}
    sector_id = np.empty(n_clientes, dtype=object)
    actividad_id = np.empty(n_clientes, dtype=object)
    lat = np.empty(n_clientes)
    lon = np.empty(n_clientes)
    act_ids = actividades["actividad_id"].to_numpy()
    for i_d, fila in enumerate(distritos.itertuples(index=False)):
        sel = np.where(idx_dist == i_d)[0]
        if len(sel) == 0:
            continue
        sec = sec_por_dist[fila.distrito_id]
        p_s = np.array(PESO_SECTOR[fila.perfil], dtype=float)
        k = rng.choice(4, size=len(sel), p=p_s / p_s.sum())
        sector_id[sel] = sec["sector_id"].to_numpy()[k]
        lat[sel] = sec["lat"].to_numpy()[k] + rng.normal(0, 0.005, size=len(sel))
        lon[sel] = sec["lon"].to_numpy()[k] + rng.normal(0, 0.005, size=len(sel))
        p_a = np.array(PESO_ACTIVIDAD[fila.perfil], dtype=float)
        actividad_id[sel] = rng.choice(act_ids, size=len(sel), p=p_a / p_a.sum())
    clientes = pd.DataFrame({
        "distrito_id": distritos["distrito_id"].to_numpy()[idx_dist],
        "sector_id": sector_id, "lat": lat, "lon": lon, "actividad_id": actividad_id,
    })
    # 3) agencia más cercana
    ag_dist = distritos.set_index("distrito")
    ag = pd.DataFrame({
        "agencia_id": [f"AG{i:02d}" for i in range(1, len(AGENCIAS) + 1)],
        "nombre": [f"Agencia sintética {c}" for c in AGENCIAS],
        "distrito_id": [ag_dist.loc[c, "distrito_id"] for c in AGENCIAS],
        "lat": [ag_dist.loc[c, "lat"] for c in AGENCIAS],
        "lon": [ag_dist.loc[c, "lon"] for c in AGENCIAS],
    })
    dm = _haversine_km(clientes["lat"].to_numpy()[:, None], clientes["lon"].to_numpy()[:, None],
                       ag["lat"].to_numpy()[None, :], ag["lon"].to_numpy()[None, :])
    clientes["agencia_id"] = ag["agencia_id"].to_numpy()[dm.argmin(axis=1)]
    # 4) atributos de amortiguación (supuestos del generador)
    act = actividades.set_index("actividad_id")
    n = n_clientes
    clientes["tiene_ingreso_secundario"] = (rng.random(n) < 0.25).astype(int)
    clientes["tiene_seguro"] = (rng.random(n) < act.loc[clientes["actividad_id"], "prob_seguro"].to_numpy()).astype(int)
    clientes["meses_reserva"] = rng.choice([0, 1, 2, 3, 5], size=n, p=[0.45, 0.25, 0.15, 0.10, 0.05])
    # 5) ids sintéticos barajados (no ordenados por distrito)
    orden = rng.permutation(n)
    clientes = clientes.iloc[orden].reset_index(drop=True)
    clientes.insert(0, "cliente_id", [f"C{i:06d}" for i in range(1, n + 1)])
    return ag, clientes


def generar_creditos(clientes: pd.DataFrame, actividades: pd.DataFrame, fecha_corte: pd.Timestamp,
                     rng: np.random.Generator):
    """Devuelve (creditos, clientes_actualizados con ingreso y antigüedad)."""
    act = actividades.set_index("actividad_id")
    n = len(clientes)
    segundo = rng.random(n) < 0.15
    filas_cli = np.concatenate([np.arange(n), np.where(segundo)[0]])
    c = clientes.iloc[filas_cli].reset_index(drop=True)
    m = len(c)
    rubro = act.loc[c["actividad_id"], "rubro"].to_numpy()
    es_agro = rubro == "agropecuario"
    u = rng.random(m)
    producto = np.where(es_agro, np.where(u < 0.60, "agropecuario", "capital_trabajo"),
                        np.where(u < 0.75, "capital_trabajo", "activo_fijo"))
    ticket = act.loc[c["actividad_id"], "ticket_mediano_soles"].to_numpy(dtype=float)
    monto = np.clip(ticket * rng.lognormal(0.0, 0.6, size=m), 500, 80_000)
    monto = np.round(monto / 100.0) * 100.0
    plazo = np.where(producto == "agropecuario", rng.integers(6, 13, size=m),
                     np.where(producto == "activo_fijo", rng.integers(12, 37, size=m),
                              rng.integers(6, 25, size=m)))
    tea_media = np.select([producto == "capital_trabajo", producto == "activo_fijo"], [38.0, 32.0], default=30.0)
    tea = np.clip(rng.normal(tea_media, 5.0), 20.0, 60.0)
    r = (1.0 + tea / 100.0) ** (1.0 / 12.0) - 1.0
    cuota = monto * r / (1.0 - (1.0 + r) ** (-plazo))
    k = np.minimum(np.floor(rng.uniform(0, 1, size=m) * plazo), plazo - 1).astype(int)  # cuotas pagadas
    saldo = monto * ((1 + r) ** plazo - (1 + r) ** k) / ((1 + r) ** plazo - 1)
    desembolso = fecha_corte - pd.to_timedelta(k * 30 + rng.integers(0, 30, size=m), unit="D")
    # atraso (sintético): ~5 % >30 días, ~10 % entre 1 y 30
    uu = rng.random(m)
    dias = np.where(uu < 0.05, np.clip(31 + rng.exponential(35, size=m), 31, 180),
                    np.where(uu < 0.15, rng.integers(1, 31, size=m), 0)).astype(int)
    estado = np.where(dias > 30, "vencido", np.where(rng.random(m) < 0.02, "refinanciado", "vigente"))
    creditos = pd.DataFrame({
        "cliente_id": c["cliente_id"].to_numpy(), "producto": producto,
        "monto_desembolsado_soles": monto, "plazo_meses": plazo, "tea_pct": tea,
        "fecha_desembolso": desembolso.strftime("%Y-%m-%d"), "cuota_mensual_soles": cuota,
        "saldo_soles": saldo, "dias_atraso": dias, "calificacion": _calificacion(dias),
        "estado": estado,
    })
    creditos = creditos.sort_values(["cliente_id", "fecha_desembolso"], kind="stable").reset_index(drop=True)
    creditos.insert(0, "credito_id", [f"CR{i:06d}" for i in range(1, len(creditos) + 1)])
    # cliente: ingreso coherente con la cuota y antigüedad coherente con el primer crédito
    cuota_total = creditos.groupby("cliente_id")["cuota_mensual_soles"].sum()
    meses_max = (creditos.assign(
        meses=((fecha_corte - pd.to_datetime(creditos["fecha_desembolso"])).dt.days // 30))
        .groupby("cliente_id")["meses"].max())
    cl = clientes.copy().set_index("cliente_id")
    # ingreso mensual derivado de la carga financiera objetivo (cuota/ingreso ~ 20 %, rango 5–55 %);
    # actividades con mayor factor_ingreso soportan menos carga relativa (supuesto del generador)
    factor = act.loc[cl["actividad_id"], "factor_ingreso"].to_numpy()
    carga_obj = np.clip(0.20 * rng.lognormal(0.0, 0.4, size=n) / np.sqrt(factor), 0.05, 0.55)
    cl["ingreso_mensual_soles"] = np.clip(cuota_total.reindex(cl.index).to_numpy() / carga_obj, 600.0, 15_000.0)
    ant = np.clip(rng.gamma(2.5, 30.0, size=n), 1, 240).astype(int)
    cl["antiguedad_meses"] = np.maximum(ant, meses_max.reindex(cl.index).to_numpy() + 1)
    cl["fecha_alta"] = (fecha_corte - pd.to_timedelta(cl["antiguedad_meses"] * 30, unit="D")).dt.strftime("%Y-%m-%d")
    cl = cl.reset_index()
    return creditos, cl


# --------------------------------------------------------------------------------------
# Eventos e impacto
# --------------------------------------------------------------------------------------
def _intensidades(tipo: str, severidad: float, rng: np.random.Generator) -> Dict[str, float]:
    return {z: float(np.clip(severidad * PATRON_ZONA[tipo][z] * np.exp(rng.normal(0, 0.15)), 0.0, 1.0))
            for z in ZONAS}


def _contexto_clientes(clientes, creditos, sectores, distritos, actividades) -> pd.DataFrame:
    saldo = creditos.groupby("cliente_id")["saldo_soles"].sum()
    cuota = creditos.groupby("cliente_id")["cuota_mensual_soles"].sum()
    ctx = clientes.merge(distritos[["distrito_id", "zona"]], on="distrito_id", how="left")
    ctx = ctx.merge(actividades[["actividad_id", "sens_lluvia_intensa", "sens_inundacion", "sens_sequia"]],
                    on="actividad_id", how="left")
    ctx["saldo_total"] = saldo.reindex(ctx["cliente_id"]).to_numpy()
    ctx["carga"] = cuota.reindex(ctx["cliente_id"]).to_numpy() / ctx["ingreso_mensual_soles"].to_numpy()
    ctx["colchon"] = (0.8 * ctx["tiene_ingreso_secundario"] + 1.0 * ctx["tiene_seguro"]
                      + 0.25 * ctx["meses_reserva"])
    idx_sector = {s: i for i, s in enumerate(sectores["sector_id"])}
    ctx["_i_sector"] = ctx["sector_id"].map(idx_sector).to_numpy()
    return ctx


def simular_impacto(ctx: pd.DataFrame, h_matriz: Dict[str, np.ndarray], tipo: str,
                    intens: Dict[str, float], rng: np.random.Generator) -> pd.DataFrame:
    """Proceso generador de la verdad: intensidad local → afectación → caída de ingreso → mora."""
    n = len(ctx)
    eps = rng.normal(0, 1, size=len(next(iter(h_matriz.values()))))  # microclima por sector y evento
    i_zona = ctx["zona"].map(intens).to_numpy(dtype=float)
    h = h_matriz[tipo][ctx["_i_sector"].to_numpy()]
    local = np.clip(h * i_zona * (1.0 + 0.25 * eps[ctx["_i_sector"].to_numpy()]), 0.0, 1.0)
    sens = ctx[f"sens_{tipo}"].to_numpy(dtype=float)
    logit = -3.0 + 8.5 * local * sens - 0.5 * ctx["colchon"].to_numpy() + rng.normal(0, 0.5, size=n)
    afectado = (rng.random(n) < _sigmoide(logit)).astype(int)
    caida = np.where(afectado == 1,
                     np.clip(0.10 + 0.6 * local * sens + rng.normal(0, 0.08, size=n), 0.05, 0.90), 0.0)
    carga_post = ctx["carga"].to_numpy() / (1.0 - caida)
    p_inc = np.where(afectado == 1, _sigmoide(-2.2 + 5.0 * carga_post), 0.01)
    incumple = (rng.random(n) < p_inc).astype(int)
    dias = np.where(incumple == 1, rng.integers(31, 91, size=n),
                    np.where(rng.random(n) < np.where(afectado == 1, 0.40, 0.10),
                             rng.integers(1, 31, size=n), 0))
    return pd.DataFrame({
        "cliente_id": ctx["cliente_id"].to_numpy(),
        "intensidad_local_real": local, "afectado": afectado, "caida_ingreso_pct": caida,
        "dias_atraso_max_90d": dias, "incumple_30d": incumple,
        "saldo_en_mora_soles": ctx["saldo_total"].to_numpy() * incumple,
    })


def generar_eventos_e_impacto(seed: int, ctx: pd.DataFrame, verdad: pd.DataFrame,
                              sectores: pd.DataFrame, escenarios: pd.DataFrame,
                              fecha_corte: pd.Timestamp):
    h_matriz = {}
    for tipo in TIPOS_AMENAZA:
        v = verdad[verdad["tipo_amenaza"] == tipo].set_index("sector_id")["susceptibilidad_real"]
        h_matriz[tipo] = v.reindex(sectores["sector_id"]).to_numpy()
    # históricos
    filas_ev, imp_h = [], []
    alta = pd.to_datetime(ctx["fecha_alta"])
    for k, (eid, tipo, fecha, sev) in enumerate(EVENTOS_HISTORICOS):
        rng = _rng_evento(seed, k)
        inten = _intensidades(tipo, sev, rng)
        filas_ev.append((eid, tipo, fecha, sev, inten["costa"], inten["sierra"], inten["selva_alta"]))
        res = simular_impacto(ctx, h_matriz, tipo, inten, rng)
        res = res[(alta <= pd.Timestamp(fecha)).to_numpy()]
        res.insert(0, "evento_id", eid)
        imp_h.append(res[["evento_id", "cliente_id", "afectado", "caida_ingreso_pct",
                          "dias_atraso_max_90d", "incumple_30d"]])
    eventos_h = pd.DataFrame(filas_ev, columns=[
        "evento_id", "tipo_amenaza", "fecha_inicio", "severidad_realizada",
        "intensidad_costa", "intensidad_sierra", "intensidad_selva_alta"])
    # backtest
    esc = escenarios.set_index("escenario_id")
    filas_b, imp_b = [], []
    sev_hist_max = max(e[3] for e in EVENTOS_HISTORICOS)
    for k, (eid, es_id, fecha) in enumerate(EVENTOS_BACKTEST):
        rng = _rng_evento(seed, 100 + k)
        e = esc.loc[es_id]
        sev = float(np.clip(e["severidad_nominal"] + rng.normal(0, e["sd_severidad"]), 0.05, 1.0))
        if e["severidad"] == "severa":
            sev = max(sev, sev_hist_max + 0.15)  # garantiza un evento mayor que todo el histórico
        inten = _intensidades(e["tipo_amenaza"], sev, rng)
        filas_b.append((eid, es_id, e["tipo_amenaza"], fecha, float(e["severidad_nominal"]), sev,
                        inten["costa"], inten["sierra"], inten["selva_alta"]))
        res = simular_impacto(ctx, h_matriz, e["tipo_amenaza"], inten, rng)
        res.insert(0, "evento_id", eid)
        imp_b.append(res)
    eventos_b = pd.DataFrame(filas_b, columns=[
        "evento_id", "escenario_id", "tipo_amenaza", "fecha_inicio_simulada", "severidad_nominal",
        "severidad_realizada", "intensidad_costa", "intensidad_sierra", "intensidad_selva_alta"])
    return eventos_h, pd.concat(imp_h, ignore_index=True), eventos_b, pd.concat(imp_b, ignore_index=True)


# --------------------------------------------------------------------------------------
# Orquestación
# --------------------------------------------------------------------------------------
def _redondear(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_float_dtype(df[col]):
            dec = 5 if col in ("lat", "lon") else (2 if "soles" in col else 4)
            df[col] = df[col].round(dec)
    return df


def generar_todo(seed: int = SEED_POR_DEFECTO, n_clientes: int = N_CLIENTES_POR_DEFECTO,
                 fecha_corte: str = FECHA_CORTE_POR_DEFECTO) -> Dict[str, pd.DataFrame]:
    """Genera todas las tablas en memoria (determinista por semilla)."""
    if n_clientes < 500:
        raise ValueError("n_clientes debe ser >= 500 para que las distribuciones tengan sentido")
    corte = pd.Timestamp(fecha_corte)
    rg = _rngs(seed)
    distritos = generar_distritos()
    actividades = generar_actividades()
    sectores = generar_sectores(distritos, rg["sectores"])
    verdad = generar_verdad_amenaza(sectores, distritos, rg["hazard"])
    mapa = generar_mapa_amenaza(sectores, verdad, rg["mapa"])
    escenarios = generar_escenarios()
    acciones = generar_acciones()
    agencias, clientes = generar_agencias_y_clientes(n_clientes, distritos, sectores, actividades, corte, rg["clientes"])
    creditos, clientes = generar_creditos(clientes, actividades, corte, rg["creditos"])
    # capacidad de visitas de cada agencia (supuesto: 1 gestor por ~350 clientes; 12 visitas/semana)
    n_cli = clientes.groupby("agencia_id").size().reindex(agencias["agencia_id"]).fillna(0).to_numpy()
    agencias["n_gestores"] = np.maximum(2, np.round(n_cli / 350.0)).astype(int)
    agencias["capacidad_visitas_semana"] = agencias["n_gestores"] * 12
    ctx = _contexto_clientes(clientes, creditos, sectores, distritos, actividades)
    ev_h, imp_h, ev_b, imp_b = generar_eventos_e_impacto(seed, ctx, verdad, sectores, escenarios, corte)
    clientes_out = clientes[["cliente_id", "agencia_id", "distrito_id", "sector_id", "lat", "lon",
                             "actividad_id", "fecha_alta", "antiguedad_meses", "ingreso_mensual_soles",
                             "tiene_ingreso_secundario", "tiene_seguro", "meses_reserva"]]
    tablas = {
        "agencias": agencias, "distritos": distritos, "sectores": sectores, "mapa_amenaza": mapa,
        "actividades": actividades, "clientes": clientes_out, "creditos": creditos,
        "escenarios": escenarios, "eventos_historicos": ev_h, "impacto_historico": imp_h,
        "acciones_preventivas": acciones, "eventos_backtest": ev_b, "impacto_backtest": imp_b,
        "verdad_amenaza_sector": verdad,
    }
    return {k: _redondear(v) for k, v in tablas.items()}


def diagnostico_embudo(tablas: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Diagnóstico de CALIDAD DEL DATASET (no es el modelo de exposición).

    «Expuesto» = cliente en un distrito con categoría alto/muy_alto en el mapa visible para el tipo
    de amenaza del evento. Muestra el embudo exposición → afectación → mora en cada evento de backtest.
    """
    cli = tablas["clientes"][["cliente_id", "distrito_id"]]
    saldo = tablas["creditos"].groupby("cliente_id")["saldo_soles"].sum().rename("saldo")
    cli = cli.merge(saldo, on="cliente_id")
    mapa = tablas["mapa_amenaza"]
    filas = []
    for ev in tablas["eventos_backtest"].itertuples(index=False):
        cat = mapa[mapa["tipo_amenaza"] == ev.tipo_amenaza][["distrito_id", "categoria"]]
        d = tablas["impacto_backtest"].query("evento_id == @ev.evento_id").merge(cli, on="cliente_id") \
            .merge(cat, on="distrito_id")
        exp = d["categoria"].isin(["alto", "muy_alto"])
        filas.append({
            "evento_id": ev.evento_id, "tipo_amenaza": ev.tipo_amenaza,
            "severidad_realizada": ev.severidad_realizada,
            "pct_saldo_expuesto": d.loc[exp, "saldo"].sum() / d["saldo"].sum(),
            "p_afectado_si_expuesto": d.loc[exp, "afectado"].mean(),
            "p_mora_si_expuesto": d.loc[exp, "incumple_30d"].mean(),
            "p_mora_si_no_expuesto": d.loc[~exp, "incumple_30d"].mean(),
            "saldo_en_mora_total_soles": d["saldo_en_mora_soles"].sum(),
            "saldo_en_mora_no_expuesto_soles": d.loc[~exp, "saldo_en_mora_soles"].sum(),
        })
    return pd.DataFrame(filas)


LEEME = """# Datos sintéticos RIE-01 (generados)

Generado por `retos/RIE-01/datos/generar.py` (versión {version}, semilla {seed}, {n} clientes, corte {corte}).
**Todo es sintético.** No hay personas reales: sin nombres, documentos ni domicilios. Los nombres de
distritos son geografía pública con coordenadas aproximadas; la huella de agencias y todos los
parámetros (sensibilidades, efectividad de acciones, severidades) son supuestos del generador, no
datos de la Caja. Material confidencial del proyecto: repo privado.

| Carpeta o archivo | Para qué sirve |
|---|---|
| `agencias, distritos, sectores, mapa_amenaza, actividades` | Geografía, mapa de amenaza visible (con error, resolución distrito) y catálogo de actividades |
| `clientes, creditos` | Cartera MYPE al corte, montos en S/ |
| `escenarios` | Escenarios hipotéticos ex ante (tipo × severidad) |
| `eventos_historicos, impacto_historico` | Eventos pasados y su efecto en clientes: **sirve para calibrar/entrenar** |
| `acciones_preventivas` | Catálogo de acciones con costos y efectividades de simulación (supuestos) |
| `backtest/` | **Verdad oculta** de eventos simulados. NO usar para entrenar ni para calibrar; solo para medir el KPI |

Diccionario completo: `retos/RIE-01/panorama.md` §b. Para regenerar:
`python retos/RIE-01/datos/generar.py --seed {seed} --n-clientes {n}`.
"""


def escribir(tablas: Dict[str, pd.DataFrame], salida: Path, seed: int, n_clientes: int,
             fecha_corte: str) -> dict:
    salida = Path(salida)
    manifiesto_archivos = {}
    for clave, rel in ARCHIVOS.items():
        ruta = salida / rel
        ruta.parent.mkdir(parents=True, exist_ok=True)
        tablas[clave].to_csv(ruta, index=False, lineterminator="\n", encoding="utf-8")
        manifiesto_archivos[rel] = {
            "filas": int(len(tablas[clave])),
            "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        }
    embudo = diagnostico_embudo(tablas).round(4).to_dict(orient="records")
    manifiesto = {
        "version_generador": VERSION_GENERADOR, "semilla": seed, "n_clientes": n_clientes,
        "fecha_corte": fecha_corte, "archivos": manifiesto_archivos,
        "diagnostico_embudo_backtest": embudo,
        "aviso": "Datos 100 % sintéticos. Los parámetros son supuestos del generador.",
    }
    (salida / "manifest.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    (salida / "LEEME.md").write_text(
        LEEME.format(version=VERSION_GENERADOR, seed=seed, n=n_clientes, corte=fecha_corte),
        encoding="utf-8")
    return manifiesto


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generador de datos sintéticos RIE-01 (sin red, con semilla).")
    p.add_argument("--seed", type=int, default=SEED_POR_DEFECTO)
    p.add_argument("--n-clientes", type=int, default=N_CLIENTES_POR_DEFECTO)
    p.add_argument("--fecha-corte", default=FECHA_CORTE_POR_DEFECTO)
    p.add_argument("--out", type=Path, default=SALIDA_POR_DEFECTO)
    a = p.parse_args(argv)
    tablas = generar_todo(a.seed, a.n_clientes, a.fecha_corte)
    man = escribir(tablas, a.out, a.seed, a.n_clientes, a.fecha_corte)
    print(f"RIE-01: {len(tablas)} tablas escritas en {a.out}")
    for rel, info in man["archivos"].items():
        print(f"  {rel:<42} {info['filas']:>9,} filas")
    print("Embudo de calidad (distrito alto/muy alto como «expuesto»):")
    print(diagnostico_embudo(tablas).round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
