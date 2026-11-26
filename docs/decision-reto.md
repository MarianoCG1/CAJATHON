# Decisión: qué desafío postulamos (25.11, noche)

**Hay que enviar UN solo concepto antes del jueves 26.11 a las 11:59 p. m.** Material confidencial: resumen con nuestras palabras.

## 1. Dónde se concentraron las dudas

No vemos los tickets de otros equipos, así que **no se puede saber cuántos equipos preguntó por cada reto**. Lo que sí es visible:

| Reto | Preguntas frecuentes publicadas | Expediente reescrito el 25.11 | Nuestra consulta |
|---|---|---|---|
| NEG-01 | **10** | **Sí** (7:02 p. m.) | Respondida |
| RIE-01 | **4** | **Sí** (7:02 p. m.) | No consultamos |
| NEG-03 | 0 | No | Respondida |
| COM-01 | 0 | No | Respondida (texto cortado en la plataforma) |
| COM-02 | 0 | No | Respondida: no comparten nada |
| RIE-03, NEG-02, RIE-02 | 0 | No | No consultamos |

**Inferencia (no dato):** que NEG-01 y RIE-01 tengan preguntas frecuentes y expediente nuevo sugiere que fueron los más consultados y quizá los más elegidos. También puede deberse a que sus owners son más activos.

## 2. Los ocho desafíos en breve

| Reto | Qué pide | Qué sabemos del owner | Lo que tenemos |
|---|---|---|---|
| **RIE-03** Deterioro de pago | Anticipar, antes del primer atraso, qué microempresarios se están deteriorando, sin alertar de más | Solo el expediente | Concepto revisado, evidencia medida, deck, ficha, video, formulario listo |
| **NEG-01** Plan de pagos al ciclo del negocio | Estimar el ciclo económico de cada negocio y armar desde el desembolso un plan de cuotas variables; compararlo con cuota fija | Muy detallado: reglas de cálculo, mínimo esperado (modelo de ciclo, motor de plan, explicación) y criterios de evaluación | Borrador inicial |
| **NEG-02** Open Finance | Aprovechar datos de otras entidades con consentimiento para dar más valor al cliente | Solo el expediente | Concepto revisado, evidencia, deck y ficha |
| **NEG-03** Continuidad al cambiar el analista | Que el cliente no se pierda cuando cambia su analista | Horizonte de 2 a 3 meses; fuga por no renovación y compra de deuda; éxito = renovación, saldo retenido y contacto oportuno | Borrador inicial |
| **RIE-01** Clima | Identificar zonas, sectores y clientes vulnerables y estimar exposición e impacto en la cartera y los estados financieros | Reescrito y ampliado: más segmentos de cartera y estados financieros; cuenta con medidas para El Niño | Concepto sobre el alcance anterior (habría que ampliarlo) |
| **RIE-02** Redes de fraude | Detectar redes sospechosas entre solicitudes sin acusar a clientes legítimos | Solo el expediente | Concepto revisado, evidencia, deck y ficha |
| **COM-01** Nuevos clientes | Encontrar dónde captar clientes con potencial de inclusión | KPI = nuevos clientes; fuentes públicas permitidas; evitar sesgos | Borrador inicial |
| **COM-02** Incentivos | Esquemas de incentivos que equilibren colocación, mora y colaboración | No comparten nada del esquema actual | Borrador inicial |

## 3. Comparación de los candidatos

| Criterio | RIE-03 | NEG-01 | NEG-03 |
|---|---|---|---|
| Claridad de lo que quiere el owner | Media (solo expediente) | **Alta** | Media-alta |
| Lo ya construido para postular | **Alto** | Bajo | Bajo |
| Encaje con el equipo | **Alto** (modelos y agentes) | Alto en negocio (Antonio) y datos (Glem) | Medio |
| Evidencia que podemos mostrar hoy | **Sí, medida** | No | No |
| Riesgo de construirlo en ~8 h por persona | Medio (31,5 h de 32) | Medio-alto: cálculo financiero exacto y modelo de ciclo sin datos de verdad | Medio |
| Competencia probable (inferencia) | Sin señales | Probablemente alta | Sin señales |

## 4. Recomendación: RIE-03

1. **Está listo y revisado.** Los otros candidatos habría que escribirlos desde cero en unas 24 horas.
2. **Tiene evidencia propia.** Sobre datos sintéticos propios, entre clientes al día el modelo ordena con AUC 0,84 y el 10 % mejor puntuado concentra alrededor de 6 de cada 10 casos (unas 6 veces el azar). Con regresión logística, la opción más simple, el resultado es el mismo.
3. **Encaja con nuestro perfil:** modelo predictivo, filtro de señal y agente con aprobación humana.
4. **Cabe en el evento** con un mínimo viable definido.
5. **Impacto fácil de explicar:** llegar antes del primer atraso. El umbral de más de 30 días coincide con la referencia de deterioro que Riesgos dio en otro desafío.

**Debilidades que hay que aceptar:** no tenemos respuesta del owner; una «alerta temprana de mora» es una idea que otros equipos pueden proponer, así que la diferencia está en el filtro de falsos positivos y la evidencia; las horas del evento van sin holgura; y la precisión absoluta es baja porque el evento es raro.

## 5. Cuándo elegir NEG-01 en lugar de RIE-03

Solo si **Antonio y Glem se comprometen esta noche** a dominar el cálculo (TEA a tasa diaria, seguros, orden de pago, tope de cuota sobre utilidad por etapa) y el modelo de ciclo con fuentes públicas. A favor: el owner dijo con precisión qué quiere ver y que no medirá mora real. En contra: se parte de cero y probablemente haya más competencia.

## 6. Lo que se necesita para enviar

- Que los cuatro revisen el `retos/RIE-03/entrega/formulario.md` y sus tres adjuntos: la plataforma pide declarar que el equipo la acordó.
- Marcar las tres declaraciones y enviar antes del jueves 11:59 p. m. (mejor no apurar hasta la última hora).
