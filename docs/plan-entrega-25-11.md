# Plan de entrega 25–26.11 — ruta por reto (RIE-03, NEG-02, RIE-01, RIE-02)

Fuente de verdad del trabajo autónomo de Claude. **Cada tarea terminada se marca aquí con `[x]` y se hace commit.** Contexto de la plataforma: `docs/investigacion/07-plataforma-24-11.md`. Regla general: no se pregunta ni se espera confirmación; se decide, se anota la decisión y se sigue. **Lo único que no se hace sin un «sí» explícito de Mariano es enviar la postulación en la plataforma** (acción irreversible); todo lo demás se deja listo para pegar.

> **Nota operativa (25.11, 07:21):** la sesión de la plataforma expiró y requiere que Mariano inicie sesión en el navegador integrado. Mientras no lo haga, **F1 no es posible**: no se escriben credenciales ni se intenta evitarlo; se anota y se sigue con las demás tareas sin marcar (I5, I6). Cuando la sesión esté activa, F1 pasa a ser lo primero.

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
- [x] R3.3 Revisión independiente y correcciones.
- [x] R3.4 Ficha PDF y diagrama (`scripts/entrega/ficha_pdf.py`; diagrama de flujo en la ficha).

### 2. NEG-02 · Open Finance con consentimiento (prioridad #3)
- [x] R2.1 Ajustes: incluir la evidencia medida del mecanismo (Caja sola 13 %, con consentimientos 31 %, información completa 95 %; rotulada como preliminar y por construcción en el techo); KPI en tres brazos; dejar claro que el valor demostrable es el consentimiento verificable, no la precisión de un clasificador.
- [x] R2.2 Paquete de entrega.
- [x] R2.3 Revisión independiente y correcciones.
- [x] R2.4 Ficha PDF y diagrama.

### 3. RIE-01 · Radar climático (prioridad #4)
- [x] R1.1 Ajustes: cambiar el criterio de aceptación («superar a las reglas en 5 de 6 eventos») por uno defendible con la señal real (no peor que la mejor regla simple al mismo presupuesto, *lift* ≥ 2× sobre el azar con capacidad realista, rango p10–p90 que cubra la mora en ≥ 4 de 6); declarar el impacto como *lift* moderado; KPI principal K1.
- [x] R1.2 Paquete de entrega.
- [x] R1.3 Revisión independiente y correcciones.
- [x] R1.4 Ficha PDF y diagrama.

### 4. RIE-02 · Redes de riesgo (prioridad #5)
- [x] R4.1 Verificar con una auditoría rápida que los señuelos siguen siendo difíciles (reglas simples vs. verdad) y anotar el resultado en `docs/investigacion/06-auditoria-datos.md`; incorporar la evidencia a Factibilidad.
- [x] R4.2 Paquete de entrega.
- [x] R4.3 Revisión independiente y correcciones.
- [x] R4.4 Ficha PDF y diagrama.

## Material de presentación por reto (`retos/<ID>/presentacion/`, pedido de Mariano el 25.11)

Contenido: storytelling (persona ficticia, antes y después), guion de demo con tiempos, preguntas del jurado con respuestas honestas y un deck de 11 láminas en PDF con flujo, pantallas ilustrativas, evidencia y plan. Fuente única: `contenido.json`; se genera con `python scripts/presentacion/armar.py <ID>`. Todo es ilustrativo (maquetas con datos ficticios): **no es un prototipo** y no adelanta la funcionalidad crítica.

- [x] P1 RIE-03: contenido, deck PDF y textos.
- [x] P2 NEG-02: `contenido.json` (pantallas de tipo `consentimiento` y `caso`), generar y revisar las láminas.
- [x] P3 RIE-01: `contenido.json` (pantallas de tipo `mapa` y `cola`), generar y revisar las láminas.
- [x] P4 RIE-02: `contenido.json` (pantallas de tipo `grafo` y `caso`), generar y revisar las láminas.
- [x] P5 Declarar `scripts/presentacion/` en `docs/preexistente.md`, enlazar el material desde `retos/README.md`, regenerar el tablero y correr las pruebas.

## Identidad Yupana Labs y presentaciones vivas (pedido de Mariano el 25.11)

Identidad en `identidad/` (guía, logos, patrón, tokens). Todo material usa esa identidad. Los decks en PDF y las fichas ya la aplican; `deck.html` se navega con flechas y tiene animaciones de entrada.

- [x] I1 Identidad de marca: guía, logos SVG, patrón y tokens (`scripts/identidad/generar_identidad.py`).
- [x] I2 Decks y fichas de los cuatro retos con la identidad (portada oscura con patrón, láminas claras y oscuras, franja de tres colores, versión HTML animada).
- [x] I3 Video de marca de Yupana Labs (sting de 8 s) con HyperFrames: la yupana se llena columna por columna, aparece el nombre y el lema. Proyecto en `video/marca/`; MP4 en `video/marca/out/yupana-labs-sting.mp4` (653 KB, renderizado en 46 s; no se versiona). Verificación `check` sin errores ni advertencias. HyperFrames ya no tiene el flujo `/motion-graphics`: se usa `/hyperframes` y sus referencias.
- [x] I4 Explicativo animado de RIE-03 (30–45 s, sin narración, con subtítulos en pantalla) con HyperFrames (`/general-video` o `/faceless-explainer`), con la historia de Rosa, la cola priorizada, la evidencia y el cierre. Proyecto en `video/rie-03/`. Usar el guion de `retos/RIE-03/presentacion/storytelling.md`. Sin cifras que no estén en el deck.
- [ ] I5 Explicativos de NEG-02, RIE-01 y RIE-02 con el mismo método y la misma identidad (uno por tarea).
- [ ] I6 Revisar los videos fotograma a fotograma (capturas), verificar que no afirmen nada no medido y registrar en el plan la herramienta y el comando de render.

Reglas: no subir los MP4 a servicios externos; si pesan mucho, no versionarlos (`video/**/out/` en `.gitignore`) y dejar el comando de render. Declarar `video/` como preexistente.

## Archivos por si piden adjunto o plantilla

- [x] E1 Versión editable en Word de cada concepto (`retos/<ID>/entrega/concepto.docx`, `python scripts/entrega/armar_docx.py`), con las 8 secciones y la identidad de Yupana Labs.

## Cierre del día

- [x] Z1 `docs/preexistente.md`, `boveda/Tablero.md`, `README` y `retos/README.md` al día; pruebas en verde.
- [x] Z2 (push autorizado por Mariano el 25.11 y hecho hasta 89c0ee4) Commit y push de lo terminado (sin textos literales de expedientes, FAQ ni tickets).
- [x] Z3 Mensaje corto para el chat del equipo con el estado de cada reto (queda como archivo `docs/mensaje-estado-24-11.md`; no se envía).

## 25.11 — cuando abra el formulario

- [ ] F1 Leer el formulario en el navegador integrado (campos, límites, adjuntos, si admite varios conceptos y la hora límite) **sin enviar nada**. Anotarlo en `docs/investigacion/07-plataforma-24-11.md` §1.
- [ ] F2 Adaptar el paquete a esos campos: un archivo `retos/<ID>/entrega/pegar-en-formulario.md` por reto, ya recortado a los límites reales.
- [ ] F3 Si admite uno solo: dejar listo solo RIE-03 y marcar los demás como material de portafolio.
- [ ] F5 (opcional, solo si el formulario admite enlace o adjunto de video) Preparar un explicativo de 45–60 s de RIE-03 con las skills de HyperFrames; si no lo admite, se deja para la fase presencial.
- [ ] F4 Dejar a Mariano una nota con los 3 pasos exactos para enviar. **Enviar solo si Mariano lo autoriza explícitamente en el chat.**

## Registro de decisiones tomadas sin consultar

- 25.11, 21:01 — Con la sesión de la plataforma sin iniciar, se adelantó la versión en Word (E1) antes que los videos restantes (I5): sirve para adjuntar o llenar una plantilla si la plataforma la pide.

- 25.11 — I4 hecho: `video/rie-03/` (44 s, 7 escenas, sin narración y sin música; MP4 de 3,7 MB en `video/rie-03/out/rie-03-explicativo.mp4`, no versionado; render en 55 s; `check` sin errores). Contenido tomado solo del deck de RIE-03. Se corrigieron antes del render dos defectos visibles: una palabra final que no se animaba en tres títulos y una etiqueta cortada. Se omitieron los tres guiones alternativos y `SPEC.md` de HyperFrames por trabajar de forma autónoma; el guion es el del deck.

- 25.11 — Identidad: nombre inspirado en la yupana (solo inspiración visual, sin afirmaciones históricas); paleta tinta, maíz, turquesa, terracota y papel; Sora e Inter en documentos y Outfit (incluida en HyperFrames) en video.
- 25.11 — HyperFrames: no se ejecutó el aviso de uso (`events`) que pide su skill porque envía una nota a un servicio externo ligada a la cuenta; se informará a Mariano. `usage --json` devolvió «desconocido».
- 25.11 — Los videos de más de 15 s deberían llevar música según la guía de HyperFrames; no hay forma local y verificable de obtener música con licencia, así que el primer corte de I4 será silencioso y se dejará anotado.

- 25.11 — Mariano autorizó el push en el chat; se hizo (13 commits, hasta `89c0ee4`). El repo seguía público al momento del push. Los commits posteriores quedan locales salvo nueva autorización.

- 24.11 — **Push bloqueado.** El sistema de permisos negó `git push` por posible filtración de información sensible: el repositorio de GitHub sigue **público** y los commits llevan contenido derivado de los expedientes de la Caja. No se intentó evitar el bloqueo. Todo queda en commits locales hasta que Mariano pase el repo a privado o autorice el push en el chat.
- 24.11 — NEG-02: premisa de deuda externa pasa a supuesto (centrales de riesgo), 31 % rotulado con la tasa de consentimiento supuesta (65 %), script de auditoría declarado como preexistente, plan pesimista de 41 h dicho en el texto.
- 24.11 — RIE-02: se agrega que una regla de dominio ajustada a mano rinde F1 ≈ 0,9 y que el aporte esperado es moderado; se declara que las pruebas del generador incluyen reglas de control; se agrega protección de datos y el momento de la evaluación (antes del desembolso, supuesto); se unifica la lista de relaciones legítimas.
- 24.11 — Se quitaron de los archivos versionados los nombres de pila de los Challenge Owners (quedan en `expediente.md`, que no se sube).
- 24.11 — Fallo y corrección: un reemplazo con expresión regular dejó marcadores de grupo en la postulación de NEG-02; se restauró desde el commit anterior y se reaplicó con la función corregida; se verificó que ningún archivo versionado conserve residuos.
- 24.11 — RIE-01: la postulación compromete la **versión mínima** del panorama (K1 y K2 en 3 eventos) y presenta K3, K4 y seis eventos como ampliación; se declara el script de auditoría como preexistente (entrena un modelo de referencia solo para medir la dificultad de los datos); el bloque «Complejidad tecnológica» de RIE-01 se capturó de la plataforma y se alineó el concepto.
- 24.11 — RIE-03: «cola diaria» pasa a «cola priorizada» (los datos son mensuales); la evidencia estrella pasa a la población que importa (clientes al día: AUC 0,84, ≈ 2/3 en el 10 % mejor, precisión 4,7 %); se declara el script de auditoría como preexistente; el plan base es el mínimo viable de 31,5 h; se agrega una ilustración aritmética del efecto rotulada como escenario.
- 24.11 — La entrega se prepara en 4 formatos porque el formulario no existe todavía.
- 24.11 — La revisión independiente la hace un agente revisor (no humano) por falta de tiempo; se rotula así.
