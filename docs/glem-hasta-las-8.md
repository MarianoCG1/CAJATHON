# Glem: plan de trabajo de hoy hasta las 7:45 p. m. (26.11)

El formulario cierra **hoy a las 11:59 p. m.** Meta del equipo: enviar antes de las 10:30. Solo se envía **un** desafío y es el que construiremos en la final. Tu revisión decide en buena parte cuál.

## Mensaje para pegar en el chat

```
Glem, hoy cerramos la entrega y necesito que tomes la revisión de todo mientras llego (8 p. m.).
Haz git pull en main y abre docs/glem-hasta-las-8.md: ahí está tu plan por bloques y un prompt para tu agente.

Contexto: tenemos 3 opciones (docs/tres-opciones.md): A) NEG-01 de Antonio, B) COM-01 y C) RIE-03.
La que enviemos hoy es la que construiremos en el evento, así que revisa pensando en «¿esto lo sacamos en 8 horas?».

Lo que te toca:
1) NEG-01: verificar el cálculo (ojo: con holgura S/ 8,000 necesita 17 meses, no 16) y contrastar con el expediente y las preguntas frecuentes.
2) Revisar la plataforma: comunicados, cambios del expediente y que nuestros textos calcen con los campos reales.
3) COM-01: nadie externo lo ha revisado; intenta romperlo (simulación y afirmaciones).
4) RIE-03: revisión rápida.
5) Para cada opción: riesgo de construcción, horas reales y tu voto.

A las 7:45 mándame un resumen: voto, errores y cambios. Y súbelo en tu rama glem/revision-26-11.
Pídele a Antonio que corrija el plazo en su concepto y panorama, y a David que lea las 3 opciones y vote.
```

## Preparación (10 min)

```powershell
git pull
```

```powershell
git switch -c glem/revision-26-11
```

```powershell
pip install pytest pandas numpy scikit-learn scipy
```

```powershell
python -m pytest -q
```

## Plan por bloques

| Bloque | Qué haces | Tiempo | Entregable |
|---|---|---|---|
| 1 | **Calcular NEG-01 por tu cuenta** (reglas abajo) y buscar casos que rompan el motor: valle sin capacidad, monto que no cabe, ciclo plano | 50 min | Confirmas o refutas cada cifra; 3 casos de prueba escritos |
| 2 | **NEG-01 contra el expediente** actualizado y sus 10 preguntas frecuentes: qué falta, qué contradice, qué presentamos como hecho siendo supuesto | 40 min | Lista priorizada de cambios al formulario |
| 3 | **Plataforma:** revisada a las 3:50 p. m. sin comunicados nuevos desde anoche. Vuelve a mirar a las 7 y avisa si hay algo | 5 min | «Sin cambios» o qué cambió |
| 4 | **Atacar COM-01** (`retos/COM-01/`): reproducir la simulación y cuestionarla. ¿La comparación «solo cartera» es justa? ¿Algún supuesto fabrica la ventaja? ¿Las cifras del formulario salen del script? | 55 min | Objeciones y cuáles invalidan una afirmación |
| 5 | **RIE-03 rápido:** repetir la auditoría y revisar el contraste con el caso real (`docs/casos-reales.md`) | 20 min | Errores o «sin hallazgos» |
| 6 | **Construibilidad de las 3:** por opción, módulo más riesgoso, horas que tú estimas para tu parte y qué recortarías. Llenar tu voto en `docs/tres-opciones.md` | 30 min | Voto y justificación en 5 líneas |
| 7 | **Cinco preguntas duras** de un jurado de la Caja para la opción que votas, con respuesta | 20 min | 5 preguntas y respuestas |
| 8 | Resumen y push de tu rama | 15 min | `retos/revision-glem-26-11.md` |

Si te falta tiempo: bloques 1, 2, 3 y 6 son los imprescindibles.

## Comandos para los bloques 4 y 5

```powershell
python scripts/auditoria/auditar_com01.py --semillas 200
```

```powershell
python scripts/auditoria/auditar_com01.py --sensibilidad
```

```powershell
python retos/RIE-03/datos/generar.py
```

```powershell
python scripts/auditoria/auditar_rie03.py
```

El concepto y el panorama de Antonio están en su rama:

```powershell
git show origin/reto/neg-01-antonio:retos/NEG-01/concepto.md
```

## Reglas para el bloque 1

- Caso: S/ 8,000, TEA 40 %, desgravamen 0,96 % anual sobre saldo, desembolso 15.01.2027, cuotas el día 15, factor 0,65.
- Tasa diaria = (1 + TEA)^(1/360) − 1; interés por días exactos sobre el saldo de capital.
- Orden de pago: seguros, interés y capital; lo no cubierto queda pendiente sin generar interés.
- Utilidad de enero a diciembre: 450, 400, 500, 2800, 4200, 3200, 900, 700, 650, 700, 600, 550. La cuota del 15 se paga con la utilidad del mes anterior.
- El Niño: abril 650, mayo 1960, junio 2940, julio 2240. Caída general: −20 %.
- Holgura en **todos** los meses: cuota = menor entre 0,65 × utilidad, utilidad con El Niño y utilidad con caída.
- Repetir con factor 0,60 (holgura bajo el tope que pide el expediente): debe dar 17 meses con interés 2,060, o 6,533 a 12 meses.
- A las 6:30 cruza tus resultados con Antonio.
- Cifras a verificar: cuota fija 801; 8 de 12 meses en déficit; déficit 1,861; con holgura 6,887 a 12 meses o 8,000 a 17.

## Reglas generales

- Solo datos sintéticos. Nada del expediente ni respuestas literales en el repositorio.
- No construir el motor ni la interfaz: se hacen en el evento. Tus hojas de verificación no se suben.
- No edites archivos de otros: tus observaciones van en `retos/revision-glem-26-11.md`. La corrección del plazo la hace Antonio en su rama.
- Nadie envía el formulario salvo el coordinador.

## Prompt para tu agente (Claude, GPT o Antigravity)

```
Soy Glem, del equipo Yupana Labs, repo CAJATHON. Lee AGENTS.md (sección «Estado al 26.11»),
docs/tres-opciones.md y docs/glem-hasta-las-8.md. El concepto y el panorama de NEG-01 están en la
rama origin/reto/neg-01-antonio (usa git show). Ayúdame con los bloques en orden, uno por uno y
avisando el tiempo. Sé crítico: verifica los cálculos de forma independiente sin copiar los del
documento, intenta refutar las afirmaciones de COM-01 y señala supuestos presentados como hechos.
Si te pego el expediente, úsalo para contrastar y no lo guardes en el repo. No construyas el motor
ni la interfaz, no envíes nada a la plataforma y solo haz push de mi rama glem/revision-26-11
cuando yo lo pida. Responde en español y termina con un resumen para WhatsApp.
```

## Para Antonio y David

```
Antonio: en tu ejemplo, con la regla de holgura aplicada a todo el plazo, S/ 8,000 necesita 17 meses y no 16. ¿Lo corriges en concepto y panorama? A las 8 quiero que nos expliques el cálculo sin leer.
```

```
David: lee docs/tres-opciones.md (10 min), dinos cuál pantalla te ves construyendo en 8 horas y vota antes de las 8:45. El formulario obliga a declarar que todos lo revisamos.
```
