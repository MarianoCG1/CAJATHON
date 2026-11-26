# Concepto de solución — NEG-01 · Plan de pagos adaptado al ciclo económico del negocio

> **v1 (pareja líder, 25.11.2026).** Prioridad **#2** · Pareja líder **Antonio + Glem** · Revisor **David** · Eje: 4 Inclusión financiera y resiliencia · Owners (plataforma): (ver plataforma).
> Reescrito sobre el expediente **actualizado el 25.11 (19:02)**, sus 10 preguntas frecuentes y la respuesta a nuestro ticket del 24.11. El título del reto en la plataforma cambió de «Cuotas que se adaptan al flujo del negocio» a «Plan de pagos adaptado al ciclo económico del negocio».
> Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. No presentarlo como hecho. Material confidencial: repo privado.
> Detalle de datos, fórmulas, arquitectura, plan del evento y evaluación: `retos/NEG-01/panorama.md`.

## 1. Problema abordado

Según el expediente, los ingresos de muchos microempresarios **no son constantes**: dependen de la estacionalidad, los ciclos agrícolas, las campañas comerciales, el clima y la dinámica de su zona; su periodicidad no es necesariamente mensual y **dos negocios del mismo rubro pueden tener ciclos distintos**. Cuando el cronograma no coincide con ese ciclo aparecen problemas de liquidez, **incluso en negocios viables**.

Hoy, según el expediente y las respuestas del owner:

- la evaluación pondera un **ingreso estándar único** (promedio de meses altos y bajos); no existe el concepto de ciclo económico ni se mide la volatilidad;
- el sistema core solo genera **cuotas fijas con una periodicidad única**; los cronogramas estacionales también tienen cuotas homogéneas. La limitación **es del core, no de la normativa**;
- el Asesor de Negocios **no tiene herramientas** para cruzar información pública del sector y la zona con la realidad de su cliente; la confiabilidad de su estimación depende de su experiencia.

El reto pide estimar el ciclo de cada negocio **desde la admisión** y construir un plan de pagos cuyas cuotas y periodos sigan ese ciclo, **sin superar la capacidad de pago en ninguna etapa** y resguardando la sostenibilidad de la Caja. Alcance: créditos nuevos (admisión, ampliación, recuperación de cliente), cualquier producto y segmento, formales e informales, con o sin historial. El plan se fija antes del desembolso. Fuera de alcance: modificar créditos vigentes.

Riesgos que el expediente obliga a mitigar y que el diseño trata uno por uno (§4 y §6): **estimación optimista del ciclo**, **concentración de capital**, **encarecimiento** por exceso de gracia o solo interés, **sobreendeudamiento** y **dependencia del modelo**.

## 2. Concepto de solución

**«Ritmo»: el asesor estima el ciclo del negocio y obtiene, en la misma pantalla, el plan de pagos más barato que el negocio puede pagar en cada etapa, con el porqué de cada cuota y su prueba de estrés frente a la cuota fija.** El asesor conserva su criterio; el comité decide. **(nombre y enfoque: supuesto del equipo)**

Tres piezas, que son las tres que el expediente pide como mínimo:

1. **(A) Modelo del ciclo económico, en dos capas.**
   - *Patrón del sector y la zona* (la «capa pública»): un índice estacional por actividad y zona, con su volatilidad, construido a partir de series y calendarios públicos (BCRP, INEI, MIDAGRI, SENAMHI, calendarios comerciales; ver panorama §b). Responde a «cómo se mueve, en promedio, una bodega en La Esperanza o un arrocero en Pacasmayo» **(ejemplos de zona: supuesto)**.
   - *Ajuste al cliente* (la «capa propia»): el patrón se corrige con lo que el asesor recoge en campo (ventas en meses buenos, regulares y malos, costos, gastos, carga familiar, evidencias de transacciones y fechas de campaña). El peso del dato propio crece con la cantidad y la calidad de la evidencia (**agregación parcial** o *partial pooling*): un cliente sin evidencia hereda el patrón de su sector y zona; uno con evidencia sólida se aparta de él. Así se responde al «dos negocios del mismo rubro pueden tener ciclos distintos».
   - Salida: la **Utilidad Neta esperada por etapa** durante toda la vida del crédito, con **banda de incertidumbre** (escenario base y escenarios adversos: caída de ventas, campaña retrasada, El Niño). No usa el historial de pagos de una cartera, como pidió el owner.
2. **(B) Motor del plan de pagos (optimización con restricciones).** Con el monto, la TEA, los seguros y el plazo, resuelve un **programa lineal** que elige cuánto capital amortiza cada cuota. Respeta, en cada etapa, **Cuota ÷ UN esperada ≤ factor elegido por el asesor ≤ factor del producto**; cuota mínima, plazo máximo y TEA única; topes de concentración de capital y de periodos sin amortización. Entre todos los planes que cumplen, elige **el de menor costo total para el cliente**, que es justamente el que amortiza el máximo capital en las cimas, como pide el owner. El cronograma se calcula con las reglas que el owner detalló: TEA → TED base 360 por días exactos, seguros por interés simple, prelación **seguros → interés → capital** y conceptos impagos que quedan pendientes en su propio concepto. Si no hay plan posible, el motor dice qué restricción lo impide y qué cambiaría (monto, plazo o factor).
3. **(C) Explicación y prueba de estrés para el comité.** Cada cuota trae su motivo, calculado por el motor y no inventado por un modelo de lenguaje: en qué etapa cae, qué UN espera, qué Cuota/UN resulta y qué restricción la limita (por ejemplo, «alta: cosecha de arroz, UN esperada alta, Cuota/UN 0,61 ≤ 0,65» o «baja: valle entre campañas; cubre seguros e intereses»). El plan se compara con **la cuota fija equivalente** (mismo monto, TEA, seguros y plazo) en escenario base y adversos. Un modelo de lenguaje intercambiable solo redacta el resumen para el comité a partir de esos números, y una verificación en código rechaza cualquier cifra que no coincida.

**Diferenciación:** hoy existen simuladores de cuota fija y cronogramas estacionales homogéneos. Nosotros entregamos **un ciclo estimado y explicado**, **un plan óptimo con restricciones verificables** y **la cuantificación de beneficios y riesgos frente a la cuota fija**, en una sola herramienta para el asesor. No es un dashboard ni un chatbot: el valor está en el modelo del ciclo y en el motor de optimización.

**Principio de diseño:** la herramienta propone y explica; el asesor ajusta (puede bajar el factor, corregir una etapa o fijar una fecha de pago) y el comité aprueba. El prototipo no se conecta a los sistemas de la Caja.

## 3. Impacto esperado en el KPI

El expediente no publica KPI ni línea base. El owner indicó que el plan funciona **si se correlaciona con el ciclo estimado y sus beneficios y riesgos se cuantifican en un escenario de prueba**, que **no se medirá mora de una cartera real**, y que **desde el negocio el indicador principal es la retención**. Por eso separamos lo que el prototipo mide de lo que mediría un piloto:

| | KPI | Cómo se mide |
|---|---|---|
| **Principal (prototipo)** | **Periodos en tensión**: porcentaje de periodos en que la cuota supera la capacidad de pago (Cuota/UN > factor; y, más grave, cuota > UN), plan adaptado frente a cuota fija, en escenario base y adversos | Simulación sobre una cartera sintética de perfiles de distintos rubros, zonas y productos (panorama §e) |
| Secundario | **Costo para el cliente**: interés y seguros totales y TCEA del plan adaptado frente a la cuota fija | Mismo banco de pruebas; el motor minimiza costo, así que muestra si hay encarecimiento y cuánto |
| Secundario | **Ajuste al ciclo**: correlación entre cuotas y UN por etapa; error del ciclo estimado frente al ciclo «verdadero» del perfil sintético | Banco de pruebas con verdad conocida (el generador sabe el ciclo real; el modelo solo ve lo que vería el asesor) |
| Secundario | **Concentración de capital** (proporción del capital en las dos cuotas más altas) y **periodos sin amortización** | Mismo banco de pruebas |
| Para la Caja | Ingreso financiero, saldo promedio expuesto y déficit de liquidez del cliente en escenarios adversos | Mismo banco de pruebas |
| **Negocio (piloto, no prototipo)** | **Retención / renovación** de clientes con plan adaptado frente a cuota fija | **[POR CONFIRMAR]** línea base y diseño del piloto con la Caja |

- **Línea base:** la **cuota fija equivalente** que genera hoy el core, calculada con las mismas condiciones; es una comparación de diseño, no una cifra de la Caja. La línea base de retención es **[POR CONFIRMAR]**.
- **Cifra de impacto esperada:** **[POR COMPLETAR]** con lo que mida el banco de pruebas. No se inventa.
- **Método:** simulación reproducible con semilla fija sobre perfiles sintéticos, con escenarios adversos definidos antes de correrla (no se ajustan para que el resultado se vea mejor).

## 4. Enfoque tecnológico

Pila: Python 3.11+, FastAPI, Pydantic v2, pandas, statsmodels y scikit-learn, SciPy (`linprog` con HiGHS) para la optimización, SQLite, Pydantic AI con proveedor de LLM intercambiable, React + Vite + Tailwind, pytest.

| Capa | Qué hace | Aporta valor real porque… |
|---|---|---|
| Patrones públicos | Índice estacional y volatilidad por actividad × zona (descomposición estacional de series públicas y calendarios de campaña) | Da al asesor lo que hoy no tiene: el ciclo de su sector y su zona |
| Modelo del ciclo | Ajuste al cliente por agregación parcial; UN por etapa con banda de incertidumbre y escenarios adversos | Responde a que dos negocios del mismo rubro difieren; la incertidumbre es explícita y alimenta la holgura |
| Asistente de campo (opcional) | Un LLM convierte las notas del asesor («vende más en campaña escolar y Navidad; febrero flojo») en parámetros del ciclo, que el asesor confirma | Usa IA donde aporta: estructurar información cualitativa de campo; nunca decide |
| Motor del plan | Programa lineal: minimiza el costo total sujeto a Cuota/UN ≤ factor por etapa, cuota mínima, plazo, concentración y gracia; cronograma con TED base 360, seguros y prelación con pendientes | Cumple las reglas del producto **por construcción** y es auditable: cada restricción activa se puede mostrar |
| Prueba de estrés | Recalcula el plan adaptado y la cuota fija en escenarios adversos, con la prelación y los pendientes | Cuantifica beneficios y riesgos para el cliente y la Caja, como pide el resultado esperado 4 |
| Explicación | Motivo de cada cuota a partir de la etapa, la UN y la restricción activa; resumen para comité redactado por LLM y verificado en código | Explicable por diseño; el LLM no puede introducir cifras |
| API e interfaz | FastAPI; interfaz del asesor: ciclo → plan → comparación → hoja para comité | El asesor y el comité ven lo mismo, con los supuestos a la vista |

Cómo se mitiga cada riesgo del expediente:

- **Ciclo optimista:** la restricción se evalúa sobre la UN esperada de cada etapa, como pide el owner, y además el plan pasa una prueba de estrés: en el escenario adverso la cuota debe quedar cubierta por la UN (**regla de holgura: supuesto, configurable**). El asesor puede usar un factor menor al del producto.
- **Concentración de capital:** tope por cuota a la proporción de capital (p. ej. ≤ 35 % del monto **(supuesto, configurable)**) y número mínimo de cuotas que amortizan.
- **Encarecimiento:** el objetivo del motor es el menor costo total; hay tope de periodos consecutivos sin amortizar y se muestra la TCEA frente a la cuota fija.
- **Sobreendeudamiento:** la UN ya descuenta el gasto financiero de otras deudas y, en personas naturales o parcialmente formales, la carga familiar; se respetan el factor y los límites del producto.
- **Dependencia del modelo:** todo es editable y visible (patrón, ajuste, factor, fechas); el motivo de cada cuota sale de reglas en código, no de una caja negra.

## 5. Tecnología preexistente

- Librerías de código abierto (FastAPI, Pydantic, pandas, statsmodels, scikit-learn, SciPy, React, etc.) bajo sus licencias.
- Herramientas de planificación del equipo (`scripts/sinergia/`, `scripts/conceptos/`, `scripts/boveda/`, `scripts/entrega/`), que no forman parte del producto.
- **Si se construye antes del evento** (decisión pendiente; ver `README.md` de este reto): un generador de perfiles de negocio sintéticos con pruebas, que se declararía en `docs/preexistente.md` con fecha y titularidad.
- **No se reutiliza código de empleadores ni de otros clientes. No se usan datos reales de clientes.** Las series públicas (BCRP, INEI, MIDAGRI, SENAMHI) son datos abiertos agregados, no datos personales.
- **No es preexistente, y se construye en el evento:** patrones sector × zona, modelo del ciclo, motor de optimización y cronograma, prueba de estrés, explicación, API, interfaz y evaluación.

## 6. Funcionalidad crítica

**Del negocio al plan de pagos explicado, en una sola pantalla del asesor.** Dado un cliente (sector, zona, modelo de negocio, datos de campo) y una operación (monto, TEA, seguros, plazo, producto), el sistema:

1. estima el **ciclo económico** del cliente durante la vida del crédito: UN esperada por etapa y su banda, combinando el patrón del sector y la zona con la información propia;
2. construye el **plan de pagos óptimo**, con monto y periodo por cuota, que cumple las reglas del producto en **todas** las etapas;
3. explica **por qué cada cuota es alta o baja** y muestra la relación Cuota/UN por etapa y los supuestos usados;
4. compara el plan con la **cuota fija equivalente** en escenario base y adversos (periodos en tensión, costo total y TCEA, concentración, déficit del cliente, ingreso y exposición de la Caja);
5. permite al asesor **ajustar** (factor menor, corrección de una etapa, fecha de pago) y recalcular, y exporta la **hoja para comité**.

**Criterios de aceptación** (verificables con pruebas, base del mínimo 3/5):

- El cronograma reproduce las reglas del owner: TEA → TED base 360 por días exactos; seguros por interés simple; prelación seguros → interés → capital; lo no cubierto queda pendiente en su concepto y se paga primero en el periodo siguiente.
- Ninguna cuota supera factor × UN esperada de su etapa; el factor usado nunca supera el del producto.
- Con un ciclo plano, el plan coincide con la cuota fija (control de cordura); con un ciclo estacional, las cuotas altas caen en las cimas.
- Ninguna cuota concentra más capital que el tope configurado y no hay más periodos sin amortizar que los permitidos.
- Si no existe plan posible, el sistema lo dice y nombra la restricción que lo impide; no entrega un plan que incumple.
- Toda cifra del resumen para comité coincide con el cálculo del motor (verificación en código).
- Misma entrada, mismo resultado (semilla fija).

Esta funcionalidad se construye **durante la fase presencial**, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

**Prototipo funcional de punta a punta con caso de uso**, sin conexión a sistemas de la Caja. Demo guionada **(supuesto)**: un productor de arroz del valle de Jequetepeque y un taller de calzado de El Porvenir piden el mismo monto; el sistema muestra que tienen ciclos distintos, propone dos planes distintos con el porqué de cada cuota, y los compara con la cuota fija en un año normal y en un escenario El Niño. Se cierra con los resultados del banco de pruebas sobre la cartera sintética: periodos en tensión, costo y ajuste al ciclo, adaptado frente a fijo.

Incluye pruebas automáticas del cálculo financiero y del motor, reporte de validación (`docs/validacion.md`) y el número antes/después del KPI.

**Fuera de alcance:** integración con el core, reprogramaciones y refinanciaciones (uso opcional que no suma en la evaluación), aprobación automática, aplicativo móvil nativo.

## 8. Factibilidad y dependencias

- **Esfuerzo estimado del MVP: 31 horas-persona (supuesto)** de 32 disponibles (4 personas × ~8 h netas). Núcleo no recortable: 26 h. Detalle y plan hora a hora en `panorama.md` §d.
- **Por qué es factible:** el cálculo financiero es determinista y se puede probar contra casos hechos a mano; el programa lineal es pequeño (decenas de variables por crédito) y se resuelve en milisegundos con SciPy; el modelo del ciclo parte de patrones por sector y zona, no de un entrenamiento pesado.
- **Cobertura del equipo:** Antonio (economista, sector financiero) lleva reglas del producto, KPI y prueba de estrés; Glem, datos y modelo del ciclo; Mariano, motor, API y LLM; David, interfaz del asesor y hoja para comité.
- **Dependencias:**
  - Datos: la Caja **no entregará datos**, ni anonimizados. Usamos perfiles sintéticos propios y series públicas.
  - Factores por producto, cuota mínima, plazo máximo y topes de sobreendeudamiento: el owner dio ejemplos ilustrativos (0,65 en inclusión, 0,85 en Pequeña Empresa); los valores reales son **[POR CONFIRMAR]** y quedan configurables.
  - LLM externo: el owner lo permite **solo para la demo**, con datos sintéticos y sin conexión a sus sistemas; el proveedor es intercambiable y hay modo sin red por plantillas.
  - Línea base de retención y diseño de un piloto: **[POR CONFIRMAR]**.
- **Riesgos principales:** patrones públicos con poca granularidad por zona (se mitiga con calendarios de campaña y el ajuste del asesor), un ciclo optimista (prueba de estrés y holgura), un problema sin solución factible (diagnóstico de la restricción) y tiempo de interfaz (vista mínima primero).
- **Recorte si falta tiempo** (en orden): asistente de notas de campo con LLM → resumen para comité con LLM (queda por plantilla) → varios escenarios adversos (queda uno) → pulido visual. **No se recorta:** ciclo con banda, motor con reglas del owner, explicación por cuota, comparación con cuota fija y pruebas.

---

## Anexo A. Tareas y horas (supuesto)

| Tarea | Habilidad | Horas |
|---|---|---|
| Perfiles y escenarios sintéticos (o carga del generador, si existe) | data_eng | 2 |
| Patrones sector × zona y modelo del ciclo con banda | ml | 4 |
| Motor de optimización y cronograma con las reglas del owner | data_sci | 5 |
| Prueba de estrés y comparación con cuota fija | biz | 3 |
| Explicación por cuota y resumen verificado para comité | agentes | 2 |
| API | backend | 2 |
| Interfaz: ciclo → plan → comparación → hoja de comité | web | 5 |
| Pruebas y validación | qa | 3 |
| **Núcleo** | | **26** |
| Flujo del asesor y del comité | ux | 1 |
| Reglas de producto, factores y casos de negocio | fin | 2 |
| Pitch y demo | pitch | 2 |
| **Total** | | **31** |

## Anexo B. Preguntas para el owner

Resueltas por las preguntas frecuentes y el ticket del 24.11 (ver cotejo en `panorama.md`): alcance (créditos nuevos), usuarios y canal, flexibilidad del plan, límite Cuota/UN, cálculo de intereses y seguros, prelación y pendientes, datos (no se entregan), variables y fuentes, qué se evaluará, uso de LLM externo (solo demo).

Siguen abiertas (los tickets cerraron el 24.11; se asumen y se marcan):

- [ ] ¿Qué factor, cuota mínima, plazo máximo y topes de sobreendeudamiento usar por producto en la demo? (supuesto: los ejemplos ilustrativos del owner, configurables)
- [ ] ¿Existe una regla de holgura frente a escenarios adversos o queda a criterio del asesor? (supuesto: cuota cubierta por la UN en el escenario adverso)
- [ ] ¿Hay un tope de concentración de capital o de periodos de gracia por producto? (supuesto: configurable)
- [ ] ¿Cómo se mediría la retención en un piloto y cuál es su línea base?

## Anexo C. Lista de revisión (criterios del pase a finalistas)

- [ ] **Alineación (25%)**: ¿ataca el problema central del expediente, con sus palabras?
- [ ] **Impacto (30%)**: ¿hay KPI, línea base y método de medición, sin cifras inventadas?
- [ ] **Viabilidad técnica (25%)**: ¿hay un enfoque coherente, con IA/analítica de valor real?
- [ ] **Factibilidad (20%)**: ¿la funcionalidad crítica cabe en ~8 h por persona? ¿Qué se recorta?
- [ ] Preexistente identificado y sin datos ni código de terceros indebidos.
- [ ] Todo lo no oficial está marcado como (supuesto) o [POR CONFIRMAR].
- [ ] Revisado por alguien que no lo escribió.
