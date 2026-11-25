# Concepto de solución — NEG-01 · Cuotas que se adaptan al flujo del negocio

> **BORRADOR v0 (generado).** Prioridad **#2** · Pareja líder **Antonio + Glem** · Eje: 4 Inclusión financiera y resiliencia · Owners (plataforma): (ver plataforma).
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.

## 1. Problema abordado

Muchos microempresarios tienen ingresos estacionales, pero los cronogramas de cuotas uniformes no siguen ese ritmo. Esto genera tensiones de liquidez incluso en negocios viables y eleva el riesgo de incumplimiento.

Riesgos y restricciones que el expediente pide respetar: Incertidumbre en la proyección de ingresos; Sobreendeudamiento; Cumplimiento de políticas y normativa.

## 2. Concepto de solución

Motor que estima el flujo estacional de ingresos de cada microempresario, propone un cronograma de cuotas ajustado y valida rentabilidad y riesgo antes de ofrecerlo, con un agente que lo explica al analista. **(supuesto)**

**Diferenciación:** Combina pronóstico de flujo y optimización del cronograma con validación de rentabilidad; no es un simple simulador de cuotas.

**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana y no se ejecutan acciones crediticias automáticas.

## 3. Impacto esperado en el KPI

KPI candidatos **(supuesto, a validar con el owner)**:

- Tasa de cumplimiento de cuotas con cronograma ajustado vs. uniforme (backtest sintético)
- Reducción de la probabilidad de incumplimiento sin bajar el margen de la Caja
- Porcentaje de propuestas que cumplen la política de crédito

- **Línea base:** [POR CONFIRMAR con el owner]
- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]
- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija.

## 4. Enfoque tecnológico

Pila base: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.

Componentes que requiere este desafío (según las tareas):

- **Dominio financiero / microfinanzas:** Reglas y criterios de dominio validados con Caja Experts
- **Machine Learning:** Modelos con scikit-learn (y LightGBM si aporta), con calibración y validación temporal
- **Data Science, estadística, grafos, optimización:** Análisis estadístico, explicabilidad y optimización con pandas, scikit-learn y SciPy
- **Análisis de negocio, KPI y backtest:** Backtest del KPI con y sin la solución (scripts/evaluar_kpi.py)
- **Backend, APIs e integración:** API REST con FastAPI y Pydantic v2; persistencia en SQLite
- **Ingeniería de datos / datos sintéticos / ETL:** Generador de datos sintéticos reproducible (semilla fija) y ETL con pandas
- **Agentes de IA:** Agente con Pydantic AI y proveedor de LLM intercambiable (Claude, OpenAI o modelo local); herramientas acotadas y aprobación humana
- **Desarrollo web / front-end:** Interfaz React + Vite + Tailwind CSS con componentes ya hechos
- **Pitch y storytelling:** Guion de demo y presentación
- **IA generativa (LLM, prompts, RAG):** LLM para redactar resúmenes y mensajes, con salidas estructuradas y verificación contra los datos
- **Pruebas y QA:** Pruebas automáticas con pytest y reporte de validación (docs/validacion.md)
- **UX/UI e investigación de usuarios:** Flujo del usuario validado con prototipo navegable

El expediente exige capacidades avanzadas con valor real y desarrollo funcional; no basta un chatbot genérico, un dashboard, un formulario o una automatización básica. El valor diferencial está en el modelo y el agente descritos arriba.

## 5. Tecnología preexistente

- Librerías de código abierto (FastAPI, pandas, scikit-learn, React, etc.) bajo sus licencias.
- Generador de datos sintéticos y herramientas de planificación del equipo (titularidad: equipo; ver `docs/preexistente.md`).
- **No se reutiliza código de empleadores ni de otros clientes.** No se usan datos reales.

## 6. Funcionalidad crítica

Dado un cliente, el sistema estima su flujo de ingresos estacional, propone un cronograma de cuotas ajustado, valida automáticamente capacidad de pago, tasa, plazo y rentabilidad contra la política, y explica la propuesta al analista, que decide. **(supuesto)**

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso: Un cliente agrícola y uno comercial: se muestra su flujo estimado, el cronograma uniforme vs. el ajustado, la validación de política y el efecto en cumplimiento y rentabilidad.

Incluye pruebas automáticas, reporte de validación y un número antes/después del KPI.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP:** 35 horas-persona **(supuesto)**. En el evento hay ~8 h por persona (32 h con 4 personas).
- **Cobertura de habilidades del equipo:** 83%. Sin brechas relevantes.
- **Brechas de la pareja líder** (cubre el resto del equipo): Diseño del flujo del analista (2 h).
- **Dependencias:** datos sintéticos de la Caja (si no llegan, usamos nuestro generador); política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**.
- **Recorte si falta tiempo:** se mantiene el núcleo (modelo + recomendación + backtest) y se simplifica la interfaz.

---

## Anexo A. Tareas y horas (supuesto)

| Tarea | Habilidad | Horas |
|---|---|---|
| Datos sintéticos de ingresos, estacionalidad y pagos | data_eng | 3 |
| Modelo de flujo de ingresos y estacionalidad | ml | 4 |
| Optimización del cronograma de cuotas | data_sci | 4 |
| Motor de cronogramas y validación de políticas | backend | 3 |
| Agente que explica la propuesta al analista | agentes | 3 |
| Mensajes y simulaciones con IA generativa | ia_gen | 2 |
| Simulador de cuotas | web | 3 |
| Diseño del flujo del analista | ux | 2 |
| Políticas de crédito, tasas y rentabilidad | fin | 4 |
| KPI y backtest de cumplimiento y rentabilidad | biz | 3 |
| Pruebas y validación | qa | 2 |
| Pitch y demo | pitch | 2 |

## Anexo B. Preguntas para el owner

- [ ] ¿Qué variantes de cronograma flexible permite hoy la normativa y la política de la Caja?
- [ ] ¿Cuál es la línea base de cumplimiento y de rentabilidad por producto?
- [ ] ¿Habrá datos sintéticos de ingresos por mes y estacionalidad por actividad?
- [ ] ¿Qué restricciones de tasa, plazo y rentabilidad mínima debe respetar la propuesta?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
