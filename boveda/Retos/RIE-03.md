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

`██████ 6/6` · [POR CONFIRMAR]: 15 · (supuesto): 14 · postulación: 754 palabras

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

- ¿Cuál es la morosidad actual de la cartera y cómo se mide (mora > 8, > 30 días)? ¿Cuál sería la mejora que consideran relevante?
- ¿Qué señales de deterioro monitorean hoy y con qué frecuencia?
- ¿Qué columnas y volumen tendrán los datos sintéticos (historial de pagos, saldos, actividad económica)?
- ¿Qué canales de contacto preventivo son viables para el gestor?
- ¿Hay restricciones para usar modelos de IA externos con datos sintéticos?

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
