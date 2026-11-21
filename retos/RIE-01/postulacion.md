# Postulación RIE-01 — texto para pegar en la plataforma

Desafío elegido: RIE-01 · Microfinanzas resilientes al clima. Equipo: Yupana Labs.

## 1. Problema abordado

Según el desafío, lluvias intensas, inundaciones o sequías pueden afectar la actividad económica de los microempresarios, sobre todo de quienes están en zonas vulnerables o tienen actividades sensibles al clima, y con ello sus ingresos y su capacidad de pago. El reto es anticipar esos riesgos y orientar estrategias preventivas que fortalezcan la resiliencia de los negocios que financia Caja Trujillo. Debemos hacerlo sin asumir que estar expuesto a una amenaza significa pérdida o incumplimiento, reconociendo que los escenarios climáticos son inciertos, y con recomendaciones sustentadas en evidencia que respeten la protección de datos y las políticas de riesgo de la Caja.

## 2. Concepto de solución

Radar Climático de Cartera (nombre de trabajo). El analista elige un escenario, por ejemplo una inundación severa en la costa norte, y la herramienta responde tres preguntas por separado: cuánta cartera está expuesta, cuánta es probablemente afectada y cuánta mora adicional cabe esperar, cada una con un rango y no con una cifra única. Un modelo combina la amenaza en el sector del cliente, la vulnerabilidad de su actividad y su colchón financiero, y su carga de deuda. Un mapa y un ranking priorizan zonas y clientes según las visitas que cada agencia puede realizar. Un agente propone, con la evidencia que lo sustenta, acciones del catálogo de la Caja, por cliente o por zona: alerta anticipada, visita, reprogramación, asesoría de continuidad y otras, a confirmar. La decisión es siempre del gestor: nada se ejecuta automáticamente.

## 3. Impacto esperado en el KPI

El KPI oficial y la línea base están a validar con el owner; no los inventamos. Proponemos medir el porcentaje de cartera afectada que se identifica antes del evento con la capacidad disponible, la precisión de la priorización frente a reglas simples (por zona o por monto), la pérdida evitada estimada, siempre como rango, y la continuidad de los negocios afectados. La medición será un backtest reproducible sobre eventos simulados con resultados ocultos, con y sin la solución. La cifra de impacto esperada está a validar con el owner cuando exista la línea base.

## 4. Enfoque tecnológico

Python, FastAPI y React. Un modelo estadístico calibrado con eventos históricos y validado en el tiempo; simulación de escenarios para entregar rangos; optimización para repartir las acciones entre los gestores disponibles; y un agente con herramientas acotadas, cuyo modelo de lenguaje es intercambiable (Claude, OpenAI o local) y que también funciona sin IA externa. El uso de IA externa está a confirmar con la política de la Caja.

## 5. Tecnología preexistente

Un generador de datos totalmente sintéticos con sus pruebas, herramienta general del equipo creada antes del evento, sin datos reales ni código de terceros, y librerías de código abierto bajo sus licencias. No se usa ningún dato real ni personal. Si la Caja entrega datos o mapas, los usaremos en su lugar. Todo lo demás se construye durante el evento.

## 6. Funcionalidad crítica

Un solo flujo de punta a punta: elegir un escenario, ver cartera expuesta, afectada y en riesgo de mora con rango, priorizar en mapa y ranking, recibir el plan que sugiere el agente, aprobarlo o rechazarlo, y medir el KPI con y sin la solución. Se desarrolla íntegramente en la fase presencial: modelo, escenarios, mapa, priorización, agente, API, interfaz y backtest. Nada de esto existe antes del hackathon.

## 7. Nivel de desarrollo esperado

Prototipo funcional de punta a punta, con pruebas automáticas, reporte de validación y una demostración de cinco minutos que termina con el número antes y después del KPI en un evento más severo que la historia. Los resultados serán sobre datos sintéticos; el impacto real depende de los datos y las acciones de la Caja, a validar con el owner.

## 8. Factibilidad y dependencias

Alcance estimado en 32 horas-persona (cuatro personas, ocho horas cada una), con hitos de control y recortes ordenados si el tiempo aprieta, sin perder el flujo de punta a punta. Dependencias a confirmar con la Caja: KPI y línea base, datos disponibles, política de IA externa y catálogo de acciones permitido por sus políticas de riesgo.
