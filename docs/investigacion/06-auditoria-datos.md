# 06 · Auditoría de dificultad de los datos sintéticos (RIE-03, NEG-02, RIE-01, RIE-02)

Fecha: 21.11.2026 · Responsable: Mariano (tarea 1 de `docs/prompts-inicio.md`) · Herramientas: `scripts/auditoria/` (3 scripts + `test_auditoria.py`).

**Pregunta:** ¿se resuelve el backtest de cada reto con una regla trivial? (En RIE-02 ocurrió: una regla simple daba 100 % y hubo que endurecer los datos.) Si pasa, el backtest no demostraría nada y el jurado lo notaría.

**Alcance:** son comprobaciones sobre el *dataset*. No son el modelo, el motor ni el agente de ningún reto, y no se reutilizan en la solución. Los resultados son sobre **datos sintéticos propios**; los umbrales y las tasas son supuestos del equipo. Para repetirlas: generar los datos (`python retos/<ID>/datos/generar.py`) y correr `python scripts/auditoria/auditar_<id>.py` (requiere `scikit-learn`).

## Resumen

| Reto | ¿Trivial? | Qué encontramos | Qué implica para el pitch |
|---|---|---|---|
| **RIE-03** | **No** | Ninguna variable sola pasa de AUC 0.85. La regla «ya tiene atraso» no sirve para quien está al día. Las señales de alerta temprana aportan ≈ +0.11 de AUC sobre mirar el atraso | Se puede demostrar anticipación real. Hablar en *lift* y captura en el top-k, no en precisión absoluta (la base es muy baja) |
| **NEG-02** | **No, pero por otra razón** | Con información completa las reglas casi lo resuelven (por construcción de la verdad). Lo que limita es la **visibilidad**: Caja sola 13 %, con consentimientos 31 %, información completa 95 % | El valor demostrable es el **mecanismo del consentimiento**, no la precisión de un clasificador. No vender «el modelo detecta 95 %» |
| **RIE-01** | **No; es el riesgo contrario** | La señal es moderada: una fórmula de 3 factores da AUC 0.66, el modelo 0.68 y el techo con la susceptibilidad real 0.69. Con 2 semanas de visitas se captura ≈ 20 % de los incumplimientos (azar 8 %) | El impacto es un *lift* de ≈ 2.5×, no una detección casi perfecta. Y la ventaja del modelo sobre la regla de zona + actividad es pequeña (≈ 2 pp): hay que decidirlo antes del evento |
| **RIE-02** | **No** | Ninguna regla simple de coincidencias logra recall alto y precisión razonable: «cualquier coincidencia» detecta 90 % del fraude pero marca el 100 % de los señuelos (precisión 12 %); exigir dos tipos de vínculo baja los señuelos marcados al 37 % pero detecta solo 43 % | Se puede demostrar el valor de ponderar por rareza y de exigir corroboración de comportamiento, midiendo señuelos marcados y recall por dificultad |

## RIE-03 — anticipar el deterioro antes del atraso

Etiqueta (definida solo para la auditoría): primer atraso > 30 días dentro de los siguientes 60 días, para créditos sin atraso > 30 d previo. Entrenamiento: cortes hasta 2025-06; prueba: cortes desde 2026-01 (hueco de purga ≥ horizonte). Población de prueba: 14,438 crédito-mes; prevalencia 1.9 %.

| Medida | Resultado |
|---|---|
| Regla «días de atraso actual», AUC | 0.805 (pero vale 0 entre quienes están al día: todos tienen 0 días) |
| Mejor variable individual | abonos del mes relativos a su promedio: AUC 0.846 |
| Logística con 14 variables | AUC 0.934 |
| Árboles con 14 variables | AUC 0.930 |
| Árboles **sin** variables de atraso | AUC 0.916 |
| **Solo clientes al día** (14,086; prevalencia 0.7 %) | árboles AUC 0.838; solo señales 0.858; precisión en el 10 % mejor puntuado 4.7 % frente a 0.7 % de base (≈ 6.7× de lift; ≈ 2/3 de los casos concentrados en ese 10 %) |

**Lectura:** no es trivial (ninguna variable sola llega a 0.90) y tampoco imposible. El caso que importa —anticipar a quien hoy está al día— tiene señal razonable. La precisión absoluta es baja porque el evento es raro: la presentación debe usar *lift*, captura en el top-k según la capacidad del analista y días de anticipación.

**Advertencias:** el AUC «al día» baja a ≈ 0.84 porque se quita el atraso actual, la variable más fácil. Cualquier cifra del evento debe calcularse así, no sobre toda la cartera. Las pruebas fijan que el dataset no se vuelva trivial (`test_rie03_...`).

## NEG-02 — Open Finance y oportunidades con consentimiento

La verdad son cinco reglas deterministas sobre la información completa (`verdad_oportunidades.csv`); el ingreso real es latente. La auditoría aplica **las mismas reglas con ingreso estimado** (declarado a la Caja o, si no hay, abonos) y distinta visibilidad:

- **A.** Solo datos de la Caja (E00).
- **B.** Caja + entidades con consentimiento VIGENTE a la Caja y finalidad de oferta, **por alcance** (productos, saldos, condiciones, transacciones).
- **C.** Información completa observable.

Recall (parte de las oportunidades que existen y se detectan):

| Oportunidad | A: solo Caja | B: con consentimientos | C: completa |
|---|---|---|---|
| Capital de trabajo MYPE | 0.54 | 0.64 | 0.96 |
| Captación de ahorro | 0.00 | 0.27 | 1.00 |
| Consolidación de deuda | 0.00 | 0.14 | 0.89 |
| Domiciliación de ingresos | 0.00 | 0.24 | 1.00 |
| Restricción por sobreendeudamiento | 0.11 | 0.25 | 0.89 |
| **Global (ponderado)** | **0.13** | **0.31** | **0.95** |

Precisión: 0.88–1.00 en las oportunidades comerciales; baja en sobreendeudamiento (0.50 → 0.60 → 0.81) porque depende de estimar el ingreso real.

**Lectura:** el motor de reglas con información completa casi resuelve el problema, **por construcción**; eso no demuestra valor. Lo que sí se demuestra es que **el consentimiento es el factor limitante** (31 % frente a 95 %) y que la visión multientidad más que duplica lo que ve la Caja sola (13 % → 31 %). Eso coincide con el concepto («el consentimiento, no el modelo, limita las oportunidades») y sostiene un KPI honesto: oportunidades identificadas y consentidas, en tres brazos.

**Advertencias:** (1) Las reglas de la auditoría replican las de la verdad, así que el 95 % es un techo mecánico, no una capacidad medida. (2) La detección de sobreendeudamiento con ingreso estimado es el punto débil y el que conviene mostrar con intervalos. (3) La dificultad real que el jurado puede apreciar está en la guardia de consentimiento (batería adversarial), no en el clasificador.

## RIE-01 — Radar climático

Se entrena con `impacto_historico` y se mide en `backtest/` (verdad oculta). Objetivo: `incumple_30d`; prevalencia 4.7 % (72,000 cliente-evento, 6 eventos). Intensidad del escenario: la nominal, no la realizada.

| Medida | Resultado |
|---|---|
| Solo amenaza del distrito (AUC) | 0.606 |
| Amenaza × sensibilidad de la actividad | 0.645 |
| Amenaza × sensibilidad × intensidad (regla de 3 factores) | 0.661 |
| Árboles con 16 variables (entrenado en histórico) | 0.682 |
| Techo: fórmula con la **susceptibilidad real** del sector (verdad oculta) | 0.694 |
| Captura de incumplimientos con visitas de 2 semanas (984 clientes, ≈ 8 %): azar / regla 3 factores / árboles / techo | 7.8 % / 17.5 % / 19.6 % / 23.7 % |
| Los 5 distritos con más incumplimiento concentran | 32 % |

**Lectura:** no es trivial: ninguna regla se acerca a 0.9. Pero el dataset es **ruidoso**: aun conociendo la susceptibilidad real, el AUC es 0.69. Lo honesto de presentar es un *lift* de ≈ 2.5× sobre el azar con la capacidad real de los gestores, no una detección casi perfecta.

**Advertencias y decisiones que conviene tomar con Glem antes del evento:**
1. **La ventaja del modelo sobre la regla de zona + actividad es pequeña** (≈ 2 pp de captura). El criterio de aceptación del concepto («superar a las reglas en 5 de 6 eventos») puede fallar por ruido. Opciones: ajustar el criterio a «no peor y con rango calibrado», o dar más estructura aprovechable al generador (por ejemplo, más efecto de la distancia al cauce y la pendiente dentro del distrito).
2. La diferencia que sí es defendible es la **resolución de sector** y la **incertidumbre calibrada**, no la precisión puntual.
3. Hay que decidir si el KPI principal es la captura de saldo en mora (más ruidosa) o la identificación de cartera afectada (K1, AUC similar).

## RIE-02 — redes de riesgo y señuelos legítimos

Partición de evaluación: 1,884 solicitudes (114 de fraude, 397 señuelos legítimos, el resto normales). Reglas de coincidencia por recurso compartido con otra solicitud (teléfono, dispositivo, dirección de domicilio o de negocio, teléfono de referencia):

| Regla | Recall del fraude | Precisión | Señuelos marcados | Normales marcadas |
|---|---|---|---|---|
| R1 comparte algún recurso | 0.90 | 0.12 | 1.00 | 0.27 |
| R2 comparte teléfono | 0.05 | 0.03 | 0.15 | 0.10 |
| R3 comparte dispositivo | 0.51 | 0.17 | 0.61 | 0.03 |
| R4 comparte dos o más tipos de recurso | 0.43 | 0.15 | 0.37 | 0.10 |
| R5 dos tipos y referencia a otro solicitante | 0.11 | 0.16 | 0.18 | 0.00 |

Por dificultad de la red, R4 marca en promedio el 72 % de las solicitudes de las redes de dificultad baja, el 53 % de las medias y el 12 % de las altas.

**Lectura:** no es trivial; el compromiso entre recall y señuelos es fuerte (ninguna regla supera 0.17 de precisión) y las redes difíciles casi no se ven con reglas de coincidencia. Esto deja espacio para la ponderación por rareza del vínculo, la corroboración de comportamiento y el expediente con explicación legítima. **Advertencia:** son reglas a nivel de solicitud; el detector del reto trabaja con grafo y comunidades, y su medición final es por red. Las pruebas fijan que ninguna regla simple logre recall y precisión altos a la vez (`test_rie02_...`).

## Qué no cubre esta auditoría

- **RIE-02:** se audita con reglas a nivel de solicitud; la medición del detector (grafo y comunidades) se hace en el evento.
- No se probó ningún modelo del reto ni se midió efecto de intervenciones: los datos no contienen intervenciones.
- Los parámetros de los generadores son supuestos nuestros: un resultado «no trivial» aquí no garantiza que los datos que entregue la Caja lo sean.
