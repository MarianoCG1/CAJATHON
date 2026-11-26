# RIE-03 — formulario «Concept Solution», listo para pegar

**Fecha límite:** jueves 26 de noviembre, 11:59 p. m. (hora de Perú). **Se envía un solo desafío por equipo.**
Cada bloque gris se copia entero en su campo. El conteo es de caracteres frente al máximo del formulario.

## Paso 1 · Identificación de la propuesta

- **Desafío seleccionado:** pestaña Riesgos → **RIE-03 · Anticipar el deterioro de pago antes del atraso**
- **Nombre de la solución** (57/80):

```text
Alerta temprana explicada: llegar antes del primer atraso
```

## Paso 2 · Concepto de solución

**¿En qué consiste su solución y cómo aborda la problemática del desafío?** (obligatoria) — 1222/2000

```text
Alerta temprana explicada para la gestión preventiva de la cartera, dirigida al gestor o asesor que acompaña a los microempresarios. En cada corte entrega una cola corta y priorizada de clientes que hoy están al día pero muestran señales de deterioro; cada alerta trae el porqué, su nivel de incertidumbre y una acción preventiva propuesta. El gestor aprueba, edita o descarta.

Qué aborda del desafío: el deterioro gradual antes del primer atraso, usando información histórica, comportamiento financiero y variaciones frente a los patrones habituales del cliente; y la necesidad de distinguir señales relevantes de fluctuaciones normales, evitando alertas innecesarias y decisiones con información insuficiente.

Nuestra lectura, a validar con el owner: sin esa distinción se actúa tarde o se alerta de más, y se cansa al gestor y al cliente.

Respeta las restricciones del desafío: protección de datos personales (identificadores, sin datos reales), revisión de sesgos, incertidumbre explícita (sin historial suficiente no se alerta), alertas sustentadas en evidencia, revisión humana y ninguna decisión crediticia automática: la alerta no cambia la calificación, el límite, la tasa ni las condiciones de ningún cliente.
```

**¿Cómo funcionaría su solución?** (obligatoria) — 1210/2000

```text
1. Entrada: historial de pagos, saldos, actividad en cuenta y variables de riesgo del cliente hasta la fecha de corte (nada posterior).
2. Variables: comparan al cliente con su propio pasado y con su sector.
3. Modelo: estima la probabilidad calibrada de pasar a atraso, con un rango de incertidumbre; con historial insuficiente no alerta.
4. Filtro señal vs. fluctuación: solo pasa lo persistente, no estacional y visible en al menos dos familias de señales (ingresos, conducta de pago, endeudamiento externo). La disponibilidad de actividad en cuenta y de deuda externa es un supuesto; el esquema se adapta a lo que haya.
5. Cola priorizada según la capacidad del gestor.
6. Agente acotado: propone canal, momento y borrador de mensaje citando la evidencia; no puede prometer condiciones crediticias.
7. Decisión humana: el gestor aprueba, edita o descarta; queda en bitácora. Nada se envía ni se ejecuta solo.
8. Medición: un backtest compara con y sin la solución frente a reglas simples: casos detectados, días de anticipación y falsos positivos.

En el prototipo la cola se recalcula por fecha de corte (mensual en nuestros datos sintéticos); una cadencia diaria sería un supuesto a validar con el owner.
```

**¿Qué diferencia su solución de otras alternativas existentes?** (obligatoria) — 612/1000

```text
No es un puntaje de mora ni una regla de días de atraso. (1) Anticipa en clientes que hoy están al día, donde la regla «ya tiene atraso» no distingue. (2) Separa señal de fluctuación con un filtro explícito de persistencia, estacionalidad y convergencia, para cuidar los falsos positivos. (3) Entrega una acción explicada, con evidencia e incertidumbre, no solo un número. (4) Mide su costo en falsos positivos frente a reglas simples. (5) Deja la decisión en la persona y registra cada paso. El agente de IA no conversa por conversar: redacta dentro de límites escritos en el código y cita la evidencia que usa.
```

**Material visual complementario** (opcional, PDF/PNG/JPG, hasta 3 de 10 MB): subir los archivos de `adjuntos/`:

- `Yupana-Labs_RIE-03_presentacion.pdf`
- `Yupana-Labs_RIE-03_ficha.pdf`
- `Yupana-Labs_RIE-03_flujo.png`

**Enlace complementario** (opcional): dejar vacío

## Paso 3 · Impacto esperado

**¿Qué impacto generaría su solución y cómo contribuiría al resultado esperado del desafío?** (obligatoria) — 1876/2000

```text
Contribución al resultado esperado: detectar antes para reducir incumplimientos, mejorar la calidad de la cartera y proteger la salud financiera del microempresario.

KPI propuesto (a validar con el owner): tasa de paso a atraso de más de 30 días en la cartera alertada, con y sin intervención (el umbral coincide con la referencia de deterioro que Riesgos indicó en la inmersión). Secundarios: precisión en el top-k, falsos positivos y días de anticipación. No tenemos línea base oficial y no prometemos una cifra sobre la cartera de la Caja.

Evidencia preliminar, medida sobre datos sintéticos propios: entre clientes al día solo el 0,7 % pasa a atraso de más de 30 días en 60 días; un modelo de árboles los ordena con un AUC de 0,84 y el 10 % mejor puntuado concentra alrededor de 6 de cada 10 de esos casos, unas 6 veces lo que lograría el azar. La precisión absoluta es baja (4,7 %) porque el evento es raro; por eso la acción propuesta es de bajo costo y el filtro se medirá como reducción de falsos positivos.

Contraste con datos reales: un estudio publicado con unos 50 000 microcréditos de Huancayo (Arriola León y Ghodrat, 2026) obtuvo un AUC de 0,73 con datos del otorgamiento, sin comportamiento mensual. Nuestro 0,84 sale de datos sintéticos más simples que la realidad y es probablemente optimista. Además, un ensayo en Uganda (Cadena y Schoar, 2011) halló que recordar antes del vencimiento mejora el pago puntual: una acción preventiva barata tiene respaldo, aunque su efecto aquí está por medir.

Ilustración aritmética (escenario, no estimación): si la gestión temprana evitara el 10, 20 o 30 % de los pasos a atraso de los casos capturados, de cada 100 créditos que pasarían a atraso se evitarían unos 6, 12 o 18.

Para el gestor: dedica su tiempo a una lista corta con el motivo claro, en lugar de revisar toda la cartera o reaccionar cuando ya hay mora.
```

## Paso 4 · Enfoque tecnológico

**¿Cuál será el enfoque tecnológico de su solución?** (obligatoria) — 1195/2000

```text
Python, FastAPI, Pydantic, pandas, scikit-learn (LightGBM solo si aporta), SQLite, Pydantic AI, React con Vite y Tailwind, y pytest.

Arquitectura de punta a punta: datos sintéticos → variables calculadas solo con información hasta la fecha de corte (para no usar el futuro) → modelo calibrado, con validación temporal y rango de incertidumbre por remuestreo → filtro de señal → cola → agente acotado → API con bitácora → interfaz del gestor. El backtest usa las mismas variables.

El proveedor del modelo de lenguaje es intercambiable (Claude, OpenAI o un modelo local) y hay un modo sin red con plantillas, así que el prototipo no depende de una política de IA externa. El prototipo no se conectará a sistemas de la Caja.

Por qué es adecuado: con pocos casos positivos, un modelo simple y calibrado es más interpretable y estable que algo complejo; el filtro responde al requisito de evitar alertas innecesarias; y el agente solo redacta dentro de reglas escritas en el código.

Datos personales y sesgos: se trabaja con identificadores y señales numéricas; sexo y edad no entran al modelo (solo sirven para auditar por grupo); la zona solo define cohortes de comparación y también se audita.
```

- **Punto de partida:** Desarrollo a partir de soluciones o componentes preexistentes

**Desarrollo preexistente 1:** nombre «Generador de datos sintéticos de cartera MYPE y auditoría de su dificultad» · tipo: Módulo o componente de software · nivel: Funcional en entorno de prueba · titularidad: Propio (equipo o integrante)

**Describan los desarrollos tecnológicos preexistentes indicados anteriormente (pregunta 4.3)** (obligatoria) — 1013/2000

```text
Solo hay dos herramientas de datos nuestras, creadas el 21.11.2026 (titular: el equipo Yupana Labs; sin licencias de terceros):

1. Un generador de datos 100 % sintéticos de una cartera de microempresarios (5.000 clientes ficticios y 34 meses de historia), con 24 pruebas automáticas y semilla fija. No contiene el modelo, el filtro, el agente, la API, la interfaz ni el backtest.

2. Un script de auditoría que comprueba si una regla simple resuelve el problema con esos datos; de él salen las cifras medidas que citamos. No forma parte de la solución ni se reutiliza en ella.

Cómo se aprovechan: el generador alimenta el prototipo; la medición del evento se escribe desde cero. Además usamos librerías de código abierto bajo sus licencias.

El material de comunicación (identidad, láminas, maquetas ilustrativas y video explicativo) no es un desarrollo tecnológico de la solución. No reutilizamos código de empleadores ni de clientes, y no usamos datos reales.

Todo lo demás se construye durante el hackathon.
```

**¿Identifican alguna limitación o riesgo técnico relevante para el desarrollo de su solución?** (opcional) — 571/800

```text
1) Pocos casos positivos en datos sintéticos: más clientes e intervalos por remuestreo. 2) Falsos positivos: filtro de señal y métrica explícita. 3) Uso accidental de información futura: variables por fecha de corte y prueba automática. 4) El efecto de intervenir no está en los datos: se muestra como escenario. 5) Tiempo: unas 31,5 horas-persona de 32; se parte de un mínimo viable y se recorta en orden el modelo de lenguaje, los árboles y la auditoría de sesgos completa. 6) Las señales de cuenta o de deuda externa pueden no existir en la Caja: el esquema se adapta.
```

## Paso 5 · Alcance del prototipo

**¿Qué nuevos desarrollos o adaptaciones realizarán durante el hackathon?** (obligatoria) — 1243/2000

```text
Funcionalidad crítica: cola preventiva con explicación y acción propuesta, con aprobación humana. Dada una fecha de corte, el sistema calcula el riesgo de cada crédito al día con información hasta esa fecha, entrega los clientes priorizados tras el filtro, muestra 2 a 3 señales contrastadas con su historial y su sector con su incertidumbre, propone la intervención y registra la decisión del gestor.

Desarrollos nuevos del hackathon: preparación de variables, modelo de deterioro calibrado, filtro señal vs. fluctuación, agente de intervención con guardas, API con bitácora, interfaz de cola y caso, y backtest.

Criterios de aceptación: con la misma fecha y los mismos datos la cola es idéntica; no usa información posterior al corte; una caída de un solo mes propia de la temporada no alerta y un deterioro gradual persistente sí; el agente nunca promete condiciones crediticias; ninguna parte envía ni ejecuta nada.

Plan base (mínimo viable): cola con puntaje e incertidumbre, explicación, filtro, intervención por plantillas, aprobación con bitácora, backtest y pruebas. Si sobra tiempo, en este orden: modelo de lenguaje para redactar, árboles además de regresión logística, auditoría de sesgos completa y varios escenarios de efecto.
```

**¿Qué resultado funcional esperan demostrar al finalizar el hackathon?** (obligatoria) — 714/1500

```text
Caso de uso: Rosa, asesora de negocios (personaje ficticio), abre la cola del corte.
1) Ve los clientes al día con riesgo, ordenados.
2) Abre un taller cuyos abonos caen tres meses seguidos mientras su sector no cae.
3) Revisa evidencia e incertidumbre y aprueba la acción propuesta, que queda en bitácora.
4) Se muestra un cliente con una fluctuación normal que no alertó.
5) Cierra con el backtest con y sin la solución: casos detectados, días de anticipación y falsos positivos frente a reglas de atraso.

Verificación: pruebas automáticas (sin uso del futuro, fluctuación vs. deterioro, guardas del agente), reporte de validación y un número antes y después. El efecto de intervenir se presenta como escenario.
```

**¿Qué funcionalidades o capacidades quedarán fuera del alcance del prototipo?** (opcional) — 262/800

```text
Envío real de mensajes; integración con sistemas de la Caja; decisiones o condiciones crediticias; recalibración continua en producción; uso de datos reales; y la cadencia diaria (en el prototipo se recalcula por fecha de corte). Quedan para una etapa posterior.
```

## Paso 6 · Datos e insumos

- **Tipo de requerimiento:** No requerimos datos ni insumos

## Antes de enviar: tres declaraciones que marca la persona

- [ ] La propuesta fue **revisada y acordada por los integrantes del equipo**, la información es veraz y cumple las bases. (Para marcarla, Glem, Antonio y David deben haberla visto.)
- [ ] Identificamos las soluciones y componentes preexistentes, su titularidad y condiciones de uso.
- [ ] Entendemos que, de ser seleccionados, haremos un desarrollo nuevo o adaptación sustantiva y demostraremos la funcionalidad crítica.

**Guardar y salir** conserva un borrador; enviar es definitivo hasta donde indique la plataforma.
