"""Tests de los ejercicios del módulo 1."""

import inspect

import pytest

import m1_ej1_saludo as ej1
import m1_ej2_operaciones as ej2
import m1_ej3_estilo as ej3


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_saludo_basico():
    assert ej1.saludar("Ada") == "Hola, Ada. ¡Te damos la bienvenida al curso!"


def test_ej1_limpia_espacios_y_mayusculas():
    esperado = "Hola, Ada Lovelace. ¡Te damos la bienvenida al curso!"
    assert ej1.saludar("  ada LOVELACE ") == esperado


@pytest.mark.parametrize("nombre", ["", "    "])
def test_ej1_nombre_vacio(nombre):
    assert ej1.saludar(nombre) == "Hola, Anónimo. ¡Te damos la bienvenida al curso!"


def test_ej1_main_pide_el_nombre_e_imprime(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda *args: "grace hopper")
    ej1.main()
    salida = capsys.readouterr().out
    assert "Hola, Grace Hopper. ¡Te damos la bienvenida al curso!" in salida


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_operaciones_basicas():
    assert ej2.sumar(7, 2) == 9
    assert ej2.restar(7, 2) == 5
    assert ej2.multiplicar(7, 2) == 14


def test_ej2_la_division_real_siempre_es_float():
    assert ej2.dividir(7, 2) == 3.5
    assert isinstance(ej2.dividir(8, 2), float)


def test_ej2_division_entera_y_resto():
    assert ej2.division_entera(7, 2) == 3
    assert ej2.resto(7, 2) == 1
    assert isinstance(ej2.division_entera(7, 2), int)


def test_ej2_potencia():
    assert ej2.potencia(7, 2) == 49
    assert ej2.potencia(2, 10) == 1024


def test_ej2_resumen():
    esperado = (
        "7 + 2 = 9 | 7 - 2 = 5 | 7 * 2 = 14 | 7 / 2 = 3.50 | "
        "7 // 2 = 3 | 7 % 2 = 1 | 7 ** 2 = 49"
    )
    assert ej2.resumen(7, 2) == esperado


def test_ej2_resumen_con_division_periodica():
    assert "10 / 3 = 3.33" in ej2.resumen(10, 3)


def test_ej2_main(monkeypatch, capsys):
    respuestas = iter(["10", "4"])
    monkeypatch.setattr("builtins.input", lambda *args: next(respuestas))
    ej2.main()
    salida = capsys.readouterr().out
    assert "10 + 4 = 14" in salida
    assert "10 / 4 = 2.50" in salida


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_la_funcion_se_llama_precio_final():
    assert hasattr(ej3, "precio_final"), "Renombra la función a precio_final"
    assert not hasattr(ej3, "PrecioFinal"), "Elimina el nombre antiguo PrecioFinal"


def test_ej3_parametros_con_nombres_descriptivos():
    parametros = list(inspect.signature(ej3.precio_final).parameters)
    assert parametros == ["precio", "iva", "descuento"]


def test_ej3_constante_iva_general():
    assert ej3.IVA_GENERAL == 21


def test_ej3_tiene_docstring():
    assert ej3.precio_final.__doc__, "Añade un docstring a la función"


def test_ej3_el_comportamiento_no_cambia():
    assert ej3.precio_final(100) == 121.0
    assert ej3.precio_final(100, iva=10) == 110.0
    assert ej3.precio_final(200, descuento=50) == 121.0
    assert ej3.precio_final(19.99, iva=4, descuento=10) == 18.71
