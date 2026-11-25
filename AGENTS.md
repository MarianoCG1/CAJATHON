# AGENTS.md — Guía para agentes (Claude, GPT/Codex, Antigravity/Gemini, otros)

Este repositorio es el espacio de trabajo del equipo **Yupana Labs** para el **Cajathon 2026** (hackathon de IA de Caja Trujillo). Si eres un agente de IA: **lee este archivo completo antes de tocar nada**. Está escrito para que sepas dónde estás, quién es la persona con la que hablas y qué toca hacer.

> Claude Code lee `CLAUDE.md`, Codex/GPT y otros leen `AGENTS.md`, Antigravity/Gemini lee `GEMINI.md`. Los tres apuntan aquí. Todo el trabajo y los documentos van **en español**.

## 1. El escenario

Somos **una consultora TI** que resuelve problemas con tecnología. La Caja publicó **8 desafíos** (los «encargos»). Hasta el **25.11** (la plataforma abre ese día) nuestro trabajo es **desarrollar la idea de cada encargo** y dejar listo el **Concepto de solución** que la plataforma pide. Eso es lo único que se entrega ahora.

- No se construye ningún prototipo todavía. Si el equipo pasa a los 12 finalistas, se elige **un** desafío y se construye en el evento presencial (03–04.12), con historial git como evidencia.
- La organización confirmó que se puede elegir cualquier desafío. Falta confirmar si se aceptan **varios conceptos por equipo**; si solo aceptan uno, se postula **RIE-03**.
- El concepto se evalúa con: Alineación 25 % · Impacto 30 % · Viabilidad técnica 25 % · Factibilidad de construcción 20 %. Un concepto sólido vale más que ocho flojos.

## 2. Primer paso: ¿con quién hablas?

Pregunta a la persona quién es y abre `retos/README.md`, sección «Reparto por persona»:

| Persona | Perfil | Lidera (pareja) | Revisa |
|---|---|---|---|
| **Mariano** (coordinador, developer) | Backend, agentes de IA, ML | RIE-03, NEG-02, RIE-01, RIE-02 | COM-02 |
| **Glem** (analista de datos) | ML, ETL, FastAPI, React | NEG-01, NEG-03, COM-01, COM-02 | RIE-03, RIE-01 |
| **Antonio** (economista) | Sector financiero, KPI, Power BI | NEG-01, NEG-02, RIE-01, COM-01 | RIE-02, NEG-03 |
| **David** (ing. industrial, UX/UI) | Usuarios, flujos, prototipado | RIE-03, RIE-02, NEG-03, COM-02 | NEG-01, NEG-02, COM-01 |

Luego abre la ficha `retos/<ID>/README.md` de cada reto de esa persona: trae el estado y las casillas de lo que falta.

## 3. Mapa del repositorio

```
AGENTS.md  CLAUDE.md  GEMINI.md  README.md
retos/
  README.md          índice de retos, parejas, revisores y reparto por persona
  <ID>/              RIE-03, NEG-01, NEG-02, RIE-01, RIE-02, NEG-03, COM-01, COM-02
    README.md        ficha del reto + tareas hasta el 25.11  ← empieza aquí
    expediente.md    texto literal del reto (CONFIDENCIAL, solo local, ignorado por git)
    concepto.md      Concepto de solución: 8 secciones + anexos (A tareas, B preguntas, C revisión)
    panorama.md      cómo se abastecería: datos, modelo, arquitectura, plan del evento, KPI, riesgos, cotejo
    postulacion.md   texto para pegar en la plataforma
    datos/           generador de datos sintéticos + pruebas (salida en datos/sintetico/, ignorada)
identidad/           guía de marca de Yupana Labs, logos SVG, patrón y tokens (CSS y JSON)
docs/
  investigacion/     bases, plataforma, equipo, sinergia, alcance comparado
  plan-conceptos.md  flujo de trabajo y calendario 21–26.11
  preexistente.md    componentes previos y su titularidad (se mantiene al día)
  validacion.md      evidencia de pruebas (se llena en el evento)
  consulta-organizacion.md · mensaje-equipo.md · mensaje-glem.md   textos listos para enviar
boveda/              bóveda Obsidian: competencia, decisiones, nodo por reto y Tablero de avance
scripts/             sinergia/ (parejas y prioridad) · conceptos/ (borradores) · boveda/ (tablero) · auditoria/ (dificultad de los datos) · entrega/ (paquetes de entrega y fichas PDF)
backend/ frontend/   esqueleto vacío para el evento; NO poner aquí la funcionalidad crítica antes del 03.12
```

## 4. Cómo se trabaja un reto (flujo)

1. **v0** (generado) → 2. **v1** (la pareja líder edita `concepto.md`) → 3. **panorama** y **cotejo** con el expediente → 4. **postulacion.md** → 5. **revisión cruzada** por el revisor (nunca por quien lo escribió) → 6. **v2** con las objeciones resueltas → 7. el coordinador carga el texto en la plataforma.

- Modelo a imitar para un reto nuevo: `retos/RIE-03/` (concepto, panorama y postulación completos).
- La revisión usa el **Anexo C** de `concepto.md`. Las objeciones van en `retos/<ID>/revision.md`.
- El avance se mide solo: `python scripts/boveda/generar_boveda.py` regenera `boveda/Tablero.md` leyendo los archivos.

## 5. Reglas que no se rompen

1. **Nada de datos reales.** Solo sintéticos (montos en S/, MYPE, agencias de La Libertad, personas y documentos ficticios).
2. **Confidencialidad.** El texto de los expedientes y el material de la Caja **no se sube** (`.gitignore` ya excluye `retos/*/expediente.md`). No pegues expedientes en servicios externos más allá de lo necesario para trabajar. Repo **privado**.
3. **Nada de código ni datos de empleadores o clientes de ninguno del equipo.**
4. **Sin cifras inventadas.** Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. KPI y línea base no están publicados: no los inventes.
5. **La funcionalidad crítica no se construye antes del 03.12** (modelo, agente, API, interfaz o backtest del reto). Sí se permiten: texto, generadores de datos sintéticos con pruebas, plantillas y herramientas de planificación, siempre declarados en `docs/preexistente.md`.
6. **Lo simple y demostrable gana.** Si algo no cabe en ~8 h por persona en el evento, dilo en el panorama.
7. **El expediente manda.** Si el concepto y el expediente literal chocan, se corrige el concepto.
8. **Una persona, una carpeta.** Edita solo los retos que lideras o revisas; si necesitas tocar otro, avisa a la pareja líder.
9. **Identidad Yupana Labs.** Todo material del equipo (decks, fichas, videos, documentos) usa la identidad de `identidad/README.md` (logo, paleta, tipografía y tono). Se regenera con `python scripts/identidad/generar_identidad.py`; no se improvisan colores ni logos.
10. **No ejecutes por el humano** acciones externas (enviar mensajes a la organización, postular en la plataforma, publicar): prepara el texto y deja que la persona lo haga.

## 6. Comandos

Python 3.10+ (el stack del evento será 3.11+). Desde la raíz:

```powershell
pip install pytest pandas numpy scikit-learn         # lo mínimo para las pruebas actuales
python -m pytest -q                                  # todas las pruebas (≈165)
python scripts/boveda/generar_boveda.py              # regenera Tablero y nodos de la bóveda
python scripts/sinergia/sinergia.py                  # informe de parejas y prioridad
python retos/RIE-03/datos/generar.py                 # datos sintéticos de un reto → retos/RIE-03/datos/sintetico/
python -m pytest retos/RIE-03/datos -q               # pruebas del generador de un reto
```

Para abrir la bóveda: Obsidian → «Abrir carpeta como bóveda» → **la carpeta raíz del repo**.

## 7. Git

- Rama por persona y reto: `reto/<id>-<persona>` (ej. `reto/neg-01-glem`). `main` solo recibe lo revisado.
- Commits pequeños, en español, imperativo: `NEG-01: concepto v1 (secciones 1–4)`.
- Antes de empezar: `git pull`. Antes de cerrar: pruebas en verde.
- El historial git es **evidencia** de desarrollo; no reescribas historia compartida.

## 8. Al terminar una tarea

Resumen corto de lo hecho, archivos tocados y siguiente paso sugerido. Marca la casilla en `retos/<ID>/README.md`.

## 9. Dónde está el contexto

- Reglas de la competencia y criterios: `boveda/Competencia/` y `docs/investigacion/01-bases-y-panorama.md`.
- Qué dice la plataforma y los comunicados: `docs/investigacion/02-plataforma-equipos.md`.
- Equipo, roles y estrategia de alcance: `docs/investigacion/03-equipo-y-alcance.md`.
- Por qué sintéticos y no reales: `boveda/Decisiones/Datos-reales-vs-sinteticos.md`.
- Contexto de fondo del proyecto: `CLAUDE.md`.
