"""Tests de los ejercicios del módulo 2."""

import pytest

import m2_ej1_tipos as ej1
import m2_ej2_operadores as ej2
import m2_ej3_condicionales as ej3
import m2_ej4_bucles as ej4


# ---------------------------------------------------------------- Ejercicio 1
@pytest.mark.parametrize(
    "valor, esperado",
    [
        (42, "entero"),
        (3.5, "decimal"),
        (True, "booleano"),
        (False, "booleano"),
        ("hola", "texto"),
        (None, "nulo"),
        ([1, 2], "otro"),
    ],
)
def test_ej1_nombre_del_tipo(valor, esperado):
    assert ej1.nombre_del_tipo(valor) == esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [("42", 42), ("  -42 ", -42), ("+7", 7), ("0", 0), ("007", 7)],
)
def test_ej1_a_entero_valido(texto, esperado):
    assert ej1.a_entero(texto) == esperado


@pytest.mark.parametrize("texto", ["3.5", "abc", "", "   ", "-", "4 2", "--3", "1e3"])
def test_ej1_a_entero_no_valido(texto):
    assert ej1.a_entero(texto) is None


def test_ej1_casi_iguales():
    assert ej1.casi_iguales(0.1 + 0.2, 0.3)
    assert not ej1.casi_iguales(0.1, 0.2)
    assert ej1.casi_iguales(1.0, 1.05, tolerancia=0.1)
    assert not ej1.casi_iguales(1.0, 1.2, tolerancia=0.1)
    assert ej1.casi_iguales(-1.0, -1.0)


def test_ej1_media():
    assert ej1.media(5, 6, 8) == 6.33
    assert ej1.media(1, 2, 3) == 2.0
    assert ej1.media(0, 0, 1) == 0.33
    assert isinstance(ej1.media(3, 3, 3), float)


@pytest.mark.parametrize(
    "importe, esperado",
    [(12.34, (12, 34)), (0.07, (0, 7)), (19.99, (19, 99)), (5, (5, 0)), (1.1, (1, 10))],
)
def test_ej1_partir_euros(importe, esperado):
    assert ej1.partir_euros(importe) == esperado


# ---------------------------------------------------------------- Ejercicio 2
@pytest.mark.parametrize(
    "anio, esperado",
    [(2024, True), (2023, False), (1900, False), (2000, True), (2100, False), (2400, True)],
)
def test_ej2_es_bisiesto(anio, esperado):
    assert ej2.es_bisiesto(anio) is esperado


@pytest.mark.parametrize(
    "segundos, esperado",
    [(0, "00:00:00"), (59, "00:00:59"), (60, "00:01:00"), (3725, "01:02:05"), (86399, "23:59:59")],
)
def test_ej2_segundos_a_hms(segundos, esperado):
    assert ej2.segundos_a_hms(segundos) == esperado


@pytest.mark.parametrize(
    "nombre, esperado",
    [("Ada", "Ada"), ("  Ada ", "Ada"), ("", "Anónimo"), ("   ", "Anónimo"), (None, "Anónimo")],
)
def test_ej2_nombre_o_anonimo(nombre, esperado):
    assert ej2.nombre_o_anonimo(nombre) == esperado


def test_ej2_en_rango():
    assert ej2.en_rango(5, 1, 10) is True
    assert ej2.en_rango(1, 1, 10) is True
    assert ej2.en_rango(10, 1, 10) is True
    assert ej2.en_rango(0, 1, 10) is False
    assert ej2.en_rango(10.01, 1, 10) is False


def test_ej2_es_par():
    assert ej2.es_par(0) is True
    assert ej2.es_par(4) is True
    assert ej2.es_par(7) is False
    assert ej2.es_par(-4) is True
    assert ej2.es_par(-3) is False


def test_ej2_reparto():
    assert ej2.reparto(17, 5) == (3, 2)
    assert ej2.reparto(20, 4) == (5, 0)
    assert ej2.reparto(3, 5) == (0, 3)


# ---------------------------------------------------------------- Ejercicio 3
@pytest.mark.parametrize(
    "nota, esperado",
    [
        (0, "Suspenso"),
        (4.99, "Suspenso"),
        (5, "Aprobado"),
        (6.99, "Aprobado"),
        (7, "Notable"),
        (8.99, "Notable"),
        (9, "Sobresaliente"),
        (10, "Sobresaliente"),
        (-0.1, "Nota no válida"),
        (10.1, "Nota no válida"),
    ],
)
def test_ej3_calificacion(nota, esperado):
    assert ej3.calificacion(nota) == esperado


@pytest.mark.parametrize(
    "edad, festivo, esperado",
    [
        (0, False, 0),
        (3, True, 0),
        (4, False, 5),
        (12, False, 5),
        (12, True, 7),
        (13, False, 9),
        (64, True, 11),
        (65, False, 6),
        (90, True, 8),
    ],
)
def test_ej3_precio_entrada(edad, festivo, esperado):
    assert ej3.precio_entrada(edad, festivo) == esperado


def test_ej3_precio_entrada_no_festivo_por_defecto():
    assert ej3.precio_entrada(30) == 9


@pytest.mark.parametrize(
    "codigo, esperado",
    [
        (200, "Correcto"),
        (201, "Creado"),
        (301, "Redirección"),
        (302, "Redirección"),
        (400, "Petición incorrecta"),
        (401, "Sin autorización"),
        (403, "Sin autorización"),
        (404, "No encontrado"),
        (500, "Error del servidor"),
        (503, "Error del servidor"),
        (599, "Error del servidor"),
        (600, "Desconocido"),
        (418, "Desconocido"),
    ],
)
def test_ej3_describir_http(codigo, esperado):
    assert ej3.describir_http(codigo) == esperado


@pytest.mark.parametrize(
    "numeros, esperado",
    [((3, 9, 5), 9), ((9, 3, 5), 9), ((3, 5, 9), 9), ((-1, -5, -3), -1), ((2, 2, 2), 2)],
)
def test_ej3_mayor_de_tres(numeros, esperado):
    assert ej3.mayor_de_tres(*numeros) == esperado


@pytest.mark.parametrize(
    "lados, esperado",
    [
        ((3, 3, 3), "equilátero"),
        ((3, 3, 5), "isósceles"),
        ((5, 3, 3), "isósceles"),
        ((3, 4, 5), "escaleno"),
        ((1, 2, 3), "no es un triángulo"),
        ((1, 1, 5), "no es un triángulo"),
        ((0, 4, 5), "no es un triángulo"),
        ((-3, 4, 5), "no es un triángulo"),
    ],
)
def test_ej3_tipo_triangulo(lados, esperado):
    assert ej3.tipo_triangulo(*lados) == esperado


# ---------------------------------------------------------------- Ejercicio 4
@pytest.mark.parametrize("n, esperado", [(0, 1), (1, 1), (5, 120), (10, 3628800)])
def test_ej4_factorial(n, esperado):
    assert ej4.factorial(n) == esperado


def test_ej4_factorial_no_desborda():
    assert ej4.factorial(25) == 15511210043330985984000000


def test_ej4_es_primo():
    primos = [n for n in range(-3, 50) if ej4.es_primo(n)]
    assert primos == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert ej4.es_primo(7919) is True
    assert ej4.es_primo(7917) is False


@pytest.mark.parametrize(
    "texto, esperado", [("Python", "nohtyP"), ("", ""), ("a", "a"), ("Atlético", "ocitéltA")]
)
def test_ej4_invertir(texto, esperado):
    assert ej4.invertir(texto) == esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [("Programación", 5), ("PYTHON", 1), ("", 0), ("xyz", 0), ("Murciélago", 5), ("pingüino", 4)],
)
def test_ej4_contar_vocales(texto, esperado):
    assert ej4.contar_vocales(texto) == esperado


@pytest.mark.parametrize("numero, esperado", [(1234, 10), (0, 0), (-905, 14), (7, 7), (99999, 45)])
def test_ej4_suma_digitos(numero, esperado):
    assert ej4.suma_digitos(numero) == esperado


def test_ej4_fizzbuzz():
    assert ej4.fizzbuzz(1) == "1"
    assert ej4.fizzbuzz(5) == "1 2 Fizz 4 Buzz"
    assert ej4.fizzbuzz(15) == (
        "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz"
    )


def test_ej4_tabla_multiplicar():
    lineas = ej4.tabla_multiplicar(7).split("\n")
    assert len(lineas) == 10
    assert lineas[0] == "7 x  1 =   7"
    assert lineas[2] == "7 x  3 =  21"
    assert lineas[9] == "7 x 10 =  70"
    assert ej4.tabla_multiplicar(12).split("\n")[9] == "12 x 10 = 120"


@pytest.mark.parametrize("a, b, esperado", [(4, 6, 12), (3, 5, 15), (7, 7, 7), (2, 8, 8), (1, 9, 9)])
def test_ej4_primer_multiplo_comun(a, b, esperado):
    assert ej4.primer_multiplo_comun(a, b) == esperado
