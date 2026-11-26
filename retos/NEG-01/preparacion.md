# NEG-01 — Preparación de Antonio (26.11.2026)

Tareas de Mariano: (1) corregir los 17 meses y la holgura; (2) revisar qué no puedo defender del formulario; (3) cinco casos a mano; (4) tasas y cifras públicas; (5) explicar el cálculo en 3 minutos sin leer. Reuniones: **18:30, cruce con Glem** · **19:45, resumen y voto a Mariano**.

## 1. Corrección hecha (17 meses y holgura)

Mariano tenía razón en los dos puntos.
- **17 meses, no 16.** Los 16 salían de aplicar El Niño solo al primer año. Un crédito que cruza dos cosechas debe resistir que la segunda también venga mala. Con la regla aplicada a toda la vida del crédito, S/ 8,000 necesita 17 meses.
- **Holgura bajo el tope.** El expediente pide «dejar holgura respecto al tope de Cuota/Utilidad Neta», y mi plan llevaba cuotas justo a 0,65. Ahora el factor efectivo es 0,585 (90 % del tope; supuesto configurable).
- **De paso:** el plan de 12 meses concentraba el 55 % del capital en dos cuotas, y el expediente pide evitarlo. Ahora el tope es 25 % del capital por cuota, así que dos cuotas nunca pasan del 50 %. Con eso, el monto máximo a 12 meses baja de S/ 6,888 a **S/ 5,895**.
- **Otro error mío:** el criterio «con ciclo plano el plan coincide con la cuota fija» era falso con nuestro motor. Ahora dice: con ciclo plano, todas las cuotas salen iguales (caso 4).

Todo está corregido en el concepto, el panorama, la postulación y el formulario.

## 2. Lo que es débil o difícil de defender en el formulario (y cómo responder)

| # | Punto débil | Qué pueden preguntar | Respuesta honesta |
|---|---|---|---|
| 1 | **Banco de pruebas circular:** nosotros generamos los perfiles sintéticos y nosotros los evaluamos | «Su modelo sale bien porque ustedes inventaron los datos» | Medimos el **plan**, no el realismo del dato: misma cartera y mismos escenarios para cuota fija y Ritmo, escenarios fijados antes de correr. La afirmación es comparativa, no una precisión absoluta. La validación real es un piloto. |
| 2 | **Sensibilidad a El Niño con series nacionales:** BCRPData tiene producción mensual por cultivo a nivel nacional; lo regional está en PDF (síntesis de La Libertad) | «¿Cómo saben cuánto afecta El Niño a Jequetepeque?» | Combinamos serie nacional por cultivo, síntesis regional del BCRP y episodios 2017 y 2023; es una aproximación. Si falta tiempo, el asesor fija el escenario El Niño. Lo dijimos como limitación. |
| 3 | **Calendario del arroz:** MIDAGRI dice que en la costa norte el arroz se cosecha casi todo el año, pero el ejemplo tiene cosecha de abril a junio | «Eso no es así en La Libertad» | La cosecha regional es continua porque cada agricultor siembra en fechas distintas; el ciclo **de cada productor** sí es marcado, y por eso ajustamos con lo que ve el asesor. El calendario del ejemplo es ilustrativo, a verificar con INIA. |
| 4 | **Parámetros nuestros:** factor efectivo de 90 % del tope, 25 % de concentración, −20 % de caída | «¿De dónde salen?» | Son supuestos configurables, no reglas de la Caja; el owner dio el factor (0,65 y 0,85) y pidió holgura sin cifra. La Caja los fijaría por producto. |
| 5 | **Menos ingreso para la Caja:** a 12 meses, seguir el ciclo paga menos interés (S/ 1,306 frente a S/ 1,572) | «¿Por qué la Caja ganaría menos?» | Menos interés porque se amortiza antes, con menos saldo expuesto y menos riesgo en los valles. El owner dijo que el indicador de negocio es la **retención**, y la herramienta muestra este intercambio en vez de esconderlo. A más plazo, más interés. |
| 6 | **Retención sin mecanismo medido** | «¿Cómo prueban que retiene?» | No lo probamos en el prototipo: el owner descartó medir mora o maduración de cartera. Lo planteamos como KPI de un piloto con línea base de la Caja. |
| 7 | **Horas al límite:** 31 de 32 horas-persona | «¿Les alcanza?» | Hay un núcleo de 26 h y un orden de recorte. El cálculo es determinista y los 5 casos ya están hechos: son las primeras pruebas. |
| 8 | **Periodicidad no mensual:** el reto la menciona y el ejemplo es mensual | «¿Y si el cliente cobra cada 4 meses?» | Las etapas del ciclo definen las fechas de pago y el cálculo usa días exactos, así que un periodo de 120 días es igual de válido. Conviene mostrarlo en la demo con un caso de una sola campaña. |
| 9 | **TEA del ejemplo (40 %)** menor que la real de Caja Trujillo para microempresa a 12 meses (55,10 %) | «Esa tasa no es la nuestra» | Es ilustrativa; con 55,10 % las conclusiones se mantienen (cuota fija S/ 846, déficit en 8 de 12 meses; S/ 8,000 a 12 meses no cabe; salida a 17 meses). Ver `casos-de-prueba.md`. |
| 10 | **«2,000 perfiles» y sus distribuciones** | «¿Por qué 2,000?» | Es un tamaño suficiente para reportar por rubro, zona y producto; es un parámetro. |

Lo que **sí** está sólido: el cálculo financiero sigue al pie de la letra las respuestas del owner; los cinco casos están calculados y son verificables en Excel; y el diseño responde a cada riesgo del expediente.

## 3. Cruce con Glem (18:30)

Pedirle que reproduzca, con su propio cálculo, estos números (tolerancia S/ 0.01):

1. Caso 1: TED 0,000935080; interés de 31 días sobre S/ 8,000 = S/ 235.18; desgravamen S/ 6.61.
2. Caso 2: cuota fija S/ 801.38; déficit en 8 de 12 meses; S/ 1,861.
3. Caso 3: interés pendiente de S/ 53.57, S/ 105.22 y S/ 129.54 en tres meses de valle.
4. Caso 4: cuota plana S/ 762.84; saldo sin pagar a 12 meses S/ 546.31.
5. Caso 5: saldo sin pagar a 12 meses S/ 2,234.79; S/ 5,895 a 12 meses; S/ 8,000 a 17 meses.

Si algún número no coincide, revisar primero: días exactos (no 30), base 360, desgravamen anual frente a mensual y el orden de la prelación.

## 4. Guion de 3 minutos para explicar el cálculo (sin leer)

**0:00–0:30. El problema en un número.** «Un arrocero gana en promedio S/ 1,304 al mes. Con ese promedio, hoy le aprobamos S/ 8,000 a 12 meses con una cuota fija de S/ 801, porque cabe en el 65 % de su utilidad. Pero mes a mes, esa cuota es mayor que lo que gana en 8 de los 12 meses. No es un mal cliente: es un mal calendario.»

**0:30–1:15. Cómo se calcula cada cuota.** «Usamos las reglas que nos dio el owner. La TEA se pasa a tasa diaria en base 360 y el interés se cobra por los días exactos de cada periodo sobre el saldo de capital. Los seguros se cobran por días. La cuota paga en orden: primero seguros, luego interés y al final capital. Si en un mes malo la cuota no alcanza ni para el interés, lo que falta queda pendiente, no genera más interés y no se paga capital hasta saldarlo.»

**1:15–2:00. La regla de capacidad.** «Cada cuota debe caber en la utilidad de **su** mes, no del promedio. Y dejamos holgura: usamos el 90 % del tope, 0,585 en vez de 0,65, y además la cuota tiene que caber aunque venga El Niño o caigan las ventas 20 %, en todos los meses del crédito. Dentro de eso, el motor carga el capital en los meses de cosecha y escoge el plan más barato para el cliente, sin que dos cuotas pasen de la mitad del capital.»

**2:00–2:45. El resultado.** «Con esas reglas, S/ 8,000 a 12 meses no cabe: quedarían S/ 2,235 sin pagar. El sistema no lo fuerza: le dice al asesor "puedes dar S/ 5,895 a 12 meses, o los S/ 8,000 a 17 meses", que alcanza dos cosechas. En las dos opciones, cero meses en que la cuota supere lo que gana, ni en año normal, ni con El Niño, ni con caída de ventas. La cuota fija a 17 meses todavía deja 8 meses en rojo.»

**2:45–3:00. Por qué confiar.** «Es un cálculo determinista: lo verificamos a mano en cinco casos que serán las primeras pruebas del prototipo. El asesor ve el porqué de cada cuota y decide; el comité aprueba.»

**Preguntas probables:** las de la tabla de §2. Las más probables son la 5 (ingreso de la Caja), la 3 (calendario del arroz) y la 1 (datos sintéticos).

## 5. Borrador del resumen y voto para Mariano (19:45)

> Mariano, resumen de NEG-01:
> 1. Corregido: holgura bajo el tope (factor efectivo 0,585 = 90 % de 0,65), El Niño en toda la vida del crédito y tope de 25 % de capital por cuota. Con eso, S/ 8,000 necesita **17 meses**, o el monto máximo a 12 meses es **S/ 5,895**. También corregí el criterio de ciclo plano, que estaba mal.
> 2. Los 5 casos están calculados en `retos/NEG-01/casos-de-prueba.md` y [cruzados / pendientes de cruzar] con Glem.
> 3. Tasas públicas: Caja Trujillo cobra 47,87 % en microempresa y 55,10 % a cuota fija de 181–360 días (SBS, oct. 2026); desgravamen de 0,105 % sobre saldo. Con esas tasas, las conclusiones se mantienen.
> 4. Lo menos defendible: que el banco de pruebas use datos que generamos nosotros, la sensibilidad a El Niño con series nacionales y el menor ingreso para la Caja a 12 meses. Tengo la respuesta para cada uno (`retos/NEG-01/preparacion.md` §2).
> 5. Mi voto: **[NEG-01 / RIE-03]**, porque ________.

**Para decidir el voto (decisión tuya):** a favor de NEG-01 están la claridad del owner sobre lo que quiere ver, un cálculo verificable que ya tenemos y tu perfil de economista como dueño del motor; además el reto es muy actual por El Niño en curso. En contra: probablemente más equipos lo elijan, y empezamos de cero en el evento. A favor de RIE-03: ya tiene generador de datos, evidencia medida (AUC 0,84) y revisión independiente.
