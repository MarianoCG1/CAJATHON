# Panorama de abastecimiento — NEG-02 · Open Finance: competir en un ecosistema financiero abierto

> Versión 1.1 (ronda 2: cotejo con el expediente literal, alcance MVP, prueba pesimista de horas) · 21.11.2026 · Pareja líder: Antonio + Mariano · Revisor: David · Owners (plataforma): Roger, Arturo.
> Material **confidencial**: repo privado. Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene de la Caja. Los datos son 100 % sintéticos.
> Este documento acompaña a `retos/NEG-02/concepto.md`. No se ha construido nada de la funcionalidad crítica: solo existe el generador de datos (`retos/NEG-02/datos/`) y esta documentación.

**Qué es lo único que ya existe:** `python retos/NEG-02/datos/generar.py` produce el ecosistema sintético descrito en §2 (2 000 clientes, 6 entidades, ~215 mil transacciones, ~1 700 consentimientos) con semilla fija. Todas las cifras de «propiedades del dataset» de este documento salen de la ejecución con la semilla `20261121`; **no son resultados del KPI**.

---

## 0. Alcance MVP en una página

**Qué entra (mínimo viable, 28 h-persona):**

- Servicio de consentimiento (otorgar, revocar, vigencia, alcance, finalidad, ventana histórica) con auditoría de accesos y denegaciones.
- Guardia por columna como único camino a los datos de otras entidades, con credencial por entidad receptora.
- APIs simuladas de 3 o más entidades, alimentadas por los CSV del generador.
- Vista 360 con **modelo de ingreso estimado** (scikit-learn, entrenado con el ingreso declarado de clientes de la Caja) y completitud del perfil.
- Motor de oportunidades con linaje: 4 ofertas (consolidación de deuda, capital de trabajo, captación de ahorro, domiciliación de ingresos) y 1 abstención por sobreendeudamiento.
- Agente delgado (Pydantic AI, herramientas de solo lectura) con redacción por plantilla verificada contra la evidencia; proveedor de LLM intercambiable.
- Interfaz de una página: consentimiento del cliente, vista 360 y oportunidades con «¿por qué?» (linaje); el ejecutivo aprueba, edita o descarta.
- `evaluar_kpi.py` con tres brazos; pruebas de guardia, fuga y extremo a extremo; `docs/validacion.md`.

**Qué queda fuera:** APIs o datos reales; conformidad con algún estándar o norma de Open Finance; scoring o decisión crediticia automática; rol de la Caja como proveedora y colaboración con otros actores del ecosistema (hoja de ruta); autenticación real de usuarios finales; app móvil; envío de mensajes; despliegue en la nube.

**Núcleo no recortable:** guardia y consentimiento (T2) · linaje en cada oferta y abstención por sobreendeudamiento (T5) · batería de fuga con consentimientos vencidos, revocados, de otro receptor, de solo vista y con alcance insuficiente (T11) · flujo extremo a extremo · número antes/después (brazo «Caja-solo» frente a 360 consentido).

**Opcional (se recorta primero; orden en §4.3 y §4.4):** redacción con LLM real, modelo de propensión, interfaz completa, sensibilidad a la tasa de consentimiento y multi-semilla del KPI, captación y domiciliación, auditoría encadenada por hash.

**Criterio de terminado (todo debe cumplirse a las 12:45 del día 2):**

1. El cliente otorga y revoca consentimientos desde la interfaz y el estado se calcula y audita.
2. Se consultan 3 o más entidades solo dentro del alcance, vigencia, finalidad y ventana consentidos; lo demás se deniega con motivo.
3. La vista 360 muestra el perfil y su completitud con y sin datos multientidad.
4. Hay al menos 2 tipos de oferta con evidencia y consentimiento citados, más 1 abstención.
5. La batería de la guardia pasa en verde (cero fugas) y toda oportunidad tiene linaje vigente.
6. El ejecutivo decide y la decisión queda auditada; nada se ejecuta solo.
7. `evaluar_kpi.py` entrega el número antes/después de forma reproducible y queda en `validacion.md`, con historial de commits.

**Guion de demo de 5 minutos (termina con el número antes/después):**

| Minuto | Qué se muestra | Qué debe quedar claro |
|---|---|---|
| 0:00–0:30 | El problema en una frase: la información del cliente está repartida y la Caja solo ve su parte | Alineación con el reto |
| 0:30–1:30 | Un **prospecto** (p. ej. «Bodega · Víctor Larco Herrera») otorga consentimiento a 3 entidades con alcances y vigencia distintos | Consentimiento claro, por alcance y con fecha de vencimiento; inclusión de quien aún no es cliente |
| 1:30–2:30 | Vista 360: perfil con solo datos de la Caja (campos conocidos X de 12) y luego con lo autorizado (Y de 12); ingreso estimado | Valor de la visión multientidad |
| 2:30–3:30 | Oferta de consolidación de deuda: clic en «¿por qué?» muestra entidad, campo, valor y consentimiento; el agente redacta; el ejecutivo aprueba | Trazabilidad al dato autorizado; decisión humana |
| 3:30–4:00 | Cliente sobreendeudado: el sistema **no ofrece crédito** y explica por qué | La visión multientidad también protege |
| 4:00–4:30 | El cliente **revoca** una entidad: la vista se reduce al instante y la denegación queda en auditoría | El consentimiento se cumple en el código |
| 4:30–5:00 | Número antes/después: clientes con oportunidad válida y consentida pasa de A % (solo Caja) a B % (360 consentido), con intervalo; ofertas indebidas bajan; fugas = 0 | Impacto medible y honesto (valores reales de la corrida del día; no se anticipan) |

Plan B de la demo: todo local y sin red (plantilla determinista), casos curados de antemano y capturas de respaldo.

---

## 1. Qué necesita el desafío

### 1.1 Lo que dice el expediente (texto literal en `retos/NEG-02/expediente.md`; aquí, resumido)

- **Pregunta de innovación:** cómo aprovechar el intercambio **seguro y autorizado** de información financiera para desarrollar soluciones que generen **mayor valor para los clientes** y fortalezcan la competitividad de Caja Trujillo.
- **Problema:** la información de un cliente está distribuida entre varias instituciones, lo que dificulta una visión integral de su comportamiento, necesidades y oportunidades de atención. El intercambio se da «con su autorización y bajo las condiciones regulatorias aplicables».
- **Resultado esperado:** nuevas propuestas de valor basadas en ese intercambio, mejorando el **conocimiento de los clientes**, la **personalización** de servicios y la identificación de oportunidades de **crecimiento e inclusión financiera**.
- **Datos e insumos:** APIs simuladas, transacciones, información multientidad, perfiles financieros, catálogo de productos, consentimientos simulados y datos sintéticos. **Nota del expediente: los datos son referenciales y no implican un compromiso de entrega de la Caja.**
- **Riesgos:** garantizar **privacidad, seguridad y uso autorizado**, considerando el consentimiento del cliente y la normativa aplicable. **Los prototipos deben usar datos sintéticos e integraciones simuladas, sin asumir disponibilidad de datos reales ni APIs operativas.**
- **Complejidad tecnológica:** IA, agentes, analítica predictiva, optimización o automatización avanzada «cuando aporten valor real»; no basta un chatbot genérico, un dashboard, un formulario ni una automatización básica; se debe demostrar desarrollo funcional, integración tecnológica y **valor diferencial frente a soluciones convencionales**.
- **No publicado:** KPI, línea base, columnas y volumen de datos, política de IA externa y el marco regulatorio concreto (el expediente habla de «normativa aplicable» sin nombrarla). Todo eso es **[POR CONFIRMAR]** (preguntas en §7). Como no hay compromiso de entrega de datos, **el caso base es nuestro propio sandbox**.

### 1.2 Componentes, insumos y quién los provee

| # | Necesidad | Para qué sirve | Origen | Estado hoy |
|---|---|---|---|---|
| 1 | **Datos multientidad sintéticos** (clientes, productos, transacciones, catálogo) | Materia prima de la vista 360 y del KPI | **Preexistente** (generador del equipo) o los que entregue la Caja | Listo: `retos/NEG-02/datos/sintetico/` |
| 2 | **Consentimientos con alcance, vigencia, finalidad y revocación** | Es el control que hace legítimo el uso del dato | Preexistente (datos) · lógica de consentimiento: **evento** | Datos listos; servicio por construir |
| 3 | **APIs simuladas por entidad** | El «ecosistema abierto» que consulta la Caja | **Evento** (sobre los CSV) | Por construir |
| 4 | **Guardia de consentimiento** (control de acceso por alcance, vigencia, finalidad, receptor y ventana histórica) y **credencial por entidad receptora** | Garantiza que lo que se ve está autorizado y que quien consulta está identificado; es la pieza de confianza y de seguridad | **Evento** | Por construir |
| 5 | **Vista 360** (agregación acotada, ingreso estimado, completitud del perfil) | Convierte datos dispersos en un perfil | **Evento** | Por construir |
| 6 | **Motor de oportunidades con linaje** (reglas + estimación) | Detecta ofertas y abstenciones, cada una con su evidencia | **Evento** | Por construir |
| 7 | **Agente** (Pydantic AI, herramientas acotadas, redacción verificada) | Explica y redacta la propuesta; no decide | **Evento** | Por construir |
| 8 | **Interfaz**: pantalla de consentimiento (cliente) y vista del ejecutivo | Demo y experiencia; el consentimiento claro es parte del diferencial | **Evento** | Por construir |
| 9 | **Catálogo de productos de la Caja y reglas de oferta responsable** | Qué se puede ofrecer y cuándo **no** | Supuesto del equipo hasta que la Caja lo valide | Catálogo supuesto listo; reglas por construir |
| 10 | **Arnés de KPI** (`scripts/evaluar_kpi.py`: 3 brazos + sensibilidad) | Número antes/después | **Evento** | Diseño en §5 |
| 11 | **Proveedor de LLM intercambiable** (`app/llm/provider.py`) | Política de IA externa sin cerrar | **Evento** | Interfaz en §3.5 |
| 12 | **Validación jurídica** (Legal/Compliance de la Caja) | Texto de consentimiento y marco normativo | Caja Experts | [POR CONFIRMAR] |

---

## 2. Cómo abastecerlo: sandbox y dataset sintético

### 2.1 Principios

1. **Todo ficticio:** entidades «Demo», sin nombres comerciales reales, sin personas, documentos, teléfonos ni correos (hay una prueba que lo verifica). Los clientes se muestran con una `etiqueta_demo` (p. ej. «Bodega · Víctor Larco Herrera»).
2. **Sin APIs operativas reales:** las «APIs» las construimos nosotros sobre los CSV en el evento. No se afirma conformidad con ningún estándar de Open Finance.
3. **Reproducible:** `SeedSequence(semilla)` con cuatro flujos independientes (clientes, productos, transacciones, consentimientos); `manifest.json` guarda semilla, parámetros y SHA-256 de cada archivo. Misma semilla y parámetros ⇒ mismos bytes (prueba incluida).
4. **La verdad está separada:** `retos/NEG-02/datos/sintetico/verdad/` contiene lo que el mundo «realmente» es (ingreso real, necesidades). **El agente, la API y la UI nunca la leen**; solo `evaluar_kpi.py`.
5. **Plausible, no real:** montos en S/, segmentos MYPE, distritos de La Libertad, calificación SBS por tramos de atraso. Todas las tasas, montos y probabilidades son **supuestos** del equipo (no tarifas de la Caja ni del mercado).

### 2.2 Entidades (todas ficticias)

| `entidad_id` | Nombre | Tipo | Rol en el sandbox |
|---|---|---|---|
| E00 | Caja Receptora (rol Caja Trujillo) | Caja municipal | **Receptora**: consulta con consentimiento |
| E01 | Banco Andino Demo | Banco | Fuente |
| E02 | Financiera Sol Andina Demo | Financiera | Fuente |
| E03 | Caja Municipal Pacifico Demo | Caja municipal | Fuente |
| E04 | Cooperativa Cumbre Demo | Cooperativa | Fuente |
| E05 | Fintech Kuntur Demo | Fintech | Fuente |

Mínimo exigido por el desafío: 3 entidades simuladas. Generamos **5 fuentes + la receptora**; la demo usa 3, el resto sirve para robustez y para el KPI.

### 2.3 Tablas

El diccionario completo (columna, tipo, descripción) lo escribe el propio generador en `retos/NEG-02/datos/sintetico/diccionario_datos.md`. Resumen:

| Archivo | Filas (semilla por defecto) | Clave | Contenido |
|---|---|---|---|
| `entidades.csv` | 6 | `entidad_id` | Las 6 entidades |
| `catalogo_productos.csv` | 23 | `producto_id` | Productos por entidad: categoría, rango de TEA, plazo y monto. Los de E00 son los ofertables (`es_oferta_caja`). Todo `es_supuesto` |
| `clientes.csv` | 2 000 | `cliente_id` | Segmento, actividad, provincia/distrito, rango de edad, `es_cliente_caja` (prospecto si es falso), ingreso **declarado** a la Caja (con ruido; vacío en prospectos) |
| `productos_cliente.csv` | 5 874 | `producto_cliente_id` | Contratos: entidad, categoría, estado (ACTIVO/MORA/CANCELADO), monto, saldo, TEA, plazo, cuota, días de atraso, calificación |
| `transacciones.csv` | 215 074 | `tx_id` | Movimientos de 6 meses (may–oct 2026): abonos (sueldo, ventas, transferencia), compras, retiros, pago de servicios, pago a proveedores y **pagos de cuota** |
| `consentimientos.csv` | 1 743 | `consentimiento_id` | Quién (cliente), a quién (receptora), de quién (fuente), finalidad, otorgado, plazo (90/180/365 d), vencimiento, revocación, estado, ventana histórica (3/6/12 m), canal, versión de texto, renovación |
| `consentimiento_alcances.csv` | 5 966 | (consentimiento, alcance) | Un renglón por alcance concedido |
| `consentimiento_eventos.csv` | 2 191 | `evento_id` | Auditoría: OTORGADO, REVOCADO, VENCIDO |
| `alcances_campos.csv` | 17 | (alcance, tabla, columna) | **Qué columna autoriza cada alcance** (ver §2.5) |
| `verdad/verdad_cliente.csv` | 2 000 | `cliente_id` | Ingreso real, arquetipos y agregados de verdad |
| `verdad/verdad_oportunidades.csv` | 10 000 | (cliente, tipo) | Para cada cliente y tipo de oportunidad, si existe con información completa |

Tamaño: ~19 MB (casi todo en `transacciones.csv`). No hace falta versionarlo: se regenera en ~6 s.

### 2.4 Volúmenes y distribuciones (parámetros del generador)

| Aspecto | Diseño | Resultado con la semilla por defecto |
|---|---|---|
| Clientes | 2 000 (parámetro `--n-clientes`) | — |
| Segmentos | MYPE comercio 35 %, MYPE servicios 20 %, MYPE agro 12 %, asalariado 20 %, independiente 13 % | 34 / 21 / 12 / 20 / 13 % |
| Ingreso mensual real | Lognormal por segmento (medianas S/ 1 900–3 200), mínimo S/ 1 130, máximo S/ 30 000 | Mediana S/ 2 570 |
| Geografía | 15 distritos de 6 provincias de La Libertad; agro concentrado en Virú, Chepén, Laredo, Casa Grande | 15 distritos |
| Clientes de la Caja vs. prospectos | 60 % clientes (65 % en agro) | 63 % / 37 % |
| Entidades por cliente | Prob. de relación: E01 38 %, E02 15 %, E03 22 %, E04 8 %, E05 18 %, más la Caja | 40 % en 1 entidad, 35 % en 2, 22 % en 3, 2 % en 4 (**60 % en 2 o más**) |
| Productos | Cuenta/billetera según entidad; 0–2 créditos por entidad; depósito a plazo (6 %); seguro (8 % de quien tiene crédito); crédito cancelado (15 %, historial) | 5 874 contratos |
| Créditos | Cuota objetivo = fracción del ingreso (8–40 % normal; 55–90 % en el arquetipo sobreendeudado); monto por anualidad con TEA del rango del catálogo; saldo por amortización francesa | Todos dentro de rango del catálogo (prueba) |
| Mora | 4 % de los créditos (30 % en sobreendeudados), con días log-uniformes 1–150 y calificación por tramos | 1.8 % de contratos en MORA |
| Sin cuenta | 12 % de los clientes no tiene cuenta transaccional (economía en efectivo): no hay flujo observable | 14.3 % sin abonos |
| Transacciones | Abonos según segmento (sueldo mensual; ventas ~6 por mes; transferencias), débitos ~7 por mes (65–100 % del abono), cuotas mensuales; estacionalidad suave; el agro es casi plano en may–oct a propósito (la estacionalidad no debe parecer crecimiento) | 215 mil filas |
| Crecimiento | 20 % de MYPE y 5 % del resto crecen 35–80 % en la ventana; el resto deriva ±8 % | Media de crecimiento 0.30 en el arquetipo vs. ~0.00 en el resto |
| Dónde cae el ingreso | Cliente de la Caja con cuenta externa: 80 % de los casos recibe 55–95 % en la Caja; arquetipo «ingresos en otra entidad» (15 %) recibe 0–25 % en la Caja | — |
| Consentimientos | `--tasa-consentimiento` 0.65 (**supuesto**; 0.65×0.65 en sobreendeudados: selección adversa). Por entidad externa consiente el 88 %. Finalidad OFERTA 80 % / VISTA 20 %. Alcance: PRODUCTOS siempre; SALDOS 92 %, CONDICIONES 88 %, TRANSACCIONES 65 % (con ajuste por «apertura» del cliente) | 1 295 vigentes, 309 vencidos, 139 revocados |
| Vigencia | Otorgado en los últimos 270 días; plazo 90 (15 %), 180 (30 %), 365 (55 %); revocación 8 %; renovación del 45 % de los vencidos (111 renovaciones) | Estado a la fecha de corte 31.10.2026 |
| Terceros | 12 % de los clientes consiente compartir con **otra** entidad (receptor ≠ Caja): no vale para la Caja | 229 consentimientos a otros receptores |
| Semilla | `20261121` (parámetro `--semilla`) | — |

**Propiedades del dataset (no son KPI):**

- Clientes con al menos un consentimiento **vigente de finalidad OFERTA** hacia la Caja: **36 %**.
- Frecuencia de cada oportunidad en la verdad de terreno: consolidación 11.6 %, capital de trabajo 10.8 %, captación de ahorro 9.5 %, domiciliación de ingresos 11.1 %, restricción por sobreendeudamiento 8.3 %.
- Casos «alcanzables» con los consentimientos del dataset (todos los datos externos que la regla necesita están cubiertos por consentimientos vigentes de finalidad OFERTA con los alcances requeridos): capital de trabajo 36 %, captación 25 %, domiciliación 18 %, consolidación 15 %, restricción 10 %. Esto muestra que **el consentimiento, no el modelo, es el cuello de botella**: por eso su experiencia (y su medición) forma parte de la propuesta.

### 2.5 Alcances del consentimiento (qué autoriza cada uno)

La tabla `alcances_campos.csv` es el contrato que la guardia aplicará **por columna**. Toda columna de datos pertenece a exactamente un alcance (hay una prueba); las claves de identificación acompañan a cualquier alcance.

| Alcance | Tabla | Columnas que habilita |
|---|---|---|
| `PRODUCTOS` | `productos_cliente` | `producto_id`, `categoria`, `estado`, `fecha_apertura`, `fecha_cierre` |
| `SALDOS` | `productos_cliente` | `monto_original_pen`, `saldo_actual_pen` |
| `CONDICIONES` | `productos_cliente` | `tasa_ea_pct`, `plazo_meses`, `cuota_mensual_pen`, `dias_atraso`, `calificacion` |
| `TRANSACCIONES` | `transacciones` | `fecha`, `sentido`, `tipo`, `categoria`, `monto_pen` (solo dentro de `historia_meses`) |

Finalidades: `OFERTA_PRODUCTOS` permite que la Caja genere ofertas; `VISTA_FINANCIERA` solo permite mostrar al cliente su propia vista (no ofertar).

Supuesto de diseño **[POR CONFIRMAR con Legal]**: los datos de la propia Caja (E00) no se condicionan a un consentimiento del sandbox (relación contractual). Su uso para ofertas podría requerir igualmente finalidad informada.

### 2.6 Tipos de oportunidad y verdad de terreno

La verdad se calcula en el generador con **información completa** (incluido el ingreso real latente, que la Caja no ve) mediante reglas explícitas. La solución debe **reconstruirla solo con lo observable y autorizado**. Umbrales = **supuestos**, constantes al inicio de `generar.py`.

| Tipo | Regla de verdad (resumen) | Datos que necesita la solución | Alcances requeridos |
|---|---|---|---|
| `CONSOLIDACION_DEUDA` | Sin restricción; ≥ 2 créditos externos activos; saldo externo ≥ S/ 4 000; algún crédito externo con TEA ≥ 40 % (el producto de la Caja cuesta menos); cuota/ingreso ≥ 0.15 | Créditos y condiciones en otras entidades; ingreso estimado | PRODUCTOS + SALDOS + CONDICIONES (y TRANSACCIONES o ingreso declarado) |
| `CAPITAL_TRABAJO_MYPE` | Segmento MYPE; sin restricción; abonos promedio ≥ S/ 800; crecimiento de abonos (2.ª mitad vs. 1.ª) ≥ 15 %; cuota/ingreso < 0.35 | Flujo de abonos en todas las entidades | PRODUCTOS + TRANSACCIONES |
| `CAPTACION_AHORRO` | ≥ S/ 8 000 en cuentas de ahorro externas con TEA ≤ 2.5 % | Saldos y tasas de ahorro externas | PRODUCTOS + SALDOS + CONDICIONES |
| `DOMICILIACION_INGRESOS` | Cliente de la Caja; abonos promedio ≥ S/ 800; menos del 30 % de los abonos llega a la Caja | Dónde caen los abonos | PRODUCTOS + TRANSACCIONES |
| `RESTRICCION_SOBREENDEUDAMIENTO` | **No es una oferta: es una abstención.** Cuota total/ingreso > 0.50 o algún crédito con calificación Deficiente o peor | Todos los créditos externos; ingreso estimado | PRODUCTOS + SALDOS + CONDICIONES |

Casos difíciles incluidos a propósito: clientes con deuda cara y dispersa **pero sobreendeudados** (no se les debe ofrecer consolidación), estacionalidad agro que no es crecimiento, prospectos sin ningún dato propio, clientes sin cuenta (flujo no observable), consentimientos vencidos con renovación vigente, consentimientos con finalidad solo «vista», consentimientos a otro receptor y ventanas históricas de 3 meses.

### 2.7 Cómo regenerar y adaptar

```powershell
python retos/NEG-02/datos/generar.py                                 # datos por defecto en retos/NEG-02/datos/sintetico/
python retos/NEG-02/datos/generar.py --n-clientes 500 --semilla 7     # variante pequeña
python retos/NEG-02/datos/generar.py --tasa-consentimiento 0.35       # sensibilidad al consentimiento
python -m pytest retos/NEG-02/datos -q                                # pruebas del generador
```

Si la Caja entrega su propio sandbox o datos, se crea un adaptador que los lleve a este mismo esquema; el resto del sistema no cambia.

---

## 3. Arquitectura (a construir en el evento)

### 3.1 Vista general

```
 Cliente ── UI de consentimiento ──► Servicio de consentimiento ──► Registro + auditoría (SQLite)
                                              │ decide(receptor, cliente, fuente, alcance, finalidad, ahora)
 Ejecutivo ── UI vista 360 ──► Vista 360 ──► GUARDIA DE CONSENTIMIENTO ──► APIs simuladas E01..E05 (FastAPI) ──► SQLite ← CSV
                                   │              (filtra filas y columnas; sella el linaje)
                                   ▼
                        Motor de oportunidades (reglas + estimación) ──► Oportunidad { tipo, evidencia[] con linaje }
                                   ▼
                        Agente (Pydantic AI) ──► LLMProvider ──► redacción ──► verificación contra la evidencia
                                   ▼
                        Ejecutivo: aprobar · editar · descartar  ──► auditoría de la decisión
```

La **guardia** es el único camino hacia los datos de otras entidades. Ni el motor, ni el agente, ni la UI tienen acceso directo a las tablas.

### 3.2 APIs simuladas (propuesta; no es un estándar)

| Método | Ruta | Alcance | Notas |
|---|---|---|---|
| GET | `/fuentes/{entidad}/clientes/{cliente}/productos` | PRODUCTOS | Una entidad por consulta |
| GET | `/fuentes/{entidad}/clientes/{cliente}/saldos` | SALDOS | |
| GET | `/fuentes/{entidad}/clientes/{cliente}/condiciones` | CONDICIONES | |
| GET | `/fuentes/{entidad}/clientes/{cliente}/transacciones?desde=&hasta=` | TRANSACCIONES | Recortado a `historia_meses` |
| POST | `/consentimientos` | — | Otorga (alcances, finalidad, plazo, historia) |
| POST | `/consentimientos/{id}/revocar` | — | Efecto inmediato |
| GET | `/consentimientos?cliente=` | — | Lista con estado calculado a `ahora` |
| GET | `/clientes/{cliente}/vista-360` | — | Pasa por la guardia; devuelve perfil, completitud y linaje |
| GET | `/clientes/{cliente}/oportunidades` | — | Ofertas y abstenciones con evidencia |
| POST | `/oportunidades/{id}/decision` | — | aprobar / editar / descartar (auditado) |

Para que la demo y el KPI sean reproducibles, el reloj es un parámetro (`ahora`, por defecto la fecha de corte 31.10.2026).

### 3.3 Guardia de consentimiento (la pieza crítica)

`decidir(receptor, cliente, fuente, alcance, finalidad, ahora) → permitir | denegar(motivo)`

Se permite solo si existe un consentimiento con **todas** estas condiciones:

1. `entidad_receptora_id` = quien consulta (los consentimientos a otros receptores no cuentan).
2. `entidad_fuente_id` = entidad consultada.
3. Vigente a `ahora`: otorgado ≤ ahora ≤ vencimiento y sin revocación anterior a `ahora`.
4. El alcance pedido figura entre los alcances concedidos.
5. La finalidad concedida cubre la pedida (`OFERTA_PRODUCTOS` cubre todo; `VISTA_FINANCIERA` no cubre ofertas).
6. Para `TRANSACCIONES`: solo filas con fecha ≥ ahora − `historia_meses`.

Con varios consentimientos vigentes se aplica la **unión** y cada fila de salida lleva el `consentimiento_id` que la autorizó. Las columnas se proyectan según `alcances_campos.csv`: lo no autorizado **no sale**, ni siquiera como `null` identificable. Cada denegación queda en auditoría con su motivo (VENCIDO, REVOCADO, ALCANCE, FINALIDAD, RECEPTOR, SIN_CONSENTIMIENTO).

**Seguridad (el expediente pide «seguro y autorizado»):** las APIs simuladas exigen una **credencial por entidad receptora** (sin credencial: 401; credencial de otra entidad: 403); la auditoría es de solo anexado y no guarda datos personales ni valores de los campos, solo identificadores y motivos; los secretos se leen de variables de entorno y nunca se versionan; el LLM solo recibe evidencia mínima y sintética. *(Opcional: auditoría encadenada por hash.)* Son controles del sandbox, no una afirmación de seguridad de producción.

### 3.4 Vista 360, motor de oportunidades y agente

- **Vista 360:** une lo autorizado de cada entidad; calcula número de entidades, deuda y cuota totales, ahorro externo, dónde caen los abonos, **ingreso estimado** por un modelo (scikit-learn) entrenado con el ingreso declarado de los clientes de la Caja a partir de señales de transacciones (nivel y estabilidad de abonos, gasto, cuotas); si no hay `TRANSACCIONES`, el ingreso declarado a la Caja; si no, desconocido; siempre con nivel de confianza. Es el componente de **analítica predictiva** del mínimo viable y la **completitud del perfil** (campos conocidos / campos definidos, §5).
- **Motor de oportunidades:** reglas con umbrales explícitos + estimación del ingreso y de la capacidad de pago. Devuelve oportunidades `{tipo, producto_caja, motivo, evidencia[]}` donde cada evidencia es `{entidad, tabla, campo, valor, consentimiento_id, alcance}`. Si no hay evidencia suficiente por falta de consentimiento, devuelve «no evaluable» (no adivina). `RESTRICCION_SOBREENDEUDAMIENTO` genera una **abstención** que bloquea las ofertas de crédito. *(Opcional si sobra tiempo: modelo de propensión con scikit-learn entrenado sobre datos sintéticos; se declara su circularidad.)*
- **Agente (Pydantic AI):** herramientas acotadas de solo lectura (`obtener_vista_360`, `listar_catalogo_caja`, `obtener_oportunidades`); salida estructurada. Redacta la propuesta para el ejecutivo. **Verificación:** todo número o entidad citado en el texto debe existir en la evidencia; si no, se descarta el texto del LLM y se usa la plantilla determinista. El agente propone; **la decisión es del ejecutivo** y no se ejecuta ninguna acción crediticia.

### 3.5 Interfaz del proveedor de LLM (`app/llm/provider.py`)

```python
class Evidencia(BaseModel):
    entidad_id: str; tabla: str; campo: str; valor: str | float | int
    consentimiento_id: str; alcance: str

class Redaccion(BaseModel):
    texto: str; proveedor: str; modelo: str

class LLMProvider(Protocol):
    nombre: str
    def redactar(self, instruccion: str, evidencia: list[Evidencia], *, max_tokens: int = 400) -> Redaccion: ...

# Implementaciones: PlantillaProvider (determinista, sin red; por defecto y respaldo de la demo),
# ClaudeProvider, OpenAIProvider, LocalProvider (modelo local). Selección por variable de entorno.
```

Reglas: el proveedor solo recibe **evidencia ya autorizada y sintética**; sin red la demo sigue funcionando (plantilla); se puede cambiar de proveedor sin tocar la lógica. La política de IA externa de la Caja es **[POR CONFIRMAR]**.

---

## 4. Plan hora a hora del evento (4 personas, ~8 h por persona)

Agenda oficial: Día 1 validación del enfoque 09:45; construcción 10:30–13:00 y 14:00–16:30; pruebas 16:30–17:30. Día 2 construcción 09:30–12:00; validación final 12:00–12:45; **entrega 13:00**; pitch 15:00. Total ≈ 8.5 h por persona (2.5 + 2.5 + 1.0 + 2.5) más 0.75 h de validación. **(Los horarios exactos se confirman con la organización.)**

Roles (CLAUDE.md §3): **M**ariano backend/agente · **G**lem datos/modelo/pruebas · **A**ntonio KPI/negocio · **D**avid UX/UI. Commits frecuentes desde la primera hora como evidencia de desarrollo.

### 4.1 Tareas y horas revisadas (supuesto)

Historial de la estimación: 38 h-persona en el borrador v0 (con 3 h de «datos sintéticos»); 35 h completo / 27 h mínimo en la ronda 1; **36 h completo / 28 h mínimo viable en la ronda 2**, porque el cotejo con el expediente obliga a incluir en el mínimo un componente de analítica predictiva (modelo de ingreso, T4 +1.0 h) y credenciales por receptor (dentro de T3).

| # | Tarea | Dueño | Completo | Mínimo viable | Qué se recorta en el mínimo |
|---|---|---|---|---|---|
| T1 | Cargador CSV → SQLite del sandbox | A | 1.0 | 1.0 | — |
| T2 | Servicio de consentimiento + guardia por columna y auditoría | M | 3.0 | 3.0 | **Núcleo, no se recorta** |
| T3 | APIs simuladas por entidad, con credencial por receptor | M | 2.5 | 2.0 | Un solo router parametrizado por entidad; 3 fuentes |
| T4 | Vista 360 + completitud + **modelo de ingreso estimado** | G | 3.5 | 3.0 | Sin segmentación; solo los campos del KPI |
| T5 | Motor de oportunidades con linaje (4 ofertas + 1 abstención) | G + M | 3.0 | 3.0 | **Núcleo**; sin modelo de propensión |
| T6 | Agente Pydantic AI + redacción verificada + proveedor intercambiable | M (+G) | 2.5 | 1.0 | Plantilla determinista; LLM opcional |
| T7 | Diseño de la experiencia de consentimiento (flujo y textos claros) | D (+A) | 2.0 | 1.5 | Un solo flujo, sin variantes |
| T8 | Interfaz: consentimiento, vista 360, oportunidades con linaje | D | 5.0 | 3.0 | Una página con tres paneles |
| T9 | Catálogo de la Caja, reglas de oferta responsable y textos | A | 2.0 | 1.5 | Solo los 4 productos usados |
| T10 | `evaluar_kpi.py`: 3 brazos, IC, sensibilidad al consentimiento | A | 3.0 | 2.0 | Sin sensibilidad ni multi-semilla |
| T11 | Pruebas (guardia, fuga, e2e) + `docs/validacion.md` | G + A + D | 4.0 | 3.0 | Matriz reducida; el núcleo se mantiene |
| T12 | Pitch, casos de demo curados y guion | A + D | 2.5 | 2.0 | Una sola historia |
| T13 | Integración, ensayo de demo y congelamiento | Todos | 2.0 | 2.0 | — |
| | **Total** | | **36.0** | **28.0** | |

**Lectura:** el plan completo (36 h) no cabe en la capacidad (4 × 8.5 = 34 h); el **mínimo viable (28 h) sí**, con **6 h de reserva** (el mínimo aguanta un desvío uniforme de solo ~21 % antes de tener que recortar: 34 / 28). Orden para gastar la reserva: T8 (+2.0 interfaz completa) → T6 (+1.5 redacción con LLM verificada) → T10 (+1.0 sensibilidad) → T11 (+1.0 más pruebas) → T3, T4, T7, T9, T12 (+0.5 cada uno). Si Legal o el owner cambian el alcance, se recorta desde el final.

Reparto por persona del **plan mínimo** (h): Mariano 7.5 (T2 3.0, T3 2.0, T5 1.0, T6 1.0, T13 0.5) · Glem 7.0 (T4 3.0, T5 2.0, T11 1.5, T13 0.5) · Antonio 7.0 (T1 1.0, T9 1.5, T10 2.0, T11 1.0, T12 1.0, T13 0.5) · David 6.5 (T7 1.5, T8 3.0, T11 0.5, T12 1.0, T13 0.5). Mariano sigue siendo quien más carga y el único en la ruta T2 → T3 → T6; ver §4.4.

### 4.2 Cronograma por bloque (plan mínimo; «libre» = reserva para extras)

| Bloque | Mariano | Glem | Antonio | David |
|---|---|---|---|---|
| **Día 1 · 10:30–13:00** (2.5 h) | T2: modelo de consentimiento, estados, guardia; **contrato `decidir()` y un doble en memoria en los primeros 30 min** para desbloquear a los demás (2.5) | T4: características y entrenamiento del modelo de ingreso con el ingreso declarado (2.5) | T1: cargador (1.0) · T9: catálogo y reglas responsables (1.5) | T7: flujo y textos de consentimiento (1.5) · T8: pantalla de consentimiento (1.0) |
| **Día 1 · 14:00–16:30** (2.5 h) | T2: auditoría y revocación (0.5) · T3: APIs simuladas con credencial por receptor (2.0) | T4: vista 360 y completitud (0.5) · T5: motor de oportunidades sobre la guardia (2.0) | T10: diseño y script con verdad (1.0) · T11: matriz de pruebas de consentimiento (0.5) · T12: casos de demo (0.5) · libre 0.5 | T8: vista 360 (1.0) · T12: casos de demo (0.5) · libre 1.0 |
| **Día 1 · 16:30–17:30** (1.0 h) | T5: integra motor con vista (1.0) | T11: pruebas de la guardia (1.0) | T10: primer número, brazo Caja-solo (0.5) · T11: borrador de `validacion.md` (0.5) | T8: conectar UI a la API (0.5) · T13: humo e2e día 1 (0.5) |
| **Día 2 · 09:30–12:00** (2.5 h) | T6: agente y proveedor (1.0) · T13 (0.5) · libre 1.0 | T11: fuga y e2e (0.5) · T13 (0.5) · libre 1.5 | T10: brazos 360 y gráfico (0.5) · T12: pitch (0.5) · T13 (0.5) · libre 1.0 | T8: panel de oportunidades con linaje (0.5) · T11: e2e de interfaz (0.5) · T12 (0.5) · libre 1.0 |
| **12:00–12:45** | Congelar, tag, `validacion.md` final | Tests verdes, manifest de datos | Número antes/después en la presentación | Capturas, ensayo de demo |
| **13:00** | **Entrega** | | | |
| **15:00** | Pitch y demo | | | |

**Hitos de control:** fin del día 1 = flujo consentimiento → consulta a 3 entidades → vista 360 funcionando sobre el sandbox + primer número del KPI (brazo base). Si a las 14:00 del día 1 la guardia no devuelve datos filtrados por alcance en pruebas, se recortan T3 y T6 antes de tocar T2.

### 4.3 Qué recortar si falta tiempo (en orden)

1. Redacción con LLM → plantilla determinista (el producto sigue funcionando; se explica que el proveedor es intercambiable).
2. Interfaz: una sola página con tres paneles; sin variantes del flujo de consentimiento.
3. Sensibilidad al consentimiento y multi-semilla del KPI → dejar una sola corrida con IC.
4. Reducir de 5 a 3 entidades fuente y de 4 ofertas a 3 (conservar consolidación, capital de trabajo y la **abstención**).
5. **No se recorta nunca:** guardia de consentimiento, linaje de cada oferta, prueba de fuga con consentimientos vencidos/revocados y número antes/después.

### 4.4 Escenario pesimista de horas

**Supuesto de la prueba:** cada tarea cuesta ×1.4 de lo estimado y las de la ruta crítica (T2, T3, T5, T6) ×1.6. Se aplica al **mínimo viable**. No incluye imprevistos ajenos al plan (red del Hub, entorno, enfermedad).

| Tarea | Mínimo | Factor | Pesimista |
|---|---|---|---|
| T1 Cargador | 1.0 | ×1.4 | 1.4 |
| T2 Consentimiento y guardia | 3.0 | ×1.6 | 4.8 |
| T3 APIs simuladas | 2.0 | ×1.6 | 3.2 |
| T4 Vista 360 y modelo de ingreso | 3.0 | ×1.4 | 4.2 |
| T5 Motor de oportunidades | 3.0 | ×1.6 | 4.8 |
| T6 Agente | 1.0 | ×1.6 | 1.6 |
| T7 Diseño de consentimiento | 1.5 | ×1.4 | 2.1 |
| T8 Interfaz | 3.0 | ×1.4 | 4.2 |
| T9 Catálogo y reglas | 1.5 | ×1.4 | 2.1 |
| T10 Arnés de KPI | 2.0 | ×1.4 | 2.8 |
| T11 Pruebas y validación | 3.0 | ×1.4 | 4.2 |
| T12 Pitch y demo | 2.0 | ×1.4 | 2.8 |
| T13 Integración y ensayo | 2.0 | ×1.4 | 2.8 |
| **Total** | **28.0** | | **41.0** |

**Resultado sin recortes:** 41.0 h frente a 34 h de capacidad (8.5 h × 4): **faltan 7.0 h (20 %)**; contra 32 h (8 h × 4) faltan 9.0. Con el reparto del mínimo, **todos** quedan por encima de su capacidad (Mariano 11.9 h, Glem 10.2, Antonio 9.8, David 9.1), así que nadie puede absorber a otro. El plan completo en pesimista sería de 52.6 h: queda descartado de entrada.

**Recortes que se activan** (en este orden; la mayoría ya figuran en §4.3):

| # | Recorte | Pesimista antes → después | Ahorro (h) |
|---|---|---|---|
| a | T6: plantilla determinista + agente delgado (una herramienta, sin verificación con LLM) | 1.6 → 0.8 | 0.8 |
| b | T3: una sola ruta de pasarela `/consulta` en vez de rutas por tipo de dato | 3.2 → 2.2 | 1.0 |
| c | T8: una página sin estilo, con dos paneles | 4.2 → 3.0 | 1.2 |
| d | T10: una sola corrida, sin intervalos ni sensibilidad | 2.8 → 1.8 | 1.0 |
| e | T11: 8 casos de guardia y 1 e2e | 4.2 → 3.0 | 1.2 |
| f | T9: 3 productos y umbrales fijos | 2.1 → 1.4 | 0.7 |
| g | T4: **sin modelo de ingreso** (promedio de abonos o ingreso declarado) | 4.2 → 2.8 | 1.4 |
| h | T7: patrón de consentimiento estándar, sin variantes | 2.1 → 1.4 | 0.7 |
| i | T12: una sola historia de demo | 2.8 → 2.1 | 0.7 |
| | **Total** | | **8.7** |

Con los nueve recortes el total baja a **32.3 h**. Reasignación para equilibrar: Mariano **8.5** (T2 4.8, T3 2.2, T6 0.8, T13 0.7) · Glem **8.3** (T4 2.8, T5 3.8, T11 1.0, T13 0.7) · Antonio **8.35** (T1 1.4, T9 1.4, T10 1.8, T5 1.0 con las reglas de oferta y la política de abstención, T11 1.0, T12 1.05, T13 0.7) · David **7.15** (T7 1.4, T8 3.0, T11 1.0, T12 1.05, T13 0.7).

**¿Cabe?** Sí en 34 h, con 1.7 h (5 %) de holgura; **no** en 32 h (faltan 0.3 h). Mariano, Glem y Antonio quedan al 98–100 %; solo David tiene unas 1.35 h libres.

**¿Se sostiene el mínimo de 3/5 en funcionamiento de la funcionalidad crítica?** Respuesta honesta: **en el límite, no con holgura.**

- *A favor:* los recortes quitan riqueza, no el flujo. Se conservan la guardia con revocación, la consulta a 3 entidades, la vista 360, las ofertas con linaje, la abstención, la decisión humana y el número antes/después; eso es lo que el jurado verá funcionando.
- *En contra 1, sin margen:* un desvío adicional de pocas horas en T2 o T3 rompe el plan. Ejemplo: T2 ×2.0 (6.0 h en vez de 4.8) deja a Mariano en 9.7 h y no hay a quién traspasar T3 (Glem y Antonio están llenos). En ese caso **el mínimo no se sostiene** y hay que elegir entre quitar la interfaz o quitar parte de la pasarela.
- *En contra 2, calidad:* para proteger el 3/5 en funcionamiento se sacrifican justo los componentes que sostienen la «complejidad tecnológica» y la innovación que pide el expediente (modelo de ingreso, agente con verificación, KPI con intervalos y sensibilidad). El producto quedaría como reglas + pasarela con consentimiento: funcional y verificable, pero con menos diferenciación frente a «soluciones convencionales». Como la condición eliminatoria pesa más que esos puntos, **se recorta primero la riqueza**, y eso debe aceptarse de antemano.
- *Cronología crítica:* con T2 en 4.8 h, la guardia cierra cerca de las 16:20 del día 1; T3 llegaría a media mañana del día 2; quedan unas 1.5 h para integrar interfaz, agente y KPI antes de las 12:00. Cualquier bloqueo de integración se come la validación final.

**Riesgo que agrega que Mariano concentre T2, T3, T5 (parte) y T6:**

1. **Ruta crítica secuencial en una sola persona:** consentimiento → APIs → motor → agente → interfaz. Un atraso en T2 retrasa a todos.
2. **Punto único de fallo:** bloqueo, enfermedad o un error sutil en la guardia (un error de confianza, el peor tipo en este reto).
3. **Sin revisión por pares** del control más importante: lo que más se vende («el consentimiento se cumple») es lo que menos ojos revisa.
4. **Los demás esperan su interfaz:** Glem (motor), David (interfaz) y Antonio (KPI) dependen de `decidir()` y de la pasarela.

**Mitigaciones:** contrato `decidir()` y doble en memoria en los primeros 30 minutos; en el pesimista, T5 completo pasa a Glem y Antonio (ya reflejado arriba); T3 se acuerda de antemano como traspasable a Glem (conoce FastAPI); revisión cruzada de 15 minutos de la guardia por Antonio contra la matriz de pruebas. **Disparadores:** si a las 14:00 del día 1 la guardia no filtra por alcance en pruebas → recortes a, b y c; si a las 16:30 del día 1 T2 no está cerrada → traspasar T3 a Glem sin esperar; si a las 10:00 del día 2 la pasarela no responde con datos filtrados → congelar alcance y dedicar todo el equipo a integración y pruebas.

---

## 5. Diseño de la medición del KPI

**El expediente no publica KPI ni línea base** → todo lo que sigue es **(supuesto)** hasta que el owner responda (§7). La medición se diseña para ser reproducible y honesta sobre lo que prueba.

### 5.1 Qué mide (y qué no)

Mide el **mecanismo**: cuánto valor agrega la visión multientidad **bajo control de consentimiento**, y que ese control no se rompe. **No** mide conversión comercial real ni mejora de cartera: eso requeriría datos y pilotos de la Caja. No se presenta ninguna cifra de impacto sin línea base.

### 5.2 Brazos del experimento

| Brazo | Datos que ve el motor | Rol |
|---|---|---|
| **A · Caja-solo** | Solo E00 (productos propios, ingreso declarado, perfil básico). **Mismo motor y mismas reglas** | **Línea base metodológica**: aísla el efecto de los datos multientidad |
| **B · 360 con consentimientos del dataset** | Lo que la guardia autoriza con los consentimientos reales del sandbox | **Escenario realista** (el resultado que se presenta) |
| **C · 360 con consentimiento total** | Todo, como si todos hubieran consentido | **Techo** para dimensionar el costo de no tener consentimiento; no se presenta como resultado |

Separar B de C permite decir cuánto de la oportunidad depende de la experiencia de consentimiento. El **brazo A es también nuestra «solución convencional»** (campañas y ofertas con los datos propios de la Caja), que es lo que el expediente pide superar con «valor diferencial».

### 5.3 Métricas

| # | Métrica | Definición | Cómo se lee |
|---|---|---|---|
| M1 | **Clientes con ≥ 1 oportunidad válida identificada y consentida** (candidato a KPI principal) | Clientes con al menos una oferta recomendada que coincide con la verdad y cuyo linaje es 100 % consentido ÷ universo. Se reporta sobre (i) todos los clientes y (ii) solo los que consintieron | Antes (A) vs. después (B), con IC 95 % |
| M2 | **Precisión y recall por tipo** | Contra `verdad_oportunidades`. Dos recalls: **absoluto** (vs. toda la verdad) y **condicional** (solo sobre casos «alcanzables» con los consentimientos, para separar calidad del motor de cobertura de consentimiento) | A vs. B vs. C |
| M3 | **Completitud del perfil** | Campos conocidos ÷ 12 campos definidos (segmento, distrito, edad, ingreso estimado, n.º de entidades, deuda total, cuota total, ahorro total, tasa media de crédito, peor calificación, abonos promedio, % de abonos en la Caja) | A vs. B, promedio y distribución |
| M4 | **Ofertas de crédito indebidas** | Ofertas de crédito emitidas a clientes con `RESTRICCION_SOBREENDEUDAMIENTO = 1` | Debe **bajar** de A a B: la visión multientidad sirve también para no ofrecer |
| M5 | **Integridad del consentimiento** | (a) % de oportunidades con linaje completo y consentimiento vigente = **100 %**; (b) fugas = **0** en la batería adversarial (§6) | Se exige, no se optimiza |
| M6 | **Conversión estimada (escenario)** | Ofertas válidas × tasa de aceptación **paramétrica** [POR CONFIRMAR con el owner]. Se reporta como rango de sensibilidad, nunca como cifra única | Secundaria; sin tasa oficial no se presenta como resultado |
| M7 | **Inclusión financiera** | M1 desglosado por **prospectos** (quienes aún no son clientes de la Caja; ~37 % del dataset) y por segmento (MYPE frente a asalariado/independiente). En el brazo A un prospecto no tiene datos propios | Cuántas personas y negocios antes invisibles quedan atendibles con su consentimiento |
| M8 | **Beneficio para el cliente (escenario)** | Para consolidaciones identificadas: ahorro anual potencial de intereses = saldo externo × (TEA externa − TEA del producto de la Caja), calculado con la evidencia y el catálogo supuesto; se reporta como **potencial**, no como resultado | Muestra «mayor valor para los clientes» sin inventar tasas de aceptación |

### 5.4 Línea base

- **Metodológica (la que usamos):** brazo A con el mismo motor.
- **De la Caja:** **[POR CONFIRMAR con el owner]**. Si la Caja entrega su línea base (p. ej. de conversión o de conocimiento del cliente), se reemplaza o se agrega como segunda referencia. Hasta entonces, **no se escribe ninguna cifra de impacto**.

### 5.5 Procedimiento (`scripts/evaluar_kpi.py`, a construir en el evento)

1. Generar datos con semilla fija y verificar el `manifest.json`.
2. Cargar el sandbox. Fijar `ahora` = fecha de corte.
3. Para cada brazo, correr el motor sobre **todos** los clientes (A restringido a E00; B a través de la guardia con los consentimientos reales; C con consentimiento total).
4. Comparar con la verdad; calcular M1–M5.
5. Intervalos: bootstrap por cliente (1 000 remuestreos, semilla fija) para M1–M4.
6. Robustez: repetir con 5 semillas del generador (si el tiempo lo permite).
7. Sensibilidad: regenerar con `--tasa-consentimiento` 0.2, 0.4, 0.65, 0.8 y graficar M1 contra la tasa. Es el argumento para invertir en la experiencia de consentimiento.
8. Escribir tabla antes/después en `docs/validacion.md` y un JSON con los resultados.

### 5.6 Amenazas a la validez (se declaran en la presentación)

- **Circularidad:** los datos y las reglas de verdad son nuestros. Mitigación: la verdad usa el ingreso **real latente** (no observable), por lo que el motor debe estimarlo; incluir casos difíciles; reportar que el resultado valida el mecanismo, no el negocio.
- **Selección adversa:** los clientes más endeudados consienten menos (lo simulamos). Se reportan ambos denominadores en M1.
- **Parámetros supuestos:** tasa de consentimiento, umbrales, TEA y tasas de aceptación se exponen como parámetros y se ofrece sensibilidad.

---

## 6. Riesgos y mitigaciones

| # | Riesgo | Impacto | Mitigación |
|---|---|---|---|
| R1 | **Privacidad:** uso de datos fuera del consentimiento | Crítico | Guardia como único camino a los datos; minimización por columna; auditoría de cada acceso y denegación; solo datos sintéticos |
| R2 | **Consentimiento mal aplicado** (vencido, revocado, otro receptor, finalidad «solo vista», alcance insuficiente, ventana histórica) | Crítico | Batería adversarial de pruebas (§8); prueba de propiedad de fuga; el dataset incluye todos esos casos |
| R3 | **Normativa:** marco de Open Finance y protección de datos. Conocemos como referencia general la Ley de Protección de Datos Personales (consentimiento libre, previo, expreso, inequívoco e informado; finalidad; derecho de revocación) y el secreto bancario, **a verificar con Legal**. No hemos verificado si existe un marco específico de Open Finance en el país **[POR CONFIRMAR]** | Alto | Pedir a los Caja Experts (Legal, Compliance) validar el texto de consentimiento y los alcances; no afirmar cumplimiento: el prototipo «respeta los principios» de consentimiento y finalidad |
| R4 | **Decisiones crediticias automáticas** | Alto | Diseño «propone, humano decide»; abstención por sobreendeudamiento; ninguna acción se ejecuta |
| R5 | **Sesgo y selección adversa** | Medio | Sin atributos sensibles (no hay sexo ni documento); reportar M1 con ambos denominadores; revisar M4 por segmento |
| R6 | **Alucinación del LLM** | Alto | Motor determinista decide; el LLM solo redacta; verificación de cifras contra la evidencia; respaldo de plantilla |
| R7 | **Política de IA externa desconocida** | Medio | Proveedor intercambiable; opción local o plantilla; el proveedor solo recibe evidencia sintética y mínima |
| R8 | **«No asumir APIs ni datos reales»** | Medio | Nuestras APIs son un sandbox propio; no se declara conformidad con ningún estándar; si la Caja entrega su sandbox, adaptador al mismo esquema |
| R9 | **Alcance excesivo para ~8 h** | Alto | Mínimo viable de 28 h con 6 h de reserva; en el escenario pesimista (41 h) solo cabe con 9 recortes y sin holgura (§4.4); recortes ordenados en §4.3; núcleo claro |
| R10 | **Circularidad de los datos sintéticos** | Medio | Verdad con variable latente, casos difíciles, discurso honesto sobre lo que se mide (§5.6) |
| R11 | **Evidencia de desarrollo nuevo (condición eliminatoria):** el generador es preexistente | Alto | Declararlo en `preexistente.md`; todo lo demás nace en el evento con commits frecuentes; la funcionalidad crítica **no** se adelanta |
| R12 | **Confidencialidad del material de la Caja** | Alto | Repo privado; el generador es genérico y publicable después; no publicar expedientes, conceptos ni panoramas |
| R13 | **La demo depende de red o del LLM** | Medio | Plantilla determinista por defecto; todo local |
| R14 | **El efecto de la experiencia de consentimiento no es medible con datos sintéticos** | Medio | Tratar la tasa de consentimiento como parámetro y mostrar sensibilidad; no afirmar un efecto causal del diseño de UX |
| R15 | **Seguridad del sandbox:** acceso sin credencial, filtración por logs o secretos en el repo | Alto | Credencial por entidad receptora (401/403), auditoría sin datos personales ni valores, secretos en variables de entorno, LLM solo con evidencia mínima sintética; pruebas de §9.2 |
| R16 | **Concentración de la ruta crítica en una persona (Mariano)** | Alto | Contrato `decidir()` y doble en memoria al inicio, traspasos y disparadores definidos en §4.4, revisión cruzada de la guardia |

---

## 7. Preguntas para el owner (Roger, Arturo)

Ordenadas por prioridad (las tres primeras condicionan el puntaje de impacto):

1. **KPI y línea base:** ¿qué KPI prioriza la Caja en Open Finance (conversión, retención, inclusión, conocimiento del cliente) y cuál es la línea base y su forma de medición?
2. **Sandbox y datos:** el expediente aclara que los datos son referenciales y no hay compromiso de entrega; por eso asumimos que **construimos nuestro propio sandbox**. ¿La Caja compartirá de todos modos algún esquema o dato simulado (columnas, volumen, entidades)? ¿Qué entidades y tipos de información multientidad espera ver?
3. **Marco regulatorio:** ¿qué marco de consentimiento debemos asumir (alcance, vigencia, finalidad, revocación)? ¿Existe una referencia normativa o de la propia Caja para el prototipo?
4. **Rol de la Caja:** ¿se espera solo recibir datos de otras entidades, o también publicar los propios (rol de proveedor)? Asumimos solo receptora.
5. **IA externa:** ¿se permite usar LLM externos con datos sintéticos? ¿Hay proveedores permitidos o prohibidos?
6. **Catálogo ofertable:** ¿qué productos de la Caja pueden ofertarse y con qué condiciones? Usamos un catálogo supuesto.
7. **Datos propios de la Caja:** ¿el uso de los datos de la propia Caja para ofertas requiere consentimiento específico?
8. **Conversión:** si el KPI es conversión, ¿qué tasa de aceptación referencial pueden compartir para el escenario?
9. **Evaluación del sandbox:** ¿el jurado valora la conformidad con algún estándar de APIs abiertas o basta un sandbox coherente?
10. **Apoyo:** ¿pueden Legal y Compliance revisar el texto de consentimiento antes del 03.12?
11. **Seguridad:** el expediente pide un intercambio «seguro»: ¿qué controles espera ver en el sandbox (autenticación de la entidad receptora, auditoría, cifrado, retención de registros)?

---

## 8. Preexistente vs. nuevo en el evento

| Componente | Estado | Titularidad | Nota |
|---|---|---|---|
| Generador de datos sintéticos `retos/NEG-02/datos/generar.py` y `test_generar.py` | **Preexistente** (21.11.2026) | Equipo | Herramienta general de datos; sin lógica de la solución |
| CSV generados en `retos/NEG-02/datos/sintetico/` | **Preexistente** | Equipo | Sintéticos; se pueden regenerar |
| Catálogo de productos y umbrales de las reglas | **Preexistente como supuesto** | Equipo | Son parámetros del generador; las reglas de oferta del producto se escriben en el evento |
| Documentación (concepto, panorama) | Preexistente | Equipo | |
| Cargador a SQLite (T1) | **Nuevo en el evento** | Equipo (cede si gana) | |
| Servicio de consentimiento y guardia (T2) | **Nuevo en el evento** | Equipo (cede si gana) | Funcionalidad crítica |
| APIs simuladas (T3) | **Nuevo en el evento** | Equipo (cede si gana) | Funcionalidad crítica |
| Vista 360 (T4) | **Nuevo en el evento** | Equipo (cede si gana) | Funcionalidad crítica |
| Motor de oportunidades con linaje (T5) | **Nuevo en el evento** | Equipo (cede si gana) | Funcionalidad crítica |
| Agente y proveedor de LLM (T6) | **Nuevo en el evento** | Equipo (cede si gana) | Funcionalidad crítica |
| Interfaz (T7, T8) | **Nuevo en el evento** | Equipo (cede si gana) | Con componentes de librerías abiertas |
| `evaluar_kpi.py`, pruebas del producto y `validacion.md` (T10, T11) | **Nuevo en el evento** | Equipo (cede si gana) | |
| Pitch y demo (T12) | **Nuevo en el evento** | Equipo | |
| FastAPI, Pydantic, pandas, scikit-learn, Pydantic AI, React, Vite, Tailwind, pytest | Librerías de terceros | Sus autores | Licencias abiertas |

**No se reutiliza código de empleadores ni de otros clientes.** Las ideas de guardia con aprobación humana vienen de experiencia previa, sin copiar código.

---

## 9. Plan de pruebas

### 9.1 Ya existen (generador, preexistente): 41 pruebas

`python -m pytest retos/NEG-02/datos -q` cubre: reproducibilidad por semilla y manifest con hashes; esquema y tipos contra la especificación; claves únicas e integridad referencial; ≥ 3 entidades fuente con clientes y ≥ 40 % de clientes en 2 o más entidades; coherencia de créditos con el catálogo (rangos, anualidad, saldo ≤ monto); calificación y mora; transacciones válidas; estado de consentimientos (vigente, vencido, revocado, bordes de fecha), renovaciones y auditoría; cobertura de columnas por alcance; consentimientos a otros receptores; **recálculo independiente de la verdad** (restricción, captación, consolidación, domiciliación); ausencia de datos personales y de nombres reales.

### 9.2 Por construir en el evento (producto)

| Nivel | Prueba | Resultado esperado |
|---|---|---|
| Guardia | Consentimiento vigente con alcance completo | Permite; devuelve solo columnas del alcance |
| Guardia | **Vencido** | Deniega `VENCIDO` |
| Guardia | **Revocado** (revocación anterior a `ahora`) | Deniega `REVOCADO`; efecto inmediato |
| Guardia | **Alcance insuficiente** (pide SALDOS, solo tiene PRODUCTOS) | Deniega `ALCANCE`; sin columnas de SALDOS |
| Guardia | **Finalidad «solo vista»** y se pide una oferta | Deniega `FINALIDAD` |
| Guardia | **Otro receptor** (consentimiento a otra entidad) | Deniega `RECEPTOR` |
| Guardia | **Ventana histórica** de 3 meses | Transacciones recortadas a 3 meses |
| Guardia | Vencido + renovación vigente | Permite por la renovación; el linaje cita la renovación |
| Guardia | Sin consentimiento | Deniega `SIN_CONSENTIMIENTO` |
| Seguridad | Consulta a las APIs **sin credencial** de receptor | 401; no se devuelve ningún dato |
| Seguridad | Credencial de una entidad usada para consultar como otra | 403; denegación auditada |
| Seguridad | Los registros de auditoría y los logs no contienen valores de campos ni datos personales | Cero hallazgos |
| Fuga (propiedad) | Para todos los clientes y combinaciones del dataset: toda columna de la salida pertenece a un alcance concedido y vigente | Cero violaciones |
| Fuga (e2e) | Ningún texto del agente cita un valor que no esté en la evidencia autorizada | Cero violaciones; si falla, cae a plantilla |
| Linaje | Toda oportunidad trae ≥ 1 evidencia con `consentimiento_id` vigente | 100 % |
| Motor | Casos de verdad conocidos (uno por tipo y los casos difíciles) | Coincide con la verdad en los casos sembrados |
| Motor | Sobreendeudado con deuda cara | Abstención; sin oferta de crédito |
| Motor | Prospecto sin consentimiento | «No evaluable»; sin oferta |
| Agente | Proveedor intercambiable (plantilla ↔ otro) | Mismo resultado estructurado |
| API | Contratos de cada ruta (códigos, esquemas, auditoría de denegaciones) | Pasa |
| e2e | Otorgar → consultar 3 entidades → vista 360 → oportunidad → revocar → la vista se reduce | Pasa |
| KPI | Reproducibilidad: misma semilla ⇒ mismas métricas | Idéntico |
| KPI | A ≤ B ≤ C en M1 (no puede ganar el brazo con menos datos) | Se cumple |
| KPI | M7 (prospectos) y M8 (ahorro potencial) se calculan solo con evidencia autorizada | Coincide con un cálculo manual en 3 casos |
| Humo de demo | Guion de 5 casos curados | Pasa antes de la entrega |

**Evidencia:** cada corrida de pruebas y del KPI se guarda en `docs/validacion.md` con fecha, semilla y hash del `manifest.json`.

---

## 10. Entrada para `docs/preexistente.md`

> No se ha modificado `docs/preexistente.md` (fuera del alcance de esta tarea). Texto a añadir en la tabla, cuando el coordinador lo decida:

```markdown
| `retos/NEG-02/datos/generar.py` y `test_generar.py` | Generador de datos sintéticos de un ecosistema abierto ficticio (entidades «Demo», clientes con productos en varias entidades, transacciones, catálogo, consentimientos con alcance/vigencia/revocación, verdad de terreno separada). Herramienta de datos; no contiene APIs, servicio de consentimiento, vista 360, motor de oportunidades, agente ni interfaz | Equipo | 21.11.2026 | No (preexistente) |
| `retos/NEG-02/datos/sintetico/` | CSV, diccionario y `manifest.json` producidos por el generador con semilla fija (100 % sintéticos; regenerables). La subcarpeta `verdad/` es solo para medición | Equipo | 21.11.2026 | No (preexistente) |
```

Declaración adicional sugerida: «Los parámetros de catálogo, tasas, umbrales y probabilidades del generador son supuestos del equipo; no provienen de la Caja ni de datos reales. La funcionalidad crítica de NEG-02 (APIs simuladas, servicio de consentimiento y guardia, vista 360, motor de oportunidades, agente e interfaz) se desarrolla durante la fase presencial».

---

## 11. Cotejo con el expediente

Comparación palabra por palabra de `retos/NEG-02/concepto.md` y de este panorama (versión 1) contra el texto literal de `retos/NEG-02/expediente.md` (actualizado por la Caja el 19.11, 06:58 p. m.). Cada desviación se corrigió en ambos archivos salvo donde se indica.

### 11.1 Desviaciones encontradas y corregidas

| # | Tipo | Qué decía nuestro texto | Qué dice el expediente | Corrección |
|---|---|---|---|---|
| 1 | **Restricción diluida** | «No asumir APIs ni datos reales» (resumen corto en concepto §1 y panorama §1.1) | «Sin asumir disponibilidad de datos reales ni APIs operativas»; los prototipos deben usar «datos sintéticos e integraciones simuladas» | Se reescribió con la formulación del expediente y su consecuencia: **el caso base es nuestro propio sandbox**; las APIs son simuladas; si la Caja entrega algo, se adapta |
| 2 | **Restricción diluida** | Solo «privacidad y consentimiento». «Autenticación real» figuraba como fuera de alcance y no había controles de seguridad | Pregunta de innovación: intercambio «**seguro** y autorizado». Riesgos: «privacidad, **seguridad** y uso autorizado» | Se añadió seguridad al concepto y al panorama (§3.3): credencial por entidad receptora, auditoría sin datos personales, secretos fuera del repo, LLM con evidencia mínima. Pruebas 401/403 en §9.2, riesgo R15 y pregunta 11 al owner. La autenticación de usuarios finales sigue fuera de alcance y así se dice |
| 3 | **Dicho y no cubierto** | Sin métrica ni función de **inclusión financiera** | Resultado esperado: «oportunidades de crecimiento e **inclusión financiera**» | Nueva métrica M7 (prospectos y segmentos) y el prospecto como protagonista de la demo; texto en concepto §3 |
| 4 | **Dicho y no cubierto** | El valor se planteaba casi solo del lado de la Caja | Pregunta de innovación: «mayor **valor para los clientes**»; «decisiones mejor informadas» | Se explicita el beneficio al cliente: vista financiera consolidada (finalidad «solo vista»), abstención que lo protege del sobreendeudamiento y métrica M8 (ahorro potencial de intereses en consolidaciones) |
| 5 | **Dicho y no cubierto** | Sin mención de «nuevas formas de colaboración entre actores del ecosistema» | Contexto: el intercambio facilitaría «nuevas formas de colaboración entre actores» | Se declara de forma explícita como **fuera de alcance** (la Caja solo como receptora; el rol de proveedora y la colaboración quedan como hoja de ruta de escalabilidad) y se pregunta al owner (pregunta 4) |
| 6 | **Dicho y no cubierto** | Se hablaba de «diferenciación» sin decir frente a qué | «Valor diferencial frente a soluciones convencionales» | Se nombra el comparador: la solución convencional es la oferta con datos propios de la Caja = **brazo A** del experimento |
| 7 | **Restricción diluida** | La «analítica predictiva» quedaba como **opcional** (modelo de propensión) y el núcleo eran reglas; riesgo de leerse como «automatización básica» | IA, agentes, analítica predictiva, optimización «cuando aporten valor real»; no bastan automatizaciones básicas | El **modelo de ingreso estimado** (scikit-learn, entrenado con el ingreso declarado) entra al mínimo viable (T4 +1.0 h; mínimo 28 h). Riesgo declarado: es lo primero que se pierde en el escenario pesimista (§4.4) |
| 8 | **Atribuido y no dicho** | Concepto §1: «un ecosistema donde otros también pueden ver al cliente completo» dentro del párrafo del problema | El expediente dice «ecosistema financiero cada vez más abierto» y «desafío competitivo»; no habla de que otros vean al cliente completo | Se reformuló con las palabras del expediente. La hipótesis de ofrecer crédito a quien ya está sobreendeudado queda como **(supuesto)** nuestro |
| 9 | **Dicho y no cubierto** | Se tomaba como posible que la Caja entregue datos o sandbox («si llegan, adaptador») | «Los datos son referenciales y no implican un compromiso de entrega» | Se recoge la nota literal; el sandbox propio es el caso base y la pregunta 2 se reformuló |
| 10 | **Título** | «Competir en un ecosistema abierto» | «Competir en un ecosistema **financiero** abierto» | Corregido en los títulos del concepto y del panorama |

### 11.2 Cobertura punto por punto

| Elemento del expediente | Dónde se cubre |
|---|---|
| Pregunta de innovación (seguro, autorizado, valor para clientes, competitividad) | Concepto §1–§2; M7, M8; §3.3 |
| Visión integral de comportamiento, necesidades y oportunidades | Vista 360 y motor de oportunidades (§3.4) |
| Experiencias personalizadas y decisiones mejor informadas | Ofertas con evidencia, vista «solo vista», agente que explica |
| Resultado esperado: conocimiento del cliente, personalización, oportunidades, inclusión | M3 (completitud), M1, M2, M7 |
| Insumos: APIs simuladas, transacciones, multientidad, perfiles, catálogo, consentimientos simulados, sintéticos | §2 completo y §3.2; sin carencias |
| Datos referenciales sin compromiso de entrega | §1.1 y pregunta 2 |
| Privacidad y uso autorizado | Guardia (§3.3), prueba de fuga (§9.2) |
| Seguridad | §3.3, R15, §9.2 |
| Normativa aplicable | R3 y pregunta 3; ver aclaración abajo |
| Datos sintéticos e integraciones simuladas, sin datos reales ni APIs operativas | §2.1, concepto §2 y §5 |
| IA, agentes, analítica predictiva, no solo chatbot, dashboard o formulario | Modelo de ingreso, agente con verificación, guardia, KPI (concepto §4) |
| Desarrollo funcional, integración tecnológica y valor diferencial | Funcionalidad crítica (concepto §6), brazo A como comparador |
| Colaboración entre actores del ecosistema | **Fuera de alcance**, declarado |

### 11.3 Aclaración sobre la normativa de consentimiento

El expediente habla de «las condiciones regulatorias aplicables» y de «la normativa aplicable» **sin nombrar ninguna norma ni exigir un modelo de consentimiento concreto**. Todo lo que decimos sobre alcance, vigencia, finalidad y revocación es **diseño nuestro**, inspirado en los principios generales de consentimiento informado y finalidad; las referencias a la ley de protección de datos personales y al secreto bancario (R3) son conocimiento general nuestro, **a verificar con Legal**, y **no** provienen del expediente. Por eso: (1) el prototipo «respeta los principios», sin afirmar cumplimiento; (2) el texto de consentimiento y el marco a asumir son preguntas abiertas (preguntas 3 y 10); (3) no se afirma que exista, ni que no exista, un marco específico de Open Finance en el país.

### 11.4 Lo que no se corrigió a propósito

- El generador y el catálogo incluyen la categoría `SEGURO` (producto financiero): no tiene relación con la «seguridad» del expediente.
- Las métricas M6 (conversión) y la tasa de consentimiento siguen siendo parámetros supuestos, porque el expediente no da KPI ni línea base.
