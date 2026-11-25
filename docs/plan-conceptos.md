# Plan para abordar los 8 conceptos (21–26.11)

Objetivo: postular un Concepto de solución sólido por cada desafío, en orden de prioridad, sin sacrificar la calidad de los primeros. Todo lo no oficial va marcado como **(supuesto)** o **[POR CONFIRMAR]**.

## 0. Condición previa (puerta de decisión)

Falta confirmar con la organización si un equipo puede postular **más de un** concepto (la plataforma dice «el desafío que eligieron», en singular) y si los 8 expedientes son elegibles (hablan de 6). Mensaje listo en `docs/investigacion/03-equipo-y-alcance.md` §6.

- **Si se permite:** se postulan los 8 en el orden de prioridad.
- **Si no se permite:** se postula el **#1 (RIE-03)** con todo el esfuerzo del equipo. Los otros 7 borradores quedan como material de portafolio.

## 1. Qué ya está listo

| Pieza | Dónde |
|---|---|
| Análisis de bases, plataforma y expedientes | `docs/investigacion/01` y `02` |
| Equipo, estrategia y puntaje de sinergia por pareja | `docs/investigacion/03` y `04`, `scripts/sinergia/` |
| Ranking de prioridad de los 8 | `docs/investigacion/04-sinergia-retos-parejas.md` §5 |
| **8 borradores v0 del concepto** (8 secciones + anexos) | `retos/<ID>/concepto.md` |
| Generador de borradores | `scripts/conceptos/generar_borradores.py` (no pisa archivos editados sin `--forzar`) |

## 2. Flujo de cada concepto

1. **v0 (generado):** estructura, problema, KPI candidatos, funcionalidad crítica, tareas y brechas.
2. **v1 (pareja líder):** completa y mejora redacción, afina la funcionalidad crítica y el alcance, reduce lo genérico. Todo lo oficial, con las palabras del expediente.
3. **Revisión cruzada (revisor):** alguien que **no** lo escribió pasa el Anexo C. Anota objeciones en el archivo.
4. **v2:** la pareja resuelve las objeciones. Si el owner ya respondió, se actualizan KPI y línea base.
5. **Final:** coordinador revisa la consistencia con el formato de la plataforma y lo carga.

**Definición de terminado:** las 8 secciones completas · Anexo C marcado · ninguna cifra inventada · preguntas al owner enviadas · revisado por otra persona.

## 3. Quién hace qué

| # | Desafío | Pareja líder | Revisor |
|---|---|---|---|
| 1 | RIE-03 Deterioro de pago | David + Mariano | Glem |
| 2 | NEG-01 Cuotas flexibles | Antonio + Glem | David |
| 3 | NEG-02 Open Finance | Antonio + Mariano | David |
| 4 | RIE-01 Clima | Antonio + Mariano | Glem |
| 5 | RIE-02 Redes de riesgo | David + Mariano | Antonio |
| 6 | NEG-03 Cambio de analista | David + Glem | Antonio |
| 7 | COM-01 Captación | Antonio + Glem | David |
| 8 | COM-02 Incentivos | David + Glem | Mariano |

Cada persona lidera 4 conceptos y revisa 2 (Mariano revisa 1 y además coordina). Reparto según `scripts/sinergia`; si alguien prefiere cambiar, se cambia: las parejas son una recomendación, no una regla.

## 4. Calendario

| Día | Foco |
|---|---|
| **Sáb 21** | Revisar este plan, corregir niveles en `team.json`, enviar consultas a la organización. Empezar v1 de RIE-03 y NEG-01 |
| **Dom 22** | v1 de RIE-03, NEG-01 y NEG-02. Primeras revisiones cruzadas |
| **Lun 23** | v2 de los tres primeros. v1 de RIE-01 y RIE-02 |
| **Mar 24** | v1 de NEG-03, COM-01 y COM-02. Revisión cruzada de todo |
| **Mié 25** | v2 y final de todos; la plataforma abre ese día. Cargar en orden de prioridad |
| **Jue 26** | Reserva para correcciones y cierre (**confirmar la hora límite**) |

Si el tiempo aprieta, se recorta desde el final de la lista (COM-02, COM-01), no desde el principio.

## 5. Consultas a los owners

- Se envían por ticket apenas se abran, o por WhatsApp/correo de la organización mientras tanto.
- Cada borrador tiene su Anexo B con las preguntas. Se agrupan por owner: (ver plataforma) son owners de RIE-03, NEG-03 y COM-02; (ver plataforma) también de COM-01.
- Prioridad de preguntas: **KPI y línea base**, datos sintéticos (columnas y volumen) y política de IA externa.

## 6. Reglas que no se rompen

- **Sin datos reales ni credenciales institucionales.** Repo privado mientras contenga material de la Caja.
- **Sin prototipos de la funcionalidad crítica antes del 03.12** en los desafíos que podrían avanzar a la final: debe construirse en el evento. Sí se permite preparar herramientas generales (generador de datos sintéticos, plantillas), declaradas en `docs/preexistente.md`.
- **Sin cifras inventadas.** Si falta el dato, va **[POR CONFIRMAR]**.
- **Un concepto sólido vale más que ocho flojos:** la calidad de los primeros no se negocia.

## 7. Si varios conceptos llegan a la final

El criterio de la organización para 12 finalistas de 18 equipos no aclara qué pasa si un mismo equipo tiene varios aprobados. **Preguntarlo antes de postular**: si hubiera que construir más de uno, el equipo elige uno y no se construyen los demás.

## 8. Portafolio en GitHub

Tu idea de que sirva para el portafolio es buena, con límites por la confidencialidad (bases §8.2):

| Se puede publicar | No se publica |
|---|---|
| `scripts/sinergia/` (herramienta genérica; quitar nombres y expedientes si se quiere) | Texto, resúmenes o capturas de los expedientes y de la plataforma |
| Generador de datos sintéticos propio | KPI, líneas base o cualquier dato entregado por la Caja |
| Arquitectura y código del prototipo con datos 100 % sintéticos propios, **después** del evento y sin referencias internas | `conceptos.json`, `retos/<ID>/concepto.md` y `docs/investigacion/` (contienen contenido de los expedientes) |
| Tests, README técnico, decisiones de diseño | Nombres de owners, contactos, logos o marca de la Caja |

Recomendación: repo **privado** para todo el trabajo del hackathon y, cuando termine el evento, un repo público **limpio** con solo lo publicable. Si el equipo gana, la Caja recibe la cesión de los derechos patrimoniales de lo desarrollado en el evento: consultar antes de publicar ese código.
