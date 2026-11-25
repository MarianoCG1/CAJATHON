# Identidad de Yupana Labs

Guía de marca del equipo que resuelve los retos. **Todo lo que salga del equipo —presentaciones, fichas, videos, documentos y código de demostración— usa esta identidad.** Los activos se generan con `python scripts/identidad/generar_identidad.py`; no se editan a mano.

## 1. Quiénes somos

**Yupana Labs** es un equipo de cuatro personas que trabaja como una pequeña consultora de tecnología: toma un problema real de negocio, lo entiende, lo diseña y lo demuestra con evidencia. Desarrollo y datos (Mariano, Glem), negocio y finanzas (Antonio) y experiencia de usuario (David).

**Nombre.** *Yupana* es el tablero andino de cálculo: una herramienta para contar y decidir. La marca se inspira visualmente en él: columnas de casillas que se llenan con semillas (1, 2, 3, 5…). Es una inspiración de diseño; no afirmamos nada histórico sobre su uso.

**Idea de marca.** *Contar bien para decidir mejor.* Cada propuesta nuestra convierte datos en una decisión humana con evidencia, y dice con claridad qué está medido y qué es un supuesto.

## 2. Voz y tono

- **Claro y directo.** Frases cortas, sin jerga innecesaria. Una idea por lámina.
- **Honesto.** Distinguimos siempre lo **medido** (sobre datos sintéticos propios), lo **supuesto** y lo **por confirmar**. No inventamos cifras de impacto.
- **Humano.** Cuentan personas (la asesora, la ejecutiva, la gestora, el especialista), no solo algoritmos. Los personajes son ficticios y se rotulan así.
- **Propositivo.** Proponemos y explicamos; la decisión final es siempre de una persona.
- **Idioma:** español neutro del Perú.

## 3. Logo

| Archivo | Uso |
|---|---|
| `logo-horizontal.svg` | Sobre fondo oscuro (tinta): portadas, cierres, video |
| `logo-horizontal-claro.svg` | Sobre fondo claro (papel o blanco): documentos, fichas |
| `logo-marca.svg` / `logo-marca-claro.svg` | Solo la marca: esquinas de láminas, favicon, sellos |
| `patron-yupana.svg` | Fondo tenue de portadas y cierres |

La marca son cuatro columnas de casillas con 1, 2, 3 y 5 semillas doradas; la última semilla de la columna más alta es turquesa (la chispa: el dato verificable). **No** deformar, girar, cambiar colores, añadir sombras ni colocarla sobre fondos que reduzcan el contraste. Dejar alrededor un margen mínimo igual al diámetro de una semilla.

## 4. Color

| Color | Hex | Rol |
|---|---|---|
| **Tinta** | `#0E1A3A` | Fondo oscuro y texto principal |
| **Maíz** | `#F4B63F` | Acento principal (la semilla): cifras, viñetas, subrayados |
| **Turquesa** | `#1BB5A8` | Acento secundario (lo verificable): formas, estados «después» |
| **Terracota** | `#E4572E` | Alerta y énfasis puntual (estados «antes», riesgo) |
| **Papel** | `#F7F3EA` | Fondo claro |
| **Piedra** | `#5C6B7A` | Texto secundario |
| **Niebla** | `#DCE3EA` | Líneas y bordes |

Para **texto** sobre fondo claro se usa un turquesa más oscuro (`#0F8F85`) para cumplir contraste. Los tokens están en `tokens.css` y `paleta.json`.

## 5. Tipografía

- **Títulos y cifras:** Sora (700–800), tracking ligeramente cerrado.
- **Texto:** Inter (400–600).
- Respaldo del sistema: Segoe UI, Arial.

## 6. Composición de presentaciones

1. **Portada oscura** con el patrón yupana y el logo horizontal; título grande, lema de una o dos líneas.
2. **Láminas claras** (papel) para explicar; **láminas oscuras** para las cifras clave y el cierre. Alternar da ritmo.
3. **Una idea por lámina.** Títulos que afirman («Cuando llega el atraso, la oportunidad de ayudar ya pasó»), no rótulos («Problema»).
4. **Cifras grandes en maíz** sobre fondo oscuro, con su etiqueta y la salvedad «sobre datos sintéticos propios».
5. **Personas antes que pantallas:** historia de antes y después, y recién después el producto.
6. **Maquetas rotuladas** «MAQUETA ILUSTRATIVA · DATOS FICTICIOS». Nunca presentar una maqueta como prototipo.
7. **Franja superior** de tres colores (maíz, turquesa, tinta) en todas las láminas y fichas.
8. **Movimiento con propósito:** en la versión HTML y en video, entradas suaves que revelan la idea en orden; nada decorativo que distraiga.
9. **Pie de honestidad** en cada lámina: lo ilustrativo y lo supuesto están marcados.

## 7. Dónde se aplica hoy

- Decks de los cuatro retos: `retos/<ID>/presentacion/deck.pdf` y `deck.html` (esta última se navega con las flechas y tiene animaciones). Se regeneran con `python scripts/presentacion/armar.py`.
- Fichas de una página: `retos/<ID>/entrega/ficha-1-pagina.pdf`. Se regeneran con `python scripts/entrega/ficha_pdf.py`.
- Videos: ver `docs/plan-entrega-25-11.md` (tareas de video con HyperFrames).

## 8. Reglas de uso

- Todo material nuevo del equipo parte de estos tokens y activos; no se improvisan colores ni logos.
- La identidad no sustituye la honestidad: ningún recurso visual debe sugerir un resultado que no se ha medido.
- No se usa la marca de Caja Trujillo ni de ninguna otra organización como si fuera nuestra; los materiales del equipo llevan la marca de Yupana Labs.
