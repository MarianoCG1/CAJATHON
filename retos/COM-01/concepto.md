# Concepto de solución — COM-01 · Encontrar oportunidades donde otros no ven clientes

> **BORRADOR v0 (generado).** Prioridad **#7** · Pareja líder **Antonio + Glem** · Eje: 2 Experiencia, retención y crecimiento · Owners (plataforma): (ver plataforma).
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.

## 1. Problema abordado

La prospección comercial depende de la experiencia del analista y de referencias. Pueden existir zonas o segmentos con potencial de inclusión financiera que no resultan evidentes con los métodos tradicionales.

Riesgos y restricciones que el expediente pide respetar: Sesgos y exclusión injustificada; Uso responsable de fuentes públicas; Potencial no es elegibilidad.

## 2. Concepto de solución

Mapa de potencial comercial por zona/segmento con un modelo de priorización y un agente que genera el brief de prospección para el analista. **(supuesto)**

**Diferenciación:** Brief accionable por zona, con evidencia y sin discriminación ni inferencias sensibles.

**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana y no se ejecutan acciones crediticias automáticas.

## 3. Impacto esperado en el KPI

KPI candidatos **(supuesto, a validar con el owner)**:

- Tasa de conversión de prospectos de zonas priorizadas vs. prospección tradicional (backtest sintético)
- Número de zonas o segmentos nuevos identificados con potencial
- Productividad de la prospección (prospectos efectivos por jornada)

- **Línea base:** [POR CONFIRMAR con el owner]
- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]
- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija.

## 4. Enfoque tecnológico

Pila base: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.

Componentes que requiere este desafío (según las tareas):

- **Data Science, estadística, grafos, optimización:** Análisis estadístico, explicabilidad y optimización con pandas, scikit-learn y SciPy
- **Desarrollo web / front-end:** Interfaz React + Vite + Tailwind CSS con componentes ya hechos
- **Análisis de negocio, KPI y backtest:** Backtest del KPI con y sin la solución (scripts/evaluar_kpi.py)
- **Backend, APIs e integración:** API REST con FastAPI y Pydantic v2; persistencia en SQLite
- **Ingeniería de datos / datos sintéticos / ETL:** Generador de datos sintéticos reproducible (semilla fija) y ETL con pandas
- **Agentes de IA:** Agente con Pydantic AI y proveedor de LLM intercambiable (Claude, OpenAI o modelo local); herramientas acotadas y aprobación humana
- **Dominio financiero / microfinanzas:** Reglas y criterios de dominio validados con Caja Experts
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

Mapa de potencial comercial que prioriza zonas y segmentos con datos territoriales y económicos, y genera para cada oportunidad un brief de prospección que el analista puede usar, sin inferir elegibilidad ni capacidad de pago. **(supuesto)**

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso: Se selecciona una provincia, el mapa prioriza distritos, y el agente entrega el brief con la actividad económica, la cobertura financiera y el abordaje sugerido.

Incluye pruebas automáticas, reporte de validación y un número antes/después del KPI.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP:** 31 horas-persona **(supuesto)**. En el evento hay ~8 h por persona (32 h con 4 personas).
- **Cobertura de habilidades del equipo:** 81%. Sin brechas relevantes.
- **Brechas de la pareja líder** (cubre el resto del equipo): Diseño del flujo del analista (2 h).
- **Dependencias:** datos sintéticos de la Caja (si no llegan, usamos nuestro generador); política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**.
- **Recorte si falta tiempo:** se mantiene el núcleo (modelo + recomendación + backtest) y se simplifica la interfaz.

---

## Anexo A. Tareas y horas (supuesto)

| Tarea | Habilidad | Horas |
|---|---|---|
| Datos territoriales y de negocios sintéticos | data_eng | 3 |
| Modelo de potencial y priorización de zonas | data_sci | 5 |
| Mapa interactivo y fichas de zona | web | 4 |
| Diseño del flujo del analista | ux | 2 |
| Agente que explica la zona y propone el abordaje | agentes | 3 |
| Redacción de briefs con IA generativa | ia_gen | 2 |
| API y persistencia | backend | 3 |
| KPI de captación y backtest | biz | 3 |
| Criterios de inclusión financiera y sesgos | fin | 2 |
| Pruebas y validación | qa | 2 |
| Pitch y demo | pitch | 2 |

## Anexo B. Preguntas para el owner

- [ ] ¿Qué datos territoriales y de cobertura financiera podemos usar?
- [ ] ¿Cuál es la línea base de conversión de prospectos y cómo se mide?
- [ ] ¿Qué fuentes digitales públicas están permitidas?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
