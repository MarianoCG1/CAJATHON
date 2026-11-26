# NEG-01: resumen para Mariano (26.11.2026)

**Estado:** listo para pegar en el formulario. El texto está en `retos/NEG-01/entrega/formulario-7-secciones.md`, con una versión corta (≤ 1,000 caracteres) y una completa por sección. El formulario cierra **hoy jueves 26.11 a las 11:59 p. m.**

## 1. Tus observaciones, corregidas

| Observación | Qué cambió |
|---|---|
| 17 meses, no 16 | El Niño ahora se aplica a **toda** la vida del crédito, no solo al primer año. Con eso, S/ 8,000 necesitan **17 meses** |
| Holgura bajo el tope | Factor efectivo **0,585**, que es el 90 % del tope de 0,65 (supuesto configurable). Además, la cuota tiene que caber en la utilidad de cada escenario adverso |
| Concentración de capital (lo detecté al corregir) | Como máximo **25 % del capital por cuota**, así que dos cuotas nunca pasan del 50 %. El monto máximo a 12 meses baja a **S/ 5,895** |
| Criterio del ciclo plano | Estaba mal. Ahora dice «con ciclo plano, todas las cuotas salen iguales» (caso 4) |

## 2. Cifras que sostienen la propuesta (ejemplo ilustrativo; no es una medición)

Arrocero de Jequetepeque, S/ 8,000, TEA 40 %, utilidad mensual entre S/ 400 y S/ 4,200 (promedio S/ 1,304).

- **Cuota fija de hoy:** S/ 801. Con el promedio «califica», pero la cuota supera la utilidad en **8 de 12 meses**, con un déficit acumulado de S/ 1,861.
- **Siguiendo el ciclo al tope, sin holgura:** si la cosecha se atrasa un mes, el déficit vuelve (S/ 1,940).
- **Ritmo:** S/ 8,000 a 12 meses no cabe. Propone **S/ 5,895 a 12 meses** o **S/ 8,000 a 17 meses**. Con cualquiera de las dos hay **0 meses en déficit** en año normal, con El Niño y con una caída de ventas de 20 %.
- **Con las tasas reales de Caja Trujillo** (55,10 % en microempresa a 181–360 días, SBS oct. 2026) las conclusiones se mantienen.
- **Cinco casos calculados a mano** en `casos-de-prueba.md`, verificables en Excel; en el evento serán las primeras pruebas automáticas. Cifras: TED 0,000935080; interés de 31 días S/ 235.18; cuota fija S/ 801.38; pendientes 53.57 → 105.22 → 129.54; saldo sin pagar a 12 meses S/ 2,234.79.

## 3. Auditoría de hoy: lo que faltaba mapear (ya está en el concepto y en el formulario)

Crucé todo contra el expediente, las 10 preguntas frecuentes y el ticket #0611. Estos puntos del expediente no estaban cubiertos o estaban mal redactados:

1. **Flujo completo de usuarios.** El ticket dice que el asesor **negocia y explica las condiciones al cliente** y que el **Asesor de Riesgos valida**. Teníamos solo la hoja para comité. Ahora hay tres salidas del mismo cálculo: **hoja para el cliente**, **vista de validación para Riesgos** y **hoja para comité**.
2. **Registro de ajustes del asesor.** Cada cambio (factor menor, corrección de una etapa, factor cualitativo como un paro o la competencia) queda guardado con su motivo. Responde al riesgo de «dependencia del modelo» y a los factores políticos, comunitarios y de competencia que pide el expediente.
3. **UN según tipo de cliente:** otras deudas, carga familiar en informales y EEFF auditados en jurídicas formales. En **ampliación**, la cuota vigente se descuenta de la UN de cada etapa.
4. **Seguros completos:** desgravamen, y multirriesgo o vivienda (excluyentes; vivienda obligatorio en hipotecario). Antes solo modelábamos el desgravamen.
5. **Validaciones de producto:** TEA ≤ tasa máxima del BCRP y seguros según producto, cada una con su prueba.
6. **Periodicidad no mensual:** periodos de 60 o 120 días, calculados por días exactos, con su criterio de aceptación.
7. **Gracia con sustento:** un periodo sin amortizar exige un motivo en el ciclo, igual que hoy en la Caja.
8. **Redacción:** el resumen y el §2 decían «Cuota/UN ≤ factor» y ahora hablan de holgura bajo el tope. El motor figuraba como «programa lineal»; ahora es programa entero mixto (`milp`), porque tiene binarias. Se añadió la fila de proyección con El Niño en el §4. El ejemplo de explicación por cuota usaba 0,65 y ahora usa las cifras corregidas.

Las versiones cortas siguen dentro del límite: resumen 407 caracteres (máximo 500); secciones entre 732 y 848 (máximo 1,000).

## 4. Lo menos defendible (respuestas en `preparacion.md` §2)

- El banco de pruebas usa datos que generamos nosotros. La afirmación es **comparativa**: misma cartera y mismos escenarios para la cuota fija y para Ritmo.
- La sensibilidad a El Niño usa series nacionales por cultivo. Es una aproximación, combinada con la síntesis regional del BCRP.
- A 12 meses la Caja cobra menos interés. Es porque amortiza antes y tiene menos saldo expuesto. El owner dijo que el indicador de negocio es la **retención**.

## 5. Antes de enviar (tú, como coordinador)

- [ ] Confirmar si el formulario admite **más de una** postulación. Si admite una sola, se decide por voto.
- [ ] Ver el límite de caracteres de cada campo: si no cabe la versión completa, pegar la corta.
- [ ] Quitar las marcas internas: «(supuesto)», «[POR CONFIRMAR]» y rutas de archivos.
- [ ] Guardar una captura del formulario enviado en `docs/`.

## 6. Mi voto

**[NEG-01 / RIE-03]**, porque ________.

## Archivos

`retos/NEG-01/`: `entrega/formulario-7-secciones.md` (para pegar) · `concepto.md` (versión 1.1 con el mapeo de la auditoría) · `casos-de-prueba.md` · `datos-publicos.md` · `preparacion.md` · `panorama.md` · `postulacion.md`.
