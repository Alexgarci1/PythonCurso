"""Tests del ejercicio 2 del Módulo 7: pandas, cargar, inspeccionar y seleccionar."""

from pathlib import Path

import pandas as pd
import pytest

import m7_ej2_pandas as ej

DATOS = Path(__file__).parent.parent / "datos"

VENTAS = [
    {"fecha": "2026-10-01", "vendedor": "Ada", "region": "Norte", "producto": "Portátil", "categoria": "Equipos", "unidades": 2, "precio": 950.0},
    {"fecha": "2026-10-01", "vendedor": "Linus", "region": "Sur", "producto": "Ratón", "categoria": "Periféricos", "unidades": 10, "precio": 19.9},
    {"fecha": "2026-10-02", "vendedor": "Grace", "region": "Centro", "producto": "Monitor", "categoria": "Periféricos", "unidades": 3, "precio": 189.0},
    {"fecha": "2026-10-05", "vendedor": "Alan", "region": "Sur", "producto": "Antivirus", "categoria": "Software", "unidades": 30, "precio": 29.5},
    {"fecha": "2026-10-09", "vendedor": "Ada", "region": "Norte", "producto": "Servidor", "categoria": "Equipos", "unidades": 1, "precio": 3200.0},
]


@pytest.fixture
def pocas():
    df = pd.DataFrame(VENTAS)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


@pytest.fixture(scope="module")
def anio():
    return pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])


def test_crear_dataframe():
    df = ej.crear_dataframe(VENTAS)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (5, 7)
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert df.loc[4, "fecha"].day == 9
    assert df["unidades"].sum() == 46


def test_cargar_ventas():
    df = ej.cargar_ventas(DATOS / "ventas_2026.csv")
    assert df.shape == (320, 7)
    assert pd.api.types.is_datetime64_any_dtype(df["fecha"])
    assert pd.api.types.is_integer_dtype(df["unidades"])
    assert "Licencia ofimática" in set(df["producto"])


def test_con_importe(pocas):
    antes = list(pocas.columns)
    resultado = ej.con_importe(pocas)
    assert resultado["importe"].tolist() == pytest.approx([1900.0, 199.0, 567.0, 885.0, 3200.0])
    assert list(resultado.columns) == antes + ["importe"]
    assert list(pocas.columns) == antes, "No modifiques el DataFrame original"


def test_resumen(pocas):
    assert ej.resumen(pocas) == {
        "filas": 5,
        "columnas": ["fecha", "vendedor", "region", "producto", "categoria", "unidades", "precio"],
        "desde": "2026-10-01",
        "hasta": "2026-10-09",
        "unidades": 46,
    }


def test_resumen_tipos(anio):
    resultado = ej.resumen(anio)
    assert resultado["filas"] == 320 and resultado["unidades"] == 2556
    assert (resultado["desde"], resultado["hasta"]) == ("2026-01-05", "2026-10-30")
    assert type(resultado["unidades"]) is int


def test_ventas_de(pocas, anio):
    resultado = ej.ventas_de(pocas, "Ada")
    assert resultado["producto"].tolist() == ["Portátil", "Servidor"]
    assert len(ej.ventas_de(anio, "Ada")) == 75
    assert len(ej.ventas_de(anio, "Nadie")) == 0


def test_filtrar_sin_criterios(pocas):
    assert len(ej.filtrar(pocas)) == 5


def test_filtrar(pocas, anio):
    assert ej.filtrar(pocas, region="Sur")["vendedor"].tolist() == ["Linus", "Alan"]
    assert ej.filtrar(pocas, categorias=["Equipos", "Software"])["producto"].tolist() == ["Portátil", "Antivirus", "Servidor"]
    assert ej.filtrar(pocas, unidades_minimas=10)["producto"].tolist() == ["Ratón", "Antivirus"]
    assert ej.filtrar(pocas, region="Sur", unidades_minimas=20)["vendedor"].tolist() == ["Alan"]
    assert len(ej.filtrar(anio, region="Sur")) == 99
    assert len(ej.filtrar(anio, categorias=["Software", "Servicios"], unidades_minimas=20)) == 38
    assert len(ej.filtrar(anio, region="Norte", categorias=["Equipos"])) == 23


def test_filtrar_no_modifica(pocas):
    copia = pocas.copy()
    ej.filtrar(pocas, region="Sur", categorias=["Software"])
    pd.testing.assert_frame_equal(pocas, copia)


def test_mayores_ventas(pocas):
    resultado = ej.mayores_ventas(pocas, 2)
    assert list(resultado.columns) == ["fecha", "vendedor", "producto", "importe"]
    assert resultado["producto"].tolist() == ["Servidor", "Portátil"]
    assert resultado["importe"].tolist() == [3200.0, 1900.0]
    assert len(ej.mayores_ventas(pocas)) == 3
    assert "importe" not in pocas.columns, "No modifiques el DataFrame original"


def test_productos(pocas, anio):
    assert ej.productos(pocas) == ["Antivirus", "Monitor", "Portátil", "Ratón", "Servidor"]
    assert len(ej.productos(anio)) == 8
    assert isinstance(ej.productos(pocas), list)


def test_precio_medio_por_categoria(pocas, anio):
    assert ej.precio_medio_por_categoria(pocas) == {"Equipos": 2075.0, "Periféricos": 104.45, "Software": 29.5}
    assert ej.precio_medio_por_categoria(anio) == {
        "Equipos": 2075.0, "Periféricos": 82.31, "Servicios": 480.0, "Software": 45.71,
    }
