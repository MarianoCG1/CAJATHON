"""Genera el borrador v0 del Concepto de solución de cada desafío (herramienta de planificación).

Combina `conceptos.json` (contenido), `../sinergia/challenges.json` (tareas y horas),
`../sinergia/team.json` (niveles) y el reparto de parejas / ranking de `sinergia.py`.

Uso:
    python scripts/conceptos/generar_borradores.py                  # crea retos/<ID>/concepto.md
    python scripts/conceptos/generar_borradores.py --forzar         # sobrescribe borradores existentes

Por seguridad NO sobrescribe archivos existentes sin --forzar, para no pisar el trabajo del equipo.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI.parent / "sinergia"))

import sinergia as sg  # noqa: E402

SECCIONES = [
    "1. Problema abordado",
    "2. Concepto de solución",
    "3. Impacto esperado en el KPI",
    "4. Enfoque tecnológico",
    "5. Tecnología preexistente",
    "6. Funcionalidad crítica",
    "7. Nivel de desarrollo esperado",
    "8. Factibilidad y dependencias",
]

TECNOLOGIA = {
    "backend": "API REST con FastAPI y Pydantic v2; persistencia en SQLite",
    "web": "Interfaz React + Vite + Tailwind CSS con componentes ya hechos",
    "ia_gen": "LLM para redactar resúmenes y mensajes, con salidas estructuradas y verificación contra los datos",
    "agentes": "Agente con Pydantic AI y proveedor de LLM intercambiable (Claude, OpenAI o modelo local); herramientas acotadas y aprobación humana",
    "ml": "Modelos con scikit-learn (y LightGBM si aporta), con calibración y validación temporal",
    "data_sci": "Análisis estadístico, explicabilidad y optimización con pandas, scikit-learn y SciPy",
    "data_eng": "Generador de datos sintéticos reproducible (semilla fija) y ETL con pandas",
    "bi": "Indicadores y vistas de seguimiento dentro de la propia interfaz",
    "qa": "Pruebas automáticas con pytest y reporte de validación (docs/validacion.md)",
    "ux": "Flujo del usuario validado con prototipo navegable",
    "biz": "Backtest del KPI con y sin la solución (scripts/evaluar_kpi.py)",
    "proc": "Mapa del proceso actual y propuesto",
    "fin": "Reglas y criterios de dominio validados con Caja Experts",
    "pitch": "Guion de demo y presentación",
}


def _tabla_tareas(info: dict) -> str:
    filas = ["| Tarea | Habilidad | Horas |", "|---|---|---|"]
    for tarea, hab, h in info["paquetes"]:
        filas.append(f"| {tarea} | {hab} | {h} |")
    return "\n".join(filas)


def borrador(id_: str, info: dict, c: dict, niveles: dict, plan: dict, rango: int, equipo_habil: dict) -> str:
    pareja = plan[id_]
    horas = sum(h for _, _, h in info["paquetes"])
    gaps_par = sg.brechas(pareja, info, niveles)
    gaps_eq = sg.brechas(tuple(sorted(niveles)), info, niveles)
    cob_eq = sg.cobertura(tuple(sorted(niveles)), info, niveles)
    habs = sorted({h for _, h, _ in info["paquetes"]}, key=lambda x: -sum(t[2] for t in info["paquetes"] if t[1] == x))
    L = []
    L.append(f"# Concepto de solución — {id_} · {info['titulo']}\n")
    L.append(f"> **BORRADOR v0 (generado).** Prioridad **#{rango}** · Pareja líder **{' + '.join(pareja)}** · "
             f"Eje: {info['eje']} · Owners (plataforma): {c['owners']}.")
    L.append("> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.\n")

    L.append(f"## {SECCIONES[0]}\n")
    L.append(c["problema"] + "\n")
    L.append("Riesgos y restricciones que el expediente pide respetar: " + "; ".join(c["riesgos_clave"]) + ".\n")

    L.append(f"## {SECCIONES[1]}\n")
    L.append(info["hipotesis"] + " **(supuesto)**\n")
    L.append(f"**Diferenciación:** {c['diferenciacion']}\n")
    L.append("**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana y no se ejecutan acciones crediticias automáticas.\n")

    L.append(f"## {SECCIONES[2]}\n")
    L.append("KPI candidatos **(supuesto, a validar con el owner)**:\n")
    for k in c["kpi_candidatos"]:
        L.append(f"- {k}")
    L.append("\n- **Línea base:** [POR CONFIRMAR con el owner]")
    L.append("- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]")
    L.append("- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija.\n")

    L.append(f"## {SECCIONES[3]}\n")
    L.append("Pila base: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.\n")
    L.append("Componentes que requiere este desafío (según las tareas):\n")
    for h in habs:
        L.append(f"- **{equipo_habil[h]}:** {TECNOLOGIA[h]}")
    L.append("\nEl expediente exige capacidades avanzadas con valor real y desarrollo funcional; "
             "no basta un chatbot genérico, un dashboard, un formulario o una automatización básica. "
             "El valor diferencial está en el modelo y el agente descritos arriba.\n")

    L.append(f"## {SECCIONES[4]}\n")
    L.append("- Librerías de código abierto (FastAPI, pandas, scikit-learn, React, etc.) bajo sus licencias.")
    L.append("- Generador de datos sintéticos y herramientas de planificación del equipo (titularidad: equipo; ver `docs/preexistente.md`).")
    L.append("- **No se reutiliza código de empleadores ni de otros clientes.** No se usan datos reales.\n")

    L.append(f"## {SECCIONES[5]}\n")
    L.append(c["funcionalidad_critica"] + " **(supuesto)**\n")
    L.append("Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.\n")

    L.append(f"## {SECCIONES[6]}\n")
    L.append(f"Prototipo funcional de punta a punta con caso de uso: {c['demo']}\n")
    L.append("Incluye pruebas automáticas, reporte de validación y un número antes/después del KPI.\n")

    L.append(f"## {SECCIONES[7]}\n")
    L.append(f"- **Esfuerzo estimado del MVP:** {horas} horas-persona **(supuesto)**. En el evento hay ~8 h por persona ({8 * len(niveles)} h con {len(niveles)} personas).")
    L.append(f"- **Cobertura de habilidades del equipo:** {cob_eq:.0%}. "
             + ("Sin brechas relevantes." if not gaps_eq else "Brechas: " + "; ".join(f"{t} ({h} h)" for t, _, _, h in gaps_eq) + "."))
    if gaps_par:
        L.append("- **Brechas de la pareja líder** (cubre el resto del equipo): " + "; ".join(f"{t} ({h} h)" for t, _, _, h in gaps_par) + ".")
    L.append("- **Dependencias:** datos sintéticos de la Caja (si no llegan, usamos nuestro generador); "
             "política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**.")
    L.append("- **Recorte si falta tiempo:** se mantiene el núcleo (modelo + recomendación + backtest) y se simplifica la interfaz.\n")

    L.append("---\n")
    L.append("## Anexo A. Tareas y horas (supuesto)\n")
    L.append(_tabla_tareas(info) + "\n")
    L.append("## Anexo B. Preguntas para el owner\n")
    for q in c["preguntas_owner"]:
        L.append(f"- [ ] {q}")
    L.append("\n## Anexo C. Lista de revisión (criterios del pase a finalistas)\n")
    L.append("- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?")
    L.append("- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?")
    L.append("- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?")
    L.append("- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?")
    L.append("- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.")
    L.append("- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].")
    L.append("- [ ] Revisado por alguien que no lo escribió.")
    return "\n".join(L) + "\n"


def generar(raiz: Path, forzar: bool = False) -> list[Path]:
    equipo, niveles, desafios = sg.cargar()
    contenido = json.loads((AQUI / "conceptos.json").read_text(encoding="utf-8"))["desafios"]
    faltan = set(desafios) ^ set(contenido)
    if faltan:
        raise ValueError(f"conceptos.json y challenges.json no coinciden: {sorted(faltan)}")
    plan, _, _ = sg.asignar(niveles, desafios)
    filas = sg.prioridad(niveles, desafios, sg.cargar_valoracion())
    rango = {f["id"]: i for i, f in enumerate(filas, 1)}
    creados = []
    for f in filas:
        id_ = f["id"]
        ruta = raiz / "retos" / id_ / "concepto.md"
        if ruta.exists() and not forzar:
            print(f"Se conserva retos/{id_}/concepto.md (ya existe; usa --forzar para regenerar)")
            continue
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(borrador(id_, desafios[id_], contenido[id_], niveles, plan, rango[id_], equipo["habilidades"]),
                        encoding="utf-8")
        creados.append(ruta)
    return creados


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", type=Path, default=RAIZ, help="raíz del proyecto (escribe en <raiz>/retos/<ID>/concepto.md)")
    ap.add_argument("--forzar", action="store_true")
    a = ap.parse_args()
    for r in generar(a.raiz, a.forzar):
        print("Creado", r.relative_to(RAIZ) if r.is_relative_to(RAIZ) else r)


if __name__ == "__main__":
    main()
