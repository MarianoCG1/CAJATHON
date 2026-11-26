"""Arma `formulario.md` (listo para pegar) y la carpeta `adjuntos/` de un reto, según el formulario real de la plataforma.

El formulario «Concept Solution» (abierto el 25.11, cierra el 26.11 a las 11:59 p. m., hora de Perú) tiene 6 pasos con límites
de caracteres. Los límites de abajo se leyeron de la propia página el 25.11 a las 21:00.

Entrada:  retos/<ID>/entrega/formulario.json
Salida:   retos/<ID>/entrega/formulario.md  y  retos/<ID>/entrega/adjuntos/ (PDF de presentación, ficha y diagrama PNG)

Uso:
    python scripts/entrega/armar_formulario.py RIE-03
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ficha_pdf import flujo_svg, navegador  # noqa: E402

MAX_NOMBRE = 80
MAX_ADJUNTOS, MAX_BYTES = 3, 10 * 1024 * 1024
# clave -> (paso, pregunta, máximo, obligatoria)
CAMPOS = [
    ("solution_description", 2, "¿En qué consiste su solución y cómo aborda la problemática del desafío?", 2000, True),
    ("solution_operation", 2, "¿Cómo funcionaría su solución?", 2000, True),
    ("solution_differentiation", 2, "¿Qué diferencia su solución de otras alternativas existentes?", 1000, True),
    ("expected_impact", 3, "¿Qué impacto generaría su solución y cómo contribuiría al resultado esperado del desafío?", 2000, True),
    ("technology_approach", 4, "¿Cuál será el enfoque tecnológico de su solución?", 2000, True),
    ("existing_description", 4, "Describan los desarrollos tecnológicos preexistentes indicados anteriormente (pregunta 4.3)", 2000, True),
    ("technical_risks", 4, "¿Identifican alguna limitación o riesgo técnico relevante para el desarrollo de su solución?", 800, False),
    ("prototype_build", 5, "¿Qué nuevos desarrollos o adaptaciones realizarán durante el hackathon?", 2000, True),
    ("prototype_demo", 5, "¿Qué resultado funcional esperan demostrar al finalizar el hackathon?", 1500, True),
    ("prototype_out_of_scope", 5, "¿Qué funcionalidades o capacidades quedarán fuera del alcance del prototipo?", 800, False),
]
PASOS = {1: "Identificación de la propuesta", 2: "Concepto de solución", 3: "Impacto esperado", 4: "Enfoque tecnológico",
         5: "Alcance del prototipo", 6: "Datos e insumos"}
PUNTO_PARTIDA = {"new": "Desarrollo desde cero", "existing": "Desarrollo a partir de soluciones o componentes preexistentes"}
DATOS = {"none": "No requerimos datos ni insumos", "desirable": "Requerimiento deseable de datos e insumos",
         "essential": "Requerimiento indispensable de datos e insumos"}


def largo(t: str) -> int:
    """Cuenta como lo hace un cuadro de texto del navegador (un salto de línea = 1 carácter)."""
    return len(t.replace("\r\n", "\n"))


def validar(f: dict) -> list[str]:
    err = []
    if largo(f["nombre"]) > MAX_NOMBRE:
        err.append(f"nombre: {largo(f['nombre'])} > {MAX_NOMBRE}")
    for clave, _, _, maximo, obligatoria in CAMPOS:
        t = f.get(clave, "")
        if obligatoria and not t:
            err.append(f"{clave}: obligatorio y vacío")
        if largo(t) > maximo:
            err.append(f"{clave}: {largo(t)} > {maximo}")
    if f["starting_point"] not in PUNTO_PARTIDA:
        err.append("starting_point inválido")
    if f["data_requirement"] not in DATOS:
        err.append("data_requirement inválido")
    if len(f["adjuntos"]) > MAX_ADJUNTOS:
        err.append("más de 3 adjuntos")
    return err


def markdown(id_: str, f: dict) -> str:
    L = [f"# {id_} — formulario «Concept Solution», listo para pegar", "",
         "**Fecha límite:** jueves 26 de noviembre, 11:59 p. m. (hora de Perú). **Se envía un solo desafío por equipo.**",
         "Cada bloque gris se copia entero en su campo. El conteo es de caracteres frente al máximo del formulario.", "",
         "## Paso 1 · Identificación de la propuesta", "",
         f"- **Desafío seleccionado:** pestaña {f['area']} → **{f['desafio']}**",
         f"- **Nombre de la solución** ({largo(f['nombre'])}/{MAX_NOMBRE}):", "", "```text", f["nombre"], "```", ""]
    paso = 1
    n = {}
    for clave, p, pregunta, maximo, obligatoria in CAMPOS:
        if p != paso:
            paso = p
            L += [f"## Paso {p} · {PASOS[p]}", ""]
        if p == 2 and clave == "solution_differentiation":
            pass
        if clave == "existing_description":
            L += [f"- **Punto de partida:** {PUNTO_PARTIDA[f['starting_point']]}", ""]
            for i, d in enumerate(f["existing_developments"], 1):
                L += [f"**Desarrollo preexistente {i}:** nombre «{d['name']}» · tipo: {d['type']} · nivel: {d['maturity']} · titularidad: {d['ownership']}", ""]
        n[p] = n.get(p, 0) + 1
        L += [f"**{pregunta}** {'(obligatoria)' if obligatoria else '(opcional)'} — {largo(f[clave])}/{maximo}", "", "```text", f[clave], "```", ""]
        if clave == "solution_differentiation":
            L += ["**Material visual complementario** (opcional, PDF/PNG/JPG, hasta 3 de 10 MB): subir los archivos de `adjuntos/`:", ""]
            L += [f"- `{a}`" for a in f["adjuntos"]] + [""]
            L += [f"**Enlace complementario** (opcional): {f['visual_link'] or 'dejar vacío'}", ""]
    L += [f"## Paso 6 · {PASOS[6]}", "", f"- **Tipo de requerimiento:** {DATOS[f['data_requirement']]}", "",
          "## Antes de enviar: tres declaraciones que marca la persona", "",
          "- [ ] La propuesta fue **revisada y acordada por los integrantes del equipo**, la información es veraz y cumple las bases. "
          "(Para marcarla, Glem, Antonio y David deben haberla visto.)",
          "- [ ] Identificamos las soluciones y componentes preexistentes, su titularidad y condiciones de uso.",
          "- [ ] Entendemos que, de ser seleccionados, haremos un desarrollo nuevo o adaptación sustantiva y demostraremos la funcionalidad crítica.", "",
          "**Guardar y salir** conserva un borrador; enviar es definitivo hasta donde indique la plataforma.", ""]
    return "\n".join(L)


def diagrama_png(id_: str, destino: Path) -> None:
    c = json.loads((RAIZ / "retos" / id_ / "entrega" / "cortos.json").read_text(encoding="utf-8"))
    logo = (RAIZ / "identidad" / "logo-horizontal-claro.svg").read_text(encoding="utf-8")
    pagina = ("<!doctype html><html><head><meta charset='utf-8'><style>"
              "body{margin:0;width:1400px;height:640px;background:#F7F3EA;font-family:'Segoe UI',Arial,sans-serif;color:#0E1A3A;position:relative;overflow:hidden}"
              "body::before{content:'';position:absolute;left:0;top:0;width:100%;height:10px;background:linear-gradient(90deg,#F4B63F 0 38%,#1BB5A8 38% 70%,#0E1A3A 70%)}"
              ".l{position:absolute;left:56px;top:42px}.l svg{height:66px;width:auto}h1{position:absolute;left:56px;top:132px;margin:0;font-size:34px}"
              ".f{position:absolute;left:56px;right:56px;top:230px}.p{position:absolute;left:56px;bottom:30px;font-size:17px;color:#5C6B7A}"
              f"</style></head><body><div class='l'>{logo}</div><h1>{id_} · Flujo de la solución</h1><div class='f'>{flujo_svg(c['ficha']['flujo'])}</div>"
              "<div class='p'>La decisión es siempre de una persona. Flujo propuesto; se construye durante la fase presencial.</div></body></html>")
    with tempfile.TemporaryDirectory() as tmp:
        h = Path(tmp) / "d.html"
        h.write_text(pagina, encoding="utf-8")
        subprocess.run([navegador(), "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={Path(tmp) / 'perfil'}",
                        "--window-size=1400,640", f"--screenshot={destino}", h.as_uri()], check=True, capture_output=True, timeout=120)


def armar(id_: str) -> list[Path]:
    base = RAIZ / "retos" / id_ / "entrega"
    f = json.loads((base / "formulario.json").read_text(encoding="utf-8"))
    err = validar(f)
    if err:
        raise ValueError(f"{id_}: " + "; ".join(err))
    (base / "formulario.md").write_text(markdown(id_, f), encoding="utf-8")
    adj = base / "adjuntos"
    adj.mkdir(exist_ok=True)
    fuentes = [RAIZ / "retos" / id_ / "presentacion" / "deck.pdf", base / "ficha-1-pagina.pdf"]
    for origen, nombre in zip(fuentes, f["adjuntos"]):
        shutil.copyfile(origen, adj / nombre)
    diagrama_png(id_, adj / f["adjuntos"][2])
    grandes = [p.name for p in adj.iterdir() if p.stat().st_size > MAX_BYTES]
    if grandes:
        raise ValueError(f"{id_}: adjuntos de más de 10 MB: {grandes}")
    return [base / "formulario.md"] + [adj / a for a in f["adjuntos"]]


def main(argv: list[str]) -> int:
    for id_ in argv or ["RIE-03"]:
        for p in armar(id_):
            print("Escrito", p.relative_to(RAIZ), p.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main(sys.argv[1:]))
