# Postulación RIE-03 — texto para pegar en la plataforma

Desafío elegido: RIE-03 · Anticipar el deterioro de pago antes del atraso. Equipo: Yupana Labs.

## 1. Problema abordado

Según el desafío, la situación económica de un microempresario puede deteriorarse poco a poco antes del primer atraso, y algunas señales tempranas pueden detectarse con información histórica. Pero no toda variación es un riesgo: hay que distinguir señales relevantes de fluctuaciones normales, evitar alertas innecesarias y no decidir con información insuficiente. Nuestra lectura, a validar con el owner, es que sin esa distinción se actúa tarde o se cansa al gestor con alertas inútiles. Respetamos las restricciones: protección de datos personales, sin sesgos, incertidumbre explícita, alertas sustentadas en evidencia y ninguna decisión crediticia automática.

## 2. Concepto de solución

Una cola corta y priorizada de clientes con riesgo de deterioro; cada alerta trae el porqué y una acción preventiva propuesta, y el gestor decide. Tiene tres piezas. Un modelo estima la probabilidad de pasar a atraso e indica su incertidumbre; con historial insuficiente, no alerta. Un filtro solo deja pasar caídas persistentes, ajenas a la estacionalidad del sector y presentes en al menos dos familias de señales (ingresos, conducta de pago, endeudamiento externo; supuesto: depende de las señales de actividad en cuenta y de deuda en otras entidades que la Caja pueda aportar, y el esquema se adapta a lo disponible). Un agente propone canal, momento y mensaje citando la evidencia, con reglas que le impiden prometer condiciones crediticias. La alerta no cambia la calificación, el límite ni la tasa de ningún cliente.

## 3. Impacto esperado en el KPI

Proponemos como KPI principal la tasa de paso a atraso de más de 30 días en la cartera alertada, con y sin intervención; como secundarios, precisión de las alertas, falsos positivos y días de anticipación. La línea base y la cifra de mejora están a validar con el owner; no las inventamos. Mediremos con un backtest reproducible sobre datos sintéticos. Como esos datos no contienen intervenciones, el efecto de actuar a tiempo se mostrará como escenario con sensibilidad; lo que sí se mide es cuántos casos se detectan, con cuánta anticipación y con qué falsos positivos, frente a reglas simples de atraso. Hablamos de mejora frente al azar y frente a la regla de atraso, no de precisión absoluta, porque el evento es poco frecuente. Ilustración aritmética, no estimación: con la captura medida (cerca de dos tercios de los casos entre clientes al día, sobre datos sintéticos propios), si la gestión temprana evitara el 10 %, el 20 % o el 30 % de los pasos a atraso de los casos capturados (efecto: escenario, a definir con el owner), de cada 100 créditos que pasarían a atraso se evitarían unos 7, 13 o 20.

## 4. Enfoque tecnológico

Analítica predictiva con probabilidades calibradas, un agente de IA acotado con proveedor de modelos intercambiable (nube, local o modo sin red), una API con bitácora de decisiones y una interfaz para el gestor, integrados de punta a punta. Usamos Python, FastAPI, scikit-learn, SQLite y React. El prototipo no se conecta a sistemas de la Caja y funciona sin red; el modelo de lenguaje, si se usa, es solo para redactar borradores. Los registros usan identificadores, sin datos personales. No es un chatbot ni un tablero: el valor está en el filtro de falsos positivos y en la acción explicada, demostrado con un backtest propio.

## 5. Tecnología preexistente

Existen antes del evento: (1) un generador de datos sintéticos para este desafío, con sus 24 pruebas automáticas; (2) los datos que produce (5,000 clientes ficticios y 34 meses de historia, sin ningún dato real); y (3) un script de auditoría que mide si una regla simple resuelve el problema con esos datos; de él salen las cifras medidas de la sección 8; no forma parte de la solución ni se reutiliza en ella. Todo es del equipo y se creó el 21.11.2026. También usamos librerías abiertas bajo sus licencias. No reutilizamos código de empleadores ni de otros clientes. Todo lo demás se construye en el evento.

## 6. Funcionalidad crítica

Dada una fecha de corte, el sistema calcula el riesgo de cada crédito con información hasta ese día, entrega la cola priorizada, muestra de dos a tres señales por cliente contrastadas con su historial y su sector, con su incertidumbre, y propone la intervención. El gestor aprueba, edita o descarta, y queda registro; nada se envía solo. Se construye íntegramente durante el evento, con commits frecuentes. En el prototipo la cola se recalcula por fecha de corte (mensual, según los datos sintéticos); una cadencia diaria sería un supuesto a validar con el owner. Verificaremos que una fluctuación estacional de un mes no alerte, que un deterioro gradual sí, y que el agente nunca prometa condiciones crediticias.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta sobre miles de clientes sintéticos: se abre la cola del día, se analiza un caso con su explicación, se aprueba la acción propuesta y se muestra el backtest con y sin la solución. Incluye pruebas automáticas, reporte de validación, revisión de sesgos por grupo (como mínimo, un cuadro de tasa de alerta por grupo) y el número antes y después del KPI. Queda fuera el envío real de mensajes y la integración con sistemas de la Caja.

## 8. Factibilidad y dependencias

Estimamos 31,5 horas-persona de 32 disponibles (supuesto), sin holgura; por eso el plan base es un mínimo viable (cola con puntaje real e incertidumbre, explicación, filtro de señal, propuesta de intervención por plantillas con reglas, aprobación humana con bitácora, backtest y pruebas) y lo demás se añade solo si sobra tiempo, en este orden: modelo de lenguaje para redactar borradores, árboles además de regresión logística, auditoría de sesgos completa y varios escenarios de efecto. El equipo cubre datos, modelos, agentes, desarrollo, experiencia de usuario y negocio. Medido sobre datos sintéticos propios (no sobre cartera de la Caja): entre los clientes al día solo el 0,7 % pasa a atraso de más de 30 días en los siguientes 60; un modelo de árboles los ordena con un AUC de 0,84 y el 10 % mejor puntuado concentra cerca de dos tercios de esos casos, unas 7 veces lo que lograría el azar; la regla «ya tiene atraso» no distingue entre ellos. La precisión absoluta es baja porque el evento es raro (4,7 % de aciertos en ese 10 % frente a 0,7 % al azar), por eso la acción propuesta es de bajo costo y el aporte del filtro de señal se medirá en el backtest como reducción de falsos positivos frente al puntaje sin filtro. El tamaño de la cola es un parámetro; la evidencia usa el 10 % por convención. A confirmar con el owner: definición de atraso y línea base, política de IA externa, qué datos entregará la Caja (si no llegan, usamos los nuestros) y cuántos clientes atiende un gestor al día.
