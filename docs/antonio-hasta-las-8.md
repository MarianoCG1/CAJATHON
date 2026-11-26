# Antonio: qué avanzar hasta las 7:45 p. m. (26.11)

El formulario cierra **hoy a las 11:59 p. m.** Meta: enviar antes de las 10:30. NEG-01 es la opción recomendada y tú eres quien la domina: de tu parte depende que podamos defenderla y construirla.

> **5 p. m.:** entregado. Lo que falta corregir está en `docs/reunion-26-11.md`, sección «Actualización».

## Mensaje para pegar en el chat

```
Antonio, tu NEG-01 quedó muy bueno y es la opción que recomiendo. Haz git pull en main y abre
docs/antonio-hasta-las-8.md. Lo urgente:
1) Corregir en tu concepto y panorama: con holgura, S/ 8,000 necesita 17 meses (no 16), y el plan
   debe dejar holgura bajo el tope Cuota/Utilidad (el expediente lo pide).
2) Calcular a mano 5 casos con su resultado esperado (serán las pruebas del evento).
3) Buscar tasas, seguros y cifras públicas de la Caja y de la SBS para sustentar reglas e impacto.
4) Prepararte para explicar el cálculo en 3 minutos sin leer.
Revisa también retos/NEG-01/entrega/formulario.md: dime si hay algo que no puedas defender.
A las 7:45 mándame tu resumen y tu voto.
```

## Tareas, en orden

| # | Tarea | Tiempo | Listo cuando |
|---|---|---|---|
| 1 | **Corregir tus documentos** en tu rama (ver abajo) | 30 min | Commit y push en `reto/neg-01-antonio` |
| 2 | **Revisar `retos/NEG-01/entrega/formulario.md`** de principio a fin: es el texto que enviaríamos | 40 min | Cambios propuestos o «lo puedo defender» |
| 3 | **Cinco casos calculados a mano** con resultado esperado: ciclo plano, valle que no cubre intereses (pendientes), monto que no cabe, campaña retrasada, dos productos con factor distinto | 60 min | Tabla de cuotas y saldos por caso |
| 4 | **Reglas con fuente pública:** TEA por producto y seguro de desgravamen del tarifario publicado, tasa máxima del BCRP. Lo que no tenga fuente queda como supuesto | 40 min | Tabla con enlaces |
| 5 | **Impacto con cifras públicas:** de la SBS y de la memoria o los informes de la Caja (clientes, cartera, mora, peso agropecuario). Sin estimar nada que no tenga fuente | 40 min | 3 a 5 cifras con enlace y fecha |
| 6 | **Explicar el cálculo** en 3 minutos y escribir 5 preguntas difíciles de un comité de créditos con su respuesta | 30 min | Ensayado una vez |

Si te falta tiempo: 1, 2 y 6 son imprescindibles.

## Correcciones de la tarea 1

1. **Plazo:** «S/ 8,000 a 16 meses» pasa a **17**. En el de 16, el segundo año se evaluó sin escenarios adversos y deja S/ 195 sin cubrir si El Niño se repite. Cambiar en el texto, la tabla, los criterios de aceptación y la prueba descrita.
2. **Holgura bajo el tope:** el expediente pide resistir escenarios adversos **y** dejar holgura respecto al tope de Cuota/Utilidad Neta. En tu ejemplo varias cuotas usan el 100 % del 0,65. Propuesta: factor de trabajo menor que el del producto, configurable. Con 0,60: S/ 8,000 a 17 meses (interés S/ 2,060) o S/ 6,533 a 12 meses.
3. **Costo:** alargar el plazo encarece (S/ 1,908 frente a S/ 1,572 con factor 0,65). Decirlo.
4. **Ejemplo del arroz:** tú mismo anotas que se cosecha casi todo el año. Para la demo, elegir un cultivo o negocio con estacionalidad clara.
5. Quitar de tu lista de envío la mención a postular RIE-03.

## Reglas

- Las cuentas a mano son material previo: avisa para declararlas en `docs/preexistente.md`. **El motor y la interfaz no se construyen** antes del 03.12.
- Solo información pública y datos sintéticos. Nada de datos de clientes ni de tu trabajo.
- Nadie envía el formulario salvo el coordinador.

## Cómo te cruzas con Glem

Glem verifica el cálculo por su cuenta, sin mirar tus números. Intercambien resultados a las **6:30**: si no coinciden, ese es el primer tema.
