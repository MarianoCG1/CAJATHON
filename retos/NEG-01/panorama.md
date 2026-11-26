# Panorama de abastecimiento — NEG-01 · Plan de pagos adaptado al ciclo económico del negocio

> Documento de trabajo del equipo (25.11.2026), escrito sobre el expediente actualizado el 25.11 (19:02), sus 10 preguntas frecuentes y la respuesta a nuestro ticket del 24.11. Material confidencial: repo privado. Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene del expediente oficial.
> Alcance: qué necesita el desafío, cómo abastecerlo con datos sintéticos y públicos, cómo se construye en el evento y cómo se mide. **Aquí no hay modelo, motor, API, interfaz ni evaluación construidos**: eso se hace en la fase presencial (03–04.12). Las fórmulas de abajo son especificación, no código.

## Alcance MVP en una página

**Qué es:** una herramienta para el Asesor de Negocios que estima el ciclo económico del cliente, construye el plan de pagos óptimo que respeta la capacidad de pago en cada etapa, explica cada cuota y lo compara con la cuota fija en escenarios base y adversos; más un banco de pruebas sobre una cartera sintética.

**Entra (núcleo, no recortable)**

1. Perfiles sintéticos de negocios con ciclo «verdadero» conocido y lo que el asesor observaría de ellos.
2. Patrones sector × zona e índice de volatilidad; modelo del ciclo con ajuste al cliente y banda de incertidumbre.
3. Cronograma con las reglas del owner (TED base 360 por días exactos, seguros por interés simple, prelación y pendientes).
4. Motor de optimización: menor costo total sujeto a Cuota/UN ≤ factor por etapa y a los topes del producto; diagnóstico si no hay solución.
5. Explicación por cuota a partir de la etapa, la UN y la restricción activa.
6. Comparación con la cuota fija equivalente en escenario base y al menos uno adverso.
7. API e interfaz mínima: ciclo → plan → comparación → hoja para comité.
8. Banco de pruebas sobre la cartera sintética y pruebas automáticas; `docs/validacion.md`.

**Entra si hay tiempo (en orden de recorte):** asistente que estructura notas de campo con LLM; resumen para comité redactado por LLM (si no, plantilla); varios escenarios adversos; plan «oráculo» (con el ciclo verdadero) como cota; pulido visual.

**Queda fuera:** integración con el core, reprogramaciones y refinanciaciones, aprobación automática, autenticación y multiusuario, app móvil nativa, mapas.

**Criterio de terminado**

- Desde un repo limpio, un comando carga los datos y levanta la demo, sin red y sin claves.
- `pytest` en verde, incluidos los casos de cálculo hechos a mano y las propiedades del motor.
- El banco de pruebas reproduce las mismas cifras con la semilla fija y `docs/validacion.md` las contiene con fecha y commit.
- Se recorre en la interfaz, con datos del sistema y no escritos a mano: cliente → ciclo → plan → ajuste del asesor → comparación → hoja de comité.

**Guion de demo de 5 minutos (supuesto; los números se llenan con lo medido)**

| Tiempo | Qué se muestra |
|---|---|
| 0:00–0:40 | El problema: dos clientes piden el mismo monto; con cuota fija, uno se ahoga en febrero y el otro en agosto |
| 0:40–1:40 | Ciclo estimado de cada uno: patrón del sector y la zona, ajuste con lo observado en campo, banda de incertidumbre |
| 1:40–2:50 | Plan propuesto: cuotas altas en las cimas, bajas en los valles, Cuota/UN por etapa bajo el factor, motivo de cada cuota |
| 2:50–3:40 | El asesor baja el factor y corrige una fecha de cosecha; el plan se recalcula |
| 3:40–4:30 | Escenario El Niño: periodos en tensión, costo y TCEA, plan adaptado frente a cuota fija |
| 4:30–5:00 | Banco de pruebas sobre la cartera sintética y hoja para comité |

## 0. Resumen

- **Problema:** el core solo genera cuotas fijas sobre un ingreso promedio; los negocios estacionales se quedan sin liquidez en los valles, aunque sean viables.
- **Solución:** modelo del ciclo en dos capas (público + cliente) → programa lineal que arma el plan más barato que cabe en cada etapa → explicación y prueba de estrés frente a la cuota fija.
- **KPI del prototipo:** periodos en tensión (adaptado frente a fijo, base y adversos); secundarios: costo y TCEA, ajuste al ciclo, concentración. **KPI de negocio:** retención, en un piloto **[POR CONFIRMAR]**.
- **Lo que no hacemos:** medir mora (el owner lo descartó), usar historial de pagos de cartera, tocar créditos vigentes.

## (a) Qué necesita el desafío

### a.1 Datos e insumos (expediente, resumido)

El expediente lista flujos de ingresos, estacionalidad, historial de pagos, condiciones crediticias, tasas y plazos, políticas de riesgo y datos sintéticos, y aclara que son referenciales. El owner precisó que la Caja **no entregará datos** y que **el historial de pagos de una cartera no es buena fuente** para estimar el ciclo. Variables sugeridas: internas (ventas, costos, gastos operativos y tributarios, evidencias de transacciones, modelo de negocio, carga familiar) y externas (sector, zona, actividad principal de la zona, ciclo del sector, estacionalidad, clima, competencia, factores políticos, comunitarios y socioeconómicos). Fuentes públicas sugeridas: INEI, BCRP, MIDAGRI, SENAMHI, SUNAT, SBS, Cámara de Comercio y calendarios comerciales.

### a.2 Mapa necesidad → dónde se cubre

| Necesidad del expediente | Dónde se cubre |
|---|---|
| (A) Modelo predictivo del ciclo que combine sector, zona y cliente | §c.2 patrones + ajuste por agregación parcial + proyección con El Niño |
| (B) Motor que construya el plan bajo las restricciones del producto | §c.3 cronograma y §c.4 programa lineal |
| (C) Explicación de por qué cada cuota es alta o baja | §c.5 motivos por restricción activa |
| Resultado 3: presentar al comité ciclo, cuotas, Cuota/UN y supuestos | Interfaz: hoja para comité |
| Resultado 4: comparar con cuota fija en escenarios base y adversos | §c.6 prueba de estrés y §e |
| Adaptabilidad a rubros, zonas y productos | Catálogo de patrones y parámetros de producto configurables (§b) |
| Riesgos: ciclo optimista, concentración, encarecimiento, sobreendeudamiento, dependencia | §f |

### a.3 Componentes del producto (todos nuevos en el evento)

`domain/ciclo.py` (patrones y ajuste) · `domain/cronograma.py` (cálculo financiero) · `domain/motor.py` (optimización y diagnóstico) · `domain/estres.py` (escenarios y comparación) · `domain/explicacion.py` · `app/llm/provider.py` (intercambiable, con plantillas sin red) · `app/api.py` · `frontend/` · `scripts/evaluar_kpi.py`.

## (b) Cómo abastecerlo: datos sintéticos y públicos

### b.1 Capa pública: fuentes verificadas el 25.11.2026

| Fuente | Qué hay (verificado) | Uso | Estado |
|---|---|---|---|
| BCRPData, API pública | Producción agropecuaria nacional mensual por cultivo, en miles de toneladas: `PN01777AM` papa, `PN01778AM` arroz cáscara (y otros cultivos de la misma familia de códigos) | Estacionalidad por cultivo y sensibilidad a El Niño | ✅ La API respondió el 25.11 con datos a junio de 2025 |
| BCRP, Sucursal Trujillo | «Síntesis de actividad económica de La Libertad» y presentaciones mensuales (PDF): producción agropecuaria y de otros sectores por mes en la región | Patrón regional (La Libertad) | ✅ Publicadas mensualmente; se extraen de PDF |
| MIDAGRI (SIEA) | Boletín mensual «El Agro en Cifras» y evaluación mensual de la dinámica agropecuaria por región; calendario de cosecha de Agromercado (17 productos, dic. 2025): el arroz tiene cosecha casi continua en la costa norte irrigada | Calendarios de campaña por cultivo y región; intenciones de siembra | ✅ PDF; el detalle por provincia está por verificar en el portal del SIEA |
| INIA (MIDAGRI) | Calendario agrícola de la Región Costa: meses recomendados de siembra y cosecha por cultivo y departamento | Ubicar cimas y valles por cultivo y zona | ✅ PDF en el repositorio del INIA |
| NOAA CPC | Índice ONI (trimestres móviles) | Estado de El Niño y regresiones históricas | ✅ Descarga directa; último dato: **ASO 2026 = +2,46** (descargado el 25.11.2026) |
| IGP / ENFEN | ICEN (Niño 1+2, El Niño costero) y comunicados oficiales del ENFEN | Estado y pronóstico de El Niño costero, que pesa más en la costa norte | ⚠️ La ruta antigua `met.igp.gob.pe/datos/icen.txt` ya no existe (404); se toma de los informes del IGP y los comunicados del ENFEN |
| SENAMHI | Pronóstico estacional (por ejemplo, señaló al valle de Jequetepeque como favorable para iniciar la campaña arrocera 2025-2026 en octubre) | Ajustar el inicio de campaña del año del crédito | ✅ Boletines PDF |
| Calendarios comerciales | Campaña escolar, Día de la Madre, Fiestas Patrias, Navidad, temporada de verano | Picos de comercio y servicios | Conocimiento público |

Procesamiento: descomposición estacional (STL o X-13) de cada serie para obtener el factor por mes y su volatilidad; para cultivos, factores derivados del calendario de cosecha por zona. Resultado: una tabla `patron(actividad, zona, mes) → factor, σ`. **Limitación honesta:** la información pública mensual llega a nivel de región y de cultivo; el detalle por provincia o valle sale de los calendarios de INIA y MIDAGRI y del ajuste del asesor, no de una serie mensual por provincia.

### b.2 Capa sintética: perfiles de negocio con verdad conocida

Para evaluar sin datos de la Caja hace falta saber el ciclo **verdadero** de cada negocio y separar lo que el asesor observaría. Especificación **(todas las distribuciones: supuesto plausible, configurable)**:

| Elemento | Especificación |
|---|---|
| Cartera | ~2,000 perfiles, semilla fija |
| Rubros y zonas (La Libertad) | Agrícola: arroz (Jequetepeque/Pacasmayo), caña (Chicama), papa (sierra: Otuzco, Sánchez Carrión), hortalizas · Manufactura: calzado (El Porvenir) · Comercio: bodega y abarrotes (Trujillo, La Esperanza) · Servicios: restaurante de playa (Huanchaco), transporte · Pecuario: crianza de aves |
| Ciclo verdadero | Patrón del rubro y zona × desviación propia (corrimiento de fase de ±1 mes, amplitud ×0,6–1,4) × ruido mensual; algunos perfiles con periodicidad no mensual (una o dos campañas por año) |
| Estructura de la UN | UN = ventas × margen − gastos operativos fijos − gasto financiero de otras deudas − carga familiar. Los costos fijos y la carga familiar no siguen a las ventas, así que la UN es más volátil que las ventas (apalancamiento operativo) |
| Lo que ve el asesor | Ventas en meses buenos, regulares y malos con error de declaración; para una parte de los perfiles, 6–12 meses de evidencias de transacciones; fechas de campaña declaradas |
| Operación | Monto S/ 3,000–60,000; plazo 6–24 meses; TEA editable (por debajo de la tasa máxima del BCRP); desgravamen opcional; multirriesgo opcional sobre valor asegurable |
| Producto | Factor Cuota/UN por producto: 0,65 (inclusión) y 0,85 (Pequeña Empresa), los ejemplos ilustrativos del owner; cuota mínima, plazo máximo y topes **[POR CONFIRMAR]**, configurables |
| Escenarios adversos | Caída de ventas (−20 %), campaña retrasada (1–2 meses), El Niño (choque por rubro según sensibilidad) |

### b.3 Semilla y reproducibilidad

Todo con semilla fija; los escenarios adversos se definen antes de correr la evaluación y no se ajustan después.

## (c) Arquitectura y especificación

### c.1 Flujo

```
Datos del cliente + operación
        │
        ▼
Patrón sector × zona ──► Ajuste al cliente ──► UN por etapa (base, banda, adversos)
                                                     │
                                                     ▼
                         Motor (programa lineal) ──► Plan: monto y periodo por cuota
                                                     │
                       ┌─────────────────────────────┼──────────────────────────┐
                       ▼                             ▼                          ▼
             Motivo de cada cuota        Prueba de estrés vs. cuota fija   Hoja para comité
```

### c.2 Modelo del ciclo

- Factor del sector y la zona por mes: `s_sz(m)`, con volatilidad `σ_sz(m)`.
- Factor observado del cliente: `s_c(m)`, a partir de las ventas declaradas o evidenciadas.
- Ajuste por agregación parcial: `log ŝ(m) = w · log s_c(m) + (1 − w) · log s_sz(m)`, con `w = n / (n + κ)`, donde `n` es la evidencia efectiva (pocos datos declarados: bajo; varios meses de transacciones: alto) y `κ` se calibra en el banco de pruebas.
- Ventas por mes: `V(m) = V̄ · ŝ(m)`; **UN por mes** según la estructura de §b.2; **UN por etapa** = suma de la UN de los días de cada periodo.
- Banda: cuantiles a partir de `σ_sz` y del error del ajuste; escenarios adversos según §b.2.
- **Proyección de los meses del crédito:** para cada sector se estima su sensibilidad a El Niño con la historia (anomalía de producción mensual frente al ONI/ICEN con rezagos de 0 a 6 meses, incluidos 2017 y 2023). Con el estado previsto (comunicado del ENFEN, ONI reciente, pronóstico del SENAMHI, intenciones de siembra) se ajustan los meses concretos del crédito y se asigna peso a los escenarios adversos. Si falta tiempo en el evento, el estado de El Niño lo fija el asesor como escenario y no se estima la sensibilidad.
- Etapas: tramos consecutivos de cima, transición y valle; definen las fechas candidatas de pago (la periodicidad sale del ciclo, no es necesariamente mensual).

### c.3 Cronograma (reglas del owner)

Para cada periodo `t` de `d_t` días, con saldo de capital `S_{t−1}`:

- `TED = (1 + TEA)^(1/360) − 1`
- Interés: `I_t = S_{t−1} · ((1 + TED)^(d_t) − 1)`
- Desgravamen (opcional): `D_t = S_{t−1} · tasa_desg · d_t / 360` **(tasa expresada anual: supuesto)**
- Multirriesgo o vivienda (opcional, excluyentes): `M_t = valor_asegurable · tasa_mr · d_t / 360`
- Aplicación de la cuota: primero seguros pendientes y del periodo, luego interés pendiente y del periodo, luego capital. Lo no cubierto queda pendiente en su concepto: suma a la deuda, no al saldo de capital.
- TCEA: tasa interna de retorno de los flujos (desembolso y cuotas con seguros), anualizada.

### c.4 Motor: programa de optimización

Variables por periodo `t`: `k_t ≥ 0` (capital amortizado), `q_t ≥ 0` (pago de seguros e interés, del periodo y pendientes), `P_t ≥ 0` (seguros e interés pendientes al cierre) y una binaria `z_t` (1 si el periodo amortiza capital).

- Saldo de capital: `S_t = Monto − Σ_{j≤t} k_j`. Interés y desgravamen del periodo (`I_t`, `D_t`) son lineales en `S_{t−1}`; el multirriesgo `M_t` es constante.
- Pendientes: `P_t = P_{t−1} + I_t + D_t + M_t − q_t`. Lo pendiente **no genera interés** y **no suma al saldo de capital** (regla del owner).
- Prelación: solo se amortiza capital si no quedan pendientes: `k_t ≤ Monto · z_t` y `P_t ≤ Grande · (1 − z_t)`.
- Cuota: `C_t = q_t + k_t`.
- **Capacidad (regla del producto):** `C_t ≤ f · UN_t^esperada`, con `f = factor del asesor ≤ factor del producto`.
- **Holgura (regla robusta, supuesto configurable):** `C_t ≤ UN_t^s` para cada escenario adverso `s` configurado. El ejemplo de §j muestra por qué: sin ella, un mes de retraso en la cosecha devuelve el déficit.
- Producto: `Σ_t k_t = Monto`, `P_n = 0`, `C_t ≥ cuota mínima` **[POR CONFIRMAR]**, `k_t ≤ c · Monto` (concentración, `c` = 35 % **(supuesto)**), y como máximo `g` periodos consecutivos y `G` en total con `z_t = 0` **(supuesto)**.
- **Objetivo:** menor costo total `Σ (I_t + D_t + M_t)`. Como el interés corre sobre el saldo, minimizar el costo equivale a amortizar lo antes posible dentro de la capacidad, que lleva el capital a las cimas como pide el owner.
- **Sin solución:** el motor relaja una restricción a la vez para identificar cuál impide el plan, y calcula dos salidas: el **monto máximo** que cabe en el plazo pedido (búsqueda sobre el monto) y el **plazo mínimo** que necesita el monto pedido (búsqueda sobre el plazo). En el ejemplo de §j: S/ 6,888 a 12 meses o S/ 8,000 a 16 meses.
- Tamaño: decenas de variables continuas y una binaria por periodo (12 a 36); HiGHS (`scipy.optimize.milp`) lo resuelve en milisegundos.

### c.5 Explicación por cuota

Para cada cuota se guardan la etapa, la UN esperada, la Cuota/UN y la **restricción activa** (capacidad, concentración, cuota mínima, holgura de estrés o ninguna). Con eso, una plantilla en código produce el motivo («alta: cosecha, la capacidad permite amortizar S/ X»; «baja: valle; cubre seguros e intereses y S/ Y de capital»). El LLM opcional solo reescribe el resumen para comité, y una verificación en código compara cada número del texto con el cálculo.

### c.6 Prueba de estrés y comparación

Plan adaptado y cuota fija equivalente (mismo monto, TEA, seguros y plazo; cuota fija calculada con el mismo motor de cronograma) se evalúan contra la UN del escenario base y de cada escenario adverso, aplicando la prelación y los pendientes. Métricas en §e.3.

### c.7 Endpoints (diseño)

`POST /ciclo` (cliente → UN por etapa y banda) · `POST /plan` (ciclo + operación + producto → plan, motivos, restricciones activas o diagnóstico) · `POST /comparar` (plan → métricas base y adversos frente a cuota fija) · `GET /hoja/{id}` (hoja para comité).

## (d) Plan hora a hora del evento (4 personas, ~8 h netas por persona)

| Bloque | Antonio | Glem | Mariano | David |
|---|---|---|---|---|
| Día 1, 10:30–13:00 | Reglas de producto y casos de cálculo hechos a mano (pruebas del cronograma) | Perfiles sintéticos y patrones sector × zona | Cronograma con reglas del owner | Flujo del asesor y del comité; maqueta de pantallas |
| Día 1, 14:00–16:30 | Prueba de estrés y métricas | Ajuste al cliente y banda | Motor de optimización y diagnóstico | Interfaz: ciclo y plan |
| Día 1, 16:30–17:30 | Pruebas | Pruebas | Pruebas e integración | Pruebas de interfaz |
| Día 2, 09:30–12:00 | Banco de pruebas y `docs/validacion.md` | Calibración de `κ` y escenarios | API, explicación y LLM opcional | Comparación y hoja para comité |
| Día 2, 12:00–12:45 | Validación final y números del pitch | Validación final | Validación final | Ensayo de demo |

Horas por tarea: ver Anexo A de `concepto.md` (31 h, núcleo 26 h). **Escenario pesimista (supuesto):** si el motor y la integración se desvían un 50 %, se recorta en el orden de `concepto.md` §8 y se mantiene el núcleo.

## (e) Diseño de la evaluación (banco de pruebas)

### e.1 Unidad y población

Cada perfil sintético con su operación. Población: la cartera de §b.2 completa, reportada también por rubro, zona y producto (adaptabilidad).

### e.2 Planes comparados

1. **Cuota fija equivalente** (lo que hace hoy el core).
2. **Plan adaptado** con el ciclo **estimado** (lo que haría el asesor con la herramienta).
3. **Plan oráculo** con el ciclo **verdadero** (opcional): cota superior; la distancia entre 2 y 3 mide el costo del error de estimación.

### e.3 Métricas

| Métrica | Qué mide |
|---|---|
| Periodos en tensión (Cuota/UN > factor) y en déficit (cuota > UN) | Capacidad de pago, base y adversos (KPI principal) |
| Pendientes acumulados | Cuánto queda sin pagar en el escenario adverso |
| Interés + seguros totales y TCEA | Encarecimiento para el cliente |
| Proporción de capital en las dos cuotas más altas; periodos sin amortizar | Concentración |
| Correlación cuota–UN por etapa; error del ciclo estimado frente al verdadero | Ajuste al ciclo y precisión del modelo |
| Ingreso financiero y saldo promedio expuesto | Efecto para la Caja |

### e.4 Cómo se obtiene el «con y sin» sin inventar el efecto

Los planes se construyen con lo que el asesor observaría, pero se evalúan contra el ciclo **verdadero** del perfil y contra los escenarios adversos fijados de antemano. No se simula comportamiento de pago ni mora (el owner lo descartó): se mide si la cuota cabe en la utilidad del negocio, que es lo que pide el reto.

## (f) Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Ciclo optimista | Restricción sobre la UN esperada de cada etapa (no un promedio); holgura de estrés; factor del asesor ≤ factor del producto; banda visible |
| Concentración de capital | Tope por cuota y mínimo de cuotas que amortizan |
| Encarecimiento | Objetivo de menor costo; tope de periodos sin amortizar; TCEA frente a cuota fija siempre visible |
| Sobreendeudamiento | UN neta de otras deudas y carga familiar; límites del producto configurables |
| Dependencia del modelo | Motivos generados por reglas; todo editable; el asesor decide y el comité aprueba |
| Patrones públicos con poca granularidad | Calendarios de cosecha por zona y ajuste del asesor; la banda refleja la incertidumbre |
| Plan infactible | Diagnóstico de la restricción que lo impide y sugerencia; nunca un plan que incumple |
| Tiempo de interfaz | Vista mínima primero; LLM y pulido al final |

## (g) Preguntas para el owner (abiertas; los tickets cerraron el 24.11)

1. Factores, cuota mínima, plazo máximo y topes de sobreendeudamiento por producto para la demo (supuesto: ejemplos ilustrativos, configurables).
2. ¿Hay una regla de holgura frente a escenarios adversos? (supuesto: cuota cubierta por la UN adversa).
3. ¿Hay topes de concentración de capital o de periodos de gracia? (supuesto: configurables).
4. Línea base de retención y forma de medirla en un piloto.

## (h) Preexistente vs. nuevo en el evento

| Componente | Estado |
|---|---|
| Este documento, el concepto y la postulación | Texto previo (permitido) |
| Generador de perfiles sintéticos | **Decisión pendiente**: si se construye antes del 03.12, se declara en `docs/preexistente.md` con sus pruebas |
| Patrones sector × zona, modelo del ciclo, cronograma, motor, estrés, explicación, API, interfaz, banco de pruebas | **Nuevo, en el evento** |

## (i) Plan de pruebas (en el evento)

- Cronograma: casos hechos a mano por Antonio (TED, días exactos, seguros, prelación, pendientes) con tolerancia de céntimos.
- Motor: con ciclo plano reproduce la cuota fija; con ciclo estacional, las cuotas altas caen en las cimas; nunca viola Cuota/UN ≤ factor ni la holgura frente a los escenarios adversos; respeta concentración y gracia; en un valle sin capacidad deja pendientes sin interés y no amortiza capital hasta saldarlos; caso infactible devuelve diagnóstico con monto máximo y plazo mínimo.
- Ejemplo de §j como prueba de regresión: cuota fija S/ 801; S/ 8,000 a 12 meses inviable con holgura; salidas S/ 6,888 a 12 meses y 16 meses de plazo (con tolerancia de céntimos).
- Ciclo: sin evidencia propia devuelve el patrón del sector; con evidencia fuerte se acerca al dato del cliente.
- Explicación: toda cifra del resumen coincide con el motor.
- Banco de pruebas: misma semilla, mismas cifras.

## (j) Ejemplo ilustrativo calculado (25.11.2026)

Cálculo hecho a mano con las reglas del owner, apoyado en un script de un solo uso que no forma parte del producto ni del repo. **No es una medición ni la salida del motor**: sirve para mostrar el problema y validar el diseño. Se reproducirá como prueba automática en el evento.

**Caso:** pequeño productor de arroz del valle de Jequetepeque; S/ 8,000 a 12 meses; TEA 40 %; desgravamen 0,96 % anual sobre saldo; desembolso 15.01.2027; cuotas el día 15; factor 0,65. Todo **(supuesto)**.

**UN mensual (S/; ilustrativa, calendario por verificar con INIA):**

| ene | feb | mar | abr | may | jun | jul | ago | set | oct | nov | dic |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 450 | 400 | 500 | 2,800 | 4,200 | 3,200 | 900 | 700 | 650 | 700 | 600 | 550 |

Escenarios: **El Niño** (abril cae a S/ 650 y la cosecha llega un mes tarde con −30 %: may 1,960, jun 2,940, jul 2,240) y **caída general** (−20 % en todos los meses).

| Plan | Cuotas (S/) | Cuota > UN (base / El Niño / caída) | Déficit acumulado S/ (base / El Niño / caída) | Interés S/ | Capital en las 2 cuotas mayores |
|---|---|---|---|---|---|
| Cuota fija, 12 m | 801 × 12 | 8 / 9 / 9 | 1,861 / 2,012 / 2,852 | 1,572 | 19 % |
| Adaptado literal, 12 m | 292, 260, 325, 1,820, 2,730, 2,080, 585, 455, 422, 373, 0, 0 | 0 / 2 / 0 | 0 / 1,940 / 0 | 1,306 | 56 % |
| Adaptado robusto, S/ 8,000 a 12 m | no cabe: queda un saldo de S/ 1,937 al final | — | — | — | — |
| Adaptado robusto, **S/ 6,888 a 12 m** | 292, 260, 325, 650, 1,960, 2,080, 585, 455, 422, 455, 390, 358 | 0 / 0 / 0 | 0 / 0 / 0 | — | — |
| Adaptado robusto, **S/ 8,000 a 16 m** | 292, 260, 325, 650, 1,960, 2,080, 585, 455, 422, 455, 390, 357, 292, 260, 325, 845 | 0 / 0 / 0 | 0 / 0 / 0 | — | — |
| Cuota fija, S/ 8,000 a 16 m | 635 × 16 | 8 de 16 en base | 1,228 en base | — | — |

TCEA de la cuota fija y del plan literal: 41,3 % en ambos (misma TEA). En el plan de 16 meses, el segundo año se evaluó con la UN base.

**Conclusiones para el diseño:** (1) con la UN promedio, el cliente «califica» con cuota fija (801 ≤ 0,65 × 1,304 = 848), pero la cuota supera la utilidad en 8 de 12 meses; (2) la regla literal sin holgura es frágil ante un retraso de campaña y concentra capital; (3) la regla robusta elimina el déficit en los tres escenarios, pero exige ajustar monto o plazo, y el motor debe proponer ambas salidas; (4) menos interés para el cliente es menos ingreso para la Caja, y la herramienta lo muestra.

## (k) Entrada para `docs/preexistente.md`

Ninguna por ahora. Si se construye el generador de perfiles antes del evento, se añade aquí y en `docs/preexistente.md` con fecha, titularidad (el equipo) y número de pruebas.

## Cotejo con el expediente

Cotejado el 25.11.2026 contra la versión del expediente actualizada ese día (19:02), sus 10 preguntas frecuentes y el ticket del equipo (24.11). Revisado otra vez tras la profundización del mismo día: la prelación y los pendientes del owner ahora están en la formulación del motor (§c.4), no solo en el cronograma.

### Desviaciones encontradas en el borrador v0 y corrección

| v0 decía | Expediente / owner | Corrección en v1 |
|---|---|---|
| «Flujo de ingresos estacional» | Pide estimar el **ciclo económico** y la UN por etapa; la periodicidad puede no ser mensual | El modelo estima la UN por etapa y las etapas definen los periodos |
| «Cronograma de cuotas ajustado» | No es redistribuir un cronograma fijo: **cada cuota con monto y periodo propios**, construido desde el ciclo | Motor que construye el plan desde cero con periodos por etapa |
| Validar «rentabilidad» | Respetar **Cuota/UN ≤ factor en cada etapa**, TEA única, cuota mínima, plazo, sobreendeudamiento | Restricciones explícitas del programa lineal |
| KPI de cumplimiento e incumplimiento (mora) por backtest | **No se medirá mora**; funciona si el plan se correlaciona con el ciclo y se cuantifican beneficios y riesgos; el negocio mira la **retención** | KPI de periodos en tensión, costo, ajuste y concentración; retención como KPI de piloto |
| Datos de «pagos» en el generador | El historial de pagos **no es buena fuente** para el ciclo; la Caja no entrega datos | Perfiles sintéticos con ciclo verdadero y fuentes públicas; sin historial de pagos |
| Agente genérico que explica | Mínimo exigido: (A) modelo del ciclo, (B) motor, (C) **por qué cada cuota es alta o baja** | Motivos por restricción activa; LLM solo redacta y se verifica |
| Sin reglas de cálculo | TED base 360 por días exactos, seguros por interés simple, prelación seguros → interés → capital y pendientes | Especificadas en §c.3 y en las pruebas |
| Sin escenarios | Comparar con cuota fija en escenarios **base y adversos** (caída de ventas, campaña retrasada, El Niño) | §c.6 y §e |

### Lo que sí coincide

Usuario principal (Asesor de Negocios; valida Riesgos; aprueba el comité), principio de decisión humana, prototipo sin conexión a la Caja, datos sintéticos, LLM externo solo para la demo.

### Lo que decimos y el expediente no dice (todo marcado como supuesto)

Nombre «Ritmo»; agregación parcial como método de ajuste; proyección con la sensibilidad a El Niño; programa de optimización con objetivo de menor costo y binarias de prelación; tope de concentración del 35 %; regla de holgura robusta frente a escenarios adversos; los datos del ejemplo de §j; topes de gracia; rubros, zonas y distribuciones de la cartera sintética; −20 % como caída de ventas; asistente de notas de campo.

### Observación

El expediente incluye «historial de pagos» entre los datos e insumos referenciales, pero el owner aclaró que no es buena fuente para el ciclo. No lo usamos para estimar el ciclo; si la Caja lo entregara en una implementación, serviría solo para monitorear el plan, no para construirlo.
