# Bases oficiales y panorama de la competencia

Fuente: https://cajathon.cajatrujillo.com.pe/bases/ (**versión 4, revisión 05.11.2026**) y página de inicio pública. Leído el 21.11.2026.
Lo marcado **(supuesto)** es inferencia nuestra, no dato oficial.

## 1. Cambios respecto a lo que teníamos (CLAUDE.md citaba la v3)

| Tema | Antes (CLAUDE.md) | Ahora (bases v4) |
|---|---|---|
| Versión | v3, 20.10 | **v4, 05.11** |
| Equipos en fase virtual | no indicado | **18 equipos** |
| Finalistas | 12 | 12 (se mantiene) |
| Nombre del entregable del 24.11 | Solution Concept | Solution Concept en las bases; la web lo llama **Challenge Solution Brief** y «Concepto de solución» en la plataforma |
| Entregables en el Hub | prototipo, demo, evidencia | además la web nombra: **Test & Learning Snapshot** y, al cierre, **Portfolio Report** (qué avanza, itera o se detiene) |
| Desafíos | 5 publicados | «hasta seis»; la web pública muestra 6 en 4 categorías (Comercial, Negocios, Riesgos, Recuperaciones) con detalle aún «muy pronto» |

Acción: confirmar con el owner cuál es el formato exacto del documento del 24.11, porque las bases dicen que la organización «comunicará el formato y mecanismo de presentación».

## 2. Reglas que condicionan nuestro diseño

- **Funcionalidad crítica:** «desarrollo nuevo o adaptación sustantiva» construida durante la fase presencial. Condición eliminatoria: promedio mínimo **3/5** en funcionamiento de la funcionalidad crítica (§5.2). Productos preexistentes sin avance sustantivo no cuentan.
- **Evidencia de desarrollo:** historial de versiones o repositorios que permitan verificar el avance respecto del Solution Concept. Hay que commitear con frecuencia durante los dos días.
- **Preexistente:** hay que identificar titularidad y condiciones de uso en el Solution Concept y **actualizarlo en la entrega final** (§8.3). Cubierto en `docs/preexistente.md`.
- **Propiedad intelectual:** ganadores ceden derechos patrimoniales **solo** de lo desarrollado en el hackathon; no equipos ganadores conservan los suyos y dan a la Caja una autorización no exclusiva para revisión. Cualquier uso posterior requiere acuerdo aparte.
- **IA externa:** §8.2 habla de «restricciones aplicables al uso de plataformas externas y herramientas de inteligencia artificial» sin detallarlas. **Pregunta abierta clave** para el owner; el proveedor de LLM debe seguir siendo intercambiable.
- **Datos:** la Caja podrá dar «información de referencia, datos sintéticos y otros recursos» (§7.2). Prohibido datos personales reales o credenciales institucionales.
- **Apoyo disponible:** Challenge Owners, Caja Experts (Legal, Seguridad, Compliance) y Tech Mentors (4–6). Usarlos: validar con Legal/Seguridad suma a viabilidad.
- **Infraestructura:** laptop propia, internet y comida en el Hub Digital UPAO (Av. América Sur 3145). Horario 9:00–18:00 ambos días.
- **Posible bono (no puntaje):** los datos de quienes consientan pueden usarse en futuros procesos de selección de la Caja; las soluciones de interés pueden recibir contacto aunque no ganen.

## 3. Criterios de puntaje (sin cambios)

Pase a finalistas: Alineación 25 · Impacto 30 · Viabilidad técnica 25 · Factibilidad de construcción 20.
Final: Impacto 35 (KPI 25 + escalabilidad 10) · Funcionalidad y validación 35 (funcionalidad crítica 20 + pruebas 15) · Innovación 20 (diferenciación 15 + simplicidad 5) · Presentación y demo 10 (5+5).

## 4. Panorama de la competencia

Datos oficiales:
- «+70 postulaciones» → **18 equipos** seleccionados → **12 finalistas** → **2 ganadores**.
- Perfiles objetivo: software factories, startups, universitarios y profesionales. Se valora la experiencia en el sector financiero.
- Premios: S/ 5,000 y S/ 3,000.

Inferencias **(supuesto)**:
- 18 equipos en 6 desafíos ≈ 3 equipos por desafío. Nosotros competimos con ~2 equipos en REC-01 si el reparto fuera parejo. Falta saber si los 12 cupos se asignan por desafío o por ranking global; la web dice que se evalúan «las 18 propuestas», lo que sugiere ranking global.
- Pasar de 18 a 12 es el 67%: el primer filtro es poco exigente. La diferenciación real ocurre en el Demo Day.
- Los rivales serán probablemente software factories con componentes reutilizables y equipos con más gente (nosotros somos 4, el máximo permitido). Nuestra ventaja debe estar en conocimiento del dominio financiero, simplicidad y evidencia medible.

Qué sabemos de los demás equipos: **nada**, la información no es pública. No intentar averiguarlo por canales no oficiales.

## 5. Implicancias para la estrategia

1. El 24.11 se decide por **alineación al desafío** (25%) e **impacto** (30%): el concepto debe citar el KPI y la línea base con números del expediente.
2. En el Hub gana quien muestre **una funcionalidad crítica real, con pruebas y un número antes/después**. Dejar claro en el concepto qué se construye en el evento y qué es preexistente.
3. Preparar desde ya el **ensayo de 8 h**, el repo con historial limpio y `docs/validacion.md` alimentado por el backtest.
4. Usar a los Caja Experts para cerrar la política de IA y de datos antes del 03.12.

## 6. Pendiente

- Contenido de la plataforma de equipos (expediente REC-01, datos de referencia, owner, canal de consultas, formato del concepto). **Requiere que alguien del equipo inicie sesión**; el acceso es con documento de identidad y correo de postulación.
- Contacto general: cajathon@cajatrujillo.com.pe (según la web pública).
