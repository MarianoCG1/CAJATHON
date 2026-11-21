# CLAUDE.md — Cajathon 2026 (Caja Trujillo)

Contexto permanente del proyecto para Claude Code. Léelo completo antes de cada tarea.

> **Antes que nada, lee `AGENTS.md`**: es la guía común para cualquier agente (Claude, GPT/Codex, Antigravity/Gemini) y trae el mapa del repo, el reparto por persona y las reglas. Este archivo es el contexto de fondo; si algo choca con `AGENTS.md`, manda `AGENTS.md`.

## 1. Qué es este proyecto

Preparación y construcción de la solución del equipo para el **Cajathon 2026**, hackathon de IA de Caja Trujillo.
Objetivo: **ganar** (1.er lugar S/ 5,000, 2.º S/ 3,000) y abrir una colaboración con Caja Trujillo.

- Equipo: **Yupana Labs** (categoría Profesionales, 4 integrantes), planteado como una **consultora TI**: cada desafío es un encargo de cliente y entregamos un Concepto de solución por encargo. Se postuló a Recuperaciones, pero la organización confirmó por WhatsApp (20.11) que **se puede elegir cualquier desafío**. **Desafío a construir: pendiente de decisión** (candidato: `RIE-03`); solo se construye uno, y solo si llegamos a la final.
- **Estado al 21.11:** la plataforma no tiene expediente de Recuperaciones (`REC-01`). Hay 8 expedientes (la organización habló de 6; aclarar): `COM-01`, `COM-02`, `NEG-01`, `NEG-02`, `NEG-03`, `RIE-01`, `RIE-02`, `RIE-03` (resumen en `docs/investigacion/02-plataforma-equipos.md`). Los códigos anteriores cambiaron. El más cercano es `RIE-03` (eje «Riesgo, fraude y recuperaciones inteligentes»).
- **Concepto de solución: se postula del 25 al 26.11** en la plataforma (no el 24.11). Confirmar hora límite.
- Fuente oficial: https://cajathon.cajatrujillo.com.pe/bases/ (**v4, 05.11.2026**; resumen y cambios en `docs/investigacion/01-bases-y-panorama.md`). Son 18 equipos en fase virtual y 12 finalistas. Plataforma del equipo: https://cajathon.cajatrujillo.com.pe/equipos/ (requiere login).

## 2. Los desafíos

Hay un expediente por desafío. El texto literal es **confidencial**: cada persona lo copia de la plataforma a `retos/<ID>/expediente.md` (archivo ignorado por git). Ficha, estado y tareas de cada uno: `retos/<ID>/README.md`; índice y reparto: `retos/README.md`.

El expediente publica problema y resultado esperado, pero **no KPI ni línea base**: son preguntas abiertas para el owner (KPI y línea base, qué datos habrá, política de IA externa, canal de contacto viable, flujo actual donde se integraría). El comunicado del 21.11 aclara que en esta etapa la organización no entrega datos.

## 3. Equipo y roles

| Integrante | Perfil | Rol en el reto |
|---|---|---|
| Mariano (developer, coordinador) | Ing. TI. Backend/APIs 5/5, agentes de IA 5/5, ML 5/5 (perfil en plataforma) | Backend, integración de IA, repo y entrega técnica |
| Glem (analista de datos) | Ciencia de Datos. ML, FastAPI, React, ETL, Power BI. 1.er puesto Datathon SUNASS 2026; sin experiencia en sector financiero | Datos sintéticos, modelo, métricas y pruebas de validación |
| Antonio (economista) | Economía. Experiencia en sector financiero (operaciones, comercial, negocios), Power BI, Python; primer hackathon | Dueño del KPI: impacto financiero, caso de negocio, backtest, pitch |
| David (ing. industrial / UX-UI) | Ing. Industrial. Investigación de usuarios, flujos, prototipado, Flask/HTML/CSS; primer hackathon | Interfaz del gestor, flujo operativo, demo y presentación |

(Coincide con los perfiles registrados en la plataforma. Detalle y estrategia de alcance en `docs/investigacion/03-equipo-y-alcance.md`.)

Experiencia previa relevante del developer (preexistente, no se cede): automatización de liquidación y cierre de pagos (AutoPS), OCR de comprobantes con conciliación, agente de correos con aprobación humana, modelo predictivo de dosificación (EMAPA Huaral).

## 4. Cómo se gana (criterios oficiales)

**Pase a los 12 finalistas — Solution Concept (postulación 25–26.11):**
Alineación al desafío 25% · Impacto potencial 30% · Viabilidad técnica 25% · Factibilidad de construcción 20%.

**Evaluación final (03–04.12):**

| Criterio | Peso | Subcriterios |
|---|---|---|
| Impacto en el negocio | 35% | Contribución al KPI 25% · Implementación y escalabilidad 10% |
| Funcionalidad y validación | 35% | Funcionalidad crítica 20% · Pruebas y evidencia 15% |
| Innovación y calidad | 20% | Diferenciación 15% · Simplicidad del diseño 5% |
| Presentación y demo | 10% | Claridad 5% · Demo 5% |

**Condición eliminatoria:** mínimo 3/5 en «funcionamiento de la funcionalidad crítica» y desarrollo nuevo hecho durante las jornadas presenciales. Sin esto no hay premio, sin importar el puntaje.

Implicancias para todo lo que construyamos:
1. Una sola **funcionalidad crítica** que funcione de punta a punta vale más que muchas a medias.
2. Todo debe poder **medir el KPI**: cada demo termina mostrando un número antes/después.
3. Las **pruebas son puntaje** (15%): tests automáticos y un reporte de validación desde el día 1.
4. Tiempo real de construcción en el evento: **~8 horas** (entrega día 2 a las 13:00).

## 5. Reglas que no se rompen

- **Preexistente vs. nuevo.** Todo componente previo (repo base, generador de datos, utilidades) se declara en `docs/preexistente.md` con su titularidad. La funcionalidad crítica se construye **en el evento**, con commits frecuentes como evidencia. No adelantarla antes del 03.12.
- **Nada de datos reales.** Prohibido usar datos personales reales, credenciales institucionales o información de nuestros empleadores. Solo datos sintéticos o los que entregue la Caja.
- **Nada de código de empleadores.** No copiar código de los proyectos del Banco de la Nación ni de otros clientes; se reutilizan ideas y experiencia, no archivos.
- **Confidencialidad.** El material de la Caja no se publica ni se sube a repos públicos. Repo **privado**.
- **IA externa.** Hasta confirmar con el owner, diseñar el proveedor de LLM como intercambiable (ver §6).
- **Propiedad intelectual.** Si ganamos, se ceden los derechos de lo desarrollado en el hackathon, no de lo preexistente.

## 6. Stack y arquitectura

- **Backend:** Python 3.11+, FastAPI, Pydantic v2.
- **Agentes / LLM:** Pydantic AI, con el proveedor detrás de una interfaz (`app/llm/provider.py`) para cambiar entre Claude, OpenAI o un modelo local sin tocar la lógica.
- **Datos y modelo:** pandas, scikit-learn (y LightGBM si aporta). Persistencia simple: SQLite.
- **Frontend:** React + Vite + Tailwind CSS. Componentes ya hechos; nada de diseño desde cero.
- **Calidad:** pytest, ruff. Git con commits pequeños y mensajes claros.

Estructura del repositorio (detalle y reparto en `AGENTS.md`):

```
CAJATHON/
├── AGENTS.md  CLAUDE.md  GEMINI.md  README.md
├── retos/
│   ├── README.md             # índice, parejas, revisores y reparto por persona
│   └── <ID>/                 # RIE-03, NEG-01, NEG-02, RIE-01, RIE-02, NEG-03, COM-01, COM-02
│       ├── README.md         # ficha del reto y tareas hasta el 25.11
│       ├── expediente.md     # literal, confidencial, SOLO local (.gitignore)
│       ├── concepto.md  panorama.md  postulacion.md
│       └── datos/            # generador sintético + pruebas; salida en datos/sintetico/ (ignorada)
├── docs/                     # investigación, plan, mensajes, preexistente, validación
├── boveda/                   # bóveda Obsidian: competencia + nodo por reto + tablero
├── scripts/                  # sinergia/, conceptos/, boveda/ (herramientas de planificación)
├── backend/  frontend/       # esqueleto para el evento (03–04.12); sin funcionalidad crítica
```

## 7. Calendario

| Fecha | Hito | Responsable principal |
|---|---|---|
| 21–22.11 (fin de semana) | Investigación dividida + hipótesis de solución + repo base | Todos |
| 22–24.11 | Conceptos v1/v2 y revisión cruzada por pareja (ver `docs/plan-conceptos.md`) | Parejas |
| **25–26.11** | **Postulación del Solution Concept en la plataforma** (confirmar hora límite) | Coordinador |
| 25–29.11 | Evaluación. Ensayo de sprint de 8 h con datos sintéticos | Todos |
| 30.11 | Anuncio de 12 finalistas | — |
| 01.12 | Inmersión tecnológica | Todos |
| **03–04.12** | **Hackathon presencial**, Hub Digital UPAO, 9:00–18:00 | Todos |

Agenda del evento: Día 1 — validación del enfoque 09:45, construcción 10:30–13:00 y 14:00–16:30, pruebas 16:30–17:30. Día 2 — construcción 09:30–12:00, validación final 12:00–12:45, **entrega 13:00**, pitch 15:00.

## 8. Entregables

**Solution Concept (25–26.11):** problema abordado · concepto de solución · impacto esperado en el KPI · enfoque tecnológico · tecnología preexistente · funcionalidad crítica · nivel de desarrollo esperado · factibilidad y dependencias.

**Final (04.12):** prototipo funcional · demo con caso de uso · evidencia de validación · impacto en el KPI · presentación · evidencia de desarrollo (historial git) · entrega técnica (docs + preexistente vs. nuevo).

## 9. Cómo debe trabajar Claude Code aquí

- Responder y documentar en **español**.
- Antes de proponer una solución, releer `retos/<ID>/expediente.md` (si existe en el equipo) y §4: toda idea se justifica contra el KPI y los pesos.
- Marcar como **supuesto** cualquier dato que no venga del expediente oficial; nunca presentarlo como hecho.
- Preferir lo simple y demostrable sobre lo sofisticado; si algo no cabe en ~8 h, decirlo.
- Cada funcionalidad nueva llega con su test y, si toca el KPI, con su actualización en `docs/validacion.md`.
- No generar ni usar datos personales reales. Los datos sintéticos deben ser plausibles para una caja municipal peruana (montos en S/, MYPE, agencias en La Libertad), sin copiar personas reales.
- Al terminar una tarea: resumen corto, archivos tocados y siguiente paso sugerido.

## 10. Qué toca ahora (hasta el 25.11)

Hecho: estructura, investigación, reparto de parejas, borradores v0 de los 8 conceptos, y concepto v1 + panorama + postulación + generador de datos de RIE-03, NEG-02, RIE-01 y RIE-02. Pendiente: revisión cruzada de esos cuatro; concepto v1, panorama y postulación de NEG-01, NEG-03, COM-01 y COM-02; confirmar con la organización si se aceptan varios conceptos. Tareas por reto en `retos/<ID>/README.md`.
