# Concepto de solución — NEG-02 · Open Finance: competir en un ecosistema financiero abierto

> **BORRADOR v1.1 (21.11.2026; cotejado con el expediente literal en `retos/NEG-02/expediente.md`).** Prioridad **#3** · Pareja líder **Antonio + Mariano** · Revisor **David** (pendiente) · Eje: 5 Open Finance y nuevos modelos de competencia · Owners (plataforma): Roger, Arturo.
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.
> El expediente no trae KPI ni línea base. Detalle de datos, arquitectura, plan del evento, medición y pruebas: `retos/NEG-02/panorama.md`.

## 1. Problema abordado

La información financiera de un cliente está distribuida entre varias instituciones, lo que dificulta una visión integral de su comportamiento, necesidades y oportunidades de atención. Open Finance permite compartirla **con su autorización y bajo las condiciones regulatorias aplicables**. La pregunta del reto es cómo aprovechar ese intercambio, seguro y autorizado, para dar **mayor valor a los clientes** y fortalecer la competitividad de Caja Trujillo en un ecosistema financiero cada vez más abierto.

Tres problemas concretos que atacamos:

1. **Visión parcial.** Con solo sus propios datos, la Caja no sabe si un cliente tiene deudas más caras en otra entidad, ahorro ocioso o ingresos que fluyen hacia otro lado, ni puede atender a quien aún no es su cliente. Pierde oportunidades de crecimiento e inclusión financiera. *(Cuánto ocurre en la práctica no lo sabemos; lo medimos en un sandbox.)*
2. **Riesgo de ofrecer mal.** Sin ver el endeudamiento en otras entidades, la Caja podría ofrecer crédito a quien ya está sobreendeudado. **(supuesto, hipótesis nuestra)**
3. **Confianza y seguridad.** Sin un consentimiento claro, verificable y revocable, y sin controles de acceso, usar datos de otras entidades es inviable. El expediente exige garantizar privacidad, seguridad y uso autorizado, y que el prototipo use **datos sintéticos e integraciones simuladas, «sin asumir disponibilidad de datos reales ni APIs operativas»**; además aclara que los datos son referenciales y que la Caja no se compromete a entregarlos.

## 2. Concepto de solución

**Asesor de oportunidades con consentimiento verificable.** Un sandbox de Open Finance (entidades, APIs y consentimientos **simulados**) sobre el que la Caja, en rol de receptora, arma una vista 360 del cliente que consintió y detecta oportunidades de producto, cada una **trazable al dato autorizado que la originó**. **(supuesto)**

Tres piezas, de adentro hacia afuera:

1. **Guardia de consentimiento.** Único camino hacia los datos de otras entidades. Aplica por código (no por interfaz) el alcance, la vigencia, la finalidad, el receptor y la ventana histórica de cada consentimiento, exige credencial a la entidad que consulta, audita cada acceso y proyecta solo las columnas autorizadas. Lo no autorizado **no llega** al motor ni al agente.
2. **Vista 360 y motor de oportunidades.** Une lo autorizado de varias entidades, estima el ingreso con un modelo predictivo entrenado sobre el ingreso declarado y las transacciones, calcula la capacidad de pago y detecta cuatro oportunidades (consolidación de deuda, capital de trabajo MYPE, captación de ahorro, domiciliación de ingresos) y una **abstención** (no ofrecer crédito si hay sobreendeudamiento). Cada resultado lleva su evidencia: entidad, campo, valor y consentimiento que lo autorizó.
3. **Agente.** Explica y redacta la propuesta para el ejecutivo con herramientas acotadas y verifica que cada cifra citada exista en la evidencia autorizada. **Propone; la decisión es siempre humana** y no se ejecuta ninguna acción crediticia automática.

**Diferenciación:**

- **Frente a la solución convencional** (ofertas con los datos propios de la Caja), la nuestra ve al cliente completo y atiende también a prospectos, pero solo con lo autorizado.
- **Cada recomendación se puede auditar hasta el dato y el consentimiento** que la autorizó.
- **El consentimiento se hace cumplir en el código y se prueba** con una batería adversarial (vencido, revocado, otro receptor, finalidad «solo vista», alcance insuficiente, ventana histórica); no es una casilla en la interfaz.
- **La visión multientidad también sirve para no ofrecer:** detecta sobreendeudamiento y se abstiene. Y le da al cliente una vista consolidada de su situación y ahorro potencial, no solo ofertas.
- **Experiencia de consentimiento clara** (alcance, vigencia y revocación comprensibles) porque, en el sandbox, el consentimiento —no el modelo— es el factor que más limita las oportunidades alcanzables.

**Fuera de alcance (no lo prometemos):** integración con APIs o datos reales, declaración de conformidad con algún estándar o norma de Open Finance, decisiones o scoring crediticio, el rol de la Caja como proveedora de datos y la **colaboración con otros actores del ecosistema** que menciona el expediente (hoja de ruta de escalabilidad), y autenticación real de usuarios finales. La seguridad que sí entra es la del sandbox: credencial por entidad receptora, auditoría y minimización.

## 3. Impacto esperado en el KPI

El expediente **no publica KPI ni línea base**. Candidatos **(supuesto, a validar con el owner)**:

- **KPI principal propuesto:** porcentaje de clientes con al menos una oportunidad de producto identificada y consentida.
- Completitud del perfil del cliente con y sin datos multientidad (conocimiento del cliente).
- **Inclusión financiera:** el mismo KPI principal medido sobre prospectos, es decir, personas y negocios que aún no son clientes de la Caja.
- **Beneficio para el cliente:** ahorro potencial de intereses en las consolidaciones identificadas, como escenario calculado con la evidencia (no como resultado).
- Ofertas de crédito indebidas (a clientes sobreendeudados): deben bajar con la visión multientidad.
- Conversión estimada de las ofertas personalizadas, solo como **escenario** con tasa de aceptación paramétrica **[POR CONFIRMAR con el owner]**; no se presenta como cifra única.
- Condición de calidad, no de optimización: **100 %** de recomendaciones con consentimiento vigente y linaje completo, y **cero fugas** en la batería adversarial.

- **Línea base:** **[POR CONFIRMAR con el owner]**. Mientras tanto usamos una línea base **metodológica**: el mismo motor con solo los datos de la Caja (brazo «Caja-solo»), que aísla el efecto de los datos multientidad.
- **Cifra de impacto esperada:** **[POR COMPLETAR cuando exista la línea base; no inventar]**.
- **Método de medición:** backtest sobre datos sintéticos con **tres brazos**: Caja-solo (base), 360 con los consentimientos del dataset (escenario realista, el resultado que se presenta) y 360 con consentimiento total (techo, solo para dimensionar el costo de no tener consentimiento). El brazo «Caja-solo» representa además la solución convencional frente a la cual el expediente pide valor diferencial. Se compara contra una verdad de terreno separada que la solución nunca ve; reproducible con semilla fija, con intervalos de confianza por *bootstrap* y sensibilidad a la tasa de consentimiento.
- **Qué mide y qué no:** valida el **mecanismo** (valor de la visión multientidad bajo control de consentimiento), no el impacto comercial real. Esa salvedad se declara en la presentación.

## 4. Enfoque tecnológico

Pila base: Python 3.11+, FastAPI, Pydantic v2, Pydantic AI, pandas, scikit-learn, SQLite, React + Vite + Tailwind, pytest.

Qué se construye y por qué no es un chatbot ni un panel:

- **Sandbox y APIs simuladas multientidad** (FastAPI) sobre datos sintéticos de 5 entidades ficticias y la Caja receptora.
- **Servicio de consentimiento y guardia por columna**, con credencial por entidad receptora, auditoría de accesos y denegaciones sin datos personales, y reloj parametrizable para que la demo y el KPI sean reproducibles.
- **Vista 360 con analítica predictiva:** modelo de ingreso estimado (scikit-learn, entrenado con el ingreso declarado de clientes de la Caja a partir de señales de transacciones), cuota total sobre ingreso, destino de los ingresos, completitud del perfil.
- **Motor de oportunidades** con reglas y umbrales explícitos sobre la estimación anterior; devuelve «no evaluable» cuando faltan datos autorizados en lugar de adivinar. *(Opcional si hay tiempo: modelo de propensión.)*
- **Agente con Pydantic AI:** herramientas de solo lectura, salida estructurada, **proveedor de LLM intercambiable** (`app/llm/provider.py`: plantilla determinista sin red por defecto, y Claude, OpenAI o modelo local) y verificación de la redacción contra la evidencia. La política de IA externa de la Caja es **[POR CONFIRMAR]**.
- **Interfaz** React: pantalla de consentimiento para el cliente y vista del ejecutivo con la oferta y su evidencia.
- **Pruebas y validación:** pruebas de la guardia, de fuga y de extremo a extremo, más el arnés de KPI (`scripts/evaluar_kpi.py`) y `docs/validacion.md`.

El expediente exige capacidades avanzadas con valor real, desarrollo funcional e integración tecnológica, y advierte que no basta con chatbots genéricos, dashboards, formularios o automatizaciones básicas, y pide desarrollo funcional, integración tecnológica y valor diferencial frente a soluciones convencionales. El valor diferencial es el control de consentimiento probado, la estimación predictiva sobre datos multientidad y el agente con evidencia verificable. **Riesgo declarado:** si falta tiempo, el modelo de ingreso y la redacción con LLM son lo primero que se recorta, y el producto quedaría más cerca de reglas con consentimiento (ver escenario pesimista en el panorama §4.4).

## 5. Tecnología preexistente

- Librerías de código abierto (FastAPI, Pydantic, pandas, scikit-learn, Pydantic AI, React, etc.) bajo sus licencias.
- **Generador de datos sintéticos NEG-02** (`retos/NEG-02/datos/generar.py` y sus 41 pruebas) y los CSV que produce en `retos/NEG-02/datos/sintetico/` (titularidad: equipo, 21.11.2026). Es solo una herramienta de datos: **no contiene** APIs, servicio de consentimiento, guardia, vista 360, motor de oportunidades, agente ni interfaz. Sus parámetros (catálogo, tasas, umbrales, probabilidades) son supuestos nuestros. Detalle en `retos/NEG-02/panorama.md` §8 y §10.
- Herramientas de planificación del equipo (`scripts/sinergia/`, `scripts/conceptos/`); no forman parte del producto.
- **No se reutiliza código de empleadores ni de otros clientes. No se usan datos reales.**

## 6. Funcionalidad crítica

**Flujo único de punta a punta:** un cliente otorga un consentimiento con alcance, vigencia y finalidad; la Caja consulta tres o más entidades simuladas **a través de la guardia**; se arma su vista 360; y el agente propone al ejecutivo ofertas (o una abstención) explicando qué dato, de qué entidad y bajo qué consentimiento las originó. Si el cliente **revoca**, la vista se reduce de inmediato. **(supuesto)**

Criterios de «funciona» (para el mínimo de 3/5 en la condición eliminatoria):

1. El cliente otorga y revoca consentimientos desde la interfaz; el estado (vigente, vencido, revocado) se calcula y audita.
2. La Caja obtiene datos de al menos 3 entidades solo dentro del alcance, la vigencia, la finalidad y la ventana consentidos, y con credencial de receptor; lo demás se deniega con motivo.
3. La vista 360 muestra el perfil y su completitud, con y sin datos multientidad.
4. Al menos 2 tipos de oferta con evidencia y consentimiento citados, **más** un caso de abstención por sobreendeudamiento.
5. La batería adversarial de la guardia pasa en verde (cero fugas).
6. El ejecutivo aprueba, edita o descarta; la decisión queda auditada; ninguna acción se ejecuta sola.
7. `evaluar_kpi.py` entrega el número antes/después de forma reproducible.

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia. Antes del evento solo existen el generador de datos, su auditoría de dificultad (`scripts/auditoria/auditar_neg02.py`) y la documentación.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso: *un cliente otorga consentimiento a la Caja sobre tres entidades simuladas, la Caja arma su perfil y el agente propone una oferta de consolidación explicando qué datos usó y bajo qué consentimiento; el cliente revoca una entidad y la propuesta desaparece; un segundo cliente sobreendeudado recibe una abstención.*

Incluye pruebas automáticas, reporte de validación (`docs/validacion.md`) y un número antes/después del KPI.

**Metas por día (plan en `retos/NEG-02/panorama.md` §4):** al cierre del día 1, consentimiento → consulta a 3 entidades → vista 360 funcionando y primer número del brazo base; el día 2 se completan motor con linaje, agente, interfaz de oportunidades, KPI de tres brazos y validación final antes de la entrega de las 13:00.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP (revisado):** **36 h-persona** con todo incluido (38 h en el v0, que sumaba 3 h de datos sintéticos que ahora son preexistentes) y **28 h-persona** en el **mínimo viable** **(supuesto)**. En el evento hay ~8 h por persona (32–34 h con 4 personas): el mínimo viable cabe con unas 6 h de reserva; el completo no cabe y se recorta por prioridad. **Prueba pesimista** (cada tarea ×1.4 y la ruta crítica ×1.6): el mínimo sube a 41 h, no cabe, y solo se sostiene con 9 recortes y sin holgura; el mínimo de 3/5 en funcionamiento queda en el límite (panorama §4.4).
- **Cobertura de habilidades del equipo:** 84 % **(supuesto; niveles de `team.json`)**. Sin brechas relevantes.
- **Brechas de la pareja líder** (cubre el resto del equipo): diseño de la experiencia de consentimiento (3 h estimadas en el v0; ahora 2 h a cargo de David con apoyo de Antonio).
- **Evidencia de factibilidad (preliminar; medida sobre nuestro generador, no sobre la Caja):** auditoría en `docs/investigacion/06-auditoria-datos.md`. Con las mismas reglas y distinta visibilidad, la Caja sola ve el 13 % de las oportunidades que existen, con los consentimientos del conjunto el 31 % y con información completa el 95 % (techo mecánico, porque la verdad se define con las mismas reglas). Conclusión de diseño: el consentimiento, no el modelo, limita lo alcanzable; la detección de sobreendeudamiento con ingreso estimado es el punto más débil (precisión 0.5–0.8) y se reportará con intervalos.
- **Dependencias:**
  - KPI y línea base **[POR CONFIRMAR]**.
  - Política de IA externa **[POR CONFIRMAR]**; sin respuesta, el producto funciona con plantilla determinista.
  - Datos o sandbox de la Caja: el expediente aclara que los datos son referenciales y sin compromiso de entrega, por lo que **nuestro generador es el caso base**; si la Caja comparte algo, se adapta al mismo esquema.
  - Marco normativo del consentimiento y validación del texto con Legal/Compliance **[POR CONFIRMAR]**.
- **Recorte si falta tiempo (en orden):** redacción con LLM → plantilla; interfaz a una sola página; sensibilidad y multi-semilla del KPI; menos entidades y ofertas. **No se recorta:** guardia de consentimiento, linaje de cada oferta, prueba de fuga con consentimientos vencidos/revocados y número antes/después.
- **Riesgos principales:** privacidad, seguridad y consentimiento mal aplicado, normativa no verificada (el expediente no la nombra), circularidad de los datos sintéticos, alcance excesivo para ~8 h y concentración de la ruta crítica (consentimiento → APIs → motor → agente) en una sola persona. Mitigaciones en `retos/NEG-02/panorama.md` §6.

---

## Anexo A. Tareas y horas (supuesto, revisado en v1)

Detalle de dueños, cronograma y recortes: `retos/NEG-02/panorama.md` §4.

| # | Tarea | Habilidad | Horas completo | Horas mínimo |
|---|---|---|---|---|
| T1 | Cargador de datos sintéticos al sandbox (los datos ya son preexistentes) | data_eng | 1.0 | 1.0 |
| T2 | Servicio de consentimiento, guardia por columna y auditoría | backend | 3.0 | 3.0 |
| T3 | APIs simuladas multientidad, con credencial por receptor | backend | 2.5 | 2.0 |
| T4 | Vista 360, modelo de ingreso estimado y completitud | data_sci | 3.5 | 3.0 |
| T5 | Motor de oportunidades con linaje (4 ofertas + 1 abstención) | agentes | 3.0 | 3.0 |
| T6 | Agente con proveedor de LLM intercambiable y redacción verificada | agentes / ia_gen | 2.5 | 1.0 |
| T7 | Diseño de la experiencia de consentimiento | ux | 2.0 | 1.5 |
| T8 | Interfaz de cliente, vista 360 y oportunidades | web | 5.0 | 3.0 |
| T9 | Catálogo, reglas de oferta responsable y textos | fin | 2.0 | 1.5 |
| T10 | Arnés de KPI de tres brazos | biz / data_sci | 3.0 | 2.0 |
| T11 | Pruebas y validación | qa | 4.0 | 3.0 |
| T12 | Pitch y demo | pitch | 2.5 | 2.0 |
| T13 | Integración y ensayo | todos | 2.0 | 2.0 |
| | **Total** | | **36.0** | **28.0** |

## Anexo B. Preguntas para el owner (de comprensión)

Son preguntas para entender el problema y su operación; **no piden datos** (la organización indicó que en esta etapa no los entrega).

- [ ] ¿Qué busca ganar la Caja con Open Finance: conocer mejor al cliente, captar clientes de otras entidades, retener, incluir? ¿Cuál pesa más y cómo mediría el éxito de una oferta (aceptación, monto colocado)?
- [ ] ¿Se imagina a la Caja solo como receptora de datos de otras entidades o también como proveedora?
- [ ] ¿Qué reglas de consentimiento (alcance, vigencia, finalidad, revocación) deben respetar las ofertas hechas con datos de terceros? ¿Legal y Compliance revisarían el texto?
- [ ] ¿Qué productos de la Caja podrían ofrecerse a partir de esta información y con qué condiciones generales?
- [ ] ¿Qué datos propios de la Caja pueden usarse para ofertas sin pedir un consentimiento adicional?
- [ ] ¿Qué controles de seguridad esperan ver (autenticación entre entidades, auditoría, cifrado, retención)?
- [ ] ¿Se espera conformidad con algún estándar de APIs abiertas o basta un entorno de prueba coherente que simule el intercambio?
- [ ] ¿Hay restricciones para usar IA externa (aun con datos sintéticos)?

Si la organización no responde, seguimos con los **supuestos marcados** en este documento y medimos el KPI con un backtest sobre datos sintéticos propios (el comunicado del 21.11 indica que en esta etapa no se entregan datos).

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
