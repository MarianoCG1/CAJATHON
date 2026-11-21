# Postulación RIE-03 — texto para pegar en la plataforma

Desafío elegido: RIE-03 · Anticipar el deterioro de pago antes del atraso. Equipo: Yupana Labs.

## 1. Problema abordado

Según el desafío, la situación económica de un microempresario puede deteriorarse poco a poco antes del primer atraso, y algunas señales tempranas pueden detectarse con información histórica. Pero no toda variación es un riesgo: hay que distinguir señales relevantes de fluctuaciones normales, evitar alertas innecesarias y no decidir con información insuficiente. Nuestra lectura, a validar con el owner, es que sin esa distinción se actúa tarde o se cansa al gestor con alertas inútiles. Respetamos las restricciones: protección de datos personales, sin sesgos, incertidumbre explícita, alertas sustentadas en evidencia y ninguna decisión crediticia automática.

## 2. Concepto de solución

Una cola diaria corta de clientes con riesgo de deterioro; cada alerta trae el porqué y una acción preventiva propuesta, y el gestor decide. Tiene tres piezas. Un modelo estima la probabilidad de pasar a atraso e indica su incertidumbre; con historial insuficiente, no alerta. Un filtro solo deja pasar caídas persistentes, ajenas a la estacionalidad del sector y presentes en al menos dos familias de señales (ingresos, conducta de pago, endeudamiento externo). Un agente propone canal, momento y mensaje citando la evidencia, con reglas que le impiden prometer condiciones crediticias. La alerta no cambia la calificación, el límite ni la tasa de ningún cliente.

## 3. Impacto esperado en el KPI

Proponemos como KPI principal la tasa de paso a atraso de más de 30 días en la cartera alertada, con y sin intervención; como secundarios, precisión de las alertas, falsos positivos y días de anticipación. La línea base y la cifra de mejora están a validar con el owner; no las inventamos. Mediremos con un backtest reproducible sobre datos sintéticos. Como esos datos no contienen intervenciones, el efecto de actuar a tiempo se mostrará como escenario con sensibilidad; lo que sí se mide es cuántos casos se detectan, con cuánta anticipación y con qué falsos positivos, frente a reglas simples de atraso.

## 4. Enfoque tecnológico

Analítica predictiva con probabilidades calibradas, un agente de IA acotado con proveedor de modelos intercambiable (nube, local o modo sin red), una API con bitácora de decisiones y una interfaz para el gestor, integrados de punta a punta. Usamos Python, FastAPI, scikit-learn, SQLite y React. Los registros usan identificadores, sin datos personales. No es un chatbot ni un tablero: el valor está en el filtro de falsos positivos y en la acción explicada, demostrado con un backtest propio.

## 5. Tecnología preexistente

Solo existen antes del evento un generador de datos sintéticos para este desafío, con sus pruebas, y los datos que produce (5,000 clientes ficticios y 34 meses de historia, sin ningún dato real). Ambos son del equipo y se crearon el 21.11.2026. También usamos librerías abiertas bajo sus licencias. No reutilizamos código de empleadores ni de otros clientes. Todo lo demás se construye en el evento.

## 6. Funcionalidad crítica

Dada una fecha de corte, el sistema calcula el riesgo de cada crédito con información hasta ese día, entrega la cola priorizada, muestra de dos a tres señales por cliente contrastadas con su historial y su sector, con su incertidumbre, y propone la intervención. El gestor aprueba, edita o descarta, y queda registro; nada se envía solo. Se construye íntegramente durante el evento, con commits frecuentes. Verificaremos que una fluctuación estacional de un mes no alerte, que un deterioro gradual sí, y que el agente nunca prometa condiciones crediticias.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta sobre miles de clientes sintéticos: se abre la cola del día, se analiza un caso con su explicación, se aprueba la acción propuesta y se muestra el backtest con y sin la solución. Incluye pruebas automáticas, reporte de validación, revisión de sesgos por grupo y el número antes y después del KPI. Queda fuera el envío real de mensajes y la integración con sistemas de la Caja.

## 8. Factibilidad y dependencias

Estimamos unas 32 horas-persona, en el límite de lo disponible; por eso fijamos de antemano un mínimo viable y un orden de recortes que protege la cola, la explicación, la aprobación humana, el backtest y las pruebas. El equipo cubre datos, modelos, agentes, desarrollo, experiencia de usuario y negocio. A confirmar con el owner: definición de atraso y línea base, política de IA externa, qué datos entregará la Caja (si no llegan, usamos los nuestros) y cuántos clientes atiende un gestor al día.
