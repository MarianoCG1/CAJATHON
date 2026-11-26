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

Ritmo ayuda al Asesor de Negocios a estimar el ciclo económico de cada cliente (patrón del sector y la zona ajustado con lo observado en campo) y a obtener el plan de pagos de menor costo que respeta Cuota/Utilidad Neta ≤ factor en cada etapa. Explica por qué cada cuota es alta o baja y compara el plan con la cuota fija en escenarios base y adversos. El asesor ajusta; el comité decide.

## 2. Concepto de solución

**Versión corta**

Hoy la evaluación usa un ingreso promedio y el core solo genera cuotas fijas; los negocios estacionales se ahogan en los valles aunque sean viables. Ritmo tiene tres piezas. (A) Modelo del ciclo: el patrón estacional del sector y la zona (BCRP, INEI, MIDAGRI, SENAMHI, calendarios comerciales) se ajusta a cada cliente según su evidencia; entrega la utilidad neta por etapa con su banda de incertidumbre. (B) Motor de optimización: elige el capital de cada cuota para que Cuota/UN ≤ factor en cada etapa, con cuota mínima, plazo y topes de concentración y gracia; entre los planes válidos escoge el de menor costo, que amortiza más en las cimas. (C) Explicación: el motivo de cada cuota y la comparación con la cuota fija. El asesor puede bajar el factor o corregir una etapa; el comité decide.

**Versión completa**

Los ingresos de muchos microempresarios dependen de campañas, cosechas, clima y la dinámica de su zona, y dos negocios del mismo rubro pueden tener ciclos distintos. Hoy la evaluación pondera un ingreso estándar único y el core solo genera cuotas fijas con una periodicidad única; el asesor no tiene cómo cruzar información del sector y la zona con la realidad de su cliente. Resultado: problemas de liquidez en los valles, incluso en negocios viables.

Ritmo es una herramienta para el Asesor de Negocios con las tres piezas que pide el desafío:

(A) **Modelo del ciclo en dos capas.** El patrón estacional del sector y la zona, construido con series y calendarios públicos, se ajusta a cada cliente con lo que el asesor recoge en campo (ventas en meses buenos, regulares y malos, costos, gastos, carga familiar, evidencias de transacciones, fechas de campaña). Cuanta más evidencia, más pesa el dato propio; sin evidencia, el cliente hereda el patrón de su sector y zona. Entrega la utilidad neta esperada por etapa durante la vida del crédito, con banda de incertidumbre y escenarios adversos.

(B) **Motor del plan de pagos.** Con monto, TEA, seguros y plazo, un programa lineal elige cuánto capital amortiza cada cuota. Respeta en cada etapa Cuota/UN ≤ factor del asesor ≤ factor del producto, cuota mínima, plazo máximo, TEA única y topes de concentración de capital y de periodos sin amortizar. Entre todos los planes que cumplen, elige el de menor costo total para el cliente, que es el que amortiza el máximo capital en las cimas. Aplica las reglas del owner: TED base 360 por días exactos, seguros por interés simple, prelación seguros → interés → capital y pendientes en su concepto. Si no hay plan posible, indica qué restricción lo impide.

(C) **Explicación y prueba de estrés.** Cada cuota trae su motivo (etapa, utilidad esperada, Cuota/UN y restricción que la limita) y el plan se compara con la cuota fija equivalente en escenario base y adversos.

El asesor conserva su criterio (factor menor, corrección de una etapa, fecha de pago) y el comité aprueba.

## 3. Impacto esperado

**Versión corta**

KPI del prototipo: porcentaje de periodos en tensión (cuota > factor × utilidad, y cuota > utilidad) del plan adaptado frente a la cuota fija, en escenario base y adversos (caída de ventas, campaña retrasada, El Niño). Secundarios: costo total y TCEA para el cliente (muestra si hay encarecimiento), ajuste de las cuotas al ciclo, error del ciclo estimado, concentración de capital, e ingreso y exposición de la Caja. No medimos mora, como indicó el owner. Se mide en un banco de pruebas reproducible con perfiles sintéticos de varios rubros, zonas y productos, cuyo ciclo verdadero se conoce. Las cifras saldrán de esa medición; no las inventamos. La retención, indicador de negocio señalado por el owner, se mediría en un piloto con línea base a confirmar.

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

Línea base del prototipo: la cuota fija equivalente que genera hoy el core (mismas condiciones). No medimos mora de cartera, como indicó el owner. Los planes se construyen con lo que observaría el asesor y se evalúan contra el ciclo verdadero de cada perfil y contra escenarios adversos fijados de antemano. Las cifras saldrán de esa medición; no las inventamos.

## 4. Enfoque tecnológico

**Versión corta**

Analítica predictiva del ciclo (descomposición estacional de series públicas y ajuste al cliente por agregación parcial), optimización con un programa lineal (SciPy, HiGHS) y cálculo financiero con las reglas del owner. Python, FastAPI, SQLite y React. Un modelo de lenguaje intercambiable, solo para la demo y con datos sintéticos, redacta el resumen para comité y estructura las notas de campo; una verificación en código impide que introduzca cifras. Funciona sin conexión a la Caja y con modo sin red. Preexistente: solo librerías abiertas y herramientas de planificación del equipo; sin código de empleadores ni datos reales. No es un dashboard ni un chatbot: el valor está en el modelo del ciclo y en el motor de optimización.

**Versión completa**

| Capa | Qué hace |
|---|---|
| Patrones públicos | Índice estacional y volatilidad por actividad y zona (descomposición estacional de series del BCRP e INEI; calendarios de cosecha de MIDAGRI; El Niño según SENAMHI/ENFEN; calendarios comerciales) |
| Modelo del ciclo | Ajuste al cliente por agregación parcial; utilidad neta por etapa con banda de incertidumbre y escenarios adversos |
| Motor del plan | Programa lineal (SciPy, HiGHS): menor costo total sujeto a Cuota/UN ≤ factor por etapa y topes del producto; diagnóstico si no hay solución |
| Cronograma | TED base 360 por días exactos; seguros por interés simple; prelación seguros → interés → capital; pendientes en su concepto; TCEA |
| Explicación | Motivo de cada cuota según la restricción activa; resumen para comité redactado por un modelo de lenguaje intercambiable y verificado en código |
| API e interfaz | FastAPI y React: ciclo → plan → comparación → hoja para comité |

Stack: Python 3.11, FastAPI, Pydantic, pandas, statsmodels, scikit-learn, SciPy, SQLite, React, pytest. El modelo de lenguaje es opcional y reemplazable (nube, local o plantillas sin red); el owner lo permite solo en la demo y con datos sintéticos.

Tecnología preexistente: librerías de código abierto bajo sus licencias y herramientas de planificación del equipo, que no forman parte de la solución. No se reutiliza código de empleadores ni de otros clientes, ni datos reales.

## 5. Alcance del prototipo

**Versión corta**

Qué construiremos en las jornadas presenciales: dado un cliente y una operación, el sistema estima su ciclo, construye el plan óptimo con monto y periodo por cuota, explica por qué cada cuota es alta o baja, muestra Cuota/UN por etapa y lo compara con la cuota fija en escenarios base y adversos; el asesor ajusta y exporta la hoja para comité. Demo: un arrocero y un taller de calzado de La Libertad con el mismo monto reciben planes distintos y explicados, en un año normal y con El Niño. Pruebas automáticas: el cronograma reproduce las reglas del owner, ninguna cuota supera el factor y con un ciclo plano el plan coincide con la cuota fija. Esfuerzo: 31 de 32 horas-persona (supuesto). Fuera de alcance: integración con el core y reprogramaciones.

**Versión completa**

Se construye íntegramente en las jornadas presenciales, con commits frecuentes como evidencia:

1. Estimación del ciclo del cliente (utilidad neta por etapa y su banda), combinando el patrón del sector y la zona con la información propia.
2. Plan de pagos óptimo con monto y periodo por cuota, que cumple las reglas del producto en todas las etapas.
3. Motivo de cada cuota y relación Cuota/UN por etapa, con los supuestos a la vista.
4. Comparación con la cuota fija equivalente en escenario base y adversos (periodos en tensión, costo y TCEA, concentración, déficit del cliente, ingreso de la Caja).
5. Ajuste por el asesor (factor menor, corrección de una etapa, fecha de pago) y hoja para comité.

Criterios de aceptación, verificados con pruebas automáticas: el cronograma reproduce las reglas del owner; ninguna cuota supera factor × utilidad de su etapa; con un ciclo plano el plan coincide con la cuota fija y con uno estacional las cuotas altas caen en las cimas; si no hay plan posible, el sistema nombra la restricción que lo impide; toda cifra del resumen coincide con el cálculo.

Factibilidad: 31 horas-persona de 32 disponibles (supuesto), con un núcleo de 26 que no se recorta. Si falta tiempo se recortan, en este orden, el asistente de notas, el resumen con modelo de lenguaje y los escenarios adicionales. El cálculo es determinista y verificable contra casos hechos a mano, y el programa lineal se resuelve en milisegundos. El equipo cubre economía y sector financiero, ciencia de datos, desarrollo y experiencia de usuario.

Fuera de alcance: integración con el core, reprogramaciones y refinanciaciones, aprobación automática y app móvil nativa.

## 6. Datos e insumos

**Versión corta**

No usamos datos de la Caja (el owner indicó que no se entregarán) ni historial de pagos, que no es buena fuente para estimar el ciclo. Usamos dos fuentes: (1) series y calendarios públicos para el patrón del sector y la zona: BCRP e INEI (estacionalidad por sector), MIDAGRI (siembra y cosecha por cultivo y zona), SENAMHI/ENFEN (El Niño) y calendarios comerciales (campaña escolar, Fiestas Patrias, Navidad, verano); (2) una cartera sintética de unos 2,000 negocios de La Libertad (arroz, caña, papa, calzado, bodegas, restaurantes, transporte, aves), cada uno con un ciclo verdadero conocido y lo que vería el asesor: ventas por tipo de mes, costos, gastos, carga familiar, transacciones y fechas de campaña. Condiciones del producto (factor, cuota mínima, plazo, TEA, seguros) configurables.

**Versión completa**

| Insumo | Fuente | Uso |
|---|---|---|
| Estacionalidad por sector | BCRP (series regionales y nacionales), INEI (producción por sector) | Patrón del sector |
| Calendario de siembra y cosecha por cultivo y zona | MIDAGRI | Cimas y valles agrícolas por zona |
| Episodios climáticos | SENAMHI / ENFEN | Escenarios adversos (El Niño) |
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
