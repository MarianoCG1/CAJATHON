# NEG-01 — Texto para el formulario de Concept Solution (7 secciones)

> Formulario habilitado el 25.11 a las 18:26 (comunicado n.º 12). **Cierra el jueves 26.11 a las 11:59 p. m.** Solo el coordinador edita y envía.
> Los campos exactos y sus límites de longitud **no se ven sin ser coordinador**. Por eso cada sección trae una **versión corta (≤ 1,000 caracteres)** y una **completa**: se pega la que quepa. Fuente: `concepto.md`, `panorama.md` y `postulacion.md` de este reto.
> El comunicado pide **describir la solución y qué se construirá o adaptará en las jornadas presenciales**, no presentar un prototipo.

---

## 1. Identificación de la propuesta

- **Desafío:** NEG-01 · Plan de pagos adaptado al ciclo económico del negocio (Eje 4: Inclusión financiera y resiliencia)
- **Equipo:** Yupana Labs
- **Nombre de la propuesta:** Ritmo: plan de pagos al ciclo del negocio
- **Resumen (≤ 500 caracteres):**

Ritmo ayuda al Asesor de Negocios a estimar el ciclo económico de cada cliente (patrón del sector y la zona ajustado con lo observado en campo) y a obtener el plan de pagos de menor costo que cabe en su utilidad en cada etapa, con holgura bajo el tope y frente a escenarios adversos. Explica cada cuota y la compara con la cuota fija. El asesor ajusta y explica al cliente; Riesgos valida; el comité decide.

## 2. Concepto de solución

**Versión corta**

Hoy la evaluación usa un ingreso promedio y el core solo genera cuotas fijas; los negocios estacionales se ahogan en los valles aunque sean viables. Ritmo tiene tres piezas. (A) Modelo del ciclo: el patrón del sector y la zona (BCRP, MIDAGRI, calendarios comerciales) se ajusta al cliente según su evidencia y se proyecta a los meses del crédito con el estado previsto de El Niño (ENFEN, ONI); entrega la utilidad neta por etapa con su banda. (B) Motor de optimización: amortiza el máximo capital en las cimas con Cuota/UN bajo el tope del producto, con holgura, y con la cuota cubierta por la utilidad en los escenarios adversos; aplica la prelación y los pendientes que fijó el owner; si el monto no cabe, propone el monto o el plazo que sí cabe. (C) El motivo de cada cuota y su comparación con la cuota fija. El asesor ajusta; el comité decide.

**Versión completa**

Los ingresos de muchos microempresarios dependen de campañas, cosechas, clima y la dinámica de su zona, y dos negocios del mismo rubro pueden tener ciclos distintos. Hoy la evaluación pondera un ingreso estándar único y el core solo genera cuotas fijas con una periodicidad única; el asesor no tiene cómo cruzar información del sector y la zona con la realidad de su cliente. Resultado: problemas de liquidez en los valles, incluso en negocios viables.

Ritmo es una herramienta para el Asesor de Negocios con las tres piezas que pide el desafío:

(A) **Modelo del ciclo en dos capas.** El patrón estacional del sector y la zona, construido con series y calendarios públicos, se ajusta a cada cliente con lo que el asesor recoge en campo (ventas en meses buenos, regulares y malos, costos, gastos, carga familiar, evidencias de transacciones, fechas de campaña). Cuanta más evidencia, más pesa el dato propio; sin evidencia, el cliente hereda el patrón de su sector y zona. Luego proyecta los meses concretos del crédito con el estado previsto de los factores externos: la sensibilidad de cada sector a El Niño se estima con la historia (producción mensual del BCRP frente a los índices ONI e ICEN, incluidos 2017 y 2023) y se aplica al estado que anuncian el ENFEN y el SENAMHI. Entrega la utilidad neta esperada por etapa durante la vida del crédito, con banda de incertidumbre y escenarios adversos.

(B) **Motor del plan de pagos.** Con monto, TEA, seguros y plazo, un programa de optimización elige cuánto capital amortiza cada cuota. Respeta en cada etapa Cuota/UN ≤ factor efectivo, por debajo del tope del producto para dejar la holgura que pide el desafío, y además que la cuota quede cubierta por la utilidad de los escenarios adversos. También respeta cuota mínima, plazo máximo, TEA única y topes de concentración de capital y de periodos sin amortizar. Amortiza el máximo capital en las cimas y, entre los planes posibles, elige el de menor costo total para el cliente. Aplica las reglas del owner: TED base 360 por días exactos, seguros por interés simple, prelación seguros → interés → capital, y pendientes sin interés cuando un valle no cubre ni los intereses. Si el monto no cabe, indica qué restricción lo impide y propone el monto máximo para ese plazo o el plazo que necesita ese monto.

(C) **Explicación y prueba de estrés.** Cada cuota trae su motivo (etapa, utilidad esperada, Cuota/UN y restricción que la limita) y el plan se compara con la cuota fija equivalente en escenario base y adversos.

El asesor conserva su criterio (factor menor, corrección de una etapa, fecha de pago) y el comité aprueba.

## 3. Impacto esperado

**Versión corta**

KPI del prototipo: meses en que la cuota supera la capacidad (Cuota/UN > factor, y cuota > utilidad), plan adaptado frente a cuota fija, en escenario base y adversos. Secundarios: costo y TCEA, ajuste al ciclo, concentración e ingreso de la Caja. No medimos mora, como indicó el owner; la retención se mediría en un piloto. Ejemplo ilustrativo calculado con las reglas del owner (no es una medición): un arrocero de Jequetepeque pide S/ 8,000 a 12 meses. Con su utilidad promedio califica para cuota fija (S/ 801), pero esa cuota supera su utilidad en 8 de 12 meses. Con holgura bajo el tope y frente a El Niño, el motor propone S/ 5,895 a 12 meses o S/ 8,000 a 17 meses, sin ningún mes de déficit en año normal, con El Niño ni con caída de ventas de 20 %. Las cifras de impacto saldrán del banco de pruebas con perfiles sintéticos.

**Versión completa**

Para el cliente: cuotas que caben en su utilidad en cada etapa, menos meses de asfixia y un plan cuyo costo se muestra frente a la cuota fija. Para la Caja: un plan sustentado y explicable ante el comité, con riesgos cuantificados antes del desembolso, y una herramienta que apoya la retención de clientes estacionales.

| KPI | Cómo se mide |
|---|---|
| **Principal:** periodos en tensión (Cuota/UN > factor; cuota > UN), adaptado frente a cuota fija, base y adversos | Banco de pruebas con perfiles sintéticos |
| Costo total (interés + seguros) y TCEA frente a cuota fija | Mismo banco de pruebas |
| Ajuste al ciclo (correlación cuota–utilidad) y error del ciclo estimado frente al verdadero | Perfiles con ciclo verdadero conocido |
| Concentración de capital y periodos sin amortizar | Mismo banco de pruebas |
| Ingreso financiero y saldo expuesto de la Caja | Mismo banco de pruebas |
| **Negocio (piloto):** retención y renovación | Línea base a confirmar con la Caja |

**Ejemplo ilustrativo** (calculado a mano con las reglas del owner; no es una medición). Un pequeño arrocero del valle de Jequetepeque pide S/ 8,000 a 12 meses (TEA 40 %, factor 0,65; utilidad mensual ilustrativa entre S/ 400 y S/ 4,200, promedio S/ 1,304):

| Plan | Meses con cuota > utilidad (año normal / El Niño / caída de 20 %) | Déficit acumulado del cliente |
|---|---|---|
| Cuota fija, S/ 801 × 12 | 8 / 9 / 9 de 12 | S/ 1,861 / 2,012 / 2,852 |
| Siguiendo el ciclo al tope, sin holgura | 0 / 2 / 0 | S/ 0 / 1,940 / 0 |
| Ritmo con holgura: S/ 5,895 a 12 meses, o S/ 8,000 a 17 meses | 0 / 0 / 0 | S/ 0 |
| Cuota fija a 17 meses, S/ 606 | 8 / 8 / 11 de 17 | S/ 994 / 994 / 1,941 |

Con la utilidad promedio el cliente «califica» para la cuota fija, pero esa cuota supera su utilidad en 8 de 12 meses. Seguir el ciclo al tope, sin holgura, es frágil ante un mes de retraso en la cosecha. Ritmo deja holgura bajo el tope (factor efectivo de 0,585 frente a 0,65), cubre los escenarios adversos en toda la vida del crédito y limita la concentración de capital; por eso no fuerza el monto pedido y propone el monto o el plazo que sí caben.

Línea base del prototipo: la cuota fija equivalente que genera hoy el core (mismas condiciones). No medimos mora de cartera, como indicó el owner. Los planes se construyen con lo que observaría el asesor y se evalúan contra el ciclo verdadero de cada perfil y contra escenarios adversos fijados de antemano. Las cifras saldrán de esa medición; no las inventamos.

## 4. Enfoque tecnológico

**Versión corta**

Analítica predictiva del ciclo (descomposición estacional de series públicas y ajuste al cliente por agregación parcial), optimización con un programa lineal (SciPy, HiGHS) y cálculo financiero con las reglas del owner. Python, FastAPI, SQLite y React. Un modelo de lenguaje intercambiable, solo para la demo y con datos sintéticos, redacta el resumen para comité y estructura las notas de campo; una verificación en código impide que introduzca cifras. Funciona sin conexión a la Caja y con modo sin red. Preexistente: solo librerías abiertas y herramientas de planificación del equipo; sin código de empleadores ni datos reales. No es un dashboard ni un chatbot: el valor está en el modelo del ciclo y en el motor de optimización.

**Versión completa**

| Capa | Qué hace |
|---|---|
| Patrones públicos | Índice estacional y volatilidad por actividad y zona (descomposición estacional de series del BCRP e INEI; calendarios de cosecha de MIDAGRI; El Niño según SENAMHI/ENFEN; calendarios comerciales) |
| Modelo del ciclo | Ajuste al cliente por agregación parcial; utilidad neta por etapa con banda de incertidumbre y escenarios adversos |
| Proyección | Sensibilidad de cada sector a El Niño estimada con series del BCRP frente a ONI/ICEN con rezagos; ajuste de los meses del crédito con el estado previsto (ENFEN, SENAMHI) |
| Motor del plan | Programa entero mixto (SciPy `milp`, HiGHS): máximo capital en cimas y menor costo, con Cuota/UN ≤ factor efectivo (90 % del tope, configurable), cuota cubierta por la utilidad de cada escenario adverso en todos los meses, tope de capital por cuota y de periodos sin amortizar; una binaria por periodo para la prelación y los pendientes; si no cabe, propone monto máximo o plazo mínimo |
| Cronograma | TED base 360 por días exactos y periodos de cualquier duración; seguros por interés simple (desgravamen, multirriesgo o vivienda); prelación seguros → interés → capital; pendientes en su concepto; TCEA |
| Validaciones | TEA ≤ tasa máxima del BCRP; seguros excluyentes y obligatorios según producto; UN según tipo de cliente (otras deudas, carga familiar, EEFF) |
| Explicación | Motivo de cada cuota según la restricción activa; resumen para comité redactado por un modelo de lenguaje intercambiable y verificado en código |
| API e interfaz | FastAPI y React: ciclo → plan → comparación; hoja para el cliente, vista de validación para Riesgos con registro de ajustes del asesor, y hoja para comité |

Stack: Python 3.11, FastAPI, Pydantic, pandas, statsmodels, scikit-learn, SciPy, SQLite, React, pytest. El modelo de lenguaje es opcional y reemplazable (nube, local o plantillas sin red); el owner lo permite solo en la demo y con datos sintéticos.

Tecnología preexistente: librerías de código abierto bajo sus licencias y herramientas de planificación del equipo, que no forman parte de la solución. No se reutiliza código de empleadores ni de otros clientes, ni datos reales.

## 5. Alcance del prototipo

**Versión corta**

Qué construiremos en las jornadas presenciales: dado un cliente y una operación, el sistema estima su ciclo, construye el plan óptimo con monto y periodo por cuota, explica por qué cada cuota es alta o baja, muestra Cuota/UN por etapa y lo compara con la cuota fija en escenarios base y adversos; el asesor ajusta y exporta la hoja para el cliente, la vista para Riesgos y la hoja para comité. Demo: un arrocero y un taller de calzado de La Libertad con el mismo monto reciben planes distintos y explicados, en un año normal y con El Niño. Pruebas automáticas: el cronograma reproduce las reglas del owner, ninguna cuota supera el factor y con un ciclo plano todas las cuotas salen iguales. Esfuerzo: 31 de 32 horas-persona (supuesto). Fuera de alcance: integración con el core y reprogramaciones.

**Versión completa**

Se construye íntegramente en las jornadas presenciales, con commits frecuentes como evidencia:

1. Estimación del ciclo del cliente (utilidad neta por etapa y su banda), combinando el patrón del sector y la zona con la información propia.
2. Plan de pagos óptimo con monto y periodo por cuota, que cumple las reglas del producto en todas las etapas.
3. Motivo de cada cuota y relación Cuota/UN por etapa, con los supuestos a la vista.
4. Comparación con la cuota fija equivalente en escenario base y adversos (periodos en tensión, costo y TCEA, concentración, déficit del cliente, ingreso de la Caja).
5. Ajuste por el asesor (factor menor, corrección de una etapa, fecha de pago, factor cualitativo con su motivo) con registro de cambios; hoja para el cliente, vista para el Asesor de Riesgos y hoja para comité.

Criterios de aceptación, verificados con pruebas automáticas: el cronograma reproduce las reglas del owner, también con periodos no mensuales; ninguna cuota supera factor efectivo × utilidad de su etapa ni la utilidad de los escenarios adversos; cinco casos calculados a mano (entre ellos, S/ 8,000 a 12 meses que no cabe y la salida a 17 meses) son las primeras pruebas; con un ciclo plano todas las cuotas salen iguales y con uno estacional las cuotas altas caen en las cimas; si no hay plan posible, el sistema nombra la restricción que lo impide; toda cifra del resumen coincide con el cálculo.

Factibilidad: 31 horas-persona de 32 disponibles (supuesto), con un núcleo de 26 que no se recorta. Si falta tiempo se recortan, en este orden, el asistente de notas, el resumen con modelo de lenguaje y los escenarios adicionales. El cálculo es determinista y verificable contra casos hechos a mano, y el programa lineal se resuelve en milisegundos. El equipo cubre economía y sector financiero, ciencia de datos, desarrollo y experiencia de usuario.

Fuera de alcance: integración con el core, reprogramaciones y refinanciaciones, aprobación automática y app móvil nativa.

## 6. Datos e insumos

**Versión corta**

No usamos datos de la Caja (no se entregarán) ni historial de pagos, que el owner descartó para estimar el ciclo. Fuentes públicas: BCRP (producción mensual por cultivo, como arroz y papa, y síntesis mensual de La Libertad); MIDAGRI e INIA (calendarios de siembra y cosecha, intenciones de siembra); NOAA (índice ONI), IGP y ENFEN (El Niño costero); SENAMHI (pronóstico estacional); calendarios comerciales. Datos del negocio: cartera sintética de unos 2,000 negocios de La Libertad (arroz, caña, papa, calzado, bodegas, restaurantes, transporte, aves), cada uno con ciclo verdadero conocido y lo que vería el asesor: ventas por tipo de mes, costos, gastos, carga familiar, transacciones y fechas de campaña. Condiciones del producto configurables.

**Versión completa**

| Insumo | Fuente | Uso |
|---|---|---|
| Estacionalidad por cultivo y sector | BCRPData (producción mensual por cultivo, por ejemplo arroz cáscara PN01778AM y papa PN01777AM); síntesis mensual de La Libertad del BCRP (Sucursal Trujillo); INEI (producción por sector) | Patrón del sector y la región |
| Calendario de siembra y cosecha por cultivo y zona | MIDAGRI (El Agro en Cifras, evaluación regional, intenciones de siembra) e INIA (calendario agrícola de la Región Costa) | Cimas y valles agrícolas por zona |
| Episodios climáticos | NOAA (índice ONI), IGP (ICEN) y comunicados del ENFEN; pronóstico estacional del SENAMHI | Sensibilidad de cada sector a El Niño y escenarios adversos |
| Calendarios comerciales | Campaña escolar, Día de la Madre, Fiestas Patrias, Navidad, verano | Picos de comercio y servicios |
| Datos del negocio | Cartera sintética propia: ventas en meses buenos, regulares y malos; costos; gastos; carga familiar; evidencias de transacciones; fechas de campaña | Ajuste al cliente y banco de pruebas |
| Condiciones del producto | Factor Cuota/UN (ejemplos del owner: 0,65 inclusión, 0,85 Pequeña Empresa), cuota mínima, plazo máximo, TEA, seguros | Restricciones del motor, todas configurables |

La cartera sintética tiene unos 2,000 negocios de La Libertad (arroz en Jequetepeque, caña en Chicama, papa en la sierra, calzado en El Porvenir, bodegas en Trujillo, restaurantes en Huanchaco, transporte y aves) con semilla fija. Cada perfil tiene un ciclo verdadero conocido y, por separado, lo que observaría el asesor, para medir la precisión del modelo sin datos reales.

No usamos datos de la Caja (el owner indicó que no se entregarán, ni anonimizados) ni historial de pagos de cartera, que el owner descartó como fuente para el ciclo. Las series públicas son datos abiertos y agregados; no hay datos personales.

## 7. Revisión y envío

Antes de enviar (coordinador):

- [ ] Comparar cada campo con su límite de caracteres; si no cabe la versión completa, pegar la corta.
- [ ] Confirmar que el desafío seleccionado es NEG-01 y que el título coincide.
- [ ] Confirmar con el equipo si el formulario admite **más de una** postulación. Si admite solo una, la regla del equipo es postular **RIE-03**.
- [ ] Verificar que no quedan marcas internas: «[POR CONFIRMAR]», «(supuesto)» o rutas de archivos.
- [ ] Guardar una captura del formulario enviado en el repo, en `docs/`.
- [ ] Enviar antes del **jueves 26.11, 11:59 p. m.**
