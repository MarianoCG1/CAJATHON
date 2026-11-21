# RIE-01 · Microfinanzas resilientes al clima

| | |
|---|---|
| **Prioridad** | #4 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 4 Inclusión financiera y resiliencia |
| **Pareja líder** | Antonio + Mariano |
| **Revisor (no escribe este reto)** | Glem |
| **Owners en la plataforma** | Miriam |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

Mapa de exposición de la cartera a eventos climáticos con escenarios, que prioriza a los clientes expuestos y recomienda acciones preventivas a través de un agente. *(supuesto del equipo, no del expediente)*

## Qué hay en esta carpeta

| Archivo | Para qué sirve | Estado |
|---|---|---|
| `expediente.md` | Texto literal del reto copiado de la plataforma. **Confidencial: solo local, está en `.gitignore`** | ⬜ cada persona lo copia de la plataforma |
| `concepto.md` | Concepto de solución (8 secciones + anexos). Ya editado a v1. | ✅ existe |
| `panorama.md` | Cómo se abastecería el reto: datos, modelo, arquitectura, plan del evento, KPI, riesgos, cotejo con el expediente | ✅ existe |
| `postulacion.md` | Texto para pegar en el formulario de la plataforma (25–26.11) | ✅ existe |
| `datos/` | Generador de datos sintéticos con pruebas (`generar.py`, `test_generar.py`); la salida va a `datos/sintetico/` (ignorada por git) | ✅ existe |

## Qué toca hacer hasta el 25.11

Marca las casillas editando este archivo y haz commit. El avance automático lo lee `boveda/Tablero.md`.

- [ ] Copiar el expediente desde la plataforma a `retos/RIE-01/expediente.md` (solo local).
- [ ] **Revisión cruzada** (Glem): leer `concepto.md`, `panorama.md` y `postulacion.md` contra el expediente y el Anexo C de `concepto.md`; anotar objeciones en `retos/RIE-01/revision.md`.
- [ ] La pareja líder resuelve las objeciones (v2) y actualiza `postulacion.md`.
- [ ] Comprobar que los datos sintéticos no se resuelven con una regla trivial (en RIE-02 ya se endureció): correr el generador y probar un modelo simple.
- [ ] Reformular las preguntas del Anexo B del concepto a preguntas de **comprensión** del problema (la organización dijo que en esta etapa no entrega datos).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Mapa de exposición climática de la cartera con escenarios, que prioriza clientes y zonas con mayor vulnerabilidad y propone acciones preventivas a través de un agente, sin asumir que exposición equivale a incumplimiento.

## Preguntas para el owner (a reformular como comprensión)

- ¿Qué fuentes climáticas y mapas de amenaza podemos usar (públicas o sintéticas)?
- ¿Cuál es hoy el indicador de exposición o pérdida por eventos climáticos?
- ¿Qué acciones preventivas son viables para la Caja (reprogramación, alertas, seguros)?
