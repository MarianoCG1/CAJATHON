# Prompts de inicio por persona

Cada integrante abre su agente (Claude Code, Codex/GPT, Antigravity u otro) **dentro de la carpeta del repositorio** y pega el prompt de su nombre. Todos hacen lo mismo primero: leer `AGENTS.md`, ubicarse y empezar por su primera tarea.

## 0. Antes del prompt (una sola vez)

El repositorio es **privado**: Mariano debe invitar a cada persona como colaboradora en GitHub (Settings → Collaborators).

```powershell
git clone https://github.com/MarianoCG1/CAJATHON.git
cd CAJATHON
pip install pytest pandas numpy
python -m pytest -q
```

Si las pruebas pasan, el entorno está listo. Luego, **copiar de la plataforma** (https://cajathon.cajatrujillo.com.pe/equipos/) el texto literal de los expedientes de sus retos a `retos/<ID>/expediente.md`. Esos archivos están en `.gitignore`: no se suben.

Antes de trabajar, cada uno crea su rama: `git checkout -b reto/<id>-<nombre>` (por ejemplo `reto/neg-01-glem`).

## 1. Prompt de Mariano (coordinador, developer)

```
Soy Mariano, coordinador del equipo Yupana Labs en el Cajathon 2026. Estás en el repositorio del equipo.

Antes de hacer nada, lee completos AGENTS.md, retos/README.md y la ficha retos/<ID>/README.md de cada reto que lidero: RIE-03, NEG-02, RIE-01 y RIE-02 (reviso COM-02). Resúmeme en 10 líneas dónde estamos y qué falta, sin modificar archivos.

Somos una consultora TI: hasta el 25.11 solo desarrollamos el Concepto de solución de cada desafío; no se construye ningún prototipo antes del 03.12. Respeta las reglas de AGENTS.md: solo datos sintéticos, expedientes confidenciales, nada inventado (todo lo no oficial va como (supuesto) o [POR CONFIRMAR]).

Mis tareas, en este orden:
1. Verificar que los datos sintéticos de RIE-03, NEG-02 y RIE-01 no se resuelvan con una regla trivial (en RIE-02 ya se endureció). Corre cada generador, prueba un modelo o regla simple contra la verdad de terreno y dime si el backtest tendría sentido. Propón cambios; no los apliques sin mostrármelos.
2. En el Anexo B de concepto.md de mis cuatro retos, reformular las preguntas al owner como preguntas de comprensión del problema (la organización dijo que en esta etapa no entrega datos).
3. Apoyar a quien se atrase, empezando por NEG-01.
4. Preparar (sin enviar) el texto final de cada postulacion.md para cargarlo yo en la plataforma el 25.11.

No envíes mensajes ni postules por mí. Trabaja en una rama reto/<id>-mariano, con commits pequeños en español, y al terminar cada tarea dame: resumen corto, archivos tocados y siguiente paso.
```

## 2. Prompt de Glem (analista de datos)

```
Soy Glem, analista de datos del equipo Yupana Labs en el Cajathon 2026. Estás en el repositorio del equipo.

Antes de hacer nada, lee completos AGENTS.md y retos/README.md. Luego lee la ficha retos/<ID>/README.md de mis retos: lidero en pareja NEG-01 (con Antonio), NEG-03 (con David), COM-01 (con Antonio) y COM-02 (con David), y reviso RIE-03 y RIE-01. Resúmeme en 10 líneas qué me toca y en qué orden, sin modificar archivos.

Contexto: somos una consultora TI; hasta el 25.11 solo desarrollamos el Concepto de solución de cada desafío (8 secciones + panorama + texto de postulación). No se construye ningún prototipo antes del 03.12. Reglas de AGENTS.md: solo datos sintéticos, expedientes confidenciales, nada inventado (todo lo no oficial va como (supuesto) o [POR CONFIRMAR]).

Mis tareas, en este orden:
1. Revisión cruzada de RIE-03 y luego RIE-01: leer concepto.md, panorama.md y postulacion.md contra el expediente literal (si ya lo copié a expediente.md) y el Anexo C del concepto. Escribir las objeciones en retos/<ID>/revision.md; no editar el concepto, eso lo hace la pareja líder. Fíjate sobre todo en datos, modelo, backtest y si un modelo trivial resolvería el dataset.
2. Corregir mis niveles de habilidad en scripts/sinergia/team.json (hoy son estimaciones) y regenerar el ranking si cambian.
3. NEG-01 (prioridad #2): concepto v1, panorama con cotejo y postulación, trabajando con Antonio. Modelo a imitar: retos/RIE-03/. Lo mío es la parte de datos, modelo y métricas; Antonio cubre KPI y negocio.
4. Después NEG-03, COM-01 y COM-02 en ese orden, mientras haya tiempo.

No envíes mensajes ni postules por mí. Trabaja en una rama reto/neg-01-glem (o la que corresponda), con commits pequeños en español, y al terminar cada tarea dame: resumen corto, archivos tocados y siguiente paso.
```

## 3. Prompt de Antonio (economista)

```
Soy Antonio, economista del equipo Yupana Labs en el Cajathon 2026. Tengo experiencia en el sector financiero (operaciones, comercial, negocios). Estás en el repositorio del equipo.

Antes de hacer nada, lee completos AGENTS.md y retos/README.md. Luego lee la ficha retos/<ID>/README.md de mis retos: lidero en pareja NEG-01 (con Glem), NEG-02 (con Mariano), RIE-01 (con Mariano) y COM-01 (con Glem), y reviso RIE-02 y NEG-03. Resúmeme en 10 líneas qué me toca y en qué orden, sin modificar archivos.

Contexto: somos una consultora TI; hasta el 25.11 solo desarrollamos el Concepto de solución de cada desafío (8 secciones + panorama + texto de postulación). No se construye ningún prototipo antes del 03.12. Reglas de AGENTS.md: solo datos sintéticos, expedientes confidenciales, nada inventado: los expedientes no publican KPI ni línea base, así que cualquier cifra va como (supuesto) o [POR CONFIRMAR]. Yo soy el dueño del KPI y del caso de negocio de cada concepto.

Mis tareas, en este orden:
1. Revisión cruzada de RIE-02: leer concepto.md, panorama.md y postulacion.md contra el expediente literal (si ya lo copié a expediente.md) y el Anexo C del concepto. Fíjate en que el impacto en el KPI esté bien planteado, con método de medición y sin cifras inventadas. Escribir objeciones en retos/RIE-02/revision.md; no editar el concepto.
2. En NEG-02 y RIE-01: leer la sección de impacto y KPI de concepto.md y panorama.md y decirme qué es débil desde la lógica financiera (supuestos de morosidad, costo, ingresos). Proponer mejoras como texto, para que yo las revise.
3. NEG-01 (prioridad #2) con Glem: concepto v1, panorama con cotejo y postulación. Modelo a imitar: retos/RIE-03/. Yo cubro KPI, caso de negocio y viabilidad económica; Glem cubre datos y modelo.
4. Después COM-01 y la revisión de NEG-03.

No envíes mensajes ni postules por mí. Trabaja en una rama reto/neg-01-antonio (o la que corresponda), con commits pequeños en español, y al terminar cada tarea dame: resumen corto, archivos tocados y siguiente paso.
```

## 4. Prompt de David (ing. industrial, UX/UI)

```
Soy David, ingeniero industrial y UX/UI del equipo Yupana Labs en el Cajathon 2026. Me enfoco en usuarios, flujos y prototipado. Estás en el repositorio del equipo.

Antes de hacer nada, lee completos AGENTS.md y retos/README.md. Luego lee la ficha retos/<ID>/README.md de mis retos: lidero en pareja RIE-03 (con Mariano), RIE-02 (con Mariano), NEG-03 (con Glem) y COM-02 (con Glem), y reviso NEG-01, NEG-02 y COM-01. Resúmeme en 10 líneas qué me toca y en qué orden, sin modificar archivos.

Contexto: somos una consultora TI; hasta el 25.11 solo desarrollamos el Concepto de solución de cada desafío (8 secciones + panorama + texto de postulación). No se construye ningún prototipo antes del 03.12. Reglas de AGENTS.md: solo datos sintéticos, expedientes confidenciales, nada inventado (todo lo no oficial va como (supuesto) o [POR CONFIRMAR]).

Mis tareas, en este orden:
1. Revisión cruzada de NEG-02 (ya desarrollado): leer concepto.md, panorama.md y postulacion.md contra el expediente literal (si ya lo copié a expediente.md) y el Anexo C. Fíjate en el flujo del usuario: quién usa la solución, en qué momento, qué decide y qué ve. Escribir objeciones en retos/NEG-02/revision.md; no editar el concepto.
2. En RIE-03 y RIE-02: revisar la sección de funcionalidad crítica y de interfaz del concepto y el panorama y decirme si el flujo del gestor es claro y cabe en el evento. Proponer un esquema simple de pantalla en texto.
3. NEG-03 y COM-02 con Glem: concepto v1, panorama con cotejo y postulación; yo cubro flujo del usuario, proceso actual y propuesto, y la demo. Modelo a imitar: retos/RIE-03/.
4. Cuando NEG-01 y COM-01 tengan concepto v1, hacer su revisión cruzada.

No envíes mensajes ni postules por mí. Trabaja en una rama reto/neg-03-david (o la que corresponda), con commits pequeños en español, y al terminar cada tarea dame: resumen corto, archivos tocados y siguiente paso.
```

## Notas

- Si el agente propone cambiar la estructura de carpetas, las parejas o las reglas, que lo consulte con Mariano antes.
- El primer prompt de cada persona pide un resumen sin modificar archivos: sirve para confirmar que el agente entendió el repositorio antes de tocar nada.
- Cuando alguien termine una tarea, marca la casilla en `retos/<ID>/README.md` y regenera el tablero con `python scripts/boveda/generar_boveda.py`.
