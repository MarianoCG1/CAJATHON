# Retos — índice, parejas y reparto por persona

Ocho encargos de la Caja, uno por carpeta. Hasta el **25.11** el trabajo es desarrollar el **Concepto de solución** de cada uno (ver `AGENTS.md`). Cada carpeta tiene su ficha `README.md` con las tareas pendientes. Estado exacto y avance: [`boveda/Tablero.md`](../boveda/Tablero.md) (se regenera con `python scripts/boveda/generar_boveda.py`).

## Los 8 retos por prioridad

El orden sale de `scripts/sinergia/` (cobertura de habilidades de la pareja, sinergia y valoración de negocio; los niveles de Glem, Antonio y David son **supuestos** a corregir en `scripts/sinergia/team.json`). Si el tiempo aprieta, se recorta desde el final de la lista.

| # | Reto | Eje | Pareja líder | Revisor | Punto de partida |
|---|---|---|---|---|---|
| 1 | [RIE-03](RIE-03/README.md) Anticipar el deterioro de pago antes del atraso | 3 Riesgo, fraude y recuperaciones inteligentes | David + Mariano | Glem | Concepto v1 + panorama + postulación + datos: **falta revisión cruzada** |
| 2 | [NEG-01](NEG-01/README.md) Cuotas que se adaptan al flujo del negocio | 4 Inclusión financiera y resiliencia | Antonio + Glem | David | Solo borrador v0: **falta desarrollarlo** |
| 3 | [NEG-02](NEG-02/README.md) Open Finance: competir en un ecosistema abierto | 5 Open Finance y nuevos modelos de competencia | Antonio + Mariano | David | Concepto v1 + panorama + postulación + datos: **falta revisión cruzada** |
| 4 | [RIE-01](RIE-01/README.md) Microfinanzas resilientes al clima | 4 Inclusión financiera y resiliencia | Antonio + Mariano | Glem | Concepto v1 + panorama + postulación + datos: **falta revisión cruzada** |
| 5 | [RIE-02](RIE-02/README.md) Descubrir redes de riesgo ocultas | 3 Riesgo, fraude y recuperaciones inteligentes | David + Mariano | Antonio | Concepto v1 + panorama + postulación + datos: **falta revisión cruzada** |
| 6 | [NEG-03](NEG-03/README.md) Continuidad del vínculo cuando cambia el analista | 2 Experiencia, retención y crecimiento | David + Glem | Antonio | Solo borrador v0: **falta desarrollarlo** |
| 7 | [COM-01](COM-01/README.md) Encontrar oportunidades donde otros no ven clientes | 2 Experiencia, retención y crecimiento | Antonio + Glem | David | Solo borrador v0: **falta desarrollarlo** |
| 8 | [COM-02](COM-02/README.md) Incentivos que impulsan un desempeño integral | 1 Productividad y transformación comercial | David + Glem | Mariano | Solo borrador v0: **falta desarrollarlo** |

## Reparto por persona

| Persona | Lidera (en pareja) | Revisa |
|---|---|---|
| **Mariano** | [RIE-03](RIE-03/README.md), [NEG-02](NEG-02/README.md), [RIE-01](RIE-01/README.md), [RIE-02](RIE-02/README.md) | [COM-02](COM-02/README.md) |
| **Glem** | [NEG-01](NEG-01/README.md), [NEG-03](NEG-03/README.md), [COM-01](COM-01/README.md), [COM-02](COM-02/README.md) | [RIE-03](RIE-03/README.md), [RIE-01](RIE-01/README.md) |
| **Antonio** | [NEG-01](NEG-01/README.md), [NEG-02](NEG-02/README.md), [RIE-01](RIE-01/README.md), [COM-01](COM-01/README.md) | [RIE-02](RIE-02/README.md), [NEG-03](NEG-03/README.md) |
| **David** | [RIE-03](RIE-03/README.md), [RIE-02](RIE-02/README.md), [NEG-03](NEG-03/README.md), [COM-02](COM-02/README.md) | [NEG-01](NEG-01/README.md), [NEG-02](NEG-02/README.md), [COM-01](COM-01/README.md) |

## Orden sugerido de trabajo (21–25.11)

1. **Todos:** copiar de la plataforma los expedientes de sus retos a `retos/<ID>/expediente.md` (archivo local, no se sube).
2. **Revisión cruzada de los 4 ya desarrollados** (RIE-03, NEG-02, RIE-01, RIE-02): la hace el revisor con el Anexo C de `concepto.md`; objeciones en `retos/<ID>/revision.md`.
3. **Desarrollar los 4 que faltan** (NEG-01, NEG-03, COM-01, COM-02): concepto v1, panorama con cotejo, postulación. Modelo: `retos/RIE-03/`. NEG-01 primero (prioridad #2).
4. **24.11:** v2 de todo con las objeciones resueltas y verificación de consistencia.
5. **25.11:** el coordinador carga las postulaciones en la plataforma, en orden de prioridad (confirmar hora límite).

Calendario completo y reglas: `docs/plan-conceptos.md`.

## Carga de trabajo (aviso)

Los cuatro retos sin desarrollar recaen en Glem, Antonio y David (con Mariano revisando COM-02); Mariano ya concentró los cuatro desarrollados. Mientras revisan, Mariano puede apoyar a quien se atrase, empezando por NEG-01.

Mariano y Glem están sobrecargados en el escenario pesimista de las horas del evento (`docs/investigacion/05-alcance-comparado.md`) y el riesgo de interfaz recae en David. Eso importa solo si llegamos a la final y hay que construir; hasta el 25.11 el reparto es de redacción y revisión.
