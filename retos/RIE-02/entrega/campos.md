# RIE-02 — campos para pegar en el formulario

**Título:** RIE-02 · Mesa del especialista de redes: priorizar redes de riesgo con evidencia citada y sin acusar a clientes legítimos

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (714 caracteres):

Algunas modalidades de fraude involucran a varias personas, negocios o solicitudes que, evaluadas una por una, no muestran irregularidad. Las conexiones entre teléfonos, dispositivos, direcciones, referencias o negocios pueden revelar patrones inusuales, pero compartir un dato no implica necesariamente fraude: una familia, los puestos de un mercado o un contador que atiende a muchos clientes también comparten información. Revisar caso por caso puede no mostrar la red, y alertar por cada coincidencia podría inundar al especialista y señalar a clientes legítimos (cómo se revisa hoy, a confirmar con el owner). Abordamos cómo distinguir lo que merece revisión y orientar acciones de prevención e investigación.

**Versión completa** (814 caracteres):

Algunas modalidades de fraude involucran a varias personas, negocios o solicitudes de crédito que, evaluadas una por una, no muestran señales de irregularidad. Las conexiones entre teléfonos, dispositivos, direcciones, referencias, contactos o negocios pueden revelar patrones inusuales, pero compartir un dato no implica necesariamente fraude: una familia, los puestos de un mismo mercado o un contador que atiende a muchos clientes también comparten información (ejemplos nuestros, a validar con la Caja). Revisar solicitud por solicitud puede no mostrar la red, y alertar por cada coincidencia podría inundar a los especialistas y señalar a clientes legítimos (cómo se revisa hoy lo confirmaremos con el owner). Abordamos cómo distinguir lo que merece revisión y orientar acciones de prevención e investigación.

## 2. Concepto de solución

**Versión corta** (688 caracteres):

Una mesa de trabajo para el especialista: convierte un lote de solicitudes en un grafo, encuentra los grupos conectados de forma inusual, los ordena por prioridad y entrega por cada red un expediente con evidencia citada y las explicaciones legítimas posibles. Cuatro ideas: el peso de un vínculo depende de lo raro que es (un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia, casi nada); las relaciones solas nunca bastan, hace falta comportamiento anómalo (ráfagas, negocios y líneas recientes); cada alerta muestra su contrapartida legítima; ninguna acción sobre un cliente se ejecuta sin revisión humana. Dice «merece revisión», nunca «fraude».

**Versión completa** (827 caracteres):

Una mesa de trabajo para el especialista de Caja Trujillo. Convierte un lote de solicitudes en un grafo de personas, negocios, teléfonos, dispositivos, direcciones y referencias; encuentra los grupos conectados de forma inusual; los ordena por prioridad; y entrega, por cada red, un expediente con evidencia citada y con las explicaciones legítimas posibles. Cuatro ideas: el peso de un vínculo depende de lo raro que es (un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia, casi nada); las relaciones solas nunca bastan, hace falta además comportamiento anómalo (ráfagas de solicitudes, negocios y líneas recientes); cada alerta muestra su contrapartida legítima; y ninguna acción que afecte a un cliente se ejecuta sin revisión humana. La alerta dice «merece revisión», nunca «fraude».

## 3. Impacto esperado

**Versión corta** (700 caracteres):

Indicadores propuestos: precisión y recall sobre redes de fraude simuladas; menos falsos positivos frente a reglas simples a igual recall; calidad de la cola y carga de revisión (alertas por cada 1.000 solicitudes). Línea base y cifra de impacto, a validar con el owner; hoy no presentamos números que no podamos sustentar. Referencia medida sobre datos sintéticos propios: marcar cualquier coincidencia obliga a revisar 46 % de las solicitudes y solo cerca del 12 % de ellas es fraude; la meta es reducir esa carga a igual recall (meta numérica fijada el primer día con la partición de desarrollo). Partición de desarrollo y de evaluación, semillas nuevas, intervalos y ablación de la corroboración.

**Versión completa** (936 caracteres):

Los indicadores propuestos son: precisión y recall sobre redes de fraude simuladas, reducción de falsos positivos frente a reglas simples a igual recall, calidad de la cola de priorización y carga de revisión (alertas por cada 1.000 solicitudes). La línea base y la cifra de impacto están a validar con el owner; no presentamos números que no podamos sustentar. Mediremos con datos sintéticos y verdad de terreno, afinando en una partición y evaluando en otra y en semillas ciegas, con intervalos de confianza, y una ablación del efecto de exigir corroboración de comportamiento. Referencia medida en nuestros datos sintéticos: marcar cualquier coincidencia obliga a revisar 871 de 1.884 solicitudes (46 %), de las que solo cerca del 12 % es fraude; la meta es reducir esa carga a igual recall. La meta numérica se fija el primer día con la partición de desarrollo y se registra antes de evaluar; hoy no inventamos una cifra de impacto.

## 4. Enfoque tecnológico

**Versión corta** (667 caracteres):

Lote de solicitudes, grafo ponderado, comunidades e indicadores de red, priorización con razones, agente que redacta el expediente y decisión humana registrada. Python, pandas, networkx y scikit-learn; Pydantic AI con proveedor intercambiable (o plantilla sin red) y un verificador de citas; FastAPI, SQLite, React y Cytoscape.js. La IA pondera la rareza de cada vínculo, corrobora estructura con comportamiento y redacta un expediente verificable. Protección de datos: solo datos sintéticos; al modelo de lenguaje solo irían identificadores seudonimizados y cada decisión queda registrada. El prototipo no se conectará a sistemas de la Caja (alcance que proponemos).

**Versión completa** (1131 caracteres):

Flujo de punta a punta: lote de solicitudes, grafo ponderado, detección de comunidades e indicadores de red, priorización con razones por factor, agente de IA que redacta el expediente, vista del especialista y decisión humana registrada. Usamos Python, pandas, networkx y scikit-learn para el grafo y la priorización; un agente con Pydantic AI de proveedor intercambiable (Claude, OpenAI, modelo local o plantilla sin red) y un verificador que rechaza citas inexistentes y frases de conclusión; FastAPI y SQLite; React y Cytoscape.js. El valor está en la ponderación por rareza, la exoneración legítima y el expediente verificable, no en un tablero. La IA aporta en tres puntos: pondera la rareza de cada vínculo, corrobora estructura con comportamiento y redacta un expediente que un verificador comprueba línea por línea. Protección de datos: trabajamos solo con datos sintéticos; al modelo de lenguaje solo irían identificadores y atributos seudonimizados, la plantilla sin red es la opción por defecto y cada decisión queda registrada con su motivo. El prototipo no se conectará a sistemas de la Caja (alcance que proponemos).

## 5. Tecnología preexistente

**Versión corta** (586 caracteres):

Antes del evento existe solo un generador de datos sintéticos propio, con 37 pruebas automáticas (creado el 21.11.2026; titular: el equipo), que produce solicitudes ficticias con redes de fraude y relaciones legítimas; no contiene el detector, la priorización ni el agente como solución. Sus pruebas incluyen reglas de control solo para comprobar que los datos no son triviales; se reescriben en el evento como línea comparativa. También existe un script de auditoría de dificultad de los datos. Librerías abiertas bajo sus licencias. Sin datos reales ni código de otras organizaciones.

**Versión completa** (869 caracteres):

Un generador de datos sintéticos propio, con sus 37 pruebas automáticas, creado el 21.11.2026, que produce solicitudes ficticias con redes de fraude simuladas y relaciones legítimas; no contiene el detector, la priorización ni el agente como solución; sus pruebas incluyen reglas de control (coincidencia simple y una regla con criterio de dominio) solo para comprobar que los datos no son triviales, y se reescriben en el evento como línea comparativa. También existe un script de auditoría de dificultad de los datos, de donde salen las cifras medidas. Es titularidad del equipo y se declara en la entrega. Además, librerías abiertas bajo sus licencias (FastAPI, pandas, networkx, scikit-learn, React, Cytoscape.js, entre otras). No usamos datos reales ni código de otras organizaciones. Grafo, puntaje, agente, verificador, API e interfaz se construyen en el evento.

## 6. Funcionalidad crítica

**Versión corta** (479 caracteres):

Un lote de solicitudes entra y sale con las redes de riesgo priorizadas, cada una con su expediente de evidencia citada, sus explicaciones legítimas y una acción sugerida de prevención o investigación, y con la decisión del especialista registrada. Debe detectar redes de vínculos débiles encadenados mejor que las reglas simples, no priorizar familias, mercados ni gestores legítimos, y no alertar nunca solo por relaciones. Se construye íntegramente durante la fase presencial.

**Versión completa** (660 caracteres):

Un lote de solicitudes entra y sale con las redes de riesgo priorizadas, cada una con su expediente de evidencia citada, sus explicaciones legítimas y una acción sugerida de prevención o investigación, y con la decisión del especialista registrada. Debe detectar redes de vínculos débiles encadenados mejor que las reglas simples, no priorizar familias, mercados, tabletas de agencia, gremios ni gestores legítimos, y no alertar nunca solo por relaciones. La evaluación ocurre al ingresar la solicitud, antes del desembolso (supuesto de flujo), para pedir verificación preventiva o escalar a investigación. Se construye íntegramente durante la fase presencial.

## 7. Nivel de desarrollo esperado

**Versión corta** (476 caracteres):

Prototipo funcional de punta a punta con un caso de uso: se carga el lote, se abre una red encadenada que las reglas simples no verían, se lee su expediente, se contrasta con un señuelo legítimo que comparte el mismo dato, el especialista decide y queda registrado. Cierra con el antes y después del KPI, pruebas automáticas, reporte de validación e historial de desarrollo. Fuera de alcance: integración con sistemas reales, bloqueo de operaciones y reentrenamiento en línea.

**Versión completa** (478 caracteres):

Prototipo funcional de punta a punta con un caso de uso: se carga el lote, se abre una red encadenada que las reglas simples no verían, se lee su expediente, se contrasta con un señuelo legítimo que comparte el mismo dato, el especialista decide y queda registrado. Cerramos con el antes y después del KPI, pruebas automáticas, reporte de validación e historial de desarrollo. Fuera de alcance: integración con sistemas reales, bloqueo de operaciones y reentrenamiento en línea.

## 8. Factibilidad y dependencias

**Versión corta** (692 caracteres):

Unas 29 horas-persona (construcción, pruebas y demostración) frente a unas 34 disponibles; si todo tarda 1,4 a 1,6 veces más, el plan completo (≈ 42 h) no cabe y queda un mínimo de ≈ 31 h con núcleo intocable (grafo ponderado, corroboración, expediente verificado, decisión humana y comparación contra reglas). Medido sobre datos sintéticos propios (evaluación: 1.884 solicitudes, 114 de fraude): marcar cualquier coincidencia detecta 90 % del fraude pero marca todos los señuelos (precisión 12 %); dos tipos de vínculo, 43 %. Frente a una regla de dominio ajustada a mano (F1 ≈ 0,9) el aporte será moderado y se reportará así. A validar: datos, IA externa, línea base y criterios de dominio.

**Versión completa** (2084 caracteres):

Estimamos unas 29 horas-persona entre construcción, pruebas y demostración, frente a unas 34 disponibles (7,5 horas de construcción y 1 de pruebas por persona; estimación nuestra). Si las tareas tardan de 1,4 a 1,6 veces más, el plan completo (unas 42 horas) no cabe; con cinco recortes ordenados queda un mínimo de unas 31 horas, con un colchón de apenas el 8 %, y un núcleo intocable: grafo, corroboración, expediente verificado, decisión humana y comparación contra reglas. En el mínimo, el análisis central es el grafo ponderado por rareza con comunidades y la regla de corroboración; el modelo de lenguaje redacta y un verificador determinista rechaza citas inexistentes; el aprendizaje automático y el agente con herramientas son mejoras si hay tiempo, no el piso. El mayor riesgo es la interfaz con grafo interactivo; el respaldo es un grafo estático servido por la API. Evidencia medida sobre nuestros datos sintéticos, no sobre la Caja (partición de evaluación: 1.884 solicitudes, 114 de fraude y 397 señuelos legítimos; la proporción de fraude y de señuelos la fijamos nosotros): una regla que marca toda solicitud que comparte teléfono, dispositivo, domicilio, local o teléfono de referencia con otra detecta el 90 % del fraude pero marca todos los señuelos y su precisión es del 12 %; exigir dos tipos de vínculo baja los señuelos marcados al 37 %, pero detecta solo el 43 % del fraude y apenas el 12 % de las solicitudes de las redes más difíciles (7 redes en evaluación). Una regla con criterio de dominio, que ajustamos a mano viendo estos mismos datos, rinde bien (F1 cercano a 0,9 sobre el lote completo): frente a ella el aporte esperado es moderado y lo reportaremos así; el valor está en la explicación por red, el expediente verificable, la corroboración que evita acusar por relaciones y la robustez en redes difíciles, no en una ventaja amplia de recall. Dependencias a validar con el owner: datos de la Caja (referenciales, sin compromiso de entrega; si no llegan, usamos los nuestros), política de uso de IA externa, línea base del KPI y criterios de dominio.
