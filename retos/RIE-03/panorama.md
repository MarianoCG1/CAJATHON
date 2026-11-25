# Panorama de abastecimiento — RIE-03 · Anticipar el deterioro de pago antes del atraso

> Documento de trabajo del equipo (21.11.2026). Material confidencial: repo privado. Lo marcado **(supuesto)** o **[POR CONFIRMAR]** no viene del expediente oficial.
> Alcance: qué necesita el desafío, cómo abastecerlo con datos sintéticos propios, cómo se construye en el evento y cómo se mide. **Aquí no hay modelo, agente, API, interfaz ni backtest**: eso se construye en la fase presencial (03–04.12). Lo único construido de antemano es el generador de datos (`retos/RIE-03/datos/`).

## Alcance MVP en una página

**Qué es:** una cola diaria preventiva para el gestor, con el porqué de cada alerta, su incertidumbre y una acción propuesta que el gestor aprueba, edita o descarta; más un backtest con y sin la solución. Todo se construye en el evento (03–04.12), salvo el generador y los datos.

**Entra (núcleo, no recortable)**

1. ETL a SQLite y variables **as-of** (solo información ≤ fecha de corte).
2. Modelo de deterioro calibrado, con rango de incertidumbre por alerta; sin alerta si el historial es insuficiente.
3. Separador de señal y fluctuación (persistencia, contraste estacional, convergencia) y control de fatiga: es el control de falsos positivos que pide el expediente.
4. Cola top-k con 2–3 señales explicadas por cliente.
5. Agente de intervención con guardas en código (canal viable, evidencia citada, nada de promesas crediticias), con respaldo por plantillas sin red.
6. API y bitácora: aprobar, editar o descartar; nada se envía.
7. Interfaz mínima: cola → caso → decisión.
8. Backtest con y sin la solución, frente a reglas simples, con sensibilidad al efecto de la intervención.
9. Pruebas automáticas y `docs/validacion.md`.

**Entra si hay tiempo (opcional, en orden de recorte)**: LLM real en el agente (si no, plantillas), GBM además de regresión logística, mini-gráficos y bitácora detallada, auditoría de sesgos completa (mínimo: un cuadro), varios escenarios de efecto, pulido visual.

**Queda fuera:** envío real de mensajes, integración con sistemas de la Caja, decisiones o condiciones crediticias, uso del score en calificación, recalibración continua, autenticación y multiusuario, más de un crédito por cliente, mapas y dashboards generales, app móvil.

**Criterio de terminado**

- Desde un repo limpio, un comando carga los datos y levanta la demo, sin red y sin claves.
- `pytest` en verde, incluida la prueba de no-fuga del futuro, las guardas del agente y que ningún endpoint envía nada.
- El backtest reproduce las mismas cifras con la semilla fija y `docs/validacion.md` las contiene con fecha y commit.
- Se recorre en la interfaz, con datos del sistema y no escritos a mano: cola → caso → intervención → aprobación → bitácora.
- Los casos de control funcionan: una fluctuación normal no alerta y un deterioro gradual sí.
- Historial de commits frecuente desde la primera hora; preexistente declarado.

**Guion de demo de 5 minutos** (los números se llenan con lo medido; nada se inventa)

| Tiempo | Qué se muestra |
|---|---|
| 0:00–0:40 | El problema con una historia ficticia (una bodega en La Esperanza que baja sus ventas durante meses antes del primer atraso) y la pregunta del expediente |
| 0:40–1:30 | Cola del día para un corte dado: k clientes con puntaje, rango de incertidumbre y estado; aparte, los créditos «sin información suficiente», que no alertan |
| 1:30–2:45 | Caso de deterioro gradual: qué cae, desde cuándo, frente al mismo mes del año anterior y a su sector; conducta de pago y deuda externa; días de anticipación |
| 2:45–3:20 | Caso de control: una fluctuación estacional que **no** alertó, y la regla que la filtró |
| 3:20–4:00 | El agente propone canal, momento y mensaje con la evidencia citada; se muestra una guarda que rechaza una promesa de condonación; el gestor edita y aprueba; queda en bitácora y no se envía |
| 4:00–5:00 | Backtest con y sin la solución: precisión en el top-k, falsos positivos (incluidos los de fluctuaciones normales) y anticipación; **cierre con el número antes/después**: tasa de paso a atraso > 30 días de la cartera alertada, «sin la solución: [medido]» frente a «con la solución: [medido bajo el escenario de efecto declarado]», con la advertencia de que el efecto es un escenario |

---

## 0. Resumen

- **Qué se abastece:** una cartera MYPE sintética de 5,000 clientes y 34 meses (2024-01 a 2026-10) con 9 tablas CSV, en `retos/RIE-03/datos/sintetico/`, generada con semilla fija.
- **Qué contiene de especial:** deterioro gradual inyectado con fecha de inicio conocida (para medir anticipación), fluctuaciones normales que imitan al deterioro (para medir falsos positivos), un pagador tardío habitual (trampa para reglas de «días de atraso»), un shock abrupto (límite de lo anticipable) y variables sensibles independientes del resultado (para auditar sesgos).
- **Qué NO tiene a propósito:** efecto de ninguna intervención. El efecto preventivo es un **parámetro de escenario** del backtest; nada de lo que muestre la demo lo prueba como hecho.
- **MVP revisado:** **31.5 h-persona** frente a 32 disponibles (4 × ~8 h): sin holgura. En el escenario pesimista (§d.4) salen **45.3 h**; solo con nueve recortes se llega a 31.7 h.

---

## (a) Qué necesita el desafío

### a.1 Datos e insumos (expediente, resumido)

Historial de pagos, comportamiento crediticio, evolución de saldos, actividad económica, variables de riesgo, eventos de incumplimiento, series históricas y datos sintéticos. La Caja no se compromete a entregarlos; si llegan, se mapean al mismo esquema. **[POR CONFIRMAR]**

### a.2 Mapa necesidad → dónde se cubre

| Necesidad del expediente | Tabla sintética | Qué permite |
|---|---|---|
| Historial de pagos | `cuotas` | Atrasos, pagos parciales, cadencia de pago, «creep» de días de atraso |
| Comportamiento crediticio | `senales_mensuales` (consultas y deuda en otras entidades), `creditos`, `clientes` | Sobreendeudamiento, antigüedad, carga cuota/ingreso |
| Evolución de saldos | `saldos_mensuales` | Saldo capital, saldo vencido, calificación por tramo |
| Actividad económica | `senales_mensuales` (abonos, operaciones, saldo de cuenta, cobros digitales) | Caída persistente de ingresos vs. estacionalidad |
| Variables de riesgo | `saldos_mensuales.calificacion`, `senales_mensuales` (consultas y deuda en otras entidades), `creditos.cuota_ingreso_origen` | Carga de cuota, sobreendeudamiento, tramo de atraso |
| Eventos de incumplimiento | `verdad_terreno` (solo para evaluar) | Etiquetas y fecha de inicio del deterioro |
| Series históricas | todas, con 34 cortes mensuales | Ventanas móviles, validación temporal |
| Canal viable de contacto | `clientes`, `gestiones` | Recomendar canal y momento con evidencia |
| Revisión humana y sesgos | `clientes.sexo`, `rango_edad`, `zona` (**solo auditoría**) | Medir disparidad de alertas sin entrenar con ellas |

### a.3 Componentes del producto (todos nuevos en el evento)

1. **ETL + features as-of**: carga de CSV a SQLite y variables calculadas solo con información ≤ fecha de corte.
2. **Modelo de deterioro**: probabilidad calibrada de pasar a atraso en un horizonte.
3. **Separador señal vs. fluctuación + explicación**: razones por alerta, contrastadas con el historial propio, la estacionalidad del sector y la persistencia.
4. **Agente de intervención**: canal, momento y propuesta, con salida estructurada y guardas.
5. **API + persistencia**: cola, caso, decisión del gestor, bitácora.
6. **Interfaz del gestor**: cola → caso → aprobar / editar / descartar.
7. **Backtest del KPI** y reporte de validación.

---

## (b) Cómo abastecerlo: especificación del dataset sintético

Implementado en `retos/RIE-03/datos/generar.py` (probado con `python -m pytest retos/RIE-03/datos -q`: 24 pruebas). Diccionario completo en `retos/RIE-03/datos/sintetico/diccionario.csv`; metadatos y hashes en `metadata.json`.

```powershell
python retos/RIE-03/datos/generar.py                          # 5,000 clientes, semilla 20261203 (lo ya generado)
python retos/RIE-03/datos/generar.py --n-clientes 15000       # más positivos para entrenar y validar
python retos/RIE-03/datos/generar.py --semilla 7 --salida C:\ruta\otra
```

Requiere Python 3.10+ (probado en 3.10.10), pandas y numpy; sin red. Misma semilla y parámetros ⇒ CSV idénticos byte a byte.

### b.1 Tablas, columnas clave y volúmenes (5,000 clientes)

| Tabla | Filas | Clave | Columnas principales (tipo) |
|---|---|---|---|
| `agencias` | 10 | `agencia_id` | nombre*, provincia, distrito, zona (urbana/periurbana/rural). *Geografía real de La Libertad; agencias **ficticias** («Sintética …») |
| `analistas` | 40 | `analista_id` | `agencia_id`, `antiguedad_meses` (int). Sin nombres |
| `clientes` | 5,000 | `cliente_id` (`CLI-00001`) | agencia, analista, `sector` (5), zona, `sexo`† , `rango_edad`† (5 tramos), antigüedad, `n_creditos_previos`, `tiene_cuenta_ahorros`, `tiene_billetera_digital`, `tiene_whatsapp` (0/1), `canal_preferido`, `mejor_franja_contacto` |
| `creditos` | 5,000 | `credito_id` (`CRE-00001`) | `producto`, `monto_desembolsado` (S/), `fecha_desembolso`, `plazo_meses`, `tea`, `cuota_mensual`, `dia_vencimiento`, `ingreso_neto_evaluacion`, `cuota_ingreso_origen` |
| `cuotas` | 73,728 | (`credito_id`, `nro_cuota`) | `fecha_vencimiento`, `monto_cuota`, `fecha_primer_pago`, `monto_primer_pago` (parcial si < cuota), `fecha_cancelacion`, `dias_atraso_cancelacion` (vacíos si impaga al corte final) |
| `saldos_mensuales` | 73,826 | (`credito_id`, `periodo`) | `saldo_capital`, `saldo_vencido` (S/), `dias_atraso_corte`, `calificacion` (normal 0–8, cpp 9–30, deficiente 31–60, dudoso 61–120, pérdida >120; tramos **(supuesto)**) |
| `senales_mensuales` | 73,826 | (`credito_id`, `periodo`) | `abonos_cuenta_mes`, `n_operaciones_cuenta_mes`, `saldo_promedio_cuenta_mes`, `cobros_digitales_mes`, `consultas_otras_entidades_mes`, `deuda_otras_entidades`, `n_entidades_con_deuda` |
| `gestiones` | 10,802 | `gestion_id` | `credito_id`, `fecha`, `canal`, `tipo`, `dias_atraso_al_gestionar` (5/15/30), `resultado` |
| `verdad_terreno` | 5,000 | `credito_id` | `trayectoria`, `mes_inicio_deterioro`, `fecha_primer_atraso_8d`, `fecha_primer_atraso_30d` |

† Solo para auditoría de sesgos; **prohibido como variable del modelo**. `verdad_terreno` es solo para evaluar; usarla como variable es fuga.

Reglas del diseño de tablas:

- Un crédito vigente por cliente; cuotas mensuales fijas (método francés), `dia_vencimiento` 1–28.
- Ventana de observación 2024-01-01 a 2026-10-31 (34 cortes). Créditos desembolsados desde 20 meses antes del inicio: el extracto empieza con cartera ya vigente, como un corte real.
- Señales mensuales visibles **al cierre del mes**; una cuota solo aparece cancelada si su fecha ≤ 2026-10-31. Ninguna tabla contiene fechas posteriores al corte final (probado).
- Un crédito sale del panel mensual al pasar de 180 días de atraso (castigo) o al cancelarse.
- Faltantes controlados: sin cuenta de ahorros (≈ 16 % global) no hay señales de cuenta; 2 % de faltantes al azar en las demás; sin billetera no hay cobros digitales.
- IDs secuenciales; sin nombres, documentos, teléfonos ni direcciones (probado por regex de nombres de columna).

### b.2 Distribuciones **(todas supuestos plausibles, a confirmar con el owner)**

| Variable | Distribución (resultado con la semilla por defecto) |
|---|---|
| Zona de agencia | 57 % urbana, 16 % periurbana, 27 % rural (por pesos de agencia) |
| Sector | comercio 38 %, servicios 20 %, agropecuario 18 %, producción 15 %, transporte 10 % (el mix depende de la zona; el agro pesa 46 % en rural) |
| Ingreso neto base mensual | lognormal con mediana S/ 2,800 (σ 0.5), recortado a [900; 20,000], ajustado por sector (transporte ×1.25, agro ×0.85) |
| Carga cuota/ingreso al originar | uniforme 0.15–0.38 (mediana 0.26) |
| Plazo (meses) | 6: 7 %, 12: 38 %, 18: 21 %, 24: 25 %, 36: 10 % |
| Monto | derivado de cuota, plazo y tasa; mediana S/ 9,000, media S/ 10,954, rango 900–73,500 |
| TEA | decrece con el monto (≈ 60 % a S/ 1,000, ≈ 46 % a S/ 50,000) más ruido; rango observado 38–62 % |
| Producto | capital de trabajo 70 %, activo fijo 18 %, agropecuario 12 % |
| Contacto | WhatsApp 44 %, llamada 28 %, visita 21 %, SMS 7 %; WhatsApp disponible 92 % urbano, 80 % periurbano, 66 % rural |
| Sexo / edad | F 52 %; tramos 12/28/30/21/9 %. **Independientes del resultado** por construcción |
| Estacionalidad mensual | perfil por sector, media 1 (comercio: pico en diciembre 1.25 y julio; agro: pico abril–junio, valle enero–febrero y de agosto a octubre; los demás casi planos) |

### b.3 Correlaciones que sí existen (y las que no)

- **Sí:** carga cuota/ingreso ↑ ⇒ más días de atraso cuando el ingreso cae; ingreso ↓ ⇒ abonos, operaciones y saldo de cuenta ↓ con ruido y estacionalidad; deterioro gradual ⇒ consultas de otras entidades ↑ y deuda externa ↑ **con un mes de rezago** respecto de la caída de ingresos; sector agropecuario ⇒ más volatilidad estacional (puede parecer deterioro).
- **No (a propósito):** sexo, rango de edad y canal preferido no influyen en el resultado. Si el modelo muestra disparidad por estos grupos, es un **artefacto del modelo** y se puede medir.

### b.4 Cómo se inyecta el deterioro y las fluctuaciones

Cada cliente recibe una trayectoria (conteos exactos, barajados con la semilla):

| Trayectoria | % | Mecanismo | Rol en la evaluación | Resultado observado (5,000) |
|---|---|---|---|---|
| `estable` | 65.5 | Ingreso estable con ruido AR(1) σ 0.08 y estacionalidad; paga a tiempo o con 1–3 días | Negativos fáciles | >8 d: 1.2 %; >30 d: 0.1 % |
| `fluctuante` | 18 | σ 0.18 y 1–3 caídas transitorias de ingreso (−12 % a −33 %, 1–3 meses) que se recuperan | **Falsos positivos potenciales**: se ven como deterioro, casi siempre se recuperan | >8 d: 16 %; >30 d: 5.4 % |
| `pagador_tardio` | 7 | Ingreso estable, hábito de pagar 3.5–8 días tarde, tope 25 días | Trampa para reglas «días de atraso > X»: parece riesgoso y no lo es | >8 d: 67 %; >30 d: 0 % |
| `deterioro_gradual` | 7 | Caída lineal del ingreso de 30–75 % durante 4–9 meses desde `mes_inicio_deterioro`; luego, creep de días de pago, pagos parciales, más consultas y deuda externa | **Positivos que se deben anticipar** | >8 d: 89 %; >30 d: 78 % |
| `shock_abrupto` | 2.5 | Caída de 50–85 % del ingreso en un mes, sin señales previas | Límite honesto de lo anticipable (recall máximo < 100 %) | >8 d: 100 %; >30 d: 100 % |

Resultados clave medidos en la semilla por defecto (los comprueban las pruebas):

- **Anticipación disponible:** mediana de ~150 días entre `mes_inicio_deterioro` y el primer atraso > 8 d en el deterioro gradual; el shock da ~26 días.
- **Prevalencia por cliente en 34 meses:** 17.1 % alguna vez > 8 d; 9.0 % alguna vez > 30 d.
- **Prevalencia por crédito-mes:** 96.6 % normal, 0.9 % CPP, 0.7 % deficiente, 1.0 % dudoso, 0.8 % pérdida. Con la etiqueta «pasa a > 30 d en los próximos 60 d», entre créditos con ≤ 8 d de atraso, la tasa de positivos es ~0.73 % (506 positivos en 69,100 crédito-mes: deterioro gradual 299, shock 146, fluctuante 54, estable 7).
- **Tamaño por partición** (cortes de `metadata.json`): entrenamiento 40,203 crédito-mes con 222 positivos (188 créditos); validación 14,515 con 134 (112); prueba 14,382 con 150 (121). **Es poco para un modelo estable**: para entrenar y validar conviene `--n-clientes 15000` (~3× positivos), declarando el cambio en el reporte. La mezcla de trayectorias y las tasas son parámetros (`Config.mezcla`).

### b.5 Semilla y reproducibilidad

Semilla por defecto `20261203`. `Config` fija semilla, número de clientes, meses y mezcla. `metadata.json` guarda semilla, conteos, prevalencias, partición temporal sugerida y SHA-256 de cada CSV. El generador no usa reloj ni red.

---

## (c) Arquitectura

### c.1 Componentes y estructura (se crean en el evento)

```
backend/app/
  main.py                 FastAPI
  api/                    cola.py, casos.py, decisiones.py, kpi.py
  domain/                 señales.py (relevante vs. fluctuación), politica.py (k, cooldown, guardas)
  ml/                     features.py (as-of), entrenar.py, scoring.py, explicar.py
  llm/                    provider.py, agente.py, guardas.py, plantillas.py
  db.py                   SQLite
scripts/evaluar_kpi.py    backtest (con y sin la solución)
frontend/                 React + Vite + Tailwind
```

### c.2 Flujo de datos

```
CSV sintéticos ──ETL──► SQLite ──features as-of(t)──► modelo ──score calibrado──► separador señal/fluctuación
                                                                                      │ (≥2 familias, persistencia, vs. estacionalidad)
                                                                                      ▼
                                              cola top-k(t) + razones ──► agente (LLMProvider) ──► intervención propuesta
                                                                                      │                  (canal, momento, propuesta, borrador)
                                                                                      ▼
                                                      gestor: aprobar | editar | descartar ──► bitácora (sin envío automático)
scripts/evaluar_kpi.py ── lee los mismos CSV, corre el mismo scoring en cortes históricos ──► docs/validacion.md
```

### c.3 Endpoints (diseño)

| Método y ruta | Función |
|---|---|
| `GET /api/cola?fecha=AAAA-MM-DD&k=N` | Cola priorizada: `credito_id`, score, **rango de incertidumbre**, banda, 2–3 señales, anticipación estimada. Los créditos con historial insuficiente salen aparte, con estado `sin_informacion_suficiente` y sin alerta |
| `GET /api/casos/{credito_id}?fecha=` | Ficha: serie de 12 meses, señales con su contraste, historial de gestiones, canal viable |
| `POST /api/casos/{credito_id}/recomendacion` | El agente devuelve la intervención propuesta (estructura validada) |
| `POST /api/casos/{credito_id}/decision` | `{accion: aprobar\|editar\|descartar, texto?, motivo?}` → bitácora. **No envía nada** |
| `GET /api/kpi/backtest` | Resultado del backtest precalculado, con y sin la solución |
| `GET /api/salud` | Versión, semilla de datos, proveedor LLM activo |

### c.4 Interfaz del proveedor de LLM (`app/llm/provider.py`, diseño)

Objetivo: cambiar entre Claude, OpenAI y un modelo local sin tocar la lógica, y poder trabajar **sin red** si la política de IA externa lo prohíbe **[POR CONFIRMAR]**.

```python
class Mensaje(BaseModel):
    rol: Literal["sistema", "usuario"]
    contenido: str

class RespuestaLLM(BaseModel):
    texto: str | None
    estructurada: BaseModel | None   # instancia del esquema pedido
    modelo: str
    proveedor: str

class LLMProvider(Protocol):
    nombre: str
    def generar(self, mensajes: list[Mensaje], *, esquema: type[BaseModel] | None = None,
                temperatura: float = 0.0) -> RespuestaLLM: ...
    def modelo_pydantic_ai(self) -> object: ...   # adaptador para Pydantic AI

# Implementaciones: AnthropicProvider, OpenAIProvider, LocalProvider (p. ej. servidor compatible con OpenAI),
# PlantillaProvider (determinista, sin red: respaldo, pruebas y recorte de tiempo).
# Selección por variable de entorno LLM_PROVIDER; claves por entorno, nunca en el repo.
```

**Agente y guardas** (las guardas son código y se prueban; no dependen del LLM):

- **Entrada:** solo `credito_id`, señales numéricas, historial de gestiones y canales viables. Sin nombres ni datos personales (protección de datos del expediente); si un proveedor externo no está permitido, el agente corre con `LocalProvider` o `PlantillaProvider`.
- **Salida estructurada:** `canal` (∈ canales viables del cliente), `franja`, `tipo_propuesta` (recordatorio, llamada de acompañamiento, visita, **sugerir evaluación de reprogramación**), `borrador_mensaje`, `justificacion` (cita ≥ 2 evidencias existentes por id), `confianza`.
- **Prohibido por validación:** prometer tasa, condonación, refinanciamiento o cualquier condición crediticia; tono amenazante; canal no viable. «Evaluación de reprogramación» es una sugerencia al analista, no una acción.
- **Acotado:** herramientas de solo lectura (historial, gestiones, calendario de cuotas) y una de escritura (guardar el borrador). El agente nunca marca «enviado».
- **Respaldo:** si el LLM falla o está prohibido, `PlantillaProvider` arma la propuesta con reglas (canal preferido + franja + plantilla por tipo de señal).

### c.5 Explicación y control de falsos positivos (`domain/señales.py`)

Una alerta entra a la cola solo si, además de un score alto, cumple:

1. **Persistencia**: la caída lleva ≥ N meses (N a calibrar, 2–3 **(supuesto)**), no un mes aislado.
2. **Contraste estacional**: la variable cae frente al mismo mes del año anterior o frente a la mediana de su cohorte del sector, no solo frente al mes previo.
3. **Convergencia**: ≥ 2 familias de señales apuntan en la misma dirección (ingreso/cuenta, conducta de pago, endeudamiento externo).
4. **Control de fatiga**: tope por gestor, enfriamiento de 30 días tras un descarte, y deduplicación de alertas repetidas.
5. **Incertidumbre explícita**: cada score lleva un rango (método a elegir en el evento, p. ej. remuestreo del modelo o conjunto de modelos); una alerta con rango muy amplio se muestra como «baja confianza» y pesa menos en la priorización.
6. **Información insuficiente**: con menos de 3 meses de señales visibles (o datos faltantes en la mayoría de las familias) no hay alerta; el crédito aparece como `sin_informacion_suficiente` para que el gestor lo vea y decida.
7. **Sin efecto crediticio**: el score es solo para gestión preventiva y no se expone a ningún proceso de calificación, límites, tasas ni condiciones.

---

## (d) Plan hora a hora del evento (4 personas, ~8 h netas por persona)

Reloj del evento: día 1 con validación del enfoque 09:45, construcción 10:30–13:00 y 14:00–16:30, pruebas 16:30–17:30; día 2 con construcción 09:30–12:00, validación final 12:00–12:45 y **entrega 13:00**. Son ~10.7 h de reloj; se asumen ~8 h netas por persona (validaciones, mentores, interrupciones). **Commits pequeños y frecuentes desde la primera hora**: son la evidencia de desarrollo.

Roles: **M** Mariano (backend, agente, integración) · **G** Glem (datos, modelo, pruebas) · **A** Antonio (KPI, dominio, caso de negocio) · **D** David (flujo y UI, demo).

### d.1 Cronograma por bloques

| Bloque | M | G | A | D | Hito (commit) |
|---|---|---|---|---|---|
| **Día 1 · 09:00–10:30** | Repo, esqueleto FastAPI, interfaz `LLMProvider`, ETL de CSV a SQLite | Exploración de datos; features v1 (ventanas 3/6 meses, tendencia, contraste estacional) | Fija con el owner/mentor etiqueta, horizonte, capacidad k y baselines; plantilla de backtest | Flujo del gestor (cola → caso → decisión) y wireframe | Repo + datos cargados |
| **D1 · 10:30–13:00** | Endpoints cola/caso/decisión + persistencia | Modelo base (regresión logística) y GBM; validación temporal | Arnés de backtest as-of: reglas B1/B2, métricas | UI: cola priorizada, filtros | `GET /cola` con score real |
| **D1 · 14:00–16:30** | Agente (Pydantic AI) con herramientas acotadas, esquema y guardas; respaldo por plantillas | Explicabilidad + separador señal/fluctuación + control de fatiga | Reglas de dominio de señales; caso de negocio con escenarios de efecto | UI del caso: señales, explicación, panel de acción, bitácora | Flujo de punta a punta (sin pulir) |
| **D1 · 16:30–17:30** | Pruebas de API y de guardas (nada se envía sin aprobación) | Pruebas de modelo y de no-fuga temporal | **Primer backtest completo → `docs/validacion.md` v1** | Prueba de flujo con 2 personas ajenas al equipo | Informe v1 con número antes/después |
| **Día 2 · 09:30–12:00** | Integración final, `/api/kpi/backtest`, ajustes del agente | Umbrales, auditoría de sesgos por grupo, revisión de calibración | Backtest final y sensibilidad al efecto; números del pitch | Pulido de UI, **modo demo guionado**, diapositivas | Demo estable |
| **D2 · 12:00–12:45** | Congelar versión, `pytest`, README técnico | Re-correr backtest con semilla fija | Verificar consistencia cifras ↔ documento | Ensayo del pitch con el reloj | Etiqueta de entrega |
| **D2 · 13:00** | **Entrega** | | | | |

### d.2 Horas por tarea (revisadas)

| Tarea | Responsable principal | Horas |
|---|---|---|
| ETL a SQLite y features as-of *(el generador ya existe)* | M + G | 2 |
| Modelo de deterioro y calibración | G | 4 |
| Explicabilidad y control de falsos positivos | G | 3 |
| Agente de intervención y guardas (con respaldo por plantillas) | M | 3 |
| API y persistencia | M | 3 |
| UI: cola y caso con aprobar / editar / descartar | D | 4 |
| Backtest, KPI y comparación contra líneas base | A (+ G) | 4 |
| Pruebas y validación (`docs/validacion.md`) | G (+ M) | 3 |
| **Núcleo no recortable** | | **26** |
| Diseño del flujo del gestor | D | 1.5 |
| Reglas de dominio y caso de negocio | A | 2 |
| Pitch y demo | A + D | 2 |
| **Total** | | **31.5 de 32 h** |

Cobertura de habilidades de la pareja líder según `scripts/sinergia`: 85 % con el equipo de 4; la brecha de la pareja David + Mariano (señales vs. fluctuación en el dominio financiero) la cubre Antonio, que además dirige el caso de negocio.

### d.3 Qué recortar si falta tiempo (en este orden)

1. **LLM del agente → plantillas deterministas** y el LLM solo redacta el borrador del mensaje (−1.5 h).
2. **GBM → solo regresión logística calibrada** (−1.5 h).
3. **Mini-gráficos y bitácora detallada** de la UI → tabla de señales y bitácora mínima (−1.5 h).
4. **Auditoría de sesgos** → un cuadro de tasa de alerta por grupo (−1 h).
5. **Sensibilidad al efecto** → un solo escenario con el rango declarado (−0.5 h).

**No se recorta nunca:** cola priorizada, explicación de cada alerta, aprobación humana con bitácora, backtest con y sin la solución, y pruebas. Esto es lo que sostiene el mínimo 3/5 de funcionalidad crítica.

### d.4 Escenario pesimista (prueba de estrés de las horas)

**Supuestos de la prueba:** cada tarea × 1.4; el agente y la integración × 1.6. Los factores los fijó el coordinador; no salen de datos. Como «integración» se toma **API y persistencia** (es el pegamento entre datos, modelo, agente e interfaz). Esto además deja a la vista que la tabla d.2 no trae una línea propia de «integración final» (que el cronograma d.1 sí ocupa el día 2) y que 31.5 h ya subestimaba esa parte.

| Tarea | Base (h) | Factor | Pesimista (h) |
|---|---|---|---|
| ETL y features as-of | 2 | 1.4 | 2.8 |
| Modelo y calibración | 4 | 1.4 | 5.6 |
| Explicabilidad y control de FP | 3 | 1.4 | 4.2 |
| Agente y guardas | 3 | 1.6 | 4.8 |
| API y persistencia (integración) | 3 | 1.6 | 4.8 |
| UI cola y caso | 4 | 1.4 | 5.6 |
| Backtest y KPI | 4 | 1.4 | 5.6 |
| Pruebas y validación | 3 | 1.4 | 4.2 |
| **Núcleo** | **26** | | **37.6** |
| Flujo del gestor | 1.5 | 1.4 | 2.1 |
| Reglas de dominio y caso de negocio | 2 | 1.4 | 2.8 |
| Pitch y demo | 2 | 1.4 | 2.8 |
| **Total** | **31.5** | | **45.3 h** frente a 32 disponibles (13.3 h de más, +42 %) |

**Qué recortes de la lista d.3 se activan:** los cinco, y en el valor pesimista.

| Recorte | Ahorro pesimista |
|---|---|
| 1. LLM del agente → plantillas | 2.4 h |
| 2. GBM → solo regresión logística | 2.1 h |
| 3. Mini-gráficos y bitácora detallada | 2.1 h |
| 4. Auditoría de sesgos → un cuadro | 1.4 h |
| 5. Sensibilidad → un solo escenario | 0.7 h |
| **Subtotal** | **8.7 h → quedan 36.6 h** |

**Con los cinco recortes todavía faltan 4.6 h.** La lista d.3 **no alcanza** en el escenario pesimista. Hay que añadir recortes que no estaban en la lista:

| Recorte adicional | Ahorro pesimista |
|---|---|
| 6. Flujo de diseño → wireframe mínimo (1.5 → 0.5 h base) | 1.4 h |
| 7. Reglas de dominio y caso de negocio → tres señales validadas con los Challenge Owners (2 → 1 h base) | 1.4 h |
| 8. Pitch → guion fijo ensayado una vez (2 → 1 h base) | 1.4 h |
| 9. Backtest → solo B0 y B1 como comparadores (−0.5 h base) | 0.7 h |
| **Subtotal** | **4.9 h → quedan 31.7 h** |

**Resultado: 31.7 h de 32, sin holgura, con el producto reducido al mínimo viable.** Además hay un problema de reparto: antes de recortar, la carga pesimista por persona es Mariano ≈ 12.4 h, Glem ≈ 14.0 h, Antonio ≈ 9.8 h y David ≈ 9.1 h; tras los nueve recortes, ≈ 10.0, 10.5, 6.3 y 4.9 h. Mariano y Glem siguen sobre 8 h mientras Antonio y David tienen margen: **hay que mover ≈ 4.5 h de trabajo en Python** (variables del ETL, pruebas del backtest) a Antonio y de API de lectura y pruebas de interfaz a David, lo que exige práctica previa (se puede ensayar con el generador y el esqueleto, no con la funcionalidad crítica).

**¿Se sostiene el mínimo de 3/5 de funcionalidad crítica?** Respuesta honesta:

- **Con el plan completo (45.3 h): no.** Faltarían 13 h; algo quedaría a medias.
- **Con los cinco recortes de d.3 (36.6 h): no.** Aún faltan 4.6 h.
- **Con los nueve recortes (31.7 h): sí, pero en el límite.** El producto que queda tiene cola con puntaje real, rango de incertidumbre, señales explicadas, filtro de fluctuaciones, intervención por plantillas con guardas, aprobación con bitácora, backtest contra B0 y B1, y pruebas. Eso es una funcionalidad crítica de punta a punta, aunque simple. Pero **no hay colchón**: si un solo bloque (el agente o la integración) se desvía por encima de ×1.6, o si alguien se enferma o se cae la red, el 3/5 queda en riesgo real. Que el jurado dé 3 o más sobre 5 también depende de su criterio, que no conocemos.
- **Un seguro que no vale:** una demo con resultados escritos a mano. La funcionalidad crítica debe funcionar con datos del sistema. El «modo demo guionado» solo fija el recorrido y los casos, nunca las cifras.

**Consecuencia para el plan:** conviene **tratar el mínimo viable como el plan base** (recortes 1–2 desde el día 1, y 6–9 como alcance real) y dejar el resto como mejora si sobra tiempo, en lugar de recortar bajo presión el día 2. Antes del 03.12, sin tocar la funcionalidad crítica, se pueden preparar herramientas generales (esqueleto vacío del repo, plantillas de pruebas, entrenamiento cruzado con el generador) y declararlas en `docs/preexistente.md`.

---

## (e) Diseño del backtest del KPI

Este diseño se implementa en `scripts/evaluar_kpi.py` **durante el evento**. Todas las definiciones marcadas **[POR CONFIRMAR]** deben validarse con el owner.

### e.1 Unidad, población y etiqueta

- **Unidad:** (crédito, fecha de corte t). Cortes mensuales (fin de mes); la cola «del día» de la demo re-ejecuta el mismo scoring en un corte elegido.
- **Población elegible:** créditos vigentes con `dias_atraso_corte ≤ 8` y ≥ 3 meses de señales visibles. Los demás se marcan «sin historial suficiente» o «ya en atraso» y no entran en la cola preventiva.
- **Etiqueta principal Y60:** el primer atraso > 30 días ocurre en (t, t + 60 días]. **[POR CONFIRMAR]** (umbral 8 vs. 30 días y horizonte).
- **Etiqueta secundaria:** primer atraso > 8 días en los próximos 30 días.
- **Regla as-of:** al cortar en t solo se usan filas con fecha ≤ t (señales del mes cerrado, cuotas y gestiones con fecha ≤ t). Hay una prueba automática de no-fuga (§i).

### e.2 Partición temporal y semilla

Entrenamiento hasta 2025-06 (con purga de 60 días antes de validar), validación 2025-07 a 2025-12 (calibración, umbral y k), **prueba 2026-01 a 2026-08 usada una sola vez**. Cortes 2026-09 y 2026-10 no tienen horizonte completo. Semilla fija en el modelo y en el remuestreo. Intervalos de confianza por bootstrap sobre créditos, no sobre crédito-mes (los crédito-mes de un mismo crédito están correlacionados).

### e.3 Línea base «sin la solución» y comparadores

| Id | Qué es | Para qué |
|---|---|---|
| **B0 (operativa)** | Política reactiva actual simulada: se gestiona desde +5 días tras el vencimiento (`gestiones`). Anticipación ≤ 0 | Línea base operativa de la demo. La verdadera línea base de la Caja es **[POR CONFIRMAR]** |
| B1 | Regla simple: atraso previo > 0 días en las últimas 3 cuotas | Muestra la trampa del pagador tardío |
| B2 | Regla de una señal: abonos de cuenta −25 % frente al mes previo | Muestra los falsos positivos de las fluctuaciones |
| B3 | Aleatorio con el mismo k | Piso de referencia |
| **Solución** | Score calibrado + persistencia + contraste estacional + convergencia + control de fatiga | Lo que se defiende |

### e.4 Métricas

| Métrica | Definición |
|---|---|
| **Principal (KPI)** | Tasa de paso a atraso > 30 d de la cartera alertada, con y sin intervención (ver e.5) |
| Precision@k | Alertas que realmente pasan a > 30 d en 60 d ÷ k. k = capacidad mensual del equipo de gestores **[POR CONFIRMAR]**; escenario inicial 5 % de los vigentes **(supuesto)** |
| Recall@k | Créditos que pasarán a > 30 d y estaban en la cola ÷ todos los que pasan |
| Tasa de falsos positivos | Alertas sin paso a > 30 d en 60 d ÷ alertas |
| **FP sobre fluctuaciones normales** | Parte de las alertas que corresponden a `fluctuante`/`pagador_tardio` (solo medible en sintético, vía `verdad_terreno`) |
| Anticipación | Días entre la primera alerta sostenida y el primer atraso > 8 d (y > 30 d); mediana y p25. Comparada con B0 (≤ 0) y con `mes_inicio_deterioro` |
| Fatiga de alertas | Alertas por gestor por día y proporción de repetidas |
| Calidad del modelo | PR-AUC, Brier y curva de calibración |
| Incertidumbre | Cobertura empírica del rango de incertidumbre en prueba (qué parte de los casos cae dentro) y proporción de alertas de «baja confianza» |
| Equidad (auditoría) | Tasa de alerta y de FP por sexo, rango de edad y zona; las tasas base son iguales por construcción, así que una brecha es del modelo. Umbral aceptable **[POR DEFINIR]** |

### e.5 Cómo se obtiene el «con y sin la solución» sin inventar el efecto

Los datos sintéticos **no contienen ninguna intervención**, así que:

- **Sin la solución:** tasa observada de paso a > 30 d entre los créditos que la solución habría alertado (contrafactual = lo que ocurrió en los datos).
- **Con la solución:** esa tasa × (1 − e), donde **e** es la efectividad de la intervención preventiva sobre quienes reciben la gestión. **e es un parámetro de escenario, no un dato**: se reporta como tabla de sensibilidad (p. ej. e ∈ {0.1, 0.2, 0.3}, valores de escenario y no estimaciones de impacto) y, si el owner da una referencia de efectividad de sus gestiones, se usa esa.
- **Lo que sí se mide como hecho (sobre datos sintéticos):** capacidad de anticipar (precision@k, recall@k, días de anticipación), costo de las alertas (falsos positivos y fatiga) y disparidad entre grupos. El mensaje al jurado: «detectamos X % de los casos Y días antes, con Z % de falsos positivos; el impacto depende de la efectividad de la intervención, que mostramos como escenario».

### e.6 Procedimiento

1. Cargar CSV, construir features as-of para cada corte elegible.
2. Entrenar con la partición de entrenamiento; calibrar y fijar k y umbral con validación.
3. Congelar; evaluar una vez en prueba: solución, B0–B3.
4. Calcular métricas con IC por bootstrap de créditos; tabla de sensibilidad de **e**.
5. Escribir `docs/validacion.md` y un JSON que sirve a `/api/kpi/backtest`.
6. Prueba de regresión: el script con semilla fija da las mismas cifras.

---

## (f) Riesgos y mitigaciones

| # | Riesgo | Mitigación |
|---|---|---|
| 1 | Pocos positivos en datos sintéticos: modelo inestable, IC anchos | Generar 15,000 clientes para entrenar; IC por bootstrap; reportar honestamente el tamaño de muestra |
| 2 | Falsos positivos y fatiga de alertas (riesgo del expediente) | Persistencia, contraste estacional, convergencia, tope por gestor, enfriamiento; métrica explícita de FP sobre fluctuaciones |
| 3 | Fuga del futuro en las features (invalida el backtest) | Funciones as-of únicas; prueba que corta los datos en t y compara; la misma función sirve a la API y al backtest |
| 4 | Los datos de la Caja (si llegan) tienen otro esquema | Capa de mapeo en el ETL; el modelo trabaja sobre features, no sobre columnas crudas |
| 5 | Política de IA externa prohíbe LLM en la nube | `LLMProvider` intercambiable, `LocalProvider` y `PlantillaProvider` sin red; la demo funciona completa sin LLM |
| 6 | El agente promete condiciones crediticias o alucina | Guardas en código (validación de salida, evidencias existentes, lista de promesas prohibidas); revisión humana obligatoria; pruebas |
| 7 | Sesgos del modelo | Sexo y edad fuera de las features; auditoría de tasa de alerta y de FP por grupo; reporte en la entrega |
| 8 | Concepto confundido con «predicción clásica de mora» | Diferenciar en la **acción**: señal explicada + intervención recomendada + backtest de falsos positivos |
| 9 | El jurado cuestiona el efecto de la intervención | Presentarlo como escenario con sensibilidad; lo medible se mide (e.5) |
| 10 | No cabe en ~8 h por persona | Núcleo de 26 h; recortes en orden (d.3); modo demo guionado como seguro |
| 11 | Preexistente confundido con desarrollo nuevo (condición eliminatoria) | Solo el generador y el dataset son previos y están declarados; todo lo demás se commitea desde el evento |
| 12 | Muchos equipos eligen RIE-03 | Diferenciación en la acción, el control de FP y la auditoría de sesgos; datos y backtest propios y reproducibles |
| 13 | Protección de datos personales (restricción del expediente) si más adelante se usan datos de la Caja | Seudonimización y minimización por diseño; el agente y la bitácora no reciben datos personales; sexo y edad solo para auditar; consulta al owner sobre campos permitidos a un LLM externo |
| 14 | Incertidumbre mal calibrada o mal comunicada (restricción del expediente) | Rango por alerta, cobertura medida en prueba, estado «baja confianza» y «sin información suficiente» visibles en la UI |
| 15 | Que el score se use para decidir crédito (restricción del expediente) | Uso declarado solo preventivo; sin integración con calificación, límites ni tasas; prueba de contrato de la API |

---

## (g) Preguntas para el owner (por prioridad)

1. **KPI y línea base:** ¿cuál es la morosidad actual y cómo se mide (mora > 8 o > 30 días)? ¿Qué mejora consideran relevante? ¿Qué horizonte de anticipación es útil (30, 60, 90 días)?
2. **Datos:** ¿entregarán datos sintéticos? ¿Con qué columnas, volumen, periodo y tasa de eventos de incumplimiento?
3. **IA externa:** ¿se permiten APIs de LLM externas con datos sintéticos, o solo modelos locales?
4. **Señales actuales:** ¿qué señales de deterioro monitorean hoy, con qué frecuencia y con qué reglas?
5. **Canales y flujo:** ¿qué canales de contacto preventivo son viables (WhatsApp, llamada, visita, SMS)? ¿En qué sistema trabaja el gestor hoy y dónde se integraría una cola diaria?
6. **Capacidad:** ¿cuántos clientes puede gestionar un analista por día? (define k y la fatiga aceptable)
7. **Intervención:** ¿qué propuestas puede ofrecer un gestor sin comité (recordatorio, reprogramación, otras)? ¿Qué está fuera de límites?
8. **Efectividad:** ¿existe alguna referencia de efectividad de la gestión temprana, para fijar el parámetro e del backtest?
9. **Equidad y datos sensibles:** ¿qué variables no pueden usarse? ¿Se pide auditoría por grupo?
10. **Evaluación:** ¿cómo se medirá la contribución al KPI en el jurado y qué evidencia se espera?

---

## (h) Preexistente vs. nuevo en el evento

| Componente | Estado | Titular | Nota |
|---|---|---|---|
| `retos/RIE-03/datos/generar.py` y `test_generar.py` | **Preexistente** (21.11.2026) | Equipo | Herramienta de datos; no es la funcionalidad crítica |
| `retos/RIE-03/datos/sintetico/*.csv`, `diccionario.csv`, `metadata.json` | **Preexistente** (salida del generador) | Equipo | 100 % sintético; reproducible con la semilla |
| Librerías abiertas (FastAPI, Pydantic, pandas, scikit-learn, LightGBM, React, Vite, Tailwind, pytest, Pydantic AI) | Terceros | Sus autores | Bajo sus licencias |
| `scripts/sinergia/`, `scripts/conceptos/`, `docs/` | Preexistente | Equipo | Planificación; no forman parte del producto |
| ETL a SQLite y features as-of | **Nuevo en el evento** | Equipo | |
| Modelo de deterioro, calibración y explicabilidad | **Nuevo en el evento** | Equipo | |
| Separador señal vs. fluctuación y control de fatiga | **Nuevo en el evento** | Equipo | |
| Agente de intervención, guardas y `app/llm/provider.py` | **Nuevo en el evento** | Equipo | |
| API, persistencia y bitácora | **Nuevo en el evento** | Equipo | |
| Interfaz del gestor | **Nuevo en el evento** | Equipo | |
| `scripts/evaluar_kpi.py`, `docs/validacion.md` | **Nuevo en el evento** | Equipo | |
| Pruebas del producto | **Nuevo en el evento** | Equipo | |

Experiencia previa del developer en agentes con aprobación humana y modelos predictivos: ideas y experiencia, **sin copiar código** de empleadores ni de otros clientes.

---

## (i) Plan de pruebas

### i.1 Hecho (generador, 24 pruebas)

Reproducibilidad (misma semilla, semillas distintas, CSV idénticos byte a byte, CLI); esquema y diccionario; claves únicas e integridad referencial; ausencia de datos personales; rangos plausibles; ninguna fecha posterior al corte final; coherencia de pagos y orden de cancelaciones; días de atraso de `saldos_mensuales` iguales a los recalculados desde `cuotas`; saldo capital no creciente; mezcla de trayectorias exacta; resultado por trayectoria; el deterioro gradual precede al atraso y el shock da menos aviso; las señales caen en gradual y no en estable; las fluctuaciones imitan caídas pero se recuperan; faltantes controlados; variables sensibles independientes del resultado.

### i.2 Por hacer en el evento (producto)

| Área | Prueba | Criterio |
|---|---|---|
| Features | **No-fuga**: features(t) con datos completos == features(t) con datos truncados en t | Igualdad exacta |
| Modelo | Calibración en validación; PR-AUC supera a B1, B2 y B3 | Brier y curva; ordenamiento de métricas |
| Cola | Respeta k, tope por gestor y enfriamiento; no incluye créditos ya en atraso | Pruebas unitarias |
| Separador | Un caso `fluctuante` sintético (caída de 1 mes, recuperada, estacional) no entra; un `deterioro_gradual` sí | Casos fijados con semilla |
| Agente | Salida cumple el esquema; canal ∈ viables; cita evidencias existentes; rechaza promesas crediticias | Pruebas con respuestas del `PlantillaProvider` y con respuestas adversarias simuladas |
| Aprobación humana | Ningún endpoint envía ni ejecuta; toda acción pasa por `decision` con bitácora | Prueba de contrato de la API |
| API | Contratos de `/cola`, `/casos`, `/decision`, `/kpi/backtest` | pytest + TestClient |
| Backtest | Misma semilla ⇒ mismas cifras; partición de prueba usada una vez | Prueba de regresión |
| Equidad | Brecha de tasa de alerta por grupo bajo el umbral definido | Reporte en `docs/validacion.md` |
| Incertidumbre | Toda alerta trae rango; con < 3 meses de señales no hay alerta y el estado es `sin_informacion_suficiente` | Pruebas unitarias; cobertura empírica en el backtest |
| Privacidad | Ni el prompt del agente ni la bitácora contienen campos sensibles (sexo, edad) ni datos personales | Prueba que inspecciona prompt y registros |
| UI | Flujo cola → caso → aprobar de punta a punta | Prueba manual guionada; E2E si hay tiempo |
| Sin red | La demo completa corre con `PlantillaProvider` | Prueba de humo |

Todo lo anterior se refleja en `docs/validacion.md` con la fecha y el commit de cada corrida.

---

## (j) Entrada para `docs/preexistente.md`

Texto sugerido para agregar a la tabla de `docs/preexistente.md` (no se edita desde esta tarea; lo aplica el coordinador):

```markdown
| `retos/RIE-03/datos/generar.py` y `test_generar.py` | Generador de cartera MYPE sintética para el desafío RIE-03 (clientes, créditos, cuotas, saldos, señales mensuales, gestiones y verdad de terreno). Reproducible con semilla fija. No contiene el modelo, el agente, la API, la interfaz ni el backtest | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-03/datos/sintetico/` | Salida del generador anterior (CSV, diccionario y metadatos): 100 % sintética, sin datos reales ni personales | Equipo | 21.11.2026 | No (preexistente) |
```

Nota para la declaración final: la funcionalidad crítica de RIE-03 (modelo, separador señal/fluctuación, agente, API, interfaz y backtest) **no** es preexistente y se construye entre el 03 y el 04.12 con historial git. Si el equipo decide usar datos entregados por la Caja, se declaran aparte como material de la organización.

---

## Cotejo con el expediente

Comparación palabra por palabra del concepto (`retos/RIE-03/concepto.md`) y de este panorama contra el texto literal de `retos/RIE-03/expediente.md` (actualizado por la Caja el viernes 20.11, 12:32 p. m.). El expediente no se modificó.

### Desviaciones encontradas y corrección

| # | Tipo | Qué decía nuestro texto | Qué dice el expediente | Corrección |
|---|---|---|---|---|
| 1 | **Restricción diluida** | El concepto listaba **tres** límites (falsos positivos, sesgos, sin decisiones automáticas) | **Protección de datos personales** es la primera restricción de «Riesgos» | Concepto §1, §2, §4, §6, §8 y Anexo B incluyen protección de datos; seudonimización y minimización por diseño; el agente y la bitácora no ven datos personales. Panorama: riesgo 13, prueba de privacidad, guarda en c.4 |
| 2 | **Restricción diluida** | No se mencionaba la incertidumbre | «considerar la incertidumbre de las predicciones» | Rango de incertidumbre por alerta en el modelo, la API y la interfaz; estado «baja confianza»; métrica de cobertura del rango; riesgo 14; prueba |
| 3 | **Restricción diluida** | «Sin decisiones crediticias automáticas» | «…que **afecten a los clientes**» | El concepto declara que la alerta no cambia calificación, condiciones, límites ni tasa; el panorama añade la guarda 7 en c.5, el riesgo 15 y la prueba de contrato |
| 4 | **Atribución indebida** | §1 afirmaba como hecho «Hoy esas señales se detectan tarde o se confunden con fluctuaciones» | El expediente no dice cómo se detectan hoy; dice que el deterioro puede ser gradual, que algunas señales podrían identificarse y que no toda variación es un riesgo | Reescrito: lo del expediente va con sus palabras; la lectura sobre «intervenciones tardías y alertas innecesarias» queda como **(supuesto, a validar con el owner)**. Esa afirmación venía del borrador v0 (generado) |
| 5 | **Cobertura faltante** | No cubríamos «decisiones basadas en información insuficiente» | «evitando alertas innecesarias y decisiones basadas en información insuficiente» | Los créditos con historial insuficiente no alertan y se muestran como `sin_informacion_suficiente` (concepto §2 y §6; panorama c.3, c.5 punto 6, prueba) |
| 6 | **Cobertura faltante** | El mapeo de insumos omitía **«Variables de riesgo»** | Lista «Variables de riesgo» entre los datos e insumos | Fila añadida en a.2 (calificación por tramo, consultas y deuda externa, carga de cuota) y el modelo las usa (concepto §2) |
| 7 | **Matiz** | «La Caja no se compromete a entregarlos» | «los datos son **referenciales** y no implican un compromiso de entrega» | Concepto §8 usa «referenciales» y mantiene el respaldo del generador |
| 8 | **Cobertura faltante** | «Demostrar integración tecnológica» no aparecía como tal | «desarrollo funcional, integración tecnológica y valor diferencial frente a soluciones convencionales» | Concepto §4: integración de punta a punta (datos → modelo → agente → API → interfaz) y diferencia frente a reglas de días de atraso y puntajes sin explicación, medida en el backtest |
| 9 | **Cobertura parcial** | Priorización y «generando información confiable» | «priorizar oportunidades de intervención preventiva, generando información confiable» | Cubierto por la cola priorizada y por la incertidumbre y el contraste estacional; concepto §1 lo cita ahora |

### Lo que sí coincide (sin cambios)

- Pregunta de innovación e idea central: identificar señales tempranas y facilitar acciones preventivas.
- Distinguir señales relevantes de fluctuaciones normales; alertas sustentadas en evidencia; minimizar falsos positivos; facilitar la revisión humana; evitar sesgos.
- Resultado esperado: reducir incumplimientos, mejorar la calidad de la cartera y preservar la salud financiera de los microempresarios.
- Complejidad tecnológica: IA, agentes y analítica predictiva con valor real; ni chatbot genérico, ni dashboard, ni formulario, ni automatización básica.
- El expediente no trae KPI ni línea base: seguimos marcándolos **[POR CONFIRMAR]**.

### Lo que decimos y el expediente no dice (todo marcado como supuesto)

KPI candidatos; umbral y horizonte de la etiqueta (8 o 30 días; 60 días); capacidad k del gestor; cola «diaria»; canales de contacto; propuestas permitidas al gestor sin comité; efectividad de la intervención; tramos de atraso por calificación; todas las distribuciones del dataset. Ninguno se presenta como dato de la Caja.

### Observaciones sin corrección necesaria

- El expediente menciona «optimización» entre las capacidades posibles. No la prometemos: la cola top-k bajo capacidad es una selección simple. Si hay tiempo, podría formularse como optimización con tope por gestor, pero no está en el alcance.
- Los datos del expediente son «referenciales»: nuestro dataset no lo reemplaza; es un respaldo hasta que el owner aclare qué entregará.
