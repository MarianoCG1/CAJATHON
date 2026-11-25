# RIE-02 — preguntas esperables del jurado y respuestas honestas

Las respuestas separan lo que está medido sobre datos sintéticos propios, lo que es supuesto y lo que depende de la Caja.

## 1. ¿Cuál es el impacto en el KPI?

No hay línea base oficial, así que no afirmamos una cifra sobre la Caja. Medimos sobre datos sintéticos propios precisión y recall por red, carga de revisión a igual recall y señuelos legítimos marcados. Como referencia, marcar cualquier coincidencia obliga a revisar el 46 % de las solicitudes de la partición de evaluación y solo cerca del 12 % de ellas es fraude; la meta es reducir esa carga sin perder recall, y se registra antes de evaluar.

## 2. ¿Por qué no alertar por cada coincidencia?

Porque compartir un dato no implica necesariamente fraude: familias, mercados y gremios comparten teléfonos y direcciones. En nuestros datos, la regla de «cualquier coincidencia» detecta el 90 % del fraude pero marca todos los señuelos legítimos. Por eso exigimos corroboración de comportamiento anómalo.

## 3. Una regla de dominio ya rinde bien. ¿Qué aporta su solución?

Es cierto: una regla con criterio de dominio, que ajustamos a mano viendo estos mismos datos, alcanza un F1 cercano a 0,9. Frente a ella el aporte esperado es moderado y lo reportaremos así. Lo que aporta es la explicación por red, el expediente verificable, la corroboración que evita acusar por relaciones y la robustez en redes difíciles, que las reglas de coincidencia casi no ven.

## 4. ¿Cómo evitan acusar a clientes legítimos?

Con tres mecanismos: el peso del vínculo depende de lo raro que es, una red solo sube si además muestra comportamiento anómalo y cada alerta muestra su contrapartida legítima. Además la alerta nunca dice «fraude»: dice que merece revisión, y ninguna acción sobre el cliente se ejecuta sin decisión humana.

## 5. ¿Qué pasa con los datos personales?

Trabajamos solo con datos sintéticos. Al modelo de lenguaje solo irían identificadores y atributos seudonimizados, la plantilla sin red es la opción por defecto y cada decisión queda registrada con su motivo.

## 6. ¿Qué parte es inteligencia artificial?

La ponderación por rareza, la detección de comunidades, la corroboración y un agente que redacta el expediente, con un verificador determinista que comprueba cada cita. El mínimo usa el grafo ponderado con comunidades y la regla de corroboración; el modelo de lenguaje redacta y el aprendizaje automático es una mejora si hay tiempo.

## 7. ¿Cabe en 8 horas por persona?

El plan es de unas 29 horas-persona frente a unas 34 disponibles. Si las tareas tardan de 1,4 a 1,6 veces más, el plan completo no cabe y queda un mínimo de unas 31 horas, con un colchón de apenas el 8 %. El mayor riesgo es la interfaz con grafo interactivo; el respaldo es un grafo estático.

## 8. ¿Y si la Caja no entrega datos?

No los necesitamos: el generador propio produce solicitudes ficticias con redes y relaciones legítimas. Si la Caja aporta datos, se mapean al mismo esquema.

## 9. ¿Quién decide y qué ve el cliente?

Decide el especialista, con un motivo registrado. El sistema no cambia el estado de una solicitud ni bloquea ni notifica al cliente.

## 10. ¿Qué es preexistente?

El generador de datos sintéticos con 37 pruebas y un script de auditoría, del equipo y creados el 21.11.2026. Las pruebas incluyen reglas de control solo para comprobar que los datos no son triviales. Grafo, puntaje, agente, verificador, API e interfaz se construyen en el evento.
