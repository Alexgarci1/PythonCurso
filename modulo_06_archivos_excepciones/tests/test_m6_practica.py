"""Tests de la práctica 6: importador de ventas en CSV."""

import csv
import inspect
import logging
from pathlib import Path

import pytest

import m6_practica_importador as imp

DATOS = Path(__file__).parent.parent / "datos"
CABECERA = "fecha,vendedor,region,producto,categoria,unidades,precio\n"
FILA = {
    "fecha": "2026-10-01",
    "vendedor": "Ada",
    "region": "Norte",
    "producto": "Portátil",
    "categoria": "Equipos",
    "unidades": "2",
    "precio": "950.0",
}
ERRORES = [
    "Línea 3: unidades no válidas: tres",
    "Línea 5: fecha no válida: 03/10/2026",
    "Línea 8: falta el campo vendedor",
    "Línea 10: unidades no válidas: -2",
    "Línea 13: precio no válido: 29,5",
    "Línea 15: precio no válido: 0",
]


def _fila(**cambios):
    return {**FILA, **cambios}


def _csv(tmp_path, contenido, nombre="entrada.csv"):
    ruta = tmp_path / nombre
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


# ---------------------------------------------------------------- excepciones
def test_jerarquia_de_excepciones():
    assert imp.ErrorDeImportacion.__bases__ == (Exception,)
    assert issubclass(imp.FicheroNoValido, imp.ErrorDeImportacion)
    assert issubclass(imp.FilaNoValida, imp.ErrorDeImportacion)
    assert not issubclass(imp.FilaNoValida, imp.FicheroNoValido)


# --------------------------------------------------------------- validar_fila
def test_validar_fila_correcta():
    venta = imp.validar_fila(FILA)
    assert venta == {**FILA, "unidades": 2, "precio": 950.0}
    assert isinstance(venta["unidades"], int) and isinstance(venta["precio"], float)


def test_validar_fila_devuelve_un_diccionario_nuevo():
    fila = dict(FILA)
    venta = imp.validar_fila(fila)
    assert venta is not fila
    assert fila == FILA, "No se puede modificar la fila recibida"


def test_validar_fila_quita_espacios_e_ignora_columnas_de_mas():
    venta = imp.validar_fila(_fila(vendedor="  Ada ", unidades=" 3 ", precio=" 10 ", extra="x"))
    assert venta["vendedor"] == "Ada"
    assert (venta["unidades"], venta["precio"]) == (3, 10.0)
    assert list(venta) == imp.CAMPOS


@pytest.mark.parametrize(
    "cambios, mensaje",
    [
        ({"vendedor": ""}, "falta el campo vendedor"),
        ({"region": "   "}, "falta el campo region"),
        ({"precio": ""}, "falta el campo precio"),
        ({"fecha": None}, "falta el campo fecha"),
        ({"vendedor": "", "precio": ""}, "falta el campo vendedor"),
        ({"fecha": "03/10/2026"}, "fecha no válida: 03/10/2026"),
        ({"fecha": "2026-02-30"}, "fecha no válida: 2026-02-30"),
        ({"unidades": "tres"}, "unidades no válidas: tres"),
        ({"unidades": "2.5"}, "unidades no válidas: 2.5"),
        ({"unidades": "0"}, "unidades no válidas: 0"),
        ({"unidades": "-2"}, "unidades no válidas: -2"),
        ({"precio": "29,5"}, "precio no válido: 29,5"),
        ({"precio": "gratis"}, "precio no válido: gratis"),
        ({"precio": "0"}, "precio no válido: 0"),
        ({"precio": "-5"}, "precio no válido: -5"),
        ({"fecha": "ayer", "unidades": "x", "precio": "y"}, "fecha no válida: ayer"),
        ({"unidades": "x", "precio": "y"}, "unidades no válidas: x"),
    ],
)
def test_validar_fila_no_valida(cambios, mensaje):
    with pytest.raises(imp.FilaNoValida) as error:
        imp.validar_fila(_fila(**cambios))
    assert str(error.value) == mensaje


def test_validar_fila_con_un_campo_ausente():
    fila = dict(FILA)
    del fila["categoria"]
    with pytest.raises(imp.FilaNoValida) as error:
        imp.validar_fila(fila)
    assert str(error.value) == "falta el campo categoria"


# ------------------------------------------------------------ importar_ventas
def test_importar_fichero_correcto():
    ventas, errores = imp.importar_ventas(DATOS / "ventas.csv")
    assert len(ventas) == 20
    assert errores == []
    assert ventas[0] == {**FILA, "unidades": 2, "precio": 950.0}
    assert round(sum(v["unidades"] * v["precio"] for v in ventas), 2) == 21686.8


def test_importar_fichero_con_errores():
    ventas, errores = imp.importar_ventas(DATOS / "ventas_con_errores.csv")
    assert len(ventas) == 12
    assert errores == ERRORES
    assert round(sum(v["unidades"] * v["precio"] for v in ventas), 2) == 12690.3


def test_importar_un_error_no_detiene_la_importacion(tmp_path):
    ruta = _csv(
        tmp_path,
        CABECERA
        + "mal,Ada,Norte,Ratón,Periféricos,1,10\n"
        + "2026-10-01,Ada,Norte,Ratón,Periféricos,1,10\n"
        + "2026-10-02,Ada,Norte,Ratón,Periféricos,x,10\n"
        + "2026-10-03,Ada,Norte,Ratón,Periféricos,2,10\n",
    )
    ventas, errores = imp.importar_ventas(ruta)
    assert [venta["fecha"] for venta in ventas] == ["2026-10-01", "2026-10-03"]
    assert errores == ["Línea 2: fecha no válida: mal", "Línea 4: unidades no válidas: x"]


def test_importar_solo_cabecera(tmp_path):
    assert imp.importar_ventas(_csv(tmp_path, CABECERA)) == ([], [])


def test_importar_acepta_columnas_en_otro_orden(tmp_path):
    ruta = _csv(
        tmp_path,
        "precio,unidades,categoria,producto,region,vendedor,fecha,nota\n"
        "10,2,Periféricos,Ratón,Norte,Ada,2026-10-01,urgente\n",
    )
    ventas, errores = imp.importar_ventas(ruta)
    assert errores == []
    assert ventas == [
        {
            "fecha": "2026-10-01",
            "vendedor": "Ada",
            "region": "Norte",
            "producto": "Ratón",
            "categoria": "Periféricos",
            "unidades": 2,
            "precio": 10.0,
        }
    ]


def test_importar_fichero_que_no_existe(tmp_path):
    ruta = tmp_path / "no_existe.csv"
    with pytest.raises(imp.FicheroNoValido) as error:
        imp.importar_ventas(ruta)
    assert str(error.value) == f"No existe el fichero {ruta}"
    assert isinstance(error.value.__cause__, FileNotFoundError), "Falta raise ... from error"


@pytest.mark.parametrize(
    "cabecera, mensaje",
    [
        ("fecha,vendedor,producto,categoria,unidades\n", "Faltan columnas: region, precio"),
        ("a,b,c\n", "Faltan columnas: " + ", ".join(imp.CAMPOS)),
        ("", "Faltan columnas: " + ", ".join(imp.CAMPOS)),
    ],
)
def test_importar_faltan_columnas(tmp_path, cabecera, mensaje):
    ruta = _csv(tmp_path, cabecera + "1,2,3,4,5\n" if cabecera else "")
    with pytest.raises(imp.FicheroNoValido) as error:
        imp.importar_ventas(ruta)
    assert str(error.value) == mensaje


def test_importar_registra_avisos(caplog):
    with caplog.at_level(logging.WARNING, logger=imp.__name__):
        imp.importar_ventas(DATOS / "ventas_con_errores.csv")
    avisos = [registro for registro in caplog.records if registro.levelno == logging.WARNING]
    assert len(avisos) == 6
    assert "unidades no válidas: tres" in avisos[0].getMessage()
    assert "3" in avisos[0].getMessage()


def test_importar_sin_avisos_si_todo_es_correcto(caplog):
    with caplog.at_level(logging.WARNING, logger=imp.__name__):
        imp.importar_ventas(DATOS / "ventas.csv")
    assert caplog.records == []


# -------------------------------------------------------------------- resumen
def test_resumen_por_region():
    ventas, _ = imp.importar_ventas(DATOS / "ventas_con_errores.csv")
    assert imp.resumen_por_region(ventas) == [
        {"region": "Norte", "ventas": 5, "unidades": 23, "importe": 8413.8},
        {"region": "Sur", "ventas": 4, "unidades": 40, "importe": 2317.0},
        {"region": "Centro", "ventas": 3, "unidades": 19, "importe": 1959.5},
    ]
    assert imp.resumen_por_region([]) == []


def test_resumen_redondea():
    ventas = [imp.validar_fila(_fila(unidades="1", precio="0.1")) for _ in range(3)]
    assert imp.resumen_por_region(ventas) == [
        {"region": "Norte", "ventas": 3, "unidades": 3, "importe": 0.3}
    ]


def test_exportar_resumen(tmp_path):
    ventas, _ = imp.importar_ventas(DATOS / "ventas_con_errores.csv")
    ruta = tmp_path / "resumen.csv"
    imp.exportar_resumen(ruta, ventas)
    assert ruta.read_bytes().decode("utf-8").replace("\r\n", "\n") == (
        "region,ventas,unidades,importe\nNorte,5,23,8413.8\nSur,4,40,2317.0\nCentro,3,19,1959.5\n"
    )
    assert b"\r\r\n" not in ruta.read_bytes(), 'Falta newline="" al abrir el fichero'


def test_exportar_resumen_sin_ventas(tmp_path):
    ruta = tmp_path / "resumen.csv"
    imp.exportar_resumen(ruta, [])
    with open(ruta, encoding="utf-8", newline="") as fichero:
        assert list(csv.reader(fichero)) == [imp.CAMPOS_RESUMEN]


def test_escribir_errores(tmp_path):
    ruta = tmp_path / "errores.txt"
    imp.escribir_errores(ruta, ERRORES)
    assert ruta.read_text(encoding="utf-8") == "\n".join(ERRORES) + "\n"
    imp.escribir_errores(ruta, [])
    assert ruta.read_text(encoding="utf-8") == ""


# ------------------------------------------------------------------- procesar
def test_procesar(tmp_path, caplog):
    salida = tmp_path / "resultados" / "octubre"
    with caplog.at_level(logging.INFO, logger=imp.__name__):
        cantidades = imp.procesar(DATOS / "ventas_con_errores.csv", salida)
    assert cantidades == {"leidas": 18, "validas": 12, "descartadas": 6}
    assert (salida / "errores.txt").read_text(encoding="utf-8").splitlines() == ERRORES
    assert (salida / "resumen.csv").read_text(encoding="utf-8").splitlines()[1] == (
        "Norte,5,23,8413.8"
    )
    informativos = [r.getMessage() for r in caplog.records if r.levelno == logging.INFO]
    assert len(informativos) == 1
    assert "12" in informativos[0] and "6" in informativos[0]


def test_procesar_fichero_correcto(tmp_path):
    cantidades = imp.procesar(DATOS / "ventas.csv", tmp_path)
    assert cantidades == {"leidas": 20, "validas": 20, "descartadas": 0}
    assert (tmp_path / "errores.txt").read_text(encoding="utf-8") == ""
    assert len((tmp_path / "resumen.csv").read_text(encoding="utf-8").splitlines()) == 4


def test_procesar_fichero_no_valido_no_escribe_nada(tmp_path):
    salida = tmp_path / "resultados"
    with pytest.raises(imp.FicheroNoValido):
        imp.procesar(tmp_path / "no_existe.csv", salida)
    assert not salida.exists()


# ----------------------------------------------------------------------- main
def test_main_correcto(tmp_path, capsys):
    assert imp.main([str(DATOS / "ventas_con_errores.csv"), str(tmp_path / "salida")]) == 0
    assert "12 válidas y 6 descartadas" in capsys.readouterr().out
    assert (tmp_path / "salida" / "resumen.csv").exists()


def test_main_fichero_no_valido(tmp_path, capsys):
    assert imp.main([str(tmp_path / "no_existe.csv"), str(tmp_path / "salida")]) == 1
    assert capsys.readouterr().out == ""
    assert not (tmp_path / "salida").exists()


# --------------------------------------------------------------------- estilo
def test_sin_print_fuera_de_main():
    for nombre in ("validar_fila", "importar_ventas", "resumen_por_region", "exportar_resumen",
                   "escribir_errores", "procesar"):
        assert "print(" not in inspect.getsource(getattr(imp, nombre)), (
            f"{nombre} no puede usar print: devuelve, lanza o registra con logging"
        )


def test_sin_except_generico():
    codigo = inspect.getsource(imp)
    lineas = [linea.strip() for linea in codigo.splitlines()]
    assert "except:" not in lineas, "No uses except: a secas"
    assert not any(linea.startswith("except Exception") for linea in lineas), (
        "Captura la excepción concreta, no Exception"
    )
