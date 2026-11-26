# Componentes preexistentes y titularidad

Todo lo que exista **antes del 03.12** y se reutilice en la solución se declara aquí. La funcionalidad crítica se construye en el evento y no figura en esta lista.

Actualizado el 25.11.2026. Los generadores de datos son preexistentes para **los cuatro desafíos preparados**; si el equipo avanza con uno solo, en la entrega final solo se declara el de ese desafío.

| Componente | Descripción | Titular | Fecha de creación | Se cede si ganamos |
|---|---|---|---|---|
| Repo base / estructura | Carpetas por reto (`retos/<ID>/`), `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, README, fichas de reto, `.gitignore`, `pytest.ini`, esqueleto vacío de `backend/` y `frontend/` | Equipo | 21.11.2026 | No (preexistente) |
| `scripts/sinergia/` | Herramienta de planificación: puntaje de sinergia por pareja y prioridad de desafíos. No forma parte del producto | Equipo | 21.11.2026 | No (preexistente) |
| `scripts/conceptos/` | Generador de borradores de concepto. No forma parte del producto | Equipo | 21.11.2026 | No (preexistente) |
| `scripts/entrega/` | Armado de los paquetes de entrega (campos del formulario, resumen, ficha de una página en PDF, checklist) a partir de los textos de postulación. No forma parte del producto | Equipo | 24.11.2026 | No (preexistente) |
| `identidad/` y `scripts/identidad/` | Identidad visual de Yupana Labs: guía de marca, logos, patrón y tokens. Es material de comunicación del equipo; no forma parte del producto | Equipo | 25.11.2026 | No (preexistente) |
| `video/` | Videos de comunicación del equipo hechos con HyperFrames (sting de marca y explicativo de RIE-03): HTML, generadores y guion; los MP4 no se versionan. Usan datos ficticios y solo cifras del deck. Son material de comunicación, no un prototipo | Equipo | 25.11.2026 | No (preexistente) |
| `scripts/presentacion/` y `retos/<ID>/presentacion/` | Material de presentación de los cuatro retos desarrollados (storytelling, guion de demo, preguntas del jurado, deck PDF con maquetas ilustrativas y datos ficticios). Es material de comunicación, **no un prototipo** y no adelanta la funcionalidad crítica | Equipo | 25.11.2026 | No (preexistente) |
| `scripts/auditoria/` | Comprobaciones de dificultad de los datasets sintéticos (¿se resuelve con una regla trivial?). No son los modelos de los retos ni forman parte del producto | Equipo | 21.11.2026 | No (preexistente) |
| `scripts/boveda/` y `boveda/` | Generador y notas de la bóveda de conocimiento (competencia, decisiones, tablero de avance). No forma parte del producto | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-03/datos/` (`generar.py`, `test_generar.py`) | Generador de cartera MYPE sintética para RIE-03: clientes, créditos, cuotas, saldos, señales mensuales, gestiones y verdad de terreno. Semilla fija. No contiene modelo, agente, API, interfaz ni backtest | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-03/datos/sintetico/` | Salida del generador anterior (CSV, diccionario y metadatos). 100 % sintética | Equipo | 21.11.2026 | No (preexistente) |
| `retos/NEG-02/datos/` (`generar.py`, `test_generar.py`) | Generador de un ecosistema abierto ficticio para NEG-02: entidades «Demo», clientes con productos en varias entidades, transacciones, catálogo, consentimientos con alcance, vigencia y revocación, y verdad de terreno separada. No contiene APIs, servicio de consentimiento, vista 360, motor de oportunidades, agente ni interfaz | Equipo | 21.11.2026 | No (preexistente) |
| `retos/NEG-02/datos/sintetico/` | CSV, diccionario y `manifest.json` del generador (100 % sintéticos, regenerables). La subcarpeta `verdad/` es solo para medición | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-01/datos/` (`generar.py`, `test_generar.py`) | Generador de datos 100 % sintéticos para RIE-01: distritos y sectores del norte del Perú, clientes MYPE y créditos en S/, mapa de amenaza con error, escenarios, eventos históricos y eventos de prueba con verdad oculta. No contiene el modelo de exposición, escenarios operativos, mapa ni agente | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-01/datos/sintetico/` | CSV del generador (semilla 20261203, 12.000 clientes); incluye `backtest/` con la verdad de los eventos simulados | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-02/datos/` (`generar.py`, `test_generar.py`) | Generador de solicitudes y su grafo para RIE-02: personas, negocios, teléfonos, dispositivos, direcciones y referencias ficticios, con redes de fraude inyectadas y relaciones legítimas «señuelo». No contiene detector, priorización, agente ni interfaz como solución (sus pruebas incluyen reglas de control, de coincidencia simple y de criterio de dominio, solo para comprobar que los datos no son triviales; se reescriben en el evento como línea comparativa) | Equipo | 21.11.2026 | No (preexistente) |
| `retos/RIE-02/datos/sintetico/` | Salida del generador (semilla 2026): documentos y teléfonos con prefijo `FIC-`. Regenerable con el script | Equipo | 21.11.2026 | No (preexistente) |
| `retos/COM-01/datos/` (`generar.py`, `test_generar.py`) | Territorio sintético para COM-01: zonas comerciales ficticias, señales públicas simuladas, historial de visitas y verdad oculta. No contiene planificador, agente, API ni interfaz | Equipo | 25.11.2026 | No (preexistente) |
| `scripts/auditoria/auditar_com01.py` | Simulación que compara estrategias de visita. **Contiene una versión mínima de la estrategia de aprendizaje; no se reutiliza:** el planificador se escribe desde cero en el evento | Equipo | 25.11.2026 | No (preexistente) |

## Experiencia previa (no se reutiliza código)

Ideas y experiencia del developer en automatización de cierre de pagos, OCR con conciliación, agentes con aprobación humana y modelos predictivos. **No se copia código** de empleadores ni de otros clientes (ver CLAUDE.md §5).

## Declaración

- No se usan datos reales ni credenciales institucionales.
- Las librerías de terceros (FastAPI, pandas, scikit-learn, React, etc.) se usan bajo sus licencias abiertas.
- Los parámetros, tasas, umbrales y probabilidades de los generadores son **supuestos del equipo**; no provienen de la Caja ni de datos reales.
- Los generadores de RIE-02 usan nombres, teléfonos y documentos ficticios; no contienen datos reales ni material de la Caja.
- La funcionalidad crítica del desafío que avance (modelo, agente, API, interfaz y backtest, según el caso) **no** es preexistente y se construye entre el 03 y el 04.12 con historial git.
- Si el equipo usa datos entregados por la Caja, se declaran aparte como material de la organización.
