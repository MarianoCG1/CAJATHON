# NEG-01 — Tasas, seguros y cifras públicas de Caja Trujillo y la SBS

> Recopilado el 26.11.2026. Solo fuentes públicas. Cada cifra lleva su fuente y fecha. Lo que no se pudo confirmar va marcado **[POR CONFIRMAR]**. Uso: calibrar los supuestos del ejemplo y del banco de pruebas, y responder preguntas del jurado.

## Tasas activas de Caja Trujillo (SBS)

Fuente: SBS, «Tasa de interés promedio del sistema de cajas municipales», tasas activas anuales en moneda nacional de las operaciones del mes, **octubre 2026** (consultada el 26.11.2026).

| Tipo de crédito | CMAC Trujillo | Promedio de las cajas |
|---|---|---|
| **Microempresas** (total) | **47,87 %** | 40,22 % |
| Microempresas, cuota fija de 91 a 180 días | 58,32 % | 52,11 % |
| Microempresas, cuota fija de 181 a 360 días | **55,10 %** | 46,44 % |
| Microempresas, cuota fija a más de 360 días | 45,70 % | 38,00 % |
| **Pequeñas empresas** (total) | **22,05 %** | 23,01 % |
| Pequeñas empresas, de 181 a 360 días | 26,70 % | 27,23 % |
| Pequeñas empresas, a más de 360 días | 21,92 % | 22,28 % |
| Consumo (total) | 33,27 % | 33,66 % |

Otras referencias:
- SBS, promedio de **todo el sistema financiero** para microempresa al 01.11.2026: 58,05 % en moneda nacional (según el portal de estadísticas de la SBS, citado en prensa) **[POR CONFIRMAR en el portal]**.
- Ranking SBS de microempresa a cuota fija de 181 a 360 días (julio 2026 para cajas): las cajas van de cerca de 37 % a 62 % (Andina, Infobae, setiembre 2026).

**Uso en NEG-01:** el ejemplo usa una TEA ilustrativa de 40 %. Con la tasa real de Caja Trujillo para microempresa a 12 meses (55,10 %), las conclusiones se mantienen (ver `casos-de-prueba.md`, sensibilidad).

## Seguros (páginas de productos de Caja Trujillo)

| Concepto | Dato publicado | Fuente |
|---|---|---|
| Desgravamen, crédito microempresa | **0,105 % sobre el saldo de capital** (aseguradora La Positiva Vida); cobertura hasta los 77 años, permanencia hasta los 80 | Página de Crédito Microempresa de Caja Trujillo |
| Microempresa: seguros incluidos | Desgravamen y multirriesgo | Página de Crédito Microempresa Activo Fijo |
| Desgravamen en otros productos | 0,05 % (CrediTaxi, MAPFRE; convenios); 0,3309 % (Rapidiario) | Páginas de productos de Caja Trujillo |

**[POR CONFIRMAR]:** la periodicidad de la tasa de 0,105 % (en los casos se trata como mensual) y la tasa de multirriesgo vigente. La fuente oficial es el tarifario de Caja Trujillo.

## Tasa máxima del BCRP (Ley 31143)

- El BCRP fija un tope a la tasa de interés de los créditos de consumo y de micro y pequeña empresa, y lo actualiza cada seis meses. Desde noviembre de 2025 el tope en moneda nacional era de 113,16 % (prensa, oct. 2025). Una nota del BCRP de abril de 2026 anunció la siguiente actualización para el **01.11.2026**.
- **[POR CONFIRMAR]:** el tope vigente desde el 01.11.2026. La serie oficial está en estadisticas.bcrp.gob.pe («Tasa máxima de interés convencional compensatorio»).
- **Uso:** la TEA del motor es editable y se valida contra ese tope, como pidió el owner.

## Cifras de Caja Trujillo

| Dato | Valor | Fuente |
|---|---|---|
| Ratio de capital global | 18,07 %, el más alto del sistema de cajas municipales | Revista Economía (cierre de 2025) |
| Utilidad neta 2025 | S/ 51,2 millones (Revista Economía) o S/ 54 millones (entrevista en Gestión); **las fuentes no coinciden** | Prensa |
| Red de agencias | 106 tiendas | Gestión |
| Cartera, clientes y morosidad 2025 | **[POR CONFIRMAR]** en la memoria anual o en el boletín de cajas de la SBS | — |

## Clima (para los escenarios)

- ONI de NOAA, trimestre agosto–octubre de 2026: **+2,46**, que corresponde a El Niño fuerte (descargado el 25.11.2026).
- El estado oficial para el Perú lo dan los comunicados del ENFEN. **[POR CONFIRMAR]** el estado de alerta vigente.

## Fuentes

- SBS, tasas por tipo de crédito y caja municipal: https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIActivaTipoCreditoEmpresa.aspx?tip=C
- SBS, tasa promedio para microempresa: https://www.sbs.gob.pe/app/pp/EstadisticasSAEEPortal/Paginas/TIPMicroEmpresa.aspx?tip=B
- Caja Trujillo, crédito microempresa: https://www.cajatrujillo.com.pe/portalnew/creditos_microempresa_.html
- Caja Trujillo, microempresa activo fijo: https://www.cajatrujillo.com.pe/creditos_microempresa_activofijo.html
- Andina, ranking de tasas a microempresas: https://andina.pe/agencia/noticia-conoce-ranking-tasas-interes-prestamos-para-las-microempresas-1033963.aspx
- BCRP, nota informativa del 07.04.2026: https://www.bcrp.gob.pe/docs/Transparencia/Notas-Informativas/2026/nota-informativa-2026-04-07.pdf
- La República, tope de tasas (oct. 2025): https://larepublica.pe/economia/2025/10/14/bcrp-reduce-tope-de-tasas-y-las-mype-podrian-quedarse-sin-credito-por-que-y-de-que-se-trata-hnews-390306
- Revista Economía, resultados de Caja Trujillo 2025: https://www.revistaeconomia.com/caja-trujillo-cierra-este-2025-con-resultados-historicos-y-fortalece-su-solidez-financiera/
- Gestión, utilidades de Caja Trujillo 2025: https://gestion.pe/economia/empresas/caja-trujillo-reporta-record-historico-de-utilidades-de-s-512-millones-en-el-2025-noticia/
- NOAA CPC, ONI: https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
