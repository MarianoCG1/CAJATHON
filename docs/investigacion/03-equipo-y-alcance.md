# Equipo Yupana Labs y alcance: ¿uno o todos los desafíos?

Fuente: perfiles registrados en la plataforma (21.11.2026), bases v4 y expedientes. **(supuesto)** = inferencia nuestra.

## 1. Fortalezas y huecos del equipo

| Integrante | Fuerte en | Hueco / riesgo |
|---|---|---|
| Mariano | Backend, agentes, ML, integración, entrega técnica | Es el cuello de botella si todo pasa por él |
| Glem | Datos, ML, FastAPI, pruebas, ETL; ganó una datathon | Sin experiencia financiera ni en cobranza |
| Antonio | Único con sector financiero; KPI, caso de negocio, Power BI | Primer hackathon; menos de 1 año de experiencia |
| David | Flujos de usuario, UI, prototipado | Primer hackathon; sin experiencia laboral ni financiera |

Lectura: equipo **fuerte en datos/IA/construcción** y **débil en conocimiento del dominio microfinanciero**. Dos personas hacen su primer hackathon. Esto favorece un desafío donde la ventaja sea técnica y medible (datos sintéticos + modelo + agente), y pide usar a los Caja Experts para el dominio.

## 2. ¿Desarrollar todos los desafíos?

**No lo recomiendo.** Razones, con las bases:

1. **Un equipo, un concepto.** La plataforma dice «el desafío que eligieron y cómo piensan resolverlo» (singular). No encontré ninguna regla que permita varios; el formulario está cerrado hasta el 25.11. **Hay que preguntarlo**; no asumirlo.
2. **Cuentas de tiempo.** El evento da ~8 h de construcción reales (3–4.12). 4 personas × 8 h = 32 horas-persona. Con 8 expedientes son **4 h-persona por desafío**, sin pruebas ni demo. Con 3 desafíos serían ~11 h cada uno.
3. **Condición eliminatoria.** Se necesita promedio ≥ 3/5 en «funcionamiento de la funcionalidad crítica» (20% del puntaje + eliminatoria). Un prototipo que funciona de punta a punta vale más que varios a medias; repartirnos aumenta el riesgo de quedar bajo 3 en alguno.
4. **Presentación.** El Demo Day es un pitch y una demo por equipo. No hay tiempo para mostrar varios productos, y el jurado premia claridad (5%) y simplicidad (5%).
5. **Evidencia de desarrollo.** Hay que mostrar historial de avances respecto del concepto. Un repo disperso en varios proyectos diluye esa evidencia.
6. **Escribir el concepto.** Cada concepto necesita KPI, línea base, impacto y datos, y los expedientes no traen KPI. Hacer 8 conceptos en 2 días (25–26.11) con 4 personas empeora cada uno. Además los owners son distintos.
7. **Riesgo de que pasen dos.** Si ambos conceptos llegaran a los 12 finalistas **(supuesto)**, habría que construir ambos en 2 días.

## 3. Lo rescatable de tu idea (parejas que rotan)

La idea de **sinergia entre parejas** sí es buena, pero aplicada a **un solo producto** con frentes de trabajo:

| Pareja | Frente | Entregable en el evento |
|---|---|---|
| Mariano + Glem | Núcleo: datos sintéticos, modelo, agente | Scoring + agente que recomienda la acción |
| Mariano + Antonio | KPI y negocio | Backtest antes/después, caso de negocio, `docs/validacion.md` |
| Mariano + David | Experiencia del gestor | Interfaz, flujo operativo, demo |
| Glem + Antonio | Validación | Pruebas, supuestos del KPI, reglas de negocio |
| Antonio + David | Narrativa | Pitch, historia del caso, presentación |
| Glem + David | Explicabilidad | Cómo se muestra el porqué de cada alerta al gestor |

Se rota por bloques de ~2 h y Mariano no queda de cuello de botella. Esto da al jurado exactamente lo que puntúa: funcionalidad, pruebas, KPI, demo.

## 4. Variante inteligente: un núcleo, un caso demostrado, escalabilidad a otros

Varios expedientes comparten el mismo insumo: historial de pagos, saldos, comportamiento y señales de cliente (**RIE-03, NEG-01, NEG-03**, en parte COM-02). Podemos diseñar una **plataforma común** (datos del cliente → señales → recomendación de acción con revisión humana) y **demostrar un solo caso** (p. ej. RIE-03). Los otros se presentan como hoja de ruta, que suma al subcriterio «implementación y escalabilidad» (10%) sin comprometer construcción extra. Es una capa de arquitectura, no trabajo adicional en el evento.

## 5. Recomendación

1. Un solo desafío, **RIE-03 como candidato** (o NEG-03/NEG-01 si el owner da mejores datos y KPI).
2. Todo el equipo en ese producto, con las parejas rotativas de §3.
3. Arquitectura reutilizable como argumento de escalabilidad (§4).
4. Antes de decidir: preguntar a la organización si se permite más de un concepto y si los 8 expedientes son elegibles.

## 6. Texto sugerido para preguntar a la organización

> Versión ampliada (5 preguntas, WhatsApp y correo) en `docs/consulta-organizacion.md`.

> Hola, somos el equipo Yupana Labs (CJT-SAXBNS). Dos consultas: (1) ¿Los 8 expedientes publicados en la plataforma (COM-01, COM-02, NEG-01, NEG-02, NEG-03, RIE-01, RIE-02, RIE-03) son elegibles, o solo los 6 mencionados? (2) ¿Un equipo puede postular Conceptos de solución para más de un desafío, o solo uno? Además, ¿cuál es la hora límite de postulación el jueves 26.11? Gracias.
