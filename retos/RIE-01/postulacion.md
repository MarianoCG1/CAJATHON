# Postulación RIE-01 — texto para pegar en la plataforma

Desafío elegido: RIE-01 · Microfinanzas resilientes al clima. Equipo: Yupana Labs.

## 1. Problema abordado

Según el desafío, lluvias intensas, inundaciones o sequías pueden afectar la actividad económica de los microempresarios, sobre todo de quienes están en zonas vulnerables o tienen actividades sensibles al clima, y con ello sus ingresos y su capacidad de pago. El reto es anticipar esos riesgos y orientar estrategias preventivas que fortalezcan la resiliencia de los negocios que financia Caja Trujillo. Debemos hacerlo sin asumir que estar expuesto a una amenaza significa pérdida o incumplimiento, reconociendo que los escenarios climáticos son inciertos, y con recomendaciones sustentadas en evidencia que respeten la protección de datos y las políticas de riesgo de la Caja.

## 2. Concepto de solución

Radar Climático de Cartera (nombre de trabajo). El analista elige un escenario, por ejemplo una inundación severa en la costa norte, y la herramienta responde tres preguntas por separado: cuánta cartera está expuesta, cuánta es probablemente afectada y cuánta mora adicional cabe esperar, cada una con un rango y no con una cifra única. Un modelo combina la amenaza en el sector del cliente, la vulnerabilidad de su actividad y su colchón financiero, y su carga de deuda. Un mapa y un ranking priorizan zonas y clientes según las visitas que cada agencia puede realizar (capacidad supuesta, a confirmar). Un agente propone, con la evidencia que lo sustenta, acciones de un catálogo que la Caja debe validar (supuesto), por cliente o por zona: alerta anticipada, visita, reprogramación, asesoría de continuidad y otras, a confirmar. La decisión es siempre del gestor: nada se ejecuta automáticamente.

## 3. Impacto esperado en el KPI

El KPI oficial y la línea base están a validar con el owner; no los inventamos. Proponemos medir el porcentaje de cartera afectada que se identifica antes del evento con la capacidad disponible, la precisión de la priorización frente a reglas simples (por zona o por monto), la pérdida evitada estimada, siempre como rango, y la continuidad de los negocios afectados. La medición será un backtest reproducible sobre eventos simulados con resultados ocultos, con y sin la solución. La cifra de impacto esperada está a validar con el owner cuando exista la línea base. Esperamos un efecto moderado y verificable: priorizar mejor que el azar y que las reglas simples con la capacidad real de visitas, con rangos de incertidumbre calibrados, y no una predicción casi perfecta. Evidencia preliminar, medida sobre datos sintéticos propios (una sola semilla) y no sobre la Caja: visitando cerca del 8 % de la cartera durante dos semanas, el azar captura cerca del 8 % de los incumplimientos y un modelo de referencia entrenado con la historia cerca del 20 %, unas 2,5 veces más; es el orden de magnitud que esperamos demostrar. El efecto de las acciones preventivas (pérdida evitada y continuidad con acciones) se simula con efectividades supuestas y se reporta como rango: es un supuesto del equipo, no una medición de impacto.

## 4. Enfoque tecnológico

Python, FastAPI y React. Un modelo estadístico calibrado con eventos históricos y validado en el tiempo; simulación de escenarios para entregar rangos; optimización para repartir las acciones entre los gestores disponibles; y un agente con herramientas acotadas, cuyo modelo de lenguaje es intercambiable (Claude, OpenAI o local) y que también funciona sin IA externa. El uso de IA externa está a confirmar con la política de la Caja.

## 5. Tecnología preexistente

Antes del evento existen solo: (1) un generador de datos sintéticos de este desafío, con sus 40 pruebas automáticas, creado el 21.11.2026 (titular: el equipo); (2) un script de auditoría que mide cuán difícil es ese conjunto de datos y que entrena un modelo de referencia únicamente con ese fin: no es el modelo de la solución y no se reutiliza; y (3) librerías de código abierto bajo sus licencias. Sin datos reales ni código de terceros. Si la Caja entrega datos o mapas, los usaremos en su lugar. Todo lo demás se construye durante el evento.

## 6. Funcionalidad crítica

Un solo flujo de punta a punta: elegir un escenario, ver cartera expuesta, afectada y en riesgo de mora con rango, priorizar en mapa y ranking, recibir el plan que sugiere el agente, aprobarlo o rechazarlo, y medir el KPI con y sin la solución. Se desarrolla íntegramente en la fase presencial: modelo, escenarios, mapa, priorización, agente, API, interfaz y backtest. La solución no existe antes del hackathon; solo la auditoría de dificultad de los datos (§5).

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta, con pruebas automáticas, reporte de validación y una demostración de cinco minutos que termina con el número antes y después del KPI en un evento más severo que la historia. Los resultados serán sobre datos sintéticos; el impacto real depende de los datos y las acciones de la Caja, a validar con el owner.

## 8. Factibilidad y dependencias

Alcance estimado en 32 horas-persona (cuatro personas, ocho horas cada una). Comprometemos una versión mínima que funciona de punta a punta: escenario, cartera expuesta, afectada y en mora con rango analítico, ranking en un mapa de puntos, plan del agente con aprobación humana y backtest de K1 y K2 en al menos tres eventos de prueba, uno más severo que la historia. Si el tiempo alcanza, se agregan la simulación por muestreo, la redacción con IA, la asignación óptima, K3 y K4 y los seis eventos. Hay hitos de control a las 13:00 y a las 16:30 del día 1 y al cierre de pruebas. Evidencia medida sobre nuestros datos sintéticos, no sobre la Caja: una fórmula simple de tres factores (amenaza del distrito, sensibilidad de la actividad e intensidad del escenario) ya captura cerca del 18 % de los incumplimientos con visitas de dos semanas, así que la ventaja del modelo no está en la precisión puntual sino en la resolución de sector y en rangos calibrados; por eso medimos contra esa fórmula y no solo contra el azar. Dependencias a confirmar con la Caja: KPI y línea base, datos disponibles, política de IA externa y catálogo de acciones permitido por sus políticas de riesgo.
