# COM-01 — texto de postulación

> Supuestos marcados como (supuesto). Cifras medidas = sobre datos sintéticos propios.

## 1. Problema abordado

La prospección se apoya en experiencia, referidos y conocimiento del territorio. Es valioso, pero se aprende sobre todo de donde ya se va: una zona que no se visita no genera información, y la falta de información puede confundirse con falta de potencial. El desafío pide identificar y priorizar oportunidades que pueden pasar inadvertidas, con evidencia, sin exclusiones injustificadas y sin tratar una señal como necesidad confirmada, capacidad de pago o elegibilidad.

## 2. Concepto de solución

Brújula comercial que aprende de cada visita. Cada semana propone a cada analista dónde prospectar, combinando la ruta que ya haría con zonas de descubrimiento y una cuota mínima para las menos conocidas. Cada zona trae su ficha: qué se sabe, de qué fuente, qué no se sabe y qué validar en campo. El analista ajusta y aprueba; registra el resultado en segundos; el reparto cambia según lo que va rindiendo. Complementa los mecanismos actuales, no los reemplaza.

## 3. Impacto esperado

KPI principal: clientes nuevos por cada 100 visitas. Complementarios: conversión, desembolsos, costo por cliente nuevo, primer acceso al sistema financiero y visitas a zonas poco atendidas. Horizonte: 12 semanas (supuesto). Medido sobre datos sintéticos propios (medianas de 200 simulaciones): en tres supuestos distintos sobre la realidad, la mezcla adaptativa quedó siempre en 91 % o más de la mejor de las cuatro estrategias comparadas; visitar solo donde ya hay clientes (simplificación nuestra) cayó hasta 47 % y un puntaje fijo hasta 62 %; cuando el potencial está ahí, esa opción gana. No hay línea base oficial y no se promete una cifra para la Caja.

## 4. Enfoque tecnológico

Python, FastAPI, pandas, scikit-learn, SQLite, Pydantic AI y React con mapa. Un modelo de potencial sirve de creencia previa a un esquema bayesiano por zona; un planificador con muestreo de Thompson respeta capacidad, distancia y cuota de exploración; un agente acotado redacta la ficha citando fuentes, con proveedor intercambiable y modo sin red. La unidad es la zona: sin datos personales ni características sensibles.

## 5. Tecnología preexistente

Del equipo, creada el 25.11.2026: un generador de territorio sintético con 7 pruebas y un script de auditoría que compara estrategias en simulación (de él salen las cifras; contiene una versión mínima de la estrategia y no se reutiliza). Librerías de código abierto bajo sus licencias. Sin código de empleadores ni datos reales.

## 6. Funcionalidad crítica

Plan semanal que combina ruta habitual y descubrimiento, con ficha de evidencia por zona, aprobación del analista y actualización al registrar resultados.

## 7. Nivel de desarrollo esperado

Prototipo de punta a punta: abrir la semana, revisar una zona de descubrimiento, aprobar, registrar resultados, ver el cambio en la semana siguiente y comparar en el backtest contra la costumbre y contra un puntaje fijo. Con pruebas automáticas, reporte de validación y cuadro de equidad por tipo de zona.

## 8. Factibilidad y dependencias

31 de 32 horas-persona (supuesto), sin holgura, con un mínimo viable definido. No requiere datos de la Caja; conteos agregados de clientes y de resultados por zona mejorarían el plan. Por confirmar: capacidad de visitas, definición de cliente nuevo y política de IA externa.
