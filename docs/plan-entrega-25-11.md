# Plan de entrega 25–26.11 — ruta por reto (RIE-03, NEG-02, RIE-01, RIE-02)

Fuente de verdad del trabajo autónomo de Claude. **Cada tarea terminada se marca aquí con `[x]` y se hace commit.** Contexto de la plataforma: `docs/investigacion/07-plataforma-24-11.md`. Regla general: no se pregunta ni se espera confirmación; se decide, se anota la decisión y se sigue. **Lo único que no se hace sin un «sí» explícito de Mariano es enviar la postulación en la plataforma** (acción irreversible); todo lo demás se deja listo para pegar.

## Hechos que condicionan la ruta

- El formulario abre el **mié 25.11** (cierra jue 26.11, hora por confirmar). Hoy no existe: se desconocen campos, límites y adjuntos. Se prepara el contenido en **4 formatos** para cubrir cualquier forma: (1) campos por componente (los 8 de las bases), (2) texto corrido, (3) resumen corto, (4) ficha de una página (PDF).
- Los expedientes de los 4 retos **no cambiaron** desde el cotejo del 21.11. No hay respuestas de owners para estos 4 (no se abrieron tickets antes de que cerraran el 24.11, 18:00).
- Si el formulario solo admite **un** concepto: se postula **RIE-03**. Orden de prioridad si admite varios: RIE-03 → NEG-02 → RIE-01 → RIE-02.
- Regla de contenido: nada de cifras de impacto inventadas; lo medido sobre datos propios se rotula «medido sobre datos sintéticos propios»; lo demás, **(supuesto)** o **[POR CONFIRMAR]**.

## Paquete de entrega por reto (`retos/<ID>/entrega/`)

| Archivo | Contenido |
|---|---|
| `campos.md` | Los 8 componentes de las bases, cada uno listo para pegar en una caja de texto (versión ≤ 1,000 caracteres y versión completa) |
| `resumen-corto.md` | Resumen de ≤ 500 caracteres y título de una línea |
| `ficha-1-pagina.md` | Ficha de una página (fuente del PDF): problema, solución, impacto, tecnología, preexistente, funcionalidad crítica, factibilidad y diagrama |
| `supuestos-sin-confirmar.md` | Lo que dependía de respuestas del owner y qué se asumió |
| `checklist-envio.md` | Pasos exactos para cargar y verificar, y las decisiones ya tomadas |

El texto corrido es `retos/<ID>/postulacion.md` (ya existe).

## Ruta común (se hace en este orden para cada reto)

1. **Ajustes de contenido** según lo aprendido (ver abajo por reto) en `concepto.md` y `postulacion.md`.
2. **Paquete de entrega** (los 5 archivos).
3. **Revisión independiente**: un agente revisor distinto del autor pasa el Anexo C y el cotejo contra los criterios del pase (25/30/25/20). Se corrigen los hallazgos. (No sustituye la revisión cruzada humana; se anota como tal.)
4. **Ficha PDF** de una página y diagrama.
5. **Coherencia final**: cifras, nombres de archivos y conteo de pruebas consistentes entre concepto, postulación y paquete; `docs/preexistente.md` al día; pruebas en verde; tablero regenerado.

## Ruta específica por reto

### 1. RIE-03 · Anticipar el deterioro (prioridad #1; fallback único)
- [x] R3.1 Ajustes: incluir en Factibilidad la evidencia medida («señales tempranas elevan el AUC de 0.81 a 0.92; entre clientes al día, el 10 % mejor puntuado concentra ≈ 2/3 de los casos», sobre datos sintéticos propios) y hablar en *lift*, no en precisión absoluta; reforzar «IA externa solo para demo/intercambiable».
- [x] R3.2 Paquete de entrega (5 archivos).
- [ ] R3.3 Revisión independiente y correcciones.
- [x] R3.4 Ficha PDF y diagrama (`scripts/entrega/ficha_pdf.py`; diagrama de flujo en la ficha).

### 2. NEG-02 · Open Finance con consentimiento (prioridad #3)
- [x] R2.1 Ajustes: incluir la evidencia medida del mecanismo (Caja sola 13 %, con consentimientos 31 %, información completa 95 %; rotulada como preliminar y por construcción en el techo); KPI en tres brazos; dejar claro que el valor demostrable es el consentimiento verificable, no la precisión de un clasificador.
- [x] R2.2 Paquete de entrega.
- [ ] R2.3 Revisión independiente y correcciones.
- [x] R2.4 Ficha PDF y diagrama.

### 3. RIE-01 · Radar climático (prioridad #4)
- [x] R1.1 Ajustes: cambiar el criterio de aceptación («superar a las reglas en 5 de 6 eventos») por uno defendible con la señal real (no peor que la mejor regla simple al mismo presupuesto, *lift* ≥ 2× sobre el azar con capacidad realista, rango p10–p90 que cubra la mora en ≥ 4 de 6); declarar el impacto como *lift* moderado; KPI principal K1.
- [x] R1.2 Paquete de entrega.
- [x] R1.3 Revisión independiente y correcciones.
- [x] R1.4 Ficha PDF y diagrama.

### 4. RIE-02 · Redes de riesgo (prioridad #5)
- [x] R4.1 Verificar con una auditoría rápida que los señuelos siguen siendo difíciles (reglas simples vs. verdad) y anotar el resultado en `docs/investigacion/06-auditoria-datos.md`; incorporar la evidencia a Factibilidad.
- [x] R4.2 Paquete de entrega.
- [ ] R4.3 Revisión independiente y correcciones.
- [x] R4.4 Ficha PDF y diagrama.

## Cierre del día

- [x] Z1 `docs/preexistente.md`, `boveda/Tablero.md`, `README` y `retos/README.md` al día; pruebas en verde.
- [ ] Z2 Commit y push de lo terminado (sin textos literales de expedientes, FAQ ni tickets).
- [x] Z3 Mensaje corto para el chat del equipo con el estado de cada reto (queda como archivo `docs/mensaje-estado-24-11.md`; no se envía).

## 25.11 — cuando abra el formulario

- [ ] F1 Leer el formulario en el navegador integrado (campos, límites, adjuntos, si admite varios conceptos y la hora límite) **sin enviar nada**. Anotarlo en `docs/investigacion/07-plataforma-24-11.md` §1.
- [ ] F2 Adaptar el paquete a esos campos: un archivo `retos/<ID>/entrega/pegar-en-formulario.md` por reto, ya recortado a los límites reales.
- [ ] F3 Si admite uno solo: dejar listo solo RIE-03 y marcar los demás como material de portafolio.
- [ ] F5 (opcional, solo si el formulario admite enlace o adjunto de video) Preparar un explicativo de 45–60 s de RIE-03 con las skills de HyperFrames; si no lo admite, se deja para la fase presencial.
- [ ] F4 Dejar a Mariano una nota con los 3 pasos exactos para enviar. **Enviar solo si Mariano lo autoriza explícitamente en el chat.**

## Registro de decisiones tomadas sin consultar

- 24.11 — RIE-01: la postulación compromete la **versión mínima** del panorama (K1 y K2 en 3 eventos) y presenta K3, K4 y seis eventos como ampliación; se declara el script de auditoría como preexistente (entrena un modelo de referencia solo para medir la dificultad de los datos); el bloque «Complejidad tecnológica» de RIE-01 se capturó de la plataforma y se alineó el concepto.
- 24.11 — Se sacó de las postulaciones la frase «cola diaria» donde los datos son mensuales solo si el revisor lo pidió (ver revisiones).
- 24.11 — La entrega se prepara en 4 formatos porque el formulario no existe todavía.
- 24.11 — La revisión independiente la hace un agente revisor (no humano) por falta de tiempo; se rotula así.
