"""Genera video/marca/index.html (sting de marca de Yupana Labs, 8 s, 1920x1080, 30 fps).

La yupana se llena columna por columna (1, 2, 3, 5 semillas); la última es la chispa turquesa; la marca se
desplaza a la izquierda y aparece el nombre; cierra el lema. Colores y marca de `identidad/`.

Uso (desde la raíz del repo):  python video/marca/generar_index.py
"""
from pathlib import Path

COLUMNAS = [1, 2, 3, 5]
SEP, R = 128, 44          # separación entre casillas y radio de la semilla (px)
W = SEP * 3 + 2 * R
H = SEP * 4 + 2 * R
LEFT, TOP = 960 - W // 2, 540 - H // 2

celdas = []
for i, n in enumerate(COLUMNAS):
    for j in range(5):
        cx = R + i * SEP
        cy = H - R - j * SEP
        celdas.append(f'<div class="anillo" id="a-{i}-{j}" style="left:{cx - R}px;top:{cy - R}px"></div>')
        if j < n:
            chispa = i == len(COLUMNAS) - 1 and j == n - 1
            clase = "semilla chispa" if chispa else "semilla"
            celdas.append(f'<div class="{clase}" id="s-{i}-{j}" style="left:{cx - R}px;top:{cy - R}px"></div>')
chispa_cx, chispa_cy = R + 3 * SEP, H - R - 4 * SEP
celdas.append(f'<div class="onda" id="onda" style="left:{chispa_cx - R}px;top:{chispa_cy - R}px"></div>')

labs = "".join(f'<span class="lab" id="b{k}">{c}</span>' for k, c in enumerate("LABS"))
letras = "".join(f'<span class="letra" id="l{k}">{c}</span>' for k, c in enumerate("yupana"))

estilos = f"""
      :root {{
        --tinta: #0E1A3A;
        --maiz: #F4B63F;
        --turquesa: #1BB5A8;
        --niebla: #9FB3C8;
        --font-display: Outfit, Inter, sans-serif;
      }}
      #root {{ position: absolute; inset: 0; overflow: hidden; background:
        radial-gradient(1100px 700px at 50% 45%, #1A2C5E 0%, var(--tinta) 70%); font-family: var(--font-display); }}
      #marca {{ position: absolute; left: {LEFT}px; top: {TOP}px; width: {W}px; height: {H}px; }}
      .anillo {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; border: 4px solid rgba(255,255,255,.22); opacity: 0; }}
      .semilla {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; background: var(--maiz); opacity: 0; }}
      .semilla.chispa {{ background: var(--turquesa); }}
      .onda {{ position: absolute; width: {2 * R}px; height: {2 * R}px; border-radius: 50%; border: 5px solid var(--turquesa); opacity: 0; }}
      #nombre {{ position: absolute; left: 815px; top: 350px; }}
      #yupana {{ display: flex; font-size: 210px; font-weight: 700; letter-spacing: -0.04em; color: #fff; line-height: 1; }}
      .letra {{ display: inline-block; opacity: 0; }}
      #labs {{ display: flex; margin-top: 6px; font-size: 62px; font-weight: 400; color: var(--niebla); letter-spacing: 0.1em; }}
      .lab {{ display: inline-block; opacity: 0; }}
      #lema {{ position: absolute; left: 0; width: 1920px; top: 800px; text-align: center; font-family: Inter, sans-serif; font-size: 52px; font-weight: 500; color: #CFE3F0; opacity: 0; }}
      #lema b {{ color: var(--maiz); font-weight: 700; }}
"""
guion = f"""
      const COLUMNAS = {COLUMNAS};
      const tl = gsap.timeline({{ paused: true }});
      COLUMNAS.forEach((n, i) => {{
        for (let j = 0; j < 5; j++) {{
          tl.fromTo("#a-" + i + "-" + j, {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 0.1 + i * 0.07 + j * 0.03);
        }}
      }});
      COLUMNAS.forEach((n, i) => {{
        for (let j = 0; j < n; j++) {{
          tl.fromTo("#s-" + i + "-" + j, {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.42, ease: "back.out(1.6)" }}, 0.75 + i * 0.3 + j * 0.1);
        }}
      }});
      tl.fromTo("#onda", {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 3.2, duration: 0.8, ease: "power2.out" }}, 2.0);
      tl.fromTo("#marca", {{ x: 0, y: 0, scale: 1 }}, {{ x: -325, y: -70, scale: 0.55, duration: 0.9, ease: "power3.inOut" }}, 2.7);
      for (let k = 0; k < 6; k++) {{
        tl.fromTo("#l" + k, {{ opacity: 0, filter: "blur(10px)", y: 14 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: 0.5, ease: "power3.out" }}, 3.15 + k * 0.1);
      }}
      for (let k = 0; k < 4; k++) {{
        tl.fromTo("#b" + k, {{ opacity: 0, x: 0 }}, {{ opacity: 1, x: k * 30, duration: 0.9, ease: "power3.out" }}, 3.7 + k * 0.05);
      }}
      tl.fromTo("#lema", {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }}, 4.9);
      window.__timelines["sting"] = tl;
"""
escena = f"""<template>
  <style>{estilos}  </style>
  <div id="root" data-composition-id="sting" data-width="1920" data-height="1080">
    <div id="marca">{"".join(celdas)}</div>
    <div id="nombre"><div id="yupana">{letras}</div><div id="labs">{labs}</div></div>
    <div id="lema">Contar bien para <b>decidir mejor</b></div>
  </div>
  <script>{guion}  </script>
</template>
"""
raiz = """<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1920px; height: 1080px; overflow: hidden; background: #0E1A3A; }
      #root { position: relative; width: 1920px; height: 1080px; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="8" data-width="1920" data-height="1080">
      <div id="sting" data-composition-id="sting" data-composition-src="compositions/sting.html" data-start="0" data-duration="8" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = gsap.timeline({ paused: true });
    </script>
  </body>
</html>
"""
base = Path(__file__).parent
(base / "compositions").mkdir(exist_ok=True)
(base / "compositions" / "sting.html").write_text(escena, encoding="utf-8")
(base / "index.html").write_text(raiz, encoding="utf-8")
print("index.html y compositions/sting.html generados")
