# Panorama de abastecimiento — RIE-02 · Descubrir redes de riesgo ocultas

> Documento de trabajo (v2, 21.11.2026) · Pareja líder David + Mariano · Revisor: Antonio.
> Material confidencial: repo privado. **Todo lo que no viene del expediente va marcado como (supuesto) o [POR CONFIRMAR].** El expediente literal está en `retos/RIE-02/expediente.md`.
> No contiene cifras de KPI, línea base ni impacto: no existen datos oficiales para ellas.
> El detector, la priorización, el agente y la interfaz **no se construyen antes del 03.12** (bases: la funcionalidad crítica se desarrolla en la fase presencial). Lo único construido hasta hoy es el generador de datos y su documentación.

Estado del dataset: **generado y probado.** `python -m pytest retos/RIE-02/datos -q` → 37 pruebas pasan. Salida en `retos/RIE-02/datos/sintetico/`.

---

## Alcance MVP en una página

**Entra (lo que se construye el 03–04.12):**

1. Carga de un lote de CSV con el esquema de b.3 (≈ 3,700 solicitudes) por línea de comandos o API.
2. Grafo tipado de personas, negocios, teléfonos, dispositivos, direcciones y referencias, con peso por rareza del dato y capacidad del inmueble o dispositivo.
3. Comunidades e indicadores de red, con **regla de corroboración**: una red solo entra a la cola si combina señales de **estructura** (relaciones) y de **comportamiento o perfil** (ráfaga, montos, antigüedad). Las relaciones solas nunca bastan.
4. Cola priorizada con puntaje y razones a favor y en contra, incluidos los factores legítimos.
5. Expediente por red con citas a filas que existen, explicaciones alternativas y qué verificar; verificador de citas; plantilla sin LLM como valor por defecto.
6. Vista del especialista: cola, grafo, ficha de evidencia y tres acciones con motivo obligatorio: **Escalar a investigación, Pedir verificación preventiva, Descartar como legítima.**
7. Decisión registrada en SQLite; el sistema **no modifica solicitudes ni notifica a clientes**.
8. Backtest contra reglas simples (R1, R2) y una regla con criterio de dominio (R4), en `dev` y `eval`.

**Queda fuera:** integración con sistemas reales de la Caja; bloqueo, rechazo o notificación a clientes; resolución de entidades (se asume hecha); conexiones y geolocalización (IP, coordenadas), que el dataset no trae; tiempo real o *streaming*; reentrenamiento en línea; autenticación real y multiusuario; app móvil; reportes regulatorios; cualquier dato real.

**Núcleo no recortable (piso del 3/5):** ETL y grafo con pesos · comunidades con regla de corroboración · priorización por reglas ponderadas con razones · expediente por plantilla con citas verificadas · cola, ficha y decisión registrada · backtest R1/R2/R4 que incluya los señuelos.

**Opcional, en orden de sacrificio:** Louvain → componentes podados · modelo de scikit-learn → reglas ponderadas · agente LLM con herramientas → plantilla (el LLM solo redacta) · grafo interactivo → SVG estático servido por la API · filtros, línea de tiempo y métricas dentro de la UI → pantalla fija de métricas · ablaciones y semillas ciegas múltiples → una sola evaluación · patrón sorpresa · medición de detección temprana · tiempo de caso.

**Criterio de terminado (todo verificable):**

- Un comando levanta API e interfaz y carga el lote en menos de un minuto.
- En `eval`, la solución supera a R1 y R2 en precisión **al mismo recall**, y reporta también R4. El umbral de aceptación lo fija el equipo el Día 1, tras ver R1, R2 y R4, y se registra antes de mirar `eval`.
- Los señuelos `familia`, `mercado` y `tableta_agencia` no ocupan la cola prioritaria, o aparecen con su razón legítima visible.
- Todo expediente cita solo filas que existen y ninguno contiene frases de conclusión (prueba automática).
- Cada decisión queda registrada con motivo.
- `scripts/evaluar_kpi.py` reproduce las métricas con la misma semilla y `docs/validacion.md` trae el antes/después.
- Pruebas verdes e historial git del evento.

**Guion de demo (5 min), termina con el antes/después:**

| Tiempo | Qué se muestra |
|---|---|
| 0:00–0:30 | El problema en una frase: la red invisible y el riesgo de acusar a clientes legítimos |
| 0:30–1:15 | Se carga el lote; aparece la cola priorizada |
| 1:15–2:15 | Una red encadenada que R1 y R2 no verían: grafo, expediente con citas y explicaciones alternativas |
| 2:15–3:00 | Un señuelo (familia o mercado) con el mismo dato compartido: baja prioridad y razón legítima visible |
| 3:00–3:45 | El especialista decide con motivo (Escalar o Pedir verificación); queda registrado; el cliente no recibe nada |
| 3:45–4:45 | **Antes/después:** reglas simples (R1, R2, R4) frente a la solución en la evaluación ciega: precisión de redes, recall, falsos positivos sobre señuelos y carga de revisión. **Valores medidos el Día 2; no se inventan antes** |
| 4:45–5:00 | Límites (datos sintéticos) y siguiente paso con datos de la Caja |

---

## (a) Qué necesita el desafío

Pregunta del expediente: identificar patrones de relaciones inusuales entre personas, negocios y solicitudes de crédito que permitan **anticipar** posibles riesgos de fraude y orientar acciones de **prevención e investigación**. Resultado esperado: prevención y detección temprana, **priorizar investigaciones, reducir falsos positivos** y orientar decisiones de riesgo sustentadas en evidencia. Riesgos: respetar la protección de datos personales, **evitar conclusiones automáticas de fraude basadas únicamente en relaciones o coincidencias**, sustentar las alertas en evidencia verificable, considerar falsos positivos y **facilitar la revisión humana antes de tomar decisiones que afecten a los clientes**. Detalle y cotejo literal: sección «Cotejo con el expediente».

| Necesidad | Qué es | Quién lo aporta | Estado hoy |
|---|---|---|---|
| Lote de solicitudes con sus atributos de contacto | Solicitudes MYPE con solicitante, negocio, teléfono, dispositivo, domicilio, referencias | La Caja (datos «referenciales», sin compromiso de entrega) **[POR CONFIRMAR]**; si no llegan, nuestro generador | **Hecho** (generador propio, 3,701 solicitudes) |
| Redes de fraude con verdad de terreno | Redes inyectadas y etiquetadas para medir precisión y recall («casos simulados» en el expediente) | La Caja **[POR CONFIRMAR]** / generador | **Hecho** (30 redes, 5 patrones) |
| Relaciones legítimas «señuelo» | Familias, mercados, tabletas de agencia, gremios, gestores: comparten datos sin ser fraude | Generador (la Caja difícilmente las etiquete) | **Hecho** (93 redes, 6 tipos) |
| Construcción del grafo | Nodos y aristas tipadas, con peso por rareza del dato compartido | Construir en el evento (pandas + networkx) | Evento |
| Detección de comunidades y anomalías | Componentes/Louvain + indicadores de red (ciclos, ráfaga temporal, exceso de capacidad del inmueble…) | Evento (networkx, scikit-learn) | Evento |
| Priorización de casos | Puntaje por red con razones por factor y regla de corroboración | Evento | Evento |
| Agente de expediente de evidencia | Resume la red con citas a filas reales, propone explicaciones alternativas legítimas, no concluye fraude | Evento (Pydantic AI + proveedor LLM intercambiable) | Evento |
| Visualización y acciones | Cola de casos, grafo, ficha de evidencia, acciones de prevención e investigación con decisión humana registrada | Evento (React + Vite + Tailwind + Cytoscape.js) | Evento |
| Medición | Precisión/recall de redes, falsos positivos frente a reglas simples, calidad de la cola | Evento (`scripts/evaluar_kpi.py`) | Evento |
| Criterios de dominio | Qué vínculos pesan más, cuándo una familia o un mercado es normal, umbral de revisión | Caja Experts / owner **[POR CONFIRMAR]** | Pendiente |
| Política de IA externa y de datos | Si se puede usar LLM en la nube, qué datos se pueden enviar | Owner / Legal **[POR CONFIRMAR]** | Pendiente (diseño tolerante: proveedor intercambiable y seudonimización) |
| Conexiones (IP, sesión) y ubicaciones (coordenadas) | El expediente lista «dispositivos y conexiones» y «direcciones y ubicaciones» | La Caja **[POR CONFIRMAR]** | **No cubierto por el dataset**; se agregaría como nuevo tipo de vínculo vía el adaptador ETL |

---

## (b) Cómo abastecerlo: dataset sintético de solicitudes y su grafo

### b.1 Principios

- **Reproducible:** misma semilla y escala ⇒ archivos idénticos byte a byte (probado). Semilla por defecto **2026**. Parámetro `--escala` multiplica los volúmenes.
- **100 % ficticio:** documentos `FIC-########`, teléfonos `FIC-#########`, huellas de dispositivo derivadas de un hash; nombres compuestos al azar de listas genéricas; agencias, mercados y calles genéricos de La Libertad (no son los de la Caja). Montos en S/ plausibles para MYPE (rango S/ 1,000–80,000). Sin red, sin datos reales.
- **Las tablas de entrada no contienen etiquetas** (probado): la verdad va en `redes_verdad.csv` y `etiquetas_solicitudes.csv`. Los ids se barajan al final, así el orden de creación no delata las redes (probado).
- **Medir falsos positivos es la mitad del diseño:** por cada patrón de fraude hay señuelos que se le parecen en la superficie.
- **No es trivial** (probado, ver b.8): ninguna regla simple llega al 100 %.
- Es un **generador propio y general**, no el detector: se declara como preexistente (sección j).

### b.2 Cómo ejecutarlo

```powershell
python retos/RIE-02/datos/generar.py --semilla 2026 --escala 1.0
python -m pytest retos/RIE-02/datos -q
```

Opciones: `--salida RUTA` (por defecto `retos/RIE-02/datos/sintetico`). Con `--escala 2` se duplican redes y solicitudes (más redes de evaluación → intervalos de confianza más estrechos). Tiempo: ~3 s la generación; ~20 s las pruebas.

### b.3 Tablas, columnas y volúmenes (semilla 2026, escala 1.0)

Convención: ids con prefijo y 6 dígitos (`S000001`). Texto vacío = ausente. UTF-8, separador coma. Fechas ISO `AAAA-MM-DD`.

**Entrada del detector** (lo que vería el sistema):

| Archivo | Filas | Columnas (tipo) |
|---|---|---|
| `solicitudes.csv` | 3,701 | `solicitud_id` (S), `fecha_solicitud` (fecha), `agencia_id`, `analista_id`, `canal` {agencia, promotor_tableta, app_movil}, `producto`, `monto_solicitado_pen` (S/, decimal), `plazo_meses` (int), `ingreso_mensual_declarado_pen` (S/), `solicitante_id` (→personas), `negocio_id` (→negocios), `telefono_id` (→telefonos), `dispositivo_id` (→dispositivos; vacío en canal agencia), `direccion_domicilio_id` (→direcciones) |
| `personas.csv` | 9,920 | `persona_id` (P), `documento_ficticio`, `nombres`, `apellido_paterno`, `apellido_materno`, `edad_anios`, `distrito_residencia`, `meses_como_cliente`, `creditos_previos`. Incluye solicitantes **y** personas de referencia |
| `negocios.csv` | 3,556 | `negocio_id` (N), `nombre_negocio`, `rubro`, `propietario_id` (→personas), `direccion_id` (→direcciones, el local), `puesto`, `antiguedad_meses` |
| `direcciones.csv` | 6,508 | `direccion_id` (D), `texto_direccion`, `distrito`, `provincia`, `tipo_inmueble` {vivienda, vivienda_multifamiliar, local_comercial, puesto_mercado, oficina_compartida}, `hogares_esperados` (int; capacidad normal del inmueble), `mercado` (nombre si aplica) |
| `telefonos.csv` | 9,875 | `telefono_id` (T), `numero_ficticio`, `tipo_linea` {movil_prepago, movil_postpago}, `antiguedad_linea_meses` |
| `dispositivos.csv` | 1,120 | `dispositivo_id` (V), `huella_ficticia`, `tipo_dispositivo` {smartphone_android, smartphone_ios, tableta_agencia}, `agencia_id` (solo tabletas) |
| `referencias.csv` | 7,401 | `referencia_id` (R), `solicitud_id` (→solicitudes), `persona_referencia_id` (→personas), `relacion` {familiar, vecino, proveedor, cliente, amigo, socio_gremial, asesor_contable}, `telefono_referencia_id` (→telefonos; el «contacto» de la referencia) |
| `agencias.csv` | 10 | `agencia_id`, `nombre_agencia`, `distrito`, `provincia` |

**Verdad de terreno** (solo para medir):

| Archivo | Filas | Columnas |
|---|---|---|
| `redes_verdad.csv` | 123 | `red_id` (RF… fraude / RL… señuelo), `clase` {fraude, legitima_senuelo}, `patron`, `dificultad` {baja, media, alta}, `particion` {dev, eval}, `n_solicitudes`, `n_personas`, `fecha_inicio`, `fecha_fin`, `vinculos_clave` (texto) |
| `etiquetas_solicitudes.csv` | 3,701 | `solicitud_id`, `etiqueta` {fraude, legitima_senuelo, normal}, `red_id` (vacío si normal), `rol`, `particion` {dev, eval} |

`manifest.json` guarda semilla, escala, versión de esquema, conteos y el umbral supuesto.

### b.4 El grafo implícito

El detector construirá el grafo; nosotros solo entregamos las tablas. Relaciones que contienen los datos (los «teléfonos, dispositivos, direcciones, referencias, contactos o negocios» del expediente):

| Vínculo entre solicitudes | Origen |
|---|---|
| Misma persona | `solicitante_id` (renovaciones legítimas) |
| Mismo teléfono | `telefono_id` |
| Mismo contacto de referencia | `persona_referencia_id` y `telefono_referencia_id` (una referencia puede ser a su vez solicitante: **aval cruzado**) |
| Mismo dispositivo | `dispositivo_id` |
| Mismo domicilio | `direccion_domicilio_id` |
| Mismo negocio o local | `negocios.direccion_id` (local compartido) y `rubro` |
| Parentesco aparente | mismo apellido paterno + mismo domicilio (factor de **exoneración**, no de sospecha) |

### b.5 Redes de fraude inyectadas (30; 6 por patrón; 2 de cada dificultad)

Señales de perfil **probabilísticas**, no deterministas: 70 % de los solicitantes de fraude son clientes nuevos (frente a 45 % en el fondo normal), negocios y líneas recientes con frecuencia pero no siempre, ingreso declarado redondeado a S/ 500 con más frecuencia. **La dificultad también dilata la ventana temporal:** mediana de 14 días en dificultad baja, ~30 en media y ~60 en alta. Algunos miembros «se pegan» a lo legítimo a propósito: pasan por la tableta de la agencia, tienen puesto en un mercado o citan a un proveedor común.

| Patrón | Qué simula | Tamaño | Cómo se esconde (dificultad) |
|---|---|---|---|
| `anillo` | Solicitantes que se avalan en círculo (A→B→C→…→A) con negocios y líneas nuevos; montos parecidos | 5–8 | Baja: además comparten un local y un dispositivo, 14 días. Media: un vínculo extra, 45 días. Alta: solo las referencias circulares, 90 días |
| `estrella` | Un contacto (cabecilla) que figura como referencia de muchos testaferros; a veces también solicita | 6–12 | Baja: además todos usan su dispositivo, 20 días. Media: la mitad, 50 días. Alta: solo la referencia común, 90 días |
| `dispositivo_compartido` | Un mismo celular envía solicitudes de identidades distintas, cada una con su teléfono y domicilio | 5–10 | Baja: ≤ 5 días y montos entre 90–100 % del umbral supuesto. Media: ≤ 20 días, 60 % estructurados. Alta: ≤ 45 días y sin estructuración |
| `direccion_fantasma` | Muchos solicitantes sin relación declaran el mismo inmueble de 1 hogar (o una oficina compartida) | 4–9 | Baja: domicilio y local iguales, 25 días. Media: solo el domicilio, 60 días. Alta: local en oficina compartida (se parece a un coworking legítimo), 100 días |
| `evasiva_debil` | Cadena de vínculos débiles de **tipos distintos** (teléfono, domicilio, referencia, dispositivo, local); ningún dato conecta a más de 2 miembros | 4–6 | Siempre vínculos débiles; la dificultad solo ensancha la ventana (28, 60 o 100 días). Cada vínculo aislado es indistinguible de una coincidencia casual |

### b.6 Señuelos legítimos (93 redes, 700 solicitudes)

Los señuelos **también llegan en ráfaga** (hogares que piden juntos, campañas en un mercado) y algunos son clientes nuevos: así el tiempo y el perfil por sí solos no separan nada.

| Señuelo | Qué simula | Por qué engaña a una regla simple | Qué lo distingue (pistas que el sistema debe aprender) |
|---|---|---|---|
| `familia` (25) | Hogar con mismo domicilio, teléfono compartido y referencias familiares mutuas; 1 de cada 4 es «extendida» (cuñados, compadres: sin apellido común) | Dato compartido + referencias cruzadas; la mitad pide en menos de 2 semanas | Apellido paterno común (salvo las extendidas), relación «familiar», inmueble de 1 hogar con vínculo de parentesco |
| `mercado` (6) | Puestos del mismo mercado que se avalan como vecinos; 4 de cada 10 grupos son de comerciantes nuevos | Mismo local, referencias cruzadas; la mitad llega en una campaña de ≤ 30 días | Inmueble tipo `puesto_mercado` con alta capacidad; rubro de mercado |
| `tableta_agencia` (10, una por agencia; hasta ~100 solicitudes) | Tableta de agencia usada por el promotor; la mitad de los usos ocurre en «jornadas de campo» de 1–2 días | El mismo dispositivo en decenas de personas y ráfagas parecidas a `dispositivo_compartido` | `tipo_dispositivo = tableta_agencia`, `canal = promotor_tableta` |
| `asociacion_gremial` (6) | Socios de un gremio con avales cruzados en cadena | Se parece al `anillo` | Negocios de más de 24 meses, clientes de larga data (en parte) |
| `gestor_contador` (6) | Un contador figura como contacto de 6–12 clientes | Se parece a la `estrella` | Relación «asesor_contable», negocios antiguos |
| `coincidencia_casual` (40) | Dos solicitudes sin relación que comparten un único dato (teléfono, dispositivo, referencia o domicilio multifamiliar) | Un solo vínculo | Ningún otro vínculo; ≥ 55 días de diferencia |

Además, **el fondo normal** (2,783 solicitudes) contiene ruido legítimo que también produce falsos positivos: renovaciones de la misma persona (≈ 200, con sus mismos datos), proveedores comunes citados como referencia por hasta 10 solicitantes y comerciantes de mercado que comparten dirección. Los hubs legítimos y los puentes hacen que se forme **un componente gigante** de ≈ 1,100 solicitudes: las redes de fraude no quedan aisladas.

### b.7 Volúmenes y etiquetas (escala 1.0)

| Concepto | Valor |
|---|---|
| Solicitudes | 3,701 (fraude 218 = 5.9 %; señuelo 700; normal 2,783) |
| Rango de fechas | 2025-10-01 a 2026-09-30 (sin domingos) |
| Redes de fraude / señuelo | 30 / 93 |
| Partición | por red, alternada por patrón: fraude 15 dev + 15 eval; señuelo 47 dev + 46 eval; las normales al azar 50/50 |

La prevalencia de fraude (≈ 6 %) es **deliberadamente alta** para tener redes suficientes en 8 horas; no representa la tasa real de la Caja, que desconocemos. **[POR CONFIRMAR con el owner.]**

### b.8 Verificación de honestidad: el backtest no es trivial

Prueba pedida: que un detector simple por reglas no llegue al 100 %. Se probaron cuatro reglas de control sobre las tablas de entrada (`test_generar.py` las ejecuta; **no son el detector**, no se reutilizan en el producto):

| Regla de control | Qué hace | Resultado (semilla 2026) | Otras semillas (9001–9003) |
|---|---|---|---|
| R1 | Dato (teléfono, dispositivo, domicilio o local) compartido por ≥ 2 personas | marca 1,101; precisión 16 %, recall 81 %, F1 0.27; 581 señuelos y 344 normales marcados | F1 0.24–0.26 |
| R2 | Igual, por ≥ 3 personas | marca 987; precisión 14 %, recall 62 %, F1 0.23 | F1 0.21–0.22 |
| Componente + ráfaga (ingenua) | Componente conexo de ≥ 3–5 solicitudes que cabe en 14–90 días; se toma la mejor combinación | mejor F1 **0.55** | mejor F1 0.35–0.45 |
| R4 (con criterio de dominio) | Ignora tabletas y puestos de mercado, descarta entidades con más de 12 usuarios, exige componente ≥ 4, ventana ≤ 90 días y ≥ 40 % de clientes nuevos | precisión 94 %, recall 89 %, **F1 0.91** | F1 0.88–0.92 |

Lecturas honestas:

- **No es trivial:** ninguna regla llega al 100 % y las reglas de coincidencia (R1, R2) inundan con falsos positivos. Antes de agregar los puentes, las ráfagas de señuelos y los perfiles traslapados, una regla de dos parámetros daba F1 = 1.0: **se detectó, se endureció el generador y se agregaron pruebas** (la regla ingenua debe quedar bajo F1 0.7, R4 bajo 0.97 y por encima de 0.6).
- **R4 es una línea comparativa fuerte.** Con conocimiento de dominio y umbrales ajustados por nosotros viendo estas semillas, una regla alcanza F1 ≈ 0.9: el aporte de la solución frente a R4 será **moderado**, y la medición debe reportarla. R4 detecta (≥ 50 % de los miembros) el 92 % de las redes de dificultad baja, el 98 % de media y el 80 % de alta (4 semillas); su punto débil es `direccion_fantasma` de dificultad alta (25 %: oficina compartida y ventana de 100 días). Los argumentos adicionales son la explicación por red, la regla de corroboración, el expediente y la robustez ante ese tipo de caso; **no** una ventaja amplia en recall.
- Estas cifras describen **nuestro dataset**; **no** son la línea base de la Caja ni se citarán como tal.

### b.9 Límites y sesgos del dataset (decirlo en el pitch)

- Los patrones de fraude los diseñamos nosotros: un buen recall sobre ellos **no prueba** que el método detecte fraude real. Mitigación: patrón sorpresa y semillas ciegas (sección e).
- **Brechas frente a los insumos del expediente:** no hay conexiones (IP, sesión), ubicaciones geográficas ni series de comportamiento (horarios, velocidad de llenado). «Patrones de comportamiento» se cubre solo con ráfagas temporales, montos y perfil. **[POR CONFIRMAR qué entregará la Caja.]**
- `hogares_esperados`, `meses_como_cliente`, antigüedad de líneas y `dispositivo_id` son datos que **suponemos** disponibles. **[POR CONFIRMAR]**
- Se asume resolución de entidades hecha (direcciones y teléfonos ya normalizados a un id). En la realidad, `Jr. Grau 120` y `Jirón Grau N° 120` son el mismo inmueble. **[POR CONFIRMAR]**
- No hay mora, pagos ni desembolsos: RIE-02 es de originación.
- El umbral de revisión de S/ 10,000 es un **supuesto** nuestro. **[POR CONFIRMAR]**
- Las señales «nuevo cliente» o «línea reciente» pueden discriminar a personas con poca bancarización: el sistema las usa solo como apoyo a una red ya formada, nunca como alerta individual.

### b.10 Si la Caja entrega datos

Se escribe un adaptador `app/etl/` que mapee sus columnas a las tablas anteriores (y agregue vínculos nuevos, como IP o ubicación, si los trae); el generador se mantiene para pruebas y para las redes etiquetadas que falten. Los datos de la Caja no se suben a repos públicos.

---

## (c) Arquitectura

```
CSV / API de lote ──► ETL ──► Grafo tipado ──► Comunidades ──► Indicadores ──► Corroboración ──► Priorización ──► Cola
                                  ▲                                                                   │            │
                    pesos por rareza y capacidad                                              razones por factor   Agente de expediente
                                                                                                                    │
                                         Vista del especialista ◄── API FastAPI ◄── Expediente con citas verificadas
                                                    │
                                    Decisión humana (SQLite, auditable)
```

1. **ETL (pandas).** Lee las tablas, valida llaves, normaliza y arma las entidades. Entrada: carpeta de CSV o lote por API.
2. **Grafo tipado (networkx).** Nodos: solicitud, persona, negocio, teléfono, dispositivo, dirección. Aristas tipadas (usa_teléfono, usa_dispositivo, domicilio_en, local_en, referencia_a, contacto_de_referencia). Proyección a un **grafo de solicitudes**: dos solicitudes se unen si comparten una entidad; el **peso** cae con la rareza (más personas usan el dato, menos pesa) y con la **capacidad esperada** (`hogares_esperados`, mercado, tableta). Un dispositivo propio compartido por 5 identidades pesa mucho; una tableta de agencia o un puesto de mercado casi nada. Con el componente gigante del dataset, **podar y ponderar es obligatorio**.
3. **Comunidades.** Podar vínculos de peso bajo → componentes conexos → Louvain dentro de componentes grandes. Para cadenas de vínculos débiles, puntuar **trayectorias** de ≥ 3 vínculos de tipos distintos.
4. **Indicadores por red.** Estructura: tamaño, personas distintas, tipos de vínculo distintos, ciclo dirigido de referencias, exceso de personas sobre la capacidad del inmueble. Comportamiento y perfil: ventana temporal, proporción de clientes nuevos, antigüedad mediana de negocio y línea, montos cercanos al umbral (supuesto). **Factores legítimos:** parentesco aparente (apellido + domicilio), inmueble tipo mercado, dispositivo de tableta, gestor con negocios antiguos y solicitudes espaciadas.
5. **Regla de corroboración.** Una red **solo se prioriza si combina al menos dos familias de señales**: (i) estructura de relaciones y (ii) comportamiento o perfil. Una familia, un mercado o un gremio tienen estructura pero no comportamiento anómalo: no suben. Esto responde a «evitar conclusiones automáticas de fraude basadas únicamente en relaciones o coincidencias»; se mide con una ablación (con y sin la regla).
6. **Priorización.** Puntaje 0–100 por red = combinación calibrada de indicadores (empezar con **reglas ponderadas** como piso explicable; si da tiempo, modelo ligero de scikit-learn —regresión logística o gradient boosting— entrenado **solo en la partición dev**). Salida: puntaje, **contribución de cada factor** (a favor y en contra) y la acción sugerida entre **verificación preventiva** o **escalar a investigación**. Nunca emite decisión sobre el cliente.
7. **Agente de expediente (Pydantic AI).** Herramientas **solo de lectura y deterministas**: `obtener_red`, `listar_vinculos`, `comparar_con_patrones_legitimos`, `historial_de_entidad`. Salida estructurada `ExpedienteEvidencia`: resumen; hechos verificables **con ids de filas citadas**; vínculos fuertes frente a débiles; **explicaciones alternativas legítimas**; qué verificar para confirmar o descartar; nivel de confianza; y una línea fija: *«Este expediente no concluye fraude; la decisión es del especialista.»* Un **verificador determinista** rechaza cualquier cita inexistente y cualquier frase de conclusión («es fraude», «cometió»). Si falla, el sistema usa la **plantilla sin LLM**.
8. **Vista del especialista (React + Vite + Tailwind + Cytoscape.js).** Cola priorizada; grafo con nodos por tipo y vínculos por grosor; panel de evidencia con las citas; acciones **Escalar a investigación / Pedir verificación preventiva / Descartar (legítima)** con motivo obligatorio. Cada decisión se guarda en SQLite con fecha y usuario ficticio. **El sistema no cambia el estado de la solicitud ni notifica al cliente.**
9. **API (FastAPI + Pydantic v2).** `GET /redes`, `GET /redes/{id}`, `GET /redes/{id}/expediente`, `POST /redes/{id}/decision`, `GET /metricas`.
10. **Proveedor de LLM intercambiable (`app/llm/provider.py`).** Interfaz mínima, a construir en el evento (≈ 30 líneas):

```python
class ProveedorLLM(Protocol):
    nombre: str
    def generar(self, instrucciones: str, entrada: BaseModel, salida: type[T]) -> T: ...
```

Implementaciones: `ClaudeProvider`, `OpenAIProvider`, `LocalProvider` (Ollama u otro modelo local) y `PlantillaProvider` (determinista, sin red; valor por defecto y respaldo). Se elige con `LLM_PROVIDER`. Al LLM solo se envían **ids y atributos seudonimizados** (sin nombres ni documentos), y solo si el owner lo permite **[POR CONFIRMAR]**.

---

## (d) Plan hora a hora del evento (4 personas, ~8 h de construcción por persona)

Agenda oficial: Día 1 — validación del enfoque 09:45, construcción 10:30–13:00 y 14:00–16:30, pruebas 16:30–17:30. Día 2 — construcción 09:30–12:00, validación final 12:00–12:45, **entrega 13:00**, pitch 15:00. Tiempo real de construcción ≈ 7.5 h + 1 h de pruebas por persona (≈ 30 h + 4 h). Roles según CLAUDE.md: **M** Mariano (backend, IA), **G** Glem (datos, modelo), **A** Antonio (KPI, dominio), **D** David (UX, interfaz).

**Antes (01.12, inmersión):** correr el generador, repartir el repo base, confirmar entorno (Python 3.11, Node), ensayo de 20 min de la agenda. Sin código de la funcionalidad crítica.

| Bloque | M | G | A | D |
|---|---|---|---|---|
| **D1 09:00–10:30** Arranque y validación del enfoque | Repo base, FastAPI vacío, `generar.py --semilla 2026`, `docs/preexistente.md` actualizado. **Contrato JSON de `/redes` y `/expediente` con un archivo de ejemplo (30 min)** | Cargar CSV, revisar datos | Criterios de revisión y factores legítimos con Caja Experts; definir qué cuenta como «alerta correcta» | Wireframe de la vista (45 min); **arranca contra el JSON de ejemplo, sin esperar al backend** |
| **D1 10:30–13:00** Construcción 1 | Constructor del grafo tipado y pesos (tarea 1) | Comunidades e indicadores (tarea 2) | Esqueleto de `evaluar_kpi.py`: coincidencia red–alerta, reglas R1, R2, R4 (tarea 8) | Estructura React: cola de casos y ficha con datos de ejemplo (tarea 6) |
| **D1 13:00** | **Hito H1 (puerta de decisión):** grafo construido y comunidades listadas por línea de comandos; **la UI muestra el JSON de ejemplo**. Si la UI no renderiza un grafo, se activa el respaldo: SVG estático servido por la API | | | |
| **D1 14:00–16:30** Construcción 2 | Proveedor LLM + plantilla de expediente y verificador (tarea 5) | Priorización con corroboración y razones, ajuste en dev (tarea 3); API y SQLite (tarea 4) | Backtest sobre dev, plantilla de `docs/validacion.md` | Grafo Cytoscape conectado a la API; panel de evidencia (tarea 6). **Glem pareja 1 h en la conexión API–UI** |
| **D1 16:30–17:30** Pruebas | Pruebas del grafo y de la API | Pruebas de señuelos (familia, mercado, tableta no alertan) | Revisión de resultados y falsos positivos | Prueba de usabilidad de 15 min con un mentor |
| **D1 17:30** | **Hito H2:** punta a punta con una red de demo (lote → ranking → grafo → decisión). Etiqueta `hito-e2e` | | | |
| **D2 09:30–12:00** Construcción 3 | Agente con herramientas encima de la plantilla, solo si H2 se cumplió (tarea 5) | Reducir falsos positivos; **congelar umbrales con dev**; ablaciones | Backtest final en eval con intervalos de confianza; cifras antes/después en `docs/validacion.md` (tareas 8–9); **pantalla de métricas** | Botones de decisión, pulido; guion de demo (tareas 6, 10) |
| **D2 11:15** | **Congelamiento de funcionalidades** (solo correcciones) | | | |
| **D2 12:00–12:45** Validación final | Ensayo completo de la demo; correr todas las pruebas | Reproducir métricas con semilla ciega | Revisar `validacion.md` y lista de entrega | Cronometrar la demo (≤ 5 min) |
| **D2 13:00** | **Entrega:** etiqueta `entrega`, README, preexistente vs nuevo, historial git | | | |
| **D2 15:00** Pitch | Responde preguntas técnicas | Responde preguntas de datos | Narra impacto, KPI y límites | Conduce la demo |

### d.1 Horas de construcción y prueba pesimista

Plan base (estimación nuestra, **supuesto**) y escenario pesimista: cada tarea ×1.4; la vista del investigador con grafo interactivo (tarea 6) y el agente (tarea 5) ×1.6. El «piso» es el MVP del 3/5 con los cinco recortes activados.

| # | Tarea | Base | Pesimista | Piso (recortado, pesimista) |
|---|---|---|---|---|
| 1 | Carga de lote y constructor del grafo tipado | 3 | 4.2 | 4.2 |
| 2 | Comunidades e indicadores de red (+ corroboración) | 3 | 4.2 | 3.2 (sin Louvain) |
| 3 | Priorización y razones | 2.5 | 3.5 | 2.1 (solo reglas ponderadas) |
| 4 | API FastAPI + SQLite | 2 | 2.8 | 2.8 |
| 5 | Expediente: agente + verificador + proveedor LLM | 4 | 6.4 | 2.9 (plantilla + verificador; LLM opcional) |
| 6 | Vista del especialista y grafo interactivo | 5.5 | 8.8 | 5.6 (cola + ficha + botones; grafo SVG o básico) |
| 7 | Reglas y criterios de revisión | 1 | 1.4 | 1.4 |
| 8 | Backtest y KPI | 3.5 | 4.9 | 3.5 (una sola evaluación) |
| 9 | Pruebas, falsos positivos y validación | 2.5 | 3.5 | 2.8 |
| 10 | Pitch y demo | 2 | 2.8 | 2.8 |
| | **Total** | **29** | **42.5** | **31.3** |
| | Disponible | | ≈ 34 (30 de construcción + 4 de pruebas) | ≈ 34 |

Recortes en orden y horas que liberan en el escenario pesimista: Louvain → componentes podados (1.0) · modelo de scikit-learn → reglas ponderadas (1.4) · agente con herramientas → plantilla (3.5) · interfaz avanzada → grafo básico o SVG (3.2) · ablaciones y semillas múltiples → una evaluación (2.1) = **11.2 h**. De 42.5 h se baja a 31.3 h.

**Carga por persona (h):** base M 8.0 · G 7.5 · A 6.5 · D 6.5. Pesimista **M 12.0 · G 10.5 · A 9.8 · D 10.2** (capacidad ≈ 8.5 cada uno). Piso: M 8.2 · G 8.4 · A 7.7 · D 7.0.

**Veredicto, con honestidad:**

- **El plan base no se sostiene en el escenario pesimista:** 42.5 h frente a ≈ 34 h disponibles (un 25 % de exceso) y Mariano quedaría en 12 h, un 40 % sobre su capacidad. Ese plan solo cabe si las estimaciones acertaran.
- **El piso sí cabe, con un colchón de apenas ≈ 2.7 h (8 %)**, y cada persona entre 7.0 y 8.4 h. Con el piso, el MVP funciona de punta a punta (lote → grafo → cola con razones → expediente por plantilla con citas verificadas → decisión registrada → backtest). **Eso debería sostener el 3/5 en funcionamiento de la funcionalidad crítica, pero sin margen:** un solo atasco de integración de más de 2–3 h (API–UI, Cytoscape) lo rompe. Lo que se pierde es **diferenciación** (agente con herramientas, interactividad, ablaciones), no el mínimo.
- Los multiplicadores 1.4 y 1.6 son una conjetura nuestra, y el cálculo no incluye imprevistos del lugar (red, configuración, comidas) ni las rondas de corrección tras la validación del enfoque.
- Si aun el piso se queda corto, las palancas siguientes son: quitar el LLM por completo (expediente solo por plantilla), reducir el backtest a R1 y R4, y recortar los patrones de la demo a dos.

**Riesgo de concentración en David (tarea 6, 5.5 h base y 8.8 h pesimista, en su primer hackathon).** David concentra la interfaz y el grafo interactivo; su perfil registrado es Flask/HTML/CSS, no React **(supuesto: no domina React ni Cytoscape)**. Si la UI se atrasa, la demo cae aunque el backend funcione. Apoyo recomendado:

1. **Contrato JSON el Día 1 a las 10:30** con un archivo de ejemplo, para que David avance sin esperar a Mariano ni a Glem.
2. **Respaldo de grafo estático (SVG servido por la API)**: si en H1 no hay grafo interactivo, se sigue con el SVG; el valor está en el expediente y la decisión, no en la animación.
3. **Pareo de ≈ 1 h con Glem el Día 1 por la tarde** para conectar la API con la UI, y **Antonio toma la pantalla de métricas** (≈ 1 h), que son tablas.
4. **Esqueleto genérico de frontend antes del 03.12** (Vite + Tailwind + Cytoscape con datos de juguete y sin lógica de dominio, declarado como preexistente): ahorraría ≈ 1.5–2 h de arranque. **Requiere decisión del equipo** (ver «Decisiones pendientes»), porque todo lo que se prepare debe declararse y no puede contener detección.
5. Regla de corte: si a las 16:30 del Día 1 la vista no muestra la cola y la ficha con datos reales, se reasigna a Mariano la integración de la API con la UI y David pasa al guion y a la pantalla de métricas.

### d.2 Qué recortar si falta tiempo (de arriba hacia abajo)

1. Louvain → solo componentes conexos podados.
2. Modelo de scikit-learn → solo reglas ponderadas con pesos ajustados en dev.
3. Agente con herramientas → plantilla determinista, y el LLM solo redacta el resumen.
4. Interfaz avanzada (filtros, línea de tiempo, métricas dentro de la UI) → grafo básico o SVG, ficha y botones.
5. Ablaciones y semillas múltiples → una sola evaluación.

**No se recorta:** el backtest contra reglas simples y R4, la medición sobre señuelos, la regla de corroboración, las citas verificadas del expediente y la decisión humana registrada. Sin ellos no hay KPI, ni evidencia, ni seguridad.

### d.3 Decisiones pendientes del equipo

- ¿Se aprueba el esqueleto genérico de frontend previo al 03.12, declarado como preexistente y sin lógica de dominio? (Conviene confirmarlo con la organización.)
- ¿Se acepta el piso (31.3 h) como alcance real y la puerta de decisión H1 del Día 1 a las 13:00?

---

## (e) Diseño de la medición

**Qué se mide (candidatos, a validar con el owner):**

1. Precisión y recall sobre redes de fraude inyectadas.
2. Reducción de falsos positivos frente a reglas simples.
3. Calidad de la cola de priorización: precisión@K y recall@K sobre las K primeras alertas, porque el resultado esperado habla de «priorizar investigaciones».
4. Opcional, **detección temprana**: fracción de la red que ya había ingresado cuando se emite la alerta (se reproduce el lote en orden de fechas). El expediente habla de «detección temprana».
5. Tiempo de preparación de un caso (candidato nuestro, **supuesto**; no figura en el expediente).

**Unidades.**

- **Red:** una alerta (comunidad priorizada) **acierta** si su solapamiento con una red de fraude cumple Jaccard ≥ 0.5 sobre solicitudes; coincidencia 1 a 1, la de mayor solapamiento primero. Precisión de redes = alertas que aciertan / alertas emitidas. Recall de redes = redes de fraude detectadas / redes de fraude inyectadas.
- **Solicitud:** precisión, recall y F1 de las solicitudes incluidas en alertas frente a `etiqueta = fraude`.
- **Falsos positivos:** (i) alertas que cubren un señuelo o solo solicitudes normales; (ii) **tasa de FP sobre señuelos** = señuelos alertados / señuelos totales; (iii) **carga de revisión** = alertas por cada 1,000 solicitudes.

**Línea comparativa:** R1 «dato compartido por ≥ 2 personas», R2 «≥ 3 personas» y **R4** (regla con criterio de dominio, ver b.8: F1 ≈ 0.9 en nuestro dataset). Si la Caja entrega sus reglas actuales, se usan **esas** como línea base **[POR CONFIRMAR]**. Reportar contra R4 es obligatorio: ganarle solo a R1 y R2 sería ganarle a un hombre de paja.

**Reducción de falsos positivos.** Se compara en el **mismo recall**: se ajusta el umbral de cada método hasta igualar el recall de la solución y se reportan FP absolutos y relativos. Sin igualar recall, la comparación sería trampa.

**Procedimiento.**

1. Generar el dataset con la semilla de desarrollo (2026). Afinar **solo** con la partición `dev`.
2. **Congelar** umbrales y pesos (commit y etiqueta antes de mirar `eval`).
3. Evaluar **una vez** en la partición `eval` y, además, en **semillas ciegas** (p. ej. 9001–9005) generadas el Día 2.
4. Reportar con **intervalo de confianza por remuestreo de redes** (1,000 réplicas): con 15 redes de fraude de evaluación por semilla, las diferencias chicas no son concluyentes y hay que decirlo.
5. Reportar **por dificultad** y **por patrón**: el recall en las redes de dificultad alta (en especial `direccion_fantasma`) es donde el grafo ponderado debería superar a R4; si no lo hace, hay que decirlo.
6. **Ablaciones:** sin normalización por capacidad, sin factores legítimos, **sin regla de corroboración**, sin recorte de vínculos débiles.
7. **Patrón sorpresa (opcional):** una persona que no construyó el detector inyecta a mano una red con una forma nueva y se mide si se detecta sin tocar el código.
8. **Tiempo de caso (opcional):** cronometrar a una persona armando el caso a mano con las tablas frente al expediente generado, 3 casos cada uno. Es una **simulación nuestra (supuesto)**; no se presenta como tiempo real de la Caja. **[POR CONFIRMAR el tiempo actual con el owner.]**
9. Todo se ejecuta con `scripts/evaluar_kpi.py` y su salida va a `docs/validacion.md`.

**Qué NO se afirmará:** ninguna cifra de impacto en la Caja, ninguna tasa real de fraude, ninguna reducción de costo. Solo resultados sobre datos sintéticos, con sus límites.

---

## (f) Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| **Falsos positivos** sobre familias, mercados, gremios, gestores | Daño a clientes legítimos; especialistas ahogados | Señuelos en el dataset (también en ráfaga y con clientes nuevos); pesos por rareza y capacidad; factores legítimos visibles; medición de FP contra R1, R2 y R4; umbral que prioriza precisión |
| **Concluir fraude por relaciones o coincidencias** (restricción literal del expediente) | Decisión injusta | **Regla de corroboración** (estructura + comportamiento); la alerta dice «patrón que merece revisión», nunca «fraude»; el expediente lista explicaciones alternativas; el verificador rechaza frases de conclusión; ablación que mide el efecto de la regla |
| **Acción sobre el cliente sin revisión humana** | Afecta al cliente | El sistema no cambia estados ni notifica; toda acción pasa por una decisión humana registrada con motivo |
| **Protección de datos** | Incumplimiento (Ley N.º 29733 y reglamento; confirmar con Legal) | Solo datos sintéticos; seudonimización antes de cualquier LLM externo; proveedor local o plantilla como alternativa; mínimo de datos por consulta; registro de decisiones. **[POR CONFIRMAR con Caja Experts]** |
| **Sesgos** | Discriminación por distrito, apellido o poca bancarización | Distrito y apellido no entran al puntaje de riesgo (el apellido solo **exonera** por parentesco); «cliente nuevo» solo refuerza una red ya formada; revisar tasa de alertas por agencia |
| **Alucinación del agente** | Evidencia falsa | Herramientas de solo lectura; salida estructurada; **verificador de citas**; plantilla de respaldo |
| **Sobreajuste al generador propio** | Resultados inflados | Partición dev/eval; semillas ciegas; patrón sorpresa; R4 como línea fuerte; reportar límites |
| **Datos reales de la Caja distintos a los supuestos** (el expediente aclara que son referenciales y sin compromiso de entrega) | Retrabajo | Adaptador ETL; preguntas al owner; diseño que no depende de columnas opcionales |
| **Tiempo (≈ 8 h por persona)** | MVP incompleto | Piso de 31.3 h con colchón de 2.7 h; hitos H1 y H2; tabla de recortes |
| **Concentración en David (UI)** | Demo sin interfaz | Contrato JSON temprano, respaldo SVG, pareo y regla de corte (d.1) |
| **Rendimiento del grafo** | Lentitud en demo | Lote de ~3,700 solicitudes; poda previa; precomputar en el arranque |
| **Dependencia de LLM externo** | Incumplir política o caída de red | Valor por defecto: plantilla sin red; proveedor intercambiable |
| **Condición eliminatoria (funcionalidad crítica ≥ 3/5)** | Descalificación | Una sola vertical punta a punta; H2 el Día 1; no construir nada antes del 03.12 |

---

## (g) Preguntas para el owner ((ver plataforma))

Prioridad alta (cambian el diseño):

- [ ] ¿Cuál es la **línea base**: reglas actuales, tasa de falsos positivos y tiempo de revisión por caso? ¿Cómo se mide hoy?
- [ ] El expediente menciona **casos simulados y datos sintéticos referenciales**: ¿vendrán **etiquetados** (redes de fraude y relaciones legítimas)? ¿En qué formato y volumen?
- [ ] ¿Qué **tipos de vínculos** son más relevantes (teléfono, dispositivo, dirección, referencia, contacto, negocio) y cuáles estarán en los datos? ¿Habrá **conexiones (IP, sesión) y ubicaciones**?
- [ ] ¿Se permite usar **LLM externos** (Claude, OpenAI) o solo modelos locales? ¿Qué datos pueden salir del entorno?
- [ ] ¿Quién es el **especialista** (prevención, investigación, riesgos) y cuál es su flujo y herramienta actuales?

Prioridad media:

- [ ] ¿Qué **columnas y volumen** tendrán los datos sintéticos? ¿Incluyen dispositivo, referencias, tipo de inmueble y antigüedad de cliente?
- [ ] ¿Las direcciones y teléfonos vienen **normalizados** o hay que resolver entidades?
- [ ] ¿Existe un **umbral de monto** de revisión reforzada que debamos usar (hoy suponemos S/ 10,000)?
- [ ] ¿Qué acciones de **prevención** puede orientar una alerta antes de un desembolso (verificación reforzada, pedido de más documentos) y cuáles se consideran decisiones que afectan al cliente?
- [ ] ¿Qué tipos de relaciones legítimas deben tratarse con cuidado especial (familias, mercados, gremios, gestores)?

---

## (h) Preexistente frente a nuevo en el evento

| Componente | Estado | Titular / licencia | Se declara en `docs/preexistente.md` |
|---|---|---|---|
| Generador de datos sintéticos RIE-02 (`retos/RIE-02/datos/generar.py`) y pruebas | **Preexistente** (21.11.2026) | Equipo | Sí |
| Datos generados `retos/RIE-02/datos/sintetico/` (semilla 2026) | **Preexistente** (regenerable) | Equipo | Sí |
| Este panorama y el concepto de solución | Preexistente (documentación) | Equipo | Sí (referencia) |
| Repo base: estructura de carpetas, README, configuración vacía | Preexistente | Equipo | Ya declarado |
| Esqueleto genérico de frontend (solo si el equipo lo aprueba; sin lógica de dominio) | Preexistente, **por decidir** | Equipo | Sí, si se hace |
| Librerías abiertas: FastAPI, Pydantic v2, pandas, numpy, networkx, scikit-learn, Pydantic AI, React, Vite, Tailwind, Cytoscape.js, pytest | Terceros | Licencias abiertas | Sí (resumen) |
| ETL de carga y constructor del grafo tipado con pesos | **Nuevo en el evento** | Se cede si ganamos | No |
| Comunidades, indicadores, regla de corroboración y exoneraciones legítimas | **Nuevo** | Se cede | No |
| Priorización con razones por factor | **Nuevo** | Se cede | No |
| Agente de expediente, verificador de citas, plantilla y `app/llm/provider.py` | **Nuevo** | Se cede | No |
| API FastAPI + SQLite de decisiones | **Nuevo** | Se cede | No |
| Vista del especialista y visualización del grafo | **Nuevo** | Se cede | No |
| `scripts/evaluar_kpi.py` (backtest, R1, R2, R4) y `docs/validacion.md` | **Nuevo** | Se cede | No |
| Pruebas de la funcionalidad crítica | **Nuevo** | Se cede | No |

Las reglas de control del generador (R1, R2, componente + ráfaga, R4) viven solo en `test_generar.py` para validar el dataset; **no son el detector** y en el evento se reescribirán como parte del backtest. No se reutiliza código de empleadores ni de otros clientes. Experiencia previa del equipo (agentes con aprobación humana, conciliación) se reutiliza solo como ideas.

---

## (i) Plan de pruebas

**Ya existe (37 pruebas, `retos/RIE-02/datos/test_generar.py`):**

- Integridad: ids únicos, llaves foráneas, sin huérfanos, referencias por solicitud.
- Ficticio y plausible: prefijos `FIC-`, montos, fechas, sin domingos.
- Sin fuga: ninguna columna de entrada delata la verdad; ids barajados.
- Reproducibilidad: misma semilla ⇒ mismos bytes; semilla distinta ⇒ otros datos; escala chica; CLI.
- Forma de cada patrón (anillo = ciclo de referencias; estrella = un contacto; dispositivo compartido = una huella; fantasma = un inmueble; evasiva = ningún vínculo con más de 2; familia, mercado, tableta, gremio, gestor y casualidad) y conectividad de cada red.
- **Honestidad del dataset:** R1 y R2 inundan de falsos positivos; ninguna regla de un solo vínculo es buena; la regla ingenua de componente y ráfaga queda bajo F1 0.7; R4 queda entre 0.6 y 0.97 y supera a la ingenua por más de 0.2; los señuelos también llegan en ráfaga; el fraude difícil se diluye en el tiempo; los perfiles de fraude y señuelo se traslapan.

**Se escribe en el evento:**

| Nivel | Pruebas |
|---|---|
| Grafo | Caso mínimo con aristas esperadas; peso decrece con la rareza y la capacidad; mismo resultado si se reordenan filas o ids |
| Detección | Cada patrón de fraude de dificultad baja se detecta; cada señuelo `familia`, `mercado`, `tableta_agencia` y `coincidencia_casual` **no** genera alerta; invariancia a la semilla de datos |
| Corroboración | Una red con solo estructura (familia, mercado) no se prioriza; una red con estructura y comportamiento sí; **ninguna alerta se genera por una sola coincidencia ni solo por relaciones** |
| Priorización | Más vínculos fuertes ⇒ mayor puntaje; los factores legítimos lo bajan; las razones suman al puntaje |
| Agente | Toda cita existe (verificador); ninguna frase de conclusión; la plantilla funciona sin red; contrato del proveedor con un doble de prueba |
| API | Contratos de `/redes`, `/expediente`, `/decision`; decisión sin motivo → error; auditoría escrita; **el estado de la solicitud no cambia** |
| Backtest | Misma semilla ⇒ mismas métricas; emparejamiento de redes con Jaccard; R1, R2 y R4 reproducen los valores de b.8 |
| Punta a punta | Un lote entra y sale con una alerta explicada y una decisión registrada (prueba de la demo) |
| Humana | Los Caja Experts revisan 3 expedientes y los criterios; se anotan en `docs/validacion.md` |

Meta: cobertura medida con `pytest --cov` de la lógica de dominio; informe de validación con las métricas, los intervalos y los límites.

---

## (j) Entrada para `docs/preexistente.md`

Texto para añadir a la tabla de componentes (la sesión de RIE-02 **no** edita ese archivo; lo hará quien coordine):

```markdown
| `retos/RIE-02/datos/generar.py` y `retos/RIE-02/datos/test_generar.py` | Generador de datos sintéticos para el desafío RIE-02: solicitudes MYPE ficticias con su grafo de personas, negocios, teléfonos, dispositivos, direcciones y referencias; redes de fraude inyectadas, relaciones legítimas señuelo y verdad de terreno. Reproducible con semilla. Las pruebas incluyen reglas de control para validar la dificultad del dataset. No contiene el detector ni la priorización | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-02/datos/sintetico/` | Salida del generador (semilla 2026, escala 1.0): 100 % sintética, documentos y teléfonos con prefijo FIC-. Regenerable con el script | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-02/panorama.md` | Especificación del dataset, arquitectura, plan del evento y diseño de la medición. Documentación, no código | Equipo | 21.11.2026 | No (preexistente) |
```

Y, en «Declaración», si el equipo elige RIE-02: *«El generador de datos de RIE-02 usa nombres, teléfonos y documentos ficticios; no contiene datos reales ni material de la Caja.»*

---

## Cotejo con el expediente

Comparado palabra por palabra contra `retos/RIE-02/expediente.md` (texto literal, actualizado por la Caja el 19.11, 12:21 p. m.), el concepto v1 (`retos/RIE-02/concepto.md`) y este panorama v1.

### Desviaciones encontradas y corregidas

| # | Tipo | Qué decía v1 | Qué dice el expediente | Corrección |
|---|---|---|---|---|
| 1 | **Atribuido sin decirlo** | El concepto citaba como «texto del expediente» una paráfrasis de v0 («Algunos fraudes involucran…») y dejaba un [POR CONFIRMAR contra el expediente literal] | «Algunas modalidades de fraude financiero pueden involucrar múltiples personas, negocios o solicitudes de crédito que, evaluadas individualmente, no presentan señales evidentes de irregularidad» | Concepto §1 usa el texto literal; se retiró el [POR CONFIRMAR] que ya no aplica |
| 2 | **Atribuido sin decirlo** | «Riesgos que el expediente pide respetar: falsos positivos y **reputación del cliente**… sin **decisiones crediticias automáticas**» | No dice «reputación» ni «decisiones crediticias automáticas» (esa frase viene del resumen común de los desafíos de riesgo, no del texto de RIE-02) | Se citan las restricciones literales; la reputación pasa a ser una preocupación nuestra, no del expediente |
| 3 | **Restricción diluida** | «Una sola coincidencia nunca alerta» y «la alerta nunca dice fraude» | «evitar conclusiones automáticas de fraude basadas únicamente en relaciones o coincidencias»: aplica también a **varias** relaciones juntas, no solo a una coincidencia | **Regla de corroboración:** una red solo se prioriza si combina estructura **y** comportamiento o perfil; ablación que la mide; prueba de que familias y mercados (solo estructura) no suben; salida «merece revisión», nunca conclusión |
| 4 | **Restricción diluida** | «No se ejecutan acciones crediticias automáticas» | «facilitar la revisión humana antes de tomar decisiones que afecten a los clientes» (más amplio que lo crediticio: bloqueo, rechazo, notificación, reporte) | El sistema no cambia el estado de la solicitud ni notifica al cliente; toda acción pasa por una decisión humana registrada con motivo; prueba de API |
| 5 | **No cubierto** | El concepto trataba solo la investigación | La pregunta pide «anticipar posibles riesgos de fraude y orientar acciones de **prevención e investigación**» | Se agrega la acción «Pedir verificación preventiva» antes de un desembolso, además de «Escalar a investigación», y la pregunta correspondiente al owner |
| 6 | **No cubierto** | Los KPI no medían la calidad de la cola ni la oportunidad | «mejorando la capacidad de **priorizar investigaciones**»; «prevención y **detección temprana**» | Se agregan precisión@K y recall@K de la cola y, opcional, detección temprana con *replay* temporal. El «tiempo de preparación de un caso» queda marcado como candidato nuestro (supuesto) |
| 7 | **No cubierto** | Los vínculos eran «teléfono, dispositivo, dirección, referencia» | «teléfonos, dispositivos, direcciones, referencias, **contactos o negocios**» | Se nombran contactos (la persona de referencia y su teléfono) y negocios (local y rubro compartidos) en el grafo, el diccionario y las preguntas |
| 8 | **No cubierto** | Se hablaba de los datos como «datos de la Caja, si llegan» | Insumos: «dispositivos y **conexiones**», «direcciones y **ubicaciones**», «**patrones de comportamiento**», «**casos simulados**»; y la nota: «datos referenciales, sin compromiso de entrega» | Se declara la brecha: el dataset no trae conexiones (IP) ni ubicaciones geográficas; «patrones de comportamiento» se cubre solo con ráfagas, montos y perfil; la nota de no compromiso entra en dependencias y riesgos; la pregunta sobre casos simulados cita el expediente |
| 9 | **No cubierto** | El concepto dejaba fuera la «integración con sistemas reales» sin explicar qué integración se demuestra | «desarrollo funcional, **integración tecnológica** y valor diferencial frente a soluciones convencionales»; «no será suficiente… dashboards» | Se explicita la integración que sí se demuestra (ETL → grafo → priorización → agente → API → interfaz, proveedor de LLM intercambiable, adaptador para datos de la Caja) y el diferencial medido contra reglas simples y R4; se aclara que la interfaz no es el valor |
| 10 | **Atribuido sin decirlo** | El panorama escribía «mínimos falsos positivos» | «considerar posibles falsos positivos» y, como resultado, «reducir falsos positivos» | Se corrigió la redacción |
| 11 | **Término ajeno** | Todos los documentos usan «investigador» | El expediente habla de «especialistas de Caja Trujillo» y de «prevención e investigación» | Se usa «especialista (prevención e investigación)» y se pregunta quién es **[POR CONFIRMAR]**; «investigador» queda como forma abreviada (supuesto) |
| 12 | **Marca obsoleta** | Panorama (a): «[POR CONFIRMAR contra el texto literal… `docs/reto.md` aún no lo trae]» | El texto literal ya existe en `retos/RIE-02/expediente.md` | Se reemplazó por la lectura literal |
| 13 | **Pregunta imprecisa** | «¿Habrá casos simulados etiquetados?» | El expediente **ya menciona** «casos simulados» y «datos sintéticos» como insumos | La pregunta ahora pregunta por su etiquetado, formato y volumen |

### Lo que el expediente dice y está cubierto sin desviación

| Expediente | Dónde se cubre |
|---|---|
| Owner: (ver plataforma); Eje 3 | Encabezado del concepto |
| «respetar la protección de datos personales» | (f), seudonimización, datos sintéticos, proveedor local o plantilla |
| «alertas… sustentadas en evidencia verificable» | Expediente con citas y verificador (c.7) |
| «considerar posibles falsos positivos» | Señuelos, R1/R2/R4, tasa de FP sobre señuelos |
| «facilitar la revisión humana» | Acciones y decisión registrada (c.8) |
| «distinguir relaciones legítimas de patrones que realmente merecen una revisión» | Factores legítimos, explicaciones alternativas, señuelos |
| «IA, agentes inteligentes, analítica predictiva… cuando aporten valor real» | Grafo ponderado, priorización, agente con verificador, comparado contra reglas |

### Cobertura de los insumos del expediente por el dataset

| Insumo del expediente | En `retos/RIE-02/datos/sintetico/` |
|---|---|
| Solicitudes de crédito | Sí (`solicitudes.csv`) |
| Datos de contacto | Sí (teléfonos y contactos de referencia) |
| Dispositivos y conexiones | Dispositivos sí; **conexiones (IP, sesión) no** |
| Direcciones y ubicaciones | Direcciones sí; **ubicaciones geográficas no** |
| Referencias y vínculos | Sí (`referencias.csv`, avales cruzados) |
| Patrones de comportamiento | Parcial: ráfagas, montos, perfil nuevo; no horarios ni velocidad de llenado |
| Casos simulados | Sí, como redes inyectadas con verdad de terreno |
| Datos sintéticos | Sí |
