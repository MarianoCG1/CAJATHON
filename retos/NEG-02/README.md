# NEG-02 · Open Finance: competir en un ecosistema financiero abierto

| | |
|---|---|
| **Prioridad** | #3 de 8 (ranking en `docs/investigacion/04-sinergia-retos-parejas.md`) |
| **Eje** | 5 Open Finance y nuevos modelos de competencia |
| **Pareja líder** | Antonio + Mariano |
| **Revisor (no escribe este reto)** | David |
| **Owners en la plataforma** | (ver plataforma) |
| **Avance** | se calcula solo: `boveda/Tablero.md` |

## En una frase

Sandbox de Open Finance con APIs y consentimientos simulados que construye una vista 360 del cliente y un agente que detecta oportunidades de producto con su autorización. *(supuesto del equipo, no del expediente)*

## Qué hay en esta carpeta

| Archivo | Para qué sirve | Estado |
|---|---|---|
| `expediente.md` | Texto literal del reto copiado de la plataforma. **Confidencial: solo local, está en `.gitignore`** | ⬜ cada persona lo copia de la plataforma |
| `concepto.md` | Concepto de solución (8 secciones + anexos). Ya editado a v1. | ✅ existe |
| `panorama.md` | Cómo se abastecería el reto: datos, modelo, arquitectura, plan del evento, KPI, riesgos, cotejo con el expediente | ✅ existe |
| `postulacion.md` | Texto para pegar en el formulario de la plataforma (25–26.11) | ✅ existe |
| `datos/` | Generador de datos sintéticos con pruebas (`generar.py`, `test_generar.py`); la salida va a `datos/sintetico/` (ignorada por git) | ✅ existe |

## Qué toca hacer hasta el 25.11

Marca las casillas editando este archivo y haz commit. El avance automático lo lee `boveda/Tablero.md`.

- [ ] Copiar el expediente desde la plataforma a `retos/NEG-02/expediente.md` (solo local).
- [ ] **Revisión cruzada** (David): leer `concepto.md`, `panorama.md` y `postulacion.md` contra el expediente y el Anexo C de `concepto.md`; anotar objeciones en `retos/NEG-02/revision.md`.
- [ ] La pareja líder resuelve las objeciones (v2) y actualiza `postulacion.md`.
- [ ] Comprobar que los datos sintéticos no se resuelven con una regla trivial (en RIE-02 ya se endureció): correr el generador y probar un modelo simple.
- [x] Preguntas del Anexo B reformuladas a **comprensión** del problema (21.11, Mariano).
- [ ] Decisión de postular (sí/no) — la toma el coordinador con el equipo.

## Reglas de este reto

- Todo lo que no venga del expediente va marcado **(supuesto)** o **[POR CONFIRMAR]**. Ninguna cifra inventada.
- Datos solo sintéticos. La funcionalidad crítica **no se construye antes del 03.12**.
- Contraste siempre con el expediente literal; si el texto del concepto y el expediente chocan, manda el expediente.

## Funcionalidad crítica propuesta (supuesto)

Sandbox con APIs y consentimientos simulados que arma una vista 360 del cliente a partir de varias entidades y un agente que identifica oportunidades de producto o servicio, siempre dentro del consentimiento otorgado.

## Preguntas para el owner (de comprensión; ver Anexo B del concepto)

- ¿Qué busca ganar la Caja con Open Finance: conocer mejor al cliente, captar clientes de otras entidades, retener, incluir? ¿Cuál pesa más y cómo mediría el éxito de una oferta (aceptación, monto colocado)?
- ¿Se imagina a la Caja solo como receptora de datos de otras entidades o también como proveedora?
- ¿Qué reglas de consentimiento (alcance, vigencia, finalidad, revocación) deben respetar las ofertas hechas con datos de terceros? ¿Legal y Compliance revisarían el texto?
- ¿Qué productos de la Caja podrían ofrecerse a partir de esta información y con qué condiciones generales?
- ¿Qué datos propios de la Caja pueden usarse para ofertas sin pedir un consentimiento adicional?
- ¿Qué controles de seguridad esperan ver (autenticación entre entidades, auditoría, cifrado, retención)?
- ¿Se espera conformidad con algún estándar de APIs abiertas o basta un entorno de prueba coherente que simule el intercambio?
- ¿Hay restricciones para usar IA externa (aun con datos sintéticos)?
