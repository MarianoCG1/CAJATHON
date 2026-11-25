---
tipo: reto
id: RIE-03
prioridad: 1
estado: Listo para revisión cruzada
avance: 6/6
pareja: David + Mariano
revisor: Glem
actualizado: 2026-11-21
---

<!-- AUTO:inicio (no editar; se regenera) -->

# RIE-03 · Anticipar el deterioro de pago antes del atraso

Volver al [[boveda/00-HUB-Cajathon|HUB]] · [[boveda/Tablero|Tablero]]

**Estado:** Listo para revisión cruzada · **Prioridad:** #1 · **Eje:** 3 Riesgo, fraude y recuperaciones inteligentes
**Pareja líder:** David + Mariano · **Revisor:** Glem · **Owners (plataforma):** Wilson, Harold, Paul

## Avance (automático)

- [x] Borrador v0 del concepto
- [x] Concepto v1 (editado por la pareja)
- [x] Panorama de abastecimiento
- [x] Cotejo con el expediente literal
- [x] Generador de datos sintéticos con pruebas
- [x] Texto de postulación

`██████ 6/6` · [POR CONFIRMAR]: 15 · (supuesto): 14 · postulación: 878 palabras

## Documentos

- Ficha del reto: [[retos/RIE-03/README|Ficha del reto]]
- Concepto: [[retos/RIE-03/concepto|Concepto]]
- Panorama de abastecimiento: [[retos/RIE-03/panorama|Panorama de abastecimiento]]
- Texto de postulación: [[retos/RIE-03/postulacion|Texto de postulación]]
- Generador de datos: `retos/RIE-03/datos/generar.py`
- Expediente literal (confidencial, solo local; no se sube al repo): `retos/RIE-03/expediente.md` — presente en este equipo

## Hipótesis de solución (supuesto)

Modelo de alerta temprana de deterioro de pago con explicación de señales y un agente que recomienda la intervención preventiva (canal, momento, propuesta), con revisión humana.

## KPI candidatos (supuesto, a validar con el owner)

- Tasa de paso a atraso a 30 días de la cartera alertada con intervención vs. sin intervención (backtest)
- Precisión de las alertas en el top-k diario y tasa de falsos positivos
- Días de anticipación promedio respecto del primer atraso

## Alcance estimado

33 h-persona de MVP en el borrador v0 (el panorama trae horas revisadas y el escenario pesimista).

## Riesgos clave

- Falsos positivos y fatiga de alertas
- Sesgos en el modelo
- No se pueden tomar decisiones crediticias automáticas

## Preguntas para el owner

- ¿Cómo define hoy la Caja el «deterioro» de un cliente MYPE y en qué momento se entera (días de atraso, calificación, visita)? ¿Con cuánta anticipación sería útil avisar: 30, 60 o 90 días?
- ¿Qué señales siguen hoy los analistas para sospechar que un cliente empeora, y cada cuánto las revisan?
- ¿Cómo se mide hoy la morosidad y la recuperación (mora > 8 días, > 30 días, cartera en riesgo)? ¿Cuál de esas medidas es la prioritaria para este desafío?
- ¿Cuántos clientes gestiona un analista al día y cuántos contactos preventivos son razonables sin saturar al cliente?
- ¿Qué puede ofrecer el analista por su cuenta (recordatorio, reprogramación, asesoría) y qué requiere comité? ¿Qué canales de contacto son aceptables?
- ¿En qué herramienta trabaja hoy el analista y dónde debería aparecer la alerta?
- ¿Qué esperan ver en la explicación de una alerta para confiar en ella?
- ¿Hay restricciones para usar IA externa (aun con datos sintéticos) o variables que no deben usarse por criterios de equidad?

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
