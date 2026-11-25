# RIE-01 · Microfinanzas resilientes al clima

| | |
|---|---|
| **Prioridad** | #4 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 4 Inclusión financiera y resiliencia |
| **Pareja líder** | Antonio + Mariano |
| **Revisor (no escribe este reto)** | Glem |
| **Owners en la plataforma** | (ver plataforma) |
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
- [x] Preguntas del Anexo B reformuladas a **comprensión** del problema (21.11, Mariano).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Mapa de exposición climática de la cartera con escenarios, que prioriza clientes y zonas con mayor vulnerabilidad y propone acciones preventivas a través de un agente, sin asumir que exposición equivale a incumplimiento.

## Preguntas para el owner (de comprensión; ver Anexo B del concepto)

- ¿Cómo mide y gestiona hoy la Caja el riesgo por eventos climáticos (El Niño, lluvias, sequías)? ¿Qué pérdida o mora se les atribuye y quién la calcula?
- ¿Qué acciones preventivas son viables (alerta, visita, reprogramación, ampliación de plazo, capital de reposición, microseguro) y cuáles requieren comité o normativa? ¿Qué implica una reprogramación preventiva para la calificación?
- ¿Cuántos gestores hay por agencia y cuántas visitas por semana son realistas ante una emergencia?
- ¿Qué sabe hoy la Caja de sus clientes que ayude a medir su exposición (ubicación, actividad, seguro, ingresos secundarios, reservas)?
- ¿Se puede usar información pública de clima y mapas de amenaza como referencia?
- ¿Cuál es el resultado principal que esperan: mora evitada, exposición identificada a tiempo, clientes contactados antes del evento?
- ¿Dónde vería el gestor la alerta hoy y con qué anticipación sirve?
- ¿Hay restricciones para usar IA externa (aun con datos sintéticos)? ¿Cuál es el formato exacto de la postulación y la hora límite del 26.11?
