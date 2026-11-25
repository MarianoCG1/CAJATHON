# Video de Yupana Labs

Videos del equipo, hechos con [HyperFrames](https://hyperframes.heygen.com) (HTML que se renderiza a video fotograma a fotograma). Usan la identidad de `identidad/README.md`: tinta, maíz y turquesa, la marca de yupana que se llena columna por columna, y el lema «Contar bien para decidir mejor». En video se usa **Outfit** (incluida en HyperFrames) para los títulos, por equivalencia con Sora, y Inter para el texto.

| Proyecto | Qué es | Estado |
|---|---|---|
| `video/marca/` | Sting de marca de 8 s: la yupana se llena, aparece el nombre y el lema | Hecho |
| `video/rie-03/` | Explicativo animado de RIE-03: 44 s, 7 escenas (gancho, Rosa, la cola, el caso, decide la persona, lo que medimos, cierre), sin narración ni música | Hecho |

## Cómo se genera

Cada proyecto tiene su `generar.py` (o `generar_index.py`) que escribe el HTML; el contenido sale de `retos/<ID>/presentacion/contenido.json`. Ejemplo con RIE-03:

```powershell
python video/rie-03/generar.py
cd video/rie-03
npx --yes hyperframes@0.9.94 check
npx --yes hyperframes@0.9.94 render --output out/rie-03-explicativo.mp4
```

Y con el sting de marca:

```powershell
python video/marca/generar_index.py                                   # regenera el HTML desde el generador
cd video/marca
npx --yes hyperframes@0.9.94 check                                    # verificación (lint, runtime, layout)
npx --yes hyperframes@0.9.94 snapshot --at 0.6,1.6,2.3,3.4,4.2,6      # fotogramas para revisar
npx --yes hyperframes@0.9.94 render --output out/yupana-labs-sting.mp4
```

Los MP4 (`out/`) no se versionan; se regeneran con el comando de render. La versión de HyperFrames está fijada (0.9.94) para que el render sea reproducible.

## Reglas

- Todo video muestra solo lo que está en el deck del reto: nada de cifras nuevas, y las medidas dicen «sobre datos sintéticos propios». Las pantallas son maquetas con datos ficticios.
- No se suben los videos a servicios externos sin autorización de Mariano.
- Este material es de comunicación del equipo y está declarado como preexistente en `docs/preexistente.md`.
