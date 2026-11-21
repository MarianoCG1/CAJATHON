# Sinergia por pareja y desafío

Generado por `scripts/sinergia/sinergia.py`. Datos: `team.json` (niveles) y `challenges.json` (tareas por desafío).
**Advertencia:** los niveles de Glem, Antonio y David, y todas las horas por tarea, son **estimaciones** nuestras. Corregirlas y volver a ejecutar.

Fórmula: puntaje = 100 × (0.6 × cobertura + 0.4 × min(1, sinergia/0.2)). Cobertura = habilidad de la pareja (la mejor de los dos en cada tarea) ponderada por horas. Sinergia = cobertura de la pareja menos la de su mejor integrante solo.

## 1. Alcance de cada desafío

| Desafío | Título | Horas MVP | Equipo de 4 (cobertura) | Horas por persona (4) |
|---|---|---|---|---|
| COM-01 | Encontrar oportunidades donde otros no ven clientes | 31 | 81% | 7.8 |
| COM-02 | Incentivos que impulsan un desempeño integral | 34 | 79% | 8.5 |
| NEG-01 | Cuotas que se adaptan al flujo del negocio | 35 | 83% | 8.8 |
| NEG-02 | Open Finance: competir en un ecosistema abierto | 38 | 84% | 9.5 |
| NEG-03 | Continuidad del vínculo cuando cambia el analista | 35 | 83% | 8.8 |
| RIE-01 | Microfinanzas resilientes al clima | 32 | 83% | 8.0 |
| RIE-02 | Descubrir redes de riesgo ocultas | 36 | 83% | 9.0 |
| RIE-03 | Anticipar el deterioro de pago antes del atraso | 33 | 85% | 8.2 |

Suma de los 8 desafíos: **274 h-persona** de MVP. Con 4 personas son 68 h cada una. Son horas de construcción: en el evento solo hay ~8 h por persona y solo si el equipo es finalista; para el concepto (hasta el miércoles) se necesita una fracción.

## 2. Matriz de puntaje (0–100) por pareja

| Desafío | Antonio+David | Antonio+Glem | Antonio+Mariano | David+Glem | David+Mariano | Glem+Mariano |
|---|---|---|---|---|---|---|
| COM-01 | 43 | **56** | 54 | 46 | 53 | 48 |
| COM-02 | 42 | **57** | 49 | 54 | 52 | 48 |
| NEG-01 | 42 | **62** | 60 | 45 | 52 | 48 |
| NEG-02 | 44 | **60** | 58 | 47 | 56 | 47 |
| NEG-03 | 44 | 52 | 49 | 57 | **58** | 49 |
| RIE-01 | 42 | **57** | 55 | 47 | 53 | 50 |
| RIE-02 | 40 | 52 | **53** | 47 | **53** | 51 |
| RIE-03 | 41 | 56 | **56** | 47 | 55 | 50 |

## 3. Mejor pareja por desafío, sinergia y brechas

- **COM-01** Encontrar oportunidades donde otros no ven clientes: mejor pareja **Antonio + Glem** (puntaje 56, cobertura 68%, sinergia +8%).
  - Brechas: Diseño del flujo del analista (2 h, nivel 1)
- **COM-02** Incentivos que impulsan un desempeño integral: mejor pareja **Antonio + Glem** (puntaje 57, cobertura 68%, sinergia +8%).
  - Brechas: Diseño del simulador y de la vista del analista (2 h, nivel 1)
- **NEG-01** Cuotas que se adaptan al flujo del negocio: mejor pareja **Antonio + Glem** (puntaje 62, cobertura 70%, sinergia +10%).
  - Brechas: Diseño del flujo del analista (2 h, nivel 1)
- **NEG-02** Open Finance: competir en un ecosistema abierto: mejor pareja **Antonio + Glem** (puntaje 60, cobertura 68%, sinergia +9%).
  - Brechas: Diseño de la experiencia de consentimiento (3 h, nivel 1)
- **NEG-03** Continuidad del vínculo cuando cambia el analista: mejor pareja **David + Mariano** (puntaje 58, cobertura 79%, sinergia +5%).
- **RIE-01** Microfinanzas resilientes al clima: mejor pareja **Antonio + Glem** (puntaje 57, cobertura 69%, sinergia +7%).
  - Brechas: Diseño del mapa y del flujo del gestor (2 h, nivel 1)
- **RIE-02** Descubrir redes de riesgo ocultas: mejor pareja **Antonio + Mariano** (puntaje 53, cobertura 77%, sinergia +3%).
  - Brechas: Diseño de la vista del investigador (2 h, nivel 1)
- **RIE-03** Anticipar el deterioro de pago antes del atraso: mejor pareja **Antonio + Mariano** (puntaje 56, cobertura 80%, sinergia +4%).
  - Brechas: Diseño del flujo del gestor y explicación de alertas (2 h, nivel 1)

## 4. Reparto rotativo óptimo (carga equilibrada, cada pareja ≤ 2 veces)

| Desafío | Pareja | Puntaje | Brechas (horas sin cobertura) |
|---|---|---|---|
| COM-01 | Antonio + Glem | 56 | 2 h |
| COM-02 | David + Glem | 54 | 4 h |
| NEG-01 | Antonio + Glem | 62 | 2 h |
| NEG-02 | Antonio + Mariano | 58 | 3 h |
| NEG-03 | David + Glem | 57 | 3 h |
| RIE-01 | Antonio + Mariano | 55 | 2 h |
| RIE-02 | David + Mariano | 53 | 2 h |
| RIE-03 | David + Mariano | 55 | 2 h |

Puntaje total: 450 (promedio 56).

| Persona | Desafíos | Horas MVP asignadas (si se construyeran todos) |
|---|---|---|
| Antonio | 4 | 45 h |
| David | 4 | 30 h |
| Glem | 4 | 89 h |
| Mariano | 4 | 110 h |

**Alerta de carga:** el reparto equilibra *cuántos* desafíos toca a cada uno, pero Mariano acumularía 110 h de MVP frente a 30 h de David. Construir los 8 no cabe; solo es viable redactar los conceptos y construir el que avance.

## 5. Ranking de prioridad

Se calcula con tres juegos de pesos y se ordena por el **rango promedio**, para que el resultado no dependa de una sola ponderación. Cada criterio se normaliza entre el mejor y el peor desafío (0–1). Cobertura, sinergia y esfuerzo salen de los datos del equipo; impacto, medibilidad y competencia son **supuestos** de `valoracion.json`.

Pesos: **base** = cobertura 20%, sinergia 20%, esfuerzo 15%, impacto 20%, medibilidad 15%, competencia 10%; **equipo** = cobertura 40%, sinergia 40%, esfuerzo 20%; **negocio** = impacto 40%, medibilidad 35%, competencia 25%.

| Orden | Desafío | Rango promedio | Puntaje base | Rango base | Rango equipo | Rango negocio | Pareja del reparto |
|---|---|---|---|---|---|---|---|
| 1 | RIE-03 Anticipar el deterioro de pago antes del atraso | 1.3 | 74 | 1 | 2 | 1 | David + Mariano |
| 2 | NEG-01 Cuotas que se adaptan al flujo del negocio | 1.7 | 66 | 2 | 1 | 2 | Antonio + Glem |
| 3 | NEG-02 Open Finance: competir en un ecosistema abierto | 3.3 | 50 | 3 | 3 | 4 | Antonio + Mariano |
| 4 | RIE-01 Microfinanzas resilientes al clima | 4.3 | 48 | 4 | 4 | 5 | Antonio + Mariano |
| 5 | RIE-02 Descubrir redes de riesgo ocultas | 5.3 | 42 | 5 | 8 | 3 | David + Mariano |
| 6 | NEG-03 Continuidad del vínculo cuando cambia el analista | 5.7 | 40 | 6 | 5 | 6 | David + Glem |
| 7 | COM-01 Encontrar oportunidades donde otros no ven clientes | 7.0 | 37 | 7 | 6 | 8 | Antonio + Glem |
| 8 | COM-02 Incentivos que impulsan un desempeño integral | 7.3 | 28 | 8 | 7 | 7 | David + Glem |

**Cómo usarlo:** escribir los conceptos en este orden. Los primeros reciben más tiempo y más revisión; los últimos se completan después, con la pareja que indica el reparto. Si la organización limita a un concepto por equipo, el primero de la lista es el candidato.


Lo que **no** mide este modelo: calidad y volumen de los datos que entregue la Caja, KPI y línea base (no publicados), cuántos equipos eligen cada desafío, ni el riesgo de que un MVP no alcance 3/5 en funcionalidad crítica.
