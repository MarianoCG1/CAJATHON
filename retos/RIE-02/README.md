# RIE-02 · Descubrir redes de riesgo ocultas

| | |
|---|---|
| **Prioridad** | #5 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 3 Riesgo, fraude y recuperaciones inteligentes |
| **Pareja líder** | David + Mariano |
| **Revisor (no escribe este reto)** | Antonio |
| **Owners en la plataforma** | Carlos |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

Detector de redes sospechosas entre personas, negocios, teléfonos, direcciones y dispositivos con análisis de grafos, que prioriza casos y entrega la evidencia a un investigador con ayuda de un agente. *(supuesto del equipo, no del expediente)*

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

- [ ] Copiar el expediente desde la plataforma a `retos/RIE-02/expediente.md` (solo local).
- [ ] **Revisión cruzada** (Antonio): leer `concepto.md`, `panorama.md` y `postulacion.md` contra el expediente y el Anexo C de `concepto.md`; anotar objeciones en `retos/RIE-02/revision.md`.
- [ ] La pareja líder resuelve las objeciones (v2) y actualiza `postulacion.md`.
- [ ] Reformular las preguntas del Anexo B del concepto a preguntas de **comprensión** del problema (la organización dijo que en esta etapa no entrega datos).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Detección de redes inusuales con análisis de grafos sobre solicitudes, que prioriza los casos más sospechosos y arma para el investigador un expediente con la evidencia, distinguiendo relaciones legítimas de patrones de riesgo.

## Preguntas para el owner (a reformular como comprensión)

- ¿Qué tipos de vínculos son más relevantes para la Caja (teléfono, dispositivo, dirección, referencia)?
- ¿Habrá casos simulados etiquetados para validar el detector?
- ¿Cuál es la tasa actual de falsos positivos y el tiempo de revisión por caso?
