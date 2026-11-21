import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

import generar_boveda as gb

RAIZ = gb.RAIZ


@pytest.fixture()
def copia(tmp_path):
    """Proyecto mínimo en tmp: solo lo que lee el generador, para no tocar la bóveda real."""
    import shutil
    shutil.copytree(RAIZ / "retos", tmp_path / "retos", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "sintetico"))
    return tmp_path


def test_genera_8_nodos_hub_y_tablero(copia):
    escritos = gb.generar(copia, hoy="2026-11-21")
    assert len(escritos) == 10
    assert len(list((copia / "boveda/Retos").glob("*.md"))) == 8
    assert (copia / "boveda/Tablero.md").exists()
    assert (copia / "boveda/00-HUB-Cajathon.md").exists()


def test_avance_refleja_los_archivos():
    rie03 = gb.avance("RIE-03")
    assert rie03["hechos"] == rie03["total"] == 6
    assert rie03["estado"] == "Listo para revisión cruzada"
    neg01 = gb.avance("NEG-01")
    assert neg01["pasos"]["borrador"] and not neg01["pasos"]["v1"]
    assert neg01["hechos"] == 1
    assert neg01["estado"] == "Borrador v0"


def test_cotejo_exige_panorama_con_su_cotejo():
    # NEG-01 no tiene panorama: el cotejo no puede darse por hecho
    assert gb.avance("NEG-01")["pasos"]["cotejo"] is False


def test_regenerar_conserva_las_notas_manuales(copia):
    gb.generar(copia, hoy="2026-11-21")
    nodo = copia / "boveda/Retos/RIE-03.md"
    nodo.write_text(nodo.read_text(encoding="utf-8") + "\nNOTA PERSONAL DE GLEM: revisar el umbral\n", encoding="utf-8")
    gb.generar(copia, hoy="2026-11-22")
    texto = nodo.read_text(encoding="utf-8")
    assert "NOTA PERSONAL DE GLEM" in texto
    assert "actualizado: 2026-11-22" in texto


def test_los_enlaces_a_documentos_apuntan_a_archivos_que_existen(copia):
    gb.generar(copia, hoy="2026-11-21")
    for nodo in (copia / "boveda/Retos").glob("*.md"):
        for destino in re.findall(r"\[\[([^\]|]+)\|", nodo.read_text(encoding="utf-8")):
            if destino.startswith("boveda/"):
                continue  # nodos hermanos: se comprueban abajo contra la bóveda real
            assert (copia / f"{destino}.md").exists() or (copia / destino).exists(), (nodo.name, destino)


def test_el_tablero_ordena_por_prioridad_y_suma(copia):
    gb.generar(copia, hoy="2026-11-21")
    t = (copia / "boveda/Tablero.md").read_text(encoding="utf-8")
    filas = [l for l in t.splitlines() if re.match(r"\| \d+ \|", l)]
    assert len(filas) == 8
    assert filas[0].startswith("| 1 |") and "RIE-03" in filas[0]
    assert "Avance global" in t


def test_los_wikilinks_del_hub_y_competencia_resuelven_en_la_boveda_real():
    gb.generar(RAIZ, hoy="2026-11-21")
    faltan = []
    for md in (RAIZ / "boveda").rglob("*.md"):
        for destino in re.findall(r"\[\[([^\]|#]+)", md.read_text(encoding="utf-8")):
            if not (RAIZ / f"{destino}.md").exists():
                faltan.append((md.name, destino))
    assert faltan == []
