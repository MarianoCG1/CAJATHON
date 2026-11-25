# Concepto de solución — NEG-03 · Continuidad del vínculo cuando cambia el analista

> **BORRADOR v0 (generado).** Prioridad **#6** · Pareja líder **David + Glem** · Eje: 2 Experiencia, retención y crecimiento · Owners (plataforma): (ver plataforma).
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.

## 1. Problema abordado

Cuando un analista cambia de cartera o deja la institución, parte del conocimiento sobre el negocio y el comportamiento del cliente se pierde. El vínculo se debilita y crece el riesgo de desvinculación.

Riesgos y restricciones que el expediente pide respetar: No asumir que cambiar de analista implica perder al cliente; Privacidad de datos; Resúmenes sin evidencia (alucinación).

## 2. Concepto de solución

Agente de traspaso que resume la relación, historial y señales de cada cliente para el nuevo analista, más un modelo que prioriza a los clientes con riesgo de desvinculación y sugiere la primera acción. **(supuesto)**

**Diferenciación:** Combina memoria resumida de la relación con priorización predictiva; no es solo un resumen de historial.

**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana y no se ejecutan acciones crediticias automáticas.

## 3. Impacto esperado en el KPI

KPI candidatos **(supuesto, a validar con el owner)**:

- Tasa de retención o renovación de clientes tras un cambio de analista (backtest)
- Tiempo hasta el primer contacto efectivo del nuevo analista
- Precisión del modelo de riesgo de desvinculación

- **Línea base:** [POR CONFIRMAR con el owner]
- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]
- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija.

## 4. Enfoque tecnológico

Pila base: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.

Componentes que requiere este desafío (según las tareas):

- **Agentes de IA:** Agente con Pydantic AI y proveedor de LLM intercambiable (Claude, OpenAI o modelo local); herramientas acotadas y aprobación humana
- **Machine Learning:** Modelos con scikit-learn (y LightGBM si aporta), con calibración y validación temporal
- **IA generativa (LLM, prompts, RAG):** LLM para redactar resúmenes y mensajes, con salidas estructuradas y verificación contra los datos
- **Análisis de negocio, KPI y backtest:** Backtest del KPI con y sin la solución (scripts/evaluar_kpi.py)
- **Backend, APIs e integración:** API REST con FastAPI y Pydantic v2; persistencia en SQLite
- **Ingeniería de datos / datos sintéticos / ETL:** Generador de datos sintéticos reproducible (semilla fija) y ETL con pandas
- **Mejora de procesos:** Mapa del proceso actual y propuesto
- **Desarrollo web / front-end:** Interfaz React + Vite + Tailwind CSS con componentes ya hechos
- **UX/UI e investigación de usuarios:** Flujo del usuario validado con prototipo navegable
- **Pitch y storytelling:** Guion de demo y presentación
- **Pruebas y QA:** Pruebas automáticas con pytest y reporte de validación (docs/validacion.md)

El expediente exige capacidades avanzadas con valor real y desarrollo funcional; no basta un chatbot genérico, un dashboard, un formulario o una automatización básica. El valor diferencial está en el modelo y el agente descritos arriba.

## 5. Tecnología preexistente

- Librerías de código abierto (FastAPI, pandas, scikit-learn, React, etc.) bajo sus licencias.
- Generador de datos sintéticos y herramientas de planificación del equipo (titularidad: equipo; ver `docs/preexistente.md`).
- **No se reutiliza código de empleadores ni de otros clientes.** No se usan datos reales.

## 6. Funcionalidad crítica

Agente de traspaso que resume la relación, el historial y las señales de cada cliente para el nuevo analista y prioriza, con un modelo de riesgo de desvinculación, a quién contactar primero y con qué mensaje, con revisión humana. **(supuesto)**

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso: Un analista deja su cartera; el nuevo recibe la ficha de traspaso por cliente, la lista priorizada y el mensaje sugerido para el primer contacto.

Incluye pruebas automáticas, reporte de validación y un número antes/después del KPI.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP:** 35 horas-persona **(supuesto)**. En el evento hay ~8 h por persona (32 h con 4 personas).
- **Cobertura de habilidades del equipo:** 83%. Sin brechas relevantes.
- **Brechas de la pareja líder** (cubre el resto del equipo): KPI de retención y backtest (3 h).
- **Dependencias:** datos sintéticos de la Caja (si no llegan, usamos nuestro generador); política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**.
- **Recorte si falta tiempo:** se mantiene el núcleo (modelo + recomendación + backtest) y se simplifica la interfaz.

---

## Anexo A. Tareas y horas (supuesto)

| Tarea | Habilidad | Horas |
|---|---|---|
| Datos sintéticos de interacciones, cambios de analista y renovaciones | data_eng | 3 |
| Modelo de riesgo de desvinculación | ml | 4 |
| Agente de traspaso que resume y recomienda | agentes | 5 |
| Resúmenes y mensajes con IA generativa | ia_gen | 4 |
| API y persistencia | backend | 3 |
| Ficha de traspaso e interfaz del analista | web | 3 |
| Diseño del flujo de traspaso | ux | 3 |
| Proceso de traspaso y gobierno | proc | 3 |
| KPI de retención y backtest | biz | 3 |
| Pruebas y validación | qa | 2 |
| Pitch y demo | pitch | 2 |

## Anexo B. Preguntas para el owner

- [ ] ¿Cuál es la tasa actual de desvinculación tras un cambio de analista y cómo se mide?
- [ ] ¿Qué interacciones se registran hoy y dónde (CRM, notas)?
- [ ] ¿Podemos asumir datos sintéticos de interacciones y renovaciones?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
