"""Arma `campos.md` y `resumen-corto.md` de un reto a partir de su texto de postulación y de sus textos cortos.

Entrada:
  retos/<ID>/postulacion.md           texto completo, 8 secciones «## 1. …» a «## 8. …»
  retos/<ID>/entrega/cortos.json      {"titulo": str, "resumen": str, "cortos": {"1": str, … "8": str}}

Salida (en retos/<ID>/entrega/):
  campos.md                  los 8 componentes de las bases, cada uno en versión corta (≤ LIMITE_CORTO) y completa, con conteo
  resumen-corto.md           título y resumen (≤ LIMITE_RESUMEN)
  ficha-1-pagina.md          ficha de una página (clave «ficha» del JSON; `ficha_pdf.py` la convierte en PDF)
  supuestos-sin-confirmar.md lo que se asumió por falta de respuesta del owner (clave «asumimos» del JSON)
  checklist-envio.md         pasos para cargar y verificar

Es una herramienta de planificación: no forma parte del producto. La versión completa se copia de
`postulacion.md` para que no haya dos textos que se desalineen.

Uso:
    python scripts/entrega/armar_paquete.py            # los 4 retos preparados
    python scripts/entrega/armar_paquete.py RIE-03     # uno
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
LIMITE_CORTO = 1000
LIMITE_RESUMEN = 500
RETOS = ["RIE-03", "NEG-02", "RIE-01", "RIE-02"]
COMPONENTES = {
    "1": "Problema abordado",
    "2": "Concepto de solución",
    "3": "Impacto esperado",
    "4": "Enfoque tecnológico",
    "5": "Tecnología preexistente",
    "6": "Funcionalidad crítica",
    "7": "Nivel de desarrollo esperado",
    "8": "Factibilidad y dependencias",
}


def secciones(texto: str) -> dict[str, str]:
    """Devuelve {'1': cuerpo, …} a partir de los encabezados «## N. …»."""
    partes = re.split(r"^## (\d)\. [^\n]*\n", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes) - 1, 2)}


def validar(id_: str, cortos: dict, completas: dict[str, str]) -> list[str]:
    errores = []
    for k in COMPONENTES:
        if k not in completas:
            errores.append(f"{id_}: falta la sección {k} en postulacion.md")
        c = cortos["cortos"].get(k, "")
        if not c:
            errores.append(f"{id_}: falta el texto corto {k}")
        elif len(c) > LIMITE_CORTO:
            errores.append(f"{id_}: el texto corto {k} tiene {len(c)} caracteres (máx. {LIMITE_CORTO})")
    if len(cortos["resumen"]) > LIMITE_RESUMEN:
        errores.append(f"{id_}: el resumen tiene {len(cortos['resumen'])} caracteres (máx. {LIMITE_RESUMEN})")
    return errores


def armar(id_: str, raiz: Path = RAIZ) -> list[Path]:
    base = raiz / "retos" / id_
    cortos = json.loads((base / "entrega" / "cortos.json").read_text(encoding="utf-8"))
    completas = secciones((base / "postulacion.md").read_text(encoding="utf-8"))
    errores = validar(id_, cortos, completas)
    if errores:
        raise ValueError("\n".join(errores))
    L = [f"# {id_} — campos para pegar en el formulario", "",
         f"**Título:** {cortos['titulo']}", "",
         "Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** "
         f"(≤ {LIMITE_CORTO} caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). "
         "Si el formulario pide un solo texto, usar `postulacion.md`.", ""]
    for k, nombre in COMPONENTES.items():
        L += [f"## {k}. {nombre}", "",
              f"**Versión corta** ({len(cortos['cortos'][k])} caracteres):", "", cortos["cortos"][k], "",
              f"**Versión completa** ({len(completas[k])} caracteres):", "", completas[k], ""]
    campos = base / "entrega" / "campos.md"
    campos.write_text("\n".join(L), encoding="utf-8")
    resumen = base / "entrega" / "resumen-corto.md"
    resumen.write_text(
        f"# {id_} — resumen corto\n\n**Título:** {cortos['titulo']}\n\n"
        f"**Resumen** ({len(cortos['resumen'])} de {LIMITE_RESUMEN} caracteres):\n\n{cortos['resumen']}\n",
        encoding="utf-8")
    salida = [campos, resumen]
    if "ficha" in cortos:
        (base / "entrega" / "ficha-1-pagina.md").write_text(ficha_md(id_, cortos), encoding="utf-8")
        salida.append(base / "entrega" / "ficha-1-pagina.md")
    if "asumimos" in cortos:
        (base / "entrega" / "supuestos-sin-confirmar.md").write_text(supuestos_md(id_, cortos), encoding="utf-8")
        salida.append(base / "entrega" / "supuestos-sin-confirmar.md")
    (base / "entrega" / "checklist-envio.md").write_text(checklist_md(id_), encoding="utf-8")
    salida.append(base / "entrega" / "checklist-envio.md")
    return salida


def ficha_md(id_: str, cortos: dict) -> str:
    f = cortos["ficha"]
    L = [f"# {cortos['titulo']}", "", "*Yupana Labs · Cajathon 2026 · Concepto de solución*", "",
         f"**Resumen.** {cortos['resumen']}", ""]
    for clave, titulo in (("problema", "Problema"), ("solucion", "Solución"), ("impacto", "Impacto esperado"),
                          ("tecnologia", "Tecnología"), ("preexistente", "Preexistente"),
                          ("critica", "Funcionalidad crítica (se construye en el evento)"), ("factibilidad", "Factibilidad")):
        L.append(f"- **{titulo}:** {f[clave]}")
    L += ["", "**Flujo:**", "", " → ".join(f["flujo"]), "", "```mermaid", "flowchart LR"]
    L += [f'  N{i}["{s}"]' for i, s in enumerate(f["flujo"])]
    L += [f"  N{i} --> N{i + 1}" for i in range(len(f["flujo"]) - 1)]
    L += ["```", ""]
    return "\n".join(L)


def supuestos_md(id_: str, cortos: dict) -> str:
    L = [f"# {id_} — supuestos que seguimos sin confirmar", "",
         "No hubo respuesta del owner para este desafío (el envío de tickets cerró el 24.11 a las 18:00 y no alcanzamos a enviar las "
         "preguntas de este reto). Mientras tanto el concepto trabaja con estos supuestos, marcados en el texto como **(supuesto)** o "
         "**[POR CONFIRMAR]**:", "", "| Tema | Qué asumimos |", "|---|---|"]
    L += [f"| {a['tema']} | {a['supuesto']} |" for a in cortos["asumimos"]]
    L += ["", "Si la organización responde o entrega datos, se actualiza el concepto; ninguna cifra de impacto se afirma sin línea base.", ""]
    return "\n".join(L)


def checklist_md(id_: str) -> str:
    return f"""# {id_} — checklist de envío

El formulario de «Concepto de solución» abre el mié 25.11 y cierra el jue 26.11 (hora límite por confirmar). **No enviar sin revisar este checklist.**

## Antes de abrir el formulario
- [ ] Leer `campos.md` y `resumen-corto.md`; confirmar que el reto y los números siguen vigentes.
- [ ] Revisar `supuestos-sin-confirmar.md`: ¿respondió el owner algo nuevo? Si sí, actualizar `postulacion.md` y volver a correr `python scripts/entrega/armar_paquete.py {id_}`.
- [ ] Tener a mano la ficha de una página (`ficha-1-pagina.pdf`) por si el formulario admite adjunto.

## En el formulario
- [ ] Elegir el desafío **{id_}**. Si el formulario solo admite un concepto, **el reto elegido debe ser RIE-03**.
- [ ] Pegar cada componente en su campo: versión completa si cabe; si no, la versión corta (≤ 1,000 caracteres).
- [ ] Si hay un solo cuadro de texto, pegar `postulacion.md` completo; si hay límite, usar los cortos en el mismo orden.
- [ ] Adjuntar la ficha PDF solo si el formulario lo permite.
- [ ] Declarar la tecnología preexistente tal como está en el componente 5 y en `docs/preexistente.md`.

## Antes de enviar
- [ ] No hay datos reales, nombres de personas, contactos de owners ni texto literal del expediente en lo que se pega.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR]; no hay cifras de impacto inventadas.
- [ ] Las cifras medidas dicen «sobre datos sintéticos propios».
- [ ] Guardar una captura o copia de lo enviado y anotar la hora.
"""


def main(argv: list[str]) -> int:
    ids = argv or RETOS
    for id_ in ids:
        for p in armar(id_):
            print("Escrito", p.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
