# Concepto de solución — RIE-02 · Descubrir redes de riesgo ocultas

> **BORRADOR v1.1 (21.11.2026, corregido tras cotejar con el expediente literal).** Prioridad **#5** · Pareja líder **David + Mariano** · Revisor: Antonio · Eje: 3 Riesgo, fraude y recuperaciones inteligentes · Owner (plataforma): Carlos.
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.
> Expediente literal: `retos/RIE-02/expediente.md`. Datos, arquitectura, plan del evento, medición y cotejo: `retos/RIE-02/panorama.md`. Texto para pegar en la plataforma: `retos/RIE-02/postulacion.md`.

## 1. Problema abordado

Pregunta de innovación del expediente: ¿cómo identificar patrones de relaciones inusuales entre personas, negocios y solicitudes de crédito que permitan anticipar posibles riesgos de fraude y orientar acciones de prevención e investigación?

Texto del expediente: «Algunas modalidades de fraude financiero pueden involucrar múltiples personas, negocios o solicitudes de crédito que, evaluadas individualmente, no presentan señales evidentes de irregularidad.» Las conexiones entre teléfonos, dispositivos, direcciones, referencias, contactos o negocios pueden revelar patrones inusuales, pero compartir información o mantener vínculos no implica necesariamente una conducta fraudulenta: el desafío está en distinguir relaciones legítimas de patrones que realmente merecen una revisión.

Restricciones del expediente: respetar la protección de datos personales; **evitar conclusiones automáticas de fraude basadas únicamente en relaciones o coincidencias**; sustentar las alertas en evidencia verificable; considerar posibles falsos positivos; y **facilitar la revisión humana antes de tomar decisiones que afecten a los clientes**.

**La tensión que resolvemos (supuesto):** quien revisa solicitud por solicitud no ve la red; quien alerta por cada dato compartido inunda al especialista y señala a clientes legítimos, porque los hogares, los puestos de un mercado, un gremio o un contador que atiende a muchos clientes también comparten teléfonos, direcciones o referencias. Cómo se revisa hoy y con qué reglas **[POR CONFIRMAR con el owner]**.

## 2. Concepto de solución

**Mesa del especialista de redes** (el expediente habla de «especialistas de Caja Trujillo» en prevención e investigación; quién es exactamente **[POR CONFIRMAR]**): convierte un lote de solicitudes en un grafo de personas, negocios, teléfonos, dispositivos, direcciones y referencias; encuentra los grupos de solicitudes conectados de forma inusual; los ordena por prioridad; y entrega un **expediente con evidencia citada fila por fila y con las explicaciones legítimas posibles**, junto con una acción sugerida de **prevención** (pedir verificación antes del desembolso) o de **investigación** (escalar). **(supuesto)**

Cuatro ideas:

1. **El peso de un vínculo depende de lo raro que es.** Un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia, un puesto de mercado o un hogar con cuatro miembros pesan poco.
2. **Las relaciones solas no bastan (regla de corroboración).** Una red solo se prioriza si combina señales de **estructura** (varios vínculos de tipos distintos) y de **comportamiento o perfil** (ráfaga de solicitudes, montos, antigüedad de negocios y líneas). Una familia, un mercado o un gremio tienen estructura pero no comportamiento anómalo, y no suben. Así se cumple el «evitar conclusiones automáticas basadas únicamente en relaciones o coincidencias».
3. **Cada alerta muestra su contrapartida legítima:** parentesco aparente, mercado, gremio, gestor.
4. **Un agente redacta el expediente, pero no decide.** Solo usa herramientas de lectura; un verificador rechaza citas que no existan y frases que concluyan fraude.

**Diferenciación:** evidencia verificable y control de falsos positivos para distinguir relaciones legítimas de patrones sospechosos, medido contra reglas simples y contra una regla con criterio de dominio, sobre redes inyectadas y señuelos legítimos.

**Principio de diseño:** la solución propone y explica; **ninguna acción que afecte a un cliente se ejecuta sin revisión humana**. El sistema no cambia el estado de una solicitud, no bloquea ni notifica: registra la decisión del especialista con su motivo. La alerta dice «patrón que merece revisión», nunca «fraude».

## 3. Impacto esperado en el KPI

El expediente no publica KPI ni línea base. Su resultado esperado: mejorar la capacidad de **priorizar investigaciones, reducir falsos positivos** y orientar decisiones sustentadas en evidencia, con **detección temprana**. KPI candidatos **(supuesto, a validar con el owner)**:

- **Precisión y recall sobre redes de fraude inyectadas** en datos sintéticos (a nivel de red y de solicitud).
- **Reducción de falsos positivos frente a reglas simples**, comparada con el mismo recall, y también frente a una regla con criterio de dominio.
- **Calidad de la cola de priorización:** precisión y recall sobre las primeras K alertas. Opcional: oportunidad de detección (qué parte de la red había ingresado cuando se alertó).
- Candidato nuestro, no del expediente: tiempo de preparación de un caso (simulación propia).

- **Línea base:** [POR CONFIRMAR con el owner]. Si la Caja entrega sus reglas actuales, esas serán la línea base; mientras tanto se compara contra reglas de coincidencia que definimos nosotros.
- **Cifra de impacto esperada:** [POR COMPLETAR cuando exista la línea base; no inventar]. No se afirmará ninguna tasa real de fraude ni ahorro en la Caja.
- **Método de medición:** backtest sobre datos sintéticos con verdad de terreno, reproducible con semilla fija. Se afina solo con la partición de desarrollo, se congelan umbrales y se evalúa una vez en la partición de evaluación y en semillas ciegas, con intervalos de confianza por remuestreo de redes y resultados por patrón y dificultad. Una ablación mide el efecto de la regla de corroboración. Procedimiento completo: `retos/RIE-02/panorama.md` §e.

## 4. Enfoque tecnológico

Flujo de punta a punta: **lote de solicitudes → grafo tipado con pesos → comunidades e indicadores → regla de corroboración y priorización con razones → agente de expediente con citas verificadas → vista del especialista → decisión humana registrada.**

| Pieza | Qué hace | Con qué |
|---|---|---|
| Grafo tipado | Nodos: solicitud, persona, negocio, teléfono, dispositivo, dirección. Vínculos por teléfono, dispositivo, domicilio, local de negocio, referencia y contacto de referencia. Pesos por rareza y por capacidad esperada del inmueble o dispositivo | pandas, networkx |
| Comunidades y anomalías | Componentes tras podar vínculos débiles, Louvain en componentes grandes y puntaje de cadenas de vínculos débiles de tipos distintos | networkx, scikit-learn |
| Indicadores de red | Estructura (ciclos de referencias, tipos de vínculo, exceso de personas sobre la capacidad del inmueble); comportamiento y perfil (ventana temporal, antigüedad de negocios y líneas, clientes nuevos, montos cercanos a un umbral **(supuesto)**); factores legítimos (parentesco, mercado, tableta, gestor) | pandas |
| Corroboración y priorización | Puntaje 0–100 con la contribución de cada factor, a favor y en contra, solo si hay estructura **y** comportamiento. Empieza con reglas ponderadas explicables; modelo ligero si da tiempo | scikit-learn |
| Agente de expediente | Resumen con hechos citados, vínculos fuertes frente a débiles, explicaciones alternativas, qué verificar, nivel de confianza; verificador determinista y plantilla de respaldo sin LLM | Pydantic AI; `app/llm/provider.py` intercambiable (Claude, OpenAI, modelo local o plantilla) |
| Vista del especialista | Cola priorizada, grafo, panel de evidencia y tres acciones con motivo: Escalar a investigación, Pedir verificación preventiva, Descartar como legítima | React + Vite + Tailwind + Cytoscape.js |
| API y auditoría | Redes, expediente y decisiones | FastAPI, Pydantic v2, SQLite |
| Medición | Backtest contra reglas simples y contra una regla de dominio, con y sin la solución | `scripts/evaluar_kpi.py`, pytest |

**Integración tecnológica que se demuestra:** ETL → grafo → priorización → agente → API → interfaz, con proveedor de LLM intercambiable y un adaptador para cargar los datos que entregue la Caja. **Valor diferencial** frente a lo convencional: reglas simples de coincidencia (medidas) y la regla de corroboración; no un dashboard ni un chatbot. El proveedor de LLM es intercambiable porque la política de IA externa está **[POR CONFIRMAR]**; al LLM solo irían ids y atributos seudonimizados, y la plantilla sin red es el valor por defecto.

## 5. Tecnología preexistente

- **Generador de datos sintéticos RIE-02** (`retos/RIE-02/datos/generar.py` y sus 37 pruebas) y los datos que produce (`retos/RIE-02/datos/sintetico/`, semilla 2026): solicitudes ficticias con su grafo, 5 patrones de fraude inyectados, 6 tipos de relaciones legítimas y verdad de terreno. Titularidad: equipo, creado el 21.11.2026. **No contiene el detector, la priorización ni el agente.** Las pruebas incluyen reglas de control solo para comprobar que el dataset no es trivial.
- Repo base y estructura de carpetas; este concepto y el panorama (`retos/RIE-02/panorama.md`) como documentación. Un esqueleto genérico de frontend sin lógica de dominio, **solo si el equipo lo aprueba**, declarado como preexistente.
- Librerías de código abierto bajo sus licencias: FastAPI, Pydantic v2 y Pydantic AI, pandas, numpy, networkx, scikit-learn, React, Vite, Tailwind, Cytoscape.js, pytest.
- **No se reutiliza código de empleadores ni de otros clientes. No se usan datos reales.** Se declara en `docs/preexistente.md`.

Todo lo demás se construye en el evento: ETL y grafo, comunidades e indicadores, regla de corroboración, priorización, agente y verificador, `app/llm/provider.py`, API, interfaz y backtest.

## 6. Funcionalidad crítica

**Un lote de solicitudes entra y sale con las redes de riesgo priorizadas, cada una con su expediente de evidencia citada, sus explicaciones legítimas y una acción sugerida de prevención o investigación, y con la decisión del especialista registrada.** **(supuesto)**

Debe funcionar de punta a punta sobre el lote sintético y cumplir cuatro condiciones medibles:

1. Detecta redes de fraude inyectadas, incluidas las de vínculos débiles encadenados, mejor que las reglas simples.
2. **No prioriza** (o lo hace con puntaje bajo y razón visible) familias, mercados, tabletas de agencia, gremios y gestores legítimos.
3. **Nunca alerta solo por relaciones o coincidencias:** exige corroboración de comportamiento o perfil; el expediente cita solo filas que existen y nunca concluye fraude.
4. Ninguna acción sobre el cliente sin decisión humana registrada con motivo.

Fuera de la funcionalidad crítica: integración con sistemas reales de la Caja, bloqueo de operaciones, reentrenamiento en línea, resolución de entidades (se asume hecha), conexiones (IP) y geolocalización (el dataset no las trae).

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia; **no se adelanta antes del 03.12**.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta con caso de uso. Demo (≤ 5 min):

1. Se carga el lote (≈ 3,700 solicitudes **(supuesto de volumen)**). La cola muestra las redes priorizadas.
2. Se abre una red de vínculos encadenados que ninguna regla simple vería: el grafo la resalta y el agente arma el expediente con citas y alternativas legítimas.
3. Se abre un **señuelo** (una familia o un puesto de mercado) con el mismo dato compartido: el sistema lo baja de prioridad y lo explica.
4. El especialista decide («Escalar», «Pedir verificación» o «Descartar») con motivo; queda registrado y el cliente no recibe nada.
5. Pantalla final **antes/después**: reglas simples frente a la solución en la evaluación ciega (precisión y recall de redes, falsos positivos sobre señuelos, carga de revisión). Los valores se miden el Día 2; no se inventan antes.

Incluye pruebas automáticas, reporte de validación (`docs/validacion.md`) y un número antes/después del KPI. Alcance en una página: `retos/RIE-02/panorama.md`.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP: 29 horas-persona (supuesto)**, frente a 36 en v0, porque los datos sintéticos ya existen y se usan networkx y Cytoscape.js. Disponible: ~7.5 h de construcción más ~1 h de pruebas por persona (≈ 34 h).
- **Prueba pesimista (cada tarea ×1.4; interfaz y agente ×1.6):** el plan completo sale a **42.5 h y no cabe**. Con los cinco recortes activados queda un **piso de 31.3 h** con ≈ 2.7 h de colchón (8 %), que debería sostener el mínimo de 3/5 en funcionamiento de la funcionalidad crítica **pero sin margen**: un atasco de integración de 2–3 h lo rompe. Se pierde diferenciación, no el mínimo. Detalle en `retos/RIE-02/panorama.md` §d.1.
- **Mayor riesgo de alcance:** la interfaz y el grafo interactivo recaen en una sola persona en su primer hackathon. Mitigación: contrato JSON temprano, respaldo con grafo estático, pareo con otra persona y regla de corte.
- **Cobertura de habilidades del equipo:** 83 % (estimación de `scripts/sinergia`, con niveles aún por corregir).
- **Brechas de la pareja líder** (las cubre el resto del equipo): reglas de fraude y criterios de revisión (Antonio, con Caja Experts) y diseño de la vista del especialista (David lo asume con prototipo y prueba rápida con un mentor).
- **Dependencias:** datos de la Caja, que el expediente describe como referenciales y **sin compromiso de entrega** (si no llegan, nuestro generador); política de IA externa **[POR CONFIRMAR]**; KPI y línea base **[POR CONFIRMAR]**; criterios de dominio **[POR CONFIRMAR con Caja Experts]**.
- **Riesgos principales:** falsos positivos sobre clientes legítimos, protección de datos, sobreajuste a nuestro propio generador (partición dev/eval, semillas ciegas, patrón sorpresa; una regla con criterio de dominio rinde bien en nuestro dataset, así que el aporte frente a ella será moderado y se reportará así) y tiempo.
- **Recorte si falta tiempo, en este orden:** Louvain → componentes podados; modelo de scikit-learn → reglas ponderadas; agente con herramientas → plantilla con LLM solo para redactar; interfaz avanzada → grafo básico, ficha y botones; ablaciones → una sola evaluación. **No se recorta:** el backtest contra reglas simples y de dominio, la medición sobre señuelos, la regla de corroboración, las citas verificadas y la decisión humana.

---

## Anexo A. Tareas y horas en el evento (supuesto)

| Tarea | Habilidad | v0 | v1 base | Pesimista | Piso |
|---|---|---|---|---|---|
| Datos sintéticos con redes de fraude inyectadas | data_eng | 5 | 0 (preexistente) | 0 | 0 |
| Carga de lote y constructor del grafo tipado | data_eng / data_sci | — | 3 | 4.2 | 4.2 |
| Comunidades, anomalías e indicadores de red | data_sci | 5 | 3 | 4.2 | 3.2 |
| Priorización con razones y corroboración | ml | 3 | 2.5 | 3.5 | 2.1 |
| API y persistencia | backend | 3 | 2 | 2.8 | 2.8 |
| Agente de expediente, verificador y proveedor LLM | agentes | 4 | 4 | 6.4 | 2.9 |
| Vista del especialista y grafo | web + ux | 7 | 5.5 | 8.8 | 5.6 |
| Reglas de fraude y criterios de revisión | fin | 2 | 1 | 1.4 | 1.4 |
| Backtest, KPI y falsos positivos | biz | 2 | 3.5 | 4.9 | 3.5 |
| Pruebas, falsos positivos y validación | qa | 3 | 2.5 | 3.5 | 2.8 |
| Pitch y demo | pitch | 2 | 2 | 2.8 | 2.8 |
| **Total** | | **36** | **29** | **42.5** | **31.3** |

## Anexo B. Preguntas para el owner

Prioridad alta:

- [ ] ¿Cuál es la línea base: reglas actuales, tasa de falsos positivos y tiempo de revisión por caso, y cómo se mide hoy?
- [ ] El expediente menciona casos simulados y datos sintéticos referenciales: ¿vendrán etiquetados (redes de fraude y relaciones legítimas)? ¿En qué formato y volumen?
- [ ] ¿Qué tipos de vínculos son más relevantes (teléfono, dispositivo, dirección, referencia, contacto, negocio) y cuáles estarán en los datos? ¿Habrá conexiones (IP, sesión) y ubicaciones?
- [ ] ¿Se permite usar LLM externos (Claude, OpenAI) o solo modelos locales? ¿Qué datos pueden salir del entorno?
- [ ] ¿Quién es el especialista (prevención, investigación, riesgos) y cuál es su flujo y herramienta actuales?

Prioridad media:

- [ ] ¿Qué columnas y volumen tendrán los datos sintéticos (dispositivo, referencias, tipo de inmueble, antigüedad del cliente)? ¿Direcciones y teléfonos vienen normalizados?
- [ ] ¿Existe un umbral de monto de revisión reforzada? (Hoy suponemos S/ 10,000.)
- [ ] ¿Qué acciones de prevención puede orientar una alerta antes de un desembolso y cuáles se consideran decisiones que afectan al cliente?
- [ ] ¿Qué relaciones legítimas requieren cuidado especial (familias, mercados, gremios, gestores)?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.

## Anexo D. Cambios

**De v0 a v1:** tensión central del problema; cuatro ideas concretas; método de medición con partición dev/eval; preexistente declarado y separado del evento; funcionalidad crítica con condiciones medibles; esfuerzo de 36 a 29 h-persona.

**De v1 a v1.1 (cotejo con el expediente literal; 13 desviaciones, tabla en `retos/RIE-02/panorama.md`):** el problema se cita literal y se retiran las atribuciones que el expediente no hace («reputación», «decisiones crediticias automáticas»); se refuerza la restricción de no concluir fraude solo por relaciones con la **regla de corroboración**; la revisión humana se amplía a toda decisión que afecte a clientes; se agrega la **prevención** (verificación preventiva) junto con la investigación; se agregan la calidad de la cola y la detección temprana a la medición; se nombran contactos y negocios entre los vínculos; se declaran las brechas de datos (conexiones, ubicaciones, comportamiento) y la nota de no compromiso de entrega; se explicita la integración tecnológica que se demuestra; «investigador» pasa a «especialista»; se agrega la prueba pesimista de horas.
