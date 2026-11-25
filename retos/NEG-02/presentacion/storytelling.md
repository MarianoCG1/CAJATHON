# NEG-02 — storytelling

> Open Finance simulado: la Caja ve más del cliente solo cuando él lo autoriza, y cada oferta muestra el dato y el consentimiento que la originó.

*Personaje ficticio, creado para explicar la solución. No es una persona real ni un caso de la Caja.*

## Quién es Lucía

Lucía atiende a microempresarios y personas. Quiere ofrecerles lo que de verdad les conviene, pero solo ve lo que ellos hacen con la Caja. Es un personaje ficticio, creado para explicar la solución.

## Antes: un día sin la solución

- Solo ve los productos del cliente en la Caja.
- No sabe si paga deudas más caras en otra entidad ni si tiene ahorro ocioso.
- Puede ofrecer crédito a quien ya está sobreendeudado.
- Si usara datos de otras entidades, no habría forma de probar que el cliente lo autorizó.

## El momento clave

El cliente revoca una entidad y la oferta de consolidación desaparece sola, porque el consentimiento se aplica en el código y no en la interfaz.

## Después: un día con la solución

- El cliente autoriza qué puede ver la Caja, de qué entidad, por cuánto tiempo y para qué.
- Lucía ve una vista integral solo de lo autorizado.
- Cada oferta muestra el dato, la entidad y el consentimiento que la originó.
- Si el cliente revoca, la vista se reduce de inmediato; si hay sobreendeudamiento, el sistema se abstiene.

## La historia en tres frases (para decir en voz alta)

1. Lucía quiere ofrecer lo que conviene, pero hoy solo ve una parte del cliente y no puede usar datos ajenos sin consentimiento.
2. Con un control de consentimiento en el código, la Caja ve solo lo autorizado, propone productos con evidencia y se abstiene si hay sobreendeudamiento.
3. Cada consulta queda registrada, el cliente puede revocar en cualquier momento y la decisión final es siempre de Lucía.

## Cómo funciona, sin tecnicismos

1. **El cliente otorga un consentimiento.** Con alcance, vigencia, finalidad y entidad; puede revocarlo cuando quiera.
2. **Control de consentimiento.** Único camino a los datos de otras entidades; aplica alcance, vigencia, finalidad y receptor, y registra cada acceso.
3. **Vista integral.** Une lo autorizado de varias entidades y estima el ingreso con un modelo predictivo.
4. **Motor de oportunidades.** Consolidación de deuda, capital de trabajo MYPE, captación de ahorro y domiciliación, cada una con su evidencia.
5. **Abstención.** Si la visión integral muestra sobreendeudamiento, no se ofrece crédito.
6. **Ejecutivo y medición.** El ejecutivo aprueba, edita o descarta; el KPI se mide en tres brazos sintéticos.

## Lo que no prometemos

- Una cifra de impacto comercial sobre la Caja: no hay línea base.
- APIs o datos reales, ni conformidad con un estándar de Open Finance.
- Decisiones o scoring crediticio automáticos.
- Que el 95 % sea una capacidad medida: es un tope teórico.
