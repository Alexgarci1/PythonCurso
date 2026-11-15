"""Tests del ejercicio 4 del Módulo 7: agrupar, agregar y combinar."""

from pathlib import Path

import pandas as pd
import pytest

import m7_ej4_agrupacion as ej

DATOS = Path(__file__).parent.parent / "datos"


@pytest.fixture(scope="module")
def ventas():
    df = pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])
    df["importe"] = df["unidades"] * df["precio"]
    return df


@pytest.fixture(scope="module")
def objetivos():
    return pd.read_csv(DATOS / "objetivos.csv")


@pytest.fixture
def pocas():
    df = pd.DataFrame({
        "fecha": pd.to_datetime(["2026-01-10", "2026-01-20", "2026-02-03", "2026-02-15", "2026-04-01"]),
        "vendedor": ["Ada", "Linus", "Ada", "Grace", "Linus"],
        "region": ["Norte", "Sur", "Norte", "Sur", "Sur"],
        "producto": ["Ratón", "Teclado", "Antivirus", "Ratón", "Antivirus"],
        "categoria": ["Periféricos", "Periféricos", "Software", "Periféricos", "Software"],
        "unidades": [10, 2, 5, 20, 1],
        "importe": [200.0, 100.0, 150.0, 400.0, 150.0],
    })
    return df


def test_importe_por(pocas, ventas):
    resultado = ej.importe_por(pocas, "vendedor")
    assert isinstance(resultado, pd.Series)
    assert resultado.to_dict() == {"Grace": 400.0, "Ada": 350.0, "Linus": 250.0}
    assert resultado.index.tolist() == ["Grace", "Ada", "Linus"], "De mayor a menor"
    por_region = ej.importe_por(ventas, "region")
    assert por_region.index.tolist() == ["Sur", "Norte", "Centro", "Este"]
    assert por_region["Sur"] == pytest.approx(133490.4)


def test_cuota(pocas, ventas):
    assert ej.cuota(pocas, "region").to_dict() == {"Sur": 65.0, "Norte": 35.0}
    assert ej.cuota(ventas, "region").to_dict() == {"Sur": 30.4, "Norte": 25.5, "Centro": 23.3, "Este": 20.8}


def test_resumen_por_vendedor(pocas):
    resultado = ej.resumen_por_vendedor(pocas)
    assert list(resultado.columns) == ["ventas", "unidades", "importe", "ticket_medio"]
    assert resultado.index.tolist() == ["Grace", "Ada", "Linus"]
    assert resultado.loc["Ada"].tolist() == [2, 15, 350.0, 175.0]
    assert resultado.loc["Linus"].tolist() == [2, 3, 250.0, 125.0]


def test_resumen_por_vendedor_anio(ventas):
    resultado = ej.resumen_por_vendedor(ventas)
    assert resultado.index.tolist() == ["Ada", "Grace", "Margaret", "Alan", "Linus"]
    assert resultado["ventas"].tolist() == [75, 76, 66, 54, 49]
    assert resultado["unidades"].tolist() == [541, 640, 491, 485, 399]
    assert resultado["importe"].tolist() == pytest.approx([111944.0, 107132.2, 88130.4, 69360.4, 62281.9])
    assert resultado["ticket_medio"].tolist() == [1492.59, 1409.63, 1335.31, 1284.45, 1271.06]


def test_importe_mensual(pocas, ventas):
    resultado = ej.importe_mensual(pocas)
    assert resultado.to_dict() == {"2026-01": 300.0, "2026-02": 550.0, "2026-04": 150.0}
    assert resultado.index.tolist() == ["2026-01", "2026-02", "2026-04"]
    anual = ej.importe_mensual(ventas)
    assert len(anual) == 10
    assert anual.idxmax() == "2026-09" and anual.idxmin() == "2026-02"
    assert anual["2026-09"] == pytest.approx(72526.9)


def test_tabla_region_categoria(pocas, ventas):
    resultado = ej.tabla_region_categoria(pocas)
    assert resultado.index.tolist() == ["Norte", "Sur"]
    assert list(resultado.columns) == ["Periféricos", "Software"]
    assert resultado.loc["Norte"].tolist() == [200.0, 150.0]
    assert resultado.loc["Sur"].tolist() == [500.0, 150.0]
    anual = ej.tabla_region_categoria(ventas)
    assert anual.shape == (4, 4)
    assert anual.loc["Sur", "Equipos"] == pytest.approx(81150.0)
    assert anual.loc["Este", "Software"] == pytest.approx(10846.5)


def test_tabla_region_categoria_rellena_con_cero(pocas):
    solo_norte_software = pocas[~((pocas["region"] == "Norte") & (pocas["categoria"] == "Software"))]
    resultado = ej.tabla_region_categoria(solo_norte_software)
    assert resultado.loc["Norte", "Software"] == 0


def test_producto_estrella(pocas, ventas):
    assert ej.producto_estrella(pocas).to_dict() == {"Periféricos": "Ratón", "Software": "Antivirus"}
    assert ej.producto_estrella(ventas).to_dict() == {
        "Equipos": "Portátil", "Periféricos": "Ratón", "Servicios": "Soporte anual", "Software": "Antivirus",
    }


def test_con_objetivos(ventas, objetivos):
    resumen = ej.resumen_por_vendedor(ventas)
    resultado = ej.con_objetivos(resumen, objetivos)
    assert list(resultado.columns) == ["ventas", "unidades", "importe", "ticket_medio", "objetivo", "cumplimiento", "cumplido"]
    assert resultado.index.tolist() == ["Ada", "Grace", "Margaret", "Alan", "Linus"]
    assert resultado["objetivo"].tolist() == [100000, 115000, 90000, 85000, 60000]
    assert resultado["cumplimiento"].tolist() == [111.9, 93.2, 97.9, 81.6, 103.8]
    assert resultado["cumplido"].tolist() == [True, False, False, False, True]
    assert "objetivo" not in resumen.columns, "No modifiques el resumen recibido"


def test_con_objetivos_vendedor_sin_objetivo(pocas):
    objetivos = pd.DataFrame({"vendedor": ["Ada", "Grace"], "objetivo": [300, 500]})
    resultado = ej.con_objetivos(ej.resumen_por_vendedor(pocas), objetivos)
    assert resultado.index.tolist() == ["Grace", "Ada", "Linus"]
    assert pd.isna(resultado.loc["Linus", "objetivo"])
    assert resultado["cumplido"].tolist() == [False, True, False]
    assert resultado.loc["Ada", "cumplimiento"] == 116.7
