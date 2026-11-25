# COM-01 · Encontrar oportunidades donde otros no ven clientes

| | |
|---|---|
| **Prioridad** | #7 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 2 Experiencia, retención y crecimiento |
| **Pareja líder** | Antonio + Glem |
| **Revisor (no escribe este reto)** | David |
| **Owners en la plataforma** | (ver plataforma) |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

Mapa de potencial comercial por zona/segmento con un modelo de priorización y un agente que genera el brief de prospección para el analista. *(supuesto del equipo, no del expediente)*

## Qué hay en esta carpeta

| Archivo | Para qué sirve | Estado |
|---|---|---|
| `expediente.md` | Texto literal del reto copiado de la plataforma. **Confidencial: solo local, está en `.gitignore`** | ⬜ cada persona lo copia de la plataforma |
| `concepto.md` | Concepto de solución (8 secciones + anexos). Borrador v0 generado: hay que editarlo a v1. | ✅ existe |
| `panorama.md` | Cómo se abastecería el reto: datos, modelo, arquitectura, plan del evento, KPI, riesgos, cotejo con el expediente | ⬜ por crear |
| `postulacion.md` | Texto para pegar en el formulario de la plataforma (25–26.11) | ⬜ por crear |
| `datos/` | Generador de datos sintéticos con pruebas (`generar.py`, `test_generar.py`); la salida va a `datos/sintetico/` (ignorada por git) | ⬜ por crear |

## Qué toca hacer hasta el 25.11

Marca las casillas editando este archivo y haz commit. El avance automático lo lee `boveda/Tablero.md`.

- [ ] Copiar el expediente desde la plataforma a `retos/COM-01/expediente.md` (solo local).
- [ ] **Concepto v1:** editar `concepto.md` (completar las 8 secciones, ajustar la funcionalidad crítica, quitar lo genérico). Modelo a imitar: `retos/RIE-03/concepto.md`.
- [ ] **Panorama de abastecimiento:** crear `panorama.md` con las secciones del modelo `retos/RIE-03/panorama.md` (datos, modelo, arquitectura, plan del evento, KPI, riesgos, preexistente, cotejo).
- [ ] **Cotejo** palabra por palabra con el expediente: añadir al panorama una sección «Cotejo con el expediente».
- [ ] Decidir si hace falta un generador de datos sintéticos (`datos/`). Si sí: semilla fija, pruebas y declararlo en `docs/preexistente.md`. **No construir la funcionalidad crítica.**
- [ ] **Texto de postulación** en `postulacion.md` (~700–750 palabras, *supuesto del equipo*; confirmar el formato del formulario). Modelo: `retos/RIE-03/postulacion.md`.
- [ ] **Revisión cruzada** (David) y v2.
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Mapa de potencial comercial que prioriza zonas y segmentos con datos territoriales y económicos, y genera para cada oportunidad un brief de prospección que el analista puede usar, sin inferir elegibilidad ni capacidad de pago.

## Preguntas para el owner (a reformular como comprensión)

- ¿Qué datos territoriales y de cobertura financiera podemos usar?
- ¿Cuál es la línea base de conversión de prospectos y cómo se mide?
- ¿Qué fuentes digitales públicas están permitidas?
