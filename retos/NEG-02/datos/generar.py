"""Generador de datos sintéticos para NEG-02 «Open Finance: competir en un ecosistema abierto».

Simula un ecosistema abierto ficticio: una Caja receptora (rol de Caja Trujillo) y cinco
entidades fuente ficticias; clientes con productos en varias entidades; transacciones;
catálogo de productos; consentimientos con alcance, vigencia y revocación; y una «verdad
de terreno» separada para medir el KPI (con y sin datos multientidad).

Reglas del proyecto:
- Todo es sintético: no hay personas, documentos, teléfonos ni entidades reales.
- Reproducible: misma semilla y mismos parámetros => mismos bytes (ver manifest.json).
- Sin red. Solo pandas y numpy.
- Esto NO es la funcionalidad crítica: no hay API, ni servicio de consentimiento, ni agente.
  Solo datos de entrada. La verdad de terreno (carpeta ``verdad/``) jamás se entrega al agente.

Uso:
    python retos/NEG-02/datos/generar.py
    python retos/NEG-02/datos/generar.py --semilla 7 --n-clientes 500 --salida /ruta/salida

Los parámetros de plausibilidad (tasas, montos, probabilidades) son SUPUESTOS del equipo, no
datos de la Caja ni del mercado. Se documentan en retos/NEG-02/panorama.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

VERSION_GENERADOR = "1.0"
SEMILLA_POR_DEFECTO = 20261121
TASA_CONSENTIMIENTO_POR_DEFECTO = 0.65   # SUPUESTO: P(un cliente comparte datos con la Caja)
N_CLIENTES_POR_DEFECTO = 2000
MESES_POR_DEFECTO = 6
FECHA_CORTE = date(2026, 10, 31)
SALIDA_POR_DEFECTO = Path(__file__).resolve().parent / "sintetico"

# ---------------------------------------------------------------------------
# Parámetros de las reglas de verdad de terreno (SUPUESTOS documentados)
# ---------------------------------------------------------------------------
UMBRAL_RATIO_SOBREENDEUDAMIENTO = 0.50   # cuota total / ingreso mensual real
CALIFICACIONES_RIESGO = ("DEFICIENTE", "DUDOSO", "PERDIDA")
CONSOL_MIN_CREDITOS_EXTERNOS = 2
CONSOL_MIN_SALDO_EXTERNO = 4000.0        # S/
CONSOL_TEA_MIN = 40.0                    # % TEA: al menos un crédito externo tan caro o más
CONSOL_RATIO_MIN = 0.15
CAPITAL_CRECIMIENTO_MIN = 0.15           # crecimiento de abonos (2.ª mitad vs. 1.ª mitad de la ventana)
CAPITAL_RATIO_MAX = 0.35
AHORRO_SALDO_MIN = 8000.0                # S/ en cuentas de ahorro externas de baja tasa
AHORRO_TEA_MAX = 2.5                     # % TEA
DOM_SHARE_MAX = 0.30                     # share de abonos que llega a la Caja
ABONOS_PROMEDIO_MIN = 800.0              # S/ por mes, para considerar que hay flujo observable

TIPOS_OPORTUNIDAD = (
    "CONSOLIDACION_DEUDA",
    "CAPITAL_TRABAJO_MYPE",
    "CAPTACION_AHORRO",
    "DOMICILIACION_INGRESOS",
    "RESTRICCION_SOBREENDEUDAMIENTO",
)

ALCANCES = ("PRODUCTOS", "SALDOS", "CONDICIONES", "TRANSACCIONES")
FINALIDADES = ("OFERTA_PRODUCTOS", "VISTA_FINANCIERA")

CATEGORIAS_CREDITO = ("CREDITO_MYPE", "CREDITO_CONSUMO", "CREDITO_CONSOLIDACION", "TARJETA_CREDITO")
CATEGORIAS_TRANSACCIONALES = ("CUENTA_AHORRO", "BILLETERA_DIGITAL")
SEGMENTOS = ("MYPE_COMERCIO", "MYPE_SERVICIOS", "MYPE_AGRO", "ASALARIADO", "INDEPENDIENTE")
SEGMENTOS_MYPE = ("MYPE_COMERCIO", "MYPE_SERVICIOS", "MYPE_AGRO")

# ---------------------------------------------------------------------------
# Esquema (también genera el diccionario de datos y lo valida la prueba)
# ---------------------------------------------------------------------------
COLUMNAS: dict[str, list[tuple[str, str, str]]] = {
    "entidades": [
        ("entidad_id", "str", "Identificador de la entidad (E00 = Caja receptora)."),
        ("nombre", "str", "Nombre FICTICIO de la entidad."),
        ("tipo", "str", "CAJA_MUNICIPAL, BANCO, FINANCIERA, COOPERATIVA o FINTECH."),
        ("rol_sandbox", "str", "RECEPTORA (consulta con consentimiento) o FUENTE (expone datos)."),
        ("ficticia", "bool", "Siempre True: ninguna entidad es real."),
    ],
    "catalogo_productos": [
        ("producto_id", "str", "Identificador del producto del catálogo."),
        ("entidad_id", "str", "Entidad que lo ofrece."),
        ("categoria", "str", "CREDITO_MYPE, CREDITO_CONSUMO, CREDITO_CONSOLIDACION, TARJETA_CREDITO, "
                              "CUENTA_AHORRO, BILLETERA_DIGITAL, DEPOSITO_PLAZO o SEGURO."),
        ("nombre", "str", "Nombre comercial ficticio."),
        ("tea_min_pct", "float", "TEA mínima del rango (%). SUPUESTO."),
        ("tea_max_pct", "float", "TEA máxima del rango (%). SUPUESTO."),
        ("plazo_min_meses", "int", "Plazo mínimo en meses (0 si no aplica)."),
        ("plazo_max_meses", "int", "Plazo máximo en meses (0 si no aplica)."),
        ("monto_min_pen", "float", "Monto mínimo en S/ (en tarjetas, línea mínima)."),
        ("monto_max_pen", "float", "Monto máximo en S/ (en tarjetas, línea máxima)."),
        ("es_oferta_caja", "bool", "True si el producto lo puede ofrecer la Caja receptora."),
        ("es_supuesto", "bool", "Siempre True: condiciones inventadas por el equipo, no tarifas reales."),
    ],
    "clientes": [
        ("cliente_id", "str", "Identificador sintético (C000001...)."),
        ("segmento", "str", "MYPE_COMERCIO, MYPE_SERVICIOS, MYPE_AGRO, ASALARIADO o INDEPENDIENTE."),
        ("actividad", "str", "Actividad genérica."),
        ("provincia", "str", "Provincia de La Libertad."),
        ("distrito", "str", "Distrito de La Libertad."),
        ("edad_rango", "str", "Rango de edad."),
        ("antiguedad_actividad_anios", "int", "Años de la actividad (vacío si no aplica)."),
        ("es_cliente_caja", "bool", "True si ya tiene productos en la Caja; False = prospecto."),
        ("fecha_alta_caja", "date", "Alta en la Caja (vacío en prospectos)."),
        ("ingreso_declarado_caja_pen", "float", "Ingreso mensual que declaró en la Caja, con ruido (vacío en prospectos)."),
        ("etiqueta_demo", "str", "Texto para mostrar en la demo (actividad · distrito). No es un nombre."),
    ],
    "productos_cliente": [
        ("producto_cliente_id", "str", "Identificador del contrato."),
        ("cliente_id", "str", "Cliente titular."),
        ("entidad_id", "str", "Entidad donde está el producto."),
        ("producto_id", "str", "Producto del catálogo."),
        ("categoria", "str", "Categoría del producto."),
        ("estado", "str", "ACTIVO, MORA (más de 8 días de atraso) o CANCELADO."),
        ("fecha_apertura", "date", "Apertura del contrato."),
        ("fecha_cierre", "date", "Cierre (solo CANCELADO)."),
        ("monto_original_pen", "float", "Monto desembolsado, línea aprobada (tarjeta) o depósito inicial."),
        ("saldo_actual_pen", "float", "Saldo de capital, utilizado (tarjeta) o saldo de la cuenta/depósito."),
        ("tasa_ea_pct", "float", "TEA vigente del contrato (%)."),
        ("plazo_meses", "int", "Plazo pactado (vacío en tarjetas, cuentas y billeteras)."),
        ("cuota_mensual_pen", "float", "Cuota mensual (crédito), pago mínimo (tarjeta) o prima (seguro)."),
        ("dias_atraso", "int", "Días de atraso a la fecha de corte."),
        ("calificacion", "str", "NORMAL, CPP, DEFICIENTE, DUDOSO o PERDIDA (solo créditos; tramos aproximados, SUPUESTO)."),
    ],
    "transacciones": [
        ("tx_id", "str", "Identificador del movimiento."),
        ("cliente_id", "str", "Cliente titular."),
        ("entidad_id", "str", "Entidad donde ocurre."),
        ("producto_cliente_id", "str", "Cuenta, billetera o crédito afectado."),
        ("fecha", "date", "Fecha del movimiento."),
        ("sentido", "str", "CREDITO (entra dinero) o DEBITO (sale)."),
        ("tipo", "str", "ABONO_SUELDO, ABONO_VENTAS, ABONO_TRANSFERENCIA, PAGO_CUOTA, PAGO_SERVICIOS, COMPRA, "
                        "RETIRO, TRANSFERENCIA_ENVIADA o PAGO_PROVEEDOR."),
        ("categoria", "str", "Rubro del gasto o SIN_CATEGORIA."),
        ("monto_pen", "float", "Monto en S/ (siempre positivo; el sentido indica la dirección)."),
    ],
    "consentimientos": [
        ("consentimiento_id", "str", "Identificador del consentimiento."),
        ("cliente_id", "str", "Titular de los datos."),
        ("entidad_receptora_id", "str", "Quien recibe los datos. E00 = Caja receptora."),
        ("entidad_fuente_id", "str", "Quien comparte los datos."),
        ("finalidad", "str", "OFERTA_PRODUCTOS (permite ofertar) o VISTA_FINANCIERA (solo mostrar al cliente)."),
        ("fecha_otorgado", "date", "Cuándo se otorgó."),
        ("plazo_dias", "int", "Vigencia pactada en días (90, 180 o 365)."),
        ("fecha_vencimiento", "date", "fecha_otorgado + plazo_dias."),
        ("fecha_revocado", "date", "Cuándo lo revocó el cliente (vacío si no)."),
        ("estado", "str", "VIGENTE, VENCIDO o REVOCADO a la fecha de corte."),
        ("historia_meses", "int", "Meses hacia atrás de transacciones que cubre (3, 6 o 12)."),
        ("canal", "str", "APP, AGENCIA o WEB."),
        ("version_texto", "str", "Versión del texto de consentimiento mostrado."),
        ("renueva_a", "str", "Consentimiento anterior que renueva (vacío si no es renovación)."),
    ],
    "consentimiento_alcances": [
        ("consentimiento_id", "str", "Consentimiento."),
        ("alcance", "str", "PRODUCTOS, SALDOS, CONDICIONES o TRANSACCIONES."),
    ],
    "consentimiento_eventos": [
        ("evento_id", "str", "Identificador del evento de auditoría."),
        ("consentimiento_id", "str", "Consentimiento."),
        ("tipo", "str", "OTORGADO, REVOCADO o VENCIDO."),
        ("fecha", "date", "Fecha del evento."),
    ],
    "alcances_campos": [
        ("alcance", "str", "Alcance de consentimiento."),
        ("tabla", "str", "Tabla de datos."),
        ("columna", "str", "Columna que ese alcance autoriza a ver."),
        ("descripcion", "str", "Qué revela."),
    ],
    "verdad_cliente": [
        ("cliente_id", "str", "Cliente."),
        ("ingreso_mensual_real_pen", "float", "Ingreso real latente (NO observable por la Caja)."),
        ("arquetipo_sobreendeudado", "bool", "Rasgo con el que se generó al cliente."),
        ("arquetipo_deuda_cara_dispersa", "bool", "Rasgo con el que se generó al cliente."),
        ("arquetipo_ahorrista_externo", "bool", "Rasgo con el que se generó al cliente."),
        ("arquetipo_ingresos_en_otra_entidad", "bool", "Rasgo con el que se generó al cliente."),
        ("arquetipo_crecimiento", "bool", "Rasgo con el que se generó al cliente."),
        ("n_entidades", "int", "Entidades distintas con productos no cancelados."),
        ("deuda_total_pen", "float", "Saldo de créditos activos en todas las entidades."),
        ("cuota_total_pen", "float", "Cuotas mensuales de créditos activos en todas las entidades."),
        ("ratio_cuota_ingreso", "float", "cuota_total / ingreso real."),
        ("n_creditos_externos", "int", "Créditos activos fuera de la Caja."),
        ("saldo_credito_externo_pen", "float", "Saldo de créditos activos fuera de la Caja."),
        ("tea_max_externa_pct", "float", "TEA máxima entre créditos externos activos."),
        ("ahorro_externo_baja_tasa_pen", "float", "Saldo en cuentas de ahorro externas con TEA baja."),
        ("abonos_prom_mensual_pen", "float", "Abonos promedio por mes, todas las entidades."),
        ("share_abonos_caja", "float", "Fracción de los abonos que entra a la Caja."),
        ("crecimiento_abonos", "float", "Abonos de la 2.ª mitad / 1.ª mitad de la ventana - 1."),
    ],
    "verdad_oportunidades": [
        ("cliente_id", "str", "Cliente."),
        ("tipo_oportunidad", "str", "CONSOLIDACION_DEUDA, CAPITAL_TRABAJO_MYPE, CAPTACION_AHORRO, "
                                    "DOMICILIACION_INGRESOS o RESTRICCION_SOBREENDEUDAMIENTO."),
        ("existe", "int", "1 si la regla de verdad se cumple con información completa; 0 si no."),
    ],
}

ARCHIVOS = {
    "entidades": "entidades.csv",
    "catalogo_productos": "catalogo_productos.csv",
    "clientes": "clientes.csv",
    "productos_cliente": "productos_cliente.csv",
    "transacciones": "transacciones.csv",
    "consentimientos": "consentimientos.csv",
    "consentimiento_alcances": "consentimiento_alcances.csv",
    "consentimiento_eventos": "consentimiento_eventos.csv",
    "alcances_campos": "alcances_campos.csv",
    "verdad_cliente": "verdad/verdad_cliente.csv",
    "verdad_oportunidades": "verdad/verdad_oportunidades.csv",
}

# ---------------------------------------------------------------------------
# Entidades y catálogo (todo ficticio; condiciones = SUPUESTO)
# ---------------------------------------------------------------------------
ENTIDADES = [
    ("E00", "Caja Receptora (rol Caja Trujillo)", "CAJA_MUNICIPAL", "RECEPTORA"),
    ("E01", "Banco Andino Demo", "BANCO", "FUENTE"),
    ("E02", "Financiera Sol Andina Demo", "FINANCIERA", "FUENTE"),
    ("E03", "Caja Municipal Pacifico Demo", "CAJA_MUNICIPAL", "FUENTE"),
    ("E04", "Cooperativa Cumbre Demo", "COOPERATIVA", "FUENTE"),
    ("E05", "Fintech Kuntur Demo", "FINTECH", "FUENTE"),
]
EXTERNAS = ["E01", "E02", "E03", "E04", "E05"]

# producto_id, entidad, categoria, nombre, tea_min, tea_max, plazo_min, plazo_max, monto_min, monto_max
CATALOGO = [
    ("P00-01", "E00", "CREDITO_MYPE", "Crédito MYPE Capital de Trabajo", 34, 42, 6, 36, 1000, 50000),
    ("P00-02", "E00", "CREDITO_CONSOLIDACION", "Crédito de Consolidación de Deudas", 30, 34, 12, 48, 3000, 40000),
    ("P00-03", "E00", "CREDITO_CONSUMO", "Crédito Consumo Personal", 42, 52, 6, 48, 500, 20000),
    ("P00-04", "E00", "CUENTA_AHORRO", "Ahorro Caja", 1.0, 2.0, 0, 0, 10, 100000),
    ("P00-05", "E00", "DEPOSITO_PLAZO", "Depósito a Plazo Caja", 4.5, 6.0, 3, 24, 1000, 200000),
    ("P00-06", "E00", "SEGURO", "Microseguro de Protección", 0, 0, 12, 12, 8, 25),
    ("P01-01", "E01", "TARJETA_CREDITO", "Tarjeta Clásica Andino", 75, 95, 0, 0, 800, 15000),
    ("P01-02", "E01", "CREDITO_CONSUMO", "Préstamo Personal Andino", 35, 55, 12, 60, 1000, 40000),
    ("P01-03", "E01", "CUENTA_AHORRO", "Cuenta Ahorro Andino", 0.2, 1.0, 0, 0, 0, 100000),
    ("P01-04", "E01", "DEPOSITO_PLAZO", "Depósito Plazo Andino", 3.0, 4.5, 3, 24, 1000, 200000),
    ("P01-05", "E01", "SEGURO", "Seguro Desgravamen Andino", 0, 0, 12, 12, 8, 25),
    ("P02-01", "E02", "CREDITO_CONSUMO", "Efectivo Express Sol", 60, 95, 6, 36, 500, 15000),
    ("P02-02", "E02", "TARJETA_CREDITO", "Tarjeta Sol", 85, 110, 0, 0, 500, 8000),
    ("P02-03", "E02", "CREDITO_MYPE", "Crédito Negocio Sol", 48, 65, 6, 36, 1000, 30000),
    ("P03-01", "E03", "CREDITO_MYPE", "Crédito Pyme Pacífico", 36, 55, 6, 48, 1000, 60000),
    ("P03-02", "E03", "CREDITO_CONSUMO", "Consumo Pacífico", 45, 65, 6, 48, 500, 20000),
    ("P03-03", "E03", "CUENTA_AHORRO", "Ahorro Pacífico", 0.8, 2.5, 0, 0, 0, 100000),
    ("P03-04", "E03", "DEPOSITO_PLAZO", "Depósito Plazo Pacífico", 4.0, 5.5, 3, 24, 1000, 200000),
    ("P04-01", "E04", "CREDITO_CONSUMO", "Crédito Socio Cumbre", 28, 45, 6, 48, 500, 25000),
    ("P04-02", "E04", "CUENTA_AHORRO", "Ahorro Socio Cumbre", 1.0, 2.5, 0, 0, 0, 100000),
    ("P04-03", "E04", "DEPOSITO_PLAZO", "Depósito Plazo Cumbre", 3.5, 5.0, 3, 24, 1000, 200000),
    ("P05-01", "E05", "BILLETERA_DIGITAL", "Billetera Kuntur", 0, 0, 0, 0, 0, 5000),
    ("P05-02", "E05", "CREDITO_CONSUMO", "Microcrédito Digital Kuntur", 90, 150, 3, 12, 100, 3000),
]

# Probabilidad de que un cliente tenga relación con cada entidad externa (SUPUESTO)
P_ENTIDAD = {"E01": 0.38, "E02": 0.15, "E03": 0.22, "E04": 0.08, "E05": 0.18}
P_CUENTA = {"E00": 0.90, "E01": 0.85, "E02": 0.0, "E03": 0.60, "E04": 0.70, "E05": 0.95}
P_CREDITO = {"E00": 0.50, "E01": 0.35, "E02": 0.35, "E03": 0.30, "E04": 0.30, "E05": 0.20}
EXT_CON_CUENTA = ["E01", "E03", "E04", "E05"]
EXT_CON_AHORRO = ["E01", "E03", "E04"]
EXT_CREDITO_CARO = ["E01", "E02", "E03", "E05"]

P_SEGMENTO = [0.35, 0.20, 0.12, 0.20, 0.13]
INGRESO_PARAMS = {  # (mediana S/, sigma log) SUPUESTO de plausibilidad
    "MYPE_COMERCIO": (3200, 0.55),
    "MYPE_SERVICIOS": (3000, 0.55),
    "MYPE_AGRO": (2600, 0.60),
    "ASALARIADO": (1900, 0.40),
    "INDEPENDIENTE": (2200, 0.50),
}
ACTIVIDADES = {
    "MYPE_COMERCIO": ["Bodega", "Ferretería", "Venta de ropa", "Minimarket", "Librería", "Venta de calzado"],
    "MYPE_SERVICIOS": ["Taller mecánico", "Restaurante", "Transporte local", "Peluquería", "Lavandería"],
    "MYPE_AGRO": ["Productor de arroz", "Productor de espárrago", "Productor de palta", "Productor de maíz"],
    "ASALARIADO": ["Empleado dependiente", "Docente", "Técnico en planilla"],
    "INDEPENDIENTE": ["Técnico independiente", "Conductor", "Costurera", "Servicios de diseño"],
}
DISTRITOS = [  # (distrito, provincia, peso)
    ("Trujillo", "Trujillo", 0.22), ("La Esperanza", "Trujillo", 0.17), ("El Porvenir", "Trujillo", 0.13),
    ("Víctor Larco Herrera", "Trujillo", 0.08), ("Florencia de Mora", "Trujillo", 0.04),
    ("Huanchaco", "Trujillo", 0.05), ("Moche", "Trujillo", 0.04), ("Salaverry", "Trujillo", 0.02),
    ("Laredo", "Trujillo", 0.03), ("Chepén", "Chepén", 0.05), ("Guadalupe", "Pacasmayo", 0.03),
    ("Pacasmayo", "Pacasmayo", 0.03), ("Casa Grande", "Ascope", 0.03), ("Virú", "Virú", 0.04),
    ("Otuzco", "Otuzco", 0.04),
]
DISTRITOS_AGRO = [
    ("Virú", "Virú", 0.25), ("Chepén", "Chepén", 0.20), ("Laredo", "Trujillo", 0.15),
    ("Casa Grande", "Ascope", 0.12), ("Guadalupe", "Pacasmayo", 0.10), ("Moche", "Trujillo", 0.08),
    ("Otuzco", "Otuzco", 0.10),
]
EDADES = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
P_EDADES = [0.08, 0.27, 0.30, 0.20, 0.11, 0.04]

# Estacionalidad simple por mes calendario (1.0 si no figura). Agro plano en mayo-oct a propósito:
# la estacionalidad no debe confundirse con crecimiento en la ventana por defecto.
ESTACIONALIDAD = {
    "MYPE_COMERCIO": {5: 1.03, 6: 0.98, 7: 1.04, 8: 0.97, 9: 1.0, 10: 1.02, 11: 1.08, 12: 1.15},
    "MYPE_SERVICIOS": {},
    "MYPE_AGRO": {4: 0.95, 5: 1.0, 6: 0.95, 7: 0.9, 8: 0.95, 9: 1.0, 10: 1.05, 11: 1.1, 12: 1.05},
    "ASALARIADO": {},
    "INDEPENDIENTE": {},
}
RUBROS_COMPRA = ["ALIMENTOS", "TRANSPORTE", "SALUD", "EDUCACION", "HOGAR", "OTROS"]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def _ultimos_meses(meses: int) -> list[tuple[int, int]]:
    """Lista (año, mes) de los últimos `meses` meses que terminan en la fecha de corte."""
    anio, mes = FECHA_CORTE.year, FECHA_CORTE.month
    out = []
    for k in range(meses - 1, -1, -1):
        m = mes - k
        a = anio
        while m <= 0:
            m += 12
            a -= 1
        out.append((a, m))
    return out


def _factor_cuota(tea_pct: float, n: int) -> tuple[float, float]:
    """Factor de anualidad y tasa mensual: cuota = capital * factor."""
    r = (1 + tea_pct / 100.0) ** (1 / 12) - 1
    return r / (1 - (1 + r) ** (-n)), r


def calificacion_por_dias(dias: int) -> str:
    """Calificación aproximada por días de atraso (tramos SUPUESTOS, no normativa vigente)."""
    if dias <= 8:
        return "NORMAL"
    if dias <= 30:
        return "CPP"
    if dias <= 60:
        return "DEFICIENTE"
    if dias <= 120:
        return "DUDOSO"
    return "PERDIDA"


def _elegir(rng: np.random.Generator, opciones, p=None):
    i = int(rng.choice(len(opciones), p=p))
    return opciones[i]


def _a_fecha(d: date) -> pd.Timestamp:
    return pd.Timestamp(d)


# ---------------------------------------------------------------------------
# Tablas maestras
# ---------------------------------------------------------------------------
def generar_entidades() -> pd.DataFrame:
    df = pd.DataFrame(ENTIDADES, columns=["entidad_id", "nombre", "tipo", "rol_sandbox"])
    df["ficticia"] = True
    return df


def generar_catalogo() -> pd.DataFrame:
    cols = ["producto_id", "entidad_id", "categoria", "nombre", "tea_min_pct", "tea_max_pct",
            "plazo_min_meses", "plazo_max_meses", "monto_min_pen", "monto_max_pen"]
    df = pd.DataFrame(CATALOGO, columns=cols)
    df["es_oferta_caja"] = df["entidad_id"] == "E00"
    df["es_supuesto"] = True
    for c in ("tea_min_pct", "tea_max_pct", "monto_min_pen", "monto_max_pen"):
        df[c] = df[c].astype(float)
    return df


def generar_alcances_campos() -> pd.DataFrame:
    filas = [
        ("PRODUCTOS", "productos_cliente", "producto_id", "Qué producto del catálogo tiene"),
        ("PRODUCTOS", "productos_cliente", "categoria", "Tipo de producto"),
        ("PRODUCTOS", "productos_cliente", "estado", "Si está activo, en mora o cancelado"),
        ("PRODUCTOS", "productos_cliente", "fecha_apertura", "Antigüedad del producto"),
        ("PRODUCTOS", "productos_cliente", "fecha_cierre", "Cuándo se canceló"),
        ("SALDOS", "productos_cliente", "monto_original_pen", "Monto original o línea"),
        ("SALDOS", "productos_cliente", "saldo_actual_pen", "Saldo actual"),
        ("CONDICIONES", "productos_cliente", "tasa_ea_pct", "Tasa del contrato"),
        ("CONDICIONES", "productos_cliente", "plazo_meses", "Plazo pactado"),
        ("CONDICIONES", "productos_cliente", "cuota_mensual_pen", "Cuota o pago mínimo"),
        ("CONDICIONES", "productos_cliente", "dias_atraso", "Comportamiento de pago"),
        ("CONDICIONES", "productos_cliente", "calificacion", "Calificación del crédito"),
        ("TRANSACCIONES", "transacciones", "fecha", "Cuándo ocurrió el movimiento"),
        ("TRANSACCIONES", "transacciones", "sentido", "Si entra o sale dinero"),
        ("TRANSACCIONES", "transacciones", "tipo", "Naturaleza del movimiento"),
        ("TRANSACCIONES", "transacciones", "categoria", "Rubro del gasto"),
        ("TRANSACCIONES", "transacciones", "monto_pen", "Monto del movimiento"),
    ]
    return pd.DataFrame(filas, columns=["alcance", "tabla", "columna", "descripcion"])


# Columnas de identificación que acompañan a cualquier alcance (no son un alcance por sí mismas)
COLUMNAS_CLAVE = {
    "productos_cliente": ["producto_cliente_id", "cliente_id", "entidad_id"],
    "transacciones": ["tx_id", "cliente_id", "entidad_id", "producto_cliente_id"],
}


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
def generar_clientes(rng: np.random.Generator, n: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Devuelve (clientes públicos, latente interna con ingreso real y arquetipos)."""
    ids = [f"C{i:06d}" for i in range(1, n + 1)]
    seg = [SEGMENTOS[i] for i in rng.choice(len(SEGMENTOS), size=n, p=P_SEGMENTO)]
    es_mype = np.array([s in SEGMENTOS_MYPE for s in seg])

    pesos_u = np.array([d[2] for d in DISTRITOS]); pesos_u = pesos_u / pesos_u.sum()
    pesos_a = np.array([d[2] for d in DISTRITOS_AGRO]); pesos_a = pesos_a / pesos_a.sum()
    distrito, provincia, actividad, ingreso, etiqueta = [], [], [], [], []
    for s in seg:
        if s == "MYPE_AGRO":
            d = DISTRITOS_AGRO[int(rng.choice(len(DISTRITOS_AGRO), p=pesos_a))]
        else:
            d = DISTRITOS[int(rng.choice(len(DISTRITOS), p=pesos_u))]
        distrito.append(d[0]); provincia.append(d[1])
        a = _elegir(rng, ACTIVIDADES[s]); actividad.append(a)
        etiqueta.append(f"{a} · {d[0]}")
        med, sig = INGRESO_PARAMS[s]
        v = np.exp(np.log(med) + sig * rng.standard_normal())
        ingreso.append(float(np.clip(round(v, -1), 1130, 30000)))
    ingreso = np.array(ingreso)

    edad = [EDADES[i] for i in rng.choice(len(EDADES), size=n, p=P_EDADES)]
    antig = np.where(es_mype, np.minimum(25, rng.geometric(0.18, size=n)), -1)
    p_caja = np.where(np.array(seg) == "MYPE_AGRO", 0.65, 0.60)
    es_caja = rng.random(n) < p_caja

    f_sobre = rng.random(n) < 0.09
    f_consol = rng.random(n) < 0.14
    f_ahorro = rng.random(n) < 0.09
    f_dom = es_caja & (rng.random(n) < 0.15)
    f_crece = rng.random(n) < np.where(es_mype, 0.20, 0.05)
    sin_cuenta = (rng.random(n) < 0.12) & ~f_crece & ~f_dom & ~f_ahorro

    dias_alta = rng.integers(60, 3000, size=n)
    alta = [pd.Timestamp(FECHA_CORTE - timedelta(days=int(d))) if c else pd.NaT for d, c in zip(dias_alta, es_caja)]
    declarado = np.where(es_caja, np.round(ingreso * np.exp(0.25 * rng.standard_normal(n)), -1), np.nan)

    clientes = pd.DataFrame({
        "cliente_id": ids,
        "segmento": seg,
        "actividad": actividad,
        "provincia": provincia,
        "distrito": distrito,
        "edad_rango": edad,
        "antiguedad_actividad_anios": pd.array(np.where(antig < 0, -1, antig), dtype="Int64"),
        "es_cliente_caja": es_caja,
        "fecha_alta_caja": pd.to_datetime(alta),
        "ingreso_declarado_caja_pen": declarado,
        "etiqueta_demo": etiqueta,
    })
    clientes.loc[clientes["antiguedad_actividad_anios"] == -1, "antiguedad_actividad_anios"] = pd.NA
    latente = pd.DataFrame({
        "cliente_id": ids, "segmento": seg, "ingreso_real": ingreso, "es_caja": es_caja,
        "f_sobre": f_sobre, "f_consol": f_consol, "f_ahorro": f_ahorro, "f_dom": f_dom,
        "f_crece": f_crece, "sin_cuenta": sin_cuenta,
    })
    return clientes, latente


# ---------------------------------------------------------------------------
# Productos de cada cliente
# ---------------------------------------------------------------------------
def generar_productos(rng: np.random.Generator, latente: pd.DataFrame, catalogo: pd.DataFrame) -> pd.DataFrame:
    prods: dict[str, list[dict]] = {}
    for r in catalogo.to_dict("records"):
        prods.setdefault(r["entidad_id"], []).append(r)

    def de_categoria(ent: str, cats: tuple[str, ...]) -> list[dict]:
        return [p for p in prods[ent] if p["categoria"] in cats]

    filas: list[dict] = []
    contador = 0

    def nuevo_id() -> str:
        nonlocal contador
        contador += 1
        return f"PC{contador:07d}"

    def completar(ext: list[str], candidatos: list[str], minimo: int) -> None:
        while len([e for e in ext if e in candidatos]) < minimo:
            faltan = [e for e in candidatos if e not in ext]
            if not faltan:
                return
            ext.append(_elegir(rng, faltan))

    for c in latente.to_dict("records"):
        cid, seg, ingreso = c["cliente_id"], c["segmento"], c["ingreso_real"]
        es_mype = seg in SEGMENTOS_MYPE

        # 1) entidades con las que tiene relación
        ext = [e for e in EXTERNAS if rng.random() < P_ENTIDAD[e]]
        if c["f_consol"]:
            completar(ext, EXT_CREDITO_CARO, 2)
        if c["f_sobre"]:
            completar(ext, EXTERNAS, 2)
        if c["f_ahorro"]:
            completar(ext, EXT_CON_AHORRO, 1)
        if c["f_dom"]:
            completar(ext, EXT_CON_CUENTA, 1)
        if not ext and not c["es_caja"]:
            pesos = np.array([P_ENTIDAD[e] for e in EXTERNAS]); pesos = pesos / pesos.sum()
            ext.append(_elegir(rng, EXTERNAS, p=pesos))
        ents = (["E00"] if c["es_caja"] else []) + ext

        # 2) cuentas / billeteras
        cuentas: dict[str, dict] = {}
        for e in ents:
            if not c["sin_cuenta"] and rng.random() < P_CUENTA[e]:
                cuentas[e] = {}
        if c["f_dom"] and not [e for e in cuentas if e != "E00"]:
            cuentas[_elegir(rng, [e for e in ext if e in EXT_CON_CUENTA])] = {}
        if c["f_crece"] and not cuentas:
            cand = [e for e in ents if e in ("E00",) + tuple(EXT_CON_CUENTA)]
            if not cand:  # solo tenía una financiera (sin cuentas): se le agrega otra entidad
                nueva = _elegir(rng, EXT_CON_CUENTA)
                ext.append(nueva)
                ents.append(nueva)
                cand = [nueva]
            cuentas[_elegir(rng, cand)] = {}
        ahorro_forzado = None
        if c["f_ahorro"]:
            ahorro_forzado = _elegir(rng, [e for e in ext if e in EXT_CON_AHORRO])
            cuentas[ahorro_forzado] = {"saldo_forzado": float(round(rng.uniform(AHORRO_SALDO_MIN + 500, 60000), 2))}

        # 3) créditos (ranuras)
        ranuras: list[dict] = []
        forzadas: set[str] = set()
        if c["f_consol"]:
            cands = [e for e in ext if e in EXT_CREDITO_CARO]
            forzadas.update(cands[:2])
        if c["f_sobre"]:
            for e in ext[:2]:
                forzadas.add(e)
        for e in ents:
            tiene = e in forzadas or rng.random() < P_CREDITO[e]
            if not tiene:
                continue
            if e == "E00":
                cat_caja = "CREDITO_MYPE" if (es_mype and rng.random() < 0.7) else "CREDITO_CONSUMO"
                prod = de_categoria("E00", (cat_caja,))[0]
            else:
                opc = de_categoria(e, CATEGORIAS_CREDITO)
                pesos = np.array([2.0 if (p["categoria"] == "CREDITO_MYPE" and es_mype) else 1.0 for p in opc])
                prod = _elegir(rng, opc, p=pesos / pesos.sum())
            ranuras.append({"entidad": e, "producto": prod, "caro": c["f_consol"] and e in forzadas})
            if rng.random() < 0.12 and prod["categoria"] != "TARJETA_CREDITO" and e not in forzadas:
                ranuras.append({"entidad": e, "producto": prod, "caro": False})

        # 4) relación mínima con la Caja
        if c["es_caja"] and not any(e == "E00" for e in cuentas) and not any(r["entidad"] == "E00" for r in ranuras):
            if c["sin_cuenta"]:
                prod = de_categoria("E00", ("CREDITO_CONSUMO",))[0]
                ranuras.append({"entidad": "E00", "producto": prod, "caro": False})
            else:
                cuentas["E00"] = {}

        # 5) todo cliente tiene al menos un producto no cancelado
        if not cuentas and not ranuras:
            e = ents[0]
            opc = de_categoria(e, ("CREDITO_CONSUMO",) if e == "E00" else CATEGORIAS_CREDITO)
            ranuras.append({"entidad": e, "producto": _elegir(rng, opc), "caro": False})

        # --- construcción de filas ---
        # cuentas y billeteras
        for e, extra in cuentas.items():
            prod = [p for p in prods[e] if p["categoria"] in CATEGORIAS_TRANSACCIONALES][0]
            tea = float(round(rng.uniform(prod["tea_min_pct"], prod["tea_max_pct"]), 2))
            if "saldo_forzado" in extra:
                saldo = extra["saldo_forzado"]
            elif prod["categoria"] == "BILLETERA_DIGITAL":
                saldo = float(np.exp(np.log(80) + 1.0 * rng.standard_normal()))
            else:
                saldo = float(np.exp(np.log(600) + 1.1 * rng.standard_normal()))
            saldo = float(round(min(max(saldo, 5.0), prod["monto_max_pen"]), 2))
            apertura = FECHA_CORTE - timedelta(days=int(rng.integers(60, 2500)))
            filas.append(_fila(nuevo_id(), cid, e, prod, "ACTIVO", apertura, None, None, saldo, tea,
                               None, 0.0, 0, ""))

        # créditos
        if ranuras:
            if c["f_sobre"]:
                r_obj = rng.uniform(0.55, 0.90)
            elif c["f_consol"]:
                r_obj = rng.uniform(0.20, 0.42)
            else:
                r_obj = rng.uniform(0.08, 0.40)
            w = rng.dirichlet(np.ones(len(ranuras)) * 2.0)
            p_mora = 0.30 if c["f_sobre"] else 0.04
            for ran, wi in zip(ranuras, w):
                filas.append(_credito(rng, nuevo_id(), cid, ran, wi * r_obj * ingreso, p_mora))

        # crédito cancelado (historial)
        if ents and rng.random() < 0.15:
            e = _elegir(rng, ents)
            opc = [p for p in de_categoria(e, CATEGORIAS_CREDITO) if p["categoria"] != "TARJETA_CREDITO"]
            if opc:
                prod = _elegir(rng, opc)
                filas.append(_credito_cancelado(rng, nuevo_id(), cid, prod, ingreso))

        # depósitos a plazo
        for e in ents:
            if e in ("E00", "E01", "E03", "E04") and rng.random() < 0.06:
                prod = _elegir(rng, de_categoria(e, ("DEPOSITO_PLAZO",)))
                plazo = int(_elegir(rng, [3, 6, 12, 18, 24]))
                tea = float(round(rng.uniform(prod["tea_min_pct"], prod["tea_max_pct"]), 2))
                saldo = float(round(min(max(np.exp(np.log(5000) + 0.9 * rng.standard_normal()), 1000), prod["monto_max_pen"]), 2))
                apertura = FECHA_CORTE - timedelta(days=int(rng.integers(5, plazo * 30)))
                filas.append(_fila(nuevo_id(), cid, e, prod, "ACTIVO", apertura, None, saldo, saldo, tea,
                                   plazo, 0.0, 0, ""))

        # seguros (solo quien tiene crédito)
        if ranuras and rng.random() < 0.08:
            e = _elegir(rng, [x for x in ("E00", "E01") if x in ents] or ["E01"])
            prod = de_categoria(e, ("SEGURO",))[0]
            prima = float(round(rng.uniform(prod["monto_min_pen"], prod["monto_max_pen"]), 2))
            apertura = FECHA_CORTE - timedelta(days=int(rng.integers(30, 900)))
            filas.append(_fila(nuevo_id(), cid, e, prod, "ACTIVO", apertura, None, None, 0.0, 0.0, 12, prima, 0, ""))

    cols = [c[0] for c in COLUMNAS["productos_cliente"]]
    df = pd.DataFrame(filas, columns=cols)
    for col in ("fecha_apertura", "fecha_cierre"):
        df[col] = pd.to_datetime(df[col])
    df["plazo_meses"] = df["plazo_meses"].astype("Int64")
    df["dias_atraso"] = df["dias_atraso"].astype(int)
    return df


def _fila(pid, cid, ent, prod, estado, apertura, cierre, monto, saldo, tea, plazo, cuota, dias, calif) -> dict:
    return {
        "producto_cliente_id": pid, "cliente_id": cid, "entidad_id": ent, "producto_id": prod["producto_id"],
        "categoria": prod["categoria"], "estado": estado,
        "fecha_apertura": apertura, "fecha_cierre": cierre,
        "monto_original_pen": monto, "saldo_actual_pen": saldo, "tasa_ea_pct": tea,
        "plazo_meses": plazo, "cuota_mensual_pen": cuota, "dias_atraso": dias,
        "calificacion": calif if calif else None,
    }


def _credito(rng, pid, cid, ran, cuota_obj: float, p_mora: float) -> dict:
    prod, ent = ran["producto"], ran["entidad"]
    if ran["caro"]:
        lo = max(41.0, (prod["tea_min_pct"] + prod["tea_max_pct"]) / 2)
        tea = float(round(rng.uniform(lo, max(lo + 1, prod["tea_max_pct"])), 2))
    else:
        tea = float(round(rng.uniform(prod["tea_min_pct"], prod["tea_max_pct"]), 2))
    dias = 0
    if rng.random() < p_mora:
        dias = int(np.exp(rng.uniform(np.log(1), np.log(150))))
    estado = "MORA" if dias > 8 else "ACTIVO"
    calif = calificacion_por_dias(dias)

    if prod["categoria"] == "TARJETA_CREDITO":
        saldo_obj = cuota_obj / 0.06
        u = rng.uniform(0.35, 0.95)
        linea = float(np.clip(round(saldo_obj / u, -1), prod["monto_min_pen"], prod["monto_max_pen"]))
        saldo = float(round(min(saldo_obj, linea), 2))
        cuota = float(round(max(30.0, 0.06 * saldo), 2))
        apertura = FECHA_CORTE - timedelta(days=int(rng.integers(100, 1500)))
        return _fila(pid, cid, ent, prod, estado, apertura, None, linea, saldo, tea, None, cuota, dias, calif)

    pmin, pmax = prod["plazo_min_meses"], prod["plazo_max_meses"]
    if pmax - pmin >= 6:
        n = int(_elegir(rng, list(range(max(6, pmin), pmax + 1, 6))))
    else:
        n = int(rng.integers(pmin, pmax + 1))
    factor, r = _factor_cuota(tea, n)
    monto = float(np.clip(round(cuota_obj / factor, -1), prod["monto_min_pen"], prod["monto_max_pen"]))
    cuota = float(round(monto * factor, 2))
    k = int(rng.integers(0, n))  # cuotas pagadas
    saldo = monto * ((1 + r) ** n - (1 + r) ** k) / ((1 + r) ** n - 1)
    saldo = float(round(min(max(saldo, 0.0), monto), 2))
    apertura = FECHA_CORTE - timedelta(days=int(round(k * 30.4375 + rng.uniform(0, 29))))
    return _fila(pid, cid, ent, prod, estado, apertura, None, monto, saldo, tea, n, cuota, dias, calif)


def _credito_cancelado(rng, pid, cid, prod, ingreso: float) -> dict:
    tea = float(round(rng.uniform(prod["tea_min_pct"], prod["tea_max_pct"]), 2))
    pmin, pmax = prod["plazo_min_meses"], prod["plazo_max_meses"]
    n = int(rng.integers(max(pmin, 3), pmax + 1))
    factor, _ = _factor_cuota(tea, n)
    monto = float(np.clip(round(ingreso * rng.uniform(0.5, 3.0), -1), prod["monto_min_pen"], prod["monto_max_pen"]))
    cierre = FECHA_CORTE - timedelta(days=int(rng.integers(30, 400)))
    apertura = cierre - timedelta(days=int(n * 30 + rng.integers(0, 30)))
    return _fila(pid, cid, prod["entidad_id"], prod, "CANCELADO", apertura, cierre, monto, 0.0, tea, n, 0.0, 0, "NORMAL")


# ---------------------------------------------------------------------------
# Transacciones
# ---------------------------------------------------------------------------
def generar_transacciones(rng: np.random.Generator, latente: pd.DataFrame, productos: pd.DataFrame, meses: int) -> pd.DataFrame:
    lista_meses = _ultimos_meses(meses)
    por_cliente: dict[str, list[dict]] = {}
    for p in productos.to_dict("records"):
        por_cliente.setdefault(p["cliente_id"], []).append(p)

    bloques: dict[str, list] = {k: [] for k in
                                ("cliente_id", "entidad_id", "producto_cliente_id", "fecha", "sentido", "tipo", "categoria", "monto")}

    def emitir(cid, ent, pcid, fechas, sentido, tipos, cats, montos) -> None:
        k = len(montos)
        bloques["cliente_id"].append(np.full(k, cid, dtype=object))
        bloques["entidad_id"].append(np.full(k, ent, dtype=object))
        bloques["producto_cliente_id"].append(np.full(k, pcid, dtype=object))
        bloques["fecha"].append(fechas)
        bloques["sentido"].append(np.full(k, sentido, dtype=object))
        bloques["tipo"].append(np.array(tipos, dtype=object))
        bloques["categoria"].append(np.array(cats, dtype=object))
        bloques["monto"].append(np.round(np.maximum(montos, 1.0), 2))

    tipos_deb = ["COMPRA", "PAGO_SERVICIOS", "RETIRO", "TRANSFERENCIA_ENVIADA", "PAGO_PROVEEDOR"]
    for c in latente.to_dict("records"):
        cid, seg, ingreso = c["cliente_id"], c["segmento"], c["ingreso_real"]
        prods = por_cliente.get(cid, [])
        cuentas = [p for p in prods if p["categoria"] in CATEGORIAS_TRANSACCIONALES]
        creditos = [p for p in prods if p["categoria"] in CATEGORIAS_CREDITO and p["estado"] != "CANCELADO"]

        pos = np.arange(meses) / max(1, meses - 1)
        if c["f_crece"]:
            crec = 1 + rng.uniform(0.35, 0.80) * pos
        else:
            crec = 1 + float(np.clip(rng.normal(0, 0.04), -0.08, 0.08)) * pos
        estac = np.array([ESTACIONALIDAD[seg].get(m, 1.0) for (_, m) in lista_meses])
        ruido = rng.uniform(0.93, 1.07, size=meses)
        ing_mes = ingreso * estac * crec * ruido

        if cuentas:
            caja = [a for a in cuentas if a["entidad_id"] == "E00"]
            ext = [a for a in cuentas if a["entidad_id"] != "E00"]
            shares: dict[str, float] = {}
            if caja and ext:
                if c["f_dom"]:
                    s_caja = rng.uniform(0.0, 0.25)
                elif rng.random() < 0.8:
                    s_caja = rng.uniform(0.55, 0.95)
                else:
                    s_caja = rng.uniform(0.30, 0.60)
                shares[caja[0]["producto_cliente_id"]] = s_caja
                w = rng.dirichlet(np.ones(len(ext)) * 2.0) * (1 - s_caja)
                for a, wi in zip(ext, w):
                    shares[a["producto_cliente_id"]] = wi
            elif caja:
                shares[caja[0]["producto_cliente_id"]] = 1.0
            else:
                w = rng.dirichlet(np.ones(len(ext)) * 2.0)
                for a, wi in zip(ext, w):
                    shares[a["producto_cliente_id"]] = wi

            for a in cuentas:
                s = shares.get(a["producto_cliente_id"], 0.0)
                if s <= 0:
                    continue
                for mi, (anio, mes) in enumerate(lista_meses):
                    total = ing_mes[mi] * s
                    if total < 1:
                        continue
                    base = np.datetime64(f"{anio:04d}-{mes:02d}-01", "D")
                    # abonos
                    if seg == "ASALARIADO":
                        k = 1 + int(rng.poisson(0.5))
                    elif seg == "INDEPENDIENTE":
                        k = 1 + int(rng.poisson(2.5))
                    else:
                        k = 1 + int(rng.poisson(5))
                    w = rng.gamma(2.0, size=k)
                    montos = total * w / w.sum()
                    dias = rng.integers(1, 29, size=k)
                    if seg == "ASALARIADO":
                        tipos = ["ABONO_SUELDO"] + ["ABONO_TRANSFERENCIA"] * (k - 1)
                        dias[0] = 28
                    elif seg == "INDEPENDIENTE":
                        tipos = ["ABONO_TRANSFERENCIA"] * k
                    else:
                        tipos = [("ABONO_VENTAS" if rng.random() < 0.8 else "ABONO_TRANSFERENCIA") for _ in range(k)]
                    fechas = base + (dias - 1).astype("timedelta64[D]")
                    emitir(cid, a["entidad_id"], a["producto_cliente_id"], fechas, "CREDITO", tipos,
                           ["SIN_CATEGORIA"] * k, montos)
                    # débitos
                    kd = 1 + int(rng.poisson(6))
                    wd = rng.gamma(2.0, size=kd)
                    montos_d = total * rng.uniform(0.65, 1.0) * wd / wd.sum()
                    pesos_t = np.array([0.35, 0.10, 0.25, 0.15, 0.15 if seg in SEGMENTOS_MYPE else 0.0])
                    pesos_t = pesos_t / pesos_t.sum()
                    tipos_d = [tipos_deb[i] for i in rng.choice(len(tipos_deb), size=kd, p=pesos_t)]
                    cats = []
                    for t in tipos_d:
                        if t == "COMPRA":
                            cats.append(_elegir(rng, RUBROS_COMPRA))
                        elif t == "PAGO_SERVICIOS":
                            cats.append("SERVICIOS_BASICOS")
                        elif t == "PAGO_PROVEEDOR":
                            cats.append("INSUMOS_NEGOCIO")
                        else:
                            cats.append("SIN_CATEGORIA")
                    dias_d = rng.integers(1, 29, size=kd)
                    emitir(cid, a["entidad_id"], a["producto_cliente_id"], base + (dias_d - 1).astype("timedelta64[D]"),
                           "DEBITO", tipos_d, cats, montos_d)

        # pagos de cuotas de crédito (se omiten los últimos meses si hay atraso)
        for cr in creditos:
            omitir = int(np.ceil(cr["dias_atraso"] / 30.0)) if cr["dias_atraso"] > 8 else 0
            dia_venc = min(28, cr["fecha_apertura"].day)
            for mi, (anio, mes) in enumerate(lista_meses):
                if mi >= meses - omitir:
                    continue
                venc = date(anio, mes, dia_venc)
                if venc <= cr["fecha_apertura"].date():
                    continue
                emitir(cid, cr["entidad_id"], cr["producto_cliente_id"],
                       np.array([np.datetime64(venc, "D")]), "DEBITO", ["PAGO_CUOTA"], ["SIN_CATEGORIA"],
                       np.array([cr["cuota_mensual_pen"]]))

    cols = [c[0] for c in COLUMNAS["transacciones"]]
    if not bloques["fecha"]:
        return pd.DataFrame(columns=cols)
    df = pd.DataFrame({
        "cliente_id": np.concatenate(bloques["cliente_id"]),
        "entidad_id": np.concatenate(bloques["entidad_id"]),
        "producto_cliente_id": np.concatenate(bloques["producto_cliente_id"]),
        "fecha": pd.to_datetime(np.concatenate(bloques["fecha"])),
        "sentido": np.concatenate(bloques["sentido"]),
        "tipo": np.concatenate(bloques["tipo"]),
        "categoria": np.concatenate(bloques["categoria"]),
        "monto_pen": np.concatenate(bloques["monto"]),
    })
    df = df.sort_values(["cliente_id", "fecha"], kind="stable").reset_index(drop=True)
    df.insert(0, "tx_id", [f"T{i:08d}" for i in range(1, len(df) + 1)])
    return df[cols]


# ---------------------------------------------------------------------------
# Consentimientos
# ---------------------------------------------------------------------------
def estado_consentimiento(fecha_revocado, fecha_vencimiento, corte: date = FECHA_CORTE) -> str:
    """REVOCADO si hay fecha de revocación; VENCIDO si el vencimiento es anterior al corte; si no, VIGENTE."""
    if fecha_revocado is not None and not pd.isna(fecha_revocado):
        return "REVOCADO"
    if pd.Timestamp(fecha_vencimiento).date() < corte:
        return "VENCIDO"
    return "VIGENTE"


def generar_consentimientos(rng: np.random.Generator, latente: pd.DataFrame, productos: pd.DataFrame,
                            tasa: float = TASA_CONSENTIMIENTO_POR_DEFECTO) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ents_por_cliente = productos.groupby("cliente_id")["entidad_id"].unique().to_dict()
    filas: list[dict] = []
    alcances: list[dict] = []
    contador = 0

    def nuevo_id() -> str:
        nonlocal contador
        contador += 1
        return f"K{contador:06d}"

    def crear(cid, receptor, fuente, apertura_cliente, fecha_ini=None, finalidad=None, renueva=None,
              permitir_revocar=True, alcance_base=None) -> dict:
        kid = nuevo_id()
        fin = finalidad or ("OFERTA_PRODUCTOS" if rng.random() < 0.80 else "VISTA_FINANCIERA")
        if alcance_base is None:
            alc = ["PRODUCTOS"]
            for nombre, p in (("SALDOS", 0.92), ("CONDICIONES", 0.88), ("TRANSACCIONES", 0.65)):
                p2 = float(np.clip(p + (apertura_cliente - 0.5) * 0.4, 0.05, 0.98))
                if rng.random() < p2:
                    alc.append(nombre)
        else:
            alc = list(alcance_base)
        otorgado = fecha_ini or (FECHA_CORTE - timedelta(days=int(rng.integers(1, 271))))
        plazo = int(_elegir(rng, [90, 180, 365], p=[0.15, 0.30, 0.55]))
        venc = otorgado + timedelta(days=plazo)
        revocado = None
        if permitir_revocar and rng.random() < 0.08:
            tope = max(1, min(plazo, (FECHA_CORTE - otorgado).days))
            revocado = otorgado + timedelta(days=int(rng.integers(1, tope + 1)))
        hist = int(_elegir(rng, [3, 6, 12], p=[0.2, 0.4, 0.4]))
        canal = _elegir(rng, ["APP", "AGENCIA", "WEB"], p=[0.5, 0.3, 0.2])
        fila = {
            "consentimiento_id": kid, "cliente_id": cid, "entidad_receptora_id": receptor,
            "entidad_fuente_id": fuente, "finalidad": fin, "fecha_otorgado": otorgado, "plazo_dias": plazo,
            "fecha_vencimiento": venc, "fecha_revocado": revocado, "historia_meses": hist, "canal": canal,
            "version_texto": "v1.0" if otorgado < date(2026, 7, 1) else "v1.1", "renueva_a": renueva,
        }
        filas.append(fila)
        for a in alc:
            alcances.append({"consentimiento_id": kid, "alcance": a})
        return {"fila": fila, "alcances": alc}

    for c in latente.to_dict("records"):
        cid = c["cliente_id"]
        ents = [str(e) for e in ents_por_cliente.get(cid, [])]
        externas = [e for e in ents if e != "E00"]
        apertura = float(rng.random())
        p_consiente = tasa * (0.65 if c["f_sobre"] else 1.0)  # selección adversa: los más endeudados comparten menos
        if externas and rng.random() < p_consiente:
            elegidas = [e for e in externas if rng.random() < 0.88] or [externas[0]]
            for e in elegidas:
                info = crear(cid, "E00", e, apertura)
                fila = info["fila"]
                vencido_sin_revocar = fila["fecha_revocado"] is None and fila["fecha_vencimiento"] < FECHA_CORTE
                if vencido_sin_revocar and rng.random() < 0.45:
                    ini = fila["fecha_vencimiento"] + timedelta(days=int(rng.integers(0, 16)))
                    if ini <= FECHA_CORTE:
                        crear(cid, "E00", e, apertura, fecha_ini=ini, finalidad=fila["finalidad"],
                              renueva=fila["consentimiento_id"], alcance_base=info["alcances"])
        # consentimientos de terceros (otro receptor): el sistema no debe confundirlos con los de la Caja
        if ents and rng.random() < 0.12:
            fuente = _elegir(rng, ents)
            receptor = _elegir(rng, [e for e in EXTERNAS if e != fuente])
            crear(cid, receptor, fuente, apertura, finalidad="OFERTA_PRODUCTOS")

    cols = [c[0] for c in COLUMNAS["consentimientos"] if c[0] != "estado"]
    df = pd.DataFrame(filas, columns=cols)
    for col in ("fecha_otorgado", "fecha_vencimiento", "fecha_revocado"):
        df[col] = pd.to_datetime(df[col])
    df["estado"] = [estado_consentimiento(r, v) for r, v in zip(df["fecha_revocado"], df["fecha_vencimiento"])]
    df = df[[c[0] for c in COLUMNAS["consentimientos"]]]

    eventos = []
    for r in df.to_dict("records"):
        eventos.append((r["consentimiento_id"], "OTORGADO", r["fecha_otorgado"]))
        if not pd.isna(r["fecha_revocado"]):
            eventos.append((r["consentimiento_id"], "REVOCADO", r["fecha_revocado"]))
        elif r["fecha_vencimiento"].date() < FECHA_CORTE:
            eventos.append((r["consentimiento_id"], "VENCIDO", r["fecha_vencimiento"]))
    ev = pd.DataFrame(eventos, columns=["consentimiento_id", "tipo", "fecha"])
    ev["fecha"] = pd.to_datetime(ev["fecha"])
    ev = ev.sort_values(["fecha", "consentimiento_id"], kind="stable").reset_index(drop=True)
    ev.insert(0, "evento_id", [f"EV{i:06d}" for i in range(1, len(ev) + 1)])
    al = pd.DataFrame(alcances, columns=["consentimiento_id", "alcance"])
    return df, al, ev


# ---------------------------------------------------------------------------
# Verdad de terreno (solo para medir; el agente jamás la ve)
# ---------------------------------------------------------------------------
def calcular_verdad(latente: pd.DataFrame, productos: pd.DataFrame, tx: pd.DataFrame, meses: int
                    ) -> tuple[pd.DataFrame, pd.DataFrame]:
    idx = latente["cliente_id"]
    activos = productos[productos["estado"] != "CANCELADO"]
    cred = activos[activos["categoria"].isin(CATEGORIAS_CREDITO)]

    g = cred.groupby("cliente_id")
    deuda = g["saldo_actual_pen"].sum()
    cuota = g["cuota_mensual_pen"].sum()
    riesgo = cred.assign(r=cred["calificacion"].isin(CALIFICACIONES_RIESGO)).groupby("cliente_id")["r"].any()
    ext = cred[cred["entidad_id"] != "E00"].groupby("cliente_id")
    n_ext = ext["producto_cliente_id"].count()
    saldo_ext = ext["saldo_actual_pen"].sum()
    tea_ext = ext["tasa_ea_pct"].max()
    ahorro = activos[(activos["categoria"] == "CUENTA_AHORRO") & (activos["entidad_id"] != "E00")
                     & (activos["tasa_ea_pct"] <= AHORRO_TEA_MAX)].groupby("cliente_id")["saldo_actual_pen"].sum()
    n_ent = activos.groupby("cliente_id")["entidad_id"].nunique()

    ab = tx[tx["tipo"].str.startswith("ABONO")].copy()
    primero = _ultimos_meses(meses)[0]
    ab["mes_idx"] = ab["fecha"].dt.year * 12 + ab["fecha"].dt.month - (primero[0] * 12 + primero[1])
    h = max(1, meses // 2)
    tot = ab.groupby("cliente_id")["monto_pen"].sum()
    caja = ab[ab["entidad_id"] == "E00"].groupby("cliente_id")["monto_pen"].sum()
    ini = ab[ab["mes_idx"] < h].groupby("cliente_id")["monto_pen"].sum()
    fin = ab[ab["mes_idx"] >= meses - h].groupby("cliente_id")["monto_pen"].sum()

    v = latente[["cliente_id"]].copy().set_index("cliente_id")
    v["ingreso_mensual_real_pen"] = latente.set_index("cliente_id")["ingreso_real"]
    for col, f in (("arquetipo_sobreendeudado", "f_sobre"), ("arquetipo_deuda_cara_dispersa", "f_consol"),
                   ("arquetipo_ahorrista_externo", "f_ahorro"), ("arquetipo_ingresos_en_otra_entidad", "f_dom"),
                   ("arquetipo_crecimiento", "f_crece")):
        v[col] = latente.set_index("cliente_id")[f].astype(bool)
    v["n_entidades"] = n_ent.reindex(idx).fillna(0).astype(int).values
    v["deuda_total_pen"] = deuda.reindex(idx).fillna(0.0).values
    v["cuota_total_pen"] = cuota.reindex(idx).fillna(0.0).values
    v["ratio_cuota_ingreso"] = v["cuota_total_pen"] / v["ingreso_mensual_real_pen"]
    v["n_creditos_externos"] = n_ext.reindex(idx).fillna(0).astype(int).values
    v["saldo_credito_externo_pen"] = saldo_ext.reindex(idx).fillna(0.0).values
    v["tea_max_externa_pct"] = tea_ext.reindex(idx).values
    v["ahorro_externo_baja_tasa_pen"] = ahorro.reindex(idx).fillna(0.0).values
    v["abonos_prom_mensual_pen"] = tot.reindex(idx).fillna(0.0).values / meses
    total_ab = tot.reindex(idx).values
    with np.errstate(divide="ignore", invalid="ignore"):
        v["share_abonos_caja"] = np.where(total_ab > 0, caja.reindex(idx).fillna(0.0).values / total_ab, np.nan)
        i_ = ini.reindex(idx).values
        f_ = fin.reindex(idx).values
        v["crecimiento_abonos"] = np.where(i_ > 0, f_ / i_ - 1.0, np.nan)

    es_caja = latente.set_index("cliente_id")["es_caja"]
    es_mype = latente.set_index("cliente_id")["segmento"].isin(SEGMENTOS_MYPE)
    riesgo_s = np.isin(idx.values, riesgo[riesgo].index.values)
    restr = (v["ratio_cuota_ingreso"].values > UMBRAL_RATIO_SOBREENDEUDAMIENTO) | riesgo_s
    flujo = v["abonos_prom_mensual_pen"].values >= ABONOS_PROMEDIO_MIN
    ratio = v["ratio_cuota_ingreso"].values

    existe = {
        "CONSOLIDACION_DEUDA": (~restr) & (v["n_creditos_externos"].values >= CONSOL_MIN_CREDITOS_EXTERNOS)
                               & (v["saldo_credito_externo_pen"].values >= CONSOL_MIN_SALDO_EXTERNO)
                               & (np.nan_to_num(v["tea_max_externa_pct"].values) >= CONSOL_TEA_MIN)
                               & (ratio >= CONSOL_RATIO_MIN),
        "CAPITAL_TRABAJO_MYPE": (~restr) & es_mype.values & flujo
                                & (np.nan_to_num(v["crecimiento_abonos"].values, nan=-1) >= CAPITAL_CRECIMIENTO_MIN)
                                & (ratio < CAPITAL_RATIO_MAX),
        "CAPTACION_AHORRO": v["ahorro_externo_baja_tasa_pen"].values >= AHORRO_SALDO_MIN,
        "DOMICILIACION_INGRESOS": es_caja.values & flujo
                                  & (np.nan_to_num(v["share_abonos_caja"].values, nan=1.0) < DOM_SHARE_MAX),
        "RESTRICCION_SOBREENDEUDAMIENTO": restr,
    }
    largo = pd.concat([
        pd.DataFrame({"cliente_id": idx.values, "tipo_oportunidad": t, "existe": np.asarray(e).astype(int)})
        for t, e in existe.items()
    ], ignore_index=True)
    vc = v.reset_index()
    for col in ("ingreso_mensual_real_pen", "deuda_total_pen", "cuota_total_pen"):
        vc[col] = vc[col].round(2)
    for col in ("ratio_cuota_ingreso", "share_abonos_caja", "crecimiento_abonos"):
        vc[col] = vc[col].round(4)
    vc["abonos_prom_mensual_pen"] = vc["abonos_prom_mensual_pen"].round(2)
    vc["saldo_credito_externo_pen"] = vc["saldo_credito_externo_pen"].round(2)
    vc["ahorro_externo_baja_tasa_pen"] = vc["ahorro_externo_baja_tasa_pen"].round(2)
    return vc[[c[0] for c in COLUMNAS["verdad_cliente"]]], largo[[c[0] for c in COLUMNAS["verdad_oportunidades"]]]


# ---------------------------------------------------------------------------
# Orquestación
# ---------------------------------------------------------------------------
def generar(n_clientes: int = N_CLIENTES_POR_DEFECTO, meses: int = MESES_POR_DEFECTO,
            semilla: int = SEMILLA_POR_DEFECTO, tasa_consentimiento: float = TASA_CONSENTIMIENTO_POR_DEFECTO) -> dict[str, pd.DataFrame]:
    """Genera todas las tablas en memoria. Mismos argumentos => mismas tablas."""
    if n_clientes < 10:
        raise ValueError("n_clientes debe ser >= 10")
    if not 0.0 <= tasa_consentimiento <= 1.0:
        raise ValueError("tasa_consentimiento debe estar entre 0 y 1")
    if not 2 <= meses <= 12:
        raise ValueError("meses debe estar entre 2 y 12")
    hijos = np.random.SeedSequence(semilla).spawn(4)
    r_cli, r_prod, r_tx, r_cons = (np.random.default_rng(h) for h in hijos)

    entidades = generar_entidades()
    catalogo = generar_catalogo()
    clientes, latente = generar_clientes(r_cli, n_clientes)
    productos = generar_productos(r_prod, latente, catalogo)
    tx = generar_transacciones(r_tx, latente, productos, meses)
    cons, alc, ev = generar_consentimientos(r_cons, latente, productos, tasa_consentimiento)
    v_cli, v_op = calcular_verdad(latente, productos, tx, meses)
    return {
        "entidades": entidades, "catalogo_productos": catalogo, "clientes": clientes,
        "productos_cliente": productos, "transacciones": tx, "consentimientos": cons,
        "consentimiento_alcances": alc, "consentimiento_eventos": ev,
        "alcances_campos": generar_alcances_campos(),
        "verdad_cliente": v_cli, "verdad_oportunidades": v_op,
    }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def diccionario_markdown() -> str:
    lineas = [
        "# Diccionario de datos — NEG-02 (sintético)", "",
        "Generado por `retos/NEG-02/datos/generar.py`. **Todo es ficticio**: ni personas, ni entidades, ni tarifas reales.",
        "Las condiciones comerciales son SUPUESTOS del equipo. La carpeta `verdad/` es solo para medir el KPI: "
        "el agente y la API del sandbox nunca deben leerla.", "",
    ]
    for tabla, cols in COLUMNAS.items():
        lineas += [f"## {ARCHIVOS[tabla]}", "", "| Columna | Tipo | Descripción |", "|---|---|---|"]
        lineas += [f"| `{c}` | {t} | {d} |" for c, t, d in cols]
        lineas.append("")
    return "\n".join(lineas) + "\n"


def escribir(tablas: dict[str, pd.DataFrame], salida: Path, semilla: int, meses: int,
             tasa_consentimiento: float = TASA_CONSENTIMIENTO_POR_DEFECTO) -> dict:
    """Escribe los CSV, el diccionario y el manifest (con hashes). Devuelve el manifest."""
    salida = Path(salida)
    (salida / "verdad").mkdir(parents=True, exist_ok=True)
    archivos = {}
    for nombre, df in tablas.items():
        ruta = salida / ARCHIVOS[nombre]
        df.to_csv(ruta, index=False, encoding="utf-8", lineterminator="\n", date_format="%Y-%m-%d")
        archivos[ARCHIVOS[nombre]] = {"filas": int(len(df)), "sha256": _sha256(ruta)}
    (salida / "diccionario_datos.md").write_text(diccionario_markdown(), encoding="utf-8", newline="\n")
    manifest = {
        "version_generador": VERSION_GENERADOR,
        "semilla": semilla,
        "n_clientes": int(len(tablas["clientes"])),
        "meses_transacciones": meses,
        "tasa_consentimiento": tasa_consentimiento,
        "fecha_corte": FECHA_CORTE.isoformat(),
        "aviso": "Datos 100% sintéticos. Sin personas, entidades ni APIs reales. verdad/ es solo para medición.",
        "archivos": archivos,
    }
    (salida / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8", newline="\n")
    return manifest


def resumen(tablas: dict[str, pd.DataFrame]) -> str:
    cli, prod, cons = tablas["clientes"], tablas["productos_cliente"], tablas["consentimientos"]
    vo = tablas["verdad_oportunidades"]
    n = len(cli)
    ents = prod[prod["estado"] != "CANCELADO"].groupby("cliente_id")["entidad_id"].nunique()
    lineas = [f"clientes={n}  productos={len(prod)}  transacciones={len(tablas['transacciones'])}  "
              f"consentimientos={len(cons)}",
              f"clientes con productos en >=2 entidades: {(ents >= 2).mean():.0%}  (media {ents.mean():.2f})",
              "estado de consentimientos: " + ", ".join(f"{k}={v}" for k, v in cons["estado"].value_counts().items()),
              "prevalencia de oportunidades (verdad): " + ", ".join(
                  f"{t}={g['existe'].mean():.1%}" for t, g in vo.groupby("tipo_oportunidad"))]
    return "\n".join(lineas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Genera datos sintéticos de NEG-02 (Open Finance).")
    ap.add_argument("--semilla", type=int, default=SEMILLA_POR_DEFECTO)
    ap.add_argument("--n-clientes", type=int, default=N_CLIENTES_POR_DEFECTO)
    ap.add_argument("--meses", type=int, default=MESES_POR_DEFECTO)
    ap.add_argument("--tasa-consentimiento", type=float, default=TASA_CONSENTIMIENTO_POR_DEFECTO,
                    help="Probabilidad (0-1) de que un cliente comparta datos con la Caja. SUPUESTO.")
    ap.add_argument("--salida", type=Path, default=SALIDA_POR_DEFECTO)
    a = ap.parse_args(argv)
    tablas = generar(a.n_clientes, a.meses, a.semilla, a.tasa_consentimiento)
    escribir(tablas, a.salida, a.semilla, a.meses, a.tasa_consentimiento)
    print(resumen(tablas))
    print(f"Escrito en {a.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
