"""Tests de la práctica 7: análisis de las ventas del año."""

import os

os.environ.setdefault("MPLBACKEND", "Agg")

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

import m7_practica_analisis as pr

DATOS = Path(__file__).parent.parent / "datos"
COLUMNAS = ["fecha", "vendedor", "region", "producto", "categoria", "unidades", "precio", "importe", "mes"]


@pytest.fixture(scope="module")
def ventas():
    return pr.preparar(pr.cargar(DATOS / "ventas_2026.csv"))


@pytest.fixture(scope="module")
def sucias():
    return pr.preparar(pr.cargar(DATOS / "ventas_sucias.csv"))


@pytest.fixture(scope="module")
def objetivos():
    return pd.read_csv(DATOS / "objetivos.csv")


# ---------------------------------------------------------------- cargar y preparar
def test_cargar_lee_todo_como_texto():
    df = pr.cargar(DATOS / "ventas_sucias.csv")
    assert df.shape == (63, 7)
    assert "tres" in set(df["unidades"].dropna())


def test_preparar_columnas_y_tipos(ventas):
    assert list(ventas.columns) == COLUMNAS
    assert len(ventas) == 320
    assert pd.api.types.is_datetime64_any_dtype(ventas["fecha"])
    assert pd.api.types.is_integer_dtype(ventas["unidades"])
    assert pd.api.types.is_float_dtype(ventas["precio"])
    assert ventas["importe"].sum() == pytest.approx(438848.9)
    assert ventas.loc[0, "mes"] == "2026-01" and ventas["mes"].nunique() == 10
    assert ventas.index.tolist() == list(range(320))
    assert ventas["fecha"].is_monotonic_increasing


def test_preparar_limpia(sucias):
    assert len(sucias) == 54
    assert sucias.isna().sum().sum() == 0
    assert sorted(sucias["vendedor"].unique()) == ["Ada", "Alan", "Grace", "Linus", "Margaret"]
    assert (sucias["region"] == "Sin región").sum() == 2
    assert "Norte" in set(sucias["region"]) and " norte" not in set(sucias["region"])
    assert sucias["importe"].sum() == pytest.approx(54097.6)
    assert (sucias["unidades"] > 0).all()
    assert sucias.index.tolist() == list(range(54))


def test_preparar_coma_decimal():
    df = pd.DataFrame({
        "fecha": ["2026-05-02", "2026-05-01"], "vendedor": ["ada", "ADA"], "region": [None, "Sur"],
        "producto": ["Antivirus", "Ratón"], "categoria": ["Software", "Periféricos"],
        "unidades": ["2", "1"], "precio": ["29,5", "19.9"],
    })
    resultado = pr.preparar(df)
    assert resultado["producto"].tolist() == ["Ratón", "Antivirus"], "Ordenado por fecha"
    assert resultado["importe"].tolist() == pytest.approx([19.9, 59.0])
    assert resultado["region"].tolist() == ["Sur", "Sin región"]
    assert resultado["vendedor"].tolist() == ["Ada", "Ada"]


def test_preparar_no_modifica():
    bruto = pr.cargar(DATOS / "ventas_sucias.csv")
    copia = bruto.copy()
    pr.preparar(bruto)
    pd.testing.assert_frame_equal(bruto, copia)


# ---------------------------------------------------------------- indicadores
def test_indicadores(ventas):
    assert pr.indicadores(ventas) == {
        "ventas": 320,
        "importe_total": 438848.9,
        "ticket_medio": 1371.4,
        "mejor_vendedor": "Ada",
        "mejor_mes": "2026-09",
        "producto_mas_vendido": "Antivirus",
    }


def test_indicadores_sucias(sucias):
    assert pr.indicadores(sucias) == {
        "ventas": 54,
        "importe_total": 54097.6,
        "ticket_medio": 1001.81,
        "mejor_vendedor": "Ada",
        "mejor_mes": "2026-01",
        "producto_mas_vendido": "Licencia ofimática",
    }


def test_indicadores_tipos(ventas):
    resultado = pr.indicadores(ventas)
    assert type(resultado["ventas"]) is int
    assert type(resultado["importe_total"]) is float and type(resultado["ticket_medio"]) is float
    assert type(resultado["mejor_vendedor"]) is str


# ---------------------------------------------------------------- ranking
def test_ranking_vendedores(ventas, objetivos):
    ranking = pr.ranking_vendedores(ventas, objetivos)
    assert list(ranking.columns) == ["vendedor", "ventas", "importe", "objetivo", "cumplimiento", "cumplido"]
    assert ranking.index.tolist() == [0, 1, 2, 3, 4]
    assert ranking["vendedor"].tolist() == ["Ada", "Grace", "Margaret", "Alan", "Linus"]
    assert ranking["ventas"].tolist() == [75, 76, 66, 54, 49]
    assert ranking["importe"].tolist() == [111944.0, 107132.2, 88130.4, 69360.4, 62281.9]
    assert ranking["objetivo"].tolist() == [100000, 115000, 90000, 85000, 60000]
    assert ranking["cumplimiento"].tolist() == [111.9, 93.2, 97.9, 81.6, 103.8]
    assert ranking["cumplido"].tolist() == [True, False, False, False, True]


def test_ranking_vendedores_sucias(sucias, objetivos):
    ranking = pr.ranking_vendedores(sucias, objetivos)
    assert ranking["vendedor"].tolist() == ["Ada", "Grace", "Alan", "Margaret", "Linus"]
    assert ranking["cumplimiento"].tolist() == [15.6, 11.7, 12.2, 8.7, 11.5]
    assert not ranking["cumplido"].any()


# ---------------------------------------------------------------- evolución
def test_evolucion_mensual(ventas):
    mensual = pr.evolucion_mensual(ventas)
    assert list(mensual.columns) == ["mes", "importe", "variacion"]
    assert mensual["mes"].tolist() == [f"2026-{m:02d}" for m in range(1, 11)]
    assert mensual["importe"].tolist() == [35982.5, 18936.9, 42354.9, 47667.5, 33559.7,
                                           44101.4, 48997.2, 36720.9, 72526.9, 58001.0]
    assert pd.isna(mensual.loc[0, "variacion"])
    assert mensual["variacion"].tolist()[1:] == [-47.4, 123.7, 12.5, -29.6, 31.4, 11.1, -25.1, 97.5, -20.0]
    assert mensual.index.tolist() == list(range(10))


# ---------------------------------------------------------------- gráficos y exportación
def test_generar_graficos(ventas, tmp_path):
    abiertas = plt.get_fignums()
    carpeta = tmp_path / "salida" / "graficos"
    rutas = pr.generar_graficos(ventas, carpeta)
    assert rutas == [carpeta / "importe_por_vendedor.png", carpeta / "evolucion_mensual.png"]
    for ruta in rutas:
        assert ruta.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        assert ruta.stat().st_size > 5000
    assert plt.get_fignums() == abiertas, "Cierra las figuras después de guardarlas"


def test_exportar(ventas, objetivos, tmp_path):
    ranking = pr.ranking_vendedores(ventas, objetivos)
    ruta = tmp_path / "resultados" / "ranking.csv"
    pr.exportar(ranking, ruta)
    with open(ruta, encoding="utf-8", newline="") as fichero:
        filas = list(csv.reader(fichero))
    assert filas[0] == ["vendedor", "ventas", "importe", "objetivo", "cumplimiento", "cumplido"], "Sin columna de índice"
    assert filas[1][:3] == ["Ada", "75", "111944.0"]
    assert len(filas) == 6


def test_exportar_conserva_las_tildes(tmp_path):
    tabla = pd.DataFrame({"producto": ["Portátil", "Licencia ofimática"], "unidades": [1, 2]})
    pr.exportar(tabla, tmp_path / "productos.csv")
    assert "Portátil" in (tmp_path / "productos.csv").read_text(encoding="utf-8")
