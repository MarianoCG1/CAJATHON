import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generar_borradores as g


def test_genera_un_borrador_por_desafio_con_las_8_secciones(tmp_path):
    creados = g.generar(tmp_path)
    assert len(creados) == 8
    for ruta in creados:
        texto = ruta.read_text(encoding="utf-8")
        for seccion in g.SECCIONES:
            assert f"## {seccion}" in texto, (ruta.name, seccion)
        assert "[POR CONFIRMAR" in texto
        assert "Anexo B. Preguntas para el owner" in texto


def test_no_inventa_cifras_de_impacto(tmp_path):
    for ruta in g.generar(tmp_path):
        assert "[POR COMPLETAR cuando exista la línea base; no inventar]" in ruta.read_text(encoding="utf-8")


def test_escribe_en_la_carpeta_de_cada_reto(tmp_path):
    creados = g.generar(tmp_path)
    for ruta in creados:
        assert ruta.name == "concepto.md" and ruta.parent.parent == tmp_path / "retos"
    assert (tmp_path / "retos" / "RIE-03" / "concepto.md").exists()


def test_la_prioridad_figura_en_el_encabezado(tmp_path):
    g.generar(tmp_path)
    assert "Prioridad **#1**" in (tmp_path / "retos" / "RIE-03" / "concepto.md").read_text(encoding="utf-8")


def test_no_sobrescribe_sin_forzar(tmp_path):
    g.generar(tmp_path)
    editado = tmp_path / "retos" / "RIE-03" / "concepto.md"
    editado.write_text("TRABAJO DEL EQUIPO", encoding="utf-8")
    assert g.generar(tmp_path) == []
    assert editado.read_text(encoding="utf-8") == "TRABAJO DEL EQUIPO"
    assert len(g.generar(tmp_path, forzar=True)) == 8
    assert "TRABAJO DEL EQUIPO" not in editado.read_text(encoding="utf-8")
