# RIE-03 — preguntas esperables del jurado y respuestas honestas

Las respuestas separan lo que está medido sobre datos sintéticos propios, lo que es supuesto y lo que depende de la Caja.

## 1. ¿Cuál es el impacto en el KPI?

No hay línea base oficial, así que no afirmamos una cifra sobre la cartera de la Caja. Medimos sobre datos sintéticos propios cuántos casos detecta la cola, con cuánta anticipación y con qué falsos positivos frente a reglas simples. El efecto de intervenir es un escenario: si evitara 10, 20 o 30 % de los pasos a atraso de los casos capturados, de cada 100 que pasarían a atraso se evitarían unos 6, 12 o 18. Es una ilustración aritmética, no una estimación.

## 2. ¿Por qué no basta con mirar los días de atraso?

Porque la regla «ya tiene atraso» no distingue entre clientes que hoy están al día, que son los que queremos anticipar. Sobre datos sintéticos propios, las señales tempranas ordenan a esos clientes con un AUC de 0,84, y el 10 % mejor puntuado concentra alrededor de 6 de cada 10 casos.

## 3. ¿Cómo evitan los falsos positivos?

Con un filtro que exige que la caída sea persistente, no estacional y visible en al menos dos familias de señales. Es nuestra propuesta de control y su efecto se mide en el backtest: todavía no está medido. La precisión absoluta es baja (4,7 %) porque el evento es raro, por eso la acción propuesta es de bajo costo.

## 4. ¿Cómo tratan datos personales y sesgos?

Trabajamos solo con datos sintéticos. Los registros usan identificadores; sexo y edad solo auditan sesgos y no entran al modelo; la zona define cohortes de comparación y también se audita por grupo. Como mínimo, un cuadro de tasa de alerta por grupo.

## 5. ¿Qué parte es inteligencia artificial y cuál no?

El modelo calibrado con incertidumbre y el agente acotado que redacta la propuesta. En el mínimo viable el agente funciona con plantillas y el modelo es una regresión logística; el modelo de lenguaje y los árboles se añaden si sobra tiempo. El proveedor es intercambiable y existe modo sin red.

## 6. ¿Cabe en 8 horas por persona?

Estimamos 31,5 horas-persona de 32, sin holgura; en el escenario pesimista son unas 45. Por eso el plan base es un mínimo viable con recortes ordenados que protegen la cola, la explicación, la aprobación humana con bitácora, el backtest y las pruebas.

## 7. ¿Y si la Caja no entrega datos?

No los necesitamos para el prototipo: ya existe un generador propio con 5,000 clientes y 34 meses. Si la Caja aporta datos o un esquema, se mapean al mismo formato.

## 8. ¿Esto decide créditos?

No. La alerta no cambia calificación, límite ni tasa de ningún cliente y ningún endpoint envía mensajes ni ejecuta acciones: el gestor aprueba, edita o descarta.

## 9. ¿La cola es diaria?

En el prototipo se recalcula por fecha de corte (mensual, según los datos sintéticos). Una cadencia diaria sería un supuesto a validar con el owner.

## 10. ¿Qué es preexistente y qué se construye en el evento?

Preexistente: el generador de datos con sus pruebas, sus datos y un script de auditoría de dificultad, todos del equipo y creados el 21.11.2026. En el evento se construyen el modelo, el filtro, el agente, la API, la interfaz y el backtest.
