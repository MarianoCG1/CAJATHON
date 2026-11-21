# Cajathon 2026 — Yupana Labs

Espacio de trabajo del equipo para el **Cajathon 2026**, hackathon de IA de **Caja Trujillo**. Somos una consultora TI: cada desafío publicado es un encargo y hasta el **25.11** desarrollamos el **Concepto de solución** de los 8. Si llegamos a la final (03–04.12), construimos uno.

> Repositorio **privado**. Solo datos sintéticos. Los expedientes literales de la Caja **no se suben** (están en `.gitignore`).

## Empieza aquí

- **Persona:** abre [`retos/README.md`](retos/README.md), busca tu nombre en «Reparto por persona» y entra a la ficha de cada reto.
- **Agente de IA (Claude, GPT/Codex, Antigravity/Gemini):** pídele que lea [`AGENTS.md`](AGENTS.md) primero. Los archivos `CLAUDE.md` y `GEMINI.md` apuntan ahí.
- **Primera vez:** [`docs/prompts-inicio.md`](docs/prompts-inicio.md) trae cómo clonar y el prompt de arranque de cada integrante.
- **Seguimiento:** [`boveda/Tablero.md`](boveda/Tablero.md) (avance de cada reto, calculado solo).

## Estructura

| Ruta | Contenido |
|---|---|
| `AGENTS.md` · `CLAUDE.md` · `GEMINI.md` | Guía para agentes y contexto de fondo |
| `retos/<ID>/` | Un reto por carpeta: ficha, concepto, panorama, postulación, generador de datos |
| `docs/` | Investigación, plan, mensajes listos, preexistente, validación |
| `boveda/` | Bóveda Obsidian (abrir la carpeta raíz): competencia, decisiones, nodo por reto, tablero |
| `scripts/` | `sinergia/` (parejas y prioridad), `conceptos/` (borradores), `boveda/` (tablero) |
| `backend/` · `frontend/` | Esqueleto para el evento; sin funcionalidad crítica antes del 03.12 |

## Comandos

```powershell
pip install pytest pandas numpy
python -m pytest -q                         # todas las pruebas
python scripts/boveda/generar_boveda.py     # regenera el tablero
python retos/RIE-03/datos/generar.py        # datos sintéticos de un reto
```

## Calendario clave

- **21–25.11** — desarrollar y revisar los conceptos
- **25–26.11** — postulación del Concepto de solución en la plataforma (la web pública decía 24.11; confirmar hora límite)
- **30.11** — anuncio de finalistas
- **03–04.12** — hackathon presencial (entrega 04.12 a las 13:00)
