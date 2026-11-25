# NEG-02 — preguntas esperables del jurado y respuestas honestas

Las respuestas separan lo que está medido sobre datos sintéticos propios, lo que es supuesto y lo que depende de la Caja.

## 1. ¿Cuál es el impacto en el KPI?

No hay línea base oficial, así que no afirmamos una cifra sobre la Caja. Medimos en un sandbox sintético, con tres brazos, cuántos clientes tienen una oportunidad válida dentro de su consentimiento. Como dato preliminar, con las mismas reglas la Caja sola identifica el 13 % de las oportunidades y abstenciones que existen, con los consentimientos del conjunto el 31 % (tasa supuesta de 65 %) y con información completa el 95 %, que es un tope teórico.

## 2. ¿Por qué el consentimiento se aplica en el código y no en la interfaz?

Porque una casilla en la interfaz no impide que un dato no autorizado llegue al motor o al agente. En nuestro diseño el control de consentimiento es el único camino a los datos de otras entidades, aplica alcance, vigencia, finalidad y receptor, registra cada acceso y se prueba con una batería adversarial que debe dar cero fugas.

## 3. ¿La Caja no ve ya el endeudamiento externo por las centrales de riesgo?

Es un supuesto que hacemos explícito: suponemos que la Caja tendría, como mucho, información agregada de centrales de riesgo, y que no ve tasas, ahorro ni flujo de ingresos de otras entidades. Si el owner confirma que las centrales ya forman parte del flujo, añadimos un cuarto brazo: Caja más central de riesgo.

## 4. ¿El 31 % no depende de supuestos suyos?

Sí, y lo decimos: depende de una tasa de consentimiento de 65 % que definimos nosotros y de reglas de alcance. En el evento medimos la sensibilidad a esa tasa. El 95 % es un tope teórico porque la verdad se define con las mismas reglas.

## 5. ¿Qué pasa con un cliente sobreendeudado?

El sistema se abstiene: no ofrece crédito y lo explica con la evidencia autorizada. La estimación del ingreso es el punto más débil de esta parte (precisión de 0,5 a 0,8 en nuestras pruebas) y se reportará con intervalos.

## 6. ¿Qué parte es inteligencia artificial?

Un modelo predictivo estima el ingreso, el motor detecta oportunidades con linaje y un agente explica con herramientas acotadas y verifica que cada cifra citada exista en los datos autorizados. El mínimo comprometido incluye el modelo de ingreso y el motor; el agente con redacción por IA se incorpora si el tiempo lo permite y siempre existe el modo con plantilla sin red.

## 7. ¿Cabe en 8 horas por persona?

El mínimo estimado es de 28 horas-persona y el completo de 36, frente a unas 32 a 34 disponibles; en el escenario pesimista el mínimo sube a unas 41 y solo cabe con recortes ya definidos: primero la redacción con IA y la interfaz, nunca el control de consentimiento ni la evidencia.

## 8. ¿Y si la Caja no entrega datos?

No los necesitamos: el generador propio produce clientes y entidades ficticias, transacciones, catálogo y consentimientos. Si la Caja aporta datos o un esquema, se adaptan.

## 9. ¿Cumplen algún estándar de Open Finance?

No declaramos conformidad con ningún estándar. El sandbox simula el intercambio con credencial por entidad receptora, auditoría y minimización; los requisitos reales de TI y Seguridad quedarían para una etapa posterior.

## 10. ¿Qué es preexistente?

El generador de datos sintéticos con 41 pruebas y un script de auditoría de los datos, ambos del equipo y creados el 21.11.2026. El servicio de consentimiento, las APIs simuladas, la vista integral, el motor, el agente, la interfaz y la medición del KPI se construyen en el evento.
