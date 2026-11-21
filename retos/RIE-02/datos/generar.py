"""Generador de datos sintéticos para RIE-02 «Descubrir redes de riesgo ocultas».

Produce un lote de solicitudes de crédito MYPE de una caja municipal ficticia (La Libertad)
con su grafo implícito (personas, negocios, teléfonos, dispositivos, direcciones, referencias),
más redes de fraude inyectadas y relaciones legítimas «señuelo» para medir falsos positivos.

Reglas:
- 100 % sintético y reproducible: misma semilla y misma escala => archivos idénticos byte a byte.
- Sin red, sin datos reales. Documentos y teléfonos llevan el prefijo «FIC-» (claramente ficticios).
  Los nombres son combinaciones aleatorias de listas genéricas; cualquier parecido es casual.
- Las tablas de entrada NO contienen etiquetas. La verdad de terreno va aparte
  (redes_verdad.csv y etiquetas_solicitudes.csv). Los ids se barajan al final para que el orden
  de creación no delate las redes.
- Es una herramienta de datos: NO contiene el detector, la priorización ni el agente.

Uso:
    python retos/RIE-02/datos/generar.py [--semilla 2026] [--escala 1.0] [--salida RUTA]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

VERSION_ESQUEMA = "1.0"
SEMILLA_POR_DEFECTO = 2026
FECHA_INICIO = date(2025, 10, 1)
DIAS_LOTE = 365
# Umbral interno de revisión reforzada: SUPUESTO nuestro, no dato de la Caja [POR CONFIRMAR].
UMBRAL_REVISION_PEN = 10_000
PATRONES_FRAUDE = (
    "anillo",
    "estrella",
    "dispositivo_compartido",
    "direccion_fantasma",
    "evasiva_debil",
)
PATRONES_SENUELO = (
    "familia",
    "mercado",
    "tableta_agencia",
    "asociacion_gremial",
    "gestor_contador",
    "coincidencia_casual",
)
DIFICULTADES = ("baja", "media", "alta")

# Agencias y distritos ficticios/genéricos de La Libertad: (id, nombre, distrito, provincia, peso).
AGENCIAS = [
    ("AG01", "Agencia Trujillo Centro", "Trujillo", "Trujillo", 0.28),
    ("AG02", "Agencia La Esperanza", "La Esperanza", "Trujillo", 0.16),
    ("AG03", "Agencia El Porvenir", "El Porvenir", "Trujillo", 0.14),
    ("AG04", "Agencia Víctor Larco", "Víctor Larco Herrera", "Trujillo", 0.10),
    ("AG05", "Agencia Florencia de Mora", "Florencia de Mora", "Trujillo", 0.06),
    ("AG06", "Agencia Laredo", "Laredo", "Trujillo", 0.05),
    ("AG07", "Agencia Chepén", "Chepén", "Chepén", 0.07),
    ("AG08", "Agencia Pacasmayo", "Pacasmayo", "Pacasmayo", 0.04),
    ("AG09", "Agencia Virú", "Virú", "Virú", 0.05),
    ("AG10", "Agencia Huamachuco", "Huamachuco", "Sánchez Carrión", 0.05),
]
# Mercados ficticios (nombre, índice de agencia/distrito donde están).
MERCADOS = [
    ("Mercado Las Palmeras", 0),
    ("Mercado San Camilo Norte", 0),
    ("Mercado Esperanza Unida", 1),
    ("Mercado El Progreso", 2),
    ("Mercado Costa Verde", 3),
    ("Mercado Chepén Sur", 6),
]
# rubro: (nombre comercial, admite puesto en mercado)
RUBROS = {
    "bodega": ("Bodega", True),
    "ropa": ("Boutique", True),
    "calzado": ("Calzados", True),
    "restaurante": ("Restaurante", True),
    "frutas_verduras": ("Frutería", True),
    "avicola": ("Avícola", True),
    "ferreteria": ("Ferretería", False),
    "taller_mecanico": ("Taller", False),
    "transporte": ("Transportes", False),
    "panaderia": ("Panadería", False),
    "peluqueria": ("Salón", False),
    "agricola": ("Agro", False),
}
RUBROS_MERCADO = [r for r, (_, m) in RUBROS.items() if m]
FANTASIA = [
    "El Sol", "Los Andes", "La Esperanza", "San José", "Santa Rosa", "El Progreso",
    "Los Pinos", "Mi Pueblo", "La Unión", "Nuevo Amanecer", "El Norteño", "La Perla",
]
NOMBRES = [
    "Luis", "Carlos", "José", "Juan", "Pedro", "Miguel", "Jorge", "Víctor", "Walter", "Raúl",
    "María", "Rosa", "Carmen", "Ana", "Luz", "Elena", "Julia", "Sofía", "Teresa", "Marleni",
    "Segundo", "Eloy", "Wilder", "Nelly", "Betty", "Gladys", "Fidel", "Edwin", "Yolanda", "Lidia",
]
APELLIDOS = [
    "Alva", "Vásquez", "Rodríguez", "Quispe", "Chávez", "Torres", "Gonzales", "Sánchez", "Cruz",
    "Mendoza", "Díaz", "Flores", "Rojas", "Ramos", "Castillo", "Vega", "Ríos", "Paredes",
    "Zavaleta", "Gil", "Lozano", "Cabrera", "Salazar", "Leiva", "Benites", "Reyes", "Aguilar",
    "Pinedo", "Valverde", "Huamán",
]
VIAS = ["Jr.", "Av.", "Calle", "Psje."]
CALLES = [
    "Los Sauces", "Las Dalias", "Santa Rosa", "Los Olivos", "La Merced", "San Martín",
    "Los Cedros", "Las Flores", "Grau", "Libertad", "Independencia", "Los Laureles",
    "El Inca", "Las Palmeras", "Túpac Amaru", "Los Jazmines",
]
CANALES = ("agencia", "promotor_tableta", "app_movil")
PRODUCTOS = ("capital_trabajo", "activo_fijo", "mejora_local")
RELACIONES_NORMALES = ("familiar", "vecino", "proveedor", "cliente", "amigo")

TABLAS = ("personas", "negocios", "direcciones", "telefonos", "dispositivos", "solicitudes",
          "referencias", "agencias")
ARCHIVOS_VERDAD = ("redes_verdad", "etiquetas_solicitudes")


class Mundo:
    """Acumula entidades y relaciones. Todos los ids son temporales hasta `finalizar`."""

    def __init__(self, semilla: int, escala: float) -> None:
        self.semilla = semilla
        self.escala = escala
        self.rng = np.random.default_rng(semilla)
        self.t: dict[str, list[dict]] = {
            k: [] for k in ("personas", "negocios", "direcciones", "telefonos", "dispositivos",
                            "solicitudes", "referencias", "etiquetas")
        }
        self.redes: dict[str, dict] = {}
        self._c: dict[str, int] = {}
        self._textos: set[str] = set()
        self._tablets: dict[int, str] = {}
        self._mercados: dict[int, str] = {}
        self._prov: list[tuple[str, str] | None] = []
        self._prov_uso: list[int] = []
        self._red_tab: dict[int, str] = {}
        self._jornadas_ag: dict[int, list[int]] = {}
        self.puente_ref = False
        self._n_prov = 0

    # ---------- utilidades ----------
    def n(self, base: float) -> int:
        return max(1, int(round(base * self.escala)))

    def entero(self, a: int, b: int) -> int:
        return int(self.rng.integers(a, b + 1))

    def elegir(self, opciones):
        return opciones[int(self.rng.integers(0, len(opciones)))]

    def _id(self, prefijo: str) -> str:
        self._c[prefijo] = self._c.get(prefijo, 0) + 1
        return f"{prefijo}{self._c[prefijo]:06d}"

    def _numero(self, clave: str, digitos: int) -> str:
        """Número pseudoaleatorio, único (biyectivo) por contador. Solo para valores ficticios."""
        c = self._c[clave]
        m = 10**digitos
        base = m // 10
        return str((c * 7919 + 12345) % (m - base) + base)

    def dia(self, offset: int) -> date:
        d = FECHA_INICIO + timedelta(days=int(offset))
        return d + timedelta(days=1) if d.weekday() == 6 else d  # sin domingos

    def fecha_aleatoria(self, desde: int = 0, hasta: int = DIAS_LOTE - 1) -> date:
        return self.dia(self.entero(desde, hasta))

    def inicio_ventana(self, ventana: int) -> int:
        return self.entero(0, max(0, DIAS_LOTE - 1 - ventana))

    def distrito_idx(self) -> int:
        p = np.array([a[4] for a in AGENCIAS])
        return int(self.rng.choice(len(AGENCIAS), p=p / p.sum()))

    # ---------- entidades ----------
    def persona(self, perfil: str = "normal", apellidos: tuple[str, str] | None = None,
                distrito: str | None = None) -> str:
        r = self.rng
        p_nuevo = {"fraude": 0.70, "maduro": 0.20}.get(perfil, 0.45)
        nuevo = r.random() < p_nuevo
        if nuevo:
            meses, creditos = 0, 0
        else:
            meses = self.entero(18 if perfil == "maduro" else 6, 120)
            creditos = self.entero(2 if perfil == "maduro" else 1, 8 if perfil == "maduro" else 6)
        pid = self._id("P")
        ap = apellidos or (self.elegir(APELLIDOS), self.elegir(APELLIDOS))
        self.t["personas"].append({
            "persona_id": pid,
            "documento_ficticio": f"FIC-{self._numero('P', 8)}",
            "nombres": self.elegir(NOMBRES),
            "apellido_paterno": ap[0],
            "apellido_materno": ap[1],
            "edad_anios": self.entero(22, 62),
            "distrito_residencia": distrito or AGENCIAS[self.distrito_idx()][2],
            "meses_como_cliente": meses,
            "creditos_previos": creditos,
        })
        return pid

    def direccion(self, tipo: str, distrito: str, hogares: int = 1) -> str:
        for _ in range(50):
            texto = (f"{self.elegir(VIAS)} {self.elegir(CALLES)} {self.entero(100, 999)}, "
                     f"Mz. {chr(65 + self.entero(0, 17))} Lt. {self.entero(1, 30)}")
            if texto not in self._textos:
                break
        else:
            texto = f"{texto} #{self._c.get('D', 0) + 1}"
        self._textos.add(texto)
        did = self._id("D")
        prov = next(a[3] for a in AGENCIAS if a[2] == distrito)
        self.t["direcciones"].append({
            "direccion_id": did, "texto_direccion": texto, "distrito": distrito,
            "provincia": prov, "tipo_inmueble": tipo, "hogares_esperados": hogares,
            "mercado": "",
        })
        return did

    def mercado(self, idx: int) -> str:
        if idx not in self._mercados:
            nombre, ag = MERCADOS[idx]
            did = self._id("D")
            self._mercados[idx] = did
            self.t["direcciones"].append({
                "direccion_id": did, "texto_direccion": f"{nombre}, Av. Comercio s/n",
                "distrito": AGENCIAS[ag][2], "provincia": AGENCIAS[ag][3],
                "tipo_inmueble": "puesto_mercado", "hogares_esperados": 300, "mercado": nombre,
            })
        return self._mercados[idx]

    def telefono(self, joven: bool = False, tipo: str = "movil") -> str:
        tid = self._id("T")
        if tipo == "fijo":
            numero = f"FIC-044{self._numero('T', 6)}"
        else:
            numero = f"FIC-9{self._numero('T', 8)}"
        if joven:
            ant = self.entero(0, 6) if self.rng.random() < 0.60 else self.entero(7, 48)
        else:
            ant = int(np.clip(self.rng.lognormal(np.log(30), 0.8), 1, 240))
        self.t["telefonos"].append({
            "telefono_id": tid, "numero_ficticio": numero, "tipo_linea": (
                "fijo" if tipo == "fijo" else self.elegir(("movil_prepago", "movil_prepago",
                                                          "movil_postpago"))),
            "antiguedad_linea_meses": ant,
        })
        return tid

    def dispositivo(self, tipo: str = "smartphone", agencia: str = "") -> str:
        did = self._id("V")
        huella = hashlib.sha1(f"{self.semilla}-{did}".encode()).hexdigest()[:16]
        if tipo == "smartphone":
            tipo = self.elegir(("smartphone_android", "smartphone_android", "smartphone_ios"))
        self.t["dispositivos"].append({
            "dispositivo_id": did, "huella_ficticia": huella, "tipo_dispositivo": tipo,
            "agencia_id": agencia,
        })
        return did

    def tablet(self, ag_idx: int) -> str:
        if ag_idx not in self._tablets:
            self._tablets[ag_idx] = self.dispositivo("tableta_agencia", AGENCIAS[ag_idx][0])
        return self._tablets[ag_idx]

    def negocio(self, propietario: str, direccion: str, rubro: str, antiguedad: int,
                puesto: str = "") -> str:
        nid = self._id("N")
        self.t["negocios"].append({
            "negocio_id": nid,
            "nombre_negocio": f"{RUBROS[rubro][0]} {self.elegir(FANTASIA)}",
            "rubro": rubro, "propietario_id": propietario, "direccion_id": direccion,
            "puesto": puesto, "antiguedad_meses": antiguedad,
        })
        return nid

    def identidad(self, perfil: str = "normal", d_idx: int | None = None, rubro: str | None = None,
                  domicilio: str | None = None, local: str | None = None, tel: str | None = None,
                  disp: str | None = None, canal: str | None = None,
                  apellidos: tuple[str, str] | None = None, mercado_idx: int | None = None,
                  antig_min: int | None = None, persona: str | None = None) -> dict:
        """Persona + negocio + teléfono + dispositivo + domicilio, con valores nuevos por defecto."""
        d_idx = self.distrito_idx() if d_idx is None else d_idx
        distrito = AGENCIAS[d_idx][2]
        rubro = rubro or self.elegir(list(RUBROS))
        canal = canal or self.elegir(CANALES)
        if self.puente_ref and perfil == "fraude":
            # Puentes con lo legítimo: algunos miembros del fraude pasan por la tableta de la
            # agencia o tienen puesto en un mercado, y así se conectan con grupos legítimos.
            if disp is None and canal in ("agencia", "app_movil") and self.rng.random() < 0.12:
                canal = "promotor_tableta"
            if local is None and mercado_idx is None and RUBROS[rubro][1]:
                merc = [i for i, m in enumerate(MERCADOS) if m[1] == d_idx]
                if merc and self.rng.random() < 0.25:
                    mercado_idx = self.elegir(merc)
        persona = persona or self.persona(perfil, apellidos, distrito)
        domicilio = domicilio or self.direccion(
            "vivienda" if self.rng.random() < 0.85 else "vivienda_multifamiliar", distrito,
            1 if self.rng.random() < 0.85 else self.entero(4, 8))
        puesto = ""
        if local is None:
            if mercado_idx is not None:
                local = self.mercado(mercado_idx)
                puesto = f"Puesto {self.entero(1, 400)}"
            else:
                local = self.direccion("local_comercial", distrito)
        if perfil == "fraude":
            antig = self.entero(0, 5) if self.rng.random() < 0.65 else self.entero(6, 36)
        else:
            antig = self.entero(antig_min or 3, max(antig_min or 3, 120))
        negocio = self.negocio(persona, local, rubro, antig, puesto)
        tel = tel or self.telefono(joven=(perfil == "fraude"))
        if disp is None:
            if canal == "app_movil":
                disp = self.dispositivo("smartphone")
            elif canal == "promotor_tableta":
                disp = self.tablet(d_idx)
        return {"persona": persona, "negocio": negocio, "tel": tel, "disp": disp or "",
                "dom": domicilio, "d_idx": d_idx, "canal": canal, "perfil": perfil,
                "rubro": rubro}

    def solicitud(self, ident: dict, fecha: date, monto: float | None = None,
                  plazo: int | None = None, etiqueta: str = "normal", red: str = "",
                  rol: str = "", estructurar: bool = False) -> str:
        r = self.rng
        if monto is None:
            monto = float(np.clip(r.lognormal(np.log(7000), 0.7), 1000, 80000))
        if estructurar:
            monto = UMBRAL_REVISION_PEN * (0.90 + 0.095 * r.random())
        monto = float(round(monto / 100) * 100)
        ratio = float(np.clip(r.lognormal(np.log(3.5), 0.5), 1.0, 12.0))
        ingreso = max(800.0, monto / ratio)
        paso = 500 if (ident["perfil"] == "fraude" and r.random() < 0.6) else 50
        ingreso = float(round(ingreso / paso) * paso)
        sid = self._id("S")
        ag = AGENCIAS[ident["d_idx"]][0]
        analista = f"AN{ident['d_idx'] * 3 + self.entero(1, 3):02d}"
        self.t["solicitudes"].append({
            "solicitud_id": sid, "fecha_solicitud": fecha.isoformat(), "agencia_id": ag,
            "analista_id": analista, "canal": ident["canal"],
            "producto": str(self.rng.choice(PRODUCTOS, p=[0.70, 0.20, 0.10])),
            "monto_solicitado_pen": monto,
            "plazo_meses": plazo or int(self.elegir((6, 9, 12, 12, 18, 24, 36))),
            "ingreso_mensual_declarado_pen": ingreso, "solicitante_id": ident["persona"],
            "negocio_id": ident["negocio"], "telefono_id": ident["tel"],
            "dispositivo_id": ident["disp"], "direccion_domicilio_id": ident["dom"],
        })
        self.t["etiquetas"].append({
            "solicitud_id": sid, "etiqueta": etiqueta, "red_id": red, "rol": rol,
        })
        return sid

    def referencia(self, sid: str, persona: str, relacion: str, tel: str) -> None:
        self.t["referencias"].append({
            "referencia_id": self._id("R"), "solicitud_id": sid, "persona_referencia_id": persona,
            "relacion": relacion, "telefono_referencia_id": tel,
        })

    def referencia_nueva(self, sid: str, relacion: str | None = None, perfil: str = "normal",
                         joven: bool = False) -> None:
        # Puente: a veces la referencia es un proveedor común (hub legítimo del fondo). Así las
        # redes se pegan al resto del grafo, como en la realidad, y no quedan aisladas.
        if self.puente_ref and self._n_prov and self.rng.random() < 0.25:
            c = self.entero(0, self._n_prov - 1)
            if c >= len(self._prov_uso) or self._prov_uso[c] < 10:
                persona, tel = self._proveedor(c)
                self.referencia(sid, persona, "proveedor", tel)
                return
        self.referencia(sid, self.persona(perfil), relacion or self.elegir(RELACIONES_NORMALES),
                        self.telefono(joven=joven))

    def red(self, clase: str, patron: str, dificultad: str, vinculos: str) -> str:
        orden = sum(1 for v in self.redes.values() if v["patron"] == patron)
        prefijo = "RF" if clase == "fraude" else "RL"
        rid = f"{prefijo}{len(self.redes) + 1:03d}"
        self.redes[rid] = {
            "red_id": rid, "clase": clase, "patron": patron, "dificultad": dificultad,
            "vinculos_clave": vinculos, "_orden": orden,
        }
        return rid

    # ---------- fondo (solicitudes normales y comportamientos cotidianos) ----------
    def _proveedor(self, ranura: int) -> tuple[str, str]:
        while len(self._prov) <= ranura:
            self._prov.append(None)
            self._prov_uso.append(0)
        if self._prov[ranura] is None:
            self._prov[ranura] = (self.persona("maduro"), self.telefono())
        self._prov_uso[ranura] += 1
        return self._prov[ranura]

    def fondo(self) -> None:
        r = self.rng
        n_prov = self.n(30)
        self._n_prov = n_prov
        previos: list[tuple[dict, list[tuple[str, str, str]], date]] = []
        for _ in range(self.n(3000)):
            canal = str(r.choice(CANALES, p=[0.60, 0.12, 0.28]))
            d_idx = self.distrito_idx()
            rubro = self.elegir(list(RUBROS))
            merc = [i for i, m in enumerate(MERCADOS) if m[1] == d_idx]
            en_mercado = RUBROS[rubro][1] and merc and r.random() < 0.35
            ident = self.identidad("normal", d_idx, rubro, canal=canal,
                                   mercado_idx=self.elegir(merc) if en_mercado else None)
            fecha = self.fecha_aleatoria()
            if canal == "promotor_tableta" and r.random() < 0.5:  # jornada de campo del promotor
                fecha = self.dia(self._jornadas(d_idx)[int(r.integers(0, 6))] + self.entero(0, 1))
            sid = self._etiquetar_fondo(ident, fecha)
            previos.append((ident, self._referencias_fondo(sid, n_prov), fecha))
        # Reincidencia legítima: la misma persona renueva con sus mismos datos (>= 90 días después).
        for _ in range(self.n(200)):
            ident, refs, f0 = previos[int(r.integers(0, len(previos)))]
            d0 = (f0 - FECHA_INICIO).days
            if d0 > DIAS_LOTE - 100:
                continue
            sid2 = self._etiquetar_fondo(ident, self.dia(d0 + self.entero(90, DIAS_LOTE - 1 - d0)))
            for persona, relacion, tel in refs:
                self.referencia(sid2, persona, relacion, tel)

    def _jornadas(self, ag_idx: int) -> list[int]:
        if ag_idx not in self._jornadas_ag:
            self._jornadas_ag[ag_idx] = [self.entero(0, DIAS_LOTE - 3) for _ in range(6)]
        return self._jornadas_ag[ag_idx]

    def _etiquetar_fondo(self, ident: dict, fecha: date) -> str:
        """Las solicitudes por tableta de agencia son señuelo (mismo dispositivo, personas distintas)."""
        if ident["canal"] == "promotor_tableta":
            return self.solicitud(ident, fecha, etiqueta="legitima_senuelo",
                                  red=self._red_tableta(ident["d_idx"]), rol="usuario_tableta")
        return self.solicitud(ident, fecha)

    def _red_tableta(self, ag_idx: int) -> str:
        if ag_idx not in self._red_tab:
            self._red_tab[ag_idx] = self.red(
                "legitima_senuelo", "tableta_agencia", "media",
                "mismo dispositivo (tableta de agencia) en solicitudes de personas distintas")
        return self._red_tab[ag_idx]

    def _referencias_fondo(self, sid: str, n_prov: int) -> list[tuple[str, str, str]]:
        refs = []
        for _ in range(2):
            ranura = -1
            if self.rng.random() < 0.25:  # proveedor común: hub legítimo con grado alto
                c = self.entero(0, n_prov - 1)
                if c >= len(self._prov_uso) or self._prov_uso[c] < 10:
                    ranura = c
            if ranura >= 0:
                persona, tel = self._proveedor(ranura)
                relacion = "proveedor"
            else:
                persona, tel = self.persona("normal"), self.telefono()
                relacion = self.elegir(RELACIONES_NORMALES)
            self.referencia(sid, persona, relacion, tel)
            refs.append((persona, relacion, tel))
        return refs

    # ---------- redes de fraude ----------
    def _ventana_senuelo(self, corta: int, larga: int, p_corta: float) -> tuple[int, int]:
        """Los señuelos también pueden llegar en ráfaga (campañas, hogares que piden juntos)."""
        v = corta if self.rng.random() < p_corta else larga
        return self.inicio_ventana(v), v

    def _fechas(self, k: int, ventana: int) -> list[date]:
        ini = self.inicio_ventana(ventana)
        return sorted(self.dia(ini + self.entero(0, ventana)) for _ in range(k))

    def anillo(self, dificultad: str) -> None:
        k = self.entero(5, 8)
        extras = {"baja": 2, "media": 1, "alta": 0}[dificultad]
        rid = self.red("fraude", "anillo", dificultad,
                       "referencias circulares entre solicitantes; negocios y teléfonos recientes")
        d_idx = self.distrito_idx()
        rubros = [self.elegir(list(RUBROS)) for _ in range(2)]
        local_comun = self.direccion("local_comercial", AGENCIAS[d_idx][2]) if extras >= 1 else None
        disp_comun = self.dispositivo("smartphone") if extras >= 2 else None
        idents = []
        for i in range(k):
            canal = "app_movil" if (extras >= 2 and i in (1, 3)) else self.elegir(("agencia", "app_movil"))
            idents.append(self.identidad(
                "fraude", d_idx, rubros[i % 2], canal=canal,
                local=local_comun if i in (0, 2) else None,
                disp=disp_comun if i in (1, 3) else None))
        centro = float(self.rng.uniform(8000, 14000))
        sids = []
        for i, (ident, f) in enumerate(zip(idents, self._fechas(k, {'baja': 14, 'media': 45, 'alta': 90}[dificultad]))):
            sids.append(self.solicitud(ident, f, monto=centro * self.rng.uniform(0.85, 1.15),
                                       etiqueta="fraude", red=rid, rol="miembro"))
        for i, sid in enumerate(sids):
            sig = idents[(i + 1) % k]
            self.referencia(sid, sig["persona"], self.elegir(("amigo", "proveedor", "cliente")),
                            sig["tel"])
            self.referencia_nueva(sid, "vecino")

    def estrella(self, dificultad: str) -> None:
        k = self.entero(6, 12)
        p_disp = {"baja": 1.0, "media": 0.5, "alta": 0.0}[dificultad]
        rid = self.red("fraude", "estrella", dificultad,
                       "un mismo contacto de referencia (y teléfono) respalda solicitudes de personas "
                       "sin relación aparente")
        d_idx = self.distrito_idx()
        cab_persona = self.persona("fraude")
        tel_cab = self.telefono(joven=True)
        disp_cab: list[str] = []  # se crea al primer uso para no dejar dispositivos huérfanos

        def dispositivo_cabecilla() -> str:
            if not disp_cab:
                disp_cab.append(self.dispositivo("smartphone"))
            return disp_cab[0]

        fechas = self._fechas(k + 1, {'baja': 20, 'media': 50, 'alta': 90}[dificultad])
        if self.rng.random() < 0.5:  # a veces el cabecilla también solicita
            cab = self.identidad("fraude", d_idx, canal="app_movil", persona=cab_persona,
                                 tel=tel_cab, disp=dispositivo_cabecilla())
            sid = self.solicitud(cab, fechas[-1], etiqueta="fraude", red=rid, rol="cabecilla")
            self.referencia_nueva(sid, "vecino")
        for i in range(k):
            usa_disp = self.rng.random() < p_disp
            ident = self.identidad("fraude", d_idx, canal="app_movil" if usa_disp else
                                   self.elegir(("agencia", "app_movil")),
                                   disp=dispositivo_cabecilla() if usa_disp else None)
            sid = self.solicitud(ident, fechas[i], etiqueta="fraude", red=rid, rol="testaferro")
            self.referencia(sid, cab_persona, self.elegir(("familiar", "amigo", "proveedor")), tel_cab)
            self.referencia_nueva(sid, "vecino")

    def dispositivo_compartido(self, dificultad: str) -> None:
        k = self.entero(5, 10)
        ventana = {"baja": 5, "media": 20, "alta": 45}[dificultad]
        p_estruct = {"baja": 1.0, "media": 0.6, "alta": 0.0}[dificultad]
        rid = self.red("fraude", "dispositivo_compartido", dificultad,
                       "un mismo dispositivo envía solicitudes de identidades distintas; montos "
                       "cercanos al umbral de revisión")
        d_idx = self.distrito_idx()
        disp = self.dispositivo("smartphone")
        for f in self._fechas(k, ventana):
            ident = self.identidad("fraude", d_idx, canal="app_movil", disp=disp)
            sid = self.solicitud(ident, f, etiqueta="fraude", red=rid, rol="identidad_usada",
                                 estructurar=self.rng.random() < p_estruct)
            self.referencia_nueva(sid, perfil="fraude", joven=True)
            self.referencia_nueva(sid)

    def direccion_fantasma(self, dificultad: str) -> None:
        k = self.entero(4, 9)
        d_idx = self.distrito_idx()
        distrito = AGENCIAS[d_idx][2]
        compartida = dificultad == "alta"
        rid = self.red("fraude", "direccion_fantasma", dificultad,
                       "muchos solicitantes sin relación declaran el mismo inmueble de pocos hogares"
                       if not compartida else
                       "muchos negocios nuevos declaran el mismo local en oficina compartida")
        fantasma = self.direccion("oficina_compartida" if compartida else "vivienda", distrito,
                                  12 if compartida else 1)
        for f in self._fechas(k, {'baja': 25, 'media': 60, 'alta': 100}[dificultad]):
            ident = self.identidad(
                "fraude", d_idx, canal=self.elegir(("agencia", "app_movil")),
                domicilio=None if compartida else fantasma,
                local=fantasma if dificultad in ("baja", "alta") else None)
            sid = self.solicitud(ident, f, etiqueta="fraude", red=rid, rol="negocio_fantasma")
            self.referencia_nueva(sid)
            self.referencia_nueva(sid)

    def evasiva_debil(self, dificultad: str) -> None:
        self.puente_ref = False
        try:
            self._evasiva_debil(dificultad)
        finally:
            self.puente_ref = True

    def _evasiva_debil(self, dificultad: str) -> None:
        k = self.entero(4, 6)
        rid = self.red("fraude", "evasiva_debil", dificultad,
                       "cadena de vínculos débiles de tipos distintos (teléfono, domicilio, "
                       "referencia, dispositivo, local); ningún vínculo aislado alcanza para alertar")
        d_idx = self.distrito_idx()
        fechas = self._fechas(k, {'baja': 28, 'media': 60, 'alta': 100}[dificultad])
        ref_comun = (self.persona("fraude"), self.telefono(joven=True))
        idents: list[dict] = []
        for i in range(k):  # eslabones: 0-1 teléfono, 1-2 domicilio, 2-3 referencia, 3-4 dispositivo, 4-5 local
            kw: dict = {"canal": "app_movil" if i in (3, 4) else self.elegir(("agencia", "app_movil"))}
            if i == 1:
                kw["tel"] = idents[0]["tel"]
            if i == 2:
                kw["domicilio"] = idents[1]["dom"]
            if i == 4:
                kw["disp"] = idents[3]["disp"]
            if i == 5:
                kw["local"] = self._local_de(idents[4])
            idents.append(self.identidad("fraude", d_idx, **kw))
        for i, (ident, f) in enumerate(zip(idents, fechas)):
            sid = self.solicitud(ident, f, etiqueta="fraude", red=rid, rol="eslabon",
                                 estructurar=self.rng.random() < 0.7)
            if i in (2, 3):
                self.referencia(sid, ref_comun[0], "amigo", ref_comun[1])
            else:
                self.referencia_nueva(sid)
            self.referencia_nueva(sid)

    def _local_de(self, ident: dict) -> str:
        return next(n["direccion_id"] for n in self.t["negocios"] if n["negocio_id"] == ident["negocio"])

    # ---------- señuelos legítimos ----------
    def familia(self) -> None:
        k = self.entero(2, 5)
        rid = self.red("legitima_senuelo", "familia", "alta",
                       "hogar con mismo domicilio, teléfono compartido y referencias familiares mutuas")
        d_idx = self.distrito_idx()
        distrito = AGENCIAS[d_idx][2]
        ap = (self.elegir(APELLIDOS), self.elegir(APELLIDOS))
        extendida = self.rng.random() < 0.25  # cuñados, compadres: sin apellido común
        dom = self.direccion("vivienda", distrito, 1)
        comunes: dict[str, str] = {}  # teléfono del hogar y local familiar, creados al primer uso
        idents = []
        for i in range(k):
            kw: dict = {}
            if self.rng.random() >= 0.4:
                if "tel" not in comunes:
                    comunes["tel"] = self.telefono()
                kw["tel"] = comunes["tel"]
            if self.rng.random() < 0.4:
                if "local" not in comunes:
                    comunes["local"] = self.direccion("local_comercial", distrito)
                kw["local"] = comunes["local"]
            idents.append(self.identidad(
                "maduro", d_idx, domicilio=dom, canal=self.elegir(("agencia", "app_movil")),
                apellidos=(self.elegir(APELLIDOS), self.elegir(APELLIDOS)) if (i and extendida) else (
                    (ap[0], self.elegir(APELLIDOS)) if i else ap), **kw))
        base, v = self._ventana_senuelo(12, 190, 0.50)
        sids = [self.solicitud(ident, self.dia(base + self.entero(0, v)),
                               etiqueta="legitima_senuelo", red=rid, rol="miembro_hogar")
                for ident in idents]
        for i, sid in enumerate(sids):
            otro = idents[(i + 1) % k]
            self.referencia(sid, otro["persona"], "familiar", otro["tel"])
            self.referencia_nueva(sid)

    def mercado_grupo(self) -> None:
        k = self.entero(8, 14)
        rid = self.red("legitima_senuelo", "mercado", "media",
                       "puestos del mismo mercado: dirección compartida y referencias entre vecinos")
        idx = self.entero(0, len(MERCADOS) - 1)
        d_idx = MERCADOS[idx][1]
        perfil = "maduro" if self.rng.random() < 0.6 else "normal"  # a veces, comerciantes nuevos
        idents = [self.identidad(perfil, d_idx, self.elegir(RUBROS_MERCADO),
                                 canal=self.elegir(("agencia", "app_movil")), mercado_idx=idx)
                  for _ in range(k)]
        base, v = self._ventana_senuelo(30, 240, 0.50)
        sids = [self.solicitud(i, self.dia(base + self.entero(0, v)),
                               etiqueta="legitima_senuelo", red=rid, rol="comerciante_mercado")
                for i in idents]
        for sid, ident in zip(sids, idents):
            otros = [x for x in idents if x is not ident]
            for pos in self.rng.choice(len(otros), 2, replace=False):
                self.referencia(sid, otros[int(pos)]["persona"],
                                self.elegir(("vecino", "proveedor")), otros[int(pos)]["tel"])

    def asociacion_gremial(self) -> None:
        k = self.entero(5, 9)
        rid = self.red("legitima_senuelo", "asociacion_gremial", "alta",
                       "socios de un gremio con avales cruzados en cadena; negocios antiguos y "
                       "clientes de larga data")
        d_idx = self.distrito_idx()
        rubro = self.elegir(("transporte", "avicola", "agricola", "panaderia"))
        idents = [self.identidad("maduro", d_idx, rubro, antig_min=24,
                                 canal=self.elegir(("agencia", "app_movil"))) for _ in range(k)]
        base, v = self._ventana_senuelo(45, 190, 0.50)
        sids = [self.solicitud(i, self.dia(base + self.entero(0, v)),
                               etiqueta="legitima_senuelo", red=rid, rol="socio_gremial")
                for i in idents]
        for i, sid in enumerate(sids):
            for j in (1, 2):
                if k > j:
                    otro = idents[(i + j) % k]
                    self.referencia(sid, otro["persona"], "socio_gremial", otro["tel"])

    def gestor_contador(self) -> None:
        k = self.entero(6, 12)
        rid = self.red("legitima_senuelo", "gestor_contador", "alta",
                       "un mismo contador/gestor figura como contacto de muchos solicitantes "
                       "con negocios antiguos")
        d_idx = self.distrito_idx()
        contador = self.persona("maduro")
        tel_c = self.telefono()
        base, v = self._ventana_senuelo(60, 270, 0.40)
        for _ in range(k):
            ident = self.identidad("maduro", d_idx, antig_min=18,
                                   canal=self.elegir(("agencia", "app_movil")))
            sid = self.solicitud(ident, self.dia(base + self.entero(0, v)),
                                 etiqueta="legitima_senuelo", red=rid, rol="cliente_de_gestor")
            self.referencia(sid, contador, "asesor_contable", tel_c)
            self.referencia_nueva(sid)

    def coincidencia_casual(self) -> None:
        self.puente_ref = False
        try:
            self._coincidencia_casual()
        finally:
            self.puente_ref = True

    def _coincidencia_casual(self) -> None:
        tipo = self.elegir(("telefono", "dispositivo", "referencia", "domicilio"))
        rid = self.red("legitima_senuelo", "coincidencia_casual", "baja",
                       f"un único dato compartido por casualidad ({tipo}); sin otros vínculos")
        d_idx = self.distrito_idx()
        f1 = self.entero(0, DIAS_LOTE - 130)
        f2 = f1 + self.entero(60, 120)
        kw1: dict = {}
        kw2: dict = {}
        compartido: dict = {}
        if tipo == "telefono":
            compartido["tel"] = self.telefono()
            kw1["tel"] = kw2["tel"] = compartido["tel"]
        elif tipo == "dispositivo":
            compartido["disp"] = self.dispositivo("smartphone")
            kw1.update(disp=compartido["disp"], canal="app_movil")
            kw2.update(disp=compartido["disp"], canal="app_movil")
        elif tipo == "domicilio":
            compartido["dom"] = self.direccion("vivienda_multifamiliar",
                                               AGENCIAS[d_idx][2], self.entero(4, 8))
            kw1["domicilio"] = kw2["domicilio"] = compartido["dom"]
        for kw in (kw1, kw2):
            kw.setdefault("canal", self.elegir(("agencia", "app_movil")))
        a = self.identidad("normal", d_idx, **kw1)
        b = self.identidad("normal", d_idx, **kw2)
        sa = self.solicitud(a, self.dia(f1), etiqueta="legitima_senuelo", red=rid, rol="coincidencia")
        sb = self.solicitud(b, self.dia(f2), etiqueta="legitima_senuelo", red=rid, rol="coincidencia")
        if tipo == "referencia":
            p, t = self.persona("normal"), self.telefono()
            self.referencia(sa, p, "vecino", t)
            self.referencia(sb, p, "amigo", t)
        else:
            self.referencia_nueva(sa)
            self.referencia_nueva(sb)
        self.referencia_nueva(sa)
        self.referencia_nueva(sb)

    # ---------- cierre ----------
    def finalizar(self) -> dict[str, pd.DataFrame]:
        r = self.rng
        sol = pd.DataFrame(self.t["solicitudes"])
        # Orden por fecha con desempate aleatorio: el orden de creación no delata las redes.
        sol = (sol.assign(_k=r.random(len(sol))).sort_values(["fecha_solicitud", "_k"])
               .drop(columns="_k").reset_index(drop=True))
        dfs = {k: pd.DataFrame(v) for k, v in self.t.items()}
        dfs["solicitudes"] = sol

        def mapa(df: pd.DataFrame, col: str, prefijo: str, orden: bool = False) -> dict[str, str]:
            viejos = df[col].tolist()
            nuevos = list(range(1, len(viejos) + 1))
            if not orden:
                nuevos = [int(x) + 1 for x in r.permutation(len(viejos))]
            return {v: f"{prefijo}{n:06d}" for v, n in zip(viejos, nuevos)}

        m_p = mapa(dfs["personas"], "persona_id", "P")
        m_n = mapa(dfs["negocios"], "negocio_id", "N")
        m_d = mapa(dfs["direcciones"], "direccion_id", "D")
        m_t = mapa(dfs["telefonos"], "telefono_id", "T")
        m_v = mapa(dfs["dispositivos"], "dispositivo_id", "V")
        m_s = mapa(dfs["solicitudes"], "solicitud_id", "S", orden=True)
        m_v[""] = ""

        dfs["personas"]["persona_id"] = dfs["personas"]["persona_id"].map(m_p)
        dfs["negocios"]["negocio_id"] = dfs["negocios"]["negocio_id"].map(m_n)
        dfs["negocios"]["propietario_id"] = dfs["negocios"]["propietario_id"].map(m_p)
        dfs["negocios"]["direccion_id"] = dfs["negocios"]["direccion_id"].map(m_d)
        dfs["direcciones"]["direccion_id"] = dfs["direcciones"]["direccion_id"].map(m_d)
        dfs["telefonos"]["telefono_id"] = dfs["telefonos"]["telefono_id"].map(m_t)
        dfs["dispositivos"]["dispositivo_id"] = dfs["dispositivos"]["dispositivo_id"].map(m_v)
        s = dfs["solicitudes"]
        old_sid = s["solicitud_id"].copy()
        s["solicitud_id"] = old_sid.map(m_s)
        s["solicitante_id"] = s["solicitante_id"].map(m_p)
        s["negocio_id"] = s["negocio_id"].map(m_n)
        s["telefono_id"] = s["telefono_id"].map(m_t)
        s["dispositivo_id"] = s["dispositivo_id"].map(m_v)
        s["direccion_domicilio_id"] = s["direccion_domicilio_id"].map(m_d)
        ref = dfs["referencias"]
        ref["solicitud_id"] = ref["solicitud_id"].map(m_s)
        ref["persona_referencia_id"] = ref["persona_referencia_id"].map(m_p)
        ref["telefono_referencia_id"] = ref["telefono_referencia_id"].map(m_t)
        ref = ref.sort_values(["solicitud_id"], kind="stable").reset_index(drop=True)
        ref["referencia_id"] = [f"R{i + 1:06d}" for i in range(len(ref))]
        dfs["referencias"] = ref
        et = dfs["etiquetas"]
        et["solicitud_id"] = et["solicitud_id"].map(m_s)

        for nombre, col in (("personas", "persona_id"), ("negocios", "negocio_id"),
                            ("direcciones", "direccion_id"), ("telefonos", "telefono_id"),
                            ("dispositivos", "dispositivo_id")):
            dfs[nombre] = dfs[nombre].sort_values(col).reset_index(drop=True)
        dfs["solicitudes"] = s.sort_values("solicitud_id").reset_index(drop=True)
        dfs["agencias"] = pd.DataFrame(
            [{"agencia_id": a[0], "nombre_agencia": a[1], "distrito": a[2], "provincia": a[3]}
             for a in AGENCIAS])

        # Partición dev/eval: por red (alternada por patrón) y al azar para solicitudes normales.
        redes = pd.DataFrame(self.redes.values())
        part: dict[str, str] = {}
        for patron, grupo in redes.groupby("patron", sort=True):
            ids = grupo["red_id"].tolist()
            inicio = int(r.integers(0, 2))
            orden = [ids[i] for i in r.permutation(len(ids))]
            for j, rid in enumerate(orden):
                part[rid] = "dev" if (j + inicio) % 2 == 0 else "eval"
        redes["particion"] = redes["red_id"].map(part)
        cuenta = dfs["solicitudes"].merge(et, on="solicitud_id")
        cuenta = cuenta[cuenta["red_id"] != ""]
        agg = cuenta.groupby("red_id").agg(
            n_solicitudes=("solicitud_id", "count"),
            n_personas=("solicitante_id", "nunique"),
            fecha_inicio=("fecha_solicitud", "min"), fecha_fin=("fecha_solicitud", "max"))
        redes = redes.merge(agg, left_on="red_id", right_index=True, how="left")
        redes = redes[["red_id", "clase", "patron", "dificultad", "particion", "n_solicitudes",
                       "n_personas", "fecha_inicio", "fecha_fin", "vinculos_clave"]]
        dfs["redes_verdad"] = redes.sort_values("red_id").reset_index(drop=True)

        et["particion"] = et["red_id"].map(part)
        normales = et["red_id"] == ""
        et.loc[normales, "particion"] = np.where(r.random(int(normales.sum())) < 0.5, "dev", "eval")
        dfs["etiquetas_solicitudes"] = et.sort_values("solicitud_id").reset_index(drop=True)
        del dfs["etiquetas"]
        return dfs


def generar(semilla: int = SEMILLA_POR_DEFECTO, escala: float = 1.0) -> dict[str, pd.DataFrame]:
    """Genera todas las tablas en memoria. Determinista para (semilla, escala)."""
    m = Mundo(semilla, escala)
    m.fondo()
    m.puente_ref = True
    builders = {
        "anillo": m.anillo, "estrella": m.estrella,
        "dispositivo_compartido": m.dispositivo_compartido,
        "direccion_fantasma": m.direccion_fantasma, "evasiva_debil": m.evasiva_debil,
    }
    for patron in PATRONES_FRAUDE:
        for i in range(m.n(6)):
            builders[patron](DIFICULTADES[i % len(DIFICULTADES)])
    for _ in range(m.n(25)):
        m.familia()
    for _ in range(m.n(6)):
        m.mercado_grupo()
    for _ in range(m.n(6)):
        m.asociacion_gremial()
    for _ in range(m.n(6)):
        m.gestor_contador()
    for _ in range(m.n(40)):
        m.coincidencia_casual()
    return m.finalizar()


def resumen(dfs: dict[str, pd.DataFrame], semilla: int, escala: float) -> dict:
    et = dfs["etiquetas_solicitudes"]
    redes = dfs["redes_verdad"]
    return {
        "version_esquema": VERSION_ESQUEMA,
        "aviso": "Datos 100 % sintéticos. Documentos y teléfonos ficticios (prefijo FIC-). "
                 "Sin personas reales.",
        "semilla": semilla,
        "escala": escala,
        "umbral_revision_pen_supuesto": UMBRAL_REVISION_PEN,
        "rango_fechas": [dfs["solicitudes"]["fecha_solicitud"].min(),
                         dfs["solicitudes"]["fecha_solicitud"].max()],
        "filas": {k: int(len(v)) for k, v in sorted(dfs.items())},
        "solicitudes_por_etiqueta": {k: int(v) for k, v in et["etiqueta"].value_counts().sort_index().items()},
        "redes_por_patron": {k: int(v) for k, v in redes["patron"].value_counts().sort_index().items()},
        "redes_fraude": int((redes["clase"] == "fraude").sum()),
        "redes_senuelo": int((redes["clase"] == "legitima_senuelo").sum()),
    }


def escribir(dfs: dict[str, pd.DataFrame], salida: Path, semilla: int, escala: float) -> dict:
    salida.mkdir(parents=True, exist_ok=True)
    for nombre, df in dfs.items():
        df.to_csv(salida / f"{nombre}.csv", index=False, encoding="utf-8", lineterminator="\n")
    info = resumen(dfs, semilla, escala)
    (salida / "manifest.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return info


def main(argv: list[str] | None = None) -> int:
    aqui = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--semilla", type=int, default=SEMILLA_POR_DEFECTO)
    ap.add_argument("--escala", type=float, default=1.0, help="multiplica los volúmenes (1.0 = estándar)")
    ap.add_argument("--salida", type=Path, default=aqui / "sintetico")
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    info = escribir(generar(a.semilla, a.escala), a.salida, a.semilla, a.escala)
    print(f"Datos sintéticos RIE-02 escritos en {a.salida}")
    print(json.dumps(info["filas"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
