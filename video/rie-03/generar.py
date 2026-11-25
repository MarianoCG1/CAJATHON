"""Genera el explicativo animado de RIE-03 (44 s, 1920x1080, 30 fps, sin narración) con identidad Yupana Labs.

Contenido tomado de `retos/RIE-03/presentacion/contenido.json` (nada nuevo: ninguna cifra que no esté en el deck).
Escenas: 1 gancho · 2 Rosa · 3 la cola · 4 el caso · 5 decide la persona · 6 evidencia · 7 cierre.

Uso (desde la raíz del repo):  python video/rie-03/generar.py
"""
import json
from pathlib import Path

BASE = Path(__file__).parent
C = json.loads((BASE.parents[1] / "retos" / "RIE-03" / "presentacion" / "contenido.json").read_text(encoding="utf-8"))

DURS = [5.5, 5.5, 8.0, 8.0, 5.0, 6.0, 6.0]
STARTS = [sum(DURS[:i]) for i in range(len(DURS))]
TOTAL = sum(DURS)

VARS = """
      :root { --tinta: #0E1A3A; --tinta2: #16264F; --maiz: #F4B63F; --turquesa: #1BB5A8; --terracota: #E4572E; --papel: #F7F3EA; --piedra: #5C6B7A; --niebla: #9FB3C8; --font-display: Outfit, Inter, sans-serif; }
      #root { position: absolute; inset: 0; overflow: hidden; font-family: Inter, sans-serif; }
"""
OSC = "#root { background: radial-gradient(1200px 760px at 50% 40%, #1A2C5E 0%, var(--tinta) 72%); color: #fff; }"
CLA = "#root { background: var(--papel); color: var(--tinta); }"
BANDA = ".banda { position: absolute; left: 0; top: 0; width: 1920px; height: 10px; background: linear-gradient(90deg, #F4B63F 0 38%, #1BB5A8 38% 70%, #0E1A3A 70%); }"


def escena(idx: int, nombre: str, css: str, html: str, js: str, claro=False) -> str:
    dur = DURS[idx]
    fondo = CLA if claro else OSC
    return f"""<template>
  <style>{VARS}      {fondo}
      {BANDA}
{css}  </style>
  <div id="root" data-composition-id="{nombre}" data-width="1920" data-height="1080">
    <div class="banda"></div>
    <div id="{nombre}-vel">{html}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{nombre}-vel", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, 0);
{js}
    tl.to("#{nombre}-vel", {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, {dur - 0.38});
    window.__timelines["{nombre}"] = tl;
  </script>
</template>
"""


def palabras(texto: str, pref: str, clase="w") -> str:
    return "".join(f'<span class="{clase}" id="{pref}{k}">{w}&nbsp;</span>' for k, w in enumerate(texto.split()))


def js_palabras(pref: str, n: int, t0: float, paso=0.1) -> str:
    return "\n".join(f'    tl.fromTo("#{pref}{k}", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }}, {t0 + k * paso:.2f});' for k in range(n))


ESC = []
for _txt, _n in (("En cada corte, una lista corta de clientes al día con riesgo.", 12), ("El caso: la evidencia, antes de actuar.", 7), ("Decide la persona. Nada se envía solo.", 7)):
    assert len(_txt.split()) == _n, _txt

# ---------------------------------------------------------------- 1 gancho
t1a, t1b = "Cuando llega el atraso,", "la oportunidad de ayudar ya pasó."
serie = [0.78, 0.8, 0.76, 0.74, 0.6, 0.5, 0.38, 0.3]
pts = " ".join(f"{120 + i * 160:.0f},{330 - v * 260:.0f}" for i, v in enumerate(serie))
html1 = f"""
    <div id="e1-t1">{palabras(t1a, "e1a")}</div><div id="e1-t2">{palabras(t1b, "e1b")}</div>
    <svg id="e1-graf" viewBox="0 0 1300 400" width="1300" height="400">
      <line x1="100" y1="340" x2="1240" y2="340" stroke="rgba(255,255,255,.25)" stroke-width="2"/>
      <polyline id="e1-linea" points="{pts}" fill="none" stroke="#F4B63F" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1400" stroke-dashoffset="1400"/>
      <circle id="e1-marca" cx="{120 + 7 * 160}" cy="{330 - serie[-1] * 260:.0f}" r="22" fill="#E4572E" opacity="0"/>
      <text id="e1-etq" x="{120 + 7 * 160 + 30}" y="{330 - serie[-1] * 260 + 74:.0f}" font-size="38" font-weight="700" fill="#E4572E" text-anchor="end" opacity="0">primer atraso</text>
      <text x="120" y="388" font-size="30" fill="#9FB3C8">Actividad del negocio, mes a mes (ilustrativo)</text>
    </svg>"""
css1 = """      #e1-t1, #e1-t2 { position: absolute; left: 120px; font-family: var(--font-display); font-weight: 700; letter-spacing: -0.02em; }
      #e1-t1 { top: 150px; font-size: 96px; color: #fff; } #e1-t2 { top: 270px; font-size: 96px; color: var(--maiz); }
      .w { display: inline-block; opacity: 0; } #e1-graf { position: absolute; left: 310px; top: 560px; }"""
js1 = js_palabras("e1a", len(t1a.split()), 0.5) + "\n" + js_palabras("e1b", len(t1b.split()), 1.5, 0.12) + """
    tl.to("#e1-linea", { strokeDashoffset: 0, duration: 2.2, ease: "power2.inOut" }, 1.6);
    tl.fromTo("#e1-marca", { opacity: 0, scale: 0, transformOrigin: "center" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 3.8);
    tl.fromTo("#e1-etq", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 4.1);"""
ESC.append(("e1", escena(0, "e1", css1, html1, js1)))

# ---------------------------------------------------------------- 2 Rosa
filas, cols = 5, 10
puntos = "".join(f'<div class="cli" id="e2c{r * cols + c}" style="left:{c * 78}px;top:{r * 78}px"></div>' for r in range(filas) for c in range(cols))
alertas = [3, 17, 36]
html2 = f"""
    <div id="e2-rol">ROSA · ASESORA DE NEGOCIOS · PERSONAJE FICTICIO</div>
    <div id="e2-t">{palabras("No puede revisar a todos sus clientes cada mes.", "e2w")}</div>
    <div id="e2-grid">{puntos}</div>"""
css2 = """      #e2-rol { position: absolute; left: 120px; top: 150px; font-size: 28px; letter-spacing: .18em; color: var(--maiz); font-weight: 700; opacity: 0; }
      #e2-t { position: absolute; left: 120px; top: 230px; width: 780px; font-family: var(--font-display); font-size: 84px; line-height: 1.08; font-weight: 700; letter-spacing: -0.02em; }
      .w { display: inline-block; opacity: 0; }
      #e2-grid { position: absolute; left: 1000px; top: 250px; width: 780px; height: 400px; }
      .cli { position: absolute; width: 56px; height: 56px; border-radius: 50%; background: rgba(244,182,63,.9); opacity: 0; }"""
js2 = 'tl.fromTo("#e2-rol", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 0.4);\n' + js_palabras("e2w", 9, 0.9, 0.12) + "\n" + "\n".join(
    f'    tl.fromTo("#e2c{k}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {1.0 + k * 0.025:.3f});' for k in range(filas * cols)) + "\n" + "\n".join(
    f'    tl.to("#e2c{k}", {{ backgroundColor: "#E4572E", scale: 1.25, duration: 0.4, ease: "power2.out" }}, {3.6 + i * 0.25:.2f});' for i, k in enumerate(alertas))
ESC.append(("e2", escena(1, "e2", css2, html2, js2)))

# ---------------------------------------------------------------- 3 la cola
p3 = C["pantallas"][0]
filas3 = ""
js3 = ""
for k, f in enumerate(p3["elementos"][:5]):
    nivel = f["nivel"]
    color = "#E4572E" if nivel > 0.66 else ("#D98E04" if nivel > 0.4 else "#1BB5A8")
    filas3 += (f'<div class="fila" id="e3f{k}"><b>{f["id"]}</b><div class="barra"><i id="e3b{k}" style="background:{color};width:{int(nivel * 100)}%"></i></div>'
               f'<div class="por"><span>{f["porque"][0]}</span><em>{f["porque"][1]}</em></div><div class="acc">{f["accion"]}</div></div>')
    js3 += (f'    tl.fromTo("#e3f{k}", {{ opacity: 0, y: 26 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {1.4 + k * 0.4:.2f});\n'
            f'    tl.fromTo("#e3b{k}", {{ scaleX: 0 }}, {{ scaleX: 1, transformOrigin: "left center", duration: 0.7, ease: "power3.out" }}, {1.7 + k * 0.4:.2f});\n')
html3 = f"""
    <div id="e3-t">{palabras("En cada corte, una lista corta de clientes al día con riesgo.", "e3w")}</div>
    <div id="e3-panel"><div id="e3-cab">Cola de clientes con riesgo de deterioro · todos al día hoy</div>{filas3}</div>
    <div id="e3-pie">Maqueta ilustrativa · datos ficticios</div>"""
css3 = """      #e3-t { position: absolute; left: 120px; top: 118px; width: 1680px; font-family: var(--font-display); font-size: 62px; font-weight: 700; letter-spacing: -0.02em; }
      .w { display: inline-block; opacity: 0; }
      #e3-panel { position: absolute; left: 120px; top: 250px; width: 1680px; background: #fff; border-radius: 22px; box-shadow: 0 24px 60px rgba(14,26,58,.14); padding: 26px 34px; }
      #e3-cab { font-size: 26px; font-weight: 700; color: #0F8F85; padding-bottom: 14px; border-bottom: 3px solid var(--maiz); margin-bottom: 8px; }
      .fila { display: grid; grid-template-columns: 220px 260px 1fr 470px; align-items: center; gap: 24px; height: 116px; border-bottom: 1px solid #E4DFD2; }
      .fila b { font-family: var(--font-display); font-size: 34px; } .barra { height: 18px; border-radius: 9px; background: #E4EBF1; overflow: hidden; } .barra i { display: block; height: 100%; border-radius: 9px; }
      .por span { display: block; font-size: 28px; font-weight: 600; } .por em { display: block; font-style: normal; font-size: 24px; color: var(--piedra); margin-top: 4px; }
      .acc { font-size: 28px; font-weight: 700; color: var(--tinta); }
      #e3-pie { position: absolute; left: 120px; top: 1000px; font-size: 22px; color: var(--piedra); }"""
js3 = js_palabras("e3w", 12, 0.4, 0.1) + "\n" + js3
ESC.append(("e3", escena(2, "e3", css3, html3, js3, claro=True)))

# ---------------------------------------------------------------- 4 el caso
ev = C["pantallas"][1]["elementos"]
g = ev["grafico"]
def poly(serie_, x0=60, y0=440, w=860, h=330):
    n = len(serie_)
    return " ".join(f"{x0 + i * w / (n - 1):.0f},{y0 - v * h:.0f}" for i, v in enumerate(serie_))
html4 = f"""
    <div id="e4-t">{palabras("El caso: la evidencia, antes de actuar.", "e4w")}</div>
    <div id="e4-sub">{ev["encabezado"]} · ficticio</div>
    <svg id="e4-graf" viewBox="0 0 1000 500" width="1000" height="500">
      <rect x="0" y="0" width="1000" height="500" rx="22" fill="rgba(255,255,255,.05)"/>
      <text x="40" y="52" font-size="30" font-weight="700" fill="#F4B63F">{g["titulo"]}</text>
      <polyline id="e4-ref" points="{poly(g["referencia"])}" fill="none" stroke="#9FB3C8" stroke-width="6" stroke-dasharray="14 12" stroke-dashoffset="0" opacity="0"/>
      <polyline id="e4-cli" points="{poly(g["serie"])}" fill="none" stroke="#E4572E" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1500" stroke-dashoffset="1500"/>
      <text x="40" y="482" font-size="26" fill="#9FB3C8">Roja: el cliente · Punteada: su sector (ilustrativo)</text>
    </svg>
    <ul id="e4-ev">{"".join(f'<li id="e4l{k}">{t}</li>' for k, t in enumerate(ev["evidencia"]))}</ul>
    <div id="e4-acc"><small>Acción propuesta</small><b>{ev["accion"]}</b></div>"""
css4 = """      #e4-t { position: absolute; left: 120px; top: 112px; font-family: var(--font-display); font-size: 62px; font-weight: 700; letter-spacing: -0.02em; }
      .w { display: inline-block; opacity: 0; }
      #e4-sub { position: absolute; left: 120px; top: 210px; font-size: 30px; color: var(--niebla); }
      #e4-graf { position: absolute; left: 120px; top: 290px; }
      #e4-ev { position: absolute; left: 1210px; top: 300px; width: 600px; list-style: none; }
      #e4-ev li { font-size: 34px; font-weight: 600; margin-bottom: 26px; padding-left: 38px; position: relative; opacity: 0; }
      #e4-ev li::before { content: ""; position: absolute; left: 0; top: 12px; width: 18px; height: 18px; border-radius: 50%; background: var(--maiz); }
      #e4-acc { position: absolute; left: 1210px; top: 700px; width: 600px; padding: 24px 30px; border-radius: 18px; background: rgba(27,181,168,.16); border: 3px solid var(--turquesa); opacity: 0; }
      #e4-acc small { display: block; font-size: 24px; letter-spacing: .14em; text-transform: uppercase; color: var(--turquesa); font-weight: 700; margin-bottom: 8px; }
      #e4-acc b { font-family: var(--font-display); font-size: 40px; }"""
js4 = js_palabras("e4w", 7, 0.4, 0.11) + """
    tl.fromTo("#e4-ref", { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power2.out" }, 1.2);
    tl.to("#e4-cli", { strokeDashoffset: 0, duration: 2.2, ease: "power2.inOut" }, 1.5);
""" + "\n".join(f'    tl.fromTo("#e4l{k}", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, {2.4 + k * 0.7:.2f});' for k in range(4)) + """
    tl.fromTo("#e4-acc", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 5.6);"""
ESC.append(("e4", escena(3, "e4", css4, html4, js4)))

# ---------------------------------------------------------------- 5 decide la persona
html5 = f"""
    <div id="e5-t">{palabras("Decide la persona. Nada se envía solo.", "e5w")}</div>
    <div id="e5-btns"><div class="btn ok" id="e5-ok">Aprobar</div><div class="btn" id="e5-ed">Editar</div><div class="btn" id="e5-de">Descartar</div></div>
    <div id="e5-log">Bitácora · decisión registrada con su motivo</div>
    <div id="e5-lim">La alerta no cambia calificación, límite ni tasa del cliente.</div>"""
css5 = """      #e5-t { position: absolute; left: 120px; top: 200px; font-family: var(--font-display); font-size: 96px; font-weight: 700; letter-spacing: -0.02em; }
      .w { display: inline-block; opacity: 0; }
      #e5-btns { position: absolute; left: 120px; top: 520px; display: flex; gap: 40px; }
      .btn { width: 380px; height: 120px; border-radius: 20px; border: 5px solid var(--tinta); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 44px; font-weight: 700; opacity: 0; background: #fff; }
      .btn.ok { background: #0F8F85; border-color: #0F8F85; color: #fff; }
      #e5-log { position: absolute; left: 120px; top: 720px; font-size: 38px; font-weight: 600; color: #0F8F85; opacity: 0; }
      #e5-lim { position: absolute; left: 120px; top: 800px; font-size: 32px; color: var(--piedra); opacity: 0; }"""
js5 = js_palabras("e5w", 7, 0.4, 0.12) + """
    tl.fromTo("#e5-ok", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 1.4);
    tl.fromTo("#e5-ed", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 1.55);
    tl.fromTo("#e5-de", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 1.7);
    tl.to("#e5-ok", { scale: 0.94, duration: 0.12, ease: "power2.in" }, 2.6);
    tl.to("#e5-ok", { scale: 1, duration: 0.3, ease: "back.out(2.5)" }, 2.72);
    tl.fromTo("#e5-log", { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 2.9);
    tl.fromTo("#e5-lim", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power2.out" }, 3.4);"""
ESC.append(("e5", escena(4, "e5", css5, html5, js5, claro=True)))

# ---------------------------------------------------------------- 6 evidencia
cif = C["evidencia"]["cifras"]
html6 = f"""
    <div id="e6-t">{palabras("Lo que medimos", "e6w")}</div>
    <div id="e6-cifras">{"".join(f'<div class="cif" id="e6c{k}"><b>{x["valor"]}</b><span>{x["etiqueta"]}</span></div>' for k, x in enumerate(cif))}</div>
    <div id="e6-nota">Medido solo sobre datos sintéticos propios, no sobre la cartera de la Caja. La precisión absoluta es baja (4,7 %) porque el evento es raro.</div>"""
css6 = """      #e6-t { position: absolute; left: 120px; top: 130px; font-family: var(--font-display); font-size: 70px; font-weight: 700; color: var(--maiz); letter-spacing: -0.02em; }
      .w { display: inline-block; opacity: 0; }
      #e6-cifras { position: absolute; left: 120px; top: 290px; width: 1680px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 36px; }
      .cif { border-radius: 24px; padding: 34px 36px; background: var(--tinta2); border: 1px solid rgba(255,255,255,.14); opacity: 0; }
      .cif b { display: block; font-family: var(--font-display); font-size: 150px; line-height: 1; color: var(--maiz); letter-spacing: -0.03em; }
      .cif span { display: block; margin-top: 16px; font-size: 32px; color: #CFE3F0; line-height: 1.3; }
      #e6-nota { position: absolute; left: 120px; top: 840px; width: 1500px; font-size: 32px; color: var(--niebla); line-height: 1.4; opacity: 0; }"""
js6 = js_palabras("e6w", 3, 0.4, 0.12) + "\n" + "\n".join(
    f'    tl.fromTo("#e6c{k}", {{ opacity: 0, y: 40, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.7, ease: "power3.out" }}, {1.0 + k * 0.6:.2f});' for k in range(3)) + """
    tl.fromTo("#e6-nota", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, 3.4);"""
ESC.append(("e6", escena(5, "e6", css6, html6, js6)))

# ---------------------------------------------------------------- 7 cierre
COLUMNAS = [1, 2, 3, 5]
SEP, R = 74, 25
W, H = SEP * 3 + 2 * R, SEP * 4 + 2 * R
celdas = ""
js7 = ""
for i, n in enumerate(COLUMNAS):
    for j in range(5):
        cx, cy = R + i * SEP, H - R - j * SEP
        celdas += f'<div class="an" style="left:{cx - R}px;top:{cy - R}px"></div>'
        if j < n:
            chispa = i == 3 and j == n - 1
            celdas += f'<div class="se{" ch" if chispa else ""}" id="e7s{i}{j}" style="left:{cx - R}px;top:{cy - R}px"></div>'
            js7 += f'    tl.fromTo("#e7s{i}{j}", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {0.5 + i * 0.18 + j * 0.06:.2f});\n'
html7 = f"""
    <div id="e7-marca" style="left:{960 - 560}px;top:{300}px;width:{W}px;height:{H}px">{celdas}</div>
    <div id="e7-nom"><div id="e7-y">yupana</div><div id="e7-l">LABS</div></div>
    <div id="e7-t">RIE-03 · Alerta temprana explicada</div>
    <div id="e7-pie">Maqueta ilustrativa · datos ficticios · cifras medidas sobre datos sintéticos propios · supuestos marcados</div>"""
css7 = f"""      #e7-marca {{ position: absolute; }}
      .an {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; border: 3px solid rgba(255,255,255,.22); }}
      .se {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; background: var(--maiz); opacity: 0; }} .se.ch {{ background: var(--turquesa); }}
      #e7-nom {{ position: absolute; left: {960 - 560 + W + 50}px; top: 322px; }}
      #e7-y {{ font-family: var(--font-display); font-size: 150px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; opacity: 0; }}
      #e7-l {{ font-family: var(--font-display); font-size: 48px; letter-spacing: .5em; color: var(--niebla); margin-top: 4px; opacity: 0; }}
      #e7-t {{ position: absolute; left: 0; width: 1920px; top: 720px; text-align: center; font-family: var(--font-display); font-size: 64px; font-weight: 700; color: var(--maiz); opacity: 0; }}
      #e7-pie {{ position: absolute; left: 0; width: 1920px; top: 960px; text-align: center; font-size: 26px; color: var(--niebla); opacity: 0; }}"""
js7 += """    tl.fromTo("#e7-y", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "power3.out" }, 1.3);
    tl.fromTo("#e7-l", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, 1.7);
    tl.fromTo("#e7-t", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.7, ease: "power3.out" }, 2.4);
    tl.fromTo("#e7-pie", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, 3.2);"""
esc7 = escena(6, "e7", css7, html7, js7)
# la última escena no se desvanece: se queda quieta hasta el final
esc7 = esc7.replace('    tl.to("#e7-vel", { opacity: 0, duration: 0.35, ease: "power2.in" }, %s);\n' % (DURS[6] - 0.38), "")
ESC.append(("e7", esc7))

# ---------------------------------------------------------------- ensamblado
(BASE / "compositions").mkdir(exist_ok=True)
hosts = ""
for k, (nombre, texto) in enumerate(ESC):
    (BASE / "compositions" / f"{nombre}.html").write_text(texto, encoding="utf-8")
    hosts += (f'      <div id="{nombre}" data-composition-id="{nombre}" data-composition-src="compositions/{nombre}.html" data-start="{STARTS[k]:g}" '
              f'data-duration="{DURS[k]:g}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>\n')
raiz = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0E1A3A; }}
      #root {{ position: relative; width: 1920px; height: 1080px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:g}" data-width="1920" data-height="1080">
{hosts}    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(BASE / "index.html").write_text(raiz, encoding="utf-8")
print(f"Generado: {len(ESC)} escenas, {TOTAL:g} s")
