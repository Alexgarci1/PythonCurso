"""Tests de la práctica 1: conversor de unidades."""

import pytest

import m1_practica_conversor as conversor


def test_constantes():
    assert conversor.KM_POR_MILLA == 1.609344
    assert conversor.KG_POR_LIBRA == 0.45359237


@pytest.mark.parametrize(
    "celsius, fahrenheit",
    [(0, 32), (100, 212), (-40, -40), (37, 98.6)],
)
def test_temperaturas(celsius, fahrenheit):
    assert conversor.celsius_a_fahrenheit(celsius) == pytest.approx(fahrenheit)
    assert conversor.fahrenheit_a_celsius(fahrenheit) == pytest.approx(celsius)


def test_distancias():
    assert conversor.km_a_millas(1.609344) == pytest.approx(1)
    assert conversor.millas_a_km(26.2) == pytest.approx(42.1648128)


def test_pesos():
    assert conversor.kg_a_libras(0.45359237) == pytest.approx(1)
    assert conversor.libras_a_kg(150) == pytest.approx(68.0388555)


def test_las_conversiones_devuelven_float():
    assert isinstance(conversor.celsius_a_fahrenheit(10), float)
    assert isinstance(conversor.millas_a_km(10), float)
    assert isinstance(conversor.libras_a_kg(10), float)


def test_ida_y_vuelta():
    assert conversor.millas_a_km(conversor.km_a_millas(42)) == pytest.approx(42)
    assert conversor.libras_a_kg(conversor.kg_a_libras(80)) == pytest.approx(80)


def test_formatear():
    assert conversor.formatear(100, "°C", 212.0, "°F") == "100.00 °C = 212.00 °F"
    assert conversor.formatear(5, "km", 3.106855, "mi") == "5.00 km = 3.11 mi"


@pytest.mark.parametrize(
    "opcion, valor, esperado",
    [
        ("1", "100", "100.00 °C = 212.00 °F"),
        ("2", "212", "212.00 °F = 100.00 °C"),
        ("3", "10", "10.00 km = 6.21 mi"),
        ("4", "10", "10.00 mi = 16.09 km"),
        ("5", "10", "10.00 kg = 22.05 lb"),
        ("6", "10", "10.00 lb = 4.54 kg"),
    ],
)
def test_main_convierte_segun_la_opcion(monkeypatch, capsys, opcion, valor, esperado):
    respuestas = iter([opcion, valor])
    monkeypatch.setattr("builtins.input", lambda *args: next(respuestas))
    conversor.main()
    assert esperado in capsys.readouterr().out


def test_main_opcion_no_valida(monkeypatch, capsys):
    respuestas = iter(["9", "10"])
    monkeypatch.setattr("builtins.input", lambda *args: next(respuestas))
    conversor.main()
    assert "Opción no válida" in capsys.readouterr().out
