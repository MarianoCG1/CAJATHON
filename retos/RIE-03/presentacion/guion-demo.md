# RIE-03 — guion de demostración (5 minutos)

Guion para la fase presencial, con el prototipo construido en el evento. Hoy es solo un guion: no hay prototipo.

| Minuto | Qué se muestra | Qué se dice |
|---|---|---|
| 0–0.5 | Abrir la cola del día (corte de fin de mes en los datos sintéticos) | Estos clientes están al día y son los que más riesgo tienen de deteriorarse; ninguno tiene atraso hoy. |
| 0.5–1.5 | Abrir un caso con deterioro gradual | Sus abonos caen tres meses seguidos mientras su sector no cae: no es estacional. |
| 1.5–2 | Mostrar evidencia e incertidumbre | Cada alerta trae su rango; sin historial suficiente, el sistema no alerta. |
| 2–3 | Aprobar la acción propuesta | El agente propone canal y mensaje citando la evidencia; el gestor aprueba y queda en la bitácora; no se envía nada solo. |
| 3–3.5 | Mostrar un cliente con fluctuación normal que no alertó | Una caída de un mes, propia de su temporada, no entra a la cola. |
| 3.5–5 | Backtest con y sin la solución | Casos detectados, días de anticipación y falsos positivos frente a reglas de atraso; el efecto de intervenir se muestra como escenario. |

## Si algo falla en vivo

- Si falla el modelo de lenguaje externo: usar el modo con plantillas, sin red.
- Si falla la interfaz: mostrar la cola y el caso desde la API en texto.
- Si falla el backtest en vivo: mostrar los resultados guardados con semilla fija.
