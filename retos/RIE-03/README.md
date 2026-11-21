# RIE-03 · Anticipar el deterioro de pago antes del atraso

| | |
|---|---|
| **Prioridad** | #1 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 3 Riesgo, fraude y recuperaciones inteligentes |
| **Pareja líder** | David + Mariano |
| **Revisor (no escribe este reto)** | Glem |
| **Owners en la plataforma** | Wilson, Harold, Paul |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

Modelo de alerta temprana de deterioro de pago con explicación de señales y un agente que recomienda la intervención preventiva (canal, momento, propuesta), con revisión humana. *(supuesto del equipo, no del expediente)*

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

- [ ] Copiar el expediente desde la plataforma a `retos/RIE-03/expediente.md` (solo local).
- [ ] **Revisión cruzada** (Glem): leer `concepto.md`, `panorama.md` y `postulacion.md` contra el expediente y el Anexo C de `concepto.md`; anotar objeciones en `retos/RIE-03/revision.md`.
- [ ] La pareja líder resuelve las objeciones (v2) y actualiza `postulacion.md`.
- [ ] Comprobar que los datos sintéticos no se resuelven con una regla trivial (en RIE-02 ya se endureció): correr el generador y probar un modelo simple.
- [ ] Reformular las preguntas del Anexo B del concepto a preguntas de **comprensión** del problema (la organización dijo que en esta etapa no entrega datos).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Cola diaria priorizada de clientes con riesgo de deterioro, con la explicación de las señales que la originan y una intervención recomendada por un agente (canal, momento, propuesta). El gestor aprueba, edita o descarta; nada se ejecuta de forma automática.

## Preguntas para el owner (a reformular como comprensión)

- ¿Cuál es la morosidad actual de la cartera y cómo se mide (mora > 8, > 30 días)? ¿Cuál sería la mejora que consideran relevante?
- ¿Qué señales de deterioro monitorean hoy y con qué frecuencia?
- ¿Qué columnas y volumen tendrán los datos sintéticos (historial de pagos, saldos, actividad económica)?
- ¿Qué canales de contacto preventivo son viables para el gestor?
- ¿Hay restricciones para usar modelos de IA externos con datos sintéticos?
