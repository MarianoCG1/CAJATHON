---
tipo: reto
id: RIE-02
prioridad: 5
estado: Listo para revisión cruzada
avance: 6/6
pareja: David + Mariano
revisor: Antonio
actualizado: 2026-11-21
---

<!-- AUTO:inicio (no editar; se regenera) -->

# RIE-02 · Descubrir redes de riesgo ocultas

Volver al [[boveda/00-HUB-Cajathon|HUB]] · [[boveda/Tablero|Tablero]]

**Estado:** Listo para revisión cruzada · **Prioridad:** #5 · **Eje:** 3 Riesgo, fraude y recuperaciones inteligentes
**Pareja líder:** David + Mariano · **Revisor:** Antonio · **Owners (plataforma):** Carlos

## Avance (automático)

- [x] Borrador v0 del concepto
- [x] Concepto v1 (editado por la pareja)
- [x] Panorama de abastecimiento
- [x] Cotejo con el expediente literal
- [x] Generador de datos sintéticos con pruebas
- [x] Texto de postulación

`██████ 6/6` · [POR CONFIRMAR]: 28 · (supuesto): 16 · postulación: 726 palabras

## Documentos

- Ficha del reto: [[retos/RIE-02/README|Ficha del reto]]
- Concepto: [[retos/RIE-02/concepto|Concepto]]
- Panorama de abastecimiento: [[retos/RIE-02/panorama|Panorama de abastecimiento]]
- Texto de postulación: [[retos/RIE-02/postulacion|Texto de postulación]]
- Generador de datos: `retos/RIE-02/datos/generar.py`
- Expediente literal (confidencial, solo local; no se sube al repo): `retos/RIE-02/expediente.md` — presente en este equipo

## Hipótesis de solución (supuesto)

Detector de redes sospechosas entre personas, negocios, teléfonos, direcciones y dispositivos con análisis de grafos, que prioriza casos y entrega la evidencia a un investigador con ayuda de un agente.

## KPI candidatos (supuesto, a validar con el owner)

- Precisión y recall sobre redes de fraude inyectadas en datos sintéticos
- Reducción de falsos positivos frente a reglas simples
- Tiempo de preparación de un caso para el investigador

## Alcance estimado

36 h-persona de MVP en el borrador v0 (el panorama trae horas revisadas y el escenario pesimista).

## Riesgos clave

- Falsos positivos y reputación del cliente
- Protección de datos
- No concluir fraude solo por coincidencias

## Preguntas para el owner

- ¿Qué tipos de vínculos son más relevantes para la Caja (teléfono, dispositivo, dirección, referencia)?
- ¿Habrá casos simulados etiquetados para validar el detector?
- ¿Cuál es la tasa actual de falsos positivos y el tiempo de revisión por caso?

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
