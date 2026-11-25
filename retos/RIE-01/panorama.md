# Panorama de abastecimiento — RIE-01 · Microfinanzas resilientes al clima

> Documento de preparación (21.11.2026). Material confidencial: repo privado. Todo lo no oficial va marcado **(supuesto)** o **[POR CONFIRMAR]**.
> El expediente oficial no publica KPI, línea base ni datos concretos (`docs/investigacion/02`). Aquí no se inventa ninguna cifra de impacto: las cifras que aparecen describen **nuestro dataset sintético**, no a la Caja.
> Concepto asociado: `retos/RIE-01/concepto.md`. Generador: `retos/RIE-01/datos/generar.py`. Datos: `retos/RIE-01/datos/sintetico/`.

## Alcance MVP en una página

**Qué entra** (se construye en el evento, en este orden de valor):
1. Escenario ex ante (tipo × severidad) que el analista elige.
2. Modelo en tres capas sobre datos sintéticos: amenaza local por sector → vulnerabilidad del negocio → mora; con tres cifras separadas (**expuesta**, **probablemente afectada**, **mora incremental**) y rango p10–p50–p90.
3. Mapa por distrito y sector, y ranking de clientes por zona con el motivo de cada uno.
4. Priorización bajo la capacidad de visitas de cada agencia.
5. Agente que propone acciones del catálogo (por cliente y por zona), con evidencia y costo; el gestor aprueba o rechaza y queda registro. Proveedor de LLM intercambiable y variante determinista.
6. Backtest con `scripts/evaluar_kpi.py`: K1 y K2 como mínimo (K3 y K4 si hay tiempo) contra las reglas de zona y de saldo, en eventos simulados con verdad oculta.
7. Pruebas automáticas y `docs/validacion.md`.

**Qué queda fuera:** integración con el core de la Caja; envío real de mensajes o ejecución de acciones; pronóstico meteorológico propio; datos reales o descargados (SENAMHI, CENEPRED, ANA, etc. quedan como ruta de sustitución); modelado separado de daño en infraestructura o acceso a mercados (se resume en la caída de ingreso); probabilidades de escenarios; autenticación, despliegue productivo y rendimiento a escala.

**Núcleo no recortable** (sostiene el 3/5): escenario → tres cifras con rango (aunque sea analítico) → ranking en mapa (aunque sea puntos en SVG) → plan con aprobación humana (aunque sea determinista) → backtest de un KPI frente a una línea base.
**Opcional, en orden de recorte:** teselas de mapa · redacción con LLM · Monte Carlo · asignación entera · sequía en la demo · resolución de sector · K3 y K4 · réplica por semillas (§d).

**Criterio de terminado** (a las 12:00 del día 2, antes de la validación final):
- Los 6 criterios de aceptación del concepto §6 se ven funcionando en la demo, con datos del generador.
- `python -m pytest -q` pasa y `docs/validacion.md` recoge comandos, resultados y fallas conocidas.
- Existe la tabla con/sin del KPI en al menos 3 eventos de prueba, incluido uno más severo que toda la historia.
- Historial de commits que muestra el avance por hitos; `docs/preexistente.md` actualizado.
- Demo ensayada al menos dos veces y video de respaldo de 30–60 s.

**Guion de demo de 5 minutos**

| Tiempo | Qué se muestra | Mensaje |
|---|---|---|
| 0:00–0:30 | La pregunta del reto y la solución en una frase | Anticipar y actuar antes del evento |
| 0:30–1:15 | El embudo de la cartera sintética: expuesta → afectada → en mora | Exposición no es pérdida ni incumplimiento |
| 1:15–2:15 | Se activa «inundación severa en la costa norte»: mapa y tres cifras con rango | Incertidumbre explícita |
| 2:15–3:00 | Ranking dentro de la capacidad de cada agencia; ficha con el porqué de un cliente | Evidencia, no caja negra |
| 3:00–3:45 | El agente propone el plan; el gestor aprueba una acción y rechaza otra | La decisión es humana |
| 3:45–4:45 | **Backtest: número antes/después.** «Con la regla de zona, a igual presupuesto de visitas, se captura X % del saldo que luego cae en mora; con el Radar, Y %», en un evento más severo que la historia | El resultado se mide, y se dice que es sobre datos sintéticos |
| 4:45–5:00 | Límites y siguiente paso: datos y KPI de la Caja, acciones reales | Honestidad y continuidad |

X e Y se obtienen en el evento; hoy no existen y no se estiman.

---

## Resumen en 10 líneas

1. Lo que el desafío necesita es **conectar tres mundos**: dónde está la cartera, qué amenazas climáticas la pueden golpear y qué haría la Caja al respecto.
2. Sin datos de la Caja, todo se abastece con un **mundo sintético** (distritos y sectores del norte del Perú, 12 000 clientes, créditos en S/, mapa de amenaza con error, escenarios, historia y eventos de prueba con «verdad» oculta).
3. El generador ya existe, es reproducible (semilla 20261203) y tiene **40 pruebas** que pasan. Es lo único preexistente; el modelo, los escenarios, el mapa y el agente se construyen en el evento.
4. El dataset trae a propósito dos propiedades que el expediente pide respetar: **exposición ≠ pérdida ni incumplimiento** (el embudo se estrecha) e **incertidumbre de escenarios** (el evento real no coincide con el escenario ex ante). Añade una propiedad propia: **datos geográficos imperfectos** (el mapa visible es grueso y con error); el expediente solo dice que los datos son referenciales.
5. La verdad del backtest vive aparte (`backtest/`) y no se usa para calibrar: evita que el KPI sea circular.
6. La solución se mide con 4 KPI candidatos (K1–K4) contra 4 líneas base (azar, regla de zona, regla de zona + actividad, por saldo); la línea base real de la Caja es **[POR CONFIRMAR]**.
7. Si la Caja o fuentes públicas dan mapas reales, se sustituyen tablas sin cambiar el modelo (§b.5, **[POR CONFIRMAR]**; no se descargó nada).
8. MVP revisado: **30,5 h de trabajo + 1,5 h de colchón = 32 h-persona** (4 × 8 h). Recortes ordenados en §d.
9. Mayor riesgo técnico: **que el backtest sintético parezca un examen que nosotros mismos escribimos**. Mitigación en §e.4 y §f.
10. Mayor riesgo de concepto: confundir exposición con pérdida. El diseño separa tres capas y cada número se muestra con su rango.

---

## (a) Qué necesita el desafío

Basado en el expediente literal (`retos/RIE-01/expediente.md`): la pregunta de innovación («anticipar los riesgos que los eventos climáticos representan para los negocios financiados […] y desarrollar estrategias preventivas que fortalezcan su resiliencia»), el contexto (los eventos «pueden afectar» a microempresarios «en zonas vulnerables o que desarrollan actividades sensibles al clima», «potencialmente» sus ingresos y capacidad de pago), los datos e insumos listados (ubicación geográfica, actividad económica, información climática, mapas de amenazas, escenarios climáticos, exposición crediticia, datos sintéticos; «referenciales», sin compromiso de entrega) y los riesgos: considerar la incertidumbre de los escenarios, no asumir que exposición implica pérdidas económicas o incumplimiento, sustentar recomendaciones en evidencia y respetar la protección de datos y las políticas de riesgo de la Caja.

| Necesidad | Para qué | Quién la aporta | Cómo la cubrimos |
|---|---|---|---|
| **Ubicación de cada cliente/negocio** (distrito y, si se puede, sector o coordenadas) | Cruzar cartera con amenaza | Caja **[POR CONFIRMAR]** qué granularidad tiene | `clientes.csv`: distrito, sector y lat/lon aleatorios por sector |
| **Actividad económica y sensibilidad al clima** | Una bodega y un arrozal no sufren igual | Caja (CIIU o rubro) + criterio experto | `actividades.csv`: 14 actividades con sensibilidad por amenaza (**supuesto**) |
| **Exposición crediticia** (saldo, cuota, atraso, calificación, producto) | Medir cuánta cartera y cuánta mora potencial hay | Caja | `creditos.csv` en S/ |
| **Capacidad de amortiguación** (otros ingresos, seguro, reservas) | Explica por qué no todo expuesto se afecta | Caja **[POR CONFIRMAR]** si existe | `clientes.csv`: 3 variables (**supuesto**) |
| **Mapa de amenaza** | Dónde pega cada tipo de evento | Fuentes públicas o la Caja **[POR CONFIRMAR]** | `mapa_amenaza.csv` (distrito, con error) + rasgos de terreno por sector |
| **Escenarios climáticos** | Qué pasaría si… con incertidumbre | Criterio experto + fuentes públicas | `escenarios.csv`: 9 (3 amenazas × 3 severidades) con desviación |
| **Historia de eventos y su efecto en pagos** | Calibrar afectación y mora | Caja **[POR CONFIRMAR]** (si hay historia) | `eventos_historicos.csv` + `impacto_historico.csv` (10 eventos) |
| **Eventos de prueba con verdad conocida** | Medir el KPI con y sin la solución | Generador | `backtest/` (6 eventos) |
| **Catálogo de acciones preventivas y sus costos** | Que el agente proponga algo realizable | Caja **[POR CONFIRMAR]** | `acciones_preventivas.csv` (7 acciones, parámetros de simulación) |
| **Capacidad operativa** (gestores, visitas por semana) | Que el plan quepa en la realidad | Caja **[POR CONFIRMAR]** | `agencias.csv`: `n_gestores`, `capacidad_visitas_semana` (**supuesto**) |
| **Componentes de software** | Modelo, escenarios, mapa, API, agente, backtest | Equipo, en el evento | §c |
| **Proveedor de LLM intercambiable** | El agente redacta y razona sobre evidencia | Política de IA externa **[POR CONFIRMAR]** | `app/llm/provider.py` con 4 implementaciones (§c.5) |

---

## (b) Cómo abastecerlo

### b.1 Principios de diseño del mundo sintético

* **Plausible, no real.** Distritos reales del norte del Perú (nombres públicos, coordenadas aproximadas a ±5 km), pero todo lo demás es inventado. La huella de agencias es **sintética**, no la red real de la Caja. Pesa más La Libertad (≈67 % de clientes) porque el proyecto asume agencias allí; la huella real es **[POR CONFIRMAR]**.
* **Sin personas.** No hay nombres, documentos, teléfonos ni domicilios. Los ids (`C000001`) son secuenciales **barajados** (no se ordenan por distrito). Las coordenadas son un punto aleatorio alrededor del centroide de un sector.
* **Montos en soles.** Saldos desde unas decenas hasta ≈ S/ 76 000; mediana ≈ S/ 3 800. Cartera total de la muestra ≈ S/ 73 millones **(sintético, no representa a la Caja)**.
* **Verdad separada de lo visible.** El mapa que ve el modelo es una aproximación gruesa (distrito) con error; la susceptibilidad real por sector y los resultados de los eventos de backtest van en `backtest/`.
* **Exposición ≠ pérdida por construcción.** Tres filtros sucesivos: estar en zona amenazada → resultar afectado (depende de actividad, intensidad local y colchón) → entrar en mora (depende de la carga financiera tras la caída de ingreso).
* **Incertidumbre de escenarios.** El backtest activa un *escenario ex ante* con severidad nominal; el evento realizado difiere (desviación 0,10–0,15) y al menos un evento supera la severidad máxima histórica (prueba de extrapolación).
* **Sin red, con semilla.** Solo pandas y numpy. Mismo `--seed` y parámetros ⇒ mismos archivos (hashes verificados en la prueba y en `manifest.json`).

### b.2 Especificación de tablas

Volúmenes con los valores por defecto (`--n-clientes 12000`, semilla 20261203, corte 31.10.2026). Con otra semilla o tamaño cambian las filas de `creditos` (~1,15 por cliente) e `impacto_historico` (depende de la antigüedad de clientes).

| Archivo | Filas (por defecto) | Rol |
|---|---|---|
| `agencias.csv` | 13 | Referencia |
| `distritos.csv` | 44 | Referencia |
| `sectores.csv` | 176 (4 por distrito) | Referencia, rasgos de terreno observables |
| `mapa_amenaza.csv` | 132 (44 × 3) | **Visible**: mapa con error, resolución distrito |
| `actividades.csv` | 14 | Referencia |
| `clientes.csv` | 12 000 | Cartera |
| `creditos.csv` | ≈ 13 800 | Cartera, S/ |
| `escenarios.csv` | 9 | Ex ante |
| `eventos_historicos.csv` | 10 | Calibración |
| `impacto_historico.csv` | ≈ 60 000 | Calibración (entrenar aquí) |
| `acciones_preventivas.csv` | 7 | Catálogo (supuestos) |
| `backtest/eventos_backtest.csv` | 6 | **Verdad**: no usar para entrenar |
| `backtest/impacto_backtest.csv` | 72 000 (6 × 12 000) | **Verdad** |
| `backtest/verdad_amenaza_sector.csv` | 528 (176 × 3) | **Verdad** |
| `manifest.json`, `LEEME.md` | — | Semilla, filas, `sha256` y diagnóstico del embudo |

#### `agencias.csv`
| Columna | Tipo | Descripción |
|---|---|---|
| `agencia_id` | str | `AG01`…`AG13`. Agencia **sintética** |
| `nombre` | str | «Agencia sintética <ciudad>» |
| `distrito_id` | str | Distrito donde se ubica |
| `lat`, `lon` | float | Aproximadas |
| `n_gestores` | int | ≥ 2; ≈ 1 por 350 clientes asignados (**supuesto**) |
| `capacidad_visitas_semana` | int | `n_gestores × 12` (**supuesto**) |

#### `distritos.csv`
| Columna | Tipo | Descripción |
|---|---|---|
| `distrito_id` | str | `D01`…`D44` (código propio; el ubigeo INEI real es **[POR CONFIRMAR]** si se cruza con fuentes públicas) |
| `distrito`, `provincia`, `departamento` | str | Nombres geográficos reales: La Libertad, Lambayeque, Piura, Áncash, Cajamarca |
| `lat`, `lon` | float | Aproximadas (±5 km) |
| `altitud_m` | int | Aproximada |
| `zona` | str | `costa` / `sierra` / `selva_alta` |
| `perfil` | str | `urbano`, `agricola_costa`, `sierra`, `selva_alta`, `pesquero_turistico` |
| `peso_relativo` | float | Peso para repartir clientes (inventado) |

#### `sectores.csv` — 4 sectores por distrito: ribera de cauce, llanura urbana, campiña regada, ladera de secano
| Columna | Tipo | Descripción |
|---|---|---|
| `sector_id` | str | `D01-R`, `D01-U`, `D01-C`, `D01-L` |
| `distrito_id` | str | FK |
| `tipo_sector` | str | `ribera_cauce` / `llanura_urbana` / `campina_regada` / `ladera_secano` |
| `lat`, `lon`, `altitud_m` | float | Centroide |
| `dist_cauce_km` | float | Rango por tipo: ribera 0,02–0,4; llanura 0,5–3; campiña 0,3–2; ladera 1–6 |
| `pendiente_pct` | float | Ribera 0,5–4; llanura 0–3; campiña 1–5; ladera 15–45 |
| `peso_area` | float | Peso del sector en su distrito (por perfil) |

Estos rasgos son **observables** (en la vida real saldrían de un modelo de elevación e hidrografía) y permiten estimar susceptibilidad más fina que el mapa distrital.

#### `mapa_amenaza.csv` — lo que ve el modelo
| Columna | Tipo | Descripción |
|---|---|---|
| `distrito_id`, `tipo_amenaza` | str | `lluvia_intensa` / `inundacion` / `sequia` |
| `indice` | float 0–1 | Promedio ponderado de la susceptibilidad real por sector **+ ruido N(0; 0,07)** |
| `categoria` | str | `bajo` (40 %), `medio` (30 %), `alto` (20 %), `muy_alto` (10 %) por cuantiles dentro de cada amenaza |
| `error_estandar` | float | 0,07 (se declara para que el modelo pueda usarlo) |
| `resolucion`, `fuente` | str | `distrito`, `sintetico_v1` |

#### `actividades.csv`
| Columna | Tipo | Descripción |
|---|---|---|
| `actividad_id` | str | `A01`…`A14` |
| `actividad`, `rubro` | str | Rubros: agropecuario, pesca, comercio, servicios, transporte, manufactura, construcción, turismo |
| `sens_lluvia_intensa`, `sens_inundacion`, `sens_sequia` | float 0–1 | Sensibilidad por amenaza (**supuesto**) |
| `es_sensible_clima` | int | 1 si la sensibilidad máxima ≥ 0,60 |
| `ticket_mediano_soles`, `factor_ingreso`, `prob_seguro` | num | Parámetros de generación (**supuesto**) |

Mezcla resultante: ≈ 32 % de clientes en actividades sensibles; agropecuario 29 %, comercio 27 %, servicios 18 %, manufactura 8 %, transporte 8 %, construcción 5 %, turismo 3 %, pesca 3 %. Los distritos agrícolas de costa tienen ≥ 20 puntos más de actividades sensibles que los urbanos (hay una prueba para eso).

#### `clientes.csv` (12 000)
| Columna | Tipo | Descripción |
|---|---|---|
| `cliente_id` | str | `C000001`…, barajado |
| `agencia_id`, `distrito_id`, `sector_id`, `actividad_id` | str | FK |
| `lat`, `lon` | float | Punto aleatorio ≈ ±0,5 km del sector (no es un domicilio) |
| `fecha_alta`, `antiguedad_meses` | str / int | Antigüedad 1–240 meses (≥ 1 mes más que su crédito más antiguo) |
| `ingreso_mensual_soles` | float | 600–15 000; derivado de la cuota con carga objetivo ≈ 20 % (mediana ≈ S/ 3 500) |
| `tiene_ingreso_secundario` | 0/1 | ≈ 25 % |
| `tiene_seguro` | 0/1 | ≈ 5 % (10 % en agropecuario) |
| `meses_reserva` | int | 0, 1, 2, 3 o 5 (45/25/15/10/5 %) |

Distribución geográfica: La Libertad 67 %, Piura 15 %, Lambayeque 10 %, Áncash 4 %, Cajamarca 3,5 %; costa 91 %, sierra 8 %, selva alta 1,6 %.

#### `creditos.csv` (≈ 13 800)
| Columna | Tipo | Descripción |
|---|---|---|
| `credito_id`, `cliente_id` | str | 15 % de clientes tiene un segundo crédito |
| `producto` | str | `capital_trabajo` (65 %), `activo_fijo` (17 %), `agropecuario` (17 %) |
| `monto_desembolsado_soles` | float | 500–80 000, múltiplos de 100 |
| `plazo_meses` | int | Agro 6–12; activo fijo 12–36; capital de trabajo 6–24 |
| `tea_pct` | float | 20–60 (media 38 / 32 / 30 según producto; **supuesto**) |
| `fecha_desembolso` | str | Coherente con cuotas pagadas |
| `cuota_mensual_soles`, `saldo_soles` | float | Sistema francés; saldo ≤ monto |
| `dias_atraso` | int | 0 en ≈ 85 %; 1–30 en ≈ 10 %; > 30 en ≈ 5 % (**mora sintética, no representa a la Caja**) |
| `calificacion` | str | `normal` ≤ 8 d, `cpp` ≤ 30, `deficiente` ≤ 60, `dudoso` ≤ 120, `perdida` > 120 (simplificación) |
| `estado` | str | `vigente`, `vencido` (> 30 d), `refinanciado` (2 %) |

#### `escenarios.csv` (9)
`escenario_id` (`ES01`–`ES09`), `nombre`, `tipo_amenaza`, `severidad` (leve/moderada/severa), `severidad_nominal` (0,30/0,55/0,85), `sd_severidad` (0,10/0,12/0,15), `intensidad_costa|sierra|selva_alta` (= severidad × patrón por zona), `duracion_semanas` (lluvia 3–6; inundación 2–5; sequía 12–32), `descripcion`. La intensidad se reparte por zona con un patrón por amenaza (p. ej. la sequía pega más en sierra que en costa irrigada).

#### `eventos_historicos.csv` y `impacto_historico.csv` (para calibrar)
10 eventos con fechas ficticias 2018–2025 (no replican episodios reales) y severidad máxima 0,55. `impacto_historico` trae, por evento y cliente que ya existía: `afectado`, `caida_ingreso_pct`, `dias_atraso_max_90d`, `incumple_30d`. **No** trae la intensidad local ni el saldo en mora, para no filtrar la verdad. Simplificación **(supuesto)**: las características del cliente son las del corte, no las de la fecha del evento.

#### `acciones_preventivas.csv` (7)
`accion_id`, `accion`, `tipo`, `descripcion`, `costo_unitario_soles`, `efectividad_min`, `efectividad_max` (reducción relativa de P(mora | afectado)), `aplica_rubros`, `requiere_aprobacion_humana` (=1), `origen_parametros` (=`supuesto_generador`). Acciones: alerta temprana, visita preventiva, reprogramación preventiva, ampliación de plazo, capital de reposición, derivación a microseguro (**[POR CONFIRMAR]** si la Caja lo ofrece), asesoría de continuidad. **Costos y efectividades son parámetros de simulación, no política de la Caja ni estimación de impacto**; el KPI de pérdida evitada se reporta como rango y condicionado a ellos.

#### `backtest/` (verdad oculta)
* `eventos_backtest.csv`: `evento_id` (`EB01`–`EB06`), `escenario_id` (el escenario ex ante que se activaría), `tipo_amenaza`, `fecha_inicio_simulada` (2027), `severidad_nominal`, `severidad_realizada`, intensidades realizadas por zona. Mezcla: lluvia moderada, inundación severa, sequía severa, inundación moderada, lluvia severa, sequía leve.
* `impacto_backtest.csv`: por evento y cliente: `intensidad_local_real`, `afectado`, `caida_ingreso_pct`, `dias_atraso_max_90d`, `incumple_30d`, `saldo_en_mora_soles`.
* `verdad_amenaza_sector.csv`: susceptibilidad real por sector y amenaza.

### b.3 Cómo se genera el «mundo» (para razonar sobre circularidad)

Todos los parámetros son **supuestos del generador**.

1. **Susceptibilidad real por sector y amenaza**: `h = base[amenaza][tipo_sector] × patrón_zona × factor_distrito × lognormal(0; 0,2)`; en inundación se multiplica además por `0,5 + 0,5·exp(−dist_cauce/1,5)`. `factor_distrito ~ lognormal(0; 0,35)` representa cuenca, drenaje o riego.
2. **Mapa visible**: promedio ponderado por `peso_area` de `h` en el distrito, más ruido N(0; 0,07), recortado a [0, 1].
3. **Evento**: intensidad por zona = severidad × patrón × exp(N(0; 0,15)). Intensidad local = `h × intensidad_zona × (1 + 0,25·ε_sector,evento)`; el `ε` es un microclima por sector y evento que **ningún modelo puede ver**.
4. **Afectación**: `logit = −3,0 + 8,5·intensidad_local·sensibilidad − 0,5·colchón + N(0; 0,5)`, con `colchón = 0,8·ingreso_secundario + 1·seguro + 0,25·meses_reserva`.
5. **Caída de ingreso** (si afectado): `0,10 + 0,6·intensidad_local·sensibilidad + N(0; 0,08)`, entre 5 % y 90 %.
6. **Mora ≥ 30 días**: afectado → `sigmoide(−2,2 + 5·carga/(1 − caída))`; no afectado → 1 %. La carga es cuota/ingreso.

Consecuencia: el mapa distrital explica parte de la afectación, pero hay varianza intra-distrito (prueba: desviación media entre sectores del mismo distrito > 0,10), microclima y ruido individual. Un modelo que use rasgos de sector, actividad y colchón debería superar a la regla de zona; **si no lo hiciera, es un resultado válido y se reporta**.

### b.4 Diagnóstico del dataset: el embudo (no es el modelo)

Calculado por `diagnostico_embudo()` y guardado en `manifest.json`. «Expuesto» = cliente en distrito `alto` o `muy_alto` del mapa visible para esa amenaza (la regla más simple posible).

| Evento | Amenaza | Severidad realizada | % saldo expuesto | P(afectado \| expuesto) | P(mora \| expuesto) | P(mora \| no expuesto) | % de la mora fuera de lo marcado |
|---|---|---|---|---|---|---|---|
| EB01 | lluvia | 0,45 | 36 % | 10 % | 4,4 % | 3,0 % | 53 % |
| EB02 | inundación | 0,97 | 29 % | 20 % | 8,7 % | 6,3 % | 65 % |
| EB03 | sequía | 0,85 | 23 % | 9,7 % | 4,8 % | 2,5 % | 62 % |
| EB04 | inundación | 0,70 | 29 % | 14 % | 5,4 % | 4,5 % | 67 % |
| EB05 | lluvia | 0,76 | 36 % | 26 % | 11 % | 5,4 % | 46 % |
| EB06 | sequía | 0,37 | 23 % | 6,4 % | 3,1 % | 2,4 % | 73 % |

Lectura: de lo «expuesto» solo entre 6 % y 26 % resulta afectado y entre 3 % y 11 % entra en mora; y entre 46 % y 73 % de la mora ocurre fuera de lo que la regla de zona marcó. **Eso es lo que la solución debe mejorar**. Son cifras del mundo sintético, no un hallazgo sobre la Caja.

### b.5 Fuentes climáticas y de amenaza públicas que podrían sustituir lo sintético **[POR CONFIRMAR con el owner]**

> **No se descargó ni se consultó nada** para este documento. Los nombres de entidades y productos salen de conocimiento general; hay que verificar que existan hoy, su formato, su licencia, su resolución y si la política de la Caja y las bases permiten usarlos (y declararlos como preexistente de terceros). Los datos públicos de peligro por distrito no son datos personales, pero igual hay que confirmarlo.

| Posible fuente | Qué aportaría | Reemplazaría a | Resolución esperada | Esfuerzo (supuesto) |
|---|---|---|---|---|
| SENAMHI (Perú) | Precipitación y temperatura observadas, pronósticos, índices de sequía | `eventos_historicos` / intensidades | Estación → distrito | Medio: limpieza e interpolación |
| CENEPRED / INDECI (Perú) | Escenarios y mapas de peligro por inundación y movimientos en masa; registro histórico de emergencias | `mapa_amenaza`, historia de eventos | Distrito o menor | Medio: formatos geoespaciales |
| ANA (Perú) | Zonas inundables, puntos críticos, información de cuencas | `sectores.dist_cauce_km`, peligro de inundación | Cuenca / tramo | Alto |
| ENFEN (Perú) | Comunicados e índices de El Niño costero para el escenario ex ante | `escenarios` | Regional | Bajo |
| INEI (Perú) | Ubigeo y límites distritales, censo agropecuario, indicadores distritales | `distritos`, perfiles de actividad | Distrito | Bajo–medio |
| MIDAGRI (Perú) | Calendario y estadística agraria | Estacionalidad de actividades agro | Provincia / región | Medio |
| MINAM / IGN (Perú) | Capas de hidrografía y relieve | `sectores` (pendiente, cauce) | Variable | Medio |
| Productos globales (precipitación satelital tipo CHIRPS, reanálisis tipo NASA POWER, inundación tipo GloFAS, índices de sequía tipo SPEI, modelos de elevación abiertos) | Series históricas y escenarios | Intensidades de eventos; terreno | ≈ 5–25 km (clima), ≈ 30 m (relieve) | Medio–alto |

Decisión propuesta (**supuesto**): llevar al evento solo datos sintéticos, y presentar una **ruta de sustitución** (qué tabla se reemplaza por qué fuente) como argumento de escalabilidad. Usar datos públicos reales exige descarga, licencia y declaración como preexistente; no es necesario para demostrar la funcionalidad y consume horas escasas.

---

## (c) Arquitectura

### c.1 Vista general

```
                     retos/RIE-01/datos/sintetico (CSV)  ──►  ETL (pandas)  ──►  SQLite
                     (o datos de la Caja, adaptador)                         │
                                                                             ▼
 ┌───────────────────────────── backend (FastAPI + Pydantic v2) ─────────────────────────────┐
 │ domain/escenarios   : escenario ex ante ──► muestras de severidad (p10/p50/p90, Monte Carlo)│
 │ ml/exposicion       : 3 capas ─ exposición → afectación → mora, por cliente y sector        │
 │ domain/priorizacion : lista priorizada bajo capacidad de gestores (optimización)            │
 │ llm/agente_acciones : plan por cliente/zona con evidencia, SIEMPRE con aprobación humana    │
 │ llm/provider.py     : interfaz intercambiable (Claude · OpenAI · local · determinista)      │
 └──────────────────────────────────────────────┬──────────────────────────────────────────┘
                                                │ REST
                       frontend (React + Vite + Tailwind): mapa · ranking · ficha · aprobación
                                                │
        scripts/evaluar_kpi.py: backtest con/sin la solución sobre backtest/  ──►  docs/validacion.md
```

### c.2 Modelo de exposición (tres capas, el corazón del concepto)

| Capa | Pregunta | Salida | Método (supuesto, a decidir en el evento) |
|---|---|---|---|
| 1. Amenaza local | ¿Qué tan probable es que el evento golpee **este** sector? | `amenaza_estimada` ∈ [0, 1] por sector y escenario | Combina mapa distrital (con su `error_estandar`) + rasgos de sector (`tipo_sector`, `dist_cauce_km`, `pendiente_pct`) + intensidad del escenario por zona; calibrada con `impacto_historico` |
| 2. Vulnerabilidad | Si golpea, ¿el ingreso de **este** negocio cae? | `P(afectado)` y caída esperada | Regresión logística o GBM sobre actividad × amenaza local × colchón; validación **temporal** (entrenar con eventos antiguos, validar en los recientes) y calibración de probabilidades |
| 3. Impacto crediticio | Si cae, ¿entra en mora? | `P(mora ≥ 30 d)` y mora incremental | `carga/(1 − caída)`; pérdida esperada incremental = `saldo × ΔPD × LGD` con LGD **[POR CONFIRMAR]** |

Salidas agregadas por escenario: **cartera expuesta** (saldo en amenaza alta), **cartera probablemente afectada** (Σ saldo × P(afectado)) y **mora incremental esperada**, cada una como p10–p50–p90. Los tres números nunca se funden en uno: ahí está la respuesta a «exposición no es pérdida».

### c.3 Escenarios
* Un escenario = tipo + severidad nominal + desviación. Se muestrean `B ≈ 200` severidades (Monte Carlo ligero), se propagan por zona y se recalcula la cartera ⇒ rangos. Si falta tiempo: rango analítico `±k·sd`.
* Se comparan sin reentrenar: el modelo se entrena **una vez** con historia; los escenarios solo cambian la entrada.
* **Límite declarado**: la incertidumbre modelada es la de severidad e intensidad por zona dentro de un escenario. No asignamos probabilidades a los escenarios ni generamos escenarios alternativos de cada amenaza: el analista compara escenarios, no los pondera. El expediente pide «considerar la incertidumbre de los escenarios climáticos»; esto es lo que cubrimos y lo que no.
* La incertidumbre se muestra en la interfaz (barra de rango, no un solo número) y se evalúa en el backtest (§e, M4).

### c.4 Mapa y priorización
* **Mapa**: puntos o burbujas por distrito y sector coloreados por cartera probablemente afectada; clic abre ranking de clientes de esa zona. Sin teselas externas (SVG/canvas) en la versión recortada; con teselas si hay internet y tiempo.
* **Priorización**: de `ranking por valor esperado` a **asignación bajo presupuesto**: maximizar mora evitada esperada por sol invertido, sujeto a `capacidad_visitas_semana` por agencia (`agencias.csv`) y al catálogo de acciones. Primera versión: voraz por razón beneficio/costo; mejora: programación lineal entera (SciPy) si hay tiempo.
* **Ficha de cliente**: por qué está en la lista (actividad, sector, colchón, carga), con evidencia trazable.

### c.5 Agente de acciones preventivas y proveedor de LLM

**Alcance del agente**: toma la lista priorizada de un escenario y propone, **para revisión humana**, qué acción aplicar a cada segmento o cliente y qué decir. No ejecuta acciones, no cambia condiciones de crédito, no contacta a nadie. La revisión humana es un criterio propio **(supuesto)**: los expedientes RIE-02 y RIE-03 la exigen, el de RIE-01 no la menciona. Sí exige que las recomendaciones se sustenten en evidencia y respeten la protección de datos y las políticas de riesgo de la Caja, y de ahí salen el campo `evidencia`, el uso de ids seudónimos y el catálogo cerrado de acciones **[POR CONFIRMAR con la Caja qué acciones permiten sus políticas de riesgo]**. También propone estrategias a nivel de zona o segmento, no solo por cliente, porque el reto habla de «estrategias preventivas».

Herramientas acotadas (solo lectura salvo el registro de la propuesta):

| Herramienta | Qué devuelve |
|---|---|
| `resumen_escenario(escenario_id)` | Cartera expuesta/afectada/mora con rangos |
| `clientes_prioritarios(zona, n)` | Lista seudonimizada con motivos |
| `catalogo_acciones(cliente_id)` | Acciones aplicables, costo, efectividad (rango) |
| `capacidad_agencia(agencia_id)` | Visitas disponibles |
| `registrar_propuesta(plan)` | Guarda la propuesta como «pendiente de aprobación» |

Salida: modelo Pydantic `PlanPreventivo` con acción, motivo, **evidencia** (campos usados), **incertidumbre**, costo estimado y `requiere_aprobacion=True`. Validación: acción dentro del catálogo; si no, se rechaza.

**Interfaz de proveedor** (`backend/app/llm/provider.py`; todo código nuevo, se escribe en el evento):

```python
class LLMProvider(Protocol):
    nombre: str
    def generar(self, sistema: str, mensajes: list[Mensaje], *,
                esquema: type[BaseModel] | None = None,
                temperatura: float = 0.0, max_tokens: int = 1024) -> RespuestaLLM: ...

# Implementaciones: ClaudeProvider · OpenAIProvider · LocalProvider (modelo local, p. ej. Ollama)
#                   DeterministaProvider  ← plantillas y reglas, sin LLM
# Selección por variable de entorno LLM_PROVIDER; Pydantic AI usa el proveedor vía adaptador.
```

* `DeterministaProvider` garantiza que **la demo funciona sin red ni claves** y que la funcionalidad crítica no depende de la política de IA externa. El LLM mejora la redacción y la explicación, no el cálculo.
* **Privacidad**: al LLM solo llegan ids seudónimos y variables agregadas o discretizadas; nada personal (no existe en el dataset). Si la política prohíbe IA externa **[POR CONFIRMAR]**, se usa `LocalProvider` o `DeterministaProvider`.
* Registro de cada llamada (entrada, salida, proveedor) en SQLite para la evidencia de validación.

### c.6 API (borrador)
`GET /escenarios` · `POST /escenarios/{id}/simular` (rangos + mapa) · `GET /zonas/{id}/clientes` · `POST /planes` (agente) · `POST /planes/{id}/decision` (aprobar/rechazar, con motivo) · `GET /kpi/backtest`.

---

## (d) Plan hora a hora del evento (4 personas × ≈ 8 h)

Agenda oficial: **Día 1** validación del enfoque 09:45; construcción 10:30–13:00 y 14:00–16:30; pruebas 16:30–17:30. **Día 2** construcción 09:30–12:00; validación final 12:00–12:45; **entrega 13:00**; pitch 15:00. Brutas ≈ 9,5 h; ≈ 1,5 h se van en coordinación, pausas y consultas a mentores, de ahí las 8 h netas.

**Revisión del esfuerzo del MVP** (v0 decía 32 h; se reparte distinto porque el generador de datos ya existe):

| # | Tarea | Horas v0 | Horas v1 | Responsable |
|---|---|---|---|---|
| 1 | Carga, validación e integración de datos sintéticos (el generador es preexistente) | 4 | 1,5 | Mariano 0,75 · Glem 0,75 |
| 2 | Modelo de amenaza local, vulnerabilidad e impacto (3 capas) | 4 | 4,5 | Glem |
| 3 | Escenarios y propagación con incertidumbre | 3 | 3,5 | Glem 2,0 · Antonio 1,5 |
| 4 | API FastAPI y persistencia | 3 | 2,5 | Mariano |
| 5 | Mapa y vista del gestor (React) + flujo | 4 + 2 | 4,0 + 1,5 | David |
| 6 | Agente de acciones preventivas y proveedor de LLM | 3 | 3,5 | Mariano |
| 7 | Backtest del KPI y `evaluar_kpi.py` | 3 | 4,0 | Antonio (con Glem) |
| 8 | Pruebas y `docs/validacion.md` | 2 | 2,5 | Glem 0,75 · Mariano 0,75 · Antonio 1,0 |
| 9 | Pitch y demo | 2 | 2,0 | David 1,5 · Antonio 0,5 |
| 10 | Criterios financieros y acciones (Caja Experts) | 2 | 1,0 | Antonio |
| | Colchón | — | 1,5 | Mariano 0,5 · David 1,0 |
| | **Total** | **32** | **32 (30,5 + 1,5)** | |

Cada persona queda en 8,0 h. El total no cambia porque el ahorro en datos (−2,5 h) se reinvierte en modelo, escenarios y backtest, que son los que puntúan.

**Plan por bloques**

| Bloque | Mariano (backend, agente) | Glem (datos, modelo) | Antonio (KPI, negocio) | David (UX, mapa, demo) |
|---|---|---|---|---|
| **D1 10:30–11:30** | Esqueleto FastAPI, contratos Pydantic, CSV → SQLite | Loader y chequeos; embudo de los datos | Fija escenarios, LGD, supuestos de acciones y fórmulas de los 4 KPI (los dos últimos solo si hay tiempo) | Flujo en wireframe (escenario → mapa → ranking → plan → aprobar); elige librería de mapa |
| **D1 11:30–13:00** | `/escenarios` y `/simular` con reglas simples | Amenaza local por sector (v0) calibrada con la historia | `evaluar_kpi.py`: líneas base B0–B3 y métricas M1–M3 | Selector de escenario, mapa por distrito, tabla |
| ▶ **Hito H1 (13:00)** | Datos en SQLite; un escenario devuelve cartera por distrito y el mapa lo pinta | | | |
| **D1 14:00–15:15** | Agente: herramientas y `DeterministaProvider` | Vulnerabilidad por cliente + impacto crediticio | Backtest v0 en un evento | Vista del gestor: ranking y ficha con «por qué» |
| **D1 15:15–16:30** | Proveedores LLM reales, esquema de salida, aprobación persistida | Monte Carlo (p10/p50/p90) | Backtest con modelo real; métrica de calibración M4 | Integración con la API; rangos en el mapa |
| ▶ **Hito H2 (16:30)** | **Rebanada vertical**: escenario → rangos → ranking → plan sugerido → aprobar. Si no está, se congela el alcance y se recorta (abajo) | | | |
| **D1 16:30–17:30** | Pruebas de API y agente | Pruebas del modelo (jerarquía, monotonía, semilla) | Backtest en los 6 eventos; primera tabla con/sin | Recorrido manual; lista de fallas de UX |
| ▶ **Hito H3 (17:30)** | KPI con/sin corriendo; `docs/validacion.md` v0; commit y etiqueta | | | |
| **D2 09:30–10:45** | Asignación bajo capacidad de gestores | Ablaciones: solo mapa / + sector / + actividad / + colchón | Sensibilidad a efectividad y costo (rangos); caso de negocio | Pulido de UI; escenario de demo guardado |
| **D2 10:45–12:00** | Integración extremo a extremo; arranque en un comando | Regresión y reproducibilidad con varias semillas | `validacion.md` final; lámina del KPI | Guion de demo y video de respaldo (30–60 s) |
| ▶ **12:00** | **Congelar funcionalidad** | | | |
| **D2 12:00–13:00** | Validación final con mentores; empaquetado y entrega (repo, docs, `preexistente.md` actualizado, historial) | Idem | Ensayo del pitch | Ensayo de demo |

**Disciplina de evidencia**: commits pequeños cada hito, mensajes descriptivos, nada de volcar el repo entero de golpe; los commits son la prueba de desarrollo en el evento.

**Qué recortar si falta tiempo** (en este orden; el núcleo no se toca)

| Orden | Recorte | Ahorro | Qué se pierde |
|---|---|---|---|
| 1 | Teselas del mapa ⇒ puntos en SVG | ≈ 1,0 h | Estética |
| 2 | Redacción con LLM ⇒ plantillas del `DeterministaProvider` | ≈ 2,0 h | Naturalidad; la demo sigue funcionando sin red |
| 3 | Monte Carlo ⇒ rango analítico `±k·sd` | ≈ 1,0 h | Rigor de la incertidumbre (se declara) |
| 4 | Optimización entera ⇒ voraz | ≈ 0,5 h | Calidad de la asignación |
| 5 | Sequía fuera del demo (queda en el backtest si ya existe) | ≈ 0,5 h | Variedad de escenarios |
| 6 | Resolución sector ⇒ solo distrito | ≈ 1,5 h | **Diferenciación**; último recurso |

**Núcleo no negociable** (da el 3/5 de funcionalidad crítica): escenario ex ante → cartera expuesta/afectada/mora con rango → ranking en mapa → plan con aprobación humana → backtest con un KPI frente a una línea base.

### d.2 Prueba pesimista de horas

Las 30,5 h (+ 1,5 h de colchón) son una estimación nuestra, no medida. Prueba: cada tarea × 1,4; el modelo (#2), los escenarios con Monte Carlo (#3) y el agente (#6) × 1,6 (son lo más incierto y lo que depende de aprender sobre la marcha). En el escenario pesimista el colchón desaparece (se lo come la sobrecarga).

| Tarea | v1 | Factor | Pesimista |
|---|---|---|---|
| 1 Datos | 1,5 | 1,4 | 2,1 |
| 2 Modelo (3 capas) | 4,5 | 1,6 | 7,2 |
| 3 Escenarios + Monte Carlo | 3,5 | 1,6 | 5,6 |
| 4 API | 2,5 | 1,4 | 3,5 |
| 5 Mapa + flujo del gestor | 5,5 | 1,4 | 7,7 |
| 6 Agente + proveedor LLM | 3,5 | 1,6 | 5,6 |
| 7 Backtest y KPI | 4,0 | 1,4 | 5,6 |
| 8 Pruebas y validación | 2,5 | 1,4 | 3,5 |
| 9 Pitch y demo | 2,0 | 1,4 | 2,8 |
| 10 Criterios financieros | 1,0 | 1,4 | 1,4 |
| **Total** | **30,5** | | **45,0** |

**Resultado: 45,0 h-persona frente a 32 h netas disponibles: faltan 13 h (41 % de exceso).** Ni siquiera caben en las ≈ 38 h brutas de la agenda (4 × 9,5 h) sin pausas ni consultas.

Por persona, con el reparto actual: Glem **12,5 h** (modelo, escenarios y pruebas del modelo: es el cuello de botella), Antonio **11,5 h**, Mariano **11,2 h**, David **9,8 h**; contra 8 h cada uno. Equilibrado a partes iguales serían 11,25 h por persona, así que además de recortar hay que **pasar trabajo de Glem a Mariano y David** (p. ej. escenarios a Antonio por completo).

**Recortes de la lista que se activan** (ahorro recalculado con los factores pesimistas):

| Orden | Recorte | Ahorro pesimista |
|---|---|---|
| 1 | Teselas del mapa ⇒ puntos en SVG | 1,4 h |
| 2 | Redacción con LLM ⇒ plantillas deterministas | 3,2 h |
| 3 | Monte Carlo ⇒ rango analítico | 1,6 h |
| 4 | Asignación entera ⇒ voraz | 0,7 h |
| 5 | Sequía fuera de la demo | 0,7 h |
| 6 | Sector ⇒ solo distrito | 2,4 h |
| | **Subtotal de la lista** | **10,0 h** → quedan 35,0 h, **aún 3,0 h sobre 32** |

**Recortes adicionales necesarios** (no estaban en la lista original; se agregan a ella):

| Recorte | Ahorro pesimista | Costo |
|---|---|---|
| Backtest en 3 eventos (uno por amenaza, uno severo), sin réplica por semillas ni ablaciones, y solo K1 y K2 (sin K3 ni K4) | 2,1 h | Menos evidencia y sin continuidad de negocios (K4) |
| Aprobación sin persistir (en memoria) y ficha de cliente reducida a una fila expandible | 1,4 h | Menos trazabilidad |
| Capa 3 simplificada: `P(mora \| afectado)` por actividad y tramo de carga, tomada de la historia, en lugar de un modelo | 1,6 h | Se pierde parte de la diferenciación de las tres capas |
| **Subtotal** | **5,1 h** | → **29,9 h**, dentro de las 32 h con 2,1 h de holgura |

**¿Se sostiene el mínimo de 3/5 de funcionalidad crítica?** Honestamente: **solo con los 9 recortes y sin margen real.** Con todo aplicado queda un flujo completo pero mínimo: escenario, dos capas completas más una tercera simplificada, rangos analíticos, mapa de puntos, ranking con aprobación en memoria, agente determinista (reglas y plantillas) y backtest de K1 y K2 en 3 eventos. Eso funciona de punta a punta y debería alcanzar 3/5 en funcionamiento, **si la rebanada vertical (hito H2, 16:30 del día 1) está viva**. Pero:
- El agente quedaría sin LLM: puede leerse como un motor de reglas y debilitar «agentes de IA» en viabilidad y diferenciación. El valor técnico recaería en el modelo calibrado y la asignación.
- La holgura de 2,1 h es menor que la pérdida de un solo integrante durante dos horas (hay dos primeras participaciones en hackathon).
- **No se sostiene** si el modelo (#2) no está funcionando al terminar el día 1 (16:30 + pruebas): sin él, el mapa y el agente no tienen qué mostrar, y esa es la causa más probable de caer bajo 3/5.
- **No se sostiene** si además la interfaz del mapa (#5, 7,7 h pesimistas) se complica: ya está al máximo de su recorte.

Reglas de decisión para el evento: (i) si en H1 (13:00) los datos no están cargados y un escenario no devuelve cartera por distrito, se aplican de inmediato los recortes 1–6; (ii) si en H2 (16:30) no hay rebanada vertical, se aplican los recortes adicionales y se congela el alcance; (iii) si en H3 (17:30) el backtest no corre, el día 2 se dedica solo a que corra en un evento y a la demo.

### d.3 ¿Es el de mayor alcance de los cuatro y por qué es arriesgado?

Con las horas revisadas en cada panorama (estimaciones propias de cada sesión, sin verificar): RIE-01 30,5 h de trabajo + 1,5 de colchón; RIE-03 31,5 h de 32; RIE-02 29 h; NEG-02 27 h (de 35 antes). Por horas **empata con RIE-03 en lo más alto**. Por **ancho** es el de mayor alcance: reúne siete piezas que deben encajar (datos geoespaciales, modelo en tres capas, escenarios con muestreo, mapa interactivo, optimización de asignación, agente con proveedor intercambiable y backtest con verdad oculta), y sus dos piezas más visuales (mapa y escenarios) son las que más cuestan en tiempo de interfaz.

Qué lo hace arriesgado para un equipo con dos personas en su primer hackathon:
1. **Mapa interactivo**: el trabajo de interfaz es el más grande de los cuatro y recae en David (primer hackathon). Un bloqueo con la librería de mapa consume horas sin mejorar el KPI.
2. **Incertidumbre**: Monte Carlo, calibración y rangos exigen criterio estadístico que hay que ejercer a la vez que se programa; el peso cae en Glem, que no tiene experiencia financiera.
3. **Dominio**: elegir actividades sensibles, LGD, costos y acciones requiere criterio financiero; Antonio (primer hackathon, menos de un año de experiencia) es el único con sector financiero y también lidera backtest y negocio.
4. **Backtest sintético**: se puede percibir como un examen escrito por nosotros mismos. Es el criterio de «pruebas y evidencia» (15 %) y el riesgo de credibilidad más delicado.
5. **Dependencia en cadena**: mapa, ranking y agente dependen del modelo; un retraso en el modelo bloquea al resto.
6. **Cuello de botella**: Glem pasaría de 8 a 12,5 h en el escenario pesimista.

Qué lo hace menos arriesgado: los datos ya existen y están probados; el flujo es secuencial y fácil de recortar por capas; la demo no depende de internet ni de un LLM externo.

**Decisión que necesita el equipo (para el día 21–22):** confirmar, antes de postular, que si RIE-01 llega a la final se acepta de antemano la **versión mínima** de §d.2 (agente determinista, mapa de puntos, backtest de 3 eventos con K1 y K2). Si el equipo prefiere no aceptar ese techo, RIE-01 no debería ser el desafío elegido frente a uno de menor ancho.

---

## (e) Diseño del backtest del KPI contra eventos simulados

### e.1 Objetivo y KPI
Medir, sobre eventos con verdad conocida, si la solución **identifica antes** la cartera que luego se deteriora y cuánto se reduce el daño con acciones. Son los 4 KPI candidatos del concepto (K1–K4) (**supuesto, a validar con el owner**); el KPI oficial y su línea base son **[POR CONFIRMAR]** y no se inventan.

Notación: `S_i` saldo total del cliente, `A_i` afectado, `M_i` incumple ≥ 30 días, `L(K)` lista priorizada ex ante de tamaño K.

| KPI | Definición | Candidato del concepto |
|---|---|---|
| **K1 Cobertura anticipada** | `Σ_{i∈L} S_i·A_i / Σ_i S_i·A_i` | «% de cartera expuesta identificado anticipadamente por escenario» |
| **K2 Precisión de priorización** | `precisión@K = media_{i∈L}(M_i)`; `lift = precisión / tasa base del evento`; captura de saldo en mora `Σ_{i∈L} S_i·M_i / Σ_i S_i·M_i` | «Precisión de la priorización frente a eventos simulados» |
| **K3 Pérdida evitada (estimada)** | `Σ_{i∈L} S_i·M_i·LGD·ef(a_i) − Σ_{i∈L} costo(a_i)`, con `ef` entre `efectividad_min` y `efectividad_max`; se reporta como **rango** | «Pérdida esperada evitada con acciones preventivas (estimada)» |
| **K4 Continuidad de negocios afectados** (resultado esperado: «proteger la continuidad de los negocios») | Entre clientes con `A_i = 1`, % con `M_i = 0`, con y sin acciones (acciones simuladas con `efectividad_min`/`max`); es la resiliencia del cliente, no de la cartera | Candidato nuestro; no estaba en el v0 |

Métricas de apoyo: **M4 calibración** (cobertura del intervalo p10–p90 de la mora total del evento, esperada ≈ 80 %, y curva de calibración de `P(afectado)`); **M5 falsos positivos** (% de la lista que no resultó afectada); **M6 degradación por severidad** (K1/K2 en eventos moderados vs severos).

### e.2 Líneas base («sin la solución»)
| Línea | Qué hace | Por qué |
|---|---|---|
| **B0 Azar** | Lista aleatoria del mismo tamaño (esperanza analítica) | Piso |
| **B1 Regla de zona** | Clientes de distritos `alto`/`muy_alto` del mapa visible, por orden de saldo | Lo que haría un analista con un mapa |
| **B2 Zona + actividad** | B1 restringida a actividades sensibles (`es_sensible_clima`) | Regla sencilla con criterio de negocio |
| **B3 Por saldo** | Mayores saldos primero | Gestión por monto |
| **Real de la Caja** | Cómo se identifica hoy la cartera expuesta | **[POR CONFIRMAR]** con el owner; mientras tanto B1 y B2 son **proxies nuestros**, no la línea base oficial |

### e.3 Procedimiento
1. **Congelar el corte** (`fecha_corte`) y el escenario ex ante de cada evento (`eventos_backtest.escenario_id`). El modelo **no ve** `severidad_realizada`.
2. **Calibrar** solo con `eventos_historicos` + `impacto_historico`. Prohibido leer `backtest/` antes de este paso; el código de evaluación es el único que lo abre (prueba que lo verifique).
3. **Predecir** cada evento activando el escenario ex ante y obtener rangos y `L(K)`.
4. **Presupuesto K**: (i) por capacidad: `Σ capacidad_visitas_semana × 2 semanas` ≈ 8 % de los clientes con los valores por defecto (**supuesto**); (ii) curva con K = 5 %, 10 %, 20 % del saldo, y área bajo la curva de captura.
5. **Medir** K1–K3 y M4–M6 por evento, con las líneas base al mismo K.
6. **Replicar en varios mundos**: repetir con, por ejemplo, 20 semillas del generador y reportar media ± desviación; así un resultado no depende de un sorteo.
7. **Reportar** en `docs/validacion.md`: tabla con/sin por evento, K3 como rango, ablaciones y fallas.

Criterio interno de aceptación (**supuesto**; no es un objetivo de impacto): la solución supera a B1 y B3 en captura de saldo en mora al mismo K en al menos 5 de 6 eventos; no queda por debajo de B2 más allá del ruido entre semillas; logra un *lift* de al menos 2× sobre el azar (B0) con la capacidad real de visitas; y el intervalo p10–p90 cubre la mora total en al menos 4 de 6. Si no se cumple, se reporta tal cual y se explica. Ajustado el 24.11 con la auditoría de datos (`docs/investigacion/06-auditoria-datos.md`): el dataset es ruidoso (techo ≈ 24 % de captura con visitas de dos semanas frente a ≈ 8 % del azar), por lo que se promete *lift* moderado y no una detección casi perfecta.

### e.4 Cómo evitar un backtest circular
* La verdad se genera con **variables ocultas** (microclima por sector y evento, ruido individual) y el mapa visible tiene error: ningún modelo llega al 100 %.
* Eventos de backtest **distintos** de los históricos; al menos tres con severidad mayor que cualquier evento histórico (prueba de extrapolación).
* Si el modelo del evento usa la misma forma funcional que el generador, el resultado favorece al modelo. Se declara como limitación y se mitiga con ablaciones y con una variante «mundo alternativo» (cambiar sensibilidades en el generador y volver a medir).
* Con datos reales, la calibración y el backtest se repetirían con historia de la Caja **[POR CONFIRMAR]**; lo sintético prueba la **mecánica**, no el nivel de impacto.

---

## (f) Riesgos y mitigaciones

| Riesgo | Efecto | Mitigación |
|---|---|---|
| **Exposición no es pérdida** | Alarmar con números enormes (todo saldo en zona de riesgo) y perder credibilidad | Tres capas separadas; el titular es «probablemente afectada» y «mora incremental» con rango; «expuesta» solo como contexto; el embudo del dataset se muestra en la demo |
| **Incertidumbre de escenarios** | Un escenario no es un pronóstico; una cifra única engaña | Rangos p10–p50–p90; probar con eventos realizados distintos al ex ante; el agente cita siempre el rango |
| **Datos geográficos y climáticos de baja calidad** (riesgo propio; el expediente solo dice que los datos son referenciales y sin compromiso de entrega) | Ubicación imprecisa, mapas gruesos | Modelar el error del mapa, caer a distrito cuando falta sector, y reportar sensibilidad al error |
| **Políticas de riesgo y protección de datos de la Caja** (expediente) | Una recomendación que la política no permite, o un dato personal en un lugar indebido | Catálogo cerrado de acciones **[POR CONFIRMAR]** con la Caja; el agente rechaza lo que no esté en el catálogo; solo ids seudónimos hacia el LLM; revisión con Compliance y Legal de los Caja Experts |
| **Recomendaciones sin evidencia** (expediente) | Un gestor no puede defender la sugerencia | Cada propuesta lleva `evidencia` (variables y valores usados), rango de incertidumbre y fuente del escenario; sin evidencia, no se emite |
| **Medir solo la cartera y no la resiliencia del cliente** (resultado esperado del expediente) | El KPI se lee como «cobranza», no como protección del negocio | K4 de continuidad de negocios afectados; acciones de continuidad, capital de reposición y microseguro en el catálogo |
| **Backtest circular** | El jurado desconfía del KPI | §e.4; declarar que es mundo sintético; ablaciones; semillas múltiples |
| **Sobreajuste a un solo escenario** | Funciona en la demo y no en otros | 6 eventos, 3 amenazas, extrapolación a severidad mayor |
| **Parámetros de acciones inventados** (efectividad, costo, LGD) | K3 se lee como impacto real | Rangos, etiqueta «supuesto», sensibilidad, validar con owner; K3 nunca se presenta como cifra única |
| **Política de IA externa** | Prohíben LLM externo | `DeterministaProvider` y `LocalProvider`; el cálculo no depende del LLM |
| **Decisiones automáticas de crédito** | Incumple la restricción del expediente | El agente solo propone; aprobación humana registrada; ninguna acción se ejecuta |
| **Sesgo y equidad** | Penalizar zonas pobres por vivir en zonas de riesgo (se restringe el crédito) | El objetivo es **proteger** (prevenir) no **restringir**; acciones de apoyo, no de rechazo; revisar con Compliance **[POR CONFIRMAR]** |
| **Mora basal confundida con efecto del evento** | Atribuir al clima lo que ya ocurría | El generador incluye 1 % de mora basal; el backtest la reporta; con datos reales se usaría diferencia contra periodo previo |
| **Falta de tiempo** (≈ 8 h por persona) | Rebanada vertical incompleta | Hitos H1–H3, orden de recortes, núcleo definido |
| **Preexistente mal declarado** | Descalificación o pérdida de puntos | §h y §j; el modelo, mapa y agente se construyen y se commitean en el evento |
| **Datos públicos con licencia o política poco claras** | Problemas legales | No usarlos en el evento; ruta de sustitución solo documentada |

---

## (g) Preguntas para el owner (Miriam, según la plataforma)

Prioridad 1 (cambian el diseño):
1. **KPI oficial y línea base**: ¿cuál es el indicador y cómo se mide hoy la exposición o pérdida por eventos climáticos? ¿Quién lo calcula y con qué frecuencia?
2. **Datos**: ¿entregan datos sintéticos? ¿con qué tablas, columnas y volumen? ¿incluyen ubicación del cliente (ubigeo, coordenadas o solo agencia)?
3. **IA externa**: ¿se permite un proveedor externo de LLM o solo modelos locales?
4. **Acciones viables**: ¿cuáles puede tomar la Caja ante un evento (alerta, visita, reprogramación, ampliación de plazo, capital de reposición, microseguro)? ¿Cuáles requieren comité o normativa?

Prioridad 2:
5. **Fuentes**: ¿qué fuentes climáticas y mapas de amenaza podemos usar (públicas o sintéticos de la Caja)? ¿Se permite usar datos públicos reales con clientes sintéticos?
6. **Historia**: ¿hay registro de eventos pasados y su efecto en mora, aunque sea agregado por distrito?
7. **Actividad económica**: ¿qué clasificación se usa (CIIU, rubro interno) y existe estacionalidad de ingresos?
8. **Amortiguación**: ¿se registra seguro, ingresos secundarios o reservas del cliente?
9. **Capacidad**: ¿cuántos gestores por agencia y cuántas visitas por semana son realistas?
10. **Alcance de decisión**: ¿qué aprobación existe hoy para una reprogramación preventiva y qué implica para la calificación? (**[POR CONFIRMAR]** con Compliance y la normativa vigente de la SBS.)
11. **Flujo del gestor**: ¿qué sistema usa hoy y dónde se mostraría la alerta?
12. **Formato**: ¿cuál es el formato exacto del concepto en la plataforma y la hora límite del 26.11?

---

## (h) Preexistente vs. nuevo en el evento

| Componente | Estado | Titular / condiciones | Dónde |
|---|---|---|---|
| Generador de datos sintéticos RIE-01 | **Preexistente** | Equipo; sin datos reales; sin código de empleadores | `retos/RIE-01/datos/generar.py` |
| Pruebas del generador (40) | **Preexistente** | Equipo | `retos/RIE-01/datos/test_generar.py` |
| CSV generados | **Preexistente** | Equipo; sintéticos; confidenciales mientras el repo sea privado | `retos/RIE-01/datos/sintetico/` |
| Estructura del repo, bibliotecas abiertas (FastAPI, pandas, scikit-learn, React, SciPy, etc.) | Preexistente (terceros) | Licencias abiertas | — |
| Este panorama y el concepto | Documentación previa | Equipo | `retos/<ID>/panorama.md`, `retos/<ID>/concepto.md` |
| Carga de datos y ETL a SQLite | **Nuevo** | Evento | `backend/app/` |
| Modelo de amenaza local, vulnerabilidad e impacto (3 capas) | **Nuevo** | Evento | `backend/app/ml/` |
| Escenarios y propagación con incertidumbre | **Nuevo** | Evento | `backend/app/domain/` |
| Priorización bajo capacidad | **Nuevo** | Evento | `backend/app/domain/` |
| API FastAPI | **Nuevo** | Evento | `backend/app/api/` |
| Agente y `provider.py` | **Nuevo** | Evento | `backend/app/llm/` |
| Mapa, ranking, ficha y aprobación (React) | **Nuevo** | Evento | `frontend/` |
| `evaluar_kpi.py`, `docs/validacion.md`, pruebas del producto | **Nuevo** | Evento | `scripts/`, `backend/tests/`, `docs/` |
| Pitch y demo | **Nuevo** | Evento | — |

Regla: ningún archivo del modelo, escenarios, mapa, agente o API existe antes del 03.12. El generador y sus datos son herramientas generales y no contienen la funcionalidad crítica (el único cálculo que incluye es un diagnóstico de calidad del dataset: el embudo, §b.4).

---

## (i) Plan de pruebas

| Nivel | Qué se prueba | Herramienta | Estado |
|---|---|---|---|
| **Datos** (hecho) | Reproducibilidad, integridad, rangos, ausencia de datos personales, sin red, embudo exposición ≠ pérdida, mapa informativo pero imperfecto, historia menos severa que backtest, colchón protege | `pytest` en `retos/RIE-01/datos` | **40 pruebas, pasan** |
| **Modelo** (evento) | Monotonía (más amenaza o sensibilidad ⇒ más afectación esperada); jerarquía `expuesta ≥ afectada ≥ mora`; saldos suman; calibración (Brier, curva) en validación temporal; invariancia a ids; semilla | `pytest` | Pendiente |
| **Escenarios** | Rangos ordenados p10 ≤ p50 ≤ p90; severidad mayor ⇒ cartera afectada ≥; sd = 0 ⇒ rango degenerado | `pytest` | Pendiente |
| **Priorización** | Respeta `capacidad_visitas_semana`; no excede presupuesto; casos pequeños con óptimo conocido | `pytest` | Pendiente |
| **API** | Contratos Pydantic, códigos HTTP, escenarios inválidos, idempotencia de simulación | `pytest` + `httpx` | Pendiente |
| **Agente** | Nunca ejecuta acciones; solo acciones del catálogo; salida válida contra el esquema; funciona con `DeterministaProvider` sin red; no envía datos personales al LLM; registra propuesta como pendiente | `pytest` con proveedor simulado | Pendiente |
| **Backtest** | Métricas con casos manuales (p. ej. 4 clientes con respuesta conocida); no lee `backtest/` en la fase de calibración | `pytest` | Pendiente |
| **Extremo a extremo** | Escenario → mapa → plan → aprobación, con datos del generador | Script de humo | Pendiente |
| **Regresión de KPI** | El KPI no empeora entre commits en 3 semillas | `evaluar_kpi.py` | Pendiente |
| **Manual / UX** | Recorrido con David y Antonio; video de respaldo | — | Pendiente |

Reporte: `docs/validacion.md` con comandos, resultado de cada nivel, tabla con/sin por evento y fallas conocidas.

---

## (j) Entrada para `docs/preexistente.md`

> Texto propuesto para **añadir** en `docs/preexistente.md` (este panorama no lo edita; que lo incorpore quien coordine). Si hay varias entradas de otros desafíos, unificar el formato.

Agregar estas filas a la tabla principal:

```markdown
| `retos/RIE-01/datos/generar.py` | Generador de datos 100 % sintéticos para el desafío RIE-01 (clima): distritos y sectores del norte del Perú, clientes MYPE y créditos en S/, mapa de amenaza con error, escenarios, eventos históricos y eventos de prueba con verdad oculta. Reproducible con semilla, sin red. No contiene el modelo de exposición, escenarios operativos, mapa ni agente | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-01/datos/test_generar.py` | 40 pruebas del generador (integridad, reproducibilidad, ausencia de datos personales, embudo exposición ≠ pérdida) | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-01/datos/sintetico/` | CSV producidos por el generador (semilla 20261203, 12 000 clientes); incluye `backtest/` con la verdad de los eventos simulados | Equipo | 21.11.2026 | No (preexistente) |
```

Agregar en «Declaración»:

```markdown
- RIE-01: el generador y sus datos son herramientas generales preexistentes. Los coeficientes y parámetros del mundo sintético (sensibilidades, severidades, costos y efectividades de acciones) son supuestos propios del generador, no datos de la Caja. Distritos: nombres geográficos públicos con coordenadas aproximadas; la huella de agencias es sintética. La funcionalidad crítica (modelo de exposición en tres capas, escenarios con incertidumbre, mapa, priorización, agente y `app/llm/provider.py`, backtest) se desarrolla durante la fase presencial y no figura en esta lista.
- Si se usaran fuentes climáticas o de amenaza públicas (SENAMHI, CENEPRED/INDECI, ANA u otras), se declararán aquí con su titular y licencia **[POR CONFIRMAR]**; hoy no se usa ninguna.
- Nota de transparencia **[POR CONFIRMAR]**: decidir como equipo si se declara que el generador se escribió con asistencia de herramientas de IA (las bases leídas no lo exigen).
```

---

## Cotejo con el expediente

Comparado palabra por palabra con `retos/RIE-01/expediente.md` (texto literal, actualizado por la Caja el 19.11, 12:04 p. m.), contra el concepto (`retos/RIE-01/concepto.md`) y este panorama. Resultado: **7 desviaciones por atribución o dilución (D1–D7) y 5 huecos de cobertura (H1–H5)**, todas corregidas o declaradas.

### Desviaciones encontradas (versión de la primera entrega) y corrección

| # | Dónde | Qué decía | Qué dice el expediente | Corrección |
|---|---|---|---|---|
| D1 | Concepto §1; panorama (a) | Atribuía al expediente que «la Caja no siempre anticipa qué parte de su cartera está expuesta» | No lo dice. Venía del borrador v0 generado | Quitada la atribución; ahora el concepto afirma que el expediente no dice cómo se identifica hoy y lo deja **[POR CONFIRMAR]** |
| D2 | Concepto §1; panorama (a) | «afectan los ingresos y la capacidad de pago» (categórico) | «pueden afectar […] potencialmente sus ingresos y capacidad de pago» | Texto ajustado a «pueden»/«potencialmente», con la pregunta de innovación y el resultado esperado citados |
| D3 | Concepto §1; panorama (a) | «sobre todo en zonas vulnerables» | «especialmente de aquellos ubicados en zonas vulnerables **o que desarrollan actividades sensibles al clima**» | Añadida la segunda condición. El modelo ya la cubría (sector y actividad) |
| D4 | Concepto §1; panorama resumen, (a) y (f) | Atribuía al expediente el riesgo «calidad de datos geográficos y climáticos» | No está. Solo dice que los datos son «referenciales» y sin compromiso de entrega. Venía de `riesgos_clave` del v0 | Reclasificado como riesgo **propio**; citada la nota de datos referenciales |
| D5 | Concepto §1; panorama (c.5), (f) | Diluía la sección «Riesgos»: faltaban «sustentarse en evidencia», «protección de datos» y **«políticas de riesgo de Caja Trujillo»**; esta última no tenía mecanismo | Las tres son exigencias textuales | Las tres citadas; mecanismos: campo `evidencia` obligatorio, ids seudónimos, **catálogo cerrado de acciones [POR CONFIRMAR] con la Caja**; filas nuevas en riesgos; revisión con Compliance y Legal |
| D6 | Concepto §1; panorama (c.5) | Atribuía la revisión humana a «los desafíos de riesgo» como restricción de este | RIE-01 **no** la menciona (RIE-02 y RIE-03 sí) | Se mantiene como criterio propio, etiquetado **(supuesto)** y con la fuente real |
| D7 | Concepto §4 | «lo que el expediente exige más allá de un tablero» | El bloque «Complejidad tecnológica» de RIE-01 **no se había capturado** | Capturado el 24.11: pide capacidades avanzadas con valor real y desarrollo funcional; el concepto §4 se alineó |

### Huecos de cobertura

| # | Elemento del expediente | Estado antes | Corrección |
|---|---|---|---|
| H1 | Resultado esperado: «fortalecer la **resiliencia de los clientes** […] proteger la **continuidad de los negocios**» | Solo se medía la cartera (K1–K3) | Nuevo **K4** (continuidad de los negocios afectados); lenguaje de «resiliencia»; acciones de continuidad, capital de reposición y microseguro |
| H2 | «desarrollar **estrategias** preventivas» | Acciones solo por cliente | El agente propone también a nivel de zona o segmento |
| H3 | Mecanismos de daño: infraestructura, inventarios, acceso a mercados, interrupciones | No se mencionaban | Declarado: se resumen en la caída de ingreso; no se modela por separado el acceso a mercados ni la infraestructura **(supuesto)** |
| H4 | «**Información climática**» como insumo | Solo escenarios e intensidades por zona | Declarado: entra como escenario; series observadas son ruta de sustitución **[POR CONFIRMAR]** |
| H5 | «**Incertidumbre de los escenarios**» | Cubierta para severidad e intensidad | Límite declarado en §c.3: no asignamos probabilidades a los escenarios ni generamos escenarios alternativos |

### Lo que sí coincide
* **Dato literal:** Desafío de Riesgos, owner Miriam, eje 4 «Inclusión financiera y resiliencia». ✔
* **Insumos del expediente** (ubicación, actividad, información climática, mapas de amenazas, escenarios, exposición crediticia, datos sintéticos): cubiertos con las salvedades H4 y la nota de «datos referenciales». ✔
* **«Exposición no implica pérdidas ni incumplimiento»:** el expediente nombra dos cosas distintas, pérdida económica del negocio e incumplimiento crediticio. Las tres capas las separan: *afectada* (pérdida económica del negocio, medida como caída de ingreso), *mora* (incumplimiento), y *expuesta* solo como contexto. Un riesgo de dilución que sí existía: el KPI candidato del v0 («% de cartera **expuesta** identificado») se leía como si exposición fuera daño; **K1 ahora se define sobre cartera afectada**, no expuesta. ✔
* **Incertidumbre de escenarios:** rangos p10–p50–p90, eventos de backtest distintos del escenario ex ante y eventos más severos que la historia (con el límite H5). ✔

### Pendiente de confirmar en la plataforma
Si los expedientes se actualizaron después del 19.11; formato del concepto y hora límite del 26.11.
