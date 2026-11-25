"""Genera los activos de la identidad de Yupana Labs en `identidad/` (logos SVG, patrón, tokens y paleta).

La marca se inspira en la yupana, el tablero andino de cálculo: columnas de casillas que se llenan de
semillas (1, 2, 3, 5…). Es una inspiración visual; no afirmamos nada histórico sobre su uso.

Uso:
    python scripts/identidad/generar_identidad.py
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "identidad"

PALETA = {
    "tinta": "#0E1A3A",       # fondo oscuro y texto principal
    "tinta-2": "#16264F",     # superficies sobre fondo oscuro
    "maiz": "#F4B63F",        # acento principal (la semilla)
    "turquesa": "#1BB5A8",    # acento secundario (el dato verificable)
    "terracota": "#E4572E",   # alerta y énfasis puntual
    "papel": "#F7F3EA",       # fondo claro
    "piedra": "#5C6B7A",      # texto secundario
    "niebla": "#DCE3EA",      # líneas y bordes
}
TIPOGRAFIA = {"titulos": "Sora", "texto": "Inter", "respaldo": "'Segoe UI', Arial, sans-serif"}
COLUMNAS = [1, 2, 3, 5]  # semillas por columna: la yupana


def marca(fondo_claro: bool = False, solo_llenas: bool = False) -> tuple[str, int, int]:
    """Devuelve (contenido SVG, ancho, alto) de la marca: cuatro columnas de casillas, llenas de abajo hacia arriba."""
    sep_x, sep_y, r = 26, 22, 8.5
    ancho, alto = sep_x * (len(COLUMNAS) - 1) + 2 * r + 2, sep_y * 4 + 2 * r + 2
    vacio = PALETA["tinta"] if fondo_claro else "#FFFFFF"
    op_vacio = 0.16 if fondo_claro else 0.22
    partes = []
    for i, n in enumerate(COLUMNAS):
        cx = r + 1 + i * sep_x
        for j in range(5):
            cy = alto - r - 1 - j * sep_y
            if j < n:
                es_chispa = i == len(COLUMNAS) - 1 and j == n - 1
                color = PALETA["turquesa"] if es_chispa else PALETA["maiz"]
                partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')
            elif not solo_llenas:
                partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 1.2}" fill="none" stroke="{vacio}" stroke-opacity="{op_vacio}" stroke-width="1.6"/>')
    return "".join(partes), int(ancho), int(alto)


def svg_marca(fondo_claro: bool = False) -> str:
    cuerpo, w, h = marca(fondo_claro)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * 2}" height="{h * 2}" role="img" aria-label="Yupana Labs">{cuerpo}</svg>\n'


def svg_horizontal(fondo_claro: bool = False) -> str:
    cuerpo, w, h = marca(fondo_claro)
    texto = PALETA["tinta"] if fondo_claro else "#FFFFFF"
    sub = PALETA["piedra"] if fondo_claro else "#9FB3C8"
    total_w = w + 16 + 250
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {h}" width="{total_w * 2}" height="{h * 2}" role="img" aria-label="Yupana Labs">'
            f'{cuerpo}<g transform="translate({w + 16} 0)">'
            f'<text x="0" y="{h * 0.56:.0f}" font-family="Sora, \'Segoe UI\', Arial, sans-serif" font-size="46" font-weight="700" fill="{texto}" letter-spacing="-1">yupana</text>'
            f'<text x="0" y="{h * 0.9:.0f}" font-family="Sora, \'Segoe UI\', Arial, sans-serif" font-size="30" font-weight="400" fill="{sub}" letter-spacing="6">LABS</text></g></svg>\n')


def svg_patron() -> str:
    """Patrón de fondo: una yupana grande y tenue, para portadas y cierres."""
    partes = []
    for i, n in enumerate([1, 2, 3, 5, 3, 2, 1, 2, 3, 5]):
        for j in range(5):
            cx, cy = 40 + i * 120, 560 - j * 100
            if j < n:
                partes.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="{PALETA["maiz"]}" fill-opacity="0.07"/>')
            else:
                partes.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="#FFFFFF" stroke-opacity="0.05" stroke-width="3"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 620" width="1240" height="620" preserveAspectRatio="xMidYMid slice">{"".join(partes)}</svg>\n'


def tokens_css() -> str:
    lineas = [":root {"] + [f"  --yl-{k}: {v};" for k, v in PALETA.items()]
    lineas += [f"  --yl-fuente-titulos: {TIPOGRAFIA['titulos']}, {TIPOGRAFIA['respaldo']};",
               f"  --yl-fuente-texto: {TIPOGRAFIA['texto']}, {TIPOGRAFIA['respaldo']};",
               "  --yl-radio: 14px;", "}"]
    return "\n".join(lineas) + "\n"


def generar(salida: Path = SALIDA) -> list[Path]:
    salida.mkdir(parents=True, exist_ok=True)
    archivos = {
        "logo-marca.svg": svg_marca(False), "logo-marca-claro.svg": svg_marca(True),
        "logo-horizontal.svg": svg_horizontal(False), "logo-horizontal-claro.svg": svg_horizontal(True),
        "patron-yupana.svg": svg_patron(), "tokens.css": tokens_css(),
        "paleta.json": json.dumps({"colores": PALETA, "tipografia": TIPOGRAFIA}, ensure_ascii=False, indent=2) + "\n",
    }
    out = []
    for nombre, texto in archivos.items():
        (salida / nombre).write_text(texto, encoding="utf-8")
        out.append(salida / nombre)
    return out


if __name__ == "__main__":
    for p in generar():
        print("Escrito", p.relative_to(RAIZ))
