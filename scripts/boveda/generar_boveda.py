"""Genera los nodos de reto, el HUB y el tablero de avance de la bóveda (herramienta de planificación).

La bóveda es Markdown con enlaces [[...]] (compatible con Obsidian). Para que los enlaces
con ruta funcionen, abrir la carpeta RAÍZ del proyecto como bóveda.

Qué genera:
  boveda/00-HUB-Cajathon.md    punto de entrada (competencia + retos + equipo)
  boveda/Tablero.md            avance de todos los retos, calculado leyendo los archivos
  boveda/Retos/<ID>.md         un nodo por reto, con avance automático

Las notas de `boveda/Competencia/` y `boveda/Decisiones/` son manuales y no se tocan.
Cada nodo tiene un bloque automático entre marcas; **lo que se escriba debajo de la
marca final se conserva** al regenerar.

Uso:
    python scripts/boveda/generar_boveda.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(AQUI.parent / "sinergia"))

import sinergia as sg  # noqa: E402

INICIO = "<!-- AUTO:inicio (no editar; se regenera) -->"
FIN = "<!-- AUTO:fin -->"

REVISOR = {
    "RIE-03": "Glem", "NEG-01": "David", "NEG-02": "David", "RIE-01": "Glem",
    "RIE-02": "Antonio", "NEG-03": "Antonio", "COM-01": "David", "COM-02": "Mariano",
}

PASOS = [
    ("borrador", "Borrador v0 del concepto"),
    ("v1", "Concepto v1 (editado por la pareja)"),
    ("panorama", "Panorama de abastecimiento"),
    ("cotejo", "Cotejo con el expediente literal"),
    ("datos", "Generador de datos sintéticos con pruebas"),
    ("postulacion", "Texto de postulación"),
]

NOTAS_MANUALES = """
## Notas del equipo (se conservan al regenerar)

### Seguimiento manual
- [ ] Preguntas enviadas al owner
- [ ] Respuesta del owner recibida (KPI y línea base)
- [ ] Revisión cruzada hecha por el revisor
- [ ] Decisión de postular este reto

### Notas
-
"""


def _wiki(ruta: str, texto: str) -> str:
    return f"[[{ruta}|{texto}]]"


def _leer(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _rutas(id_: str, raiz: Path, orden: int) -> dict[str, Path | None]:
    base = raiz / "retos" / id_
    concepto = base / "concepto.md"
    return {
        "concepto": concepto if concepto.exists() else None,
        "panorama": base / "panorama.md",
        "expediente": base / "expediente.md",  # confidencial: no se sube al repo (.gitignore)
        "postulacion": base / "postulacion.md",
        "generador": base / "datos" / "generar.py",
        "datos": base / "datos" / "sintetico",
    }


def avance(id_: str, raiz: Path = RAIZ) -> dict:
    """Estado de cada paso, leyendo el disco. Devuelve pasos, métricas y estado global."""
    r = _rutas(id_, raiz, 0)
    concepto = _leer(r["concepto"]) if r["concepto"] else ""
    panorama = _leer(r["panorama"])
    pasos = {
        "borrador": bool(concepto),
        "v1": bool(concepto) and "BORRADOR v0 (generado)" not in concepto,
        "panorama": r["panorama"].exists(),
        # el expediente literal no viaja en el repo; el cotejo queda registrado en el propio panorama
        "cotejo": "Cotejo con el expediente" in panorama,
        "datos": r["generador"].exists(),
        "postulacion": r["postulacion"].exists(),
    }
    n = sum(pasos.values())
    if pasos["postulacion"] and pasos["cotejo"] and pasos["panorama"]:
        estado = "Listo para revisión cruzada"
    elif pasos["v1"]:
        estado = "Concepto v1"
    elif pasos["borrador"]:
        estado = "Borrador v0"
    else:
        estado = "Sin empezar"
    texto = concepto + "\n" + panorama
    return {
        "pasos": pasos,
        "hechos": n,
        "total": len(PASOS),
        "estado": estado,
        "por_confirmar": len(re.findall(r"\[POR CONFIRMAR", texto)),
        "supuestos": len(re.findall(r"\(supuesto", texto)),
        "palabras_postulacion": len(_leer(r["postulacion"]).split()),
        "rutas": r,
    }


def _barra(n: int, total: int) -> str:
    return "█" * n + "░" * (total - n) + f" {n}/{total}"


def _rel(p: Path, raiz: Path) -> str:
    return p.relative_to(raiz).with_suffix("").as_posix()


def nodo_reto(id_: str, orden: int, info: dict, c: dict, par: tuple, raiz: Path, hoy: str) -> str:
    a = avance(id_, raiz)
    r = a["rutas"]
    horas = sum(h for _, _, h in info["paquetes"])
    L = ["---", "tipo: reto", f"id: {id_}", f"prioridad: {orden}", f"estado: {a['estado']}",
         f"avance: {a['hechos']}/{a['total']}", f"pareja: {' + '.join(par)}",
         f"revisor: {REVISOR[id_]}", f"actualizado: {hoy}", "---", "", INICIO, "",
         f"# {id_} · {info['titulo']}", "",
         f"Volver al {_wiki('boveda/00-HUB-Cajathon', 'HUB')} · {_wiki('boveda/Tablero', 'Tablero')}", "",
         f"**Estado:** {a['estado']} · **Prioridad:** #{orden} · **Eje:** {info['eje']}",
         f"**Pareja líder:** {' + '.join(par)} · **Revisor:** {REVISOR[id_]} · **Owners (plataforma):** {c['owners']}", "",
         "## Avance (automático)", ""]
    for clave, etiqueta in PASOS:
        L.append(f"- [{'x' if a['pasos'][clave] else ' '}] {etiqueta}")
    L.append(f"\n`{_barra(a['hechos'], a['total'])}` · [POR CONFIRMAR]: {a['por_confirmar']} · (supuesto): {a['supuestos']}"
             + (f" · postulación: {a['palabras_postulacion']} palabras" if a["palabras_postulacion"] else ""))
    L.append("\n## Documentos\n")
    enlaces = [("Ficha del reto", raiz / "retos" / id_ / "README.md"), ("Concepto", r["concepto"]),
               ("Panorama de abastecimiento", r["panorama"]), ("Texto de postulación", r["postulacion"]),
               ("Generador de datos", r["generador"])]
    for etiqueta, ruta in enlaces:
        if ruta and ruta.exists() and ruta.suffix == ".md":
            L.append(f"- {etiqueta}: {_wiki(_rel(ruta, raiz), etiqueta)}")
        elif ruta and ruta.exists():
            L.append(f"- {etiqueta}: `{ruta.relative_to(raiz).as_posix()}`")
        else:
            L.append(f"- {etiqueta}: _pendiente_")
    L.append(f"- Expediente literal (confidencial, solo local; no se sube al repo): `retos/{id_}/expediente.md` — "
             + ("presente en este equipo" if r["expediente"].exists() else "no está en este equipo; copiarlo de la plataforma"))
    L.append("\n## Hipótesis de solución (supuesto)\n")
    L.append(info["hipotesis"])
    L.append("\n## KPI candidatos (supuesto, a validar con el owner)\n")
    L.extend(f"- {k}" for k in c["kpi_candidatos"])
    L.append(f"\n## Alcance estimado\n\n{horas} h-persona de MVP en el borrador v0 (el panorama trae horas revisadas y el escenario pesimista).")
    L.append("\n## Riesgos clave\n")
    L.extend(f"- {k}" for k in c["riesgos_clave"])
    L.append("\n## Preguntas para el owner\n")
    L.extend(f"- {q}" for q in c["preguntas_owner"])
    L.append("\nLas respuestas del owner actualizan KPI y línea base; el comunicado del 21.11 indica que en esta etapa no entregan datos.")
    L.append("\n" + FIN)
    return "\n".join(L) + "\n" + NOTAS_MANUALES


def tablero(filas: list[dict], hoy: str) -> str:
    L = ["---", "tipo: tablero", f"actualizado: {hoy}", "---", "",
         "# Tablero de avance", "",
         f"Calculado leyendo los archivos del proyecto el {hoy}. Volver al {_wiki('boveda/00-HUB-Cajathon', 'HUB')}.", "",
         "| # | Reto | Estado | Avance | Pareja | Revisor | [POR CONFIRMAR] | Postulación |",
         "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        L.append(f"| {f['orden']} | {_wiki('boveda/Retos/' + f['id'], f['id'])} {f['titulo']} | {f['estado']} | "
                 f"`{_barra(f['hechos'], f['total'])}` | {f['pareja']} | {f['revisor']} | {f['por_confirmar']} | "
                 f"{f['palabras'] or '—'} |")
    hechos = sum(f["hechos"] for f in filas)
    total = sum(f["total"] for f in filas)
    L.append(f"\n**Avance global:** {hechos}/{total} pasos ({hechos / total:.0%}).")
    L.append("\nPasos que se miden: " + " · ".join(e for _, e in PASOS) + ".")
    L.append("Los pasos manuales (preguntas, respuesta del owner, revisión cruzada, decisión) se anotan en cada nodo.")
    return "\n".join(L) + "\n"


def hub(filas: list[dict], hoy: str) -> str:
    L = ["---", "tipo: hub", f"actualizado: {hoy}", "---", "", INICIO, "",
         "# HUB · Cajathon 2026 — Yupana Labs", "",
         "Punto de entrada de la bóveda. Material **confidencial**: no publicar. Abrir la carpeta raíz del proyecto como bóveda.", "",
         "## 1. Competencia (nodo principal)", "",
         f"- {_wiki('boveda/Competencia/Bases-v4', 'Bases v4')}: objetivo, fases, equipos, entregables",
         f"- {_wiki('boveda/Competencia/Reglas-y-restricciones', 'Reglas y restricciones')}: confidencialidad, IA, propiedad intelectual, condición mínima",
         f"- {_wiki('boveda/Competencia/Criterios-de-evaluacion', 'Criterios de evaluación')}: pesos del pase y de la final",
         f"- {_wiki('boveda/Competencia/Calendario', 'Calendario')}: hitos y discrepancias de fechas",
         f"- {_wiki('boveda/Competencia/Plataforma-y-comunicados', 'Plataforma y comunicados')}: expedientes, recursos, confirmaciones",
         f"- {_wiki('boveda/Competencia/Panorama-competencia', 'Panorama de la competencia')}: 18 → 12 equipos",
         f"- {_wiki('boveda/Decisiones/Datos-reales-vs-sinteticos', 'Decisión: datos reales vs. sintéticos')}", "",
         "## 2. Retos (por prioridad)", "",
         f"Ver el {_wiki('boveda/Tablero', 'Tablero')} para el avance de cada uno.", "",
         "| # | Reto | Estado | Avance |", "|---|---|---|---|"]
    for f in filas:
        L.append(f"| {f['orden']} | {_wiki('boveda/Retos/' + f['id'], f['id'])} {f['titulo']} | {f['estado']} | `{_barra(f['hechos'], f['total'])}` |")
    L += ["", "## 3. Equipo y método", "",
          f"- {_wiki('docs/investigacion/03-equipo-y-alcance', 'Equipo y alcance')}",
          f"- {_wiki('docs/investigacion/04-sinergia-retos-parejas', 'Sinergia por pareja y prioridad')}",
          f"- {_wiki('docs/investigacion/05-alcance-comparado', 'Alcance comparado de los 4 desarrollados')}",
          f"- {_wiki('AGENTS', 'Guía para agentes (AGENTS.md)')} · {_wiki('retos/README', 'Índice de retos y asignaciones')}",
          f"- {_wiki('docs/plan-conceptos', 'Plan de conceptos')} · {_wiki('docs/preexistente', 'Preexistente')} · {_wiki('docs/consulta-organizacion', 'Consulta a la organización')}",
          "", FIN]
    return "\n".join(L) + "\n" + NOTAS_MANUALES


def _escribir(ruta: Path, nuevo: str) -> None:
    """Reemplaza el bloque automático y conserva lo que haya debajo de la marca final."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if ruta.exists() and FIN in _leer(ruta):
        manual = _leer(ruta).split(FIN, 1)[1]
        nuevo = nuevo.split(FIN, 1)[0] + FIN + manual
    ruta.write_text(nuevo, encoding="utf-8")


def generar(raiz: Path = RAIZ, hoy: str | None = None) -> list[Path]:
    hoy = hoy or dt.date.today().isoformat()
    _, niveles, desafios = sg.cargar()
    contenido = json.loads((AQUI.parent / "conceptos" / "conceptos.json").read_text(encoding="utf-8"))["desafios"]
    plan, _, _ = sg.asignar(niveles, desafios)
    orden = sg.prioridad(niveles, desafios, sg.cargar_valoracion())
    b = raiz / "boveda"
    escritos, filas = [], []
    for i, f in enumerate(orden, 1):
        id_ = f["id"]
        a = avance(id_, raiz)
        ruta = b / "Retos" / f"{id_}.md"
        _escribir(ruta, nodo_reto(id_, i, desafios[id_], contenido[id_], plan[id_], raiz, hoy))
        escritos.append(ruta)
        filas.append({"orden": i, "id": id_, "titulo": desafios[id_]["titulo"], "estado": a["estado"],
                      "hechos": a["hechos"], "total": a["total"], "pareja": " + ".join(plan[id_]),
                      "revisor": REVISOR[id_], "por_confirmar": a["por_confirmar"],
                      "palabras": a["palabras_postulacion"]})
    (b / "Tablero.md").write_text(tablero(filas, hoy), encoding="utf-8")
    _escribir(b / "00-HUB-Cajathon.md", hub(filas, hoy))
    return escritos + [b / "Tablero.md", b / "00-HUB-Cajathon.md"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.parse_args()
    for p in generar():
        print("Escrito", p.relative_to(RAIZ))


if __name__ == "__main__":
    main()
