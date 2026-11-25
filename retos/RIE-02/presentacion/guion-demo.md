# RIE-02 — guion de demostración (5 minutos)

Guion para la fase presencial, con el prototipo construido en el evento. Hoy es solo un guion: no hay prototipo.

| Minuto | Qué se muestra | Qué se dice |
|---|---|---|
| 0–0.5 | Cargar el lote de solicitudes sintéticas | Son unas 3.700 solicitudes con redes de fraude simuladas y relaciones legítimas mezcladas. |
| 0.5–1.5 | Mostrar la cola de redes priorizadas | El especialista ve redes, no coincidencias sueltas, ordenadas con sus razones. |
| 1.5–2.5 | Abrir una red encadenada que las reglas simples no verían | El grafo resalta los vínculos raros y el comportamiento que corrobora. |
| 2.5–3.5 | Leer el expediente con evidencia y explicación legítima | Cada cita existe en los datos; el sistema dice «merece revisión», nunca «fraude». |
| 3.5–4 | Contrastar con un señuelo: una familia que comparte el mismo teléfono | El mismo dato compartido, pero sin comportamiento anómalo: baja de prioridad y se explica. |
| 4–5 | El especialista decide y se muestra el antes y después | Decisión con motivo registrado; el cliente no recibe nada; comparación con reglas simples y con la regla de dominio en la evaluación ciega. |

## Si algo falla en vivo

- Si falla el modelo de lenguaje externo: usar la plantilla sin red.
- Si falla el grafo interactivo: mostrar el grafo estático servido por la API.
- Si falla la evaluación en vivo: mostrar los resultados guardados con semilla fija.
