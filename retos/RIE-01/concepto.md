# Concepto de solución — RIE-01 · Microfinanzas resilientes al clima

> **BORRADOR v1 (21.11.2026).** Prioridad **#4** · Pareja líder **Antonio + Mariano** · Revisor: Glem (pendiente) · Eje: 4 Inclusión financiera y resiliencia · Owner (plataforma): Miriam.
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.
> Detalle de datos, arquitectura, plan del evento y backtest: `retos/RIE-01/panorama.md`. Generador de datos sintéticos: `retos/RIE-01/datos/`.
> Nombre de trabajo de la solución: **Radar Climático de Cartera** **(supuesto)**.

## 1. Problema abordado

Pregunta de innovación del expediente: «¿Cómo podríamos anticipar los riesgos que los eventos climáticos representan para los negocios financiados por Caja Trujillo y desarrollar estrategias preventivas que fortalezcan su resiliencia?».

Según el expediente, los fenómenos climáticos (lluvias intensas, inundaciones o sequías) **pueden** afectar la actividad económica de los microempresarios, **especialmente los ubicados en zonas vulnerables o que desarrollan actividades sensibles al clima**. Pueden causar daños en infraestructura, pérdida de inventarios, dificultades de acceso a mercados e interrupciones de operaciones, y **potencialmente** afectar sus ingresos y su capacidad de pago. El desafío es anticipar y priorizar esos riesgos para que la Caja tome mejores decisiones y fortalezca la resiliencia de los negocios que financia. Resultado esperado: fortalecer la resiliencia de los clientes y de la cartera mediante la identificación anticipada de riesgos, facilitando decisiones preventivas que protejan la continuidad de los negocios y reduzcan posibles impactos financieros.

Lo que ocurre hoy en la práctica **[POR CONFIRMAR con el owner]**: el expediente no dice cómo identifica hoy la Caja la cartera expuesta ni qué hace cuando llega un evento. Nuestra lectura **(supuesto)**: se reacciona cuando aparece la mora, no antes.

El problema tiene tres partes que conviene no mezclar:

1. **Dónde está la cartera frente a cada amenaza**: no basta el distrito; dentro de un distrito la ribera de un río y una ladera de secano no sufren lo mismo.
2. **Quién pierde ingreso y quién puede pagar igual**: un arrozal y una bodega responden distinto, y un cliente con otros ingresos, seguro o reservas aguanta más.
3. **Qué hacer, a quién y con qué capacidad**: los gestores son pocos y las acciones cuestan.

Lo que el expediente pide respetar (sección «Riesgos»): considerar **la incertidumbre de los escenarios climáticos**; **evitar asumir que la exposición a una amenaza implica necesariamente pérdidas económicas o incumplimiento crediticio**; **sustentar las recomendaciones en evidencia**; y respetar **la protección de datos y las políticas de riesgo de Caja Trujillo**. Cada una tiene un mecanismo en el diseño (§2 y §6): rangos y eventos fuera de muestra; tres cifras separadas (expuesta, afectada, mora); evidencia trazable en cada recomendación; solo ids seudónimos y acciones del catálogo aprobado por la Caja **[POR CONFIRMAR: qué acciones permiten sus políticas de riesgo]**.

Dos criterios propios, no escritos en este expediente: la calidad imperfecta de los datos geográficos y climáticos (el expediente habla de datos «referenciales», sin compromiso de entrega) y la decisión humana (los expedientes RIE-02 y RIE-03 exigen revisión humana; el de RIE-01 no lo dice, pero lo adoptamos): la solución propone y el gestor decide; no genera decisiones crediticias automáticas. **(supuesto)**

## 2. Concepto de solución

**Radar Climático de Cartera** convierte un escenario climático en una lista corta de clientes y zonas donde conviene actuar antes del evento, con el rango de incertidumbre y la acción sugerida para cada caso. **(supuesto)**

Cómo funciona, de punta a punta:

1. El analista elige un **escenario ex ante** (tipo de amenaza × severidad, p. ej. «inundación severa en la costa norte»).
2. Un **modelo en tres capas** recalcula la cartera: *amenaza local* del sector del cliente → *vulnerabilidad* de su negocio (actividad, colchón financiero) → *impacto crediticio* (carga de deuda tras la caída de ingreso). Así separa **cartera expuesta**, **cartera probablemente afectada** y **mora incremental esperada**, cada una con rango (p10–p50–p90).
3. Un **mapa** muestra zonas y clientes; un **ranking** prioriza con las capacidades reales de cada agencia (visitas por semana), no solo por saldo.
4. Un **agente** propone, con evidencia, la acción preventiva de un catálogo, a nivel de cliente y también de zona o segmento (alerta, visita, reprogramación, ampliación de plazo, capital de reposición, asesoría de continuidad del negocio, derivación a microseguro **[POR CONFIRMAR] si existe**). Son las «estrategias preventivas» que pide el reto; el catálogo real **[POR CONFIRMAR]**. El gestor **aprueba o rechaza**; nada se ejecuta solo.
5. Un **backtest** mide, sobre eventos simulados con verdad conocida, cuánto mejora la identificación anticipada frente a reglas simples.

**Diferenciación** (por qué no es «un mapa de calor»):
- **Tres capas, tres números**: nunca presenta el saldo en zona de riesgo como si fuera pérdida.
- **Incertidumbre visible**: cada cifra viene con su rango; el modelo se evalúa contra eventos distintos del escenario ex ante, incluidos eventos más severos que la historia.
- **Resolución más fina que el distrito** cuando hay datos de sector o ubicación; cae a distrito si no los hay **[POR CONFIRMAR]**.
- **Del mapa a la acción con presupuesto**: optimiza qué hacer con los gestores disponibles y deja trazabilidad de la aprobación.
- **Evidencia medible** con baselines explícitas y ablaciones, en lugar de afirmar impacto.

**Principio de diseño:** la solución propone y explica; la decisión es siempre humana. El objetivo es **fortalecer la resiliencia del cliente y proteger la cartera**, no restringir crédito en zonas de riesgo. **(supuesto, revisar con Compliance)**

**Alcance frente a los mecanismos del expediente:** el expediente menciona daños en infraestructura, pérdida de inventarios, dificultades de acceso a mercados e interrupciones de operaciones. El modelo los resume en una sola variable, la **caída de ingreso del negocio**, que depende de actividad, amenaza local y colchón financiero. No modela por separado el acceso a mercados (vías, transporte) ni el daño a infraestructura. **(supuesto, declarado)**

## 3. Impacto esperado en el KPI

El expediente no publica KPI ni línea base. Los siguientes son **candidatos (supuesto, a validar con el owner)**, definidos para que se puedan medir sobre eventos con verdad conocida. Con `S_i` el saldo del cliente, `A_i` si resultó afectado, `M_i` si cayó en mora ≥ 30 días y `L` la lista priorizada ex ante:

| KPI candidato | Cómo se mide |
|---|---|
| **K1. Porcentaje de cartera afectada identificado anticipadamente por escenario** | `Σ_{i∈L} S_i·A_i / Σ_i S_i·A_i`, con una lista de tamaño limitado por la capacidad de gestores |
| **K2. Precisión de la priorización frente a eventos simulados** | Precisión@K y *lift* frente a la tasa base del evento; captura de saldo en mora `Σ_{i∈L} S_i·M_i / Σ_i S_i·M_i` |
| **K3. Pérdida esperada evitada con acciones preventivas (estimada)** | `Σ_{i∈L} S_i·M_i·LGD·efectividad − costo de acciones`, reportada como **rango**; depende de supuestos de efectividad y de LGD **[POR CONFIRMAR]** |
| **K4. Continuidad de los negocios afectados** (resiliencia del cliente, no solo de la cartera) | Entre los clientes afectados, % que se mantiene al día (no cae en mora ≥ 30 días), con y sin acciones; sale de `afectado` y `incumple_30d`. Responde al resultado esperado «proteger la continuidad de los negocios». Candidato nuestro |

- **Línea base:** **[POR CONFIRMAR con el owner]** (cómo se identifica hoy la cartera expuesta). Para el backtest se comparan **proxies nuestros**: azar, regla de zona (distritos de amenaza alta), regla de zona + actividad sensible y orden por saldo. No sustituyen la línea base oficial.
- **Cifra de impacto esperada:** **[POR COMPLETAR cuando exista la línea base; no inventar]**. No se promete un porcentaje.
- **Método de medición:** backtest sobre datos sintéticos, con y sin la solución, reproducible con semilla fija; seis eventos de prueba (lluvia, inundación y sequía, de leve a severa) con verdad oculta, calibración solo con eventos históricos, y réplica en varias semillas. Procedimiento completo en `retos/RIE-01/panorama.md` §e.
- **Qué mide y qué no:** el backtest sintético prueba la **mecánica** de identificar y priorizar, no el nivel de impacto en la Caja. Con datos reales se repetiría la calibración **[POR CONFIRMAR]**.
- **Criterio interno de aceptación (supuesto, no es meta de impacto; ajustado el 24.11 tras la auditoría de datos):** (1) superar a las reglas de zona (B1) y de saldo (B3) en captura de saldo en mora, al mismo presupuesto, en al menos 5 de 6 eventos; (2) no quedar por debajo de la regla de zona + actividad (B2) más allá del ruido entre semillas, porque esa regla ya captura buena parte de la señal; (3) un *lift* de al menos 2× sobre el azar con la capacidad real de visitas; y (4) que el rango p10–p90 cubra la mora total en al menos 4 de 6. Si no se cumple, se reporta tal cual. **Qué esperar:** la auditoría (`docs/investigacion/06-auditoria-datos.md`) mide que, con visitas de dos semanas (≈ 8 % de la cartera), el azar captura ≈ 8 % de los incumplimientos, una fórmula de tres factores ≈ 17.5 % y un modelo entrenado en la historia ≈ 19.6 %; el techo con la susceptibilidad real del sector es ≈ 24 %. El impacto demostrable es un *lift* moderado (≈ 2.5×), y la diferencia defendible frente a las reglas es la resolución de sector y la incertidumbre calibrada, no la precisión puntual.

## 4. Enfoque tecnológico

**Pila:** Python 3.11+, FastAPI, Pydantic v2, pandas, scikit-learn (SciPy para la asignación), SQLite, React + Vite + Tailwind, pytest, ruff.

**Dónde está la complejidad real.** El bloque «Complejidad tecnológica» de RIE-01 no se capturó **[POR CONFIRMAR en la plataforma]**; en RIE-02, RIE-03 y NEG-02 dice que no basta con chatbots genéricos, dashboards, formularios o automatizaciones básicas, y asumimos lo mismo aquí:

| Componente | Técnica | Por qué aporta valor |
|---|---|---|
| Amenaza local y vulnerabilidad | Modelo estadístico (regresión logística o árboles) calibrado con historia de eventos, validación **temporal** y calibración de probabilidades | Pasa de «zona de riesgo» a probabilidad de afectación por negocio |
| Escenarios con incertidumbre | Muestreo Monte Carlo de la severidad y propagación por zona | Entrega rangos, no una cifra única |
| Priorización | Asignación bajo capacidad de gestores y costo de acciones (voraz; programación entera si hay tiempo) | Convierte el ranking en un plan realizable |
| Agente de acciones | Pydantic AI con herramientas acotadas de solo lectura, salida validada con esquema y aprobación humana persistida; proveedor de LLM intercambiable en `app/llm/provider.py` (Claude, OpenAI, modelo local) y una variante **determinista** sin LLM | Explica y redacta con evidencia; la demo funciona aun sin IA externa |
| Backtest | Eventos simulados con verdad oculta, líneas base, ablaciones, réplica por semillas | Evidencia en lugar de promesas |

Lo que **no** es el núcleo: el mapa (visualización) ni el LLM (redacción). El valor está en el modelo, la incertidumbre y la asignación.

Hay un conjunto de datos sintéticos propio (distritos del norte del Perú, clientes MYPE, créditos en S/, mapa de amenaza con error, escenarios, historia y eventos de prueba). Si la Caja entrega datos o mapas, se sustituyen tablas sin cambiar el modelo. Las fuentes públicas de clima y amenaza (SENAMHI, CENEPRED/INDECI, ANA y otras) son una **ruta de sustitución [POR CONFIRMAR]**; hoy no se usa ninguna ni se descargó nada.

**Política de IA externa: [POR CONFIRMAR].** Al LLM solo llegan ids seudónimos y variables discretizadas, y el cálculo no depende de él.

## 5. Tecnología preexistente

Se declara en `docs/preexistente.md` (texto propuesto en `retos/RIE-01/panorama.md` §j):

- **Generador de datos sintéticos RIE-01** (`retos/RIE-01/datos/generar.py`) y sus **40 pruebas**, más los **CSV** que produce (`retos/RIE-01/datos/sintetico/`). Titular: equipo; creado el 21.11.2026; sin datos reales ni código de empleadores. Es una herramienta general: contiene los datos y un diagnóstico de calidad del dataset, pero **no** el modelo de exposición, los escenarios operativos, el mapa ni el agente.
- Librerías de código abierto (FastAPI, pandas, scikit-learn, SciPy, React, etc.) bajo sus licencias.
- Estructura del repositorio y herramientas de planificación del equipo (no forman parte del producto).
- **No se reutiliza código de empleadores ni de otros clientes. No se usan datos reales ni personales.** Los nombres de distritos son geografía pública con coordenadas aproximadas; los parámetros del mundo sintético son supuestos propios, no datos de la Caja.

Todo lo demás se **construye en el evento** (§6).

## 6. Funcionalidad crítica

**Un solo flujo de punta a punta:** *escenario ex ante → cartera expuesta / probablemente afectada / mora incremental con rango → mapa y ranking priorizado por zona y por cliente → plan de acciones sugerido por el agente → aprobación o rechazo del gestor → KPI con y sin la solución en el backtest.* Todo sin asumir que exposición equivale a incumplimiento. **(supuesto)**

**Criterios de aceptación** (lo que debe verse funcionando para sostener ≥ 3/5):
1. Cambiar de escenario recalcula la cartera y el mapa.
2. Las tres cifras (expuesta, afectada, mora incremental) se muestran separadas y con rango.
3. El ranking respeta la capacidad de visitas por agencia y muestra el motivo de cada cliente.
4. El agente propone solo acciones del catálogo, con evidencia y costo, y deja la propuesta «pendiente de aprobación»; el gestor decide y queda registro.
5. `scripts/evaluar_kpi.py` entrega la tabla con/sin en los seis eventos de prueba.
6. Pruebas automáticas pasan y `docs/validacion.md` recoge los resultados.

**Fuera de alcance** (para que quepa en ~8 h por persona): integración con el core de la Caja, envío real de mensajes, ejecución de acciones, pronóstico meteorológico propio, datos reales o descargados, autenticación y despliegue productivo.

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia. No se adelanta ninguna parte (modelo, escenarios, mapa, priorización, agente, API ni interfaz) antes del 03.12.

## 7. Nivel de desarrollo esperado

**Prototipo funcional de punta a punta** con un caso de uso para la demo (4–5 min):

1. Se muestra la cartera sintética y el *embudo* de los datos: de lo «expuesto» solo una fracción resulta afectada y menos aún entra en mora.
2. Se activa un escenario de inundación severa en la costa norte: el mapa muestra distritos y sectores, y la cartera expuesta, afectada y en riesgo de mora **con su rango**.
3. El ranking prioriza clientes dentro de la capacidad de visitas de cada agencia; la ficha explica el motivo.
4. El agente propone el plan; el gestor aprueba uno y rechaza otro.
5. Se cierra con el backtest: número **antes/después** del KPI frente a las reglas simples, incluido un evento más severo que cualquiera de la historia.

Incluye pruebas automáticas (ver `retos/RIE-01/panorama.md` §i), reporte de validación y un número antes/después del KPI. El número se obtendrá en el evento; hoy no existe y no se estima.

**Declaración de límites:** los resultados son sobre un mundo sintético y el nivel de impacto real depende de datos y acciones de la Caja **[POR CONFIRMAR]**.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP (revisado en v1):** **32 horas-persona** = 30,5 h de trabajo + 1,5 h de colchón **(supuesto)**. En el evento hay ~8 h por persona (32 h con 4 personas). Las horas por tarea cambian respecto al v0 porque el generador de datos ya existe (datos: 4 → 1,5 h) y esas horas se reinvierten en modelo, escenarios y backtest. Detalle en el Anexo A.
- **Reparto (4 × 8 h):** Mariano: API y agente. Glem: modelo y escenarios. Antonio: KPI, backtest, criterios financieros y caso de negocio. David: mapa, flujo del gestor y demo. Plan por bloques con tres hitos (13:00 y 16:30 del día 1; 17:30 de cierre de pruebas) en `retos/RIE-01/panorama.md` §d.
- **Cobertura de habilidades del equipo:** 83% (modelo de sinergia, con supuestos). Sin brechas relevantes.
- **Brechas de la pareja líder** (las cubre el resto del equipo): diseño del mapa y del flujo del gestor (2 h) → David.
- **Dependencias:** datos o mapas de la Caja (el expediente aclara que son referenciales y no implican compromiso de entrega: si no llegan, se usa el generador, ya listo); política de IA externa **[POR CONFIRMAR]** (hay variante determinista); KPI y línea base **[POR CONFIRMAR]**; catálogo real de acciones y su costo **[POR CONFIRMAR]**; si hay conexión a internet en el Hub para teselas de mapa y LLM externo (la demo no depende de ello).
- **Recorte si falta tiempo** (en orden): teselas ⇒ puntos en SVG (≈ 1,0 h); redacción con LLM ⇒ plantillas deterministas (≈ 2,0 h); Monte Carlo ⇒ rango analítico (≈ 1,0 h); asignación entera ⇒ voraz (≈ 0,5 h); sequía fuera de la demo (≈ 0,5 h); sector ⇒ solo distrito (≈ 1,5 h, último recurso). **Núcleo que no se recorta:** escenario → tres cifras con rango → ranking en mapa → plan con aprobación → backtest con un KPI frente a una línea base.
- **Riesgos principales:** confundir exposición con pérdida (tres capas y rangos); backtest circular (verdad oculta, eventos fuera de muestra, ablaciones y réplica por semillas); parámetros de acciones inventados (rangos y sensibilidad, validar con el owner). Tabla completa en el panorama §f.

---

## Anexo A. Tareas y horas (v1, supuesto)

| Tarea | Habilidad | Horas v0 | Horas v1 | Quién (propuesta) |
|---|---|---|---|---|
| Carga y validación de datos sintéticos (el generador es preexistente) | data_eng | 4 | 1,5 | Mariano · Glem |
| Modelo de amenaza local, vulnerabilidad e impacto | data_sci | 4 | 4,5 | Glem |
| Escenarios y propagación con incertidumbre | ml | 3 | 3,5 | Glem · Antonio |
| Mapa de riesgo interactivo | web | 4 | 4,0 | David |
| Diseño del mapa y del flujo del gestor | ux | 2 | 1,5 | David |
| Agente de acciones preventivas y proveedor de LLM | agentes | 3 | 3,5 | Mariano |
| API y persistencia | backend | 3 | 2,5 | Mariano |
| Backtest, impacto en cartera y KPI | biz | 3 | 4,0 | Antonio |
| Criterios de riesgo y financieros (Caja Experts) | fin | 2 | 1,0 | Antonio |
| Pruebas y validación | qa | 2 | 2,5 | Glem · Mariano · Antonio |
| Pitch y demo | pitch | 2 | 2,0 | David · Antonio |
| Colchón | — | — | 1,5 | Mariano · David |
| **Total** | | **32** | **32** | |

## Anexo B. Preguntas para el owner (de comprensión)

Son preguntas para entender el problema y su operación; **no piden datos** (la organización indicó que en esta etapa no los entrega).

- [ ] ¿Cómo mide y gestiona hoy la Caja el riesgo por eventos climáticos (El Niño, lluvias, sequías)? ¿Qué pérdida o mora se les atribuye y quién la calcula?
- [ ] ¿Qué acciones preventivas son viables (alerta, visita, reprogramación, ampliación de plazo, capital de reposición, microseguro) y cuáles requieren comité o normativa? ¿Qué implica una reprogramación preventiva para la calificación?
- [ ] ¿Cuántos gestores hay por agencia y cuántas visitas por semana son realistas ante una emergencia?
- [ ] ¿Qué sabe hoy la Caja de sus clientes que ayude a medir su exposición (ubicación, actividad, seguro, ingresos secundarios, reservas)?
- [ ] ¿Se puede usar información pública de clima y mapas de amenaza como referencia?
- [ ] ¿Cuál es el resultado principal que esperan: mora evitada, exposición identificada a tiempo, clientes contactados antes del evento?
- [ ] ¿Dónde vería el gestor la alerta hoy y con qué anticipación sirve?
- [ ] ¿Hay restricciones para usar IA externa (aun con datos sintéticos)? ¿Cuál es el formato exacto de la postulación y la hora límite del 26.11?

Si la organización no responde, seguimos con los **supuestos marcados** en este documento y medimos el KPI con un backtest sobre datos sintéticos propios (el comunicado del 21.11 indica que en esta etapa no se entregan datos).

## Anexo C. Lista de revisión (criterios del pase a finalistas)

> Pendiente de revisión por alguien que no lo escribió (Glem). Autor: sesión de apoyo con Antonio y Mariano como pareja líder. No marcar sin revisión.

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.

Puntos que el revisor debería mirar con especial atención:
1. El problema (§1) ya se cotejó con `retos/RIE-01/expediente.md` (ver «Cotejo con el expediente» al final del panorama). Falta confirmar el bloque «Complejidad tecnológica», no capturado.
2. ¿Los KPI K1–K4 son los que pediría el owner? Son candidatos nuestros.
3. ¿La separación en tres capas (expuesta, afectada, mora) se entiende sin explicación oral?
4. ¿Las 32 h son realistas? El generador reduce la tarea de datos; modelo y backtest suben.
