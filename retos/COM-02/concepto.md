# Concepto de solución — COM-02 · Incentivos que impulsan un desempeño integral

> **BORRADOR v0 (generado).** Prioridad **#8** · Pareja líder **David + Glem** · Eje: 1 Productividad y transformación comercial · Owners (plataforma): Wilson, Harold, Paul.
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.

## 1. Problema abordado

Los incentivos comerciales influyen en el comportamiento del analista y pueden priorizar el crecimiento sobre la calidad de cartera. Además, el desempeño depende del territorio, la madurez de la cartera y la experiencia.

Riesgos y restricciones que el expediente pide respetar: Equidad entre colaboradores; Normativa laboral; Incentivos perjudiciales para clientes o cartera.

## 2. Concepto de solución

Simulador de esquemas de incentivos con ajuste por territorio y madurez de cartera, que optimiza entre crecimiento, calidad de cartera y presupuesto, con un asistente que explica el efecto de cada regla. **(supuesto)**

**Diferenciación:** Ajuste justo por contexto y optimización con presupuesto, con transparencia sobre cada regla.

**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana y no se ejecutan acciones crediticias automáticas.

## 3. Impacto esperado en el KPI

KPI candidatos **(supuesto, a validar con el owner)**:

- Productividad ajustada por territorio y calidad de cartera bajo distintos esquemas (simulación)
- Índice de equidad entre analistas del esquema propuesto
- Costo del esquema frente al presupuesto

- **Línea base:** [POR CONFIRMAR con el owner]
- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]
- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija.

## 4. Enfoque tecnológico

Pila base: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.

Componentes que requiere este desafío (según las tareas):

- **Data Science, estadística, grafos, optimización:** Análisis estadístico, explicabilidad y optimización con pandas, scikit-learn y SciPy
- **Análisis de negocio, KPI y backtest:** Backtest del KPI con y sin la solución (scripts/evaluar_kpi.py)
- **Desarrollo web / front-end:** Interfaz React + Vite + Tailwind CSS con componentes ya hechos
- **Backend, APIs e integración:** API REST con FastAPI y Pydantic v2; persistencia en SQLite
- **Ingeniería de datos / datos sintéticos / ETL:** Generador de datos sintéticos reproducible (semilla fija) y ETL con pandas
- **Mejora de procesos:** Mapa del proceso actual y propuesto
- **Agentes de IA:** Agente con Pydantic AI y proveedor de LLM intercambiable (Claude, OpenAI o modelo local); herramientas acotadas y aprobación humana
- **Pitch y storytelling:** Guion de demo y presentación
- **Pruebas y QA:** Pruebas automáticas con pytest y reporte de validación (docs/validacion.md)
- **UX/UI e investigación de usuarios:** Flujo del usuario validado con prototipo navegable

El expediente exige capacidades avanzadas con valor real y desarrollo funcional; no basta un chatbot genérico, un dashboard, un formulario o una automatización básica. El valor diferencial está en el modelo y el agente descritos arriba.

## 5. Tecnología preexistente

- Librerías de código abierto (FastAPI, pandas, scikit-learn, React, etc.) bajo sus licencias.
- Generador de datos sintéticos y herramientas de planificación del equipo (titularidad: equipo; ver `docs/preexistente.md`).
- **No se reutiliza código de empleadores ni de otros clientes.** No se usan datos reales.

## 6. Funcionalidad crítica

Simulador de esquemas de incentivos que ajusta el desempeño por territorio y madurez de cartera, optimiza el esquema bajo restricción de presupuesto y explica el efecto de cada regla, sin modificar remuneraciones de forma automática. **(supuesto)**

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso: Se comparan el esquema actual y uno propuesto: se ven el efecto en crecimiento, calidad de cartera, equidad y costo, con la explicación de cada regla.

Incluye pruebas automáticas, reporte de validación y un número antes/después del KPI.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP:** 34 horas-persona **(supuesto)**. En el evento hay ~8 h por persona (32 h con 4 personas).
- **Cobertura de habilidades del equipo:** 79%. Sin brechas relevantes.
- **Brechas de la pareja líder** (cubre el resto del equipo): Diseño de incentivos, equidad y presupuesto (4 h).
- **Dependencias:** datos sintéticos de la Caja (si no llegan, usamos nuestro generador); política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**.
- **Recorte si falta tiempo:** se mantiene el núcleo (modelo + recomendación + backtest) y se simplifica la interfaz.

---

## Anexo A. Tareas y horas (supuesto)

| Tarea | Habilidad | Horas |
|---|---|---|
| Datos sintéticos de analistas, metas y cartera | data_eng | 3 |
| Modelo de desempeño ajustado por territorio y madurez | data_sci | 5 |
| Optimización de esquema bajo restricción de presupuesto | data_sci | 3 |
| Asistente que explica y compara esquemas | agentes | 3 |
| Simulador interactivo | web | 4 |
| Diseño del simulador y de la vista del analista | ux | 2 |
| API y motor de reglas | backend | 3 |
| Diseño de incentivos, equidad y presupuesto | biz | 4 |
| Proceso de evaluación y reconocimiento | proc | 3 |
| Pruebas y validación | qa | 2 |
| Pitch y demo | pitch | 2 |

## Anexo B. Preguntas para el owner

- [ ] ¿Cuáles son hoy los indicadores y metas de los analistas y su peso?
- [ ] ¿Qué restricciones presupuestarias y laborales debe respetar el modelo?
- [ ] ¿Habrá datos sintéticos por analista (cartera, territorio, antigüedad)?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
