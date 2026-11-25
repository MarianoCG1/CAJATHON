# NEG-02 — campos para pegar en el formulario

**Título:** NEG-02 · Asesor de oportunidades con consentimiento verificable para un ecosistema financiero abierto

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (654 caracteres):

La información financiera de una persona o negocio está repartida entre varias instituciones y ninguna ve el cuadro completo; compartirla con autorización del cliente puede darle más valor si es segura y cumple la normativa. Suponemos que hoy la Caja ve con detalle solo lo que el cliente hace con ella (supuesto a validar con el owner). Sin las tasas, el ahorro ni el flujo de ingresos que el cliente tiene en otras entidades, es difícil saber si paga deudas más caras, si tiene ahorro ocioso o si sus ingresos llegan a otro lugar, y atender a quien aún no es su cliente. Además podría ofrecer crédito a quien ya está sobreendeudado (hipótesis nuestra).

**Versión completa** (749 caracteres):

La información financiera de una persona o negocio está repartida entre varias instituciones, y ninguna ve el cuadro completo. Compartirla con autorización del cliente puede darle mayor valor, si es seguro y respeta la normativa. Suponemos que hoy la Caja ve con detalle solo lo que el cliente hace con ella y que de otras entidades tendría, como mucho, información agregada de centrales de riesgo (supuesto a validar con el owner). Sin las tasas, el ahorro ni el flujo de ingresos que el cliente tiene en otras entidades, es difícil saber si paga deudas más caras, si tiene ahorro ocioso o si sus ingresos llegan a otro lugar, y atender a quien aún no es su cliente. Además podría ofrecer crédito a quien ya está sobreendeudado (hipótesis nuestra).

## 2. Concepto de solución

**Versión corta** (588 caracteres):

Un asesor de oportunidades con consentimiento verificable. Sobre un sandbox de Open Finance simulado, la Caja recibe datos de otras entidades solo cuando el cliente lo autoriza, arma su vista integral y propone productos que podrían convenirle; cada propuesta muestra qué dato, de qué entidad y bajo qué consentimiento la originó. También sabe abstenerse: si detecta sobreendeudamiento, no ofrece crédito. El consentimiento no es una casilla: un control en el código decide qué se puede ver según alcance, vigencia, finalidad y revocación. El sistema propone; decide siempre el ejecutivo.

**Versión completa** (810 caracteres):

Un asesor de oportunidades con consentimiento verificable. Sobre un sandbox de Open Finance simulado, la Caja recibe datos de otras entidades solo cuando el cliente lo autoriza, arma su vista integral y propone productos que podrían convenirle, con la evidencia que lo sustenta. Cada propuesta muestra qué dato, de qué entidad y bajo qué consentimiento la originó. También sabe abstenerse: si detecta sobreendeudamiento, no ofrece crédito. El consentimiento no es una casilla: un control en el código decide qué se puede ver, según alcance, vigencia, finalidad y revocación. El sistema propone y la decisión es siempre del ejecutivo; no se ejecuta ninguna acción crediticia automática. Frente a la solución convencional, que ofrece con datos propios, vemos al cliente completo y atendemos también a prospectos.

## 3. Impacto esperado

**Versión corta** (757 caracteres):

KPI principal propuesto: porcentaje de clientes con una oportunidad válida identificada dentro de su consentimiento; complementos: completitud del perfil, alcance a quienes aún no son clientes (aproximación a la inclusión), ahorro potencial (con un catálogo de tasas supuesto) y reducción de ofertas de crédito indebidas. Calidad: cero fugas en la batería adversarial y 100 % de ofertas con consentimiento vigente y trazabilidad. Línea base y cifra de impacto, por validar con el owner. Tres brazos sintéticos: solo Caja, con consentimientos y consentimiento total. Dato preliminar sobre datos sintéticos propios: Caja sola 13 %, con consentimientos (tasa supuesta 65 %) 31 %, completa 95 % (tope teórico). Valida el mecanismo, no el impacto comercial real.

**Versión completa** (1576 caracteres):

El expediente no publica KPI ni línea base; ambos están por validar con el owner. Proponemos como KPI principal el porcentaje de clientes con una oportunidad válida identificada dentro de su consentimiento, y como complementos la completitud del perfil, el alcance a personas y negocios que aún no son clientes de la Caja (aproximación a la inclusión financiera; el conjunto sintético solo incluye personas con productos en otras entidades), el ahorro potencial para el cliente (calculado con un catálogo de tasas supuesto) y la reducción de ofertas de crédito indebidas. Condición de calidad: cero fugas en la batería adversarial de pruebas y el 100 % de las ofertas con consentimiento vigente y trazabilidad al dato. La línea base de la Caja y la cifra de impacto están por validar con el owner; no anticipamos ninguna cifra. Medimos con datos sintéticos, con tres brazos: solo datos de la Caja (base), datos autorizados de varias entidades según los consentimientos del conjunto (el escenario realista) y consentimiento total (el techo, para dimensionar lo que cuesta no tener consentimiento). Valida el mecanismo, no el impacto comercial real. Primer dato preliminar sobre datos sintéticos propios: sin consentimientos la visión de la Caja alcanza el 13 % de las oportunidades y abstenciones que existen y con los consentimientos del conjunto (tasa supuesta de 65 %) el 31 %, unas 2,4 veces; en el evento se mide con tres brazos e intervalos. Si el owner confirma que las centrales de riesgo ya forman parte del flujo, se añade un cuarto brazo, Caja más central de riesgo.

## 4. Enfoque tecnológico

**Versión corta** (536 caracteres):

Python, FastAPI y SQLite para las APIs simuladas y el consentimiento; React para la interfaz. Un modelo predictivo (scikit-learn) estima el ingreso a partir de los movimientos; un motor detecta oportunidades con evidencia; un agente (Pydantic AI) las explica con herramientas acotadas y verifica que cada cifra citada exista en los datos autorizados. El proveedor de IA es intercambiable y puede funcionar sin red. Cada entidad consultante usa credencial y cada acceso queda registrado. El prototipo no se conecta a sistemas de la Caja.

**Versión completa** (803 caracteres):

Python, FastAPI y SQLite para las APIs simuladas y el consentimiento; React para la interfaz. Un modelo predictivo (scikit-learn) estima el ingreso del cliente a partir de sus movimientos. Un motor detecta oportunidades con evidencia, y un agente (Pydantic AI) las explica con herramientas acotadas, verificando que cada cifra citada exista en los datos autorizados. El proveedor de IA es intercambiable y puede funcionar sin red; la política de IA externa de la Caja está por confirmar. Cada entidad consultante usa credencial y cada acceso queda registrado. Mínimo comprometido: control de consentimiento, modelo de ingreso estimado y motor con evidencia; el agente con redacción por IA y la verificación de cifras se incorporan si el tiempo lo permite, y siempre existe el modo con plantilla sin red.

## 5. Tecnología preexistente

**Versión corta** (618 caracteres):

Antes del evento existen solo: un generador de datos sintéticos del equipo, con 41 pruebas automáticas, que produce clientes y entidades ficticios, transacciones, catálogo y consentimientos, y un script de auditoría que mide cuánto del conjunto de datos es visible con distinta información (análisis del conjunto, no motor ni medición del KPI). Ambos creados el 21.11.2026; titular: el equipo. Librerías abiertas bajo sus licencias. Sin datos reales ni código de empleadores o de otros clientes. Servicio de consentimiento, APIs simuladas, vista integral, motor, agente, interfaz y medición se construyen en el evento.

**Versión completa** (554 caracteres):

Solo librerías de código abierto y dos herramientas de datos del equipo creadas el 21.11.2026: un generador de datos sintéticos, con 41 pruebas automáticas, que produce clientes y entidades ficticios, transacciones, catálogo y consentimientos; y un script de auditoría que mide cuánto del conjunto de datos es visible con distinta información (análisis del conjunto, no motor ni sistema de medición). Ninguna contiene la solución; la medición del KPI se escribe desde cero en el evento. No usamos datos reales, código de empleadores ni de otros clientes.

## 6. Funcionalidad crítica

**Versión corta** (577 caracteres):

Un cliente otorga un consentimiento con alcance y vigencia; la Caja consulta tres o más entidades simuladas a través del control de consentimiento; se arma la vista integral; y el ejecutivo recibe ofertas, o una abstención, con su evidencia. Si el cliente revoca, la vista se reduce de inmediato. Criterios: lo no autorizado no llega al motor ni al agente (batería adversarial con cero fugas: consentimiento vencido, revocado, de otro receptor, solo vista, alcance insuficiente, ventana histórica excedida); el ejecutivo aprueba, edita o descarta; toda decisión queda auditada.

**Versión completa** (493 caracteres):

Un cliente otorga un consentimiento con alcance y vigencia; la Caja consulta tres o más entidades simuladas a través del control de consentimiento; se arma la vista integral; y el ejecutivo recibe ofertas, o una abstención, con su evidencia. Si el cliente revoca, la vista se reduce de inmediato. Se construye por completo durante la fase presencial: servicio de consentimiento, APIs simuladas, vista integral, motor, agente, interfaz y medición del KPI, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

**Versión corta** (467 caracteres):

Prototipo funcional de punta a punta con un caso: un prospecto autoriza a tres entidades, la Caja propone consolidar sus deudas y explica los datos usados; el cliente revoca una entidad y la propuesta desaparece; un cliente sobreendeudado recibe una abstención. Incluye pruebas automáticas, reporte de validación y el número antes y después del KPI. Fuera de alcance: APIs o datos reales, conformidad con un estándar de Open Finance, scoring o decisiones crediticias.

**Versión completa** (642 caracteres):

Prototipo funcional de punta a punta con un caso: un prospecto autoriza a tres entidades, la Caja propone consolidar sus deudas y explica los datos usados; el cliente revoca una entidad y la propuesta desaparece; un cliente sobreendeudado recibe una abstención. Incluye pruebas automáticas, reporte de validación y el número antes y después. Alcance: la Caja actúa como receptora de datos de otras entidades (supuesto); su rol como proveedora y la colaboración con otros actores del ecosistema quedan como hoja de ruta; no hay APIs ni datos reales, ni conformidad declarada con un estándar de Open Finance, ni decisiones o scoring crediticio.

## 8. Factibilidad y dependencias

**Versión corta** (610 caracteres):

28 horas-persona para el mínimo viable y 36 para el completo, frente a 32 a 34 disponibles; en un escenario pesimista el mínimo sube a unas 41 h y solo cabe con recortes ya definidos (primero la redacción con IA y la interfaz, nunca el consentimiento ni la evidencia). Mínimo comprometido: control de consentimiento, modelo de ingreso estimado y motor con evidencia. Dato preliminar sobre datos sintéticos propios: Caja sola 13 % de las oportunidades y abstenciones, con consentimientos 31 % (tasa supuesta 65 %), completa 95 % (tope teórico). Pendiente: KPI y línea base, IA externa y marco de consentimiento.

**Versión completa** (1030 caracteres):

Estimamos 28 horas-persona para el mínimo viable y 36 para el completo, frente a unas 32 a 34 disponibles (cuatro personas, de 8 a 8,5 horas cada una). En un escenario pesimista el mínimo sube a unas 41 horas y solo cabe con recortes que ya definimos: primero la redacción con IA y la interfaz, nunca el control de consentimiento ni la evidencia. Evidencia preliminar medida sobre datos sintéticos propios (no sobre la Caja): con las mismas reglas, la Caja sola identifica el 13 % de las oportunidades y abstenciones que existen; con los consentimientos del conjunto, bajo una tasa de consentimiento supuesta de 65 %, el 31 %; con información completa, el 95 % (tope teórico, porque la verdad se define con las mismas reglas). En el evento mediremos la sensibilidad a esa tasa. Dependemos de la respuesta del owner sobre KPI y línea base, política de IA externa y marco de consentimiento. Como los datos son referenciales y sin compromiso de entrega, usaremos nuestro sandbox sintético; si la Caja comparte datos, los adaptaremos.
