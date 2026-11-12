"""Tests de los ejercicios del módulo 3."""

import inspect
import random
from pathlib import Path

import pytest

import m3_ej1_funciones as ej1
import m3_ej2_parametros as ej2
import m3_ej3_ambito as ej3
import m3_ej4_libreria as ej4


# ---------------------------------------------------------------- Ejercicio 1
@pytest.mark.parametrize("radio, esperado", [(1, 3.14), (2, 12.57), (0, 0.0), (0.5, 0.79)])
def test_ej1_area_circulo(radio, esperado):
    assert ej1.area_circulo(radio) == esperado


def test_ej1_area_rectangulo():
    assert ej1.area_rectangulo(3, 4) == 12
    assert ej1.area_rectangulo(2.5, 2) == 5.0
    assert ej1.area_rectangulo(0, 9) == 0


def test_ej1_area_triangulo():
    assert ej1.area_triangulo(3, 4) == 6.0
    assert ej1.area_triangulo(5, 5) == 12.5


@pytest.mark.parametrize(
    "figura, medidas, esperado",
    [
        ("circulo", {"radio": 1}, 3.14),
        ("CIRCULO", {"radio": 2}, 12.57),
        ("rectangulo", {"base": 3, "altura": 4}, 12),
        ("Triangulo", {"base": 3, "altura": 4}, 6.0),
        ("rectangulo", {"base": 0, "altura": 4}, 0),
        ("circulo", {"radio": 0}, 0.0),
    ],
)
def test_ej1_calcular_area(figura, medidas, esperado):
    assert ej1.calcular_area(figura, **medidas) == esperado


@pytest.mark.parametrize(
    "figura, medidas",
    [
        ("circulo", {}),
        ("circulo", {"base": 3, "altura": 4}),
        ("rectangulo", {"base": 3}),
        ("triangulo", {"altura": 3}),
        ("hexagono", {"radio": 1}),
    ],
)
def test_ej1_calcular_area_sin_datos(figura, medidas):
    assert ej1.calcular_area(figura, **medidas) is None


def test_ej1_calcular_area_medidas_solo_por_nombre():
    with pytest.raises(TypeError):
        ej1.calcular_area("circulo", 1)


def test_ej1_calcular_area_reutiliza_las_otras_funciones(monkeypatch):
    monkeypatch.setattr(ej1, "area_circulo", lambda radio: "circulo")
    monkeypatch.setattr(ej1, "area_rectangulo", lambda base, altura: "rectangulo")
    monkeypatch.setattr(ej1, "area_triangulo", lambda base, altura: "triangulo")
    assert ej1.calcular_area("circulo", radio=1) == "circulo"
    assert ej1.calcular_area("rectangulo", base=1, altura=1) == "rectangulo"
    assert ej1.calcular_area("triangulo", base=1, altura=1) == "triangulo"


def test_ej1_minimo_y_maximo():
    assert ej1.minimo_y_maximo(4, 8, 15) == (4, 15)
    assert ej1.minimo_y_maximo(7) == (7, 7)
    assert ej1.minimo_y_maximo(-1, -5, 0) == (-5, 0)
    assert ej1.minimo_y_maximo() == (None, None)
    assert ej1.minimo_y_maximo(*[3, 1, 2]) == (1, 3)


def test_ej1_describir():
    def sin_documentar():
        return 1

    def documentada():
        """Primera línea.

        Segunda línea.
        """

    assert ej1.describir(sin_documentar) == "sin_documentar: sin documentar"
    assert ej1.describir(documentada) == "documentada: Primera línea."
    assert ej1.describir(ej1.area_rectangulo) == (
        "area_rectangulo: Devuelve el área de un rectángulo."
    )


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_potencia():
    assert ej2.potencia(3) == 9
    assert ej2.potencia(2, 10) == 1024
    assert ej2.potencia(base=2, exponente=3) == 8
    assert ej2.potencia(4, 0.5) == 2.0
    assert ej2.potencia(5, 0) == 1


def test_ej2_sumar_todos():
    assert ej2.sumar_todos() == 0
    assert ej2.sumar_todos(5) == 5
    assert ej2.sumar_todos(1, 2, 3) == 6
    assert ej2.sumar_todos(*range(101)) == 5050
    assert ej2.sumar_todos(1.5, 2.5) == 4.0


def test_ej2_crear_usuario():
    assert ej2.crear_usuario("Ada") == {"nombre": "Ada", "activo": True}
    assert ej2.crear_usuario("Ada", activo=False) == {"nombre": "Ada", "activo": False}
    assert ej2.crear_usuario("Ada", rol="admin", edad=36) == {
        "nombre": "Ada",
        "activo": True,
        "rol": "admin",
        "edad": 36,
    }


def test_ej2_crear_usuario_activo_solo_por_nombre():
    with pytest.raises(TypeError):
        ej2.crear_usuario("Ada", False)


def test_ej2_anadir_elemento_no_comparte_la_lista():
    assert ej2.anadir_elemento(1) == [1]
    assert ej2.anadir_elemento(2) == [2], (
        "La lista por defecto se comparte entre llamadas: usa None como valor por defecto"
    )
    assert ej2.anadir_elemento(3) == [3]


def test_ej2_anadir_elemento_con_lista():
    lista = [1, 2]
    resultado = ej2.anadir_elemento(3, lista)
    assert resultado == [1, 2, 3]
    assert resultado is lista
    vacia = []
    assert ej2.anadir_elemento("a", vacia) is vacia
    assert vacia == ["a"]


def test_ej2_formatear_nombre():
    assert ej2.formatear_nombre("Ada", "Lovelace") == "Ada Lovelace"
    assert ej2.formatear_nombre(" Ada ", "  Lovelace") == "Ada Lovelace"
    assert ej2.formatear_nombre("Ada", "Lovelace", mayusculas=True) == "ADA LOVELACE"
    assert ej2.formatear_nombre("Ada", "Lovelace", separador=", ") == "Ada, Lovelace"
    assert ej2.formatear_nombre("Ada", "Lovelace", separador="_", mayusculas=True) == (
        "ADA_LOVELACE"
    )


def test_ej2_formatear_nombre_opciones_solo_por_nombre():
    with pytest.raises(TypeError):
        ej2.formatear_nombre("Ada", "Lovelace", True)


def test_ej2_estadisticas():
    assert ej2.estadisticas(2, 4, 9) == (3, 15, 5.0)
    assert ej2.estadisticas(10) == (1, 10, 10.0)
    assert ej2.estadisticas(1, 2) == (2, 3, 1.5)
    assert ej2.estadisticas(1, 1, 2) == (3, 4, 1.33)
    assert ej2.estadisticas() == (0, 0, None)
    cantidad, suma, media = ej2.estadisticas(5, 5)
    assert (cantidad, suma, media) == (2, 10, 5.0)


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_crear_contador():
    contador = ej3.crear_contador()
    assert [contador(), contador(), contador()] == [1, 2, 3]


def test_ej3_crear_contador_con_inicio():
    contador = ej3.crear_contador(10)
    assert contador() == 11
    assert contador() == 12


def test_ej3_contadores_independientes():
    uno = ej3.crear_contador()
    otro = ej3.crear_contador()
    uno()
    uno()
    assert otro() == 1
    assert uno() == 3


def test_ej3_sin_global():
    codigo = Path(ej3.__file__).read_text(encoding="utf-8")
    lineas = [linea.strip() for linea in codigo.splitlines()]
    assert not any(linea.startswith("global ") for linea in lineas), (
        "Este ejercicio se resuelve con cierres, sin la palabra global"
    )


def test_ej3_multiplicador():
    doble = ej3.multiplicador(2)
    triple = ej3.multiplicador(3)
    assert doble(10) == 20
    assert triple(10) == 30
    assert doble(triple(1)) == 6
    assert ej3.multiplicador(0.5)(8) == 4.0


def test_ej3_aplicar():
    valores = [-1, 2, -3]
    assert ej3.aplicar(abs, valores) == [1, 2, 3]
    assert valores == [-1, 2, -3]
    assert ej3.aplicar(str.upper, ["a", "b"]) == ["A", "B"]
    assert ej3.aplicar(lambda x: x * x, [1, 2, 3]) == [1, 4, 9]
    assert ej3.aplicar(len, []) == []


def test_ej3_aplicar_devuelve_lista_nueva():
    valores = [1, 2]
    resultado = ej3.aplicar(abs, valores)
    assert isinstance(resultado, list)
    assert resultado is not valores


def test_ej3_componer():
    incrementar = lambda x: x + 1  # noqa: E731
    duplicar = lambda x: x * 2  # noqa: E731
    assert ej3.componer(duplicar, incrementar)(5) == 12
    assert ej3.componer(incrementar, duplicar)(5) == 11
    assert ej3.componer(len, str.strip)("  hola  ") == 4
    assert ej3.componer(str.upper, str.strip)(" ada ") == "ADA"


def test_ej3_ordenar_por_longitud():
    palabras = ["manzana", "uva", "kiwi"]
    assert ej3.ordenar_por_longitud(palabras) == ["uva", "kiwi", "manzana"]
    assert palabras == ["manzana", "uva", "kiwi"]
    assert ej3.ordenar_por_longitud(["bb", "aa", "c"]) == ["c", "bb", "aa"]
    assert ej3.ordenar_por_longitud([]) == []


def test_ej3_mas_caro():
    productos = [("teclado", 45.0), ("monitor", 189.0), ("raton", 19.9)]
    assert ej3.mas_caro(productos) == ("monitor", 189.0)
    assert ej3.mas_caro([("zapato", 10), ("abrigo", 5)]) == ("zapato", 10)
    assert ej3.mas_caro([("a", 1)]) == ("a", 1)
    assert ej3.mas_caro([]) is None


# ---------------------------------------------------------------- Ejercicio 4
@pytest.mark.parametrize(
    "a, b, esperado", [(3, 4, 5.0), (1, 1, 1.41), (5, 12, 13.0), (0, 2, 2.0)]
)
def test_ej4_hipotenusa(a, b, esperado):
    assert ej4.hipotenusa(a, b) == esperado


@pytest.mark.parametrize(
    "inicio, fin, esperado",
    [
        ("2026-11-19", "2026-11-27", 8),
        ("2026-11-27", "2026-11-19", 8),
        ("2026-11-19", "2026-11-19", 0),
        ("2024-02-28", "2024-03-01", 2),
        ("2025-02-28", "2025-03-01", 1),
        ("2025-12-31", "2026-01-01", 1),
    ],
)
def test_ej4_dias_entre(inicio, fin, esperado):
    assert ej4.dias_entre(inicio, fin) == esperado


@pytest.mark.parametrize(
    "fecha, esperado",
    [
        ("2026-11-21", True),
        ("2026-11-22", True),
        ("2026-11-23", False),
        ("2026-11-20", False),
        ("2026-11-19", False),
    ],
)
def test_ej4_es_fin_de_semana(fecha, esperado):
    assert ej4.es_fin_de_semana(fecha) is esperado


@pytest.mark.parametrize(
    "ruta, esperado",
    [
        ("informes/Ventas.CSV", "csv"),
        ("foto.jpeg", "jpeg"),
        ("copia.tar.gz", "gz"),
        ("LEEME", ""),
        ("datos/2026/enero.xlsx", "xlsx"),
        ("carpeta.v2/fichero", ""),
    ],
)
def test_ej4_extension(ruta, esperado):
    assert ej4.extension(ruta) == esperado


def test_ej4_palabra_mas_frecuente():
    assert ej4.palabra_mas_frecuente("el gato y el perro") == "el"
    assert ej4.palabra_mas_frecuente("Python python PYTHON java") == "python"
    assert ej4.palabra_mas_frecuente("uno dos dos uno tres") == "uno"
    assert ej4.palabra_mas_frecuente("sola") == "sola"
    assert ej4.palabra_mas_frecuente("") is None
    assert ej4.palabra_mas_frecuente("   ") is None


def test_ej4_tirar_dados_cantidad_y_rango():
    tirada = ej4.tirar_dados(200)
    assert len(tirada) == 200
    assert all(isinstance(valor, int) and 1 <= valor <= 6 for valor in tirada)
    assert len(set(tirada)) > 1
    assert ej4.tirar_dados(0) == []


def test_ej4_tirar_dados_caras():
    tirada = ej4.tirar_dados(300, caras=20)
    assert all(1 <= valor <= 20 for valor in tirada)
    assert max(tirada) > 6
    assert ej4.tirar_dados(5, caras=1) == [1, 1, 1, 1, 1]


def test_ej4_tirar_dados_semilla_repetible():
    assert ej4.tirar_dados(10, semilla=42) == ej4.tirar_dados(10, semilla=42)
    assert ej4.tirar_dados(10, semilla=1) != ej4.tirar_dados(10, semilla=2)


def test_ej4_tirar_dados_usa_generador_propio():
    esperado = random.Random(7)
    assert ej4.tirar_dados(5, semilla=7) == [esperado.randint(1, 6) for _ in range(5)]


def test_ej4_tirar_dados_firma():
    parametros = inspect.signature(ej4.tirar_dados).parameters
    assert parametros["caras"].default == 6
    assert parametros["semilla"].default is None
