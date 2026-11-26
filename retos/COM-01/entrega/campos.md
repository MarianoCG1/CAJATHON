# COM-01 — campos para pegar en el formulario

**Título:** COM-01 · Brújula comercial que aprende de cada visita

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (386 caracteres):

La prospección se apoya en experiencia, referidos y conocimiento del territorio. Es valioso, pero se aprende sobre todo de donde ya se va: una zona que no se visita no genera información, y la falta de información puede confundirse con falta de potencial. El desafío pide encontrar y priorizar oportunidades que pueden pasar inadvertidas, con evidencia y sin exclusiones injustificadas.

**Versión completa** (470 caracteres):

La prospección se apoya en experiencia, referidos y conocimiento del territorio. Es valioso, pero se aprende sobre todo de donde ya se va: una zona que no se visita no genera información, y la falta de información puede confundirse con falta de potencial. El desafío pide identificar y priorizar oportunidades que pueden pasar inadvertidas, con evidencia, sin exclusiones injustificadas y sin tratar una señal como necesidad confirmada, capacidad de pago o elegibilidad.

## 2. Concepto de solución

**Versión corta** (321 caracteres):

Cada semana propone dónde prospectar: parte de la ruta habitual, parte de descubrimiento y una cuota mínima para las zonas menos conocidas. Cada zona trae su ficha con evidencia, fuentes, dudas y qué validar. El analista aprueba, registra el resultado en segundos y el reparto aprende. Complementa lo que la Caja ya hace.

**Versión completa** (461 caracteres):

Brújula comercial que aprende de cada visita. Cada semana propone a cada analista dónde prospectar, combinando la ruta que ya haría con zonas de descubrimiento y una cuota mínima para las menos conocidas. Cada zona trae su ficha: qué se sabe, de qué fuente, qué no se sabe y qué validar en campo. El analista ajusta y aprueba; registra el resultado en segundos; el reparto cambia según lo que va rindiendo. Complementa los mecanismos actuales, no los reemplaza.

## 3. Impacto esperado

**Versión corta** (429 caracteres):

KPI: clientes nuevos por cada 100 visitas; además conversión, desembolsos, costo por cliente nuevo y primer acceso. Medido sobre datos sintéticos propios, en tres supuestos sobre la realidad: la mezcla quedó siempre en 91 % o más de la mejor estrategia; visitar solo donde ya hay clientes cayó hasta 47 % y un puntaje fijo hasta 62 %; cuando el potencial está ahí, esa opción gana. Sin línea base oficial no se promete una cifra.

**Versión completa** (658 caracteres):

KPI principal: clientes nuevos por cada 100 visitas. Complementarios: conversión, desembolsos, costo por cliente nuevo, primer acceso al sistema financiero y visitas a zonas poco atendidas. Horizonte: 12 semanas (supuesto). Medido sobre datos sintéticos propios (medianas de 200 simulaciones): en tres supuestos distintos sobre la realidad, la mezcla adaptativa quedó siempre en 91 % o más de la mejor de las cuatro estrategias comparadas; visitar solo donde ya hay clientes (simplificación nuestra) cayó hasta 47 % y un puntaje fijo hasta 62 %; cuando el potencial está ahí, esa opción gana. No hay línea base oficial y no se promete una cifra para la Caja.

## 4. Enfoque tecnológico

**Versión corta** (310 caracteres):

Python, FastAPI, scikit-learn, SQLite, Pydantic AI y React con mapa. Modelo de potencial como punto de partida de un esquema bayesiano por zona; planificador con muestreo de Thompson, capacidad y cuota de exploración; agente acotado que redacta la ficha citando fuentes, con modo sin red. Sin datos personales.

**Versión completa** (421 caracteres):

Python, FastAPI, pandas, scikit-learn, SQLite, Pydantic AI y React con mapa. Un modelo de potencial sirve de creencia previa a un esquema bayesiano por zona; un planificador con muestreo de Thompson respeta capacidad, distancia y cuota de exploración; un agente acotado redacta la ficha citando fuentes, con proveedor intercambiable y modo sin red. La unidad es la zona: sin datos personales ni características sensibles.

## 5. Tecnología preexistente

**Versión corta** (215 caracteres):

Del equipo, creado el 25.11.2026: generador de territorio sintético con 7 pruebas y script de auditoría que compara estrategias (contiene una versión mínima y no se reutiliza). Librerías abiertas bajo sus licencias.

**Versión completa** (328 caracteres):

Del equipo, creada el 25.11.2026: un generador de territorio sintético con 7 pruebas y un script de auditoría que compara estrategias en simulación (de él salen las cifras; contiene una versión mínima de la estrategia y no se reutiliza). Librerías de código abierto bajo sus licencias. Sin código de empleadores ni datos reales.

## 6. Funcionalidad crítica

**Versión corta** (278 caracteres):

Plan semanal que combina ruta habitual y descubrimiento, con ficha de evidencia por zona, aprobación del analista y actualización al registrar resultados. Con los mismos datos, mismo plan; la falta de dato no castiga a una zona; la ficha no habla de personas ni de elegibilidad.

**Versión completa** (154 caracteres):

Plan semanal que combina ruta habitual y descubrimiento, con ficha de evidencia por zona, aprobación del analista y actualización al registrar resultados.

## 7. Nivel de desarrollo esperado

**Versión corta** (293 caracteres):

Prototipo de punta a punta sobre 120 zonas sintéticas: abrir la semana, revisar una zona de descubrimiento, aprobar, registrar resultados, ver cómo cambia la siguiente semana y comparar en el backtest contra la ruta habitual y un puntaje fijo. Con pruebas y cuadro de reparto por tipo de zona.

**Versión completa** (305 caracteres):

Prototipo de punta a punta: abrir la semana, revisar una zona de descubrimiento, aprobar, registrar resultados, ver el cambio en la semana siguiente y comparar en el backtest contra la costumbre y contra un puntaje fijo. Con pruebas automáticas, reporte de validación y cuadro de equidad por tipo de zona.

## 8. Factibilidad y dependencias

**Versión corta** (230 caracteres):

31 de 32 horas-persona (supuesto), con mínimo viable definido. No requiere datos de la Caja; conteos agregados por zona mejorarían el plan. Por confirmar: capacidad de visitas, definición de cliente nuevo y política de IA externa.

**Versión completa** (274 caracteres):

31 de 32 horas-persona (supuesto), sin holgura, con un mínimo viable definido. No requiere datos de la Caja; conteos agregados de clientes y de resultados por zona mejorarían el plan. Por confirmar: capacidad de visitas, definición de cliente nuevo y política de IA externa.
