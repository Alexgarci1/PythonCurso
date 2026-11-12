"""Tests de los ejercicios del módulo 6."""

import inspect
from pathlib import Path

import pytest

import m6_ej1_ficheros as ej1
import m6_ej2_csv as ej2
import m6_ej3_excepciones as ej3

DATOS = Path(__file__).parent.parent / "datos"

TEXTO = "Primera línea\n\n# comentario\n  Segunda con eñe  \nTercera: PYTHON\n"


@pytest.fixture
def notas(tmp_path):
    ruta = tmp_path / "notas.txt"
    ruta.write_text(TEXTO, encoding="utf-8")
    return ruta


@pytest.fixture
def ventas_csv(tmp_path):
    ruta = tmp_path / "ventas.csv"
    ruta.write_text(
        "producto,region,unidades,precio\n"
        "Teclado,Norte,5,45.0\n"
        '"Monitor 27"", curvo",Sur,3,189.0\n'
        "Ratón,Norte,12,19.9\n",
        encoding="utf-8",
    )
    return ruta


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_contar_lineas(notas, tmp_path):
    assert ej1.contar_lineas(notas) == 5
    assert ej1.contar_lineas(str(notas)) == 5
    vacio = tmp_path / "vacio.txt"
    vacio.write_text("", encoding="utf-8")
    assert ej1.contar_lineas(vacio) == 0
    assert ej1.contar_lineas(DATOS / "notas.txt") == 10


def test_ej1_leer_lineas_utiles(notas):
    assert ej1.leer_lineas_utiles(notas) == [
        "Primera línea",
        "Segunda con eñe",
        "Tercera: PYTHON",
    ]


def test_ej1_escribir_lineas(tmp_path):
    ruta = tmp_path / "salida.txt"
    ej1.escribir_lineas(ruta, ["uno", "dos", "año"])
    assert ruta.read_text(encoding="utf-8") == "uno\ndos\naño\n"
    ej1.escribir_lineas(ruta, ["nuevo"])
    assert ruta.read_text(encoding="utf-8") == "nuevo\n", "El modo w sustituye el contenido"
    ej1.escribir_lineas(ruta, [])
    assert ruta.read_text(encoding="utf-8") == ""


def test_ej1_escribir_lineas_crea_la_carpeta(tmp_path):
    ruta = tmp_path / "informes" / "2026" / "salida.txt"
    ej1.escribir_lineas(ruta, ["hola"])
    assert ruta.read_text(encoding="utf-8") == "hola\n"


def test_ej1_anadir_linea(tmp_path):
    ruta = tmp_path / "registro.txt"
    ej1.anadir_linea(ruta, "primera")
    ej1.anadir_linea(ruta, "segunda")
    assert ruta.read_text(encoding="utf-8") == "primera\nsegunda\n"


def test_ej1_buscar(notas):
    assert ej1.buscar(notas, "python") == [(5, "Tercera: PYTHON")]
    assert ej1.buscar(notas, "LÍNEA") == [(1, "Primera línea")]
    assert ej1.buscar(notas, "e") == [
        (1, "Primera línea"),
        (3, "# comentario"),
        (4, "  Segunda con eñe  "),
        (5, "Tercera: PYTHON"),
    ]
    assert ej1.buscar(notas, "java") == []


def test_ej1_numerar(notas, tmp_path):
    destino = tmp_path / "numerado.txt"
    assert ej1.numerar(notas, destino) == 5
    assert destino.read_text(encoding="utf-8") == (
        "  1: Primera línea\n  2: \n  3: # comentario\n  4:   Segunda con eñe  \n"
        "  5: Tercera: PYTHON\n"
    )
    assert notas.read_text(encoding="utf-8") == TEXTO


def test_ej1_numerar_fichero_vacio(tmp_path):
    origen = tmp_path / "vacio.txt"
    origen.write_text("", encoding="utf-8")
    assert ej1.numerar(origen, tmp_path / "destino.txt") == 0
    assert (tmp_path / "destino.txt").read_text(encoding="utf-8") == ""


def test_ej1_ficheros_por_extension(tmp_path):
    for nombre in ("b.csv", "a.csv", "notas.txt", "c.CSV.bak"):
        (tmp_path / nombre).write_text("x", encoding="utf-8")
    (tmp_path / "carpeta.csv").mkdir()
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "d.csv").write_text("x", encoding="utf-8")
    assert ej1.ficheros_por_extension(tmp_path, "csv") == ["a.csv", "b.csv"]
    assert ej1.ficheros_por_extension(str(tmp_path), "txt") == ["notas.txt"]
    assert ej1.ficheros_por_extension(tmp_path, "json") == []


def test_ej1_usa_with_y_utf8():
    codigo = inspect.getsource(ej1)
    assert codigo.count("open(") == codigo.count("with open(") + codigo.count(", open("), (
        "Todos los open() tienen que ir dentro de un with"
    )
    assert codigo.count("open(") <= codigo.count('encoding="utf-8"'), (
        'Todos los open() tienen que llevar encoding="utf-8"'
    )


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_leer_csv(ventas_csv):
    filas = ej2.leer_csv(ventas_csv)
    assert len(filas) == 3
    assert filas[0] == {"producto": "Teclado", "region": "Norte", "unidades": "5", "precio": "45.0"}
    assert filas[1]["producto"] == 'Monitor 27", curvo'
    assert all(isinstance(valor, str) for fila in filas for valor in fila.values())


def test_ej2_leer_csv_con_delimitador():
    filas = ej2.leer_csv(DATOS / "excel.csv", delimitador=";")
    assert [fila["producto"] for fila in filas] == ["Teclado", "Ratón", 'Monitor 27"; curvo']
    assert filas[0]["precio"] == "45,00"


def test_ej2_cabecera(ventas_csv, tmp_path):
    assert ej2.cabecera(ventas_csv) == ["producto", "region", "unidades", "precio"]
    vacio = tmp_path / "vacio.csv"
    vacio.write_text("", encoding="utf-8")
    assert ej2.cabecera(vacio) == []


def test_ej2_escribir_csv(tmp_path):
    ruta = tmp_path / "salida.csv"
    registros = [
        {"nombre": "Ada", "ciudad": "Londres, UK", "edad": 36},
        {"nombre": "Íñigo", "ciudad": "Bilbao", "edad": 41},
    ]
    ej2.escribir_csv(ruta, registros, ["nombre", "ciudad"])
    assert ruta.read_bytes().decode("utf-8").replace("\r\n", "\n") == (
        'nombre,ciudad\nAda,"Londres, UK"\nÍñigo,Bilbao\n'
    )
    assert b"\r\r\n" not in ruta.read_bytes(), 'Falta newline="" al abrir el fichero'
    assert ej2.leer_csv(ruta) == [
        {"nombre": "Ada", "ciudad": "Londres, UK"},
        {"nombre": "Íñigo", "ciudad": "Bilbao"},
    ]


def test_ej2_escribir_csv_sin_registros(tmp_path):
    ruta = tmp_path / "salida.csv"
    ej2.escribir_csv(ruta, [], ["a", "b"])
    assert ej2.cabecera(ruta) == ["a", "b"]
    assert ej2.leer_csv(ruta) == []


def test_ej2_leer_ventas(ventas_csv):
    ventas = ej2.leer_ventas(ventas_csv)
    assert ventas[0] == {"producto": "Teclado", "region": "Norte", "unidades": 5, "precio": 45.0}
    assert [type(venta["unidades"]) for venta in ventas] == [int, int, int]
    assert [type(venta["precio"]) for venta in ventas] == [float, float, float]


def test_ej2_leer_ventas_fichero_del_curso():
    ventas = ej2.leer_ventas(DATOS / "ventas.csv")
    assert len(ventas) == 20
    assert round(sum(v["unidades"] * v["precio"] for v in ventas), 2) == 21686.8
    assert ventas[0]["producto"] == "Portátil"


def test_ej2_total_columna(ventas_csv):
    assert ej2.total_columna(ventas_csv, "unidades") == 20
    assert ej2.total_columna(ventas_csv, "precio") == 253.9
    assert ej2.total_columna(DATOS / "ventas.csv", "unidades") == 166


def test_ej2_filtrar_csv(ventas_csv, tmp_path):
    destino = tmp_path / "norte.csv"
    assert ej2.filtrar_csv(ventas_csv, destino, "region", "Norte") == 2
    assert ej2.cabecera(destino) == ["producto", "region", "unidades", "precio"]
    assert [fila["producto"] for fila in ej2.leer_csv(destino)] == ["Teclado", "Ratón"]
    assert ej2.filtrar_csv(ventas_csv, destino, "region", "Este") == 0
    assert ej2.cabecera(destino) == ["producto", "region", "unidades", "precio"]
    assert ej2.leer_csv(destino) == []


def test_ej2_convertir_delimitador(tmp_path):
    destino = tmp_path / "convertido.csv"
    ej2.convertir_delimitador(DATOS / "excel.csv", destino)
    filas = ej2.leer_csv(destino)
    assert ej2.cabecera(destino) == ["producto", "unidades", "precio"]
    assert filas[0] == {"producto": "Teclado", "unidades": "5", "precio": "45,00"}
    assert filas[2]["producto"] == 'Monitor 27"; curvo'
    vuelta = tmp_path / "vuelta.csv"
    ej2.convertir_delimitador(destino, vuelta, de=",", a=";")
    assert ej2.leer_csv(vuelta, delimitador=";") == ej2.leer_csv(DATOS / "excel.csv", ";")


# ---------------------------------------------------------------- Ejercicio 3
@pytest.mark.parametrize(
    "texto, por_defecto, esperado",
    [
        ("42", None, 42),
        (" -7 ", None, -7),
        ("abc", None, None),
        ("4.2", 0, 0),
        ("", -1, -1),
        (None, 0, 0),
        (3.9, None, 3),
    ],
)
def test_ej3_a_entero(texto, por_defecto, esperado):
    assert ej3.a_entero(texto, por_defecto) == esperado


def test_ej3_a_entero_usa_try():
    assert "try:" in inspect.getsource(ej3.a_entero)
    assert "isdigit" not in inspect.getsource(ej3.a_entero)


def test_ej3_dividir():
    assert ej3.dividir(10, 4) == 2.5
    assert ej3.dividir(0, 5) == 0
    assert ej3.dividir(10, 0) is None


def test_ej3_dividir_no_esconde_otros_errores():
    with pytest.raises(TypeError):
        ej3.dividir("10", 2)


def test_ej3_leer_o_vacio(tmp_path):
    ruta = tmp_path / "fichero.txt"
    ruta.write_text("contenido con ñ\n", encoding="utf-8")
    assert ej3.leer_o_vacio(ruta) == "contenido con ñ\n"
    assert ej3.leer_o_vacio(tmp_path / "no_existe.txt") == ""


def test_ej3_leer_o_vacio_no_esconde_otros_errores(tmp_path):
    with pytest.raises(OSError):
        ej3.leer_o_vacio(tmp_path)       # es una carpeta, no un fichero


@pytest.mark.parametrize("edad", [0, 36, 130])
def test_ej3_validar_edad_valida(edad):
    assert ej3.validar_edad(edad) == edad


@pytest.mark.parametrize("edad", [-1, 131, 1000])
def test_ej3_validar_edad_fuera_de_rango(edad):
    with pytest.raises(ValueError) as error:
        ej3.validar_edad(edad)
    assert str(edad) in str(error.value), "El mensaje tiene que contener el valor recibido"


@pytest.mark.parametrize("edad", ["36", 36.5, None, True, [36]])
def test_ej3_validar_edad_tipo_incorrecto(edad):
    with pytest.raises(TypeError):
        ej3.validar_edad(edad)


def test_ej3_jerarquia_de_excepciones():
    assert issubclass(ej3.ErrorDeCuenta, Exception)
    assert ej3.ErrorDeCuenta.__bases__ == (Exception,)
    assert issubclass(ej3.ImporteNoValido, ej3.ErrorDeCuenta)
    assert issubclass(ej3.SaldoInsuficiente, ej3.ErrorDeCuenta)
    assert not issubclass(ej3.SaldoInsuficiente, ej3.ImporteNoValido)
    assert issubclass(ej3.ErrorDeConfiguracion, Exception)


def test_ej3_saldo_insuficiente_atributos():
    error = ej3.SaldoInsuficiente(100, 250)
    assert (error.saldo, error.importe) == (100, 250)
    assert "100" in str(error) and "250" in str(error)


def test_ej3_retirar():
    assert ej3.retirar(100, 30) == 70
    assert ej3.retirar(100, 100) == 0


@pytest.mark.parametrize("importe", [0, -5])
def test_ej3_retirar_importe_no_valido(importe):
    with pytest.raises(ej3.ImporteNoValido):
        ej3.retirar(100, importe)


def test_ej3_retirar_saldo_insuficiente():
    with pytest.raises(ej3.SaldoInsuficiente) as error:
        ej3.retirar(100, 250)
    assert (error.value.saldo, error.value.importe) == (100, 250)
    with pytest.raises(ej3.ErrorDeCuenta):
        ej3.retirar(100, 250)
    with pytest.raises(ej3.ErrorDeCuenta):
        ej3.retirar(100, -1)


def test_ej3_convertir_todos():
    assert ej3.convertir_todos(["1.5", "x", "2", "", "3e2", "1,5"]) == (
        [1.5, 2.0, 300.0],
        ["x", "", "1,5"],
    )
    assert ej3.convertir_todos([]) == ([], [])
    assert ej3.convertir_todos(["a", "b"]) == ([], ["a", "b"])


def test_ej3_ejecutar_sin_error():
    registro = []
    assert ej3.ejecutar(lambda: 42, registro) == 42
    assert registro == ["inicio", "ok", "fin"]


def test_ej3_ejecutar_con_error():
    registro = []
    with pytest.raises(ZeroDivisionError):
        ej3.ejecutar(lambda: 1 / 0, registro)
    assert registro == ["inicio", "error", "fin"]
    with pytest.raises(KeyError):
        ej3.ejecutar(lambda: {}["x"], registro)
    assert registro == ["inicio", "error", "fin"] * 2


def test_ej3_ejecutar_usa_finally():
    assert "finally:" in inspect.getsource(ej3.ejecutar)


def test_ej3_puerto_configurado():
    assert ej3.puerto_configurado({"puerto": "8080"}) == 8080
    assert ej3.puerto_configurado({"puerto": 443, "host": "x"}) == 443


@pytest.mark.parametrize(
    "configuracion, causa",
    [({}, KeyError), ({"host": "x"}, KeyError), ({"puerto": "ochenta"}, ValueError)],
)
def test_ej3_puerto_configurado_encadena_la_causa(configuracion, causa):
    with pytest.raises(ej3.ErrorDeConfiguracion) as error:
        ej3.puerto_configurado(configuracion)
    assert isinstance(error.value.__cause__, causa), "Falta raise ... from error"
