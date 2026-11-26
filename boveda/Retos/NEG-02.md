---
tipo: reto
id: NEG-02
prioridad: 3
estado: Listo para revisión cruzada
avance: 6/6
pareja: Antonio + Mariano
revisor: David
actualizado: 2026-11-21
---

<!-- AUTO:inicio (no editar; se regenera) -->

# NEG-02 · Open Finance: competir en un ecosistema abierto

Volver al [[boveda/00-HUB-Cajathon|HUB]] · [[boveda/Tablero|Tablero]]

**Estado:** Listo para revisión cruzada · **Prioridad:** #3 · **Eje:** 5 Open Finance y nuevos modelos de competencia
**Pareja líder:** Antonio + Mariano · **Revisor:** David · **Owners (plataforma):** (ver plataforma)

## Avance (automático)

- [x] Borrador v0 del concepto
- [x] Concepto v1 (editado por la pareja)
- [x] Panorama de abastecimiento
- [x] Cotejo con el expediente literal
- [x] Generador de datos sintéticos con pruebas
- [x] Texto de postulación

`██████ 6/6` · [POR CONFIRMAR]: 16 · (supuesto): 13 · postulación: 1138 palabras

## Documentos

- Ficha del reto: [[retos/NEG-02/README|Ficha del reto]]
- Concepto: [[retos/NEG-02/concepto|Concepto]]
- Panorama de abastecimiento: [[retos/NEG-02/panorama|Panorama de abastecimiento]]
- Texto de postulación: [[retos/NEG-02/postulacion|Texto de postulación]]
- Generador de datos: `retos/NEG-02/datos/generar.py`
- Expediente literal (confidencial, solo local; no se sube al repo): `retos/NEG-02/expediente.md` — no está en este equipo; copiarlo de la plataforma

## Hipótesis de solución (supuesto)

Sandbox de Open Finance con APIs y consentimientos simulados que construye una vista 360 del cliente y un agente que detecta oportunidades de producto con su autorización.

## KPI candidatos (supuesto, a validar con el owner)

- Porcentaje de clientes con una oportunidad de producto identificada y consentida
- Mejora del conocimiento del cliente (completitud del perfil) con y sin datos multientidad
- Tasa de conversión estimada de las ofertas personalizadas (simulada)

## Alcance estimado

38 h-persona de MVP en el borrador v0 (el panorama trae horas revisadas y el escenario pesimista).

## Riesgos clave

- Privacidad y consentimiento
- No asumir APIs ni datos reales
- Normativa aplicable

## Preguntas para el owner

- ¿Qué busca ganar la Caja con Open Finance: conocer mejor al cliente, captar clientes de otras entidades, retener, incluir? ¿Cuál pesa más y cómo mediría el éxito de una oferta (aceptación, monto colocado)?
- ¿Se imagina a la Caja solo como receptora de datos de otras entidades o también como proveedora?
- ¿Qué reglas de consentimiento (alcance, vigencia, finalidad, revocación) deben respetar las ofertas hechas con datos de terceros? ¿Legal y Compliance revisarían el texto?
- ¿Qué productos de la Caja podrían ofrecerse a partir de esta información y con qué condiciones generales?
- ¿Qué datos propios de la Caja pueden usarse para ofertas sin pedir un consentimiento adicional?
- ¿Qué controles de seguridad esperan ver (autenticación entre entidades, auditoría, cifrado, retención)?
- ¿Se espera conformidad con algún estándar de APIs abiertas o basta un entorno de prueba coherente que simule el intercambio?
- ¿Hay restricciones para usar IA externa (aun con datos sintéticos)?

Las respuestas del owner actualizan KPI y línea base; el comunicado del 21.11 indica que en esta etapa no entregan datos.

<!-- AUTO:fin -->

## Notas del equipo (se conservan al regenerar)

### Seguimiento manual
- [ ] Preguntas enviadas al owner
- [ ] Respuesta del owner recibida (KPI y línea base)
- [ ] Revisión cruzada hecha por el revisor
- [ ] Decisión de postular este reto

### Notas
-
