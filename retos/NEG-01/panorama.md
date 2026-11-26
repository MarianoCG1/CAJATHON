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
| (A) Modelo predictivo del ciclo que combine sector, zona y cliente | §c.2 patrones + ajuste por agregación parcial |
| (B) Motor que construya el plan bajo las restricciones del producto | §c.3 cronograma y §c.4 programa lineal |
| (C) Explicación de por qué cada cuota es alta o baja | §c.5 motivos por restricción activa |
| Resultado 3: presentar al comité ciclo, cuotas, Cuota/UN y supuestos | Interfaz: hoja para comité |
| Resultado 4: comparar con cuota fija en escenarios base y adversos | §c.6 prueba de estrés y §e |
| Adaptabilidad a rubros, zonas y productos | Catálogo de patrones y parámetros de producto configurables (§b) |
| Riesgos: ciclo optimista, concentración, encarecimiento, sobreendeudamiento, dependencia | §f |

### a.3 Componentes del producto (todos nuevos en el evento)

`domain/ciclo.py` (patrones y ajuste) · `domain/cronograma.py` (cálculo financiero) · `domain/motor.py` (optimización y diagnóstico) · `domain/estres.py` (escenarios y comparación) · `domain/explicacion.py` · `app/llm/provider.py` (intercambiable, con plantillas sin red) · `app/api.py` · `frontend/` · `scripts/evaluar_kpi.py`.

## (b) Cómo abastecerlo: datos sintéticos y públicos

### b.1 Capa pública: patrones sector × zona **(supuesto de fuentes; a descargar y procesar en el evento o declarar como insumo previo)**

| Fuente | Qué aporta | Uso |
|---|---|---|
| BCRP (series regionales y nacionales de producción, síntesis de La Libertad) | Estacionalidad mensual por sector | Índice estacional por actividad |
| INEI (producción nacional por sector, mensual) | Estacionalidad de comercio, manufactura y servicios | Índice estacional |
| MIDAGRI (calendarios de siembra y cosecha por cultivo y región) | Meses de cosecha y venta por cultivo y zona | Ubicar cimas y valles agrícolas por zona |
| SENAMHI / ENFEN (anomalías y alertas de El Niño) | Episodios climáticos y su intensidad | Escenarios adversos por sensibilidad sectorial |
| Calendarios comerciales | Campaña escolar, Día de la Madre, Fiestas Patrias, Navidad, temporada de verano | Picos de comercio y servicios |

Procesamiento: descomposición estacional (STL o X-13) de cada serie para obtener el factor por mes y su volatilidad; para cultivos, factores derivados del calendario de cosecha por zona. Resultado: una tabla `patron(actividad, zona, mes) → factor, σ`.

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
- Etapas: tramos consecutivos de cima, transición y valle; definen las fechas candidatas de pago (la periodicidad sale del ciclo, no es necesariamente mensual).

### c.3 Cronograma (reglas del owner)

Para cada periodo `t` de `d_t` días, con saldo de capital `S_{t−1}`:

- `TED = (1 + TEA)^(1/360) − 1`
- Interés: `I_t = S_{t−1} · ((1 + TED)^(d_t) − 1)`
- Desgravamen (opcional): `D_t = S_{t−1} · tasa_desg · d_t / 360` **(tasa expresada anual: supuesto)**
- Multirriesgo o vivienda (opcional, excluyentes): `M_t = valor_asegurable · tasa_mr · d_t / 360`
- Aplicación de la cuota: primero seguros pendientes y del periodo, luego interés pendiente y del periodo, luego capital. Lo no cubierto queda pendiente en su concepto: suma a la deuda, no al saldo de capital.
- TCEA: tasa interna de retorno de los flujos (desembolso y cuotas con seguros), anualizada.

### c.4 Motor: programa lineal

Variables: `k_t ≥ 0`, capital amortizado en el periodo `t`. Como `S_{t−1} = Monto − Σ_{j<t} k_j`, el interés y el desgravamen son **lineales** en las `k`, y la cuota `C_t = D_t + M_t + I_t + k_t` también.

- **Objetivo:** minimizar `Σ_t (I_t + D_t)`, el costo total para el cliente. Equivale a amortizar lo antes posible, lo que lleva el capital a las cimas.
- **Restricciones:**
  - `Σ_t k_t = Monto`
  - `C_t ≤ f · UN_t` en cada etapa, con `f = factor del asesor ≤ factor del producto`
  - `C_t ≥ cuota mínima` del producto **[POR CONFIRMAR]**
  - `k_t ≤ c · Monto` (concentración; `c` = 35 % **(supuesto, configurable)**)
  - Periodos sin amortización: como máximo `g` consecutivos y `G` en total **(supuesto, configurable)**; si hace falta contar periodos, se usa la variante entera (`scipy.optimize.milp`, HiGHS)
  - Holgura de estrés: `C_t ≤ UN_t^adverso` **(regla del equipo: supuesto)**; si vuelve el problema infactible, se reporta y el asesor decide
- **Sin solución:** se relajan las restricciones una a una para identificar cuál impide el plan y se informa qué cambiar (monto, plazo, factor o fechas).
- Tamaño: decenas de variables por crédito; se resuelve en milisegundos.

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
- Motor: con ciclo plano reproduce la cuota fija; con ciclo estacional, las cuotas altas caen en las cimas; nunca viola Cuota/UN ≤ factor; respeta concentración y gracia; caso infactible devuelve diagnóstico.
- Ciclo: sin evidencia propia devuelve el patrón del sector; con evidencia fuerte se acerca al dato del cliente.
- Explicación: toda cifra del resumen coincide con el motor.
- Banco de pruebas: misma semilla, mismas cifras.

## (j) Entrada para `docs/preexistente.md`

Ninguna por ahora. Si se construye el generador de perfiles antes del evento, se añade aquí y en `docs/preexistente.md` con fecha, titularidad (el equipo) y número de pruebas.

## Cotejo con el expediente

Cotejado el 25.11.2026 contra la versión del expediente actualizada ese día (19:02), sus 10 preguntas frecuentes y el ticket del equipo (24.11).

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

Nombre «Ritmo»; agregación parcial como método de ajuste; programa lineal con objetivo de menor costo; tope de concentración del 35 %; regla de holgura con la UN adversa; topes de gracia; rubros, zonas y distribuciones de la cartera sintética; −20 % como caída de ventas; asistente de notas de campo.

### Observación

El expediente incluye «historial de pagos» entre los datos e insumos referenciales, pero el owner aclaró que no es buena fuente para el ciclo. No lo usamos para estimar el ciclo; si la Caja lo entregara en una implementación, serviría solo para monitorear el plan, no para construirlo.
