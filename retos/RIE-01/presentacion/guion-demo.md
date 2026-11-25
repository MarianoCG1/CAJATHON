# RIE-01 — guion de demostración (5 minutos)

Guion para la fase presencial, con el prototipo construido en el evento. Hoy es solo un guion: no hay prototipo.

| Minuto | Qué se muestra | Qué se dice |
|---|---|---|
| 0–0.5 | Elegir el escenario: inundación severa en la costa norte | El analista no necesita esperar al evento: trabaja con un escenario ex ante. |
| 0.5–1.5 | Mostrar las tres cifras con rango | Expuesta, afectada y mora adicional son cosas distintas, y cada una trae su incertidumbre. |
| 1.5–2.5 | Mapa y ranking con la capacidad de visitas | Con las visitas que tiene la agencia, estos son los clientes a priorizar y el motivo de cada uno. |
| 2.5–3.5 | Plan del agente: aprobar una acción y rechazar otra | El agente propone con evidencia y costo; el gestor decide y queda registro; nada se ejecuta solo. |
| 3.5–4 | Cambiar de escenario | Los clientes de la ribera suben y los de la ladera bajan: la lista se recalcula. |
| 4–5 | Backtest en eventos con resultado oculto, incluido uno más severo que la historia | Frente al azar y a reglas simples, con la misma capacidad de visitas. |

## Si algo falla en vivo

- Si falla el modelo de lenguaje externo: usar el modo con plantillas, sin red.
- Si falla el mapa: mostrar el ranking y las tres cifras desde la API en tabla.
- Si falla el backtest en vivo: mostrar los resultados guardados con semilla fija.
