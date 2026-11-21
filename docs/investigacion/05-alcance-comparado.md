# Alcance comparado de los 4 desafíos desarrollados

Fuente: `retos/<ID>/panorama.md` (ronda 1 y 2, 21.11.2026). **Todas las horas son estimaciones del propio equipo (en realidad, de las sesiones que prepararon cada desafío), sin medir.** Los factores pesimistas (×1.4 y ×1.6) son una conjetura, no un dato. Verificado: 158 pruebas pasan desde la raíz con `python -m pytest -q`.

## 1. Qué se preparó

| Desafío | Datos sintéticos | Pruebas | Postulación (palabras) |
|---|---|---|---|
| RIE-03 Deterioro de pago | 5.000 clientes · 34 meses · 10 tablas | 24 | 754 |
| NEG-02 Open Finance | 2.000 clientes · 6 entidades · 215 mil transacciones | 41 | 742 |
| RIE-01 Clima | 12.000 clientes · 44 distritos | 40 | 704 |
| RIE-02 Redes de riesgo | 3.664 solicitudes · 123 redes inyectadas | 37 | 726 |

Cada uno tiene concepto v1 (`retos/<ID>/concepto.md`), panorama de abastecimiento (`retos/<ID>/panorama.md`), cotejo con el expediente literal (`retos/<ID>/expediente.md`) y texto de postulación (`retos/<ID>/postulacion.md`).

## 2. Horas: plan base frente a prueba pesimista

Capacidad común usada aquí: **32 h** (4 personas × 8 h). Algunas sesiones usaron 34 h (8,5 h por persona); se indica aparte.

| Desafío | Plan base | Pesimista sin recortar | Tras todos los recortes | Holgura sobre 32 h | ¿Sostiene 3/5? |
|---|---|---|---|---|---|
| RIE-03 | 31,5 | 45,3 | 31,7 (9 recortes) | 0,3 h | Sí, con el producto reducido al mínimo y sin margen |
| NEG-02 | 27 (mínimo) / 35 (completo) | 41,0 (mínimo) / 52,6 (completo) | 32,3 (9 recortes) | −0,3 h (con 34 h: +1,7 h) | Sí, apretado; todos al 98–100 % |
| RIE-01 | 30,5 + 1,5 colchón | 45,0 | 29,9 (9 recortes) | 2,1 h | «Solo con los 9 recortes y sin margen real»; falla si el modelo no funciona al cierre del día 1 |
| RIE-02 | 29 | 42,5 | 31,3 (5 recortes) | 0,7 h (con 34 h: +2,7 h) | Sí, pero sin margen: un atasco de integración de 2–3 h lo rompe |

## 3. Lo que se pierde al recortar

- **RIE-03:** LLM del agente (pasa a plantillas), modelo GBM (queda regresión logística), mini-gráficos, auditoría de sesgos detallada, sensibilidad al efecto, y se reduce el backtest a dos comparadores. Conserva: cola priorizada, explicación de cada alerta, aprobación humana con bitácora, backtest con y sin la solución, pruebas.
- **NEG-02:** agente con LLM, rutas por entidad, interfaz con estilo, sensibilidad del KPI, modelo de ingreso estimado (lo primero que se pierde). Conserva: guardia de consentimiento, linaje de cada oferta, prueba de fuga, número antes/después.
- **RIE-01:** teselas del mapa, LLM del agente, Monte Carlo, optimización entera, resolución por sector (pierde diferenciación) y capa 3 simplificada. Riesgo: el agente sin LLM puede leerse como un motor de reglas.
- **RIE-02:** Louvain, modelo de scikit-learn (quedan reglas ponderadas), agente con herramientas (queda plantilla con citas verificadas), interfaz avanzada y ablaciones. Conserva: backtest contra reglas simples, medición sobre señuelos, regla de corroboración, decisión humana registrada.

## 4. Riesgos transversales

1. **Reparto de la carga.** En los escenarios pesimistas Mariano y Glem superan 10 h mientras Antonio y David quedan en 5–10 h. Hay que mover trabajo hacia Antonio y David antes del evento (ensayo permitido solo con generadores y esqueletos genéricos).
2. **Esqueleto genérico de frontend previo al 03.12.** RIE-02 propone Vite + Tailwind + Cytoscape sin lógica de dominio, declarado como preexistente (ahorraría 1,5–2 h). **Decisión del equipo; conviene consultarlo con la organización.**
3. **David y la interfaz.** Su perfil es Flask/HTML/CSS, no React. Concentra 5,5 h base (8,8 h pesimistas en RIE-02). Riesgo de que la demo caiga aunque el backend funcione.
4. **Optimismo de las estimaciones.** Bajaron frente al borrador porque los datos ya existen; las hicieron los mismos autores. Los escenarios pesimistas son más realistas que los planes base.
5. **Sin KPI ni línea base oficiales** en ninguno; los cuatro comparan contra líneas base propias y declaran que la de la Caja está **[POR CONFIRMAR]**.
6. **Dataset demasiado fácil.** RIE-02 detectó que una regla de dos parámetros daba F1 = 1,0; endureció el generador y añadió pruebas para que ninguna regla simple llegue al 100 %. Conviene revisar lo mismo en los otros tres (¿un detector trivial resuelve el backtest?).

## 5. Observaciones de cotejo con el expediente

Los cuatro textos tenían entre 7 y 13 desviaciones respecto del expediente literal, casi todas **atribuciones al expediente de frases que venían de nuestro borrador v0** o **restricciones diluidas** (protección de datos, incertidumbre, «afecten a los clientes», seguridad, «conexiones» y «contactos»). Quedaron corregidas. Moraleja: el generador de borradores v0 no debe usarse como fuente; el texto literal manda.

## 6. Decisiones que quedan para el equipo

- Qué desafío o desafíos postular (depende de la respuesta de la organización sobre varios conceptos).
- Si se aprueba el esqueleto genérico de frontend previo al evento.
- Reasignar tareas para equilibrar la carga y practicarlas con el generador.
- Revisar el formato de postulación cuando abra la plataforma: los textos están en ~700 palabras y sin tablas, pero los campos reales pueden limitar la extensión.
