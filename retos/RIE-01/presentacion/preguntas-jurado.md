# RIE-01 — preguntas esperables del jurado y respuestas honestas

Las respuestas separan lo que está medido sobre datos sintéticos propios, lo que es supuesto y lo que depende de la Caja.

## 1. ¿Cuál es el impacto en el KPI?

No hay línea base oficial, así que no prometemos una cifra sobre la Caja. Sobre datos sintéticos propios, con visitas de dos semanas (cerca del 8 % de la cartera) el azar captura cerca del 8 % de los incumplimientos, una fórmula de tres factores cerca del 18 % y un modelo de referencia cerca del 20 %. Esperamos un efecto moderado y verificable, de unas 2,5 veces el azar.

## 2. ¿No es solo un mapa de calor?

No. Un mapa de calor muestra amenaza; nosotros separamos expuesta, afectada y mora adicional, mostramos rangos, priorizamos con la capacidad real de visitas y proponemos acciones con evidencia. Y lo medimos contra reglas simples en eventos con resultado oculto.

## 3. Una regla de zona más actividad ya captura casi lo mismo. ¿Qué aporta el modelo?

Es cierto: en nuestros datos la ventaja del modelo sobre esa regla es pequeña, unos dos puntos de captura. Por eso no la vendemos como precisión puntual. Lo que aporta es la resolución de sector, los rangos calibrados, la asignación bajo capacidad y la trazabilidad de cada recomendación. El criterio de aceptación es no quedar por debajo de esa regla y superar al azar y a las reglas de zona y de saldo.

## 4. ¿Exposición significa pérdida?

No, y el diseño lo evita: mostramos tres cifras separadas. Estar expuesto a una amenaza no implica necesariamente pérdida o incumplimiento; por eso la cifra de afectados y la de mora adicional se estiman aparte, con su incertidumbre.

## 5. ¿Cómo manejan la incertidumbre de los escenarios?

Cada cifra se entrega como rango (p10–p50–p90) y la solución se evalúa con eventos distintos del escenario ex ante, incluido uno más severo que la historia.

## 6. ¿Qué parte es inteligencia artificial?

El modelo calibrado en tres capas, la simulación de escenarios, la optimización de visitas y un agente que propone acciones con evidencia. El mínimo comprometido usa rango analítico y un agente determinista; el modelo de lenguaje y la simulación por muestreo se añaden si hay tiempo.

## 7. ¿Cabe en 8 horas por persona?

Estimamos 32 horas-persona, pero en el escenario pesimista son unas 45. Por eso comprometemos una versión mínima de punta a punta: escenario, tres cifras con rango analítico, ranking en un mapa de puntos, plan con aprobación y backtest de K1 y K2 en al menos tres eventos.

## 8. ¿Y si la Caja no entrega datos ni mapas?

No los necesitamos para el prototipo: el generador propio produce clientes, geografía, mapa de amenaza con error y eventos de prueba con resultado oculto. Si la Caja aporta datos o mapas, los usaremos en su lugar.

## 9. ¿Qué acciones puede proponer el agente?

Las de un catálogo que la Caja debe validar: alerta anticipada, visita, reprogramación preventiva, ampliación de plazo, capital de reposición, asesoría de continuidad y microseguro si existe. El gestor aprueba o rechaza; nada se ejecuta solo.

## 10. ¿Qué es preexistente?

El generador de datos sintéticos con 40 pruebas y un script de auditoría de dificultad, del equipo, creados el 21.11.2026. Modelo, escenarios, mapa, priorización, agente, API, interfaz y backtest se construyen en el evento.
