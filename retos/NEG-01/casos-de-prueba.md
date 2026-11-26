# NEG-01 — Cinco casos calculados a mano con su resultado esperado

> 26.11.2026. Responsable: Antonio. Cada caso se puede verificar en Excel con las fórmulas que trae. En el evento se convierten en pruebas automáticas, con una tolerancia de S/ 0.01 por cuota. Todos los datos son **ilustrativos (supuesto)**.
> Reglas del owner usadas: TEA → TED en base 360; interés por días exactos sobre el saldo de capital; seguros con interés simple por días en base 360; prelación seguros → interés → capital; lo no cubierto queda pendiente en su concepto, sin generar interés y sin sumar al saldo de capital.

## Datos comunes

- Desembolso el 15.01.2027 y cuotas el día 15 de cada mes. Días de los 12 periodos: 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31.
- UN mensual del arrocero (S/), de enero a diciembre: 450, 400, 500, 2,800, 4,200, 3,200, 900, 700, 650, 700, 600, 550. Promedio: S/ 1,304.17.
- Tope del producto: 0,65. Factor efectivo de Ritmo: 0,585 (90 % del tope). Capital por cuota: como máximo 25 % del monto.

---

## Caso 1 — Tasa diaria, interés y seguro de un periodo

**Entrada:** saldo S/ 8,000; TEA 40 %; periodo de 31 días; desgravamen 0,96 % anual sobre saldo.

**Cálculo:**
- TED = 1,40^(1/360) − 1 = **0,000935080** (0,093508 %)
- Factor del periodo = (1 + TED)^31 − 1 = **0,029398**
- Interés = 8,000 × 0,029398 = **S/ 235.18**
- Desgravamen = 8,000 × 0,0096 × 31 / 360 = **S/ 6.61**

**Excel:** `=(1+40%)^(1/360)-1` · `=8000*((1+B1)^31-1)` · `=8000*0.96%*31/360`

**Qué prueba:** la conversión de tasa y el uso de días exactos. Si alguien usa 30 días o una tasa mensual nominal, el resultado cambia.

## Caso 2 — Cuota fija de hoy y sus meses en déficit

**Entrada:** S/ 8,000 a 12 meses; TEA 40 %; desgravamen 0,96 % anual; días del calendario.

**Resultado esperado:**
- Cuota fija: **S/ 801.38** (incluye interés y desgravamen; se halla con «Buscar objetivo» de Excel para que el saldo final sea 0).
- Interés total: **S/ 1,572**; seguros: **S/ 44**; TCEA: **41,3 %**.
- Con la UN promedio, el cliente califica: 801.38 ≤ 0,65 × 1,304.17 = 847.71.
- Mes a mes, la cuota supera la UN en **8 de 12 meses** (todos salvo abril, mayo, junio y julio), con un **déficit acumulado de S/ 1,861**. Cuota/UN máxima: 2,00 en febrero.

**Qué prueba:** que el cálculo de la cuota fija coincide con lo que hace hoy el core, y que el problema del reto existe aunque el cliente «califique».

## Caso 3 — Valle profundo: pendientes y prelación

**Entrada:** saldo S/ 8,000; TEA 55,10 % (tasa publicada de Caja Trujillo para microempresa a cuota fija de 181 a 360 días, SBS, octubre 2026); desgravamen 0,105 % mensual (1,26 % anual); factor efectivo 0,585; tres meses de valle.

| Periodo | Días | UN | Capacidad (0,585 × UN) | Seguro | Interés | Paga seguro | Paga interés | Paga capital | Interés pendiente | Deuda total |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 31 | 450 | 263.25 | 8.68 | 308.14 | 8.68 | 254.57 | 0.00 | **53.57** | 8,053.57 |
| 2 | 28 | 400 | 234.00 | 7.84 | 277.81 | 7.84 | 226.16 | 0.00 | **105.22** | 8,105.22 |
| 3 | 31 | 500 | 292.50 | 8.68 | 308.14 | 8.68 | 283.82 | 0.00 | **129.54** | 8,129.54 |

En el periodo 2, los S/ 226.16 pagan primero los S/ 53.57 pendientes y luego S/ 172.59 del interés del periodo. El interés de cada periodo se calcula sobre los S/ 8,000 de capital, nunca sobre los pendientes.

**Resultado esperado:** la cuota nunca supera la capacidad; no se amortiza capital mientras haya pendientes; los pendientes no generan interés; la deuda total crece en S/ 129.54 en tres meses.

**Qué prueba:** la corrección del motor. Con tasas reales de microempresa, en los meses de valle el interés solo ya supera la capacidad, y el motor no debe declarar «sin solución» por eso. También muestra que desembolsar justo antes de un valle largo encarece el crédito, algo que la herramienta debe advertir.

## Caso 4 — Ciclo plano (control de cordura)

**Entrada:** UN constante de S/ 1,304.17 todos los meses (el mismo cliente, pero «promediado» como hoy); S/ 8,000; TEA 40 %; desgravamen 0,96 % anual; factor efectivo 0,585.

**Resultado esperado:**
- Capacidad por cuota = 0,585 × 1,304.17 = **S/ 762.84**; todas las cuotas iguales a ese valor.
- S/ 8,000 a 12 meses **no cabe**: quedan S/ 546.31 sin pagar.
- Salidas: monto máximo a 12 meses ≈ **S/ 7,616**, o S/ 8,000 en **13 meses** (12 cuotas de S/ 763 y una final de S/ 563).

**Qué prueba:** que con un ciclo plano el motor da cuotas iguales y respeta la holgura. Con el tope de 0,65 sin holgura, la cuota fija de S/ 801 cabría (≤ 847.71); con la holgura que pide el expediente, no cabe. Es la holgura actuando de forma visible.

## Caso 5 — El arrocero con Ritmo (caso de la demo)

**Entrada:** UN del arrocero; S/ 8,000; TEA 40 %; desgravamen 0,96 % anual. Escenarios adversos aplicados a todos los meses del crédito: El Niño (abril S/ 650; mayo 1,960; junio 2,940; julio 2,240) y caída general de −20 %. Regla de Ritmo: cuota ≤ mínimo entre 0,585 × UN base, UN El Niño y UN con caída; capital por cuota ≤ 25 % del monto.

**Resultado esperado:**
- S/ 8,000 a 12 meses **no cabe**: quedan **S/ 2,234.79** sin pagar. El motor no fuerza el plan.
- Salida A: **S/ 5,895 a 12 meses**. Cuotas: 263, 234, 292, 650, 1,629, 1,581, 526, 410, 380, 410, 351, 322. Interés S/ 1,121. Capital en las 2 cuotas mayores: 50 %.
- Salida B: **S/ 8,000 a 17 meses**. Cuotas: 263, 234, 292, 650, 1,960, 1,872, 526, 410, 380, 410, 351, 322, 263, 234, 292, 650, 1,055. Interés S/ 2,106. Capital en las 2 cuotas mayores: 43 %.
- En ambas salidas: **0 meses con cuota > UN** en los tres escenarios y Cuota/UN máxima de 0,585 en el escenario base.
- Comparación: la cuota fija de S/ 8,000 a 17 meses es S/ 606, con cuota > UN en 8, 8 y 11 meses y un déficit de S/ 994, 994 y 1,941 (base, El Niño, caída). Su interés total es S/ 2,231.

**Qué prueba:** el caso completo de la demo. La regla robusta y el diagnóstico dan monto máximo o plazo mínimo, y la comparación con la cuota fija.

---

## Sensibilidad con las tasas reales de Caja Trujillo

Con la TEA de 55,10 % y el desgravamen de 0,105 % mensual del caso 3, el caso 2 da una cuota fija de **S/ 846** con déficit en 8 de 12 meses (S/ 2,217). En el caso 5, S/ 8,000 a 12 meses sigue sin caber, y las salidas son **≈ S/ 5,500 a 12 meses** o **17 meses** de plazo. Las conclusiones no cambian. La cifra de 12 meses es aproximada, porque en los primeros meses entran en juego los pendientes del caso 3.
