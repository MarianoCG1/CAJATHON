"""Arma el material de presentación de un reto a partir de `retos/<ID>/presentacion/contenido.json`.

Salidas (en retos/<ID>/presentacion/):
  storytelling.md        historia de la persona usuaria, antes y después, momento clave
  guion-demo.md          guion de demostración con tiempos
  preguntas-jurado.md    preguntas esperables y respuestas honestas
  deck.html / deck.pdf   láminas 16:9 con flujo, pantallas ilustrativas, evidencia y plan

Todo es ilustrativo: las pantallas son maquetas con datos ficticios, no un prototipo. La funcionalidad
crítica se construye en el evento. Herramienta de planificación: no forma parte del producto.

Uso:
    python scripts/presentacion/armar.py            # los 4 retos preparados
    python scripts/presentacion/armar.py RIE-03     # uno
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
TEAL, NAVY, GRIS, ROJO, AMBAR = "#0b6e6e", "#102a43", "#627d98", "#c0392b", "#d98e04"


def esc(t) -> str:
    return html.escape(str(t), quote=False)


# ---------------------------------------------------------------------------
# Pantallas ilustrativas (SVG). Cada una recibe la lista «elementos» del JSON.
# ---------------------------------------------------------------------------

def _marco(titulo: str, cuerpo: str, w=760, h=400) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(titulo)}">'
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="10" fill="#fff" stroke="#bcccdc" stroke-width="2"/>'
            f'<rect x="1" y="1" width="{w - 2}" height="34" rx="10" fill="{NAVY}"/><rect x="1" y="20" width="{w - 2}" height="15" fill="{NAVY}"/>'
            f'<circle cx="20" cy="18" r="4.5" fill="#f87171"/><circle cx="36" cy="18" r="4.5" fill="#fbbf24"/><circle cx="52" cy="18" r="4.5" fill="#34d399"/>'
            f'<text x="72" y="22" font-size="12" fill="#fff" font-weight="600">{esc(titulo)}</text>'
            f'<text x="{w - 14}" y="22" font-size="9.5" fill="#9fb3c8" text-anchor="end">MAQUETA ILUSTRATIVA · DATOS FICTICIOS</text>'
            f'{cuerpo}</svg>')


def _texto(x, y, t, size=11, color=NAVY, weight="400", anchor="start") -> str:
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{esc(t)}</text>'


def _boton(x, y, w, t, color=TEAL, claro=False) -> str:
    fondo, letra = ("#fff", color) if claro else (color, "#fff")
    return (f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="6" fill="{fondo}" stroke="{color}" stroke-width="1.4"/>'
            + _texto(x + w / 2, y + 17, t, 10.5, letra, "600", "middle"))


def pantalla_cola(p: dict) -> str:
    filas = p["elementos"]
    c = _texto(20, 62, p.get("subtitulo", ""), 11, GRIS)
    c += f'<rect x="20" y="72" width="720" height="26" fill="#eef6f6"/>'
    for x, t in ((30, "Elemento"), (170, "Prioridad"), (300, "Por qué (evidencia)"), (580, "Acción propuesta")):
        c += _texto(x, 89, t, 10.5, TEAL, "700")
    y = 100
    for f in filas[:6]:
        nivel = float(f.get("nivel", 0.5))
        color = ROJO if nivel > 0.66 else (AMBAR if nivel > 0.4 else TEAL)
        c += f'<line x1="20" y1="{y + 44}" x2="740" y2="{y + 44}" stroke="#e4ebf1"/>'
        c += _texto(30, y + 26, f["id"], 11, NAVY, "700")
        c += f'<rect x="170" y="{y + 15}" width="100" height="10" rx="5" fill="#e4ebf1"/><rect x="170" y="{y + 15}" width="{100 * nivel:.0f}" height="10" rx="5" fill="{color}"/>'
        c += _texto(300, y + 20, f["porque"][0], 10.5)
        if len(f["porque"]) > 1:
            c += _texto(300, y + 35, f["porque"][1], 10.5, GRIS)
        c += _texto(580, y + 26, f["accion"], 10.5, NAVY, "600")
        y += 46
    return _marco(p["titulo"], c)


def pantalla_caso(p: dict) -> str:
    e = p["elementos"]
    c = _texto(20, 62, e["encabezado"], 12.5, NAVY, "700") + _texto(20, 79, e.get("subencabezado", ""), 10.5, GRIS)
    # gráfico de líneas (serie normalizada 0..1)
    gx, gy, gw, gh = 20, 92, 380, 190
    c += f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="#f8fafc" stroke="#e4ebf1"/>'
    c += _texto(gx + 8, gy + 16, e["grafico"]["titulo"], 10.5, TEAL, "700")
    for serie, color, dash in ((e["grafico"]["referencia"], "#9fb3c8", "5 4"), (e["grafico"]["serie"], ROJO, "")):
        n = len(serie)
        pts = " ".join(f"{gx + 14 + i * (gw - 28) / (n - 1):.1f},{gy + gh - 18 - v * (gh - 50):.1f}" for i, v in enumerate(serie))
        c += f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2" stroke-dasharray="{dash}"/>'
    c += _texto(gx + 8, gy + gh - 4, e["grafico"]["leyenda"], 9.5, GRIS)
    # panel derecho
    px = 420
    c += f'<rect x="{px}" y="92" width="320" height="190" rx="6" fill="#fff" stroke="#e4ebf1"/>'
    c += _texto(px + 12, 110, "Por qué se alertó", 10.5, TEAL, "700")
    for i, t in enumerate(e["evidencia"][:4]):
        c += _texto(px + 12, 130 + i * 20, "• " + t, 10.5)
    c += _texto(px + 12, 218, e["incertidumbre"], 10, GRIS)
    c += f'<rect x="{px}" y="228" width="320" height="54" rx="6" fill="#eef6f6" stroke="{TEAL}"/>'
    c += _texto(px + 12, 246, "Acción propuesta", 10, TEAL, "700") + _texto(px + 12, 263, e["accion"], 10.5, NAVY, "600") + _texto(px + 12, 276, e.get("nota", ""), 9.5, GRIS)
    c += _boton(20, 300, 120, "Aprobar") + _boton(150, 300, 120, "Editar", NAVY, True) + _boton(280, 300, 120, "Descartar", GRIS, True)
    c += _texto(420, 318, e["pie"], 10, GRIS)
    c += _texto(20, 365, e["limite"], 10, GRIS)
    return _marco(p["titulo"], c)


def pantalla_mapa(p: dict) -> str:
    e = p["elementos"]
    c = _texto(20, 62, e["escenario"], 12, NAVY, "700")
    # zonas como bloques con intensidad
    c += f'<rect x="20" y="74" width="430" height="260" fill="#eaf2f8" stroke="#d0dde8"/>'
    for z in e["zonas"]:
        c += f'<rect x="{20 + z["x"]}" y="{74 + z["y"]}" width="{z["w"]}" height="{z["h"]}" rx="8" fill="{ROJO if z["nivel"] > 0.66 else (AMBAR if z["nivel"] > 0.4 else TEAL)}" fill-opacity="{0.25 + 0.5 * z["nivel"]:.2f}"/>'
        c += _texto(20 + z["x"] + 8, 74 + z["y"] + 18, z["nombre"], 10, NAVY, "700")
        for k in range(z.get("puntos", 6)):
            c += f'<circle cx="{20 + z["x"] + 12 + (k * 23) % (z["w"] - 24)}" cy="{74 + z["y"] + 34 + (k * 13) % max(1, z["h"] - 44)}" r="3" fill="{NAVY}"/>'
    c += _texto(20, 350, e["leyenda"], 9.5, GRIS)
    # panel derecho: tres cifras con rango
    c += _texto(470, 66, "Tres cifras, cada una con rango", 11, TEAL, "700")
    for i, k in enumerate(e["cifras"]):
        y = 78 + i * 62
        c += f'<rect x="470" y="{y}" width="270" height="54" rx="6" fill="#fff" stroke="#e4ebf1"/>'
        c += _texto(482, y + 20, k["nombre"], 10.5, GRIS) + _texto(482, y + 42, k["valor"], 15, NAVY, "700") + _texto(728, y + 42, k["rango"], 10, GRIS, "400", "end")
    c += f'<rect x="470" y="266" width="270" height="68" rx="6" fill="#eef6f6" stroke="{TEAL}"/>'
    c += _texto(482, 284, "Plan sugerido (propone el agente)", 10, TEAL, "700") + _texto(482, 301, e["plan"][0], 10.5, NAVY, "600") + _texto(482, 316, e["plan"][1], 10, GRIS)
    c += _boton(470, 345, 120, "Aprobar") + _boton(600, 345, 120, "Rechazar", GRIS, True)
    return _marco(p["titulo"], c)


def pantalla_grafo(p: dict) -> str:
    e = p["elementos"]
    c = _texto(20, 62, e["encabezado"], 12, NAVY, "700")
    pos = {n["id"]: (n["x"], n["y"]) for n in e["nodos"]}
    for a, b, riesgo in e["enlaces"]:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        c += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ROJO if riesgo else "#9fb3c8"}" stroke-width="{2.2 if riesgo else 1.4}"/>'
    forma = {"persona": TEAL, "telefono": AMBAR, "dispositivo": NAVY, "direccion": "#7b61ff", "negocio": "#2d9cdb"}
    for n in e["nodos"]:
        r = 11 if n["tipo"] == "persona" else 9
        c += f'<circle cx="{n["x"]}" cy="{n["y"]}" r="{r}" fill="{forma.get(n["tipo"], GRIS)}" stroke="#fff" stroke-width="2"/>'
        c += _texto(n["x"], n["y"] + 24, n["id"], 9, GRIS, "400", "middle")
    c += _texto(20, 358, "Persona · Teléfono · Dispositivo · Dirección · Negocio. En rojo, los vínculos que el modelo pondera por lo raros que son.", 9.5, GRIS)
    c += f'<rect x="470" y="74" width="270" height="250" rx="6" fill="#fff" stroke="#e4ebf1"/>'
    c += _texto(482, 94, "Expediente de la red", 10.5, TEAL, "700")
    for i, t in enumerate(e["expediente"][:6]):
        c += _texto(482, 116 + i * 21, "• " + t, 10)
    c += f'<rect x="470" y="262" width="270" height="52" rx="6" fill="#eef6f6" stroke="{TEAL}"/>'
    c += _texto(482, 280, "Contrapartida legítima", 10, TEAL, "700") + _texto(482, 296, e["legitima"][0], 10, NAVY) + _texto(482, 309, e["legitima"][1], 9.5, GRIS)
    c += _boton(470, 336, 86, "Escalar") + _boton(564, 336, 86, "Verificar", NAVY, True) + _boton(658, 336, 82, "Descartar", GRIS, True)
    return _marco(p["titulo"], c)


def pantalla_consentimiento(p: dict) -> str:
    e = p["elementos"]
    c = _texto(20, 62, e["encabezado"], 12, NAVY, "700")
    c += f'<rect x="20" y="74" width="350" height="26" fill="#eef6f6"/>'
    c += _texto(30, 91, "Entidad · alcance · vigencia", 10.5, TEAL, "700") + _texto(330, 91, "Activo", 10.5, TEAL, "700", "middle")
    y = 102
    for f in e["consentimientos"][:5]:
        c += f'<line x1="20" y1="{y + 40}" x2="370" y2="{y + 40}" stroke="#e4ebf1"/>'
        c += _texto(30, y + 17, f["entidad"], 11, NAVY, "700") + _texto(30, y + 33, f["alcance"] + " · " + f["vigencia"], 10, GRIS)
        on = f["activo"]
        c += f'<rect x="315" y="{y + 12}" width="30" height="16" rx="8" fill="{TEAL if on else "#cbd5e1"}"/><circle cx="{337 if on else 323}" cy="{y + 20}" r="6" fill="#fff"/>'
        y += 44
    c += _texto(20, 308, e["nota"], 10, GRIS)
    c += f'<rect x="392" y="74" width="348" height="150" rx="6" fill="#fff" stroke="#e4ebf1"/>'
    c += _texto(404, 94, "Oferta propuesta al ejecutivo", 10.5, TEAL, "700")
    for i, t in enumerate(e["oferta"][:5]):
        c += _texto(404, 116 + i * 20, ("" if i == 0 else "• ") + t, 10.5 if i else 11.5, NAVY, "700" if i == 0 else "400")
    c += f'<rect x="392" y="234" width="348" height="92" rx="6" fill="#fff7ed" stroke="{AMBAR}"/>'
    c += _texto(404, 252, "Bitácora de acceso (cada consulta queda registrada)", 10, AMBAR, "700")
    for i, t in enumerate(e["bitacora"][:3]):
        c += _texto(404, 272 + i * 17, t, 9.5, NAVY)
    c += _boton(392, 338, 100, "Aprobar") + _boton(500, 338, 100, "Editar", NAVY, True) + _boton(608, 338, 100, "Descartar", GRIS, True)
    return _marco(p["titulo"], c)


PANTALLAS = {"cola": pantalla_cola, "caso": pantalla_caso, "mapa": pantalla_mapa, "grafo": pantalla_grafo, "consentimiento": pantalla_consentimiento}


# ---------------------------------------------------------------------------
# Flujo (SVG) reutilizado para «solución en una imagen»
# ---------------------------------------------------------------------------

def flujo_svg(pasos: list[str]) -> str:
    n = len(pasos)
    por_fila = (n + 1) // 2
    ancho, alto, sep = 196, 58, 22
    w = por_fila * ancho + (por_fila - 1) * sep + 4
    h = 2 * alto + 40
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%">',
              f'<defs><marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{TEAL}"/></marker></defs>']
    pos = []
    for i, p in enumerate(pasos):
        fila, col = divmod(i, por_fila)
        if fila == 1:
            col = por_fila - 1 - col
        x, y = 2 + col * (ancho + sep), 2 + fila * (alto + 34)
        pos.append((x, y))
        palabras, lineas, actual = p.split(), [], ""
        for pal in palabras:
            if len(actual) + len(pal) + 1 > 26 and actual:
                lineas.append(actual)
                actual = pal
            else:
                actual = (actual + " " + pal).strip()
        lineas.append(actual)
        partes.append(f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" rx="8" fill="#fff" stroke="{TEAL}" stroke-width="1.6"/>')
        partes.append(f'<text x="{x + 10}" y="{y + 16}" font-size="11" fill="{TEAL}" font-weight="700">{i + 1}</text>')
        for j, l in enumerate(lineas[:3]):
            partes.append(f'<text x="{x + ancho / 2}" y="{y + 28 + j * 13}" font-size="12.5" fill="{NAVY}" text-anchor="middle">{esc(l)}</text>')
    for i in range(n - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if y1 == y2:
            if x2 > x1:
                partes.append(f'<line x1="{x1 + ancho}" y1="{y1 + alto / 2}" x2="{x2 - 1}" y2="{y2 + alto / 2}" stroke="{TEAL}" stroke-width="1.8" marker-end="url(#f)"/>')
            else:
                partes.append(f'<line x1="{x1}" y1="{y1 + alto / 2}" x2="{x2 + ancho + 1}" y2="{y2 + alto / 2}" stroke="{TEAL}" stroke-width="1.8" marker-end="url(#f)"/>')
        else:
            partes.append(f'<line x1="{x1 + ancho / 2}" y1="{y1 + alto}" x2="{x2 + ancho / 2}" y2="{y2 - 1}" stroke="{TEAL}" stroke-width="1.8" marker-end="url(#f)"/>')
    partes.append("</svg>")
    return "".join(partes)


# ---------------------------------------------------------------------------
# Deck HTML
# ---------------------------------------------------------------------------

CSS = f"""
@page {{ size: 1280px 720px; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: 'Segoe UI', Arial, sans-serif; color: #1f2933; background: #fff; }}
.lam {{ width: 1280px; height: 720px; padding: 46px 64px 40px; position: relative; overflow: hidden; page-break-after: always; break-after: page; }}
.lam:last-child {{ page-break-after: auto; break-after: auto; }}
.marca {{ position: absolute; top: 20px; left: 64px; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: {TEAL}; font-weight: 600; }}
.num {{ position: absolute; bottom: 18px; right: 64px; font-size: 12px; color: {GRIS}; }}
.pie {{ position: absolute; bottom: 18px; left: 64px; font-size: 11px; color: {GRIS}; }}
h1 {{ font-size: 44px; line-height: 1.1; margin: 0 0 14px; color: {NAVY}; }}
h2 {{ font-size: 32px; line-height: 1.15; margin: 14px 0 18px; color: {NAVY}; }}
h3 {{ font-size: 15px; margin: 0 0 8px; color: {TEAL}; text-transform: uppercase; letter-spacing: .08em; }}
p, li {{ font-size: 19px; line-height: 1.42; }}
ul {{ margin: 0; padding-left: 22px; }}
.portada {{ background: linear-gradient(135deg, {NAVY} 0%, #0b4f5c 100%); color: #fff; }}
.portada h1 {{ color: #fff; font-size: 52px; max-width: 980px; margin-top: 150px; }}
.portada .lema {{ font-size: 24px; color: #bfe3e3; max-width: 900px; }}
.portada .marca, .portada .pie, .portada .num {{ color: #9ed3d3; }}
.dos {{ display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }}
.caja {{ border: 1px solid #d9e2ec; border-radius: 12px; padding: 18px 22px; }}
.caja.antes {{ background: #fff5f5; border-color: #f5c6c6; }}
.caja.despues {{ background: #eef6f6; border-color: #b9dcdc; }}
.cifras {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 10px 0 18px; }}
.cifra {{ border: 1px solid #d9e2ec; border-radius: 12px; padding: 16px 20px; }}
.cifra b {{ display: block; font-size: 40px; color: {TEAL}; line-height: 1.05; }}
.cifra span {{ font-size: 15px; color: {GRIS}; }}
table {{ border-collapse: collapse; width: 100%; font-size: 17px; }}
th {{ text-align: left; color: {TEAL}; font-size: 13px; text-transform: uppercase; letter-spacing: .08em; padding: 6px 10px; border-bottom: 2px solid #d9e2ec; }}
td {{ padding: 8px 10px; border-bottom: 1px solid #e4ebf1; vertical-align: top; }}
.nota {{ font-size: 14px; color: {GRIS}; margin-top: 10px; }}
.paso {{ display: grid; grid-template-columns: 44px 1fr; gap: 14px; margin-bottom: 11px; align-items: start; }}
.paso .n {{ width: 44px; height: 44px; border-radius: 50%; background: {TEAL}; color: #fff; font-weight: 700; font-size: 20px; display: flex; align-items: center; justify-content: center; }}
.paso b {{ font-size: 18px; color: {NAVY}; }} .paso span {{ font-size: 16px; color: #3e4c59; display: block; }}
"""


def lamina(num: int, cuerpo: str, clase="", pie="") -> str:
    return (f'<section class="lam {clase}"><div class="marca">Yupana Labs · Cajathon 2026 · Concepto de solución</div>{cuerpo}'
            f'<div class="pie">{esc(pie)}</div><div class="num">{num}</div></section>')


def deck_html(id_: str, c: dict) -> str:
    pie = "Ilustrativo: pantallas y datos ficticios; lo no oficial es supuesto del equipo; cifras «medidas» = sobre datos sintéticos propios."
    L = []
    n = 1
    L.append(lamina(n, f'<h1>{esc(c["titulo"])}</h1><p class="lema">{esc(c["lema"])}</p>', "portada", pie)); n += 1
    L.append(lamina(n, f'<h3>El problema</h3><h2>{esc(c["problema"]["titular"])}</h2><ul>' + "".join(f"<li>{esc(x)}</li>" for x in c["problema"]["puntos"]) + "</ul>"
                    + f'<p class="nota">{esc(c["problema"].get("nota", ""))}</p>', "", pie)); n += 1
    h = c["historia"]
    L.append(lamina(n, f'<h3>La historia de {esc(c["persona"]["nombre"])} (personaje ficticio)</h3><h2>{esc(c["persona"]["rol"])}: un día antes y un día después</h2>'
                    f'<div class="dos"><div class="caja antes"><h3>Antes</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in h["antes"]) + '</ul></div>'
                    f'<div class="caja despues"><h3>Después</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in h["despues"]) + '</ul></div></div>'
                    f'<p class="nota">Momento clave: {esc(h["momento_clave"])}</p>', "", pie)); n += 1
    L.append(lamina(n, f'<h3>La solución en una imagen</h3><h2>{esc(c["solucion"]["titular"])}</h2>' + flujo_svg(c["solucion"]["flujo"])
                    + f'<p class="nota">{esc(c["solucion"]["nota"])}</p>', "", pie)); n += 1
    pasos = "".join(f'<div class="paso"><div class="n">{i + 1}</div><div><b>{esc(p["paso"])}</b><span>{esc(p["detalle"])}</span></div></div>' for i, p in enumerate(c["como_funciona"]))
    L.append(lamina(n, f'<h3>Cómo funciona</h3><h2>Paso a paso, de los datos a la decisión humana</h2>{pasos}', "", pie)); n += 1
    for pant in c["pantallas"]:
        L.append(lamina(n, f'<h3>Así lo vería la persona usuaria</h3><h2>{esc(pant["titular"])}</h2><div style="width:900px;margin:0 auto">{PANTALLAS[pant["tipo"]](pant)}</div>'
                        f'<p class="nota" style="text-align:center">{esc(pant.get("nota", ""))}</p>', "", pie)); n += 1
    ev = "".join(f'<div class="cifra"><b>{esc(e["valor"])}</b><span>{esc(e["etiqueta"])}</span></div>' for e in c["evidencia"]["cifras"])
    kp = "".join(f"<li>{esc(x)}</li>" for x in c["impacto"]["kpi"])
    L.append(lamina(n, f'<h3>Impacto y evidencia</h3><h2>{esc(c["impacto"]["titular"])}</h2><div class="cifras">{ev}</div>'
                    f'<div class="dos"><div><h3>KPI propuestos (a validar con el owner)</h3><ul>{kp}</ul></div>'
                    f'<div><h3>Qué sí y qué no afirmamos</h3><p>{esc(c["evidencia"]["honestidad"])}</p></div></div>', "", pie)); n += 1
    filas = "".join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>' for a, b in c["tecnologia"]["filas"])
    L.append(lamina(n, f'<h3>Tecnología y preexistente</h3><h2>{esc(c["tecnologia"]["titular"])}</h2><table><tr><th>Capa</th><th>Qué hace y por qué aporta</th></tr>{filas}</table>'
                    f'<p class="nota">{esc(c["tecnologia"]["preexistente"])}</p>', "", pie)); n += 1
    filas = "".join(f'<tr><td>{esc(b["bloque"])}</td><td>{esc(b["horas"])}</td><td>{esc(b["entregable"])}</td></tr>' for b in c["plan"]["bloques"])
    L.append(lamina(n, f'<h3>Factibilidad</h3><h2>{esc(c["plan"]["titular"])}</h2><table><tr><th>Bloque del evento</th><th>Horas (supuesto)</th><th>Entregable</th></tr>{filas}</table>'
                    f'<p class="nota">{esc(c["plan"]["nota"])}</p>', "", pie)); n += 1
    L.append(lamina(n, f'<h3>Supuestos y próximos pasos</h3><h2>Lo que aún no sabemos y cómo lo cerramos</h2><div class="dos"><div><h3>Supuestos</h3><ul>'
                    + "".join(f"<li>{esc(x)}</li>" for x in c["supuestos"]) + '</ul></div><div><h3>Próximos pasos</h3><ul>'
                    + "".join(f"<li>{esc(x)}</li>" for x in c["proximos_pasos"]) + "</ul></div></div>", "", pie))
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{esc(c["titulo"])}</title><style>{CSS}</style></head><body>{"".join(L)}</body></html>'


# ---------------------------------------------------------------------------
# Documentos de texto
# ---------------------------------------------------------------------------

def storytelling_md(id_: str, c: dict) -> str:
    p, h = c["persona"], c["historia"]
    L = [f"# {id_} — storytelling", "", f"> {c['lema']}", "",
         "*Personaje ficticio, creado para explicar la solución. No es una persona real ni un caso de la Caja.*", "",
         f"## Quién es {p['nombre']}", "", p["contexto"], "", "## Antes: un día sin la solución", ""]
    L += [f"- {x}" for x in h["antes"]]
    L += ["", "## El momento clave", "", h["momento_clave"], "", "## Después: un día con la solución", ""]
    L += [f"- {x}" for x in h["despues"]]
    L += ["", "## La historia en tres frases (para decir en voz alta)", ""]
    L += [f"{i + 1}. {x}" for i, x in enumerate(c["tres_frases"])]
    L += ["", "## Cómo funciona, sin tecnicismos", ""]
    L += [f"{i + 1}. **{x['paso']}.** {x['detalle']}" for i, x in enumerate(c["como_funciona"])]
    L += ["", "## Lo que no prometemos", ""] + [f"- {x}" for x in c["no_prometemos"]] + [""]
    return "\n".join(L)


def guion_md(id_: str, c: dict) -> str:
    total = sum(float(x["min"]) for x in c["demo"])
    L = [f"# {id_} — guion de demostración ({total:g} minutos)", "",
         "Guion para la fase presencial, con el prototipo construido en el evento. Hoy es solo un guion: no hay prototipo.", "",
         "| Minuto | Qué se muestra | Qué se dice |", "|---|---|---|"]
    t = 0.0
    for x in c["demo"]:
        L.append(f"| {t:g}–{t + float(x['min']):g} | {x['accion']} | {x['mensaje']} |")
        t += float(x["min"])
    L += ["", "## Si algo falla en vivo", ""] + [f"- {x}" for x in c["plan_b"]] + [""]
    return "\n".join(L)


def preguntas_md(id_: str, c: dict) -> str:
    L = [f"# {id_} — preguntas esperables del jurado y respuestas honestas", "",
         "Las respuestas separan lo que está medido sobre datos sintéticos propios, lo que es supuesto y lo que depende de la Caja.", ""]
    for i, q in enumerate(c["preguntas"], 1):
        L += [f"## {i}. {q['p']}", "", q["r"], ""]
    return "\n".join(L)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def navegador() -> str:
    for ruta in NAVEGADORES:
        if Path(ruta).exists():
            return ruta
    for nombre in ("chrome", "msedge", "chromium"):
        r = shutil.which(nombre)
        if r:
            return r
    raise RuntimeError("No se encontró Chrome ni Edge")


def paginas(pdf: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf.read_bytes()))


def validar(c: dict) -> list[str]:
    err = []
    for k in ("titulo", "lema", "persona", "historia", "problema", "solucion", "como_funciona", "pantallas", "evidencia", "impacto", "tecnologia", "plan",
              "supuestos", "proximos_pasos", "demo", "plan_b", "preguntas", "tres_frases", "no_prometemos"):
        if k not in c:
            err.append(f"falta «{k}»")
    return err


def armar(id_: str, raiz: Path = RAIZ, pdf: bool = True) -> list[Path]:
    base = raiz / "retos" / id_ / "presentacion"
    c = json.loads((base / "contenido.json").read_text(encoding="utf-8"))
    err = validar(c)
    if err:
        raise ValueError(f"{id_}: " + "; ".join(err))
    salida = []
    for nombre, texto in (("storytelling.md", storytelling_md(id_, c)), ("guion-demo.md", guion_md(id_, c)),
                          ("preguntas-jurado.md", preguntas_md(id_, c)), ("deck.html", deck_html(id_, c))):
        (base / nombre).write_text(texto, encoding="utf-8")
        salida.append(base / nombre)
    if pdf:
        ruta_pdf = base / "deck.pdf"
        with tempfile.TemporaryDirectory() as perfil:
            cmd = [navegador(), "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={perfil}", "--no-pdf-header-footer",
                   f"--print-to-pdf={ruta_pdf}", (base / "deck.html").resolve().as_uri()]
            subprocess.run(cmd, check=True, capture_output=True, timeout=180)
        esperadas = 9 + len(c["pantallas"])  # portada, problema, historia, imagen, pasos, pantallas, impacto, tecnología, plan, supuestos
        n = paginas(ruta_pdf)
        if n != esperadas:
            raise ValueError(f"{id_}: el deck tiene {n} páginas; se esperaban {esperadas}")
        salida.append(ruta_pdf)
    return salida


def main(argv: list[str]) -> int:
    for id_ in argv or RETOS:
        for p in armar(id_):
            print("Escrito", p.relative_to(RAIZ))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
