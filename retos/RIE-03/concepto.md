# Concepto de solución — RIE-03 · Anticipar el deterioro de pago antes del atraso

> **v1 (pareja líder, 21.11.2026).** Prioridad **#1** · Pareja líder **David + Mariano** · Revisor **Glem** · Eje: 3 Riesgo, fraude y recuperaciones inteligentes · Owners (plataforma): Wilson, Harold, Paul.
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.
> Detalle de datos, arquitectura, plan del evento y backtest: `retos/RIE-03/panorama.md`.

## 1. Problema abordado

Según el expediente, la situación económica de un microempresario puede deteriorarse **gradualmente** antes de que se produzca un atraso (cambios en sus ingresos, actividad comercial, necesidades de financiamiento u otras circunstancias), y algunas señales tempranas pueden identificarse con información histórica, comportamiento financiero y variaciones en sus patrones habituales. Pero no toda variación es un riesgo real: hay que distinguir señales relevantes de fluctuaciones normales, evitando alertas innecesarias y decisiones basadas en información insuficiente.

Nuestra lectura **(supuesto, a validar con el owner)**: sin una herramienta que haga esa distinción, se cae en dos errores opuestos: **intervenciones tardías**, cuando el cliente ya está en mora, y **alertas innecesarias**, que cansan al gestor y desgastan la relación con el cliente.

El expediente pide gestión **preventiva**: priorizar oportunidades de intervención y generar información confiable para actuar a tiempo, con el fin de reducir incumplimientos, mejorar la calidad de la cartera y preservar la salud financiera de los microempresarios. Fija cinco límites que respetamos:

- **Protección de datos personales:** el diseño minimiza y seudonimiza los datos (ver §4).
- **Sesgos:** se evitan y se auditan por grupo; no se asumen ausentes.
- **Incertidumbre de las predicciones:** toda alerta muestra su grado de incertidumbre; con información insuficiente no se alerta.
- **Alertas sustentadas en evidencia, con mínimos falsos positivos y revisión humana:** una alerta sin evidencia no entra a la cola.
- **Sin decisiones crediticias automáticas que afecten a los clientes:** la alerta no cambia calificación, condiciones, límites ni tasa de nadie.

## 2. Concepto de solución

**Alerta temprana explicada con plan de intervención y aprobación humana.** Cada día el sistema entrega al gestor una cola corta de clientes con riesgo de deterioro, cada uno con el porqué y con una acción preventiva propuesta. El gestor decide. **(supuesto)**

Tres piezas, de adentro hacia afuera:

1. **Modelo de deterioro.** Estima, para cada cliente al día, la probabilidad calibrada de pasar a atraso dentro de un horizonte, a partir del historial de pagos, la evolución de saldos, la actividad económica y variables de riesgo. Cada probabilidad lleva un **rango de incertidumbre**; los clientes con historial insuficiente no se alertan y quedan marcados «sin información suficiente».
2. **Separador de señal y fluctuación.** Una alerta solo entra a la cola si la caída es **persistente**, se aparta de lo **estacional** (mismo mes del año anterior y cohorte del sector) y **converge** en al menos dos familias de señales (ingreso, conducta de pago, endeudamiento externo). Este filtro es el control de falsos positivos del expediente.
3. **Agente de intervención.** Para cada alerta de la cola propone canal, momento y propuesta, y redacta un borrador de mensaje que cita la evidencia. Está acotado por reglas en código: no promete condiciones crediticias, usa solo canales viables para ese cliente y deja siempre la decisión al gestor.

**Diferenciación:** no entregamos solo un puntaje de mora. Entregamos una **acción explicada** y **medimos su costo en falsos positivos** frente a reglas simples, algo que un modelo clásico de probabilidad de mora no muestra.

**Principio de diseño:** la solución propone y explica; la decisión final es siempre humana. Ningún endpoint envía mensajes ni ejecuta acciones crediticias, y la alerta es solo para gestión preventiva: no alimenta calificación, límites, tasas ni condiciones del cliente.

## 3. Impacto esperado en el KPI

El expediente no publica KPI ni línea base. Candidatos **(supuesto, a validar con el owner)**:

| | KPI | Cómo se mide |
|---|---|---|
| **Principal (propuesto)** | Tasa de paso a atraso > 30 días de la cartera alertada, con y sin intervención | Backtest sobre datos sintéticos; la intervención entra como parámetro de escenario |
| Secundario | Precisión en el top-k y tasa de falsos positivos, incluida la que cae sobre fluctuaciones normales | Backtest, frente a reglas simples |
| Secundario | Días de anticipación frente al primer atraso | Backtest |

- **Línea base:** **[POR CONFIRMAR con el owner]** (morosidad actual, umbral de mora de 8 o 30 días, horizonte útil). Mientras tanto, la comparación interna es contra la **política reactiva actual simulada** (se gestiona después del vencimiento) y contra reglas simples de una señal. Esa comparación es solo de demo y no sustituye a la línea base oficial.
- **Cifra de impacto esperada:** **[POR COMPLETAR]** cuando exista la línea base. No se inventa.
- **Método de medición:** backtest temporal con semilla fija, con y sin la solución. Los datos sintéticos **no contienen ninguna intervención**; por eso el efecto de actuar a tiempo se muestra como **tabla de sensibilidad** y no como un hecho. Lo que sí se mide como hecho (sobre datos sintéticos): cuántos casos se detectan, con cuántos días de anticipación y con qué falsos positivos.

## 4. Enfoque tecnológico

Pila: Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn (LightGBM solo si aporta), SQLite, Pydantic AI, React + Vite + Tailwind, pytest.

| Capa | Qué hace | Aporta valor real porque… |
|---|---|---|
| Datos | Carga la cartera sintética y calcula variables **as-of** (solo información ≤ fecha de corte) | Evita fugas del futuro; el mismo código sirve a la API y al backtest |
| Modelo | Clasificador calibrado con validación temporal (logística como base, GBM si mejora) y rango de incertidumbre por alerta (método a definir en el evento, p. ej. remuestreo) | Probabilidades interpretables, con incertidumbre explícita, comparables con reglas simples |
| Privacidad y equidad | Seudonimización y minimización: el agente y la bitácora ven solo identificadores y señales numéricas, nunca datos personales; sexo, edad y zona se usan solo para auditar sesgos, no como variables del modelo | Cumple la protección de datos y permite medir sesgos sin entrenar con ellos |
| Señal vs. fluctuación | Persistencia, contraste estacional, convergencia de familias, tope por gestor y enfriamiento | Es el control explícito de falsos positivos y de fatiga |
| Agente | Pydantic AI sobre un proveedor de LLM intercambiable (`app/llm/provider.py`: Claude, OpenAI, modelo local o plantillas sin red) | La lógica no depende de la nube; si la política de IA externa la prohíbe, la demo corre igual |
| API | FastAPI: cola, caso, decisión con bitácora, resultado del backtest | Trazabilidad de cada decisión humana |
| Interfaz | React: cola priorizada → caso con señales → aprobar, editar o descartar | El gestor ve el porqué antes de actuar |
| Backtest | `scripts/evaluar_kpi.py`: con y sin la solución, frente a reglas simples | Entrega el número antes/después |

No es un chatbot genérico, un dashboard, un formulario ni una automatización básica: el valor está en el modelo calibrado, el filtro de señal y el agente acotado, **integrados de punta a punta** (datos → modelo → agente → API → interfaz) y evaluados con un backtest propio. La diferencia frente a una solución convencional (reglas de días de atraso, o un puntaje de mora sin explicación) se mide en ese backtest.

## 5. Tecnología preexistente

- **Generador de datos sintéticos de RIE-03** (`retos/RIE-03/datos/`, con 24 pruebas) y su **salida** (`retos/RIE-03/datos/sintetico/`: 5,000 clientes, 34 meses, 9 tablas CSV). 100 % ficticia, reproducible con semilla. Titular: el equipo. Creado el 21.11.2026. Detalle y texto para `docs/preexistente.md` en `retos/RIE-03/panorama.md` §(j).
- Herramientas de planificación del equipo (`scripts/sinergia/`, `scripts/conceptos/`). No forman parte del producto.
- Librerías de código abierto (FastAPI, Pydantic, pandas, scikit-learn, React, etc.) bajo sus licencias.
- **No se reutiliza código de empleadores ni de otros clientes. No se usan datos reales.**
- **No es preexistente, y se construye en el evento:** ETL y variables, modelo, separador señal/fluctuación, agente y guardas, API, interfaz y backtest.

## 6. Funcionalidad crítica

**Cola diaria preventiva con explicación y acción propuesta, con aprobación humana.** Dada una fecha de corte, el sistema:

1. calcula el riesgo de deterioro de cada crédito vigente al día usando solo información hasta esa fecha;
2. entrega una cola priorizada de **k clientes** (k según la capacidad del gestor, **[POR CONFIRMAR]**), ya filtrada por persistencia, estacionalidad y convergencia de señales;
3. muestra por cada cliente **2–3 señales** contrastadas con su propio historial y con su sector, y el **rango de incertidumbre** del puntaje; los créditos con información insuficiente no se alertan y aparecen marcados;
4. propone una **intervención** (canal, momento, propuesta y borrador de mensaje con la evidencia citada);
5. permite al gestor **aprobar, editar o descartar**, y deja bitácora. Nada se ejecuta de forma automática. **(supuesto)**

**Criterios de aceptación** (verificables con pruebas, y base del mínimo 3/5):

- Con la misma fecha y los mismos datos, la cola es idéntica (semilla fija) y no usa información posterior a la fecha de corte.
- Un cliente con una caída de ingreso de un solo mes, recuperada y propia de su estacionalidad, **no** entra a la cola; un cliente con deterioro gradual persistente **sí**.
- Toda recomendación cita evidencia existente y un canal viable para ese cliente, y nunca promete condiciones crediticias.
- Ningún endpoint envía ni ejecuta nada; toda acción queda en bitácora con la decisión del gestor. La alerta no modifica calificación, condiciones, límites ni tasa del cliente.
- Toda alerta muestra su incertidumbre; un crédito con historial insuficiente no genera alerta.
- Lo que ve el agente y lo que se guarda no contiene datos personales; sexo y edad no entran al modelo.
- El backtest muestra, con y sin la solución, precisión, falsos positivos, anticipación y el efecto escenario sobre el KPI.

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

**Prototipo funcional de punta a punta con caso de uso**, sobre una cartera sintética de miles de clientes (5,000 en la base; hasta 15,000 si hace falta más muestra). Demo guionada: se abre la cola del día; se entra a un cliente con deterioro gradual y se ve el porqué (qué cae, desde cuándo, frente a su estacionalidad); se aprueba la acción propuesta; se muestra un cliente con fluctuación normal que **no** alertó; y se cierra con el backtest con y sin la solución.

Incluye pruebas automáticas, reporte de validación (`docs/validacion.md`), auditoría de sesgos por grupo y un número antes/después del KPI.

**Fuera de alcance** (para no prometer de más): envío real de mensajes, integración con sistemas de la Caja, decisiones o condiciones crediticias, recalibración continua en producción.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP (revisado): 31.5 horas-persona** **(supuesto)**, de 32 disponibles (4 personas × ~8 h netas). Núcleo no recortable: 26 h; el resto (flujo de diseño, reglas de dominio, pitch) suma 5.5 h. Plan hora a hora y recortes en `retos/RIE-03/panorama.md` §(d). **Prueba pesimista** (cada tarea ×1.4; agente e integración ×1.6): 45.3 h; solo con nueve recortes baja a 31.7 h, es decir, sin holgura. El mínimo viable resultante conserva una funcionalidad crítica de punta a punta, pero el riesgo de no alcanzar el 3/5 es real si un bloque se desvía más; por eso el mínimo viable se toma como plan base.
- **Ventaja de arranque:** el generador de datos ya existe y está probado, lo que quita ~3 h al MVP. El resto de la funcionalidad crítica parte de cero el 03.12.
- **Cobertura de habilidades del equipo:** 85 % **(supuesto)**. Brecha de la pareja líder: señales relevantes vs. fluctuación normal en el dominio financiero (2 h), que cubre Antonio (único con experiencia en el sector) con apoyo de los Caja Experts.
- **Dependencias:**
  - Datos sintéticos de la Caja: el expediente los llama «referenciales» y aclara que no hay compromiso de entrega. Si no llegan o llegan tarde, usamos nuestro generador; si llegan, se mapean al mismo esquema.
  - Política de IA externa **[POR CONFIRMAR]**; el proveedor es intercambiable y existe un modo sin red.
  - KPI, línea base y definición de atraso (8 o 30 días) **[POR CONFIRMAR]**.
  - Capacidad de gestión por analista (define k) **[POR CONFIRMAR]**.
- **Riesgos principales:** pocos positivos en datos sintéticos (mitigado con más clientes y bootstrap), falsos positivos (filtro de señal y métrica explícita), fuga del futuro (funciones as-of y prueba de no-fuga) y que el jurado cuestione el efecto de la intervención (se presenta como escenario).
- **Recorte si falta tiempo** (en orden): agente sobre plantillas con LLM solo para el borrador → solo regresión logística → UI más simple → auditoría de sesgos reducida a un cuadro. **No se recorta:** cola, explicación, aprobación humana con bitácora, backtest con y sin la solución, y pruebas.

---

## Anexo A. Tareas y horas (supuesto, revisadas)

| Tarea | Habilidad | Horas |
|---|---|---|
| ETL a SQLite y variables as-of (el generador ya existe) | data_eng | 2 |
| Modelo de deterioro y calibración | ml | 4 |
| Explicabilidad, separador de señal y control de falsos positivos | data_sci | 3 |
| Agente de intervención y guardas (con respaldo por plantillas) | agentes | 3 |
| API y persistencia | backend | 3 |
| Interfaz: cola y caso con aprobar / editar / descartar | web | 4 |
| KPI, backtest y comparación con reglas simples | biz | 4 |
| Pruebas y validación | qa | 3 |
| **Núcleo** | | **26** |
| Diseño del flujo del gestor y explicación de alertas | ux | 1.5 |
| Señales relevantes vs. fluctuación normal; caso de negocio | fin | 2 |
| Pitch y demo | pitch | 2 |
| **Total** | | **31.5** |

(v0: 33 h. El generador pasa a ser preexistente; se suma tiempo a backtest y pruebas.)

## Anexo B. Preguntas para el owner (de comprensión)

Son preguntas para entender el problema y su operación; **no piden datos** (la organización indicó que en esta etapa no los entrega).

- [ ] ¿Cómo define hoy la Caja el «deterioro» de un cliente MYPE y en qué momento se entera (días de atraso, calificación, visita)? ¿Con cuánta anticipación sería útil avisar: 30, 60 o 90 días?
- [ ] ¿Qué señales siguen hoy los analistas para sospechar que un cliente empeora, y cada cuánto las revisan?
- [ ] ¿Cómo se mide hoy la morosidad y la recuperación (mora > 8 días, > 30 días, cartera en riesgo)? ¿Cuál de esas medidas es la prioritaria para este desafío?
- [ ] ¿Cuántos clientes gestiona un analista al día y cuántos contactos preventivos son razonables sin saturar al cliente?
- [ ] ¿Qué puede ofrecer el analista por su cuenta (recordatorio, reprogramación, asesoría) y qué requiere comité? ¿Qué canales de contacto son aceptables?
- [ ] ¿En qué herramienta trabaja hoy el analista y dónde debería aparecer la alerta?
- [ ] ¿Qué esperan ver en la explicación de una alerta para confiar en ella?
- [ ] ¿Hay restricciones para usar IA externa (aun con datos sintéticos) o variables que no deben usarse por criterios de equidad?

Si la organización no responde, seguimos con los **supuestos marcados** en este documento y medimos el KPI con un backtest sobre datos sintéticos propios (el comunicado del 21.11 indica que en esta etapa no se entregan datos).

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
