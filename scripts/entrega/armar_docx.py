"""Genera la versión editable en Word (`retos/<ID>/entrega/concepto.docx`) del Concepto de solución.

Toma las 8 secciones de `postulacion.md` y el título de `entrega/cortos.json`, con la identidad de Yupana Labs.
Sirve para adjuntar o para pasar el contenido a la plantilla que pida la plataforma. Herramienta de planificación.

Uso:
    python scripts/entrega/armar_docx.py            # los 4 retos preparados
    python scripts/entrega/armar_docx.py RIE-03     # uno
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from armar_paquete import COMPONENTES, RETOS, secciones  # noqa: E402

TINTA = RGBColor(0x0E, 0x1A, 0x3A)
TEAL = RGBColor(0x0F, 0x8F, 0x85)
PIEDRA = RGBColor(0x5C, 0x6B, 0x7A)


def _estilo(doc: Document) -> None:
    n = doc.styles["Normal"]
    n.font.name, n.font.size, n.font.color.rgb = "Calibri", Pt(11), TINTA
    n.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    n.paragraph_format.space_after = Pt(6)
    n.paragraph_format.line_spacing = 1.15
    for nombre, tam, color in (("Title", 20, TINTA), ("Heading 1", 14, TEAL)):
        s = doc.styles[nombre]
        s.font.name, s.font.size, s.font.color.rgb, s.font.bold = "Calibri", Pt(tam), color, True
        rf = s.element.get_or_add_rPr().find(qn("w:rFonts"))
        if rf is not None:
            for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                rf.set(qn(a), "Calibri")


def _sombrear(celda, color_hex: str) -> None:
    tc_pr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tc_pr.append(shd)


def _franja(doc: Document) -> None:
    t = doc.add_table(rows=1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for celda, color in zip(t.rows[0].cells, ("F4B63F", "1BB5A8", "0E1A3A")):
        _sombrear(celda, color)
        p = celda.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(" ")
        r.font.size = Pt(2)


def generar(id_: str, raiz: Path = RAIZ) -> Path:
    base = raiz / "retos" / id_
    cortos = json.loads((base / "entrega" / "cortos.json").read_text(encoding="utf-8"))
    cuerpo = secciones((base / "postulacion.md").read_text(encoding="utf-8"))
    faltan = [k for k in COMPONENTES if k not in cuerpo]
    if faltan:
        raise ValueError(f"{id_}: faltan las secciones {faltan} en postulacion.md")
    doc = Document()
    _estilo(doc)
    s = doc.sections[0]
    s.page_height, s.page_width = Mm(297), Mm(210)
    s.top_margin = s.bottom_margin = Mm(20)
    s.left_margin = s.right_margin = Mm(22)
    _franja(doc)
    p = doc.add_paragraph()
    r = p.add_run("YUPANA LABS · CAJATHON 2026 · CONCEPTO DE SOLUCIÓN")
    r.font.size, r.font.bold, r.font.color.rgb = Pt(9), True, PIEDRA
    doc.add_paragraph(cortos["titulo"], style="Title")
    p = doc.add_paragraph()
    r = p.add_run(cortos["resumen"])
    r.italic = True
    for k, nombre in COMPONENTES.items():
        doc.add_heading(f"{k}. {nombre}", level=1)
        for parrafo in cuerpo[k].split("\n\n"):
            doc.add_paragraph(parrafo.replace("\n", " "))
    pie = doc.add_paragraph()
    r = pie.add_run("Lo no oficial está marcado como supuesto o por confirmar. Las cifras «medidas» son sobre datos sintéticos propios, no de la Caja. "
                    "Sin datos reales. La funcionalidad crítica se construye en la fase presencial.")
    r.font.size, r.font.color.rgb, r.italic = Pt(8.5), PIEDRA, True
    salida = base / "entrega" / "concepto.docx"
    doc.core_properties.author = "Yupana Labs"
    doc.core_properties.title = cortos["titulo"]
    doc.save(salida)
    return salida


def main(argv: list[str]) -> int:
    for id_ in argv or RETOS:
        print("Escrito", generar(id_).relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
