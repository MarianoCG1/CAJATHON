---
tipo: decision
estado: vigente
fecha: 2026-11-21
---
# Decisión: datos sintéticos propios frente a datos reales

Volver al [[boveda/00-HUB-Cajathon|HUB]].

## Pregunta
¿No era más sencillo buscar datos reales?

## Decisión
Para el nivel de **cliente** (pagos, saldos, solicitudes, consentimientos) usamos **datos sintéticos propios**. Para capas de **contexto agregado** (clima, territorio, economía) se **evalúa** usar fuentes públicas reales, solo si se confirma licencia y que no contienen datos personales.

## Por qué no datos reales a nivel de cliente
1. **Está prohibido.** Bases §8.2: no se pueden usar datos personales reales, credenciales institucionales ni información restringida. Los datos reales de clientes de una caja no son públicos.
2. **No existen públicos con ese nivel de detalle.** No hay conjuntos abiertos de pagos por cliente de una microfinanciera peruana; los de otros países (p. ej. de créditos de consumo) son de otra población y otro producto.
3. **Necesitamos verdad de terreno.** Para medir el KPI hace falta saber qué cliente se deterioró desde cuándo, o qué solicitudes forman una red de fraude. Con datos reales ese dato no se conoce; en los sintéticos lo inyectamos y podemos medir anticipación y falsos positivos.
4. **La Caja evalúa con datos propios.** La organización comunicó que a los finalistas les dirán qué recursos ponen (posibles datos anonimizados o sintéticos). El prototipo debe poder cambiar de fuente; por eso cada generador mantiene un esquema que se puede sustituir.
5. **Reproducibilidad.** Con semilla fija, cualquiera regenera el mismo conjunto y las pruebas son estables.

## Dónde sí ayudarían datos públicos reales (a evaluar, [POR CONFIRMAR])
| Desafío | Capa | Fuentes públicas candidatas (verificar disponibilidad y licencia) |
|---|---|---|
| RIE-01 clima | Mapas de peligro, series e históricos de eventos | SENAMHI, CENEPRED/SIGRID, INDECI, ANA |
| COM-01 captación | Actividad económica, población, concentración de negocios | INEI (censos, directorio de empresas, indicadores) |
| Varios | Referencias de morosidad y estructura del sistema | SBS y BCRP (estadísticas agregadas) |

Reglas para usarlas: solo agregados sin datos personales; citar fuente y licencia; declararlas en [[docs/preexistente|Preexistente]]; no descargar nada sin decisión del equipo. Nada de esto reemplaza los datos a nivel de cliente.

## Riesgo que aceptamos
Un dataset sintético puede parecer un examen escrito por nosotros mismos. Mitigación: verdad separada, líneas base simples, señuelos y revisión de que una regla trivial no lo resuelva (en RIE-02 se detectó y se corrigió; falta revisar los otros tres).
