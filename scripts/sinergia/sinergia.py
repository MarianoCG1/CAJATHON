"""Sinergia por pareja y desafío — Cajathon 2026 (herramienta de planificación).

Mide cuán bien una pareja del equipo cubre las tareas que exige cada desafío
y propone un reparto rotativo de parejas. No es parte del producto del hackathon.

Uso:
    python scripts/sinergia/sinergia.py                 # imprime el informe
    python scripts/sinergia/sinergia.py --salida docs/investigacion/04-sinergia-retos-parejas.md

Modelo (todo ajustable; los pesos son supuestos nuestros):
  cobertura(P, d)  = sum(horas_i * max_nivel_P(habilidad_i)) / (5 * sum(horas_i))
  sinergia(P, d)   = cobertura(P, d) - max(cobertura(a, d), cobertura(b, d))
                     (lo que aporta la pareja por encima de su mejor integrante)
  puntaje(P, d)    = 100 * (W_COB * cobertura + W_SIN * min(1, sinergia / TOPE_SIN))
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent

W_COB = 0.6
W_SIN = 0.4
TOPE_SIN = 0.20
NIVEL_BRECHA = 3  # por debajo de este nivel (en ambos) la tarea es una brecha


def cargar(ruta_equipo: Path = AQUI / "team.json", ruta_desafios: Path = AQUI / "challenges.json"):
    equipo = json.loads(ruta_equipo.read_text(encoding="utf-8"))
    desafios = json.loads(ruta_desafios.read_text(encoding="utf-8"))
    niveles = {n: p["niveles"] for n, p in equipo["integrantes"].items()}
    for nombre, d in desafios["desafios"].items():
        for tarea, hab, horas in d["paquetes"]:
            if hab not in equipo["habilidades"]:
                raise ValueError(f"{nombre}: habilidad desconocida '{hab}' en '{tarea}'")
            if horas <= 0:
                raise ValueError(f"{nombre}: horas inválidas en '{tarea}'")
    return equipo, niveles, desafios["desafios"]


def cobertura(personas: tuple[str, ...], desafio: dict, niveles: dict) -> float:
    total = sum(h for _, _, h in desafio["paquetes"])
    ganado = sum(h * max(niveles[p].get(hab, 0) for p in personas) for _, hab, h in desafio["paquetes"])
    return ganado / (5 * total)


def sinergia(pareja: tuple[str, str], desafio: dict, niveles: dict) -> float:
    c_par = cobertura(pareja, desafio, niveles)
    mejor_solo = max(cobertura((p,), desafio, niveles) for p in pareja)
    return c_par - mejor_solo


def puntaje(pareja: tuple[str, str], desafio: dict, niveles: dict) -> float:
    c = cobertura(pareja, desafio, niveles)
    s = sinergia(pareja, desafio, niveles)
    return 100 * (W_COB * c + W_SIN * min(1.0, max(0.0, s) / TOPE_SIN))


def brechas(pareja: tuple[str, ...], desafio: dict, niveles: dict) -> list[tuple[str, str, int, int]]:
    """Tareas donde nadie de la pareja llega al nivel mínimo: (tarea, habilidad, mejor_nivel, horas)."""
    salida = []
    for tarea, hab, h in desafio["paquetes"]:
        mejor = max(niveles[p].get(hab, 0) for p in pareja)
        if mejor < NIVEL_BRECHA:
            salida.append((tarea, hab, mejor, h))
    return sorted(salida, key=lambda x: -x[3])


def carga_por_persona(pareja: tuple[str, str], desafio: dict, niveles: dict) -> dict[str, float]:
    """Cada tarea la toma quien tiene mayor nivel; en empate, quien lleve menos horas."""
    carga = {p: 0.0 for p in pareja}
    for _, hab, h in sorted(desafio["paquetes"], key=lambda t: -t[2]):
        a, b = pareja
        na, nb = niveles[a].get(hab, 0), niveles[b].get(hab, 0)
        if na > nb:
            elegido = a
        elif nb > na:
            elegido = b
        else:
            elegido = min(pareja, key=lambda p: carga[p])
        carga[elegido] += h
    return carga


def matriz(niveles: dict, desafios: dict) -> dict[str, dict[tuple[str, str], float]]:
    parejas = list(itertools.combinations(sorted(niveles), 2))
    return {d: {p: puntaje(p, desafios[d], niveles) for p in parejas} for d in desafios}


def asignar(niveles: dict, desafios: dict, max_uso_pareja: int = 2):
    """Búsqueda exacta: una pareja por desafío, carga equilibrada por persona y rotación forzada."""
    nombres = sorted(niveles)
    parejas = list(itertools.combinations(nombres, 2))
    ids = list(desafios)
    m = matriz(niveles, desafios)
    plazas = 2 * len(ids)
    piso, techo = plazas // len(nombres), math.ceil(plazas / len(nombres))
    mejor_por_desafio = [max(m[d].values()) for d in ids]
    resto = [sum(mejor_por_desafio[i:]) for i in range(len(ids) + 1)]
    mejor = {"total": -1.0, "plan": None}

    def dfs(i, plan, total, carga, uso):
        if total + resto[i] <= mejor["total"]:
            return
        if i == len(ids):
            if all(piso <= carga[n] <= techo for n in nombres):
                mejor["total"], mejor["plan"] = total, list(plan)
            return
        for par in sorted(parejas, key=lambda p: -m[ids[i]][p]):
            if uso[par] >= max_uso_pareja:
                continue
            if any(carga[x] + 1 > techo for x in par):
                continue
            for x in par:
                carga[x] += 1
            uso[par] += 1
            plan.append(par)
            dfs(i + 1, plan, total + m[ids[i]][par], carga, uso)
            plan.pop()
            uso[par] -= 1
            for x in par:
                carga[x] -= 1

    dfs(0, [], 0.0, Counter(), Counter())
    if mejor["plan"] is None:
        raise RuntimeError("No hay asignación que cumpla las restricciones")
    return dict(zip(ids, mejor["plan"])), mejor["total"], m


PESOS = {
    "base": {"cobertura": 0.20, "sinergia": 0.20, "esfuerzo": 0.15, "impacto": 0.20, "medibilidad": 0.15, "competencia": 0.10},
    "equipo": {"cobertura": 0.40, "sinergia": 0.40, "esfuerzo": 0.20},
    "negocio": {"impacto": 0.40, "medibilidad": 0.35, "competencia": 0.25},
}
INVERTIDOS = {"esfuerzo", "competencia"}  # menos es mejor


def cargar_valoracion(ruta: Path = AQUI / "valoracion.json") -> dict:
    return json.loads(ruta.read_text(encoding="utf-8"))["valoracion"]


def _normalizar(valores: dict[str, float], invertir: bool) -> dict[str, float]:
    lo, hi = min(valores.values()), max(valores.values())
    if hi == lo:
        return {k: 0.5 for k in valores}
    n = {k: (v - lo) / (hi - lo) for k, v in valores.items()}
    return {k: 1 - v for k, v in n.items()} if invertir else n


def prioridad(niveles: dict, desafios: dict, valoracion: dict) -> list[dict]:
    """Ordena los desafíos por rango promedio bajo tres juegos de pesos (menor = más prioritario)."""
    equipo = tuple(sorted(niveles))
    parejas = list(itertools.combinations(equipo, 2))
    crudo = {
        "cobertura": {d: cobertura(equipo, i, niveles) for d, i in desafios.items()},
        "sinergia": {d: max(puntaje(p, i, niveles) for p in parejas) for d, i in desafios.items()},
        "esfuerzo": {d: float(sum(h for _, _, h in i["paquetes"])) for d, i in desafios.items()},
        "impacto": {d: float(valoracion[d]["impacto"]) for d in desafios},
        "medibilidad": {d: float(valoracion[d]["medibilidad"]) for d in desafios},
        "competencia": {d: float(valoracion[d]["competencia"]) for d in desafios},
    }
    norm = {c: _normalizar(v, c in INVERTIDOS) for c, v in crudo.items()}
    puntajes = {
        nombre: {d: 100 * sum(w * norm[c][d] for c, w in pesos.items()) for d in desafios}
        for nombre, pesos in PESOS.items()
    }
    rangos = {}
    for nombre, pt in puntajes.items():
        orden = sorted(pt, key=lambda d: -pt[d])
        rangos[nombre] = {d: i + 1 for i, d in enumerate(orden)}
    filas = [{
        "id": d,
        "base": puntajes["base"][d],
        "rangos": {n: rangos[n][d] for n in PESOS},
        "rango_prom": sum(rangos[n][d] for n in PESOS) / len(PESOS),
    } for d in desafios]
    return sorted(filas, key=lambda f: (f["rango_prom"], -f["base"]))


def informe(niveles: dict, desafios: dict, max_uso_pareja: int = 2, valoracion: dict | None = None) -> str:
    plan, total, m = asignar(niveles, desafios, max_uso_pareja)
    nombres = sorted(niveles)
    parejas = list(itertools.combinations(nombres, 2))
    equipo_completo = tuple(nombres)
    L = []
    L.append("# Sinergia por pareja y desafío\n")
    L.append("Generado por `scripts/sinergia/sinergia.py`. Datos: `team.json` (niveles) y `challenges.json` (tareas por desafío).")
    L.append("**Advertencia:** los niveles de Glem, Antonio y David, y todas las horas por tarea, son **estimaciones** nuestras. Corregirlas y volver a ejecutar.\n")
    L.append(f"Fórmula: puntaje = 100 × ({W_COB} × cobertura + {W_SIN} × min(1, sinergia/{TOPE_SIN})). "
             "Cobertura = habilidad de la pareja (la mejor de los dos en cada tarea) ponderada por horas. "
             "Sinergia = cobertura de la pareja menos la de su mejor integrante solo.\n")

    L.append("## 1. Alcance de cada desafío\n")
    L.append("| Desafío | Título | Horas MVP | Equipo de 4 (cobertura) | Horas por persona (4) |")
    L.append("|---|---|---|---|---|")
    for d, info in desafios.items():
        h = sum(x[2] for x in info["paquetes"])
        L.append(f"| {d} | {info['titulo']} | {h} | {cobertura(equipo_completo, info, niveles):.0%} | {h / len(nombres):.1f} |")
    horas_totales = sum(sum(x[2] for x in i["paquetes"]) for i in desafios.values())
    L.append(f"\nSuma de los {len(desafios)} desafíos: **{horas_totales} h-persona** de MVP. "
             f"Con 4 personas son {horas_totales / 4:.0f} h cada una. "
             "Son horas de construcción: en el evento solo hay ~8 h por persona y solo si el equipo es finalista; "
             "para el concepto (hasta el miércoles) se necesita una fracción.\n")

    L.append("## 2. Matriz de puntaje (0–100) por pareja\n")
    L.append("| Desafío | " + " | ".join("+".join(p) for p in parejas) + " |")
    L.append("|---|" + "---|" * len(parejas))
    for d in desafios:
        mejor = max(m[d].values())
        fila = [f"**{m[d][p]:.0f}**" if m[d][p] == mejor else f"{m[d][p]:.0f}" for p in parejas]
        L.append(f"| {d} | " + " | ".join(fila) + " |")

    L.append("\n## 3. Mejor pareja por desafío, sinergia y brechas\n")
    for d, info in desafios.items():
        par = max(parejas, key=lambda p: m[d][p])
        gaps = brechas(par, info, niveles)
        L.append(f"- **{d}** {info['titulo']}: mejor pareja **{' + '.join(par)}** "
                 f"(puntaje {m[d][par]:.0f}, cobertura {cobertura(par, info, niveles):.0%}, "
                 f"sinergia +{sinergia(par, info, niveles):.0%}).")
        if gaps:
            L.append("  - Brechas: " + "; ".join(f"{t} ({h} h, nivel {n})" for t, _, n, h in gaps))

    L.append(f"\n## 4. Reparto rotativo óptimo (carga equilibrada, cada pareja ≤ {max_uso_pareja} veces)\n")
    L.append("| Desafío | Pareja | Puntaje | Brechas (horas sin cobertura) |")
    L.append("|---|---|---|---|")
    horas_persona = Counter()
    for d, par in plan.items():
        info = desafios[d]
        gaps = brechas(par, info, niveles)
        L.append(f"| {d} | {' + '.join(par)} | {m[d][par]:.0f} | {sum(g[3] for g in gaps)} h |")
        for p, h in carga_por_persona(par, info, niveles).items():
            horas_persona[p] += h
    L.append(f"\nPuntaje total: {total:.0f} (promedio {total / len(plan):.0f}).")
    L.append("\n| Persona | Desafíos | Horas MVP asignadas (si se construyeran todos) |")
    L.append("|---|---|---|")
    for n in nombres:
        cuantos = sum(n in par for par in plan.values())
        L.append(f"| {n} | {cuantos} | {horas_persona[n]:.0f} h |")

    if horas_persona:
        mayor = max(horas_persona, key=horas_persona.get)
        menor = min(nombres, key=lambda n: horas_persona[n])
        if horas_persona[mayor] > 1.5 * max(1.0, horas_persona[menor]):
            L.append(f"\n**Alerta de carga:** el reparto equilibra *cuántos* desafíos toca a cada uno, pero {mayor} acumularía "
                     f"{horas_persona[mayor]:.0f} h de MVP frente a {horas_persona[menor]:.0f} h de {menor}. "
                     "Construir los 8 no cabe; solo es viable redactar los conceptos y construir el que avance.")

    if valoracion:
        filas = prioridad(niveles, desafios, valoracion)
        L.append("\n## 5. Ranking de prioridad\n")
        L.append("Se calcula con tres juegos de pesos y se ordena por el **rango promedio**, para que el resultado no dependa de una sola ponderación. "
                 "Cada criterio se normaliza entre el mejor y el peor desafío (0–1). "
                 "Cobertura, sinergia y esfuerzo salen de los datos del equipo; impacto, medibilidad y competencia son **supuestos** de `valoracion.json`.\n")
        L.append("Pesos: " + "; ".join(
            f"**{n}** = " + ", ".join(f"{k} {v:.0%}" for k, v in w.items() if v) for n, w in PESOS.items()) + ".\n")
        L.append("| Orden | Desafío | Rango promedio | Puntaje base | Rango base | Rango equipo | Rango negocio | Pareja del reparto |")
        L.append("|---|---|---|---|---|---|---|---|")
        for i, f in enumerate(filas, 1):
            L.append(f"| {i} | {f['id']} {desafios[f['id']]['titulo']} | {f['rango_prom']:.1f} | {f['base']:.0f} | "
                     f"{f['rangos']['base']} | {f['rangos']['equipo']} | {f['rangos']['negocio']} | {' + '.join(plan[f['id']])} |")
        L.append("\n**Cómo usarlo:** escribir los conceptos en este orden. Los primeros reciben más tiempo y más revisión; "
                 "los últimos se completan después, con la pareja que indica el reparto. "
                 "Si la organización limita a un concepto por equipo, el primero de la lista es el candidato.\n")
    L.append("\nLo que **no** mide este modelo: calidad y volumen de los datos que entregue la Caja, KPI y línea base "
             "(no publicados), cuántos equipos eligen cada desafío, ni el riesgo de que un MVP no alcance 3/5 en funcionalidad crítica.")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--equipo", type=Path, default=AQUI / "team.json")
    ap.add_argument("--desafios", type=Path, default=AQUI / "challenges.json")
    ap.add_argument("--max-uso-pareja", type=int, default=2)
    ap.add_argument("--salida", type=Path, help="Guardar el informe en este archivo Markdown")
    a = ap.parse_args()
    _, niveles, desafios = cargar(a.equipo, a.desafios)
    texto = informe(niveles, desafios, a.max_uso_pareja, cargar_valoracion())
    if a.salida:
        a.salida.parent.mkdir(parents=True, exist_ok=True)
        a.salida.write_text(texto, encoding="utf-8")
        print(f"Informe guardado en {a.salida}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
