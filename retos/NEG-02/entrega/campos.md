# NEG-02 — campos para pegar en el formulario

**Título:** NEG-02 · Asesor de oportunidades con consentimiento verificable para un ecosistema financiero abierto

Los 8 componentes son los que fijan las bases para un Solution Concept. Cada uno trae una **versión corta** (≤ 1000 caracteres, por si el campo tiene límite) y la **versión completa** (copia de `postulacion.md`). Si el formulario pide un solo texto, usar `postulacion.md`.

## 1. Problema abordado

**Versión corta** (536 caracteres):

La información financiera de una persona o negocio está repartida entre varias instituciones y ninguna ve el cuadro completo; compartirla con autorización del cliente puede darle más valor si es segura y cumple la normativa. Hoy la Caja solo conoce lo que el cliente hace con ella: no sabe si tiene deudas más caras en otra entidad, ahorro ocioso o ingresos que llegan a otro lugar, ni atiende a quien aún no es cliente. Además, sin ver el endeudamiento externo podría ofrecer crédito a quien ya está sobreendeudado (hipótesis nuestra).

**Versión completa** (555 caracteres):

La información financiera de una persona o negocio está repartida entre varias instituciones, y ninguna ve el cuadro completo. Compartirla con autorización del cliente puede darle mayor valor, si es seguro y respeta la normativa. Hoy la Caja solo conoce lo que el cliente hace con ella: no sabe si tiene deudas más caras en otra entidad, ahorro ocioso o ingresos que llegan a otro lugar, ni puede atender a quien todavía no es su cliente. Además, sin ver el endeudamiento externo, podría ofrecer crédito a quien ya está sobreendeudado (hipótesis nuestra).

## 2. Concepto de solución

**Versión corta** (565 caracteres):

Un asesor de oportunidades con consentimiento verificable. Sobre un sandbox de Open Finance simulado, la Caja recibe datos de otras entidades solo cuando el cliente lo autoriza, arma su vista integral y propone productos; cada propuesta muestra qué dato, de qué entidad y bajo qué consentimiento la originó. También sabe abstenerse: si detecta sobreendeudamiento, no ofrece crédito. El consentimiento no es una casilla: un control en el código decide qué se puede ver según alcance, vigencia, finalidad y revocación. El sistema propone; decide siempre el ejecutivo.

**Versión completa** (770 caracteres):

Un asesor de oportunidades con consentimiento verificable. Sobre un sandbox de Open Finance simulado, la Caja recibe datos de otras entidades solo cuando el cliente lo autoriza, arma su vista integral y propone productos que le convienen. Cada propuesta muestra qué dato, de qué entidad y bajo qué consentimiento la originó. También sabe abstenerse: si detecta sobreendeudamiento, no ofrece crédito. El consentimiento no es una casilla: un control en el código decide qué se puede ver, según alcance, vigencia, finalidad y revocación. El sistema propone y la decisión es siempre del ejecutivo; no se ejecuta ninguna acción crediticia automática. Frente a la solución convencional, que ofrece con datos propios, vemos al cliente completo y atendemos también a prospectos.

## 3. Impacto esperado

**Versión corta** (655 caracteres):

KPI principal propuesto: porcentaje de clientes con una oportunidad válida identificada dentro de su consentimiento; complementos: completitud del perfil, alcance a prospectos (inclusión), ahorro potencial del cliente y reducción de ofertas de crédito indebidas. Condición de calidad: cero usos de datos fuera de consentimiento. Línea base y cifra de impacto, por validar con el owner; no se anticipa ninguna. Medición sintética en tres brazos: solo datos de la Caja (base), datos autorizados de varias entidades según los consentimientos del conjunto (escenario realista) y consentimiento total (techo). Valida el mecanismo, no el impacto comercial real.

**Versión completa** (880 caracteres):

El expediente no publica KPI ni línea base; ambos están por validar con el owner. Proponemos como KPI principal el porcentaje de clientes con una oportunidad válida identificada dentro de su consentimiento, y como complementos la completitud del perfil, el alcance a prospectos (inclusión financiera), el ahorro potencial para el cliente y la reducción de ofertas de crédito indebidas. Condición de calidad: cero usos de datos fuera de consentimiento. La línea base de la Caja y la cifra de impacto están por validar con el owner; no anticipamos ninguna cifra. Medimos con datos sintéticos, con tres brazos: solo datos de la Caja (base), datos autorizados de varias entidades según los consentimientos del conjunto (el escenario realista) y consentimiento total (el techo, para dimensionar lo que cuesta no tener consentimiento). Valida el mecanismo, no el impacto comercial real.

## 4. Enfoque tecnológico

**Versión corta** (536 caracteres):

Python, FastAPI y SQLite para las APIs simuladas y el consentimiento; React para la interfaz. Un modelo predictivo (scikit-learn) estima el ingreso a partir de los movimientos; un motor detecta oportunidades con evidencia; un agente (Pydantic AI) las explica con herramientas acotadas y verifica que cada cifra citada exista en los datos autorizados. El proveedor de IA es intercambiable y puede funcionar sin red. Cada entidad consultante usa credencial y cada acceso queda registrado. El prototipo no se conecta a sistemas de la Caja.

**Versión completa** (559 caracteres):

Python, FastAPI y SQLite para las APIs simuladas y el consentimiento; React para la interfaz. Un modelo predictivo (scikit-learn) estima el ingreso del cliente a partir de sus movimientos. Un motor detecta oportunidades con evidencia, y un agente (Pydantic AI) las explica con herramientas acotadas, verificando que cada cifra citada exista en los datos autorizados. El proveedor de IA es intercambiable y puede funcionar sin red; la política de IA externa de la Caja está por confirmar. Cada entidad consultante usa credencial y cada acceso queda registrado.

## 5. Tecnología preexistente

**Versión corta** (525 caracteres):

Antes del evento existen solo: un generador de datos sintéticos del equipo, con 41 pruebas automáticas, que produce clientes y entidades ficticios, transacciones, catálogo y consentimientos (creado el 21.11.2026; titular: el equipo), y las librerías abiertas bajo sus licencias. Es una herramienta de datos: no contiene la solución. No se usan datos reales ni código de empleadores o de otros clientes. Servicio de consentimiento, APIs simuladas, vista integral, motor, agente, interfaz y medición se construyen en el evento.

**Versión completa** (351 caracteres):

Solo librerías de código abierto y un generador de datos sintéticos del equipo, con sus 41 pruebas automáticas, creado el 21.11.2026, que produce clientes ficticios, entidades ficticias, transacciones, catálogo y consentimientos. Es una herramienta de datos: no contiene la solución. No usamos datos reales, código de empleadores ni de otros clientes.

## 6. Funcionalidad crítica

**Versión corta** (549 caracteres):

Un cliente otorga un consentimiento con alcance y vigencia; la Caja consulta tres o más entidades simuladas a través del control de consentimiento; se arma la vista integral; y el ejecutivo recibe ofertas, o una abstención, con su evidencia. Si el cliente revoca, la vista se reduce de inmediato. Criterios: lo no autorizado no llega al motor ni al agente (batería adversarial con cero fugas: consentimiento vencido, revocado, de otro receptor, solo vista, alcance insuficiente); el ejecutivo aprueba, edita o descarta; toda decisión queda auditada.

**Versión completa** (493 caracteres):

Un cliente otorga un consentimiento con alcance y vigencia; la Caja consulta tres o más entidades simuladas a través del control de consentimiento; se arma la vista integral; y el ejecutivo recibe ofertas, o una abstención, con su evidencia. Si el cliente revoca, la vista se reduce de inmediato. Se construye por completo durante la fase presencial: servicio de consentimiento, APIs simuladas, vista integral, motor, agente, interfaz y medición del KPI, con commits frecuentes como evidencia.

## 7. Nivel de desarrollo esperado

**Versión corta** (467 caracteres):

Prototipo funcional de punta a punta con un caso: un prospecto autoriza a tres entidades, la Caja propone consolidar sus deudas y explica los datos usados; el cliente revoca una entidad y la propuesta desaparece; un cliente sobreendeudado recibe una abstención. Incluye pruebas automáticas, reporte de validación y el número antes y después del KPI. Fuera de alcance: APIs o datos reales, conformidad con un estándar de Open Finance, scoring o decisiones crediticias.

**Versión completa** (341 caracteres):

Prototipo funcional de punta a punta con un caso: un prospecto autoriza a tres entidades, la Caja propone consolidar sus deudas y explica los datos usados; el cliente revoca una entidad y la propuesta desaparece; un cliente sobreendeudado recibe una abstención. Incluye pruebas automáticas, reporte de validación y el número antes y después.

## 8. Factibilidad y dependencias

**Versión corta** (623 caracteres):

28 horas-persona para el mínimo viable y 36 para el completo, frente a unas 32 a 34 disponibles; si falta tiempo se recorta la redacción con IA y la interfaz, nunca el control de consentimiento ni la evidencia. Evidencia preliminar medida sobre nuestro generador (no sobre la Caja): con las mismas reglas, la Caja sola ve el 13 % de las oportunidades, con los consentimientos del conjunto el 31 % y con información completa el 95 % (techo mecánico): el consentimiento es lo que más limita. Pendiente del owner: KPI y línea base, política de IA externa y marco de consentimiento. Sin datos de la Caja usamos nuestro sandbox.

**Versión completa** (939 caracteres):

Estimamos 28 horas-persona para el mínimo viable y 36 para el completo, frente a unas 32 a 34 disponibles; si falta tiempo se recorta la redacción con IA y la interfaz, nunca el control de consentimiento ni la evidencia. Un escenario pesimista de horas solo se sostiene con recortes. Evidencia preliminar, medida sobre nuestro generador y no sobre la Caja: al aplicar las mismas reglas con distinta visibilidad, la Caja sola ve el 13 % de las oportunidades que existen, con los consentimientos del conjunto el 31 % y con información completa el 95 % (un techo mecánico); es decir, el consentimiento, y no el modelo, es lo que más limita lo alcanzable, y por eso es el centro del diseño. Dependemos de la respuesta del owner sobre KPI y línea base, política de IA externa y marco de consentimiento. Como los datos son referenciales y sin compromiso de entrega, usaremos nuestro sandbox sintético; si la Caja comparte datos, los adaptaremos.
