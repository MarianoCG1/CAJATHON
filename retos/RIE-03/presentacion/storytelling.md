# RIE-03 — storytelling

> Una cola corta y priorizada de clientes al día con riesgo de deteriorarse, con el porqué y una acción propuesta. El gestor decide.

*Personaje ficticio, creado para explicar la solución. No es una persona real ni un caso de la Caja.*

## Quién es Rosa

Rosa atiende una cartera de microempresarios. Visita negocios, recibe pagos, responde consultas y no tiene tiempo de revisar cada mes cómo evoluciona cada cliente. Es un personaje ficticio, creado para explicar la solución.

## Antes: un día sin la solución

- Se entera del problema cuando el cliente ya tiene atraso.
- Un mes bajo de un cliente estacional se ve igual que un deterioro real.
- Si llama a todos los que bajan, pierde horas y cansa a clientes sanos.
- No queda registro claro de por qué actuó ni de qué pasó después.

## El momento clave

Rosa abre el caso de un taller cuyos abonos caen tres meses seguidos frente a los de su sector, y lo llama antes del primer atraso.

## Después: un día con la solución

- Recibe una lista corta de clientes al día con riesgo, por prioridad.
- Cada alerta explica qué cae, desde cuándo y frente a qué.
- Los altibajos de temporada no entran a la lista.
- Aprueba, edita o descarta la acción propuesta y todo queda registrado.

## La historia en tres frases (para decir en voz alta)

1. Rosa no puede revisar a todos sus clientes cada mes, y cuando ve el primer atraso ya es tarde.
2. En cada corte recibe una lista corta de clientes al día con riesgo de deteriorarse, con el porqué y una acción propuesta.
3. Ella decide: nada se envía solo, y medimos cuántos casos se detectan, con cuánta anticipación y con qué falsos positivos.

## Cómo funciona, sin tecnicismos

1. **Datos de la cartera (sintéticos).** Historial de pagos, saldos y señales de actividad hasta la fecha de corte; nada posterior.
2. **Variables de cada cliente.** Comparan al cliente con su propio pasado y con su sector.
3. **Modelo de deterioro.** Probabilidad calibrada de pasar a atraso, con rango; sin historial suficiente, no alerta.
4. **Filtro de señal frente a fluctuación.** Solo pasa lo persistente, no estacional y visto en al menos dos familias de señales.
5. **Cola y agente.** Ordena por prioridad y propone canal, momento y mensaje con la evidencia citada.
6. **Decisión humana y medición.** El gestor aprueba, edita o descarta; todo queda en bitácora; el backtest compara con reglas simples.

## Lo que no prometemos

- Una cifra de impacto sobre la cartera de la Caja: no hay línea base.
- Que alertar evite el atraso: el efecto es un escenario.
- Decisiones o condiciones crediticias automáticas.
- Envío real de mensajes ni integración con sistemas de la Caja.
