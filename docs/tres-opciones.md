# Tres opciones, pensando en construirlas (26.11)

Material confidencial del equipo. **Lo que enviemos hoy es lo que construiremos el 03 y 04.12** si pasamos a la final: unas 8 horas por persona, y si la funcionalidad crítica no funciona al menos 3 de 5, no hay premio.

## De un vistazo

| | **A. NEG-01 «Ritmo»** | **B. COM-01 «Brújula comercial»** | **C. RIE-03 «Alerta temprana»** |
|---|---|---|---|
| En una frase | Cuotas que siguen el ciclo del negocio, con el porqué | Dónde prospectar cada semana, aprendiendo de cada visita | Quién va a deteriorarse antes del primer atraso |
| Usuario | Asesor de negocios y comité | Analista de negocios | Gestor de cartera |
| Horas estimadas (de 32) | 31 (núcleo 26) | 31 | 31,5 (pesimista 45) |
| Lo más difícil | Cálculo financiero exacto | Que el aprendizaje se vea creíble | Que el modelo diga algo con datos simples |

## Cómo puntúa cada una (juicio nuestro, no es una nota oficial)

| Criterio | Peso | A. NEG-01 | B. COM-01 | C. RIE-03 |
|---|---|---|---|---|
| **Hoy:** alineación | 25 % | Alta | Media-alta | Media |
| **Hoy:** impacto | 30 % | Alto | Alto | Medio-alto |
| **Hoy:** viabilidad técnica | 25 % | Alta | Media-alta | Media |
| **Hoy:** factibilidad | 20 % | Media-baja | Media-alta | Media |
| **Final:** impacto en el negocio | 35 % | Alto | Medio-alto | Medio |
| **Final:** funcionamiento y pruebas | 35 % | Alto si el cálculo sale: se prueba contra casos hechos a mano | Medio-alto: la evidencia es simulada | Medio: evidencia circular |
| **Final:** innovación y simplicidad | 20 % | Media-alta | Alta | Media-baja |
| **Final:** demo | 10 % | Muy clara (dos negocios, dos planes) | Clara | Clara |

## A. NEG-01 «Ritmo»

**Demo:** dos negocios piden el mismo monto y reciben planes distintos, explicados y comparados con la cuota fija.

| Persona | Construye |
|---|---|
| Mariano | Cronograma, motor del plan y API |
| Glem | Ciclo del negocio (patrón, ajuste, banda) y perfiles sintéticos |
| Antonio | Reglas de producto, casos calculados a mano, comparación y KPI |
| David | Pantalla del asesor y hoja para el comité |

- **Mínimo que debe funcionar:** cronograma correcto, motor de «pagar en cada periodo lo máximo permitido», motivo de cada cuota y comparación con la cuota fija.
- **Mayor riesgo:** un error de céntimos o de reglas delante de gente que sabe de créditos. **Plan B:** el asesor ingresa el ciclo a mano y el motor hace el resto.
- **Antes del 03.12 (permitido y declarado):** estudiar las reglas, preparar casos calculados a mano, generador de perfiles sintéticos, reunir series públicas.

## B. COM-01 «Brújula comercial»

**Demo:** la analista abre su semana, revisa una zona poco conocida, registra resultados y ve cómo cambia el plan.

| Persona | Construye |
|---|---|
| Mariano | Planificador, agente de ficha y API |
| Glem | Modelo de potencial con incertidumbre y backtest |
| Antonio | KPI, costo por cliente nuevo y reparto de visitas |
| David | Semana, mapa y registro de resultados |

- **Mínimo:** plan semanal reproducible, ficha por plantilla, registro y backtest.
- **Mayor riesgo:** que el jurado lo vea como «una simulación». **Plan B:** lista en lugar de mapa.
- **Antes del 03.12:** el territorio sintético ya existe; revisar condiciones de las fuentes públicas.

## C. RIE-03 «Alerta temprana»

**Demo:** cola de clientes al día con riesgo, el caso con su evidencia y la aprobación del gestor.

| Persona | Construye |
|---|---|
| Mariano | Agente de intervención y API |
| Glem | Modelo, filtro de señal y backtest |
| Antonio | KPI y escenarios de intervención |
| David | Cola y caso |

- **Mínimo:** cola con puntaje e incertidumbre, explicación, aprobación y backtest.
- **Mayor riesgo:** datos demasiado simples. **Antes del 03.12:** enriquecer el generador.

## Recomendación

1. **A (NEG-01)**, si aceptamos el recorte de alcance, se corrige el plazo a 17 meses y Antonio explica el cálculo sin ayuda.
2. **B (COM-01)**, si el cálculo financiero nos pesa. Es la más fácil de construir.
3. **C (RIE-03)**, solo como respaldo.

## Voto del equipo (llenar antes de las 8:45)

Puntúa de 1 a 5.

| Pregunta | Mariano | Glem | Antonio | David |
|---|---|---|---|---|
| ¿Cuál quiero construir? (A, B o C) | | | | |
| A: confío en que funcione en el evento | | | | |
| B: confío en que funcione en el evento | | | | |
| C: confío en que funcione en el evento | | | | |
| ¿Puedo explicar la elegida ante un jurado? | | | | |
