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
- [x] Comprobar que los datos sintéticos no se resuelven con una regla trivial (auditoría en `docs/investigacion/06-auditoria-datos.md`).
- [x] Preguntas del Anexo B reformuladas a **comprensión** del problema (21.11, Mariano).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Cola diaria priorizada de clientes con riesgo de deterioro, con la explicación de las señales que la originan y una intervención recomendada por un agente (canal, momento, propuesta). El gestor aprueba, edita o descarta; nada se ejecuta de forma automática.

## Preguntas para el owner (de comprensión; ver Anexo B del concepto)

- ¿Cómo define hoy la Caja el «deterioro» de un cliente MYPE y en qué momento se entera (días de atraso, calificación, visita)? ¿Con cuánta anticipación sería útil avisar: 30, 60 o 90 días?
- ¿Qué señales siguen hoy los analistas para sospechar que un cliente empeora, y cada cuánto las revisan?
- ¿Cómo se mide hoy la morosidad y la recuperación (mora > 8 días, > 30 días, cartera en riesgo)? ¿Cuál de esas medidas es la prioritaria para este desafío?
- ¿Cuántos clientes gestiona un analista al día y cuántos contactos preventivos son razonables sin saturar al cliente?
- ¿Qué puede ofrecer el analista por su cuenta (recordatorio, reprogramación, asesoría) y qué requiere comité? ¿Qué canales de contacto son aceptables?
- ¿En qué herramienta trabaja hoy el analista y dónde debería aparecer la alerta?
- ¿Qué esperan ver en la explicación de una alerta para confiar en ella?
- ¿Hay restricciones para usar IA externa (aun con datos sintéticos) o variables que no deben usarse por criterios de equidad?
