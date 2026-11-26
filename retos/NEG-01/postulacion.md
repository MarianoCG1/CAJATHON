# Postulación NEG-01 — texto para pegar en la plataforma

Desafío elegido: NEG-01 · Plan de pagos adaptado al ciclo económico del negocio. Equipo: Yupana Labs.

## 1. Problema abordado

Los ingresos de muchos microempresarios dependen de campañas, cosechas, clima y la dinámica de su zona, y dos negocios del mismo rubro pueden tener ciclos distintos. Hoy la evaluación pondera un ingreso estándar único y el sistema core solo genera cuotas fijas con una periodicidad única; el asesor no tiene cómo cruzar información del sector y la zona con la realidad de su cliente. Resultado: problemas de liquidez en los valles, incluso en negocios viables. El reto es estimar ese ciclo desde la admisión y construir un plan de pagos que lo siga sin superar la capacidad de pago en ninguna etapa, cuidando la sostenibilidad de la Caja.

## 2. Concepto de solución

Una herramienta para el Asesor de Negocios con las tres piezas mínimas que pide el desafío. (A) Un modelo del ciclo en dos capas: el patrón estacional del sector y la zona, construido con series y calendarios públicos (BCRP, INEI, MIDAGRI, SENAMHI, calendarios comerciales), se ajusta a cada cliente con lo que el asesor observa en campo; cuanta más evidencia, más pesa el dato propio. Luego proyecta los meses concretos del crédito con el estado previsto de El Niño (ENFEN, índices ONI e ICEN), usando la sensibilidad de cada sector estimada con la historia. Entrega la utilidad neta esperada por etapa, con su banda de incertidumbre y escenarios adversos. (B) Un motor de optimización que, con el monto, la TEA, los seguros y el plazo, elige cuánto capital amortiza cada cuota. Exige Cuota/Utilidad Neta por debajo del factor del producto en cada etapa, dejando holgura, y además que la cuota quede cubierta por la utilidad de los escenarios adversos; respeta los topes del producto, la prelación y los pendientes que fijó el owner, y amortiza más en las cimas al menor costo para el cliente. Si el monto pedido no cabe, propone el monto o el plazo que sí caben. (C) El motivo de cada cuota (etapa, utilidad esperada, Cuota/UN y restricción que la limita) y su comparación con la cuota fija equivalente. El asesor puede bajar el factor o corregir una etapa; el comité decide.

## 3. Impacto esperado en el KPI

El indicador del prototipo es el porcentaje de periodos en tensión (cuota por encima de factor × utilidad, y cuota por encima de la utilidad) del plan adaptado frente a la cuota fija, en escenario base y adversos (caída de ventas, campaña retrasada, El Niño). Como secundarios medimos costo total y TCEA para el cliente (para mostrar si hay encarecimiento), ajuste de las cuotas al ciclo, error del ciclo estimado y concentración de capital, además de ingreso y exposición de la Caja. No medimos mora, como indicó el owner. La medición se hace en un banco de pruebas reproducible con perfiles sintéticos de distintos rubros, zonas y productos, cuyo ciclo verdadero se conoce; los planes se construyen con lo que vería el asesor y se evalúan contra ese ciclo. Las cifras saldrán de esa medición; no las inventamos. Un ejemplo calculado a mano con las reglas del owner (ilustrativo, no una medición) muestra el problema: un arrocero de Jequetepeque que pide S/ 8,000 a 12 meses califica para cuota fija con su utilidad promedio (S/ 801), pero esa cuota supera su utilidad en 8 de 12 meses. Seguir el ciclo sin holgura elimina el déficit en un año normal, pero no si la cosecha se atrasa un mes. Con holgura bajo el tope y frente a El Niño en toda la vida del crédito, la herramienta propone S/ 5,895 a 12 meses o S/ 8,000 a 17 meses, sin ningún mes de déficit en año normal, con El Niño ni con una caída de ventas de 20 %. La retención, que el owner señaló como indicador de negocio, se mediría en un piloto con línea base a confirmar.

## 4. Enfoque tecnológico

Analítica predictiva del ciclo (descomposición estacional y ajuste por agregación parcial), optimización con un programa lineal (SciPy, HiGHS), cálculo financiero con las reglas del owner (TED en base 360 por días exactos, seguros por interés simple, prelación seguros, interés y capital, y pendientes en su concepto), una API y una interfaz para el asesor y el comité. Python, FastAPI, SQLite y React. Un modelo de lenguaje intercambiable, solo en la demo y con datos sintéticos, redacta el resumen para comité y estructura las notas de campo; una verificación en código impide que introduzca cifras. Funciona sin conexión a la Caja y tiene modo sin red.

## 5. Tecnología preexistente

Librerías abiertas bajo sus licencias y herramientas de planificación del equipo que no forman parte de la solución. Si construimos antes del evento un generador de perfiles sintéticos, lo declararemos con sus pruebas. No reutilizamos código de empleadores ni de otros clientes ni datos reales. El modelo del ciclo, el motor, la prueba de estrés, la explicación, la API y la interfaz se construyen en el evento.

## 6. Funcionalidad crítica

Dado un cliente y una operación, el sistema estima su ciclo, construye el plan óptimo con monto y periodo por cuota, explica por qué cada cuota es alta o baja, muestra Cuota/UN por etapa y lo compara con la cuota fija en escenarios base y adversos; el asesor ajusta y exporta la hoja para comité. Verificaremos con pruebas que el cronograma reproduce las reglas del owner, que ninguna cuota supera el factor en su etapa ni la utilidad de los escenarios adversos, que con un ciclo plano todas las cuotas salen iguales, que el ejemplo del arrocero se reproduce y que, si no hay plan posible, el sistema dice qué restricción lo impide.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta: dos clientes con el mismo monto y ciclos distintos (por ejemplo, un arrocero y un taller de calzado de La Libertad) reciben planes distintos y explicados, que se comparan con la cuota fija en un año normal y con El Niño; se cierra con el banco de pruebas sobre la cartera sintética. Incluye pruebas automáticas y reporte de validación. Fuera de alcance: integración con el core y reprogramaciones.

## 8. Factibilidad y dependencias

Estimamos 31 horas-persona de 32 disponibles (supuesto), con un núcleo de 26 que no se recorta: ciclo con banda, motor con las reglas del owner, motivos por cuota, comparación con cuota fija y pruebas. Si falta tiempo se recortan, en este orden, el asistente de notas, el resumen con modelo de lenguaje y los escenarios adicionales. El cálculo es determinista y verificable contra casos hechos a mano, y el programa lineal se resuelve en milisegundos. El equipo cubre economía y sector financiero, ciencia de datos, desarrollo y experiencia de usuario. Dependencias: factores, cuota mínima, plazos y topes por producto (usamos los ejemplos del owner, configurables) y línea base de retención, por confirmar.
