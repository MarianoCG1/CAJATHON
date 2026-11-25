# RIE-03 — campos para pegar en el formulario

**Título:** RIE-03 · Alerta temprana explicada: la cola diaria que anticipa el deterioro de pago

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (554 caracteres):

El desafío plantea que la situación económica de un microempresario puede deteriorarse poco a poco antes del primer atraso y que algunas señales tempranas pueden detectarse con información histórica, pero que no toda variación es riesgo. Hoy (a validar con el owner) se actúa tarde, cuando ya hay mora, o se alerta de más y se cansa al gestor y al cliente. Atacamos ambos errores respetando los límites del desafío: protección de datos, sin sesgos, incertidumbre explícita, alertas con evidencia, revisión humana y ninguna decisión crediticia automática.

**Versión completa** (663 caracteres):

Según el desafío, la situación económica de un microempresario puede deteriorarse poco a poco antes del primer atraso, y algunas señales tempranas pueden detectarse con información histórica. Pero no toda variación es un riesgo: hay que distinguir señales relevantes de fluctuaciones normales, evitar alertas innecesarias y no decidir con información insuficiente. Nuestra lectura, a validar con el owner, es que sin esa distinción se actúa tarde o se cansa al gestor con alertas inútiles. Respetamos las restricciones: protección de datos personales, sin sesgos, incertidumbre explícita, alertas sustentadas en evidencia y ninguna decisión crediticia automática.

## 2. Concepto de solución

**Versión corta** (646 caracteres):

Una cola diaria corta de clientes al día con riesgo de deterioro, cada uno con el porqué y una acción preventiva propuesta; el gestor decide. Tres piezas: (1) un modelo calibrado que estima la probabilidad de pasar a atraso, con su incertidumbre (sin historial suficiente no alerta); (2) un filtro que solo deja pasar caídas persistentes, ajenas a la estacionalidad y presentes en al menos dos familias de señales (ingresos, conducta de pago, endeudamiento externo); (3) un agente acotado que propone canal, momento y mensaje citando la evidencia, sin poder prometer condiciones crediticias. La alerta nunca modifica calificación, límite ni tasa.

**Versión completa** (664 caracteres):

Una cola diaria corta de clientes con riesgo de deterioro; cada alerta trae el porqué y una acción preventiva propuesta, y el gestor decide. Tiene tres piezas. Un modelo estima la probabilidad de pasar a atraso e indica su incertidumbre; con historial insuficiente, no alerta. Un filtro solo deja pasar caídas persistentes, ajenas a la estacionalidad del sector y presentes en al menos dos familias de señales (ingresos, conducta de pago, endeudamiento externo). Un agente propone canal, momento y mensaje citando la evidencia, con reglas que le impiden prometer condiciones crediticias. La alerta no cambia la calificación, el límite ni la tasa de ningún cliente.

## 3. Impacto esperado

**Versión corta** (596 caracteres):

KPI principal propuesto: tasa de paso a atraso de más de 30 días en la cartera alertada, con y sin intervención. Secundarios: precisión en el top-k, falsos positivos y días de anticipación. La línea base y la cifra de mejora están a validar con el owner; no se inventan. Se medirá con un backtest reproducible sobre datos sintéticos, contra la política reactiva y reglas simples; el efecto de intervenir se presenta como escenario de sensibilidad porque los datos no contienen intervenciones. Se reporta mejora frente al azar y a la regla de atraso, no precisión absoluta (evento poco frecuente).

**Versión completa** (733 caracteres):

Proponemos como KPI principal la tasa de paso a atraso de más de 30 días en la cartera alertada, con y sin intervención; como secundarios, precisión de las alertas, falsos positivos y días de anticipación. La línea base y la cifra de mejora están a validar con el owner; no las inventamos. Mediremos con un backtest reproducible sobre datos sintéticos. Como esos datos no contienen intervenciones, el efecto de actuar a tiempo se mostrará como escenario con sensibilidad; lo que sí se mide es cuántos casos se detectan, con cuánta anticipación y con qué falsos positivos, frente a reglas simples de atraso. Hablamos de mejora frente al azar y frente a la regla de atraso, no de precisión absoluta, porque el evento es poco frecuente.

## 4. Enfoque tecnológico

**Versión corta** (648 caracteres):

Python, FastAPI, scikit-learn, SQLite y React. Analítica predictiva calibrada con variables calculadas solo con información hasta la fecha de corte, filtro de señal frente a fluctuación, agente acotado con proveedor de modelos intercambiable (nube, local o plantillas sin red), API con bitácora de decisiones e interfaz para el gestor, integrados de punta a punta. El prototipo no se conecta a sistemas de la Caja. Los registros usan identificadores sin datos personales; sexo, edad y zona solo sirven para auditar sesgos, no entran al modelo. No es un chatbot ni un tablero: el valor está en el filtro de falsos positivos y en la acción explicada.

**Versión completa** (629 caracteres):

Analítica predictiva con probabilidades calibradas, un agente de IA acotado con proveedor de modelos intercambiable (nube, local o modo sin red), una API con bitácora de decisiones y una interfaz para el gestor, integrados de punta a punta. Usamos Python, FastAPI, scikit-learn, SQLite y React. El prototipo no se conecta a sistemas de la Caja y funciona sin red; el modelo de lenguaje, si se usa, es solo para redactar borradores. Los registros usan identificadores, sin datos personales. No es un chatbot ni un tablero: el valor está en el filtro de falsos positivos y en la acción explicada, demostrado con un backtest propio.

## 5. Tecnología preexistente

**Versión corta** (537 caracteres):

Existen antes del evento solo: (1) un generador de datos sintéticos para este desafío, con 24 pruebas automáticas, y (2) los datos que produce (5,000 clientes ficticios, 34 meses). Titular: el equipo. Creados el 21.11.2026. 100 % ficticios. Además, librerías abiertas (FastAPI, pandas, scikit-learn, React) bajo sus licencias y herramientas internas de planificación que no forman parte del producto. No se reutiliza código de empleadores ni de otros clientes. Modelo, filtro, agente, API, interfaz y backtest se construyen en el evento.

**Versión completa** (414 caracteres):

Solo existen antes del evento un generador de datos sintéticos para este desafío, con sus 24 pruebas automáticas, y los datos que produce (5,000 clientes ficticios y 34 meses de historia, sin ningún dato real). Ambos son del equipo y se crearon el 21.11.2026. También usamos librerías abiertas bajo sus licencias. No reutilizamos código de empleadores ni de otros clientes. Todo lo demás se construye en el evento.

## 6. Funcionalidad crítica

**Versión corta** (616 caracteres):

Cola diaria preventiva con explicación y acción propuesta, con aprobación humana. Dada una fecha de corte, calcula el riesgo de cada crédito vigente con información hasta ese día; entrega los k clientes priorizados tras el filtro; muestra 2–3 señales contrastadas con su historial y su sector, con la incertidumbre; propone la intervención; el gestor aprueba, edita o descarta, con bitácora. Nada se envía ni ejecuta solo. Criterios de aceptación: misma fecha, misma cola; sin fuga del futuro; una fluctuación estacional de un mes no alerta y un deterioro gradual sí; el agente nunca promete condiciones crediticias.

**Versión completa** (556 caracteres):

Dada una fecha de corte, el sistema calcula el riesgo de cada crédito con información hasta ese día, entrega la cola priorizada, muestra de dos a tres señales por cliente contrastadas con su historial y su sector, con su incertidumbre, y propone la intervención. El gestor aprueba, edita o descarta, y queda registro; nada se envía solo. Se construye íntegramente durante el evento, con commits frecuentes. Verificaremos que una fluctuación estacional de un mes no alerte, que un deterioro gradual sí, y que el agente nunca prometa condiciones crediticias.

## 7. Nivel de desarrollo esperado

**Versión corta** (500 caracteres):

Prototipo funcional de punta a punta sobre miles de clientes sintéticos: se abre la cola del día, se analiza un caso con su explicación, se aprueba la acción propuesta, se muestra un cliente con fluctuación normal que no alertó y se cierra con el backtest con y sin la solución. Incluye pruebas automáticas, reporte de validación, revisión de sesgos por grupo y el número antes y después del KPI. Fuera de alcance: envío real de mensajes, integración con sistemas de la Caja y decisiones crediticias.

**Versión completa** (413 caracteres):

Prototipo funcional de punta a punta sobre miles de clientes sintéticos: se abre la cola del día, se analiza un caso con su explicación, se aprueba la acción propuesta y se muestra el backtest con y sin la solución. Incluye pruebas automáticas, reporte de validación, revisión de sesgos por grupo y el número antes y después del KPI. Queda fuera el envío real de mensajes y la integración con sistemas de la Caja.

## 8. Factibilidad y dependencias

**Versión corta** (676 caracteres):

Unas 32 horas-persona frente a unas 32 disponibles: por eso se fija un mínimo viable y un orden de recortes que protege la cola, la explicación, la aprobación humana, el backtest y las pruebas. Evidencia medida sobre datos sintéticos propios: ninguna variable sola supera un AUC de 0.85; las señales tempranas elevan el AUC de 0.81 a 0.92 frente a la regla de atraso; entre clientes al día, el 10 % mejor puntuado concentra cerca de dos tercios de los casos. El equipo cubre datos, modelos, agentes, desarrollo, UX y negocio. A confirmar: definición de atraso y línea base, política de IA externa, datos de la Caja (si no llegan, usamos los nuestros) y capacidad por analista.

**Versión completa** (897 caracteres):

Estimamos unas 32 horas-persona, en el límite de lo disponible; por eso fijamos de antemano un mínimo viable y un orden de recortes que protege la cola, la explicación, la aprobación humana, el backtest y las pruebas. El equipo cubre datos, modelos, agentes, desarrollo, experiencia de usuario y negocio. Evidencia de factibilidad, medida sobre nuestros datos sintéticos (no sobre cartera de la Caja): el problema no es trivial, porque ninguna variable sola supera un AUC de 0.85 y la regla «ya tiene atraso» no sirve con quien está al día; las señales tempranas elevan el AUC de 0.81 a 0.92, y entre clientes al día el 10 % mejor puntuado concentra cerca de dos tercios de los casos que pasan a atraso. A confirmar con el owner: definición de atraso y línea base, política de IA externa, qué datos entregará la Caja (si no llegan, usamos los nuestros) y cuántos clientes atiende un gestor al día.
