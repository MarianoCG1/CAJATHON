# COM-01 — formulario «Concept Solution», listo para pegar

**Fecha límite:** jueves 26 de noviembre, 11:59 p. m. (hora de Perú). **Se envía un solo desafío por equipo.**
Cada bloque gris se copia entero en su campo. El conteo es de caracteres frente al máximo del formulario.

## Paso 1 · Identificación de la propuesta

- **Desafío seleccionado:** pestaña Comercial → **COM-01 · Encontrar oportunidades donde otros no ven clientes**
- **Nombre de la solución** (44/80):

```text
Brújula comercial que aprende de cada visita
```

## Paso 2 · Concepto de solución

**¿En qué consiste su solución y cómo aborda la problemática del desafío?** (obligatoria) — 1246/2000

```text
Una herramienta para el analista que cada semana propone dónde prospectar, combinando la ruta que ya haría (su experiencia y sus referidos) con zonas poco exploradas que muestran señales de potencial de inclusión financiera.

El problema que abordamos: la prospección aprende sobre todo de donde ya se va. Una zona que no se visita no genera información, y la falta de información puede confundirse con falta de potencial. Así quedan oportunidades inadvertidas.

Cada zona comercial llega con una ficha: qué se sabe (negocios, actividad, cobertura financiera, distancia y señales digitales públicas de negocios), de qué fuente y fecha, qué NO se sabe y qué validar en campo. El analista ajusta y aprueba el plan, registra el resultado de cada visita en segundos y el sistema aprende: la semana siguiente reparte mejor el esfuerzo.

Complementa los mecanismos actuales de prospección, no los reemplaza. Respeta las restricciones del desafío: la unidad es la zona, no la persona; no se recopilan datos personales ni se infieren características sensibles; las fuentes se usan según sus condiciones; la falta de dato no baja el puntaje de una zona; y una señal nunca se presenta como necesidad confirmada, capacidad de pago o elegibilidad crediticia.
```

**¿Cómo funcionaría su solución?** (obligatoria) — 1229/2000

```text
1. Reúne por zona señales públicas (censos, puntos de atención financiera, mapas, mercados y señales digitales de negocios), cada una con fuente y fecha. En el prototipo son datos sintéticos con la misma estructura.
2. Un modelo estima, para cada zona, la probabilidad de que una visita termine en un cliente nuevo, con un rango. Donde faltan datos, el rango es más ancho; el puntaje no se castiga.
3. El planificador arma la semana según la capacidad del analista: una parte de su ruta habitual, otra de descubrimiento y una cuota mínima para las zonas menos conocidas.
4. Un agente acotado redacta la ficha de cada zona: evidencia citada, dudas abiertas, qué preguntar y qué canal o actividad probar. No habla de personas ni de aprobaciones.
5. El analista aprueba, cambia o quita zonas; su motivo queda registrado.
6. En campo registra con un toque: sin interés, interesado, solicitó o desembolsado.
7. Con eso se actualizan las estimaciones y el reparto entre ruta habitual y descubrimiento según lo que va rindiendo cada una.
8. Un tablero de seguimiento muestra captación por visita, conversión, costo por cliente nuevo, primer acceso y cómo se reparten las visitas entre zonas urbanas, rurales y de poca presencia digital.
```

**¿Qué diferencia su solución de otras alternativas existentes?** (obligatoria) — 492/1000

```text
No es un mapa de calor ni un puntaje fijo. (1) Distingue «poco potencial» de «poca información» y reserva visitas para averiguarlo. (2) Aprende del resultado real de las visitas en lugar de quedarse con la primera foto. (3) Suma el conocimiento del analista como una fuente del plan, no lo sustituye. (4) Muestra cuándo NO gana: si la ruta habitual ya acierta, el plan se inclina hacia ella. (5) Audita el reparto de visitas para no excluir zonas por ser rurales, informales o poco digitales.
```

**Material visual complementario** (opcional, PDF/PNG/JPG, hasta 3 de 10 MB): subir los archivos de `adjuntos/`:

- `Yupana-Labs_COM-01_presentacion.pdf`
- `Yupana-Labs_COM-01_ficha.pdf`
- `Yupana-Labs_COM-01_flujo.png`

**Enlace complementario** (opcional): dejar vacío

## Paso 3 · Impacto esperado

**¿Qué impacto generaría su solución y cómo contribuiría al resultado esperado del desafío?** (obligatoria) — 1673/2000

```text
Contribución al resultado esperado: más oportunidades identificadas en zonas poco exploradas, prospección más efectiva, decisiones con evidencia e inclusión financiera.

KPI principal: clientes nuevos por cada 100 visitas, es decir, con el mismo esfuerzo comercial. Complementarios: conversión, desembolsos, costo por cliente nuevo, primer acceso al sistema financiero y visitas a zonas poco atendidas. Horizonte propuesto: 12 semanas (supuesto), doce ciclos de aprendizaje. No tenemos línea base oficial y no prometemos una cifra para la Caja.

Evidencia preliminar sobre datos sintéticos propios (medianas de 200 simulaciones, clientes nuevos por 100 visitas). Comparamos tres supuestos sobre la realidad. «Solo cartera» es una simplificación nuestra: visitar únicamente donde ya hay clientes; no representa cómo prospecta hoy la Caja.
- Hay oportunidades ocultas: solo cartera 7,3; puntaje fijo 11,0; nuestra mezcla 11,6.
- Donde ya hay clientes es donde está el potencial: solo cartera 13,8; fijo 10,7; mezcla 13,0.
- Los datos públicos dicen poco: solo cartera 7,2; fijo 9,5; mezcla 14,1.
Como nadie sabe de antemano en qué caso está, importa el peor resultado: la mezcla quedó en los tres casos en 91 % o más de la mejor estrategia comparada (incluida una de solo descubrimiento); «solo cartera» cayó hasta 47 % y el puntaje fijo hasta 62 %. En 11 variaciones de los parámetros de la simulación, la mezcla nunca bajó de 86 % y siempre tuvo el mejor peor caso. Cuando el potencial está donde ya hay clientes, gana «solo cartera»: por eso complementamos.

Validación posterior en la Caja: con igual capacidad, parte de las agencias usa el plan y parte trabaja como hoy.
```

## Paso 4 · Enfoque tecnológico

**¿Cuál será el enfoque tecnológico de su solución?** (obligatoria) — 1060/2000

```text
Python, FastAPI, Pydantic, pandas, scikit-learn, SQLite, Pydantic AI, React con Vite y Tailwind, mapa sobre OpenStreetMap y pytest.

Arquitectura de punta a punta: señales por zona con fuente y fecha → modelo de potencial → esquema bayesiano por zona, que usa ese modelo como punto de partida y lo corrige con los resultados → planificador con muestreo de Thompson, que respeta capacidad, distancia, agotamiento de la zona y cuota de exploración → agente acotado para la ficha → API con bitácora → interfaz de semana, mapa y registro → backtest y auditoría de reparto.

Por qué es adecuado: el problema no es solo predecir, es decidir dónde ir sabiendo poco. Un esquema bayesiano es simple, explicable, funciona con pocos datos y expresa la incertidumbre. El agente solo redacta con la evidencia de la zona; sus guardas están escritas en el código.

El proveedor del modelo de lenguaje es intercambiable (Claude, OpenAI o un modelo local) y hay modo sin red con plantillas. El prototipo no se conecta a sistemas de la Caja. No se trabaja con datos de personas.
```

- **Punto de partida:** Desarrollo a partir de soluciones o componentes preexistentes

**Desarrollo preexistente 1:** nombre «Generador de territorio sintético y script de auditoría de estrategias de prospección» · tipo: Módulo o componente de software · nivel: Funcional en entorno de prueba · titularidad: Propio (equipo o integrante)

**Describan los desarrollos tecnológicos preexistentes indicados anteriormente (pregunta 4.3)** (obligatoria) — 961/2000

```text
Dos herramientas nuestras creadas el 25.11.2026 (titular: el equipo Yupana Labs; sin licencias de terceros):

1. Un generador de territorio 100 % sintético: 120 zonas ficticias con señales simuladas y huecos, un historial de visitas y una verdad oculta para evaluar, con 7 pruebas automáticas y semilla fija.

2. Un script de auditoría que simula y compara estrategias de visita; de él salen las cifras que citamos. Contiene una versión mínima de la estrategia de aprendizaje: no es la solución, no tiene planificador de rutas, agente, API ni interfaz, y no se reutiliza en el prototipo. El planificador se escribirá desde cero en el evento.

Cómo se aprovechan: el generador alimenta el prototipo. Además usamos librerías de código abierto bajo sus licencias.

El material de comunicación (identidad, láminas y maquetas ilustrativas) no es un desarrollo tecnológico de la solución. No reutilizamos código de empleadores ni de clientes y no usamos datos reales.
```

**¿Identifican alguna limitación o riesgo técnico relevante para el desarrollo de su solución?** (opcional) — 421/800

```text
1) Las cifras dependen de nuestros supuestos: por eso se prueban tres escenarios. 2) Pocas visitas por zona para aprender: punto de partida con el modelo y zonas parecidas. 3) Si el analista no registra, no hay aprendizaje: registro de un toque. 4) Fuentes públicas antiguas o incompletas: fecha visible y rango más ancho. 5) Sesgo hacia zonas fáciles: cuota de exploración y auditoría. 6) Tiempo: 31 horas-persona de 32.
```

## Paso 5 · Alcance del prototipo

**¿Qué nuevos desarrollos o adaptaciones realizarán durante el hackathon?** (obligatoria) — 992/2000

```text
Funcionalidad crítica: plan semanal de prospección que combina ruta habitual y descubrimiento, con ficha de evidencia por zona, aprobación del analista y actualización al registrar resultados.

Desarrollos nuevos del hackathon: modelo de potencial con incertidumbre, planificador adaptativo con cuota de exploración, agente de ficha con guardas, API con bitácora, interfaz de semana, mapa y registro, backtest y auditoría de reparto.

Criterios de aceptación: con los mismos datos y semilla el plan es idéntico; la cuota de exploración se cumple; una zona sin dato digital no baja de puntaje por eso; al registrar resultados el plan siguiente cambia en la dirección esperada; la ficha nunca menciona personas, elegibilidad ni capacidad de pago; ninguna parte contacta ni ejecuta nada por sí sola.

Mínimo viable: planificador, ficha por plantilla, aprobación y registro, backtest y pruebas. Si sobra tiempo, en este orden: modelo de lenguaje para redactar, mapa y cuadro de equidad detallado.
```

**¿Qué resultado funcional esperan demostrar al finalizar el hackathon?** (obligatoria) — 704/1500

```text
Caso de uso: Carmen, analista de negocios (personaje ficticio).
1) Abre su semana: 15 salidas, unas de su ruta y otras de descubrimiento, cada una con el porqué.
2) Entra a una zona poco conocida: ve qué se sabe, qué no y qué validar.
3) Quita una zona con un motivo y aprueba el plan.
4) Registra los resultados de las visitas.
5) La semana siguiente el plan cambia y se ve por qué.
6) Cierra con el backtest: clientes nuevos por 100 visitas frente a la ruta habitual y a un puntaje fijo, en los tres escenarios, y el reparto de visitas por tipo de zona.

Verificación: pruebas automáticas (reproducibilidad, cuota, falta de dato, guardas de la ficha), reporte de validación y un número antes y después.
```

**¿Qué funcionalidades o capacidades quedarán fuera del alcance del prototipo?** (opcional) — 208/800

```text
Navegación o ruteo calle por calle; integración con sistemas de la Caja; listas de personas o contactos; evaluación o preaprobación de créditos; extracción automática de redes sociales; y uso de datos reales.
```

## Paso 6 · Datos e insumos

- **Tipo de requerimiento:** No requerimos datos ni insumos

## Antes de enviar: tres declaraciones que marca la persona

- [ ] La propuesta fue **revisada y acordada por los integrantes del equipo**, la información es veraz y cumple las bases. (Para marcarla, Glem, Antonio y David deben haberla visto.)
- [ ] Identificamos las soluciones y componentes preexistentes, su titularidad y condiciones de uso.
- [ ] Entendemos que, de ser seleccionados, haremos un desarrollo nuevo o adaptación sustantiva y demostraremos la funcionalidad crítica.

**Guardar y salir** conserva un borrador; enviar es definitivo hasta donde indique la plataforma.
