"""Pruebas del territorio sintético de COM-01."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

_ruta = Path(__file__).with_name("generar.py")
_spec = importlib.util.spec_from_file_location("generar_com01", _ruta)
gen = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = gen
_spec.loader.exec_module(gen)


@pytest.fixture(scope="module")
def tablas():
    return gen.generar(gen.Config())


def test_reproducible(tablas):
    otra = gen.generar(gen.Config())
    for nombre, df in tablas.items():
        assert df.equals(otra[nombre])


def test_unidad_es_la_zona_sin_datos_personales(tablas):
    prohibidas = {"nombre", "dni", "telefono", "direccion", "sexo", "edad", "ruc", "email"}
    for df in tablas.values():
        assert df["zona_id"].is_unique
        assert not prohibidas & set(df.columns)


def test_conversion_media_calibrada(tablas):
    assert tablas["verdad"]["conversion_real"].mean() == pytest.approx(0.08, abs=0.002)


def test_historial_sesgado_hacia_la_cartera_actual(tablas):
    z, h = tablas["zonas"], tablas["historial"]
    assert np.corrcoef(z["clientes_actuales"], h["visitas"])[0, 1] > 0.8


def test_huecos_digitales_mayores_en_zona_rural(tablas):
    z = tablas["zonas"]
    hueco = z["presencia_digital"].isna().groupby(z["tipo"]).mean()
    assert hueco["rural"] > hueco["urbana"]


def test_historial_consistente(tablas):
    h = tablas["historial"]
    assert (h["clientes_nuevos"] <= h["visitas"]).all()


def test_escenario_invalido():
    with pytest.raises(ValueError):
        gen.generar(gen.Config(escenario="otro"))
