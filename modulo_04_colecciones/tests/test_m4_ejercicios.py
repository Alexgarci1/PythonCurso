"""Tests de los ejercicios del módulo 4."""

import ast
import copy
import inspect
import textwrap

import pytest

import m4_ej1_listas as ej1
import m4_ej2_diccionarios as ej2
import m4_ej3_conjuntos as ej3
import m4_ej4_comprensiones as ej4
import m4_ej5_cadenas as ej5
import m4_ej6_datos as ej6


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_extremos():
    assert ej1.extremos([4, 8, 15]) == (4, 15)
    assert ej1.extremos([7]) == (7, 7)
    assert ej1.extremos(["a", "b"]) == ("a", "b")
    assert ej1.extremos([]) == (None, None)


@pytest.mark.parametrize(
    "lista, posiciones, esperado",
    [
        ([1, 2, 3, 4, 5], 2, [3, 4, 5, 1, 2]),
        ([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),
        ([1, 2, 3], 4, [2, 3, 1]),
        ([1, 2, 3], 1, [2, 3, 1]),
        (["a"], 3, ["a"]),
        ([], 2, []),
    ],
)
def test_ej1_rotar(lista, posiciones, esperado):
    original = list(lista)
    assert ej1.rotar(lista, posiciones) == esperado
    assert lista == original


def test_ej1_rotar_por_defecto_y_lista_nueva():
    lista = [1, 2, 3]
    resultado = ej1.rotar(lista)
    assert resultado == [2, 3, 1]
    assert resultado is not lista
    assert ej1.rotar(lista, 0) is not lista


@pytest.mark.parametrize(
    "numeros, esperado",
    [
        ([4, 42, 15, 42], 15),
        ([1, 2], 1),
        ([3, 3, 2, 2, 1], 2),
        ([-5, -1, -3], -3),
        ([5, 5], None),
        ([7], None),
        ([], None),
    ],
)
def test_ej1_segundo_mayor(numeros, esperado):
    original = list(numeros)
    assert ej1.segundo_mayor(numeros) == esperado
    assert numeros == original


@pytest.mark.parametrize(
    "lista, tamano, esperado",
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2, 3], 5, [[1, 2, 3]]),
        ([1, 2, 3], 1, [[1], [2], [3]]),
        ([], 3, []),
    ],
)
def test_ej1_trocear(lista, tamano, esperado):
    assert ej1.trocear(lista, tamano) == esperado


def test_ej1_sin_duplicados():
    lista = [3, 1, 3, 2, 1]
    assert ej1.sin_duplicados(lista) == [3, 1, 2]
    assert lista == [3, 1, 3, 2, 1]
    assert ej1.sin_duplicados(["b", "a", "b"]) == ["b", "a"]
    assert ej1.sin_duplicados([]) == []
    assert ej1.sin_duplicados([1, 1, 1]) == [1]


@pytest.mark.parametrize(
    "ordenada, valor, esperado",
    [
        ([1, 3, 5], 4, [1, 3, 4, 5]),
        ([1, 3, 5], 0, [0, 1, 3, 5]),
        ([1, 3, 5], 9, [1, 3, 5, 9]),
        ([1, 3, 5], 3, [1, 3, 3, 5]),
        ([], 7, [7]),
    ],
)
def test_ej1_insertar_ordenado(ordenada, valor, esperado):
    original = list(ordenada)
    assert ej1.insertar_ordenado(ordenada, valor) == esperado
    assert ordenada == original, "No se puede modificar la lista recibida"


def test_ej1_crear_tablero():
    assert ej1.crear_tablero(2, 3) == [[0, 0, 0], [0, 0, 0]]
    assert ej1.crear_tablero(1, 2, "-") == [["-", "-"]]
    assert ej1.crear_tablero(0, 3) == []


def test_ej1_crear_tablero_filas_independientes():
    tablero = ej1.crear_tablero(3, 3)
    tablero[0][0] = "X"
    assert tablero == [["X", 0, 0], [0, 0, 0], [0, 0, 0]], (
        "Todas las filas son la misma lista: no multipliques la lista de filas"
    )


# ---------------------------------------------------------------- Ejercicio 2
ESTUDIANTES = {"Ada": [9, 10], "Linus": [5, 6, 8], "Grace": [10], "Alan": []}


def test_ej2_punto_medio():
    assert ej2.punto_medio((0, 0), (4, 2)) == (2.0, 1.0)
    assert ej2.punto_medio((1, 1), (2, 2)) == (1.5, 1.5)
    assert ej2.punto_medio((-2, 4), (2, -4)) == (0.0, 0.0)
    assert isinstance(ej2.punto_medio((0, 0), (1, 1)), tuple)


def test_ej2_contar_palabras():
    assert ej2.contar_palabras("El gato y el perro") == {"el": 2, "gato": 1, "y": 1, "perro": 1}
    assert ej2.contar_palabras("a  a   A") == {"a": 3}
    assert ej2.contar_palabras("") == {}
    assert list(ej2.contar_palabras("uno dos uno")) == ["uno", "dos"]


def test_ej2_invertir():
    original = {"a": 1, "b": 2}
    assert ej2.invertir(original) == {1: "a", 2: "b"}
    assert original == {"a": 1, "b": 2}
    assert ej2.invertir({}) == {}


def test_ej2_notas_medias():
    assert ej2.notas_medias(ESTUDIANTES) == {"Ada": 9.5, "Linus": 6.33, "Grace": 10.0, "Alan": 0.0}
    assert ej2.notas_medias({}) == {}
    assert ESTUDIANTES["Linus"] == [5, 6, 8]


def test_ej2_mejor_estudiante():
    assert ej2.mejor_estudiante(ESTUDIANTES) == "Grace"
    assert ej2.mejor_estudiante({"Ada": [9, 10], "Linus": [5, 6, 8]}) == "Ada"
    assert ej2.mejor_estudiante({"Ada": [7], "Linus": [7]}) == "Ada"
    assert ej2.mejor_estudiante({}) is None


def test_ej2_mejor_estudiante_reutiliza_notas_medias(monkeypatch):
    monkeypatch.setattr(ej2, "notas_medias", lambda estudiantes: {"Ada": 1.0, "Zoe": 9.0})
    assert ej2.mejor_estudiante({"Ada": [10], "Zoe": [0]}) == "Zoe"


def test_ej2_total_carrito():
    assert ej2.total_carrito([("teclado", 2, 45.0), ("raton", 1, 19.9)]) == 109.9
    assert ej2.total_carrito([("a", 3, 0.1)]) == 0.3
    assert ej2.total_carrito([]) == 0


def test_ej2_fusionar_inventarios():
    a = {"teclado": 5, "raton": 2}
    b = {"raton": 3, "monitor": 1}
    assert ej2.fusionar_inventarios(a, b) == {"teclado": 5, "raton": 5, "monitor": 1}
    assert a == {"teclado": 5, "raton": 2}, "No se puede modificar el primer inventario"
    assert b == {"raton": 3, "monitor": 1}
    assert ej2.fusionar_inventarios({}, {}) == {}
    assert ej2.fusionar_inventarios(a, {}) is not a


PEDIDO = {
    "id": 7,
    "cliente": {"nombre": "Ada", "direccion": {"ciudad": "Madrid", "cp": None}},
    "lineas": [1, 2],
}


@pytest.mark.parametrize(
    "ruta, por_defecto, esperado",
    [
        ("id", None, 7),
        ("cliente.nombre", None, "Ada"),
        ("cliente.direccion.ciudad", None, "Madrid"),
        ("cliente.direccion", None, {"ciudad": "Madrid", "cp": None}),
        ("cliente.direccion.cp", "x", None),
        ("cliente.telefono", None, None),
        ("cliente.telefono", "sin datos", "sin datos"),
        ("proveedor.nombre", 0, 0),
        ("id.algo", "x", "x"),
        ("lineas.0", "x", "x"),
    ],
)
def test_ej2_valor_anidado(ruta, por_defecto, esperado):
    assert ej2.valor_anidado(PEDIDO, ruta, por_defecto) == esperado


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_elementos_comunes():
    assert ej3.elementos_comunes([1, 2, 3, 4], [3, 4, 5, 6]) == [3, 4]
    assert ej3.elementos_comunes([4, 3, 3, 4], [4, 3]) == [3, 4]
    assert ej3.elementos_comunes(["b", "a"], ["a", "b", "c"]) == ["a", "b"]
    assert ej3.elementos_comunes([1, 2], [3]) == []
    assert ej3.elementos_comunes([], []) == []


def test_ej3_solo_en_una():
    assert ej3.solo_en_una([1, 2, 3], [3, 4]) == [1, 2, 4]
    assert ej3.solo_en_una([1, 2], [1, 2]) == []
    assert ej3.solo_en_una([], [2, 1, 1]) == [1, 2]


def test_ej3_tiene_duplicados():
    assert ej3.tiene_duplicados([1, 2, 1]) is True
    assert ej3.tiene_duplicados([1, 2, 3]) is False
    assert ej3.tiene_duplicados([]) is False
    assert ej3.tiene_duplicados(["a", "A"]) is False


def test_ej3_duplicados():
    assert ej3.duplicados([3, 1, 3, 2, 1, 3]) == [1, 3]
    assert ej3.duplicados([1, 2, 3]) == []
    assert ej3.duplicados(["b", "a", "b", "a"]) == ["a", "b"]
    assert ej3.duplicados([]) == []


@pytest.mark.parametrize(
    "frase, esperado",
    [
        ("The quick brown fox jumps over the lazy dog", True),
        ("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!", True),
        ("Jovencillo emponzoñado de whisky, qué figurota exhibe", True),
        ("Hola mundo", False),
        ("abcdefghijklmnopqrstuvwxy", False),
        ("", False),
    ],
)
def test_ej3_es_pangrama(frase, esperado):
    assert ej3.es_pangrama(frase) is esperado


def test_ej3_permisos_que_faltan():
    assert ej3.permisos_que_faltan(["leer", "escribir", "borrar"], ["leer", "admin"]) == [
        "borrar",
        "escribir",
    ]
    assert ej3.permisos_que_faltan(["leer"], ["leer", "escribir"]) == []
    assert ej3.permisos_que_faltan([], ["leer"]) == []
    assert ej3.permisos_que_faltan(["b", "a", "b"], []) == ["a", "b"]


def test_ej3_habilidades_compartidas():
    equipo = {
        "Ada": ["python", "sql", "git"],
        "Linus": ["c", "git", "python"],
        "Grace": ["cobol", "python", "git"],
    }
    assert ej3.habilidades_compartidas(equipo) == ["git", "python"]
    assert ej3.habilidades_compartidas({"Ada": ["sql", "python"]}) == ["python", "sql"]
    assert ej3.habilidades_compartidas({"Ada": ["sql"], "Linus": ["c"]}) == []
    assert ej3.habilidades_compartidas({}) == []
    assert equipo["Ada"] == ["python", "sql", "git"]


# ---------------------------------------------------------------- Ejercicio 4
def test_ej4_cuadrados_de_pares():
    assert ej4.cuadrados_de_pares(6) == [0, 4, 16, 36]
    assert ej4.cuadrados_de_pares(7) == [0, 4, 16, 36]
    assert ej4.cuadrados_de_pares(0) == [0]


def test_ej4_longitudes():
    assert ej4.longitudes(["uva", "kiwi"]) == {"uva": 3, "kiwi": 4}
    assert ej4.longitudes([]) == {}


def test_ej4_iniciales():
    assert ej4.iniciales(["ada", "Alan", "grace", ""]) == {"A", "G"}
    assert ej4.iniciales([]) == set()
    assert isinstance(ej4.iniciales(["x"]), set)


def test_ej4_limpiar():
    assert ej4.limpiar(["  Ada ", "", "LINUS", "   "]) == ["ada", "linus"]
    assert ej4.limpiar([]) == []


def test_ej4_filtrar_por_precio():
    precios = {"teclado": 45.0, "raton": 19.9, "monitor": 189.0}
    assert ej4.filtrar_por_precio(precios, 50) == {"teclado": 45.0, "raton": 19.9}
    assert ej4.filtrar_por_precio(precios, 45.0) == {"teclado": 45.0, "raton": 19.9}
    assert ej4.filtrar_por_precio(precios, 1) == {}
    assert len(precios) == 3


def test_ej4_aplanar():
    assert ej4.aplanar([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]
    assert ej4.aplanar([]) == []
    assert ej4.aplanar([["a"], ["b", "c"]]) == ["a", "b", "c"]


def test_ej4_trasponer():
    assert ej4.trasponer([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert ej4.trasponer([[1, 2]]) == [[1], [2]]
    assert ej4.trasponer([]) == []
    resultado = ej4.trasponer([[1, 2], [3, 4]])
    assert all(isinstance(fila, list) for fila in resultado), "Cada fila tiene que ser una lista"


def test_ej4_suma_de_importes():
    lineas = [{"unidades": 2, "precio": 45.0}, {"unidades": 1, "precio": 19.9}]
    assert ej4.suma_de_importes(lineas) == 109.9
    assert ej4.suma_de_importes([]) == 0
    assert ej4.suma_de_importes([{"unidades": 3, "precio": 0.1}]) == 0.3


@pytest.mark.parametrize(
    "nombre",
    [
        "cuadrados_de_pares",
        "longitudes",
        "iniciales",
        "limpiar",
        "filtrar_por_precio",
        "aplanar",
        "trasponer",
        "suma_de_importes",
    ],
)
def test_ej4_una_sola_sentencia_con_comprension(nombre):
    codigo = textwrap.dedent(inspect.getsource(getattr(ej4, nombre)))
    funcion = ast.parse(codigo).body[0]
    cuerpo = funcion.body
    if isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant):
        cuerpo = cuerpo[1:]  # se descarta el docstring
    assert len(cuerpo) == 1 and isinstance(cuerpo[0], ast.Return), (
        f"{nombre} tiene que ser una sola línea return"
    )
    comprensiones = (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)
    assert any(isinstance(nodo, comprensiones) for nodo in ast.walk(cuerpo[0])), (
        f"{nombre} tiene que usar una comprensión o una expresión generadora"
    )


# ---------------------------------------------------------------- Ejercicio 5
@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Anita lava la tina", True),
        ("A man, a plan, a canal: Panama", True),
        ("reconocer", True),
        ("12321", True),
        ("Python", False),
        ("ab", False),
        ("", True),
    ],
)
def test_ej5_es_palindromo(texto, esperado):
    assert ej5.es_palindromo(texto) is esperado


@pytest.mark.parametrize(
    "texto, esperado",
    [("Programación", 5), ("AEIOU", 5), ("xyz", 0), ("", 0), ("pingüino", 4), ("Murciélago", 5)],
)
def test_ej5_contar_vocales(texto, esperado):
    assert ej5.contar_vocales(texto) == esperado


def test_ej5_invertir_palabras():
    assert ej5.invertir_palabras("  hola   mundo cruel ") == "cruel mundo hola"
    assert ej5.invertir_palabras("una") == "una"
    assert ej5.invertir_palabras("") == ""


@pytest.mark.parametrize(
    "texto, esperado",
    [
        ("Fecha de Alta", "fecha_de_alta"),
        ("  codigo-postal ", "codigo_postal"),
        ("Nombre", "nombre"),
        ("total   con  IVA", "total_con_iva"),
        ("id-de-cliente final", "id_de_cliente_final"),
    ],
)
def test_ej5_a_snake_case(texto, esperado):
    assert ej5.a_snake_case(texto) == esperado


def test_ej5_enmascarar():
    assert ej5.enmascarar("4532123456789012") == "************9012"
    assert ej5.enmascarar("123456", 2) == "****56"
    assert ej5.enmascarar("1234") == "1234"
    assert ej5.enmascarar("123") == "123"
    assert ej5.enmascarar("") == ""
    assert ej5.enmascarar("secreto", visibles=0) == "*******"


@pytest.mark.parametrize(
    "a, b, esperado",
    [
        ("Roma", "amor", True),
        ("Nacionalista", "Altisonancia", True),
        ("dormitory", "dirty room", True),
        ("hola", "halo", True),
        ("hola", "hola!", False),
        ("aab", "abb", False),
    ],
)
def test_ej5_son_anagramas(a, b, esperado):
    assert ej5.son_anagramas(a, b) is esperado


def test_ej5_parsear_configuracion():
    assert ej5.parsear_configuracion("host = localhost; puerto=8080;; modo=debug") == {
        "host": "localhost",
        "puerto": "8080",
        "modo": "debug",
    }
    assert ej5.parsear_configuracion("url=http://x.com/?a=1") == {"url": "http://x.com/?a=1"}
    assert ej5.parsear_configuracion("sin_igual; a=1") == {"a": "1"}
    assert ej5.parsear_configuracion("vacio=") == {"vacio": ""}
    assert ej5.parsear_configuracion("") == {}


def test_ej5_formatear_tabla():
    tabla = ej5.formatear_tabla([("teclado", 45), ("monitor", 189.5)])
    assert tabla == "teclado          45.00\nmonitor         189.50"
    assert ej5.formatear_tabla([]) == ""
    assert ej5.formatear_tabla([("a", 1234.567)]) == "a              1234.57"


# ---------------------------------------------------------------- Ejercicio 6
EMPLEADOS = [
    {"id": 1, "nombre": "Ada", "departamento": "IT", "salario": 52000},
    {"id": 2, "nombre": "Linus", "departamento": "IT", "salario": 48000},
    {"id": 3, "nombre": "Grace", "departamento": "Ventas", "salario": 45000},
    {"id": 4, "nombre": "Alan", "departamento": "Ventas", "salario": 39000},
    {"id": 5, "nombre": "Guido", "departamento": "IT", "salario": 48000},
    {"id": 6, "nombre": "Barbara", "departamento": "Legal", "salario": 61000},
]


@pytest.fixture
def empleados():
    return copy.deepcopy(EMPLEADOS)


@pytest.fixture(autouse=True)
def _los_datos_no_cambian(empleados):
    yield
    assert empleados == EMPLEADOS, "La función ha modificado los datos de entrada"


def test_ej6_buscar_por_id(empleados):
    assert ej6.buscar_por_id(empleados, 3)["nombre"] == "Grace"
    assert ej6.buscar_por_id(empleados, 1) is empleados[0]
    assert ej6.buscar_por_id(empleados, 99) is None
    assert ej6.buscar_por_id([], 1) is None


def test_ej6_nombres(empleados):
    assert ej6.nombres(empleados) == ["Ada", "Linus", "Grace", "Alan", "Guido", "Barbara"]
    assert ej6.nombres([]) == []


def test_ej6_filtrar(empleados):
    assert ej6.nombres(ej6.filtrar(empleados, "departamento", "IT")) == ["Ada", "Linus", "Guido"]
    assert ej6.nombres(ej6.filtrar(empleados, "salario", 48000)) == ["Linus", "Guido"]
    assert ej6.filtrar(empleados, "departamento", "Marketing") == []


def test_ej6_ordenar_por(empleados):
    por_nombre = ej6.ordenar_por(empleados, "nombre")
    assert ej6.nombres(por_nombre) == ["Ada", "Alan", "Barbara", "Grace", "Guido", "Linus"]
    por_salario = ej6.ordenar_por(empleados, "salario", descendente=True)
    assert ej6.nombres(por_salario) == ["Barbara", "Ada", "Linus", "Guido", "Grace", "Alan"]
    assert por_nombre is not empleados


def test_ej6_mejor_pagados(empleados):
    assert ej6.mejor_pagados(empleados) == ["Barbara", "Ada", "Guido"]
    assert ej6.mejor_pagados(empleados, 4) == ["Barbara", "Ada", "Guido", "Linus"]
    assert ej6.mejor_pagados(empleados, 1) == ["Barbara"]
    assert len(ej6.mejor_pagados(empleados, 50)) == 6
    assert ej6.mejor_pagados([], 3) == []


def test_ej6_agrupar_por(empleados):
    grupos = ej6.agrupar_por(empleados, "departamento")
    assert list(grupos) == ["IT", "Ventas", "Legal"]
    assert ej6.nombres(grupos["IT"]) == ["Ada", "Linus", "Guido"]
    assert ej6.nombres(grupos["Ventas"]) == ["Grace", "Alan"]
    assert ej6.nombres(grupos["Legal"]) == ["Barbara"]
    assert ej6.agrupar_por([], "departamento") == {}


def test_ej6_salario_medio_por_departamento(empleados):
    assert ej6.salario_medio_por_departamento(empleados) == {
        "IT": 49333.33,
        "Ventas": 42000.0,
        "Legal": 61000.0,
    }
    assert ej6.salario_medio_por_departamento([]) == {}


def test_ej6_emparejar():
    assert ej6.emparejar(["id", "nombre"], [[1, "Ada"], [2, "Linus"]]) == [
        {"id": 1, "nombre": "Ada"},
        {"id": 2, "nombre": "Linus"},
    ]
    assert ej6.emparejar(["a"], []) == []
    assert ej6.emparejar(["x", "y"], [(1, 2)]) == [{"x": 1, "y": 2}]
