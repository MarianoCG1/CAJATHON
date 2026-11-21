# Mensaje para Glem (listo para pegar)

> WhatsApp: texto plano. Compartirle antes la carpeta del proyecto (no hay repo en la nube todavía; el material de la Caja es confidencial, no subirlo a un repo público).

```
Glem, te resumo en qué andamos, porque tu parte es clave. 👇

📌 CONTEXTO
• Entramos a la plataforma: hay 8 desafíos publicados y la organización confirmó que podemos elegir cualquiera (Recuperaciones fue solo nuestra elección inicial).
• El Concepto de solución se postula del miércoles 25 al jueves 26 (falta confirmar la hora límite).
• Hoy el Cajathon avisó: en esta etapa NO entregan datos. En el formulario del concepto podemos pedir los datos y recursos que necesitaríamos, y recién a los finalistas les dirán qué ponen a disposición. Por eso nuestros datos sintéticos son la base de todo.

💡 QUÉ ESTAMOS HACIENDO
Preparar conceptos sólidos para varios desafíos y, si pasamos a la final, construir solo uno. Hice un programa que mide qué pareja encaja mejor con cada desafío y los ordena por prioridad. Ya desarrollé a fondo 4 (RIE-03 deterioro de pago, NEG-02 Open Finance, RIE-01 clima, RIE-02 redes de riesgo). Cada uno tiene: concepto v1, panorama de abastecimiento, generador de datos sintéticos con pruebas y texto de postulación. Hay 158 pruebas en verde.

🎯 TU PARTE (según tu perfil: datos, modelo y pruebas)
• RIE-03: modelo de deterioro y explicabilidad, y pruebas. Además revisas el concepto.
• RIE-01: modelo de tres capas y escenarios. Es el más pesado y quedas como cuello de botella. También revisas el concepto.
• RIE-02: comunidades y features de red, priorización y API.
• NEG-02: cargador, vista 360 y motor de oportunidades.
• Con Antonio: NEG-01 y COM-01. Con David: NEG-03 y COM-02 (estos cuatro aún sin desarrollar).

⚠️ LO QUE ENCONTRAMOS
• El plan de horas es optimista: en el escenario pesimista todos pasan de 41 a 45 h contra ~32 disponibles. Solo caben recortando, y a ti y a mí nos tocaría más de 10 h cada uno. Hay que repartir mejor.
• Al cotejar con el texto literal de los expedientes salieron muchas atribuciones que no eran del expediente. Ya las corregimos.
• En RIE-02 el dataset resultó demasiado fácil (una regla simple daba 100 %). Lo endurecimos. Quiero que mires si pasa lo mismo en los otros tres.

🙏 NECESITO DE TI
1. Corrige tus niveles en scripts/sinergia/team.json: puse estimaciones tuyas y el ranking depende de eso.
2. Revisa los datasets: ¿un modelo trivial resuelve el backtest? Genera con: python retos/RIE-03/datos/generar.py (igual para neg02, rie01 y rie02).
3. Lee retos/RIE-03/panorama.md y RIE-01.md, sobre todo las secciones de modelo y backtest, y dime qué recortarías.
4. Corre las pruebas desde la raíz: python -m pytest -q

⚠️ REGLAS
• Todo es confidencial: nada de esto va a un repo público.
• No construimos el modelo ni el agente de ningún desafío antes del 3 de diciembre; eso se hace en el evento. Solo generadores de datos y documentación.
• Si algo no viene del expediente, está marcado como (supuesto) o [POR CONFIRMAR].

¿Qué te parece? Dime si ves algo flojo en la parte de datos o de modelo.
```
