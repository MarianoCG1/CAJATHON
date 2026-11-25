# RIE-02 — storytelling

> Convierte un lote de solicitudes en redes priorizadas, cada una con evidencia citada y su explicación legítima posible. La alerta dice «merece revisión», nunca «fraude».

*Personaje ficticio, creado para explicar la solución. No es una persona real ni un caso de la Caja.*

## Quién es Ricardo

Ricardo revisa solicitudes sospechosas. Sabe que un fraude puede repartirse entre varias personas, pero también que muchas familias y mercados comparten teléfonos y direcciones sin hacer nada malo. Es un personaje ficticio, creado para explicar la solución.

## Antes: un día sin la solución

- Revisa solicitud por solicitud y no ve la red.
- Si alerta por cada coincidencia, se llena de casos que no son fraude.
- Señalar a un cliente legítimo cuesta confianza.
- Armar un caso toma tiempo y la evidencia queda dispersa.

## El momento clave

Ricardo abre una red de seis solicitudes encadenadas que ninguna regla simple vería y, a su lado, una familia que comparte el mismo teléfono: el sistema sube la primera y baja la segunda, y explica por qué.

## Después: un día con la solución

- Recibe las redes priorizadas, no las coincidencias sueltas.
- Una red solo sube si combina vínculos raros con comportamiento anómalo.
- Cada red trae un expediente con evidencia citada y la explicación legítima posible.
- Decide con un motivo registrado; el cliente no recibe nada sin revisión humana.

## La historia en tres frases (para decir en voz alta)

1. Ricardo no puede ver las redes si revisa caso por caso, ni puede alertar por cada coincidencia sin acusar a clientes legítimos.
2. La mesa del especialista arma el grafo, prioriza las redes que combinan vínculos raros con comportamiento anómalo y entrega un expediente verificable con su explicación legítima.
3. Ricardo decide con un motivo registrado: el sistema nunca concluye fraude ni actúa solo.

## Cómo funciona, sin tecnicismos

1. **Lote de solicitudes.** Personas, negocios, teléfonos, dispositivos, direcciones y referencias de cada solicitud, antes del desembolso.
2. **Grafo ponderado por rareza.** Un dispositivo personal compartido por cinco identidades pesa mucho; una tableta de agencia o un puesto de mercado, casi nada.
3. **Comunidades e indicadores.** Encuentra grupos de solicitudes conectados de forma inusual.
4. **Corroboración de comportamiento.** Solo sube la red que, además de vínculos, muestra ráfagas de solicitudes o negocios y líneas recientes.
5. **Expediente verificable.** El agente redacta con evidencia citada y las explicaciones legítimas posibles; un verificador rechaza citas que no existan.
6. **Decisión humana.** Escalar, pedir verificación o descartar, con un motivo registrado.

## Lo que no prometemos

- Una cifra de impacto sobre la Caja: no hay línea base.
- Una ventaja amplia sobre una regla de dominio ajustada a mano.
- Conclusiones de fraude: la alerta solo dice que merece revisión.
- Integración con sistemas reales, bloqueo de operaciones ni reentrenamiento en línea.
