"""Tests de la práctica 3: paquete m3_validacion y programa de alta."""

from datetime import date
from pathlib import Path

import pytest

import m3_practica_registro as registro
import m3_validacion
from m3_validacion import fechas, numeros, texto

HOY = date(2026, 11, 23)
DATOS_VALIDOS = ("Ada Lovelace", "ada@ejemplo.com", "12345678Z", "1990-01-01")


# -------------------------------------------------------------------- texto.py
@pytest.mark.parametrize(
    "valor, esperado",
    [(None, True), ("", True), ("   ", True), ("\t\n", True), ("a", False), (" a ", False)],
)
def test_esta_vacio(valor, esperado):
    assert texto.esta_vacio(valor) is esperado


@pytest.mark.parametrize(
    "nombre, esperado",
    [
        ("ada lovelace", "Ada Lovelace"),
        ("  ada   LOVELACE ", "Ada Lovelace"),
        ("GRACE", "Grace"),
        ("maría del carmen", "María Del Carmen"),
        ("", ""),
    ],
)
def test_normalizar_nombre(nombre, esperado):
    assert texto.normalizar_nombre(nombre) == esperado


@pytest.mark.parametrize(
    "correo",
    ["ada@ejemplo.com", "ada.lovelace@correo.ejemplo.es", "a@b.c", "nombre+etiqueta@ejemplo.org"],
)
def test_es_email_valido(correo):
    assert texto.es_email(correo) is True


@pytest.mark.parametrize(
    "correo",
    [
        "",
        "ada",
        "ada@ejemplo",
        "@ejemplo.com",
        "ada@@ejemplo.com",
        "ada@ejem@plo.com",
        "ada lovelace@ejemplo.com",
        "ada@.com",
        "ada@ejemplo.",
        "ada.ejemplo.com",
    ],
)
def test_es_email_no_valido(correo):
    assert texto.es_email(correo) is False


@pytest.mark.parametrize("dni", ["12345678Z", "12345678z", " 12345678Z ", "00000000T", "99999999R"])
def test_es_dni_valido(dni):
    assert texto.es_dni(dni) is True


@pytest.mark.parametrize(
    "dni",
    ["12345678A", "1234567Z", "123456789Z", "12345678", "ABCDEFGHZ", "", "1234 5678Z", "Z12345678"],
)
def test_es_dni_no_valido(dni):
    assert texto.es_dni(dni) is False


@pytest.mark.parametrize(
    "telefono",
    ["612345678", "612 345 678", "61234 5678", "  712 345 678  ", "900000000", "987654321"],
)
def test_es_telefono_valido(telefono):
    assert texto.es_telefono(telefono) is True


@pytest.mark.parametrize(
    "telefono",
    ["512345678", "61234567", "6123456789", "612 34A 678", "", "abcdefghi"],
)
def test_es_telefono_no_valido(telefono):
    assert texto.es_telefono(telefono) is False


@pytest.mark.parametrize(
    "iban",
    ["ES9121000418450200051332", " ES91 2100 0418 4502 0005 1332 ", "es9121000418450200051332"],
)
def test_es_iban_valido(iban):
    assert texto.es_iban(iban) is True


@pytest.mark.parametrize(
    "iban",
    ["ES9121000418450200051333", "ES91210004184502000513", "FR9121000418450200051332", "ABCDEFGHIJKLMN"],
)
def test_es_iban_no_valido(iban):
    assert texto.es_iban(iban) is False


# ------------------------------------------------------------------ numeros.py
@pytest.mark.parametrize("valor", ["42", " 42 ", "-42", "+7", "0", "007"])
def test_es_entero_valido(valor):
    assert numeros.es_entero(valor) is True


@pytest.mark.parametrize("valor", ["", "  ", "4.2", "4,2", "abc", "-", "--4", "4 2", "1e3"])
def test_es_entero_no_valido(valor):
    assert numeros.es_entero(valor) is False


@pytest.mark.parametrize("valor", ["3.14", "3,14", "-0.5", "+2,50", "42", " 7.0 ", "0,0"])
def test_es_decimal_valido(valor):
    assert numeros.es_decimal(valor) is True


@pytest.mark.parametrize(
    "valor", ["", "abc", "3.", ".5", "1.2.3", "1,2,3", "3.-5", "1.5e3", "-", ".", "3. 5"]
)
def test_es_decimal_no_valido(valor):
    assert numeros.es_decimal(valor) is False


def test_a_decimal():
    assert numeros.a_decimal("3.5") == 3.5
    assert numeros.a_decimal("3,5") == 3.5
    assert numeros.a_decimal(" -2 ") == -2.0
    assert isinstance(numeros.a_decimal("4"), float)
    assert numeros.a_decimal("abc") is None
    assert numeros.a_decimal("abc", 0.0) == 0.0
    assert numeros.a_decimal("", por_defecto=-1) == -1


@pytest.mark.parametrize(
    "valor, minimo, maximo, esperado",
    [
        (5, 1, 10, True),
        (1, 1, 10, True),
        (10, 1, 10, True),
        (0, 1, 10, False),
        (11, 1, 10, False),
        (5, None, None, True),
        (5, 6, None, False),
        (5, None, 4, False),
        (-3, None, 0, True),
        (0, 0, 0, True),
        (2.5, 2.5, 3, True),
    ],
)
def test_en_rango(valor, minimo, maximo, esperado):
    assert numeros.en_rango(valor, minimo, maximo) is esperado


def test_en_rango_limite_cero_no_es_none():
    assert numeros.en_rango(-1, minimo=0) is False
    assert numeros.en_rango(1, maximo=0) is False


# ------------------------------------------------------------------- fechas.py
def test_es_fecha_entregada():
    assert fechas.es_fecha("2026-02-28") is True
    assert fechas.es_fecha("2026-02-30") is False
    assert fechas.es_fecha("28/02/2026") is False


@pytest.mark.parametrize(
    "nacimiento, hoy, esperado",
    [
        ("2000-06-15", date(2026, 6, 14), 25),
        ("2000-06-15", date(2026, 6, 15), 26),
        ("2000-06-15", date(2026, 6, 16), 26),
        ("2000-12-31", date(2026, 1, 1), 25),
        ("2000-01-01", date(2026, 12, 31), 26),
        ("2026-11-23", date(2026, 11, 23), 0),
        ("2004-02-29", date(2026, 2, 28), 21),
        ("2004-02-29", date(2026, 3, 1), 22),
        (" 1990-01-01 ", date(2026, 11, 23), 36),
    ],
)
def test_edad(nacimiento, hoy, esperado):
    assert fechas.edad(nacimiento, hoy) == esperado


def test_edad_usa_la_fecha_actual_por_defecto():
    hoy = date.today()
    nacimiento = date(hoy.year - 30, 1, 1).isoformat()
    assert fechas.edad(nacimiento) == 30


@pytest.mark.parametrize(
    "nacimiento, esperado",
    [("2008-11-23", True), ("2008-11-24", False), ("1990-01-01", True), ("2020-05-05", False)],
)
def test_es_mayor_de_edad(nacimiento, esperado):
    assert fechas.es_mayor_de_edad(nacimiento, HOY) is esperado


def test_es_mayor_de_edad_usa_la_constante(monkeypatch):
    monkeypatch.setattr(fechas, "MAYORIA_DE_EDAD", 21)
    assert fechas.es_mayor_de_edad("2008-01-01", HOY) is False
    assert fechas.es_mayor_de_edad("2005-01-01", HOY) is True


# ----------------------------------------------------------------- __init__.py
FUNCIONES = [
    "a_decimal",
    "edad",
    "en_rango",
    "es_decimal",
    "es_dni",
    "es_email",
    "es_entero",
    "es_fecha",
    "es_iban",
    "es_mayor_de_edad",
    "es_telefono",
    "esta_vacio",
    "normalizar_nombre",
]


@pytest.mark.parametrize("nombre", FUNCIONES)
def test_paquete_reexporta(nombre):
    assert hasattr(m3_validacion, nombre), f"Falta reexportar {nombre} en __init__.py"
    assert callable(getattr(m3_validacion, nombre))


def test_paquete_all():
    assert sorted(m3_validacion.__all__) == FUNCIONES


def test_paquete_version():
    assert m3_validacion.__version__ == "1.0.0"


def test_paquete_reexporta_las_mismas_funciones():
    assert m3_validacion.es_dni is texto.es_dni
    assert m3_validacion.en_rango is numeros.en_rango
    assert m3_validacion.edad is fechas.edad


# ------------------------------------------------------ m3_practica_registro.py
def test_validar_registro_correcto():
    assert registro.validar_registro(*DATOS_VALIDOS, hoy=HOY) == []
    assert registro.validar_registro(*DATOS_VALIDOS) == []


@pytest.mark.parametrize(
    "posicion, valor, mensaje",
    [
        (0, "   ", "El nombre es obligatorio."),
        (1, "ada@ejemplo", "El correo no es válido."),
        (2, "12345678A", "El DNI no es válido."),
        (3, "01/01/1990", "La fecha de nacimiento no es válida."),
        (3, "2015-01-01", "Hay que ser mayor de edad."),
    ],
)
def test_validar_registro_un_error(posicion, valor, mensaje):
    datos = list(DATOS_VALIDOS)
    datos[posicion] = valor
    assert registro.validar_registro(*datos, hoy=HOY) == [mensaje]


def test_validar_registro_todos_los_errores_en_orden():
    assert registro.validar_registro("", "x", "y", "z", hoy=HOY) == [
        "El nombre es obligatorio.",
        "El correo no es válido.",
        "El DNI no es válido.",
        "La fecha de nacimiento no es válida.",
    ]


def test_validar_registro_respeta_hoy():
    datos = ("Ada", "ada@ejemplo.com", "12345678Z", "2008-11-24")
    assert registro.validar_registro(*datos, hoy=date(2026, 11, 23)) == [
        "Hay que ser mayor de edad."
    ]
    assert registro.validar_registro(*datos, hoy=date(2026, 11, 24)) == []


def test_validar_registro_telefono_e_iban():
    assert registro.validar_registro(
        "Ada",
        "ada@ejemplo.com",
        "12345678Z",
        "1990-01-01",
        hoy=HOY,
        telefono="612 345 678",
        iban="ES9121000418450200051332",
    ) == []

    assert registro.validar_registro(
        "Ada",
        "ada@ejemplo.com",
        "12345678Z",
        "1990-01-01",
        hoy=HOY,
        telefono="512345678",
        iban="ES9121000418450200051333",
    ) == ["El teléfono no es válido.", "El IBAN no es válido."]


def test_crear_ficha():
    ficha = registro.crear_ficha(" ada LOVELACE", "Ada@Ejemplo.com ", " 12345678z", " 1990-01-01 ")
    assert ficha == {
        "nombre": "Ada Lovelace",
        "email": "ada@ejemplo.com",
        "dni": "12345678Z",
        "nacimiento": "1990-01-01",
    }


def test_crear_ficha_con_telefono_e_iban():
    ficha = registro.crear_ficha(
        "Ada",
        "ada@ejemplo.com",
        "12345678z",
        "1990-01-01",
        telefono="612 345 678",
        iban=" es91 2100 0418 4502 0005 1332 ",
    )
    assert ficha["telefono"] == "612345678"
    assert ficha["iban"] == "ES9121000418450200051332"


def test_registro_usa_el_paquete():
    codigo = Path(registro.__file__).read_text(encoding="utf-8")
    assert "m3_validacion" in codigo, "El programa tiene que importar el paquete m3_validacion"
    assert "LETRAS_DNI" not in codigo and "% 23" not in codigo, (
        "La validación del DNI vive en el paquete, no en el programa"
    )


def _ejecutar_main(monkeypatch, capsys, respuestas):
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _="": next(entradas))
    registro.main()
    return capsys.readouterr().out


def test_main_alta_correcta(monkeypatch, capsys):
    salida = _ejecutar_main(
        monkeypatch, capsys, ["  ada LOVELACE", "Ada@Ejemplo.com", "12345678z", "1990-01-01"]
    )
    assert "Alta correcta:" in salida
    assert "nombre: Ada Lovelace" in salida
    assert "email: ada@ejemplo.com" in salida
    assert "dni: 12345678Z" in salida
    assert "nacimiento: 1990-01-01" in salida
    assert "No se puede completar" not in salida


def test_main_con_errores(monkeypatch, capsys):
    salida = _ejecutar_main(monkeypatch, capsys, ["", "ada@ejemplo", "12345678Z", "1990-01-01"])
    assert "No se puede completar el alta:" in salida
    assert " - El nombre es obligatorio." in salida
    assert " - El correo no es válido." in salida
    assert "DNI" not in salida.split("alta:")[1]
    assert "Alta correcta" not in salida


def test_main_vuelve_a_pedir_solo_datos_errores(monkeypatch, capsys):
    salida = _ejecutar_main(
        monkeypatch,
        capsys,
        ["", "ada@ejemplo", "12345678Z", "1990-01-01", "Ada Lovelace", "ada@ejemplo.com"],
    )
    assert "Alta correcta:" in salida
    assert "nombre: Ada Lovelace" in salida
    assert "email: ada@ejemplo.com" in salida
