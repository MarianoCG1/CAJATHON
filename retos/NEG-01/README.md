# NEG-01 · Plan de pagos adaptado al ciclo económico del negocio

> El 25.11 (19:02) la Caja actualizó el expediente y cambió el título (antes: «Cuotas que se adaptan al flujo del negocio»). El v1 está escrito sobre esa versión, sus 10 preguntas frecuentes y la respuesta a nuestro ticket del 24.11.

| | |
|---|---|
| **Prioridad** | #2 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 4 Inclusión financiera y resiliencia |
| **Pareja líder** | Antonio + Glem |
| **Revisor (no escribe este reto)** | David |
| **Owners en la plataforma** | (ver plataforma) |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

«Ritmo»: el asesor estima el ciclo económico del negocio (patrón del sector y la zona ajustado al cliente) y obtiene el plan de pagos de menor costo que cumple Cuota/Utilidad Neta ≤ factor en cada etapa, con el porqué de cada cuota y su prueba de estrés frente a la cuota fija. *(supuesto del equipo, no del expediente)*

## Qué hay en esta carpeta

| Archivo | Para qué sirve | Estado |
|---|---|---|
| `expediente.md` | Texto literal del reto copiado de la plataforma. **Confidencial: solo local, está en `.gitignore`** | ✅ copiado el 25.11 (versión de las 19:02, con FAQ y ticket) |
| `concepto.md` | Concepto de solución (8 secciones + anexos). v1 del 25.11. | ✅ v1 |
| `panorama.md` | Cómo se abastecería el reto: datos, modelo, arquitectura, plan del evento, KPI, riesgos, cotejo con el expediente | ✅ v1 con cotejo |
| `postulacion.md` | Texto para pegar en el formulario de la plataforma (25–26.11) | ✅ v1 |
| `datos/` | Generador de datos sintéticos con pruebas (`generar.py`, `test_generar.py`); la salida va a `datos/sintetico/` (ignorada por git) | ⬜ decisión pendiente (opcional: aporta evidencia medida a Factibilidad) |

## Qué toca hacer hasta el 25.11

Marca las casillas editando este archivo y haz commit. El avance automático lo lee `boveda/Tablero.md`.

- [x] Copiar el expediente desde la plataforma a `retos/NEG-01/expediente.md` (solo local).
- [x] **Concepto v1:** editar `concepto.md` (completar las 8 secciones, ajustar la funcionalidad crítica, quitar lo genérico). Modelo a imitar: `retos/RIE-03/concepto.md`.
- [x] **Panorama de abastecimiento:** crear `panorama.md` con las secciones del modelo `retos/RIE-03/panorama.md` (datos, modelo, arquitectura, plan del evento, KPI, riesgos, preexistente, cotejo).
- [x] **Cotejo** palabra por palabra con el expediente: añadir al panorama una sección «Cotejo con el expediente».
- [ ] Decidir si hace falta un generador de datos sintéticos (`datos/`). Si sí: semilla fija, pruebas y declararlo en `docs/preexistente.md`. **No construir la funcionalidad crítica.**
- [x] **Texto de postulación** en `postulacion.md` (~700–750 palabras, *supuesto del equipo*; confirmar el formato del formulario). Modelo: `retos/RIE-03/postulacion.md`.
- [ ] **Revisión cruzada** (David) y v2.
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Dado un cliente y una operación, el sistema estima su ciclo (UN por etapa con banda), construye el plan óptimo con monto y periodo por cuota bajo las reglas del producto, explica por qué cada cuota es alta o baja, muestra Cuota/UN por etapa y lo compara con la cuota fija en escenarios base y adversos; el asesor ajusta y el comité decide. Detalle en `concepto.md` §6.

## Preguntas para el owner

Casi todas quedaron resueltas por las preguntas frecuentes y el ticket del 24.11 (ver `panorama.md`, «Cotejo con el expediente»). Siguen abiertas y se asumen: factores, cuota mínima, plazo y topes por producto; regla de holgura frente a escenarios adversos; topes de concentración y de gracia; línea base de retención. Lista en `concepto.md`, Anexo B.
