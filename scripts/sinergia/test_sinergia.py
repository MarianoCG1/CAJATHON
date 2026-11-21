import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest

import sinergia as s

NIV = {
    "A": {"backend": 5, "ux": 0},
    "B": {"backend": 0, "ux": 5},
    "C": {"backend": 5, "ux": 0},
    "D": {"backend": 0, "ux": 5},
}
DES = {"paquetes": [["api", "backend", 4], ["ui", "ux", 4]]}


def test_cobertura_pareja_complementaria_es_total():
    assert s.cobertura(("A", "B"), DES, NIV) == pytest.approx(1.0)


def test_cobertura_solo_es_la_mitad():
    assert s.cobertura(("A",), DES, NIV) == pytest.approx(0.5)


def test_sinergia_pareja_complementaria_vs_redundante():
    assert s.sinergia(("A", "B"), DES, NIV) == pytest.approx(0.5)
    assert s.sinergia(("A", "C"), DES, NIV) == pytest.approx(0.0)


def test_puntaje_prefiere_complementarios():
    assert s.puntaje(("A", "B"), DES, NIV) > s.puntaje(("A", "C"), DES, NIV)
    assert s.puntaje(("A", "B"), DES, NIV) == pytest.approx(100.0)


def test_brechas_detecta_habilidad_sin_cubrir():
    g = s.brechas(("A", "C"), DES, NIV)
    assert [x[1] for x in g] == ["ux"]


def test_carga_asigna_a_quien_mas_sabe():
    c = s.carga_por_persona(("A", "B"), DES, NIV)
    assert c == {"A": 4.0, "B": 4.0}


def test_asignacion_respeta_carga_y_rotacion():
    desafios = {f"X{i}": DES for i in range(4)}
    plan, total, _ = s.asignar(NIV, desafios, max_uso_pareja=2)
    cuenta = {n: sum(n in p for p in plan.values()) for n in NIV}
    assert set(cuenta.values()) == {2}
    usos = {}
    for p in plan.values():
        usos[p] = usos.get(p, 0) + 1
    assert max(usos.values()) <= 2
    assert total > 0


def test_datos_reales_son_consistentes():
    equipo, niveles, desafios = s.cargar()
    assert len(niveles) == 4
    assert len(desafios) == 8
    for n, nv in niveles.items():
        assert set(nv) == set(equipo["habilidades"]), n
        assert all(0 <= v <= 5 for v in nv.values())


def test_asignacion_real_equilibrada():
    _, niveles, desafios = s.cargar()
    plan, _, _ = s.asignar(niveles, desafios)
    for n in niveles:
        assert sum(n in p for p in plan.values()) == 4
    assert len(set(plan.values())) >= 4


def test_normalizar_invierte_y_maneja_empates():
    n = s._normalizar({"a": 1.0, "b": 3.0}, invertir=True)
    assert n == {"a": 1.0, "b": 0.0}
    assert s._normalizar({"a": 2.0, "b": 2.0}, invertir=False) == {"a": 0.5, "b": 0.5}


def test_prioridad_cubre_todos_y_los_pesos_suman_uno():
    _, niveles, desafios = s.cargar()
    filas = s.prioridad(niveles, desafios, s.cargar_valoracion())
    assert sorted(f["id"] for f in filas) == sorted(desafios)
    assert [f["rango_prom"] for f in filas] == sorted(f["rango_prom"] for f in filas)
    for pesos in s.PESOS.values():
        assert sum(pesos.values()) == pytest.approx(1.0)


def test_prioridad_responde_a_la_valoracion():
    _, niveles, desafios = s.cargar()
    val = s.cargar_valoracion()
    antes = {f["id"]: f for f in s.prioridad(niveles, desafios, val)}
    assert antes["COM-02"]["rangos"]["negocio"] > 1
    sube = {d: {"impacto": 1, "medibilidad": 1, "competencia": 5} for d in val}
    sube["COM-02"] = {"impacto": 5, "medibilidad": 5, "competencia": 1}
    despues = {f["id"]: f for f in s.prioridad(niveles, desafios, sube)}
    # La valoración solo mueve el rango de negocio; el del equipo depende únicamente de los datos del equipo.
    assert despues["COM-02"]["rangos"]["negocio"] == 1
    assert despues["COM-02"]["rangos"]["equipo"] == antes["COM-02"]["rangos"]["equipo"]
