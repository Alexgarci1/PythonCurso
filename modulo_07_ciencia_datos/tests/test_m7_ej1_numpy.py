"""Tests del ejercicio 1 del Módulo 7: NumPy."""

import inspect

import numpy as np
import pytest

import m7_ej1_numpy as ej


def test_crear_rango():
    resultado = ej.crear_rango(0, 1, 0.25)
    assert isinstance(resultado, np.ndarray)
    assert resultado.tolist() == [0.0, 0.25, 0.5, 0.75]
    assert ej.crear_rango(10, 20, 5).tolist() == [10, 15]


def test_estadisticas():
    resultado = ej.estadisticas([2, 4, 4, 4, 5, 5, 7, 9])
    assert resultado == {"media": 5.0, "mediana": 4.5, "desviacion": 2.0, "minimo": 2.0, "maximo": 9.0}
    assert all(type(valor) is float for valor in resultado.values())


def test_estadisticas_admite_arrays():
    assert ej.estadisticas(np.array([1.0, 3.0]))["media"] == 2.0


def test_aplicar_iva():
    resultado = ej.aplicar_iva([100, 19.9])
    assert isinstance(resultado, np.ndarray)
    assert resultado.tolist() == [121.0, 24.08]
    assert ej.aplicar_iva([100, 50], tipo=0.10).tolist() == [110.0, 55.0]


@pytest.mark.parametrize("valores, esperado", [
    ([10, 20, 30], [0.0, 0.5, 1.0]),
    ([5, 1, 3], [1.0, 0.0, 0.5]),
    ([-2, 0, 2], [0.0, 0.5, 1.0]),
    ([7, 7, 7], [0.0, 0.0, 0.0]),
])
def test_normalizar(valores, esperado):
    assert ej.normalizar(valores).tolist() == pytest.approx(esperado)


def test_mayores_que_la_media():
    assert ej.mayores_que_la_media([1, 5, 2, 8]).tolist() == [5, 8]
    assert ej.mayores_que_la_media([3, 3, 3]).tolist() == []


def test_reemplazar_negativos():
    original = np.array([3, -1, 4, -5])
    assert ej.reemplazar_negativos(original).tolist() == [3, 0, 4, 0]
    assert ej.reemplazar_negativos(original, sustituto=9).tolist() == [3, 9, 4, 9]
    assert original.tolist() == [3, -1, 4, -5], "No modifiques el array original"


def test_totales():
    filas, columnas = ej.totales([[1, 2, 3], [4, 5, 6]])
    assert filas.tolist() == [6, 15]
    assert columnas.tolist() == [5, 7, 9]


def test_importes():
    assert ej.importes([2, 10], [950.0, 19.9]).tolist() == pytest.approx([1900.0, 199.0])
    with pytest.raises(ValueError):
        ej.importes([1, 2, 3], [1.0, 2.0])


def test_media_movil():
    assert ej.media_movil([1, 2, 3, 4, 5], 3).tolist() == pytest.approx([2.0, 3.0, 4.0])
    assert ej.media_movil([10, 20, 30, 40], 2).tolist() == pytest.approx([15.0, 25.0, 35.0])
    assert len(ej.media_movil(range(12), 4)) == 9


@pytest.mark.parametrize("nombre", [
    "estadisticas", "aplicar_iva", "normalizar", "mayores_que_la_media",
    "reemplazar_negativos", "totales", "importes",
])
def test_sin_bucles(nombre):
    codigo = inspect.getsource(getattr(ej, nombre))
    cuerpo = codigo.split('"""')[-1]
    assert "for " not in cuerpo and "while " not in cuerpo, (
        f"{nombre} se resuelve con operaciones sobre el array completo, sin bucles"
    )
