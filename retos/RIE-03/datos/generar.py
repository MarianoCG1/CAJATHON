#!/usr/bin/env python
"""Generador de datos sintéticos para RIE-03 «Anticipar el deterioro de pago antes del atraso».

Produce una cartera MYPE ficticia, plausible para una caja municipal peruana (montos en S/,
agencias en La Libertad), con trayectorias de deterioro GRADUAL inyectadas de forma
controlada, fluctuaciones NORMALES (para medir falsos positivos) y casos de control
(pagador tardío habitual, shock abrupto). Todo es ficticio: no hay personas, documentos,
teléfonos ni nombres reales, y los identificadores son secuenciales (CLI-00001, ...).

Reproducible: misma semilla + mismos parámetros => mismos CSV, byte a byte.
Sin red, solo numpy y pandas.

Uso:
    python retos/RIE-03/datos/generar.py                      # 5,000 clientes, semilla fija
    python retos/RIE-03/datos/generar.py --n-clientes 1000 --semilla 7 --salida /ruta/otra

Este script es una herramienta de datos preexistente. NO contiene el modelo de riesgo, el agente,
la API, la interfaz ni el backtest, que se construyen en la fase presencial.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

VERSION_GENERADOR = "1.0.0"
SEMILLA_DEFECTO = 20261203
INICIO = pd.Timestamp("2024-01-01")
INICIO_NP = np.datetime64("2024-01-01", "D")
N_MESES_DEFECTO = 34  # 2024-01 .. 2026-10

TRAYECTORIAS = (
    "estable",
    "fluctuante",
    "pagador_tardio",
    "deterioro_gradual",
    "shock_abrupto",
)
MEZCLA_DEFECTO = {
    "estable": 0.655,
    "fluctuante": 0.18,
    "pagador_tardio": 0.07,
    "deterioro_gradual": 0.07,
    "shock_abrupto": 0.025,
}
# Volatilidad mensual del ingreso (sigma del ruido AR(1)) por trayectoria. (supuesto)
SIGMA_RUIDO = {
    "estable": 0.08,
    "fluctuante": 0.18,
    "pagador_tardio": 0.08,
    "deterioro_gradual": 0.10,
    "shock_abrupto": 0.10,
}

# --- Geografía (nombres geográficos reales, agencias FICTICIAS) -----------------------------
AGENCIAS = [
    # id, nombre, provincia, distrito, zona, peso
    ("AG-01", "Sintética Trujillo Centro", "Trujillo", "Trujillo", "urbana", 0.20),
    ("AG-02", "Sintética El Porvenir", "Trujillo", "El Porvenir", "urbana", 0.14),
    ("AG-03", "Sintética La Esperanza", "Trujillo", "La Esperanza", "urbana", 0.13),
    ("AG-04", "Sintética Víctor Larco", "Trujillo", "Víctor Larco Herrera", "urbana", 0.10),
    ("AG-05", "Sintética Chepén", "Chepén", "Chepén", "periurbana", 0.09),
    ("AG-06", "Sintética Pacasmayo", "Pacasmayo", "Pacasmayo", "periurbana", 0.07),
    ("AG-07", "Sintética Huamachuco", "Sánchez Carrión", "Huamachuco", "rural", 0.09),
    ("AG-08", "Sintética Casa Grande", "Ascope", "Casa Grande", "rural", 0.07),
    ("AG-09", "Sintética Virú", "Virú", "Virú", "rural", 0.06),
    ("AG-10", "Sintética Otuzco", "Otuzco", "Otuzco", "rural", 0.05),
]
ZONAS = ("urbana", "periurbana", "rural")

SECTORES = ("comercio", "servicios", "agropecuario", "produccion", "transporte")
SECTOR_PROB_POR_ZONA = {
    "urbana": [0.46, 0.24, 0.04, 0.18, 0.08],
    "periurbana": [0.38, 0.18, 0.20, 0.14, 0.10],
    "rural": [0.22, 0.10, 0.46, 0.08, 0.14],
}
SECTOR_MULT_INGRESO = np.array([1.00, 1.05, 0.85, 1.10, 1.25])
# Estacionalidad mensual (ene..dic) de ingresos por sector; se normaliza a media 1. (supuesto)
_ESTACIONALIDAD = {
    "comercio": [0.90, 0.85, 0.95, 0.95, 1.00, 1.00, 1.10, 1.00, 0.95, 1.00, 1.05, 1.25],
    "servicios": [0.95, 0.95, 1.00, 1.00, 1.00, 1.00, 1.05, 1.00, 1.00, 1.00, 1.00, 1.05],
    "agropecuario": [0.75, 0.80, 1.00, 1.25, 1.35, 1.20, 1.00, 0.90, 0.85, 0.90, 0.95, 1.05],
    "produccion": [0.85, 0.85, 0.95, 1.00, 1.00, 1.00, 1.10, 1.10, 1.00, 1.05, 1.00, 1.10],
    "transporte": [0.90, 0.90, 1.00, 1.00, 1.00, 1.00, 1.10, 1.05, 1.00, 1.00, 1.00, 1.05],
}
ESTACIONALIDAD = np.array(
    [np.array(_ESTACIONALIDAD[s]) / np.mean(_ESTACIONALIDAD[s]) for s in SECTORES]
)

CANALES = ("whatsapp", "llamada", "visita", "sms")
FRANJAS = ("manana", "tarde", "noche", "fin_de_semana")
RANGOS_EDAD = ("18-29", "30-39", "40-49", "50-59", "60+")
PLAZOS = np.array([6, 12, 18, 24, 36])
PLAZOS_PROB = [0.07, 0.38, 0.20, 0.25, 0.10]

# --- Diccionario de datos (también se escribe como diccionario.csv) --------------------------
DICCIONARIO: dict[str, list[tuple[str, str, str]]] = {
    "agencias": [
        ("agencia_id", "str", "Identificador de agencia ficticia (AG-01..AG-10)."),
        ("nombre", "str", "Nombre ficticio de la agencia."),
        ("provincia", "str", "Provincia de La Libertad (geografía real, agencia ficticia)."),
        ("distrito", "str", "Distrito."),
        ("zona", "str", "urbana | periurbana | rural."),
    ],
    "analistas": [
        ("analista_id", "str", "Identificador ANA-001.. (sin nombres reales)."),
        ("agencia_id", "str", "Agencia a la que pertenece."),
        ("antiguedad_meses", "int", "Antigüedad del analista en meses."),
    ],
    "clientes": [
        ("cliente_id", "str", "Identificador CLI-00001.. (ficticio)."),
        ("agencia_id", "str", "Agencia de atención."),
        ("analista_id", "str", "Analista (gestor) asignado."),
        ("sector", "str", "comercio | servicios | agropecuario | produccion | transporte."),
        ("zona", "str", "Zona de la agencia."),
        ("sexo", "str", "F | M. SOLO para auditoría de sesgos; no usar como variable del modelo."),
        ("rango_edad", "str", "Tramo de edad. SOLO para auditoría de sesgos; no usar en el modelo."),
        ("antiguedad_cliente_meses", "int", "Meses como cliente al 2024-01-01."),
        ("n_creditos_previos", "int", "Créditos cancelados antes del vigente."),
        ("tiene_cuenta_ahorros", "int", "1 si tiene cuenta de ahorros en la Caja (habilita señales de cuenta)."),
        ("tiene_billetera_digital", "int", "1 si recibe cobros por billetera digital/QR."),
        ("tiene_whatsapp", "int", "1 si es contactable por WhatsApp."),
        ("canal_preferido", "str", "whatsapp | llamada | visita | sms."),
        ("mejor_franja_contacto", "str", "manana | tarde | noche | fin_de_semana."),
    ],
    "creditos": [
        ("credito_id", "str", "Identificador CRE-00001.. (un crédito vigente por cliente)."),
        ("cliente_id", "str", "Cliente titular."),
        ("producto", "str", "capital_trabajo | activo_fijo | agropecuario."),
        ("monto_desembolsado", "float", "Monto en S/."),
        ("fecha_desembolso", "date", "Fecha de desembolso (puede ser anterior a 2024-01-01)."),
        ("plazo_meses", "int", "Número de cuotas mensuales."),
        ("tea", "float", "Tasa efectiva anual (0-1). (supuesto)"),
        ("cuota_mensual", "float", "Cuota fija en S/ (método francés)."),
        ("dia_vencimiento", "int", "Día del mes de vencimiento (1-28)."),
        ("ingreso_neto_evaluacion", "float", "Ingreso neto mensual estimado por el analista al evaluar, S/."),
        ("cuota_ingreso_origen", "float", "cuota_mensual / ingreso_neto_evaluacion al originar."),
    ],
    "cuotas": [
        ("credito_id", "str", "Crédito."),
        ("nro_cuota", "int", "Número de cuota (1..plazo)."),
        ("fecha_vencimiento", "date", "Vencimiento programado."),
        ("monto_cuota", "float", "Monto de la cuota en S/."),
        ("fecha_primer_pago", "date", "Fecha del primer abono a la cuota (vacío si aún no hay abono hasta el corte final)."),
        ("monto_primer_pago", "float", "Monto del primer abono (< monto_cuota = pago parcial)."),
        ("fecha_cancelacion", "date", "Fecha en que se cancela la cuota completa (vacío si sigue impaga al corte final)."),
        ("dias_atraso_cancelacion", "int", "fecha_cancelacion - fecha_vencimiento, en días, mínimo 0 (vacío si impaga)."),
    ],
    "saldos_mensuales": [
        ("credito_id", "str", "Crédito."),
        ("periodo", "str", "Mes AAAA-MM."),
        ("fecha_corte", "date", "Último día del mes."),
        ("saldo_capital", "float", "Capital pendiente al corte, S/."),
        ("saldo_vencido", "float", "Suma de cuotas vencidas impagas al corte, S/."),
        ("dias_atraso_corte", "int", "Días de atraso de la cuota impaga más antigua al corte (0 si al día)."),
        ("calificacion", "str", "normal (0-8) | cpp (9-30) | deficiente (31-60) | dudoso (61-120) | perdida (>120). Tramos típicos de MYPE (supuesto)."),
    ],
    "senales_mensuales": [
        ("credito_id", "str", "Crédito."),
        ("cliente_id", "str", "Cliente."),
        ("periodo", "str", "Mes AAAA-MM; el dato se conoce al cierre del mes (fecha_corte)."),
        ("fecha_corte", "date", "Último día del mes."),
        ("abonos_cuenta_mes", "float", "Suma de abonos a la cuenta de ahorros en el mes, S/ (vacío sin cuenta o dato faltante)."),
        ("n_operaciones_cuenta_mes", "int", "Número de operaciones de la cuenta (vacío sin cuenta o dato faltante)."),
        ("saldo_promedio_cuenta_mes", "float", "Saldo promedio de la cuenta de ahorros, S/ (vacío sin cuenta o dato faltante)."),
        ("cobros_digitales_mes", "float", "Cobros por billetera digital/QR en el mes, S/ (vacío si no usa)."),
        ("consultas_otras_entidades_mes", "int", "Consultas de otras entidades a la central de riesgo en el mes (sintético)."),
        ("deuda_otras_entidades", "float", "Deuda total en otras entidades, S/ (0 si no tiene)."),
        ("n_entidades_con_deuda", "int", "Número de otras entidades con deuda."),
    ],
    "gestiones": [
        ("gestion_id", "str", "Identificador GES-0000001.."),
        ("credito_id", "str", "Crédito."),
        ("fecha", "date", "Fecha de la gestión."),
        ("canal", "str", "whatsapp | llamada | visita | sms."),
        ("tipo", "str", "recordatorio | cobranza. Política REACTIVA actual simulada (supuesto)."),
        ("dias_atraso_al_gestionar", "int", "Días de atraso de la cuota al gestionar (5, 15 o 30)."),
        ("resultado", "str", "contactado_promesa_pago | contactado_sin_compromiso | no_contesta."),
    ],
    "verdad_terreno": [
        ("credito_id", "str", "Crédito. SOLO para evaluar/backtest; NUNCA como variable del modelo."),
        ("cliente_id", "str", "Cliente."),
        ("trayectoria", "str", "estable | fluctuante | pagador_tardio | deterioro_gradual | shock_abrupto."),
        ("mes_inicio_deterioro", "str", "AAAA-MM en que empieza la caída de ingresos (vacío si no aplica). Para medir anticipación."),
        ("fecha_primer_atraso_8d", "date", "Primera fecha con atraso > 8 días (vacío si nunca hasta el corte final)."),
        ("fecha_primer_atraso_30d", "date", "Primera fecha con atraso > 30 días (vacío si nunca hasta el corte final)."),
    ],
}


@dataclass(frozen=True)
class Config:
    n_clientes: int = 5000
    semilla: int = SEMILLA_DEFECTO
    n_meses: int = N_MESES_DEFECTO
    mezcla: dict = field(default_factory=lambda: dict(MEZCLA_DEFECTO))
    clientes_por_analista: int = 125

    @property
    def fin(self) -> pd.Timestamp:
        return (INICIO + pd.offsets.MonthEnd(self.n_meses)).normalize()


class Calendario:
    """Equivalencias entre índice de mes (0 = 2024-01) y días desde 2024-01-01."""

    def __init__(self, n_meses: int, holgura: int = 40):
        self.n = n_meses
        self.h = holgura
        periodos = pd.period_range(
            start=pd.Period("2024-01", freq="M") - holgura, periods=n_meses + holgura + 3, freq="M"
        )
        self._dia_inicio = np.asarray((periodos.to_timestamp() - INICIO).days, dtype=np.int64)
        self._periodos = periodos
        self.fin_dia = int(self.dia_fin_mes(n_meses - 1))

    def dia_inicio_mes(self, m):
        return self._dia_inicio[np.asarray(m) + self.h]

    def dia_fin_mes(self, m):
        return self._dia_inicio[np.asarray(m) + 1 + self.h] - 1

    def dia_vencimiento(self, m, dia):
        return self.dia_inicio_mes(m) + np.asarray(dia) - 1

    def periodo_str(self, m) -> np.ndarray:
        idx = np.asarray(m) + self.h
        return np.asarray(self._periodos.strftime("%Y-%m"))[idx]


def a_fecha(dias: np.ndarray) -> np.ndarray:
    """Días desde 2024-01-01 a datetime64[D]; valores no finitos (>= INF_DIA) -> NaT."""
    dias = np.asarray(dias, dtype=np.int64)
    out = INICIO_NP + dias.astype("timedelta64[D]")
    return np.where(dias >= INF_DIA, np.datetime64("NaT"), out)


INF_DIA = 10**9


# ---------------------------------------------------------------------------------------------
# Tablas estáticas
# ---------------------------------------------------------------------------------------------
def _elegir_filas(rng: np.random.Generator, probs: np.ndarray) -> np.ndarray:
    """Una categoría por fila, con probabilidades por fila (n, k)."""
    u = rng.random(probs.shape[0])[:, None]
    return (u > np.cumsum(probs, axis=1)).sum(axis=1).clip(max=probs.shape[1] - 1)


def _tabla_agencias() -> pd.DataFrame:
    return pd.DataFrame(
        [(a[0], a[1], a[2], a[3], a[4]) for a in AGENCIAS],
        columns=["agencia_id", "nombre", "provincia", "distrito", "zona"],
    )


def _tabla_analistas(rng: np.random.Generator, cfg: Config) -> pd.DataFrame:
    n_ana = max(len(AGENCIAS), int(np.ceil(cfg.n_clientes / cfg.clientes_por_analista)))
    pesos = np.array([a[5] for a in AGENCIAS])
    # al menos 1 por agencia; el resto, proporcional al peso
    extra = n_ana - len(AGENCIAS)
    por_agencia = np.ones(len(AGENCIAS), dtype=int)
    if extra > 0:
        por_agencia += rng.multinomial(extra, pesos / pesos.sum())
    filas = []
    k = 1
    for (aid, *_), cnt in zip(AGENCIAS, por_agencia):
        for _ in range(int(cnt)):
            filas.append((f"ANA-{k:03d}", aid, int(rng.integers(6, 97))))
            k += 1
    return pd.DataFrame(filas, columns=["analista_id", "agencia_id", "antiguedad_meses"])


def _tabla_clientes(rng: np.random.Generator, cfg: Config, analistas: pd.DataFrame) -> pd.DataFrame:
    n = cfg.n_clientes
    pesos = np.array([a[5] for a in AGENCIAS])
    ag_idx = rng.choice(len(AGENCIAS), size=n, p=pesos / pesos.sum())
    agencia_id = np.array([a[0] for a in AGENCIAS])[ag_idx]
    zona = np.array([a[4] for a in AGENCIAS])[ag_idx]

    sector_probs = np.array([SECTOR_PROB_POR_ZONA[z] for z in zona])
    sector_idx = _elegir_filas(rng, sector_probs)

    # analista: uniforme entre los de la agencia
    analista_id = np.empty(n, dtype=object)
    for aid in np.unique(agencia_id):
        ids = analistas.loc[analistas.agencia_id == aid, "analista_id"].to_numpy()
        mask = agencia_id == aid
        analista_id[mask] = rng.choice(ids, size=int(mask.sum()))

    # Variables sensibles: INDEPENDIENTES del resultado por construcción (sirven para auditar sesgos).
    sexo = np.where(rng.random(n) < 0.52, "F", "M")
    rango_edad = np.array(RANGOS_EDAD)[_elegir_filas(rng, np.tile([0.12, 0.28, 0.30, 0.21, 0.09], (n, 1)))]

    antig = np.clip(np.round(rng.lognormal(np.log(36), 0.7, n)), 1, 180).astype(int)
    n_prev = np.clip(np.round(antig / 30 + rng.poisson(0.4, n)), 0, 6).astype(int)

    p_cuenta = np.select([zona == "urbana", zona == "periurbana"], [0.90, 0.82], default=0.72)
    tiene_cuenta = (rng.random(n) < p_cuenta).astype(int)
    p_billetera = np.select([zona == "urbana", zona == "periurbana"], [0.62, 0.48], default=0.30)
    tiene_billetera = (rng.random(n) < p_billetera).astype(int)
    p_wa = np.select([zona == "urbana", zona == "periurbana"], [0.92, 0.80], default=0.66)
    tiene_wa = (rng.random(n) < p_wa).astype(int)

    probs_canal = np.where(
        tiene_wa[:, None] == 1,
        np.array([0.55, 0.25, 0.15, 0.05]),
        np.array([0.00, 0.48, 0.37, 0.15]),
    )
    probs_canal = np.where(
        (zona == "rural")[:, None] & (tiene_wa[:, None] == 1),
        np.array([0.42, 0.25, 0.28, 0.05]),
        probs_canal,
    )
    canal = np.array(CANALES)[_elegir_filas(rng, probs_canal)]
    franja = np.array(FRANJAS)[_elegir_filas(rng, np.tile([0.35, 0.30, 0.20, 0.15], (n, 1)))]

    df = pd.DataFrame(
        {
            "cliente_id": [f"CLI-{i + 1:05d}" for i in range(n)],
            "agencia_id": agencia_id,
            "analista_id": analista_id,
            "sector": np.array(SECTORES)[sector_idx],
            "zona": zona,
            "sexo": sexo,
            "rango_edad": rango_edad,
            "antiguedad_cliente_meses": antig,
            "n_creditos_previos": n_prev,
            "tiene_cuenta_ahorros": tiene_cuenta,
            "tiene_billetera_digital": tiene_billetera,
            "tiene_whatsapp": tiene_wa,
            "canal_preferido": canal,
            "mejor_franja_contacto": franja,
        }
    )
    return df


# ---------------------------------------------------------------------------------------------
# Dinámica por cliente
# ---------------------------------------------------------------------------------------------
def _asignar_tipos(rng, n, mezcla):
    """Trayectoria de cada cliente con conteos exactos según la mezcla (barajados)."""
    tipos = list(mezcla.keys())
    p = np.array([mezcla[t] for t in tipos], dtype=float)
    p = p / p.sum()
    cuentas = np.floor(p * n).astype(int)
    resto = n - cuentas.sum()
    cuentas[np.argsort(-(p * n - cuentas))[:resto]] += 1
    arr = np.repeat(np.array(tipos, dtype=object), cuentas)
    rng.shuffle(arr)
    return arr


def _inicio_deterioro(rng, tipo, d, plazo, n_meses):
    """Mes de inicio del deterioro; el crédito debe seguir vivo y quedar tiempo para observar el atraso."""
    if tipo == "deterioro_gradual":
        lo, hi = max(d, 0) + 4, min(n_meses - 1 - 9, d + plazo - 4)
    elif tipo == "shock_abrupto":
        lo, hi = max(d, 0) + 4, min(n_meses - 1 - 5, d + plazo - 3)
    else:
        return None
    return int(rng.integers(lo, hi + 1))


def _perfil_ingreso(rng, tipo, onset, d, plazo, n_meses, r0, tau):
    """Nivel de ingreso (multiplicador), progreso de deterioro y máscara de caídas transitorias."""
    ms = np.arange(d, n_meses)
    nivel = np.ones(ms.size)
    prog = np.zeros(ms.size)
    dip = np.zeros(ms.size, dtype=bool)
    if tipo == "deterioro_gradual":
        largo = int(rng.integers(4, 10))
        depth = float(np.clip(1 - r0 / (tau + rng.uniform(0.25, 0.70)), 0.30, 0.75))
        prog = np.clip((ms - onset + 1) / largo, 0, 1)
        nivel = 1 - depth * prog
    elif tipo == "shock_abrupto":
        depth = float(np.clip(1 - r0 / (tau + rng.uniform(0.30, 0.90)), 0.50, 0.85))
        prog = (ms >= onset).astype(float)
        nivel = 1 - depth * prog
    elif tipo == "fluctuante":
        lo, hi = max(d, 0) + 2, min(n_meses - 2, d + plazo - 1)
        if hi >= lo:
            for _ in range(int(rng.choice([1, 2, 3], p=[0.45, 0.35, 0.20]))):
                s = int(rng.integers(lo, hi + 1))
                dur = int(rng.integers(1, 4))
                depth = rng.uniform(0.12, 0.33)
                sel = (ms >= s) & (ms < s + dur)
                nivel = np.where(sel, nivel * (1 - depth), nivel)
                dip |= sel
    return ms, nivel, prog, dip


def _ruido_ar1(rng, size, sigma):
    z = rng.normal(0, sigma, size)
    e = np.zeros(size)
    for t in range(size):
        e[t] = (0.5 * e[t - 1] if t else 0.0) + z[t] * np.sqrt(0.75)
    return e


def _simular(cfg: Config) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(cfg.semilla)
    cal = Calendario(cfg.n_meses)
    n_m = cfg.n_meses
    fin_dia = cal.fin_dia

    agencias = _tabla_agencias()
    analistas = _tabla_analistas(rng, cfg)
    clientes = _tabla_clientes(rng, cfg, analistas)
    n = cfg.n_clientes

    sector_idx = clientes["sector"].map({s: i for i, s in enumerate(SECTORES)}).to_numpy()
    ingreso0 = np.clip(rng.lognormal(np.log(2800), 0.5, n) * SECTOR_MULT_INGRESO[sector_idx], 900, 20000)
    margen = rng.uniform(0.18, 0.35, n)
    ventas0 = ingreso0 / margen
    tau = np.clip(rng.normal(0.52, 0.07, n), 0.38, 0.75)  # tolerancia personal a la carga de cuota
    r0 = rng.uniform(0.15, 0.38, n)
    tipos_cli = _asignar_tipos(rng, n, cfg.mezcla)
    largo = np.isin(tipos_cli, ("deterioro_gradual", "shock_abrupto"))
    p_corto = np.array(PLAZOS_PROB)
    p_largo = np.where(PLAZOS >= 12, p_corto, 0.0)
    plazos = np.where(
        largo,
        rng.choice(PLAZOS, size=n, p=p_largo / p_largo.sum()),
        rng.choice(PLAZOS, size=n, p=p_corto),
    )
    tem_hint = 0.035
    af_hint = (1 - (1 + tem_hint) ** (-plazos.astype(float))) / tem_hint
    monto = np.clip(np.round(r0 * ingreso0 * af_hint / 100) * 100, 800, 80000)
    tea = np.clip(0.60 - 0.09 * (np.log10(monto) - 3) + rng.normal(0, 0.03, n), 0.24, 0.62)
    tem = (1 + tea) ** (1 / 12) - 1
    af = (1 - (1 + tem) ** (-plazos.astype(float))) / tem
    cuota = np.round(monto / af, 2)
    dia_venc = rng.integers(1, 29, n)
    ingreso_eval = np.round(ingreso0 * rng.uniform(0.92, 1.10, n), 2)
    d_lo = np.maximum(-plazos + 8, -20)
    d_hi = np.where(largo, n_m - 14, n_m - 10)
    d_all = rng.integers(d_lo, d_hi + 1)
    # producto según sector
    prod_u = rng.random(n)
    producto = np.where(
        sector_idx == 2,
        np.where(prod_u < 0.7, "agropecuario", "capital_trabajo"),
        np.where(prod_u < 0.78, "capital_trabajo", "activo_fijo"),
    )
    tiene_cuenta = clientes["tiene_cuenta_ahorros"].to_numpy()
    tiene_bill = clientes["tiene_billetera_digital"].to_numpy()
    canal_pref = clientes["canal_preferido"].to_numpy()

    creditos = pd.DataFrame(
        {
            "credito_id": [f"CRE-{i + 1:05d}" for i in range(n)],
            "cliente_id": clientes["cliente_id"].to_numpy(),
            "producto": producto,
            "monto_desembolsado": monto,
            "fecha_desembolso": a_fecha(
                cal.dia_vencimiento(d_all, np.minimum(dia_venc, 28))
            ),
            "plazo_meses": plazos,
            "tea": np.round(tea, 4),
            "cuota_mensual": cuota,
            "dia_vencimiento": dia_venc,
            "ingreso_neto_evaluacion": ingreso_eval,
            "cuota_ingreso_origen": np.round(cuota / ingreso_eval, 4),
        }
    )

    acc = {
        k: []
        for k in (
            "cuotas",
            "saldos",
            "senales",
            "gestiones",
            "verdad",
        )
    }

    for i in range(n):
        d, plazo = int(d_all[i]), int(plazos[i])
        tipo = str(tipos_cli[i])
        onset = _inicio_deterioro(rng, tipo, d, plazo, n_m)
        ms, nivel, prog, dip = _perfil_ingreso(rng, tipo, onset, d, plazo, n_m, float(r0[i]), float(tau[i]))
        j_tot = ms.size
        ruido = _ruido_ar1(rng, j_tot, SIGMA_RUIDO[tipo])
        estac = ESTACIONALIDAD[sector_idx[i]][ms % 12]
        mult = nivel * estac * np.exp(ruido)  # ingreso realizado / ingreso base
        ingreso_m = ingreso0[i] * mult

        # ---- cuotas y pagos ----
        K = min(plazo, n_m - 1 - d)
        ks = np.arange(1, K + 1)
        venc = cal.dia_vencimiento(d + ks, dia_venc[i])
        r = cuota[i] / ingreso_m[ks]
        u = np.clip((r - tau[i]) / 0.25, 0, None)
        if tipo == "pagador_tardio":
            habito_media = rng.uniform(3.5, 8.0)
            habito = rng.poisson(habito_media, K)
        else:
            habito = np.minimum(rng.poisson(0.5, K), 3)
        estres = np.where(u > 0, np.round(rng.gamma(1.5, 2 + 25 * np.power(u, 1.5))), 0).astype(int)
        lag = habito + estres
        lag = np.minimum(lag, 25) if tipo == "pagador_tardio" else np.minimum(lag, 400)
        abandona_draw = rng.random(K) < 0.6
        parcial_p = np.clip(0.06 + 0.5 * np.minimum(u, 1.0), 0, 0.6)
        es_parcial = (rng.random(K) < parcial_p) & (lag >= 2)
        frac = rng.uniform(0.4, 0.9, K)
        frac_t = rng.uniform(0.25, 0.70, K)

        cancel = np.full(K, INF_DIA, dtype=np.int64)
        primer = np.full(K, INF_DIA, dtype=np.int64)
        prev, abandono = 0, False
        for q in range(K):
            if abandono:
                continue
            if lag[q] > 60 and abandona_draw[q]:
                abandono = True
                continue
            c = max(int(venc[q]) + int(lag[q]), prev)
            prev = c
            if c <= fin_dia:
                cancel[q] = c
            if es_parcial[q]:
                p1 = min(int(venc[q] + np.floor(lag[q] * frac_t[q])), c)
                if p1 <= fin_dia:
                    primer[q] = p1
            elif c <= fin_dia:
                primer[q] = c
        monto_primer = np.where(primer < INF_DIA, np.where(es_parcial, np.round(cuota[i] * frac, 2), cuota[i]), np.nan)

        sel_out = venc >= 0  # solo cuotas con vencimiento dentro de la ventana de observación
        cid = f"CRE-{i + 1:05d}"
        if sel_out.any():
            acc["cuotas"].append(
                pd.DataFrame(
                    {
                        "credito_id": cid,
                        "nro_cuota": ks[sel_out],
                        "fecha_vencimiento": a_fecha(venc[sel_out]),
                        "monto_cuota": cuota[i],
                        "fecha_primer_pago": a_fecha(primer[sel_out]),
                        "monto_primer_pago": monto_primer[sel_out],
                        "fecha_cancelacion": a_fecha(cancel[sel_out]),
                        "dias_atraso_cancelacion": np.where(
                            cancel[sel_out] < INF_DIA, np.maximum(cancel[sel_out] - venc[sel_out], 0), -1
                        ),
                    }
                )
            )

        # ---- saldos mensuales ----
        i_m = float(tem[i])
        cap_k = (cuota[i] - monto[i] * i_m) * (1 + i_m) ** (ks - 1)
        m_ini = max(d, 0)
        meses = np.arange(m_ini, n_m)
        cortes = cal.dia_fin_mes(meses)
        pagado = cancel[None, :] <= cortes[:, None]
        saldo_cap = np.maximum(monto[i] - (pagado * cap_k[None, :]).sum(axis=1), 0)
        impaga_venc = (venc[None, :] <= cortes[:, None]) & (cancel[None, :] > cortes[:, None])
        hay = impaga_venc.any(axis=1)
        primera = impaga_venc.argmax(axis=1)
        dias_atraso = np.where(hay, cortes - venc[primera], 0)
        saldo_venc = (impaga_venc * cuota[i]).sum(axis=1)
        castigado = np.maximum.accumulate(dias_atraso > 180)  # castigo: sale de la cartera vigente
        vivo = (saldo_cap > 0.5) & ~castigado
        if vivo.any():
            calif = np.select(
                [dias_atraso <= 8, dias_atraso <= 30, dias_atraso <= 60, dias_atraso <= 120],
                ["normal", "cpp", "deficiente", "dudoso"],
                default="perdida",
            )
            per = cal.periodo_str(meses)
            acc["saldos"].append(
                pd.DataFrame(
                    {
                        "credito_id": cid,
                        "periodo": per[vivo],
                        "fecha_corte": a_fecha(cortes[vivo]),
                        "saldo_capital": np.round(saldo_cap[vivo], 2),
                        "saldo_vencido": np.round(saldo_venc[vivo], 2),
                        "dias_atraso_corte": dias_atraso[vivo].astype(int),
                        "calificacion": calif[vivo],
                    }
                )
            )

            # ---- señales mensuales (solo meses con crédito vivo) ----
            j = meses - d
            m_mult = mult[j]
            ventas = ventas0[i] * m_mult
            share = rng.uniform(0.30, 0.80)
            ops_base = rng.uniform(8, 60)
            saldo_base = ingreso0[i] * rng.uniform(0.3, 1.5)
            has_ext = rng.random() < 0.55
            deuda_base = ingreso0[i] * rng.uniform(1.0, 6.0) if has_ext else 0.0
            nj = meses.size
            abonos = ventas * share * np.exp(rng.normal(0, 0.10, nj))
            nops = rng.poisson(ops_base * np.sqrt(np.clip(m_mult, 0.05, None)))
            saldo_cta = saldo_base * np.power(np.clip(nivel[j], 0.05, None), 1.3) * np.sqrt(estac[j]) * np.exp(
                rng.normal(0, 0.15, nj)
            )
            cobros = ventas * rng.uniform(0.10, 0.50) * np.exp(rng.normal(0, 0.12, nj))
            lam_cons = 0.10 + 0.9 * prog[j] * (tipo == "deterioro_gradual") + 0.8 * prog[j] * (tipo == "shock_abrupto") + 0.15 * dip[j]
            if tipo == "pagador_tardio":
                lam_cons = lam_cons + 0.15
            consultas = rng.poisson(lam_cons)
            prog_prev = np.where(j > 0, prog[np.maximum(j - 1, 0)], 0.0)
            crecim = 0.9 * prog_prev * (tipo == "deterioro_gradual") + 0.3 * prog_prev * (tipo == "shock_abrupto")
            deuda = deuda_base * (1 + crecim) * np.exp(np.cumsum(rng.normal(0, 0.03, nj))) if has_ext else np.zeros(nj)
            n_ent = np.where(
                deuda > 0,
                np.clip(1 + rng.poisson(0.6) + (prog_prev > 0.5), 1, 5),
                0,
            )
            faltante = rng.random(nj) < 0.02
            sin_cta = np.full(nj, not tiene_cuenta[i]) | faltante
            sin_bill = np.full(nj, not tiene_bill[i]) | faltante
            acc["senales"].append(
                pd.DataFrame(
                    {
                        "credito_id": cid,
                        "cliente_id": clientes["cliente_id"].iat[i],
                        "periodo": per[vivo],
                        "fecha_corte": a_fecha(cortes[vivo]),
                        "abonos_cuenta_mes": np.where(sin_cta, np.nan, np.round(abonos, 2))[vivo],
                        "n_operaciones_cuenta_mes": np.where(sin_cta, -1, nops)[vivo],
                        "saldo_promedio_cuenta_mes": np.where(sin_cta, np.nan, np.round(saldo_cta, 2))[vivo],
                        "cobros_digitales_mes": np.where(sin_bill, np.nan, np.round(cobros, 2))[vivo],
                        "consultas_otras_entidades_mes": consultas[vivo],
                        "deuda_otras_entidades": np.round(deuda, 2)[vivo],
                        "n_entidades_con_deuda": n_ent[vivo],
                    }
                )
            )

        # ---- gestiones reactivas (línea base actual: se gestiona DESPUÉS del vencimiento) ----
        for off, tipo_g in ((5, "recordatorio"), (15, "cobranza"), (30, "cobranza")):
            fecha_g = venc + off
            cond = (cancel > fecha_g) & (fecha_g <= fin_dia) & sel_out
            if not cond.any():
                continue
            nq = int(cond.sum())
            if off == 30:
                canal_g = np.full(nq, "visita", dtype=object)
            else:
                igual = rng.random(nq) < 0.5
                alt = np.array(CANALES, dtype=object)[rng.integers(0, 4, nq)]
                canal_g = np.where(igual, canal_pref[i], alt)
            p_contacto = np.where(canal_g == canal_pref[i], 0.70, 0.35)
            contacto = rng.random(nq) < p_contacto
            promesa = rng.random(nq) < 0.55
            res = np.where(
                contacto, np.where(promesa, "contactado_promesa_pago", "contactado_sin_compromiso"), "no_contesta"
            )
            acc["gestiones"].append(
                pd.DataFrame(
                    {
                        "credito_id": cid,
                        "fecha": a_fecha(fecha_g[cond]),
                        "canal": canal_g,
                        "tipo": tipo_g,
                        "dias_atraso_al_gestionar": off,
                        "resultado": res,
                    }
                )
            )

        # ---- verdad de terreno ----
        v_out = venc[sel_out]
        c_out = cancel[sel_out]
        def _primer(umbral):
            mask = ((c_out >= INF_DIA) | (c_out - v_out > umbral)) & (v_out + umbral + 1 <= fin_dia)
            return int((v_out[mask] + umbral + 1).min()) if mask.any() else INF_DIA

        acc["verdad"].append(
            (
                cid,
                clientes["cliente_id"].iat[i],
                tipo,
                str(cal.periodo_str(onset)) if onset is not None else None,
                _primer(8),
                _primer(30),
            )
        )

    def _cat(lst, cols):
        return pd.concat(lst, ignore_index=True) if lst else pd.DataFrame(columns=cols)

    cuotas = _cat(acc["cuotas"], [c[0] for c in DICCIONARIO["cuotas"]])
    cuotas["dias_atraso_cancelacion"] = cuotas["dias_atraso_cancelacion"].astype("Int64").where(
        cuotas["dias_atraso_cancelacion"] >= 0, pd.NA
    )
    saldos = _cat(acc["saldos"], [c[0] for c in DICCIONARIO["saldos_mensuales"]])
    senales = _cat(acc["senales"], [c[0] for c in DICCIONARIO["senales_mensuales"]])
    senales["n_operaciones_cuenta_mes"] = senales["n_operaciones_cuenta_mes"].astype("Int64").where(
        senales["n_operaciones_cuenta_mes"] >= 0, pd.NA
    )
    gest = _cat(acc["gestiones"], [c[0] for c in DICCIONARIO["gestiones"]])
    gest = gest.sort_values(["fecha", "credito_id", "dias_atraso_al_gestionar"], kind="stable").reset_index(drop=True)
    gest.insert(0, "gestion_id", [f"GES-{k + 1:07d}" for k in range(len(gest))])
    verdad = pd.DataFrame(
        acc["verdad"],
        columns=["credito_id", "cliente_id", "trayectoria", "mes_inicio_deterioro", "d8", "d30"],
    )
    verdad["fecha_primer_atraso_8d"] = a_fecha(verdad.pop("d8").to_numpy())
    verdad["fecha_primer_atraso_30d"] = a_fecha(verdad.pop("d30").to_numpy())

    return {
        "agencias": agencias,
        "analistas": analistas,
        "clientes": clientes,
        "creditos": creditos,
        "cuotas": cuotas,
        "saldos_mensuales": saldos,
        "senales_mensuales": senales,
        "gestiones": gest,
        "verdad_terreno": verdad,
    }


def generar(cfg: Config | None = None) -> dict[str, pd.DataFrame]:
    """Genera todas las tablas en memoria (sin escribir a disco)."""
    return _simular(cfg or Config())


# ---------------------------------------------------------------------------------------------
# Salida
# ---------------------------------------------------------------------------------------------
def _diccionario_df() -> pd.DataFrame:
    return pd.DataFrame(
        [(t, c, tp, ds) for t, cols in DICCIONARIO.items() for c, tp, ds in cols],
        columns=["tabla", "columna", "tipo", "descripcion"],
    )


def _metadata(cfg: Config, tablas: dict[str, pd.DataFrame], hashes: dict[str, str]) -> dict:
    v = tablas["verdad_terreno"]
    n = len(v)
    realizada = (v["trayectoria"].value_counts() / n).round(4).to_dict()
    cortes = pd.period_range("2024-01", periods=cfg.n_meses, freq="M")
    return {
        "version_generador": VERSION_GENERADOR,
        "aviso": "Datos 100% sintéticos y ficticios. Sin personas, documentos ni contactos reales. "
        "Material de trabajo del equipo; no es información de la Caja.",
        "semilla": cfg.semilla,
        "n_clientes": cfg.n_clientes,
        "n_creditos": int(len(tablas["creditos"])),
        "ventana": {"inicio": "2024-01-01", "fin": str(cfg.fin.date()), "n_meses": cfg.n_meses},
        "mezcla_objetivo": cfg.mezcla,
        "mezcla_realizada": realizada,
        "prevalencia": {
            "clientes_con_atraso_8d": round(float(v["fecha_primer_atraso_8d"].notna().mean()), 4),
            "clientes_con_atraso_30d": round(float(v["fecha_primer_atraso_30d"].notna().mean()), 4),
        },
        "filas": {k: int(len(df)) for k, df in tablas.items()},
        "particion_temporal_sugerida": {
            "nota": "Etiqueta típica: pasa a atraso > 30 d en los próximos 60 d. Dejar un hueco (purga) igual al "
            "horizonte entre entrenamiento y validación.",
            "entrenamiento_cortes": [str(cortes[0].end_time.date()), "2025-06-30"],
            "validacion_cortes": ["2025-07-31", "2025-12-31"],
            "prueba_cortes": ["2026-01-31", "2026-08-31"],
            "sin_horizonte_completo": ["2026-09-30", "2026-10-31"],
        },
        "supuestos_clave": [
            "Un crédito vigente por cliente; cuotas mensuales fijas (método francés).",
            "El generador NO incluye efecto de intervención: el efecto preventivo es un parámetro "
            "del backtest, no un hecho de los datos.",
            "Las gestiones simuladas son la política REACTIVA actual (después del vencimiento) y no "
            "alteran los pagos.",
            "Tramos de atraso (0-8, 9-30, 31-60, 61-120, >120) y todas las distribuciones: supuestos "
            "a confirmar con el owner.",
        ],
        "sha256_csv": hashes,
    }


def escribir(tablas: dict[str, pd.DataFrame], cfg: Config, salida: Path) -> dict:
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    hashes: dict[str, str] = {}
    for nombre, df in {**tablas, "diccionario": _diccionario_df()}.items():
        ruta = salida / f"{nombre}.csv"
        df.to_csv(ruta, index=False, lineterminator="\n", date_format="%Y-%m-%d", encoding="utf-8")
        hashes[f"{nombre}.csv"] = hashlib.sha256(ruta.read_bytes()).hexdigest()
    meta = _metadata(cfg, tablas, hashes)
    (salida / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return meta


def main(argv: list[str] | None = None) -> int:
    aqui = Path(__file__).resolve().parent
    p = argparse.ArgumentParser(description="Genera la cartera sintética de RIE-03 (CSV).")
    p.add_argument("--n-clientes", type=int, default=5000)
    p.add_argument("--semilla", type=int, default=SEMILLA_DEFECTO)
    p.add_argument("--salida", type=Path, default=aqui / "sintetico")
    a = p.parse_args(argv)
    cfg = Config(n_clientes=a.n_clientes, semilla=a.semilla)
    tablas = generar(cfg)
    meta = escribir(tablas, cfg, a.salida)
    print(f"Escrito en {a.salida}")
    print(json.dumps({k: meta[k] for k in ("n_clientes", "filas", "mezcla_realizada", "prevalencia")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
