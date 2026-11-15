"""Tests del ejercicio 5 del Módulo 7: visualización con Matplotlib."""

import os

os.environ.setdefault("MPLBACKEND", "Agg")      # sin ventanas: los gráficos se dibujan en memoria

import inspect

import matplotlib.pyplot as plt
import pandas as pd
import pytest
from matplotlib.figure import Figure

import m7_ej5_graficos as ej

POR_VENDEDOR = pd.Series({"Ada": 350.0, "Grace": 400.0, "Linus": 250.0})
MENSUAL = pd.Series({"2026-01": 300.0, "2026-02": 550.0, "2026-03": 0.0, "2026-04": 150.0})


@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")


def test_grafico_barras():
    figura = ej.grafico_barras(POR_VENDEDOR, "Importe por vendedor")
    assert isinstance(figura, Figure)
    assert len(figura.axes) == 1
    ejes = figura.axes[0]
    assert ejes.get_title() == "Importe por vendedor"
    assert ejes.get_ylabel() == "Importe (€)"
    assert len(ejes.patches) == 3
    assert [barra.get_height() for barra in ejes.patches] == [350.0, 400.0, 250.0]
    assert [texto.get_text() for texto in ejes.get_xticklabels()] == ["Ada", "Grace", "Linus"]


def test_grafico_barras_etiqueta():
    figura = ej.grafico_barras(POR_VENDEDOR, "Unidades", etiqueta_y="Unidades")
    assert figura.axes[0].get_ylabel() == "Unidades"


def test_grafico_lineas():
    figura = ej.grafico_lineas(MENSUAL, "Evolución")
    assert isinstance(figura, Figure)
    ejes = figura.axes[0]
    assert ejes.get_title() == "Evolución" and ejes.get_ylabel() == "Importe (€)"
    assert len(ejes.lines) == 1
    linea = ejes.lines[0]
    assert list(linea.get_ydata()) == [300.0, 550.0, 0.0, 150.0]
    assert linea.get_marker() not in (None, "None", ""), "Cada punto lleva un marcador"
    assert any(l.get_visible() for l in ejes.get_xgridlines() + ejes.get_ygridlines()), "Falta la rejilla"


def test_histograma():
    figura = ej.histograma([1, 2, 2, 3, 3, 3, 9], "Reparto", intervalos=4)
    ejes = figura.axes[0]
    assert ejes.get_title() == "Reparto"
    assert len(ejes.patches) == 4
    assert sum(barra.get_height() for barra in ejes.patches) == 7
    assert len(ej.histograma(range(100), "x").axes[0].patches) == 10


def test_panel():
    figura = ej.panel(POR_VENDEDOR, MENSUAL, "Ventas de 2026")
    assert len(figura.axes) == 2
    izquierda, derecha = figura.axes
    assert izquierda.get_title() == "Por vendedor" and len(izquierda.patches) == 3
    assert derecha.get_title() == "Evolución mensual" and len(derecha.lines) == 1
    assert figura.get_suptitle() == "Ventas de 2026"
    assert izquierda.get_position().x0 < derecha.get_position().x0, "Barras a la izquierda y líneas a la derecha"


def test_guardar(tmp_path):
    figura = ej.grafico_barras(POR_VENDEDOR, "Importe")
    numero = figura.number
    ruta = ej.guardar(figura, tmp_path / "graficos" / "barras.png")
    assert ruta == tmp_path / "graficos" / "barras.png"
    assert ruta.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert ruta.stat().st_size > 5000
    assert not plt.fignum_exists(numero), "Cierra la figura después de guardarla"


def test_guardar_acepta_texto(tmp_path):
    ruta = ej.guardar(ej.grafico_lineas(MENSUAL, "x"), str(tmp_path / "lineas.png"))
    assert ruta.exists()


@pytest.mark.parametrize("nombre", ["grafico_barras", "grafico_lineas", "histograma", "panel"])
def test_no_llaman_a_show(nombre):
    assert ".show(" not in inspect.getsource(getattr(ej, nombre)), "La función devuelve la figura; no la muestra"
