# COM-01 — panorama: de qué se abastece la solución

> Complemento de `concepto.md`. Lo no oficial es **(supuesto)**.

## Qué dijo el owner (con nuestras palabras; ticket respondido el 25.11)

- No limita el segmento: la elección debe sustentarse con evidencia.
- Ya existen herramientas de prospección; se busca **complementarlas**.
- Priorizar captación de nuevos clientes; sumar conversión, desembolsos, costo de adquisición y primer acceso. El horizonte lo define el equipo.
- Nivel geográfico libre. Rutas, campañas, captación o puntos de atención son usos posibles, ninguno obligatorio.
- Fuentes: estadísticas oficiales, mapas, directorios y señales digitales públicas de negocios, respetando condiciones; sin recopilar datos personales sin autorización ni inferir características sensibles.
- Evitar exclusión por ubicación, género, edad, nivel socioeconómico, informalidad o poca presencia digital; no sacar conclusiones automáticas de la falta de información (la respuesta publicada quedó cortada en ese punto).
- No respondió sobre IA externa: se usa el criterio estricto (solo demo, datos sintéticos, sin conexión a sistemas de la Caja).

## Cotejo con el expediente

| El expediente pide | Cómo se atiende |
|---|---|
| Identificar y priorizar oportunidades | Potencial por zona y plan semanal |
| Zonas o segmentos poco explorados | Descubrimiento y cuota mínima de exploración |
| Mejorar la efectividad de la prospección | KPI por cada 100 visitas, frente a la costumbre |
| Mejores decisiones comerciales | Ficha con evidencia, incertidumbre y qué validar |
| Inclusión financiera | Primer acceso como indicador y reparto de visitas auditado |
| Protección de datos y condiciones de las fuentes | Unidad = zona; sin datos personales; licencias declaradas |
| No discriminar ni excluir | La falta de dato ensancha el rango; auditoría por tipo de zona |
| Señal no es necesidad confirmada ni elegibilidad | La ficha lo dice y las guardas lo impiden |
| Más que chatbot o dashboard | Planificador que aprende y agente acotado, integrados |

## Referencias externas

- Brown, Guin y Kirschenmann, expansión de agencias de ProCredit en Europa del Este: abrió más donde se concentraban hogares de bajos ingresos y la proporción de hogares bancarizados subió más en esas localidades ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2226522); leído solo el resumen que devolvió la búsqueda).
- [IFC, Data Analytics and Digital Financial Services](https://www.ifc.org/content/dam/ifc/doc/mgrt/ifc-data-analytics-and-digital-financial-services-handbook.pdf): los datos geoespaciales permiten cruzar demanda con cobertura de agentes y agencias (resumen de búsqueda).
- [Nota de prensa que cita a la SBS sobre La Libertad](https://www.trujilloesnoticia.com/2025/11/el-66-de-adultos-en-la-libertad-tiene.html): cita indirecta, por confirmar.
- No encontramos un caso peruano publicado con cifras de captación antes y después de usar analítica territorial. **No afirmar que existe.**

## Datos del prototipo

`datos/generar.py` produce 120 zonas ficticias (nombres de distritos reales de La Libertad como referencia), con señales públicas simuladas y huecos (más en zonas rurales), un historial de visitas sesgado hacia donde ya hay clientes y una verdad oculta solo para evaluar. Tres escenarios: `oculto`, `conocido`, `datos_pobres`.

```powershell
python retos/COM-01/datos/generar.py --escenario oculto
```

```powershell
python scripts/auditoria/auditar_com01.py --semillas 200
```

## Arquitectura

fuentes por zona → variables con fuente y fecha → modelo de potencial (creencia previa) → planificador (Beta-Binomial, Thompson, capacidad, exploración) → API y bitácora → interfaz (mapa, semana, ficha) → registro de resultados → actualización → backtest y equidad.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Los resultados dependen de supuestos del generador | Tres escenarios, incluido uno donde la costumbre gana |
| Pocas visitas por zona para aprender | Creencia previa y compartir información entre zonas parecidas |
| El analista no registra | Cuatro opciones, un toque; se muestra cuánto falta registrar |
| Datos públicos antiguos | Fecha visible; el rango lo refleja |
| Se percibe como reemplazo | La ruta habitual es una de las fuentes del plan |
| Exclusión de zonas rurales | Cuota de exploración y cuadro de reparto |
