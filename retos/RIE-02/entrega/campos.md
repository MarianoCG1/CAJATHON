# RIE-02 — campos para pegar en el formulario

**Título:** RIE-02 · Mesa del especialista de redes: priorizar redes de riesgo con evidencia citada y sin acusar a clientes legítimos

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (614 caracteres):

Algunas modalidades de fraude involucran a varias personas, negocios o solicitudes que, evaluadas una por una, no muestran irregularidad. Las conexiones entre teléfonos, dispositivos, direcciones, referencias o negocios pueden delatarlas, pero compartir un dato no implica fraude: una familia, los puestos de un mercado o un contador que atiende a muchos clientes también comparten información. Revisar caso por caso no ve la red; alertar por cada coincidencia inunda al especialista y señala a clientes legítimos. Abordamos cómo distinguir lo que merece revisión y orientar acciones de prevención e investigación.

**Versión completa** (667 caracteres):

Algunas modalidades de fraude involucran a varias personas, negocios o solicitudes de crédito que, evaluadas una por una, no muestran señales de irregularidad. Las conexiones entre teléfonos, dispositivos, direcciones, referencias, contactos o negocios pueden delatarlas, pero compartir un dato no implica fraude: una familia, los puestos de un mismo mercado o un contador que atiende a muchos clientes también comparten información. Revisar solicitud por solicitud no ve la red; alertar por cada coincidencia inunda a los especialistas y señala a clientes legítimos. Abordamos cómo distinguir lo que merece revisión y orientar acciones de prevención e investigación.

## 2. Concepto de solución

**Versión corta** (688 caracteres):

Una mesa de trabajo para el especialista: convierte un lote de solicitudes en un grafo, encuentra los grupos conectados de forma inusual, los ordena por prioridad y entrega por cada red un expediente con evidencia citada y las explicaciones legítimas posibles. Cuatro ideas: el peso de un vínculo depende de lo raro que es (un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia, casi nada); las relaciones solas nunca bastan, hace falta comportamiento anómalo (ráfagas, negocios y líneas recientes); cada alerta muestra su contrapartida legítima; ninguna acción sobre un cliente se ejecuta sin revisión humana. Dice «merece revisión», nunca «fraude».

**Versión completa** (827 caracteres):

Una mesa de trabajo para el especialista de Caja Trujillo. Convierte un lote de solicitudes en un grafo de personas, negocios, teléfonos, dispositivos, direcciones y referencias; encuentra los grupos conectados de forma inusual; los ordena por prioridad; y entrega, por cada red, un expediente con evidencia citada y con las explicaciones legítimas posibles. Cuatro ideas: el peso de un vínculo depende de lo raro que es (un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia, casi nada); las relaciones solas nunca bastan, hace falta además comportamiento anómalo (ráfagas de solicitudes, negocios y líneas recientes); cada alerta muestra su contrapartida legítima; y ninguna acción que afecte a un cliente se ejecuta sin revisión humana. La alerta dice «merece revisión», nunca «fraude».

## 3. Impacto esperado

**Versión corta** (501 caracteres):

Indicadores propuestos: precisión y recall sobre redes de fraude simuladas; reducción de falsos positivos frente a reglas simples a igual recall; calidad de la cola de priorización. Línea base y cifra de impacto, a validar con el owner; no presentamos números que no podamos sustentar. Medición con datos sintéticos y verdad de terreno: se afina en una partición y se evalúa en otra y en semillas ciegas, con intervalos de confianza y una ablación del efecto de exigir corroboración de comportamiento.

**Versión completa** (455 caracteres):

Los indicadores propuestos son: precisión y recall sobre redes de fraude simuladas, reducción de falsos positivos frente a reglas simples a igual recall, y calidad de la cola de priorización. La línea base y la cifra de impacto están a validar con el owner; no presentamos números que no podamos sustentar. Mediremos con datos sintéticos y verdad de terreno, afinando en una partición y evaluando en otra y en semillas ciegas, con intervalos de confianza.

## 4. Enfoque tecnológico

**Versión corta** (684 caracteres):

Flujo de punta a punta: lote de solicitudes, grafo ponderado, detección de comunidades e indicadores de red, priorización con razones por factor, agente que redacta el expediente, vista del especialista y decisión humana registrada. Python, pandas, networkx y scikit-learn para el grafo y la priorización; agente con Pydantic AI de proveedor intercambiable (Claude, OpenAI, modelo local o plantilla sin red) y un verificador que rechaza citas inexistentes y frases de conclusión; FastAPI y SQLite; React y Cytoscape.js. El prototipo no se conecta a sistemas de la Caja. El valor está en la ponderación por rareza, la exoneración legítima y el expediente verificable, no en un tablero.

**Versión completa** (650 caracteres):

Flujo de punta a punta: lote de solicitudes, grafo ponderado, detección de comunidades e indicadores de red, priorización con razones por factor, agente de IA que redacta el expediente, vista del especialista y decisión humana registrada. Usamos Python, pandas, networkx y scikit-learn para el grafo y la priorización; un agente con Pydantic AI de proveedor intercambiable (Claude, OpenAI, modelo local o plantilla sin red) y un verificador que rechaza citas inexistentes y frases de conclusión; FastAPI y SQLite; React y Cytoscape.js. El valor está en la ponderación por rareza, la exoneración legítima y el expediente verificable, no en un tablero.

## 5. Tecnología preexistente

**Versión corta** (538 caracteres):

Antes del evento existe solo un generador de datos sintéticos propio, con 37 pruebas automáticas, creado el 21.11.2026 (titular: el equipo), que produce solicitudes ficticias con redes de fraude simuladas y relaciones legítimas; no contiene el detector, la priorización ni el agente. Además, librerías abiertas bajo sus licencias (FastAPI, pandas, networkx, scikit-learn, React, Cytoscape.js, entre otras). Sin datos reales ni código de otras organizaciones. Grafo, puntaje, agente, verificador, API e interfaz se construyen en el evento.

**Versión completa** (472 caracteres):

Un generador de datos sintéticos propio, con sus 37 pruebas automáticas, creado el 21.11.2026, que produce solicitudes ficticias con redes de fraude simuladas y relaciones legítimas; no contiene el detector, la priorización ni el agente. Es titularidad del equipo y se declara en la entrega. Además, librerías abiertas bajo sus licencias (FastAPI, pandas, networkx, scikit-learn, React, Cytoscape.js, entre otras). No usamos datos reales ni código de otras organizaciones.

## 6. Funcionalidad crítica

**Versión corta** (479 caracteres):

Un lote de solicitudes entra y sale con las redes de riesgo priorizadas, cada una con su expediente de evidencia citada, sus explicaciones legítimas y una acción sugerida de prevención o investigación, y con la decisión del especialista registrada. Debe detectar redes de vínculos débiles encadenados mejor que las reglas simples, no priorizar familias, mercados ni gestores legítimos, y no alertar nunca solo por relaciones. Se construye íntegramente durante la fase presencial.

**Versión completa** (479 caracteres):

Un lote de solicitudes entra y sale con las redes de riesgo priorizadas, cada una con su expediente de evidencia citada, sus explicaciones legítimas y una acción sugerida de prevención o investigación, y con la decisión del especialista registrada. Debe detectar redes de vínculos débiles encadenados mejor que las reglas simples, no priorizar familias, mercados ni gestores legítimos, y no alertar nunca solo por relaciones. Se construye íntegramente durante la fase presencial.

## 7. Nivel de desarrollo esperado

**Versión corta** (476 caracteres):

Prototipo funcional de punta a punta con un caso de uso: se carga el lote, se abre una red encadenada que las reglas simples no verían, se lee su expediente, se contrasta con un señuelo legítimo que comparte el mismo dato, el especialista decide y queda registrado. Cierra con el antes y después del KPI, pruebas automáticas, reporte de validación e historial de desarrollo. Fuera de alcance: integración con sistemas reales, bloqueo de operaciones y reentrenamiento en línea.

**Versión completa** (376 caracteres):

Prototipo funcional de punta a punta con un caso de uso: se carga el lote, se abre una red encadenada que las reglas simples no verían, se lee su expediente, se contrasta con un señuelo legítimo que comparte el mismo dato, el especialista decide y queda registrado. Cerramos con el antes y después del KPI, pruebas automáticas, reporte de validación e historial de desarrollo.

## 8. Factibilidad y dependencias

**Versión corta** (655 caracteres):

Unas 29 horas-persona frente a unas 34 disponibles (estimación nuestra); en el escenario pesimista el plan completo no cabe y se fija un mínimo de unas 31 horas con un núcleo intocable: grafo, corroboración, expediente verificado, decisión humana y comparación contra reglas. Evidencia medida sobre datos sintéticos propios: una regla que marca cualquier coincidencia detecta el 90 % del fraude pero marca todos los señuelos y su precisión es del 12 %; exigir dos tipos de vínculo baja los señuelos marcados al 37 %, pero detecta solo el 43 % del fraude. A validar con el owner: datos de la Caja, política de IA externa, línea base y criterios de dominio.

**Versión completa** (996 caracteres):

Estimamos unas 29 horas-persona de construcción, frente a unas 34 disponibles (estimación nuestra). En un escenario pesimista el plan completo no cabe; definimos un mínimo de unas 31 horas que mantiene el funcionamiento de punta a punta, con recortes ordenados y un núcleo intocable: grafo, corroboración, expediente verificado, decisión humana y comparación contra reglas. Evidencia medida sobre nuestros datos sintéticos, no sobre la Caja: el problema no es trivial. Una regla que marca cualquier coincidencia detecta el 90 % de las solicitudes de fraude pero marca todos los señuelos legítimos y su precisión es del 12 %; exigir dos tipos de vínculo baja los señuelos marcados al 37 %, pero detecta solo el 43 % del fraude y apenas el 12 % de las solicitudes de las redes más difíciles. Dependencias a validar con el owner: datos de la Caja (referenciales, sin compromiso de entrega; si no llegan, usamos los nuestros), política de uso de IA externa, línea base del KPI y criterios de dominio.
