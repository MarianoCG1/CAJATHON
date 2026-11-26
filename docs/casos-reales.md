# Casos reales comparables y qué tan simples son nuestros datos (25.11, noche)

Responde a la observación de Glem: **los datos sintéticos de RIE-03 son muy simples.** Tiene razón.

## 1. Por qué son simples

En `retos/RIE-03/datos/generar.py`:

- Cada cliente cae en una de cinco trayectorias fijas; el deterioro es una rampa lineal del ingreso.
- Casi todas las señales (abonos, cobros, saldo, consultas, deuda) salen del **mismo** número oculto. El modelo encuentra lo que nosotros pusimos.
- No hay choques que afecten a un grupo a la vez (clima, campaña, obra en la calle), ni dinero que se mueve a otra entidad, ni deuda informal, ni señales que suben por buenas razones (un negocio que pide crédito porque crece).

**Consecuencia:** el AUC de 0,84 describe nuestro generador, no la realidad. Sirve para probar que el flujo funciona, no para anticipar el desempeño en la Caja.

## 2. Caso real más cercano: microcrédito en Huancayo

Arriola León y Ghodrat (2026), *Journal of Business* 17(1), Universidad del Pacífico ([ficha y PDF](https://doi.org/10.21678/jb.2026.2798)). Leídas las secciones de método y resultados.

| | El estudio | Nuestro concepto RIE-03 |
|---|---|---|
| Datos | Unos 50 000 microcréditos reales, una microfinanciera, 2019–2021 | Sintéticos |
| Variables | Del **otorgamiento**: monto, mes, cuotas, frecuencia, tipo, producto, calificación, aval | Comportamiento **mensual** hasta la fecha de corte |
| Qué predice | Atraso acumulado mayor al 25 % del plazo | Paso a más de 30 días en los próximos 60 |
| Casos positivos | 28,7 % | 0,7 % entre clientes al día |
| Mejor resultado | AUC 0,732; sensibilidad 61 %; precisión 49 % | AUC 0,84; precisión 4,7 % |
| Límite que reconocen | Una sola entidad; resultados moderados | Generador propio |

Las cifras **no son comparables** (otra definición, otra población y otra tasa base). Lo que sí enseña:

1. Con datos reales y solo variables de otorgamiento, la discriminación es **moderada** (0,73).
2. Ninguna de esas variables se mueve después del desembolso: no pueden avisar de un deterioro que empieza meses después. Ahí está el aporte que proponemos y que **todavía no está demostrado**.
3. La frecuencia de pago fue la variable que más pesó. Nuestro generador solo tiene cuotas mensuales: es un hueco concreto.

### Cómo aplicaríamos el concepto a ese caso

1. Partir de su cartera y añadir la historia de pagos cuota por cuota (días de atraso de cada una, pagos parciales). Con una sola entidad, eso es lo que seguro existe.
2. Redefinir la pregunta: de «¿se atrasará este crédito?» a «¿quién, estando al día hoy, empeora en los próximos 60 días?».
3. Usar su modelo de otorgamiento como **línea base** y medir cuánto suma el comportamiento mensual.
4. Pasar la salida por el filtro de señal y la aprobación del gestor.
5. Probar la intervención en un grupo y no en otro, porque ningún modelo dice si avisar sirve.

## 3. ¿Sirve avisar antes? Evidencia de campo

- **Uganda** (Cadena y Schoar, NBER w17020, 2011): un SMS mensual antes del pago subió la probabilidad de pagar a tiempo (el resumen indica de 7 a 9, sin precisar si son puntos o porcentaje) y redujo unos 2 días de atraso al mes; efecto comparable a una rebaja de 25 % del interés. Leído solo el resumen. [Fuente](https://www.nber.org/papers/w17020).
- **Filipinas** (Karlan, Morten y Zinman): en promedio los recordatorios **no** mejoraron el pago; sí cuando nombraban al oficial de crédito y en clientes recurrentes. Leído el resumen de búsqueda. [Fuente](https://behavioralpolicy.org/articles/a-personal-touch-in-text-messaging-can-improve-microloan-repayment/).

**Implicancia de diseño:** el efecto no está garantizado; el mensaje debe ir a nombre del gestor y hay que medirlo con grupo de comparación.

## 4. COM-01

No encontramos un caso peruano publicado con cifras de captación antes y después de usar analítica territorial. Referencias parciales en `retos/COM-01/panorama.md`.

## 5. Qué haríamos antes del evento

Enriquecer el generador de RIE-03 (declarado como preexistente) solo si RIE-03 es el desafío elegido: frecuencias de pago distintas, choques por zona y sector, señales con ruido independiente y falsos indicios. Se espera que las métricas **bajen**, y está bien.

Usar un conjunto público de datos reales anonimizados queda descartado mientras la regla del equipo sea «solo sintéticos o los que entregue la Caja».
