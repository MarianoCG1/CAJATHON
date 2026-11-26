# Guía de estudio — qué haremos en cada reto y cómo impactaremos

Para Mariano (coordinador y pareja líder de RIE-03, NEG-02, RIE-01 y RIE-02). Resume lo que dicen `concepto.md` y `panorama.md` de cada reto, más lo que encontró la auditoría de datos (`docs/investigacion/06-auditoria-datos.md`). Todo lo no oficial es **supuesto**; el expediente no publica KPI ni línea base en ningún reto.

## 0. La idea común a los cuatro

Los cuatro retos siguen el mismo esqueleto, que es lo que el jurado va a reconocer:

1. **Un sistema que prioriza.** Convierte muchos datos en una lista corta y ordenada (clientes, redes, oportunidades) con el **porqué** de cada una.
2. **Una acción propuesta.** Cada elemento trae qué hacer (visitar, reprogramar, verificar, ofrecer).
3. **Una persona decide.** El sistema propone y registra; no ejecuta ni toma decisiones crediticias (lo piden los expedientes).
4. **Un número antes/después.** Un backtest sobre datos sintéticos compara con reglas simples. Valida el **mecanismo**, no el impacto comercial real; eso se declara.

Cómo impactamos, en una línea: **le damos al gestor la lista correcta antes de que el problema ocurra, con la evidencia para actuar, y medimos cuánto mejora frente a lo que haría una regla simple.** La cifra de impacto real depende de la línea base de la Caja, que aún no existe: no se inventa.

| | RIE-03 Deterioro | NEG-02 Open Finance | RIE-01 Clima | RIE-02 Redes de riesgo |
|---|---|---|---|---|
| **Quién usa** | Gestor/analista de cartera | Ejecutivo comercial | Gestor de agencia y analista de riesgo | Especialista de prevención/investigación |
| **Qué entrega** | Cola diaria de clientes con riesgo de deterioro | Oportunidades por cliente, trazables al consentimiento | Lista de clientes y zonas ante un escenario climático | Redes sospechosas con expediente de evidencia |
| **Acción** | Intervención preventiva con mensaje borrador | Oferta explicada (o abstención) | Alerta, visita, reprogramación, microseguro… | Pedir verificación o escalar |
| **KPI principal (supuesto)** | Paso a atraso > 30 d de la cartera alertada, con y sin intervención | % de clientes con oportunidad identificada **y consentida** | % de cartera afectada identificada antes del evento | Precisión/recall de redes y falsos positivos |
| **Línea base que usamos** | Política reactiva simulada y reglas de una señal | Brazo «solo Caja» | Azar, regla de zona, zona + actividad, orden por saldo | Reglas de coincidencia simples y una regla con criterio de dominio |
| **Datos preexistentes** | Cartera de 5,000 clientes, 34 meses | 2,000 clientes, 6 entidades ficticias, 215 mil transacciones | 12,000 clientes, 44 distritos, 6 eventos de prueba | 3,700 solicitudes, 123 redes |

---

## 1. RIE-03 · Anticipar el deterioro de pago antes del atraso (prioridad #1)

**El problema, en simple.** Un microempresario no cae en mora de un día para otro: antes baja su actividad, cambia cómo paga, se endeuda en otro lado. Esas señales se ven tarde o se confunden con altibajos normales. Resultado: se interviene cuando ya hay mora, o se alerta de más y se cansa al gestor y al cliente.

**Qué construiríamos.** Cada día, una **cola corta** de clientes al día con riesgo de deteriorarse. Tres piezas:
- *Modelo de deterioro:* probabilidad calibrada con rango de incertidumbre; sin historial suficiente, no alerta.
- *Separador de señal y fluctuación:* solo entra a la cola si la caída es persistente, no es estacional y se repite en al menos dos familias de señales (ingreso, conducta de pago, endeudamiento externo). Es el control de falsos positivos.
- *Agente de intervención:* propone canal, momento y borrador de mensaje citando la evidencia. No promete condiciones crediticias. El gestor aprueba, edita o descarta.

**Cómo impactamos y cómo lo medimos.** Menos alertas inútiles y más anticipación. En backtest: casos detectados, **días de anticipación** frente al primer atraso, falsos positivos frente a reglas simples, y el efecto de intervenir como **tabla de sensibilidad** (los datos no traen intervenciones, así que no se afirma como hecho).

**Lo que dice la auditoría de datos.** No es trivial. Quien está al día es el caso difícil: la regla «ya tiene atraso» no sirve y las señales de alerta temprana suben el AUC de 0.81 a 0.92 sobre la cartera completa. Entre clientes al día, el 10 % mejor puntuado concentra ≈ 6 de cada 10 casos (≈ 6.4× de lift). Se presenta en lift y captura, no en precisión absoluta (evento raro: 0.7 %).

**Qué debes poder defender.**
- Por qué no es «un puntaje de mora»: entrega acción explicada y mide falsos positivos.
- Por qué no hay fuga del futuro: variables *as-of* (solo información ≤ fecha de corte) y prueba de no-fuga.
- Por qué la intervención es un escenario y no un resultado.

**Riesgos.** Plan de 31.5 h para 32 disponibles; en el escenario pesimista 45 h y solo cabe con nueve recortes. Mínimo viable: cola + explicación + aprobación con bitácora + backtest + pruebas.

**Pregunta clave al owner:** definición de «deterioro» y horizonte útil (30, 60, 90 días), y capacidad del analista (define k).

---

## 2. NEG-02 · Open Finance: competir en un ecosistema abierto (prioridad #3)

**El problema, en simple.** El cliente tiene su vida financiera repartida entre varias entidades. Con su autorización, esa información puede compartirse. ¿Cómo la usa la Caja para dar más valor al cliente y competir, **sin violar el consentimiento**?

**Qué construiríamos.** Un **sandbox** con entidades, APIs y consentimientos simulados (el expediente pide datos sintéticos e integraciones simuladas) y sobre él:
- *Guardia de consentimiento:* único camino hacia datos de otras entidades. Aplica en código alcance, vigencia, finalidad, receptor y revocación; audita cada acceso. Lo no autorizado **no llega** al motor ni al agente.
- *Vista 360 y motor de oportunidades:* consolidación de deuda, capital de trabajo MYPE, captación de ahorro, domiciliación de ingresos, y una **abstención** (no ofrecer crédito a quien está sobreendeudado). Cada resultado cita el dato y el consentimiento que lo autorizó.
- *Agente:* explica y redacta la propuesta para el ejecutivo, y verifica que cada cifra citada exista en la evidencia autorizada.

**Cómo impactamos y cómo lo medimos.** Más oportunidades identificadas **con consentimiento**, menos ofertas indebidas. Backtest con tres brazos: *Caja sola* (base), *360 con los consentimientos del dataset* (el escenario realista) y *360 con consentimiento total* (techo).

**Lo que dice la auditoría de datos.** Detecta el **efecto del consentimiento**: Caja sola ve 13 % de las oportunidades existentes, con consentimientos 31 %, con información completa 95 %. La visión multientidad más que duplica lo que ve la Caja sola, y el consentimiento —no el modelo— es lo que limita. Ojo: el 95 % es un techo mecánico (las reglas de la verdad son las mismas), no una capacidad medida.

**Qué debes poder defender.**
- Por qué el consentimiento se hace cumplir en el código y no en la interfaz: batería adversarial (vencido, revocado, otro receptor, finalidad «solo vista», alcance insuficiente, ventana histórica) con cero fugas.
- Por qué se abstiene: la visión multientidad también sirve para **no** ofrecer.
- Qué **no** prometemos: APIs o datos reales, conformidad con un estándar de Open Finance, el rol de la Caja como proveedora.

**Riesgos.** El punto débil de la detección es el sobreendeudamiento con ingreso estimado (precisión 0.6–0.8). Mucho alcance para 8 h: guardia + vista 360 + motor + agente + UI + KPI.

**Pregunta clave al owner:** qué busca ganar la Caja con Open Finance y qué reglas de consentimiento deben respetar las ofertas.

---

## 3. RIE-01 · Microfinanzas resilientes al clima (prioridad #4)

**El problema, en simple.** Lluvias intensas, inundaciones y sequías golpean a los negocios financiados, sobre todo los de zonas vulnerables o actividades sensibles (un arrozal no es una bodega). Hoy probablemente se reacciona cuando aparece la mora. ¿Cómo anticiparnos y actuar antes, con pocos gestores?

**Qué construiríamos.** **Radar Climático de Cartera**: el analista elige un escenario ex ante (por ejemplo, «inundación severa en la costa norte») y el sistema:
- recalcula la cartera en **tres capas**: amenaza local → vulnerabilidad del negocio (actividad, colchón financiero) → impacto crediticio;
- entrega **tres cifras separadas**, cada una con rango p10–p50–p90: cartera *expuesta*, *probablemente afectada* y *mora incremental esperada* (el expediente pide no asumir que exposición implica pérdida);
- muestra mapa y ranking según la **capacidad real de visitas** de cada agencia;
- un agente propone acciones del catálogo (alerta, visita, reprogramación, ampliación de plazo, capital de reposición, microseguro) y el gestor aprueba o rechaza.

**Cómo impactamos y cómo lo medimos.** Cuánta cartera afectada identificamos antes del evento y cuánta mora se captura con una capacidad limitada de visitas. KPI candidatos: K1 % de cartera afectada identificada anticipadamente, K2 precisión y captura de saldo en mora, K3 pérdida evitada estimada (rango), K4 continuidad de los negocios afectados. Backtest con seis eventos con verdad oculta frente a azar, regla de zona, zona + actividad y orden por saldo.

**Lo que dice la auditoría de datos.** No es trivial, pero la señal es **moderada**: con 2 semanas de visitas (≈ 8 % de la cartera) se captura ≈ 20 % de los incumplimientos (azar 8 %, regla de 3 factores 17.5 %, techo con la susceptibilidad real 24 %). El impacto honesto es un lift de ≈ 2.5×. **Alerta:** la ventaja del modelo sobre la regla de zona + actividad es de ≈ 2 puntos; el criterio «superar a las reglas en 5 de 6 eventos» puede fallar por ruido. Hay que decidirlo con Glem antes del evento (ver `06-auditoria-datos.md`).

**Qué debes poder defender.**
- Por qué no es «un mapa de calor»: tres capas, tres números, incertidumbre visible y presupuesto de gestores.
- Por qué se evalúa también con un evento más severo que la historia.
- Qué no modelamos por separado: acceso a mercados y daño a infraestructura (se resumen en la caída de ingreso).

**Riesgos.** Es el reto con más piezas (modelo en 3 capas, mapa, ranking con capacidad, agente, backtest). El mapa es el candidato a recortar primero.

**Pregunta clave al owner:** cómo gestionan hoy el riesgo por eventos climáticos, qué acciones son viables y cuántas visitas son realistas.

---

## 4. RIE-02 · Descubrir redes de riesgo ocultas (prioridad #5)

**El problema, en simple.** Un fraude puede repartirse entre varias personas, negocios y solicitudes que, vistas una por una, parecen normales. Pero compartir un teléfono o una dirección **no es fraude**: lo hacen las familias, los puestos de un mercado, los gremios. El reto es distinguir lo legítimo de lo que merece revisión.

**Qué construiríamos.** **Mesa del especialista de redes**: convierte un lote de solicitudes en un grafo (personas, negocios, teléfonos, dispositivos, direcciones, referencias), encuentra grupos conectados de forma inusual, los prioriza y entrega un **expediente con evidencia citada y las explicaciones legítimas posibles**, con una acción de prevención (pedir verificación) o investigación (escalar). Cuatro ideas:
1. El peso de un vínculo depende de lo raro que es (un dispositivo personal compartido por cinco pesa; una tableta de agencia no).
2. **Regla de corroboración:** una red solo se prioriza si combina estructura **y** comportamiento o perfil anómalo. Cumple «no concluir fraude solo por relaciones».
3. Cada alerta muestra su contrapartida legítima.
4. El agente redacta el expediente pero no decide; un verificador rechaza citas inexistentes y frases que concluyan fraude.

**Cómo impactamos y cómo lo medimos.** Redes detectadas, **menos falsos positivos** y menos tiempo de preparación de un caso. Backtest sobre redes inyectadas y relaciones legítimas «señuelo», con partición de desarrollo y evaluación ciega, intervalos por remuestreo y una ablación de la regla de corroboración.

**Lo que dice la auditoría de datos.** Ya se endureció (la regla simple resolvía el 100 %); no se repitió esta vez. Conviene que la revisión de Antonio compruebe que los señuelos sigan siendo difíciles.

**Qué debes poder defender.**
- Por qué un expediente nunca dice «fraude», sino «patrón que merece revisión».
- Cómo bajas de prioridad una familia o un mercado con el mismo dato compartido.
- Cómo mides el efecto de la regla de corroboración (ablación).

**Riesgos.** Grafo + puntaje + agente + verificador + interfaz de grafo. El volumen (≈ 3,700 solicitudes) y la dificultad son supuestos nuestros.

**Pregunta clave al owner:** cómo se detecta hoy y con qué falsos positivos, y qué relaciones legítimas son frecuentes.

---

## 5. Qué conviene decidir esta noche con el equipo

1. **¿Se acepta más de un concepto por equipo?** Sin esa respuesta no sabemos si las ocho postulaciones valen. Consulta lista en `docs/consulta-organizacion.md`.
2. **RIE-01:** ¿ajustamos el criterio de aceptación o reforzamos la estructura del generador? (ver `06-auditoria-datos.md`).
3. **NEG-02:** ¿el KPI se presenta como «oportunidades identificadas y consentidas» en tres brazos? Es lo que la auditoría respalda.
4. **Carga:** los cuatro retos sin desarrollar recaen en Glem, Antonio y David; Mariano puede apoyar NEG-01.
5. **Antonio:** que valide la lógica financiera de los KPI de NEG-02 y RIE-01 y los supuestos de costo y efectividad.
