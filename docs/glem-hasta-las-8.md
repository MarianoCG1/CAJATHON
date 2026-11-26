# Glem: qué avanzar hasta las 8 p. m. (26.11)

El formulario cierra **hoy a las 11:59 p. m.** Meta del equipo: enviar antes de las 10:30. Solo se envía **un** desafío y solo el coordinador edita el formulario.

## Mensaje para pegar en el chat

```
Glem, hoy cerramos. Llego a las 8 y enviamos antes de las 10:30.
Lee primero docs/reunion-26-11.md. Tu parte, en este orden:
1) Verificar el cálculo de NEG-01 (cuota fija S/ 801; con holgura S/ 8,000 no cabe en 16 meses, sí en 17).
2) Contrastar el formulario de NEG-01 con el expediente y las preguntas frecuentes actuales.
3) Mirar si hay comunicados o cambios nuevos en la plataforma.
4) Revisar las fuentes que citamos y elegir un negocio con estacionalidad clara para la demo.
A las 7:45 mándame: tu voto (NEG-01, COM-01 o RIE-03), errores encontrados y cambios que propones.
Pídele a Antonio que corrija el plazo (16 → 17) en su concepto y panorama.
```

## Tareas, en orden

| # | Tarea | Tiempo | Listo cuando |
|---|---|---|---|
| 1 | Leer `docs/reunion-26-11.md` y el formulario de NEG-01; hojear el de COM-01 | 30 min | Tienes una primera opinión |
| 2 | **Verificar el cálculo** en una hoja aparte (reglas abajo) | 60 min | Confirmas o refutas 801, 8 de 12, 1,861, 6,887 y 17 meses |
| 3 | **Contrastar** el formulario de NEG-01 con el expediente actualizado y sus 10 preguntas frecuentes | 45 min | Lista de lo que falta o contradice |
| 4 | Revisar comunicados y cambios nuevos en la plataforma | 10 min | «Sin cambios» o qué cambió |
| 5 | Comprobar las fuentes citadas (BCRP, MIDAGRI, SENAMHI) y proponer un negocio y zona con estacionalidad clara, con fuente | 45 min | Una propuesta con enlace |
| 6 | Escribir las 5 preguntas más difíciles que haría un jurado de la Caja y cómo responderlas | 30 min | 5 preguntas con respuesta |

Si no alcanza el tiempo: 2, 3 y 4 son los importantes.

## Reglas para la tarea 2

- Caso: S/ 8,000, TEA 40 %, desgravamen 0,96 % anual sobre saldo, desembolso 15.01.2027, cuotas el día 15, factor 0,65.
- Tasa diaria = (1 + TEA)^(1/360) − 1; interés por días exactos sobre el saldo de capital.
- Orden de pago: seguros, interés y capital; lo no cubierto queda pendiente sin generar interés.
- Utilidad mensual de enero a diciembre: 450, 400, 500, 2800, 4200, 3200, 900, 700, 650, 700, 600, 550. La cuota del 15 de un mes se paga con la utilidad del mes anterior.
- Escenario El Niño: abril 650, mayo 1960, junio 2940, julio 2240. Caída general: −20 % todos los meses.
- Regla de holgura, en **todos** los meses del plazo: cuota = menor entre 0,65 × utilidad, utilidad con El Niño y utilidad con caída.

## Reglas generales

- Solo datos sintéticos. Nada del expediente ni respuestas literales en el repositorio.
- No construir el motor ni la interfaz: eso se hace en el evento. La hoja de verificación no se sube.
- No edites los archivos de otros: anota tus observaciones en `retos/NEG-01/revision-glem.md` o mándalas por el chat.

## Prompt para tu agente (Claude, GPT o Antigravity)

```
Estoy en el repo CAJATHON (equipo Yupana Labs). Lee AGENTS.md, docs/reunion-26-11.md,
docs/glem-hasta-las-8.md y retos/NEG-01/entrega/formulario.md. Para el concepto y el panorama
de NEG-01, usa: git show origin/reto/neg-01-antonio:retos/NEG-01/concepto.md (y panorama.md).
Ayúdame con las tareas de docs/glem-hasta-las-8.md: verifica el cálculo de forma independiente,
sin copiar el del documento; contrasta el formulario con el expediente que te pegaré (no lo
guardes en el repo); y señala errores, supuestos presentados como hechos y puntos débiles que
vería un jurado. No construyas el motor ni la interfaz, no envíes nada y no hagas push.
Responde en español.
```
