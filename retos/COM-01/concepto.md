# Concepto de solución — COM-01 · Encontrar oportunidades donde otros no ven clientes

> **Versión 1** (25.11, noche). Lo marcado **(supuesto)** no viene de la Caja. Las cifras «medidas» son **sobre datos sintéticos propios**. Material confidencial: no publicar.

**Nombre:** Brújula comercial que aprende de cada visita.

**En una frase:** cada semana propone a cada analista dónde prospectar —combinando su ruta habitual con zonas poco exploradas—, explica qué sabe y qué no sabe de cada zona, y aprende del resultado de las visitas.

## 1. Problema abordado

La prospección se apoya en experiencia, referidos y conocimiento territorial. Eso es valioso, pero **se aprende sobre todo de donde ya se va**: una zona que no se visita no genera información, y la falta de información puede confundirse con falta de potencial. El reto pide identificar y priorizar oportunidades que hoy pueden pasar inadvertidas, con evidencia y sin exclusiones injustificadas.

Contexto público (cita indirecta, **confirmar en la SBS antes de usarlo en el pitch**): una nota de prensa de nov. 2025 que atribuye las cifras a la SBS indica que el 27 % de los adultos de La Libertad tiene un crédito en el sistema financiero, frente a 33 % nacional.

## 2. Concepto de solución

1. **Mapa de evidencia por zona comercial:** concentración de negocios, actividad económica, cobertura financiera, distancia y señales digitales públicas de negocios; cada dato con fuente y fecha, y marcando lo que falta.
2. **Potencial con incertidumbre:** probabilidad de que una visita termine en un cliente nuevo, con su rango. La falta de datos **ensancha el rango; no baja el puntaje**.
3. **Plan semanal que se adapta:** reparte las salidas entre la ruta que el analista ya haría y zonas de descubrimiento, con una cuota mínima para las menos conocidas. El reparto cambia según lo que va rindiendo cada fuente.
4. **Ficha de zona redactada por un agente acotado:** qué se sabe, qué no, qué validar en campo y cómo abordarla, citando las fuentes. No habla de personas ni de capacidad de pago.
5. **Registro de resultado en segundos** (sin interés, interesado, solicitó, desembolsado): la herramienta aprende de ello.
6. **Seguimiento de KPI y equidad:** captación por visita y reparto de visitas por tipo de zona y presencia digital.

El analista decide: puede quitar o cambiar zonas, y su motivo queda registrado.

**Diferenciación:** no es un mapa de calor ni un puntaje fijo. Sabe lo que no sabe, va a averiguarlo con una cuota acotada y comprueba si le está sirviendo frente a la forma habitual de prospectar.

## 3. Impacto esperado en el KPI

El owner recomienda priorizar la **captación de nuevos clientes**, con conversión, desembolsos, costo de adquisición y primer acceso como complementos; el horizonte lo define el equipo.

- **KPI principal:** clientes nuevos **por cada 100 visitas** (mismo esfuerzo comercial).
- **Complementarios:** conversión, desembolsos, costo por cliente nuevo, porcentaje que accede por primera vez (declarado al solicitar, agregado) y visitas a zonas poco atendidas.
- **Horizonte:** 12 semanas **(supuesto)**: doce ciclos de aprendizaje y tiempo para que una visita llegue a desembolso.
- **Validación en la Caja (después del hackathon):** con la misma capacidad, parte de las agencias usa el plan y parte trabaja como hoy.

### Evidencia preliminar (medida sobre datos sintéticos propios)

Mediana de 200 simulaciones por escenario; clientes nuevos por cada 100 visitas en 12 semanas.

| Escenario (supuesto sobre la realidad) | Solo cartera | Puntaje fijo | Solo descubrimiento | **Mezcla adaptativa** |
|---|---|---|---|---|
| Hay oportunidades ocultas | 7,3 | 11,0 | 12,4 | **11,6** |
| El potencial está donde ya hay clientes | 13,8 | 10,7 | 11,1 | **13,0** |
| Los datos públicos dicen poco | 7,2 | 9,5 | 15,4 | **14,1** |
| Peor caso frente a la mejor de las cuatro | 47 % | 62 % | 80 % | **91 %** |

**Lectura:** nadie sabe de antemano en qué escenario está la Caja. La mezcla no gana siempre, pero **nunca queda lejos**. Cuando el potencial está donde ya hay clientes, gana «solo cartera»: por eso la herramienta **complementa y no reemplaza**. «Solo cartera» es una simplificación nuestra (visitar únicamente donde ya hay clientes); no representa cómo prospecta hoy la Caja. Los números salen de un generador nuestro: muestran cómo se comporta el mecanismo, no cuánto ganaría la Caja.

**Sensibilidad:** en 11 variaciones de un parámetro a la vez (capacidad, semanas, cuota de exploración, peso del punto de partida, historial), el peor caso de la mezcla se mantuvo entre 86 % y 94 % y fue siempre el mejor; los demás quedaron entre 45 % y 64 % (solo cartera), 53 % y 75 % (puntaje fijo) y 70 % y 83 % (solo descubrimiento). Se reproduce con `--sensibilidad`.

En el primer escenario, «solo cartera» visitó el 18 % de las zonas ocultas de alto potencial y la mezcla el 82 %.

## 4. Enfoque tecnológico

Python, FastAPI, Pydantic, pandas, scikit-learn, SQLite, Pydantic AI, React + Vite + Tailwind con mapa sobre OpenStreetMap, pytest.

- Modelo de potencial (regresión logística como base) que actúa como creencia previa de un esquema bayesiano Beta-Binomial por zona.
- Planificador con muestreo de Thompson, agotamiento de la zona, capacidad del analista, distancia y cuota de exploración.
- Agente acotado para la ficha, con proveedor intercambiable (Claude, OpenAI o local) y modo sin red con plantillas.
- Guardas: la unidad es la zona; no se recopilan datos personales ni se infieren características sensibles; no se extraen datos contra las condiciones de la fuente.

Fuentes públicas previstas (revisar las condiciones de cada una): INEI (censo de establecimientos y de población), SBS (puntos de atención e inclusión financiera), OpenStreetMap (licencia ODbL), registros municipales de mercados. En el prototipo, datos sintéticos con la misma estructura.

## 5. Tecnología preexistente

Creada el 25.11.2026 por el equipo: (1) generador de territorio sintético con 7 pruebas; (2) script de auditoría que compara estrategias en una simulación, de donde salen las cifras. El script contiene una versión mínima de la estrategia de aprendizaje: **no se reutiliza**; el planificador se escribe desde cero en el evento.

## 6. Funcionalidad crítica

Plan semanal de prospección que combina la ruta habitual y el descubrimiento, con ficha de evidencia por zona, que el analista ajusta y aprueba, y que **cambia cuando se registran los resultados**.

Criterios de aceptación: misma semilla y datos, mismo plan; la cuota de exploración se cumple; una zona sin dato digital no baja de puntaje por eso; al registrar resultados, el plan siguiente cambia en la dirección esperada; la ficha nunca menciona personas, elegibilidad ni capacidad de pago.

## 7. Nivel de desarrollo esperado

Prototipo de punta a punta sobre territorio sintético: la analista abre su semana, revisa una zona de descubrimiento, aprueba el plan, registra resultados, ve cómo cambia la semana siguiente y compara en el backtest contra la costumbre y contra un puntaje fijo.

## 8. Factibilidad y dependencias

| Tarea | Horas-persona (supuesto) |
|---|---|
| Territorio sintético y carga | 2 |
| Potencial con incertidumbre | 4 |
| Planificador (mezcla, exploración, capacidad) | 5 |
| Ficha de zona y agente | 4 |
| API y bitácora | 3 |
| Interfaz: mapa, plan y registro | 5 |
| Backtest, KPI y equidad | 4 |
| Pruebas, validación, pitch y demo | 4 |
| **Total** | **31 de 32** |

Mínimo viable: planificador, ficha por plantilla, aprobación y registro, backtest y pruebas. Si falta tiempo se recorta, en orden: redacción con modelo de lenguaje, mapa (queda la lista), cuadro de equidad detallado.

Dependencias **(supuestos)**: no se requieren datos de la Caja; con conteos agregados de clientes y resultados de visita por zona, el plan mejora. Capacidad de visitas, definición de «cliente nuevo» y política de IA externa: por confirmar.

## Preguntas abiertas para el owner

Unidad de zona que usan los analistas; salidas por semana y visitas por salida; cómo se registra hoy el resultado de una prospección; definición de cliente nuevo; política de IA externa.
