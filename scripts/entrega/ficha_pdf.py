"""Genera la ficha de una página (HTML y PDF) de un reto a partir de `retos/<ID>/entrega/cortos.json`.

El PDF se imprime con Chrome o Edge en modo headless (no requiere librerías extra). Falla si el PDF
pasa de una página. Herramienta de planificación: no forma parte del producto.

Uso:
    python scripts/entrega/ficha_pdf.py            # los 4 retos preparados
    python scripts/entrega/ficha_pdf.py RIE-03     # uno
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
RETOS = ["RIE-03", "NEG-02", "RIE-01", "RIE-02"]
NAVEGADORES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]
BLOQUES = [
    ("problema", "Problema"), ("solucion", "Solución"), ("impacto", "Impacto esperado"),
    ("tecnologia", "Tecnología"), ("preexistente", "Preexistente"),
    ("critica", "Funcionalidad crítica · se construye en el evento"), ("factibilidad", "Factibilidad"),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Sora:wght@600;700;800&display=swap');
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: Inter, 'Segoe UI', Arial, sans-serif; color: #0E1A3A; background: #F7F3EA; font-size: 10.2pt; line-height: 1.36; }
.hoja::before { content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 2.2mm; background: linear-gradient(90deg, #F4B63F 0 38%, #1BB5A8 38% 70%, #0E1A3A 70%); }
.hoja { position: relative; width: 210mm; height: 297mm; padding: 13mm 14mm 10mm; overflow: hidden; }
.marca svg { height: 7mm; width: auto; vertical-align: middle; margin-right: 2.5mm; }
.marca { color: #5C6B7A; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; font-weight: 600; }
h1 { font-family: Sora, 'Segoe UI', Arial, sans-serif; font-size: 16.5pt; line-height: 1.12; margin: 2mm 0 2.5mm; color: #0E1A3A; }
.resumen { background: #0E1A3A; color: #fff; border-left: 4px solid #F4B63F; padding: 2.4mm 3.4mm; margin-bottom: 3.6mm; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2.6mm 3.6mm; }
.bloque { background: #fff; border: 1px solid #DCE3EA; border-radius: 2.4mm; padding: 2.2mm 3mm; }
.bloque.ancho { grid-column: 1 / -1; }
.bloque h2 { font-size: 8pt; margin: 0 0 1mm; color: #0F8F85; text-transform: uppercase; letter-spacing: .08em; }
.flujo { margin-top: 3.6mm; }
.flujo h2 { font-size: 8pt; margin: 0 0 1.2mm; color: #0F8F85; text-transform: uppercase; letter-spacing: .08em; }
.pie { position: absolute; left: 14mm; right: 14mm; bottom: 8mm; font-size: 7.4pt; color: #627d98; border-top: 1px solid #d9e2ec; padding-top: 1.6mm; }
svg text { font-family: 'Segoe UI', Arial, sans-serif; }
"""


def _logo() -> str:
    s = (RAIZ / "identidad" / "logo-marca-claro.svg").read_text(encoding="utf-8")
    return re.sub(r'\swidth="\d+" height="\d+"', "", s).strip()


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def flujo_svg(pasos: list[str]) -> str:
    """Diagrama de flujo en dos filas, con flechas; el texto se parte en líneas de ≤ 22 caracteres."""
    n = len(pasos)
    por_fila = (n + 1) // 2
    ancho, alto, sep = 152, 44, 16
    w = por_fila * ancho + (por_fila - 1) * sep + 4
    h = 2 * alto + 26
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%">',
              '<defs><marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
              '<path d="M0,0 L8,4 L0,8 z" fill="#0F8F85"/></marker></defs>']
    pos = []
    for i, p in enumerate(pasos):
        fila, col = divmod(i, por_fila)
        if fila == 1:
            col = por_fila - 1 - col  # segunda fila de derecha a izquierda (serpiente)
        x, y = 2 + col * (ancho + sep), 2 + fila * (alto + 22)
        pos.append((x, y))
        palabras, lineas, actual = p.split(), [], ""
        for pal in palabras:
            if len(actual) + len(pal) + 1 > 22 and actual:
                lineas.append(actual)
                actual = pal
            else:
                actual = (actual + " " + pal).strip()
        lineas.append(actual)
        partes.append(f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" rx="6" fill="#ffffff" stroke="#0F8F85" stroke-width="1.2"/>')
        partes.append(f'<text x="{x + 8}" y="{y + 13}" font-size="8" fill="#0F8F85" font-weight="700">{i + 1}</text>')
        for j, l in enumerate(lineas[:3]):
            partes.append(f'<text x="{x + ancho / 2}" y="{y + 21 + j * 10.5}" font-size="9.2" fill="#0E1A3A" text-anchor="middle">{esc(l)}</text>')
    for i in range(n - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            if x2 > x1:
                partes.append(f'<line x1="{x1 + ancho}" y1="{y1 + alto / 2}" x2="{x2 - 1}" y2="{y2 + alto / 2}" stroke="#0F8F85" stroke-width="1.4" marker-end="url(#f)"/>')
            else:
                partes.append(f'<line x1="{x1}" y1="{y1 + alto / 2}" x2="{x2 + ancho + 1}" y2="{y2 + alto / 2}" stroke="#0F8F85" stroke-width="1.4" marker-end="url(#f)"/>')
        else:
            partes.append(f'<line x1="{x1 + ancho / 2}" y1="{y1 + alto}" x2="{x2 + ancho / 2}" y2="{y2 - 1}" stroke="#0F8F85" stroke-width="1.4" marker-end="url(#f)"/>')
    partes.append("</svg>")
    return "".join(partes)


def pagina_html(id_: str, c: dict) -> str:
    f = c["ficha"]
    bloques = []
    for clave, titulo in BLOQUES:
        ancho = " ancho" if clave in ("impacto", "critica", "factibilidad") else ""
        bloques.append(f'<div class="bloque{ancho}"><h2>{esc(titulo)}</h2>{esc(f[clave])}</div>')
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{esc(c["titulo"])}</title>'
            f"<style>{CSS}</style></head><body><div class=\"hoja\">"
            f'<div class="marca">{_logo()}Yupana Labs · Cajathon 2026 · Concepto de solución</div>'
            f'<h1>{esc(c["titulo"])}</h1><div class="resumen">{esc(c["resumen"])}</div>'
            f'<div class="grid">{"".join(bloques)}</div>'
            f'<div class="flujo"><h2>Flujo de la solución</h2>{flujo_svg(f["flujo"])}</div>'
            f'<div class="pie">Lo no oficial es supuesto del equipo y está marcado como tal. Cifras «medidas» = sobre datos sintéticos propios, '
            f'no de la Caja. Sin datos reales. El prototipo se construye durante la fase presencial.</div></div></body></html>')


def navegador() -> str:
    for ruta in NAVEGADORES:
        if Path(ruta).exists():
            return ruta
    for nombre in ("chrome", "msedge", "chromium"):
        r = shutil.which(nombre)
        if r:
            return r
    raise RuntimeError("No se encontró Chrome ni Edge para imprimir el PDF")


def paginas(pdf: Path) -> int:
    datos = pdf.read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", datos))


def generar(id_: str, raiz: Path = RAIZ) -> Path:
    base = raiz / "retos" / id_ / "entrega"
    c = json.loads((base / "cortos.json").read_text(encoding="utf-8"))
    ruta_html = base / "ficha-1-pagina.html"
    ruta_html.write_text(pagina_html(id_, c), encoding="utf-8")
    pdf = base / "ficha-1-pagina.pdf"
    with tempfile.TemporaryDirectory() as perfil:
        cmd = [navegador(), "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={perfil}",
               "--no-pdf-header-footer", f"--print-to-pdf={pdf}", ruta_html.resolve().as_uri()]
        subprocess.run(cmd, check=True, capture_output=True, timeout=120)
    n = paginas(pdf)
    if n != 1:
        raise ValueError(f"{id_}: la ficha tiene {n} páginas; debe ser 1")
    return pdf


def main(argv: list[str]) -> int:
    for id_ in argv or RETOS:
        print("Escrito", generar(id_).relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
