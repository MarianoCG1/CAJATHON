# NEG-01 — formulario «Concept Solution», listo para pegar

**Fecha límite:** jueves 26 de noviembre, 11:59 p. m. (hora de Perú). **Se envía un solo desafío por equipo.**
Cada bloque gris se copia entero en su campo. El conteo es de caracteres frente al máximo del formulario.

## Paso 1 · Identificación de la propuesta

- **Desafío seleccionado:** pestaña Negocios → **NEG-01 · Plan de pagos adaptado al ciclo económico del negocio**
- **Nombre de la solución** (41/80):

```text
Ritmo: plan de pagos al ciclo del negocio
```

## Paso 2 · Concepto de solución

**¿En qué consiste su solución y cómo aborda la problemática del desafío?** (obligatoria) — 1768/2000

```text
Hoy la evaluación pondera un ingreso estándar único y el sistema central solo genera cuotas fijas con una periodicidad única. Los negocios que dependen de campañas, cosechas o clima pueden quedarse sin liquidez en sus meses bajos aunque sean viables, y dos negocios del mismo rubro pueden tener ciclos distintos.

Ritmo es una herramienta para el Asesor de Negocios que, desde la admisión, estima el ciclo económico de cada cliente y construye el plan de pagos de menor costo que respeta la capacidad de pago en cada etapa. Tiene las tres piezas que pide el desafío:

(A) un modelo del ciclo, que combina el patrón del sector y la zona con lo que el asesor observa del negocio;
(B) un motor que arma el plan, con monto y periodo por cuota, bajo las reglas del producto;
(C) la explicación de por qué cada cuota es alta o baja y su comparación con la cuota fija en escenarios base y adversos.

Del mismo cálculo salen una hoja para explicar al cliente, la vista para que Riesgos valide y la hoja para comité, con el ciclo, las cuotas, la relación Cuota/Utilidad Neta por etapa y los supuestos. Cada ajuste del asesor queda registrado con su motivo; nada se aprueba solo. Trata los riesgos del desafío: estimación optimista (holgura frente a escenarios adversos), concentración de capital (tope por cuota), encarecimiento (se muestra el costo frente a la cuota fija), sobreendeudamiento (utilidad neta de otras deudas y carga familiar) y dependencia del modelo (todo es visible y editable). Sirve para créditos nuevos (admisión, ampliación y recuperación), clientes formales e informales, con o sin historial, y distintos rubros, zonas y productos. Respeta políticas, condiciones contractuales y normativa. Web adaptable al móvil, sin conexión a los sistemas de la Caja.
```

**¿Cómo funcionaría su solución?** (obligatoria) — 1320/2000

```text
1. El asesor ingresa tipo de cliente, sector, zona, modelo de negocio y lo recogido en campo: ventas en meses buenos, regulares y malos, costos, gastos, carga familiar, evidencias de transacciones y fechas de campaña.
2. El modelo del ciclo parte del patrón estacional del sector y la zona (series y calendarios públicos) y lo ajusta al cliente: cuanta más evidencia, más pesa su dato. Entrega la utilidad neta por etapa, descontando otras deudas y, en ampliaciones, la cuota vigente, con banda y escenarios adversos.
3. Un programa de optimización elige cuánto capital amortiza cada cuota. Por defecto, la Cuota/Utilidad Neta no pasa del 90 % del tope del producto (holgura configurable), la cuota debe caber en la utilidad de cada escenario adverso en todos los meses del crédito y ninguna amortiza más del 25 % del capital.
4. Aplica las reglas del owner: TEA única y editable (sin superar la tasa máxima del BCRP), TED base 360 por días exactos, periodos que pueden no ser mensuales, seguros por interés simple, prelación seguros, interés y capital, y pendientes sin interés.
5. Si el monto no cabe, dice qué restricción lo impide y propone el monto máximo para ese plazo o el plazo que necesita ese monto.
6. Muestra el motivo de cada cuota y la comparación con la cuota fija; el asesor ajusta, recalcula y exporta.
```

**¿Qué diferencia su solución de otras alternativas existentes?** (obligatoria) — 618/1000

```text
Frente a simuladores de cuota fija y cronogramas estacionales con cuotas iguales: (1) estima y explica el ciclo de cada negocio, no solo de su rubro; (2) construye el plan desde ese ciclo con restricciones verificables, no redistribuye un cronograma fijo; (3) exige holgura bajo el tope y frente a escenarios adversos y, si el monto no cabe, lo dice en vez de forzarlo; (4) cuantifica beneficios y riesgos frente a la cuota fija, incluido el costo; (5) el motivo de cada cuota sale de las reglas del cálculo, no de un modelo de lenguaje. No es un tablero ni un chatbot: el valor está en el modelo del ciclo y el motor.
```

**Material visual complementario** (opcional, PDF/PNG/JPG, hasta 3 de 10 MB): subir los archivos de `adjuntos/`:

- `Yupana-Labs_NEG-01_presentacion.pdf`
- `Yupana-Labs_NEG-01_ficha.pdf`
- `Yupana-Labs_NEG-01_flujo.png`

**Enlace complementario** (opcional): dejar vacío

## Paso 3 · Impacto esperado

**¿Qué impacto generaría su solución y cómo contribuiría al resultado esperado del desafío?** (obligatoria) — 1522/2000

```text
Para el cliente: cuotas que caben en su utilidad en cada etapa. Para la Caja: un plan sustentado ante el comité con riesgos cuantificados antes del desembolso, y apoyo a la retención de clientes estacionales.

KPI del prototipo: periodos en que la cuota supera la capacidad, plan adaptado frente a cuota fija, en escenario base y adversos. Secundarios: costo y TCEA, ajuste al ciclo, concentración de capital e ingreso de la Caja. No medimos mora, como indicó el owner; la retención se mediría en un piloto, con línea base por confirmar.

Ejemplo ilustrativo (cálculo propio con las reglas del owner y utilidades supuestas; no es una medición): un productor pide S/ 8,000 a 12 meses (TEA 40 %; utilidad entre S/ 400 y S/ 4,200, promedio S/ 1,304). Con el promedio califica para cuota fija de S/ 801, pero esa cuota supera su utilidad en 8 de 12 meses. Seguir el ciclo al tope, sin holgura, corrige el año normal, pero un mes de retraso en la cosecha le deja S/ 1,940 sin cubrir. Con nuestras reglas caben S/ 5,895 a 12 meses, o S/ 8,000 a 17 meses, sin meses en déficit en los escenarios definidos; es así por construcción, y por eso el banco de pruebas evaluará contra un ciclo verdadero que el modelo no ve.

El costo se muestra: a 17 meses el interés es S/ 2,106, más que la cuota fija a 12 (S/ 1,572) y menos que una cuota fija a 17 (S/ 2,231), que aún deja 8 meses en déficit. Con la tasa que la SBS publica para Caja Trujillo en microempresa a 181-360 días (55,10 %, octubre 2026), el plazo necesario sería 18 meses.
```

## Paso 4 · Enfoque tecnológico

**¿Cuál será el enfoque tecnológico de su solución?** (obligatoria) — 1264/2000

```text
Python, FastAPI, Pydantic, pandas, statsmodels, scikit-learn, SciPy, SQLite, React y pytest.

Arquitectura de punta a punta: series y calendarios públicos → patrón estacional por actividad y zona → ajuste al cliente por agregación parcial → utilidad neta por etapa con banda y escenarios → programa de optimización (SciPy y HiGHS) → cronograma con las reglas del owner → motivos por restricción activa → comparación con cuota fija → API → interfaz del asesor y hoja para comité.

Por qué es adecuado: el cálculo financiero es determinista y se prueba contra casos hechos a mano; el problema de optimización es pequeño y se resuelve en milisegundos; las restricciones del producto se cumplen por construcción y se pueden auditar. Antes de calcular se valida la entrada (tasa máxima, seguros según el producto).

Un modelo de lenguaje intercambiable (nube, local o plantillas sin red) solo redacta el resumen para comité y, si hay tiempo, ordena las notas de campo; una verificación en código impide que introduzca cifras. Se usa solo en la demo, con datos sintéticos y sin conexión a sistemas de la Caja.

Fuentes públicas: BCRP, INEI, MIDAGRI, INIA, SENAMHI, ENFEN y calendarios comerciales. No se usa historial de pagos para estimar el ciclo, ni datos personales.
```

- **Punto de partida:** Desarrollo desde cero

**¿Identifican alguna limitación o riesgo técnico relevante para el desarrollo de su solución?** (opcional) — 518/800

```text
1) Información pública con poca granularidad por zona: calendarios y ajuste del asesor, con banda visible. 2) Ciclo optimista: holgura frente a escenarios adversos y factor menor a criterio del asesor. 3) Plan sin solución: diagnóstico de la restricción, nunca un plan que incumple. 4) Evaluación circular: se evalúa contra un ciclo verdadero que el modelo no ve. 5) Tiempo (31 de 32 horas-persona): si falta, se recortan notas de campo, resumen con modelo de lenguaje, sensibilidad a El Niño y escenarios adicionales.
```

## Paso 5 · Alcance del prototipo

**¿Qué nuevos desarrollos o adaptaciones realizarán durante el hackathon?** (obligatoria) — 1279/2000

```text
Funcionalidad crítica: del negocio al plan de pagos explicado, en una pantalla del asesor.

Desarrollos nuevos en las jornadas presenciales: patrones por sector y zona, modelo del ciclo con banda, cronograma con las reglas del owner, motor de optimización y diagnóstico, prueba de estrés, explicación por cuota, API, interfaz, perfiles sintéticos y banco de pruebas.

Criterios de aceptación verificados con pruebas: el cronograma reproduce las reglas del owner; ninguna cuota supera el factor de trabajo de su etapa ni la utilidad de los escenarios adversos en ningún año del plazo, ni amortiza más del 25 % del capital; cinco casos calculados a mano son las primeras pruebas; con un ciclo plano todas las cuotas salen iguales y con uno estacional las cuotas altas caen en las cimas; si no hay plan posible se nombra la restricción; toda cifra del resumen coincide con el cálculo; misma entrada, mismo resultado.

Núcleo que no se recorta (26 horas-persona): ciclo con banda, motor, explicación por cuota, comparación con cuota fija y pruebas. Si falta tiempo se recortan, en este orden: redacción con modelo de lenguaje, sensibilidad a El Niño estimada (queda un escenario del asesor), vistas separadas para cliente y Riesgos (queda una hoja) y seguros multirriesgo y vivienda.
```

**¿Qué resultado funcional esperan demostrar al finalizar el hackathon?** (obligatoria) — 686/1500

```text
Caso de uso: dos negocios ficticios de La Libertad, un productor agrícola y un taller de calzado, piden el mismo monto.
1) El sistema muestra que sus ciclos son distintos.
2) Propone dos planes distintos, con el porqué de cada cuota y la relación Cuota/UN por etapa.
3) El asesor baja el factor o corrige una fecha y el plan se recalcula.
4) Se compara con la cuota fija en un año normal y en un escenario adverso, incluido el costo.
5) Se cierra con el banco de pruebas sobre perfiles sintéticos (periodos en tensión, costo y ajuste al ciclo, adaptado frente a fijo) y la hoja para comité.

Verificación: pruebas automáticas y reporte de validación, sin conexión a sistemas de la Caja.
```

**¿Qué funcionalidades o capacidades quedarán fuera del alcance del prototipo?** (opcional) — 155/800

```text
Integración con el sistema central; reprogramaciones y refinanciaciones; créditos vigentes; aprobación automática; app móvil nativa; y uso de datos reales.
```

## Paso 6 · Datos e insumos

- **Tipo de requerimiento:** No requerimos datos ni insumos

## Antes de enviar: tres declaraciones que marca la persona

- [ ] La propuesta fue **revisada y acordada por los integrantes del equipo**, la información es veraz y cumple las bases. (Para marcarla, Glem, Antonio y David deben haberla visto.)
- [ ] Identificamos las soluciones y componentes preexistentes, su titularidad y condiciones de uso.
- [ ] Entendemos que, de ser seleccionados, haremos un desarrollo nuevo o adaptación sustantiva y demostraremos la funcionalidad crítica.

**Guardar y salir** conserva un borrador; enviar es definitivo hasta donde indique la plataforma.
