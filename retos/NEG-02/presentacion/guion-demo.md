# NEG-02 — guion de demostración (5 minutos)

Guion para la fase presencial, con el prototipo construido en el evento. Hoy es solo un guion: no hay prototipo.

| Minuto | Qué se muestra | Qué se dice |
|---|---|---|
| 0–0.5 | Un cliente ficticio otorga consentimiento a tres entidades simuladas | El cliente decide qué ve la Caja, de quién, por cuánto tiempo y para qué. |
| 0.5–1.5 | La Caja consulta a través del control; una consulta fuera de alcance es denegada | El consentimiento se aplica en el código: lo no autorizado no llega al motor ni al agente, y todo queda en la bitácora. |
| 1.5–2.5 | Vista integral y oferta de consolidación con evidencia | Cada oferta muestra el dato, la entidad y el consentimiento que la originó. |
| 2.5–3.5 | El cliente revoca una entidad | La vista se reduce de inmediato y la oferta desaparece. |
| 3.5–4 | Un cliente sobreendeudado recibe una abstención | La visión integral también sirve para no ofrecer. |
| 4–5 | KPI en tres brazos | Solo Caja, con los consentimientos del conjunto y con consentimiento total; valida el mecanismo, no el impacto comercial real. |

## Si algo falla en vivo

- Si falla el modelo de lenguaje externo: usar el modo con plantilla, sin red.
- Si falla la interfaz: mostrar las consultas y la bitácora desde la API en texto.
- Si falla la medición en vivo: mostrar los resultados guardados con semilla fija.
