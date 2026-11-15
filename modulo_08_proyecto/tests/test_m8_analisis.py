"""Tests de aceptación del proyecto final: análisis de las incidencias con pandas (hito 6)."""

import inspect
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from incidencias import almacen, analisis
from incidencias.modelos import CAMPOS, ESTADOS, PRIORIDADES, Incidencia

EJEMPLO = Path(__file__).parent.parent / "datos" / "incidencias_ejemplo.csv"
HOY = date(2026, 11, 27)


@pytest.fixture(scope="module")
def tabla():
    return analisis.a_tabla(almacen.cargar(EJEMPLO))


@pytest.fixture(scope="module")
def vacia():
    return analisis.a_tabla([])


# ---------------------------------------------------------------- a_tabla
def test_analisis_a_tabla(tabla):
    assert isinstance(tabla, pd.DataFrame)
    assert list(tabla.columns) == CAMPOS
    assert len(tabla) == 8
    assert tabla["id"].tolist() == [1, 2, 3, 4, 5, 6, 7, 8]
    assert pd.api.types.is_integer_dtype(tabla["id"])
    assert tabla.loc[3, "titulo"] == "Caída del servidor de ficheros"


def test_analisis_a_tabla_fechas(tabla):
    assert pd.api.types.is_datetime64_any_dtype(tabla["fecha_alta"])
    assert pd.api.types.is_datetime64_any_dtype(tabla["fecha_cierre"])
    assert tabla.loc[0, "fecha_alta"] == pd.Timestamp("2026-11-02")
    assert tabla["fecha_cierre"].notna().tolist() == [True, False, False, False, False, False, False, True]


def test_analisis_a_tabla_acepta_cualquier_iterable():
    incidencias = (Incidencia(n, f"Incidencia {n}", "Ada", date(2026, 11, n)) for n in (1, 2, 3))
    resultado = analisis.a_tabla(incidencias)
    assert len(resultado) == 3
    assert resultado["estado"].tolist() == ["abierta"] * 3


def test_analisis_a_tabla_vacia(vacia):
    assert list(vacia.columns) == CAMPOS
    assert len(vacia) == 0


# ---------------------------------------------------------------- dias_de_resolucion
def test_analisis_dias_de_resolucion(tabla, vacia):
    dias = analisis.dias_de_resolucion(tabla)
    assert isinstance(dias, pd.Series)
    assert dias.to_dict() == {1: 3, 8: 1}
    assert pd.api.types.is_integer_dtype(dias)
    assert len(analisis.dias_de_resolucion(vacia)) == 0


# ---------------------------------------------------------------- tabla_estado_prioridad
def test_analisis_tabla_estado_prioridad(tabla):
    resultado = analisis.tabla_estado_prioridad(tabla)
    assert resultado.index.tolist() == list(ESTADOS)
    assert list(resultado.columns) == list(PRIORIDADES)
    assert resultado.values.tolist() == [
        [1, 2, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 0],
        [1, 0, 1, 0],
    ]
    assert all(pd.api.types.is_integer_dtype(tipo) for tipo in resultado.dtypes)


def test_analisis_tabla_estado_prioridad_completa_lo_que_falta(tabla, vacia):
    solo_abiertas = analisis.tabla_estado_prioridad(tabla[tabla["estado"] == "abierta"])
    assert solo_abiertas.shape == (4, 4)
    assert solo_abiertas.loc["abierta"].tolist() == [1, 2, 0, 0]
    assert solo_abiertas.loc["cerrada"].tolist() == [0, 0, 0, 0]
    sin_datos = analisis.tabla_estado_prioridad(vacia)
    assert sin_datos.shape == (4, 4) and sin_datos.values.sum() == 0


# ---------------------------------------------------------------- resumen_por_tecnico
def test_analisis_resumen_por_tecnico(tabla):
    resultado = analisis.resumen_por_tecnico(tabla)
    assert list(resultado.columns) == ["asignadas", "pendientes", "cerradas"]
    assert resultado.index.tolist() == ["Sin asignar", "Marta", "Pablo"]
    assert resultado.loc["Sin asignar"].tolist() == [4, 3, 1]
    assert resultado.loc["Marta"].tolist() == [2, 1, 1]
    assert resultado.loc["Pablo"].tolist() == [2, 1, 0]


def test_analisis_resumen_por_tecnico_vacio(vacia):
    resultado = analisis.resumen_por_tecnico(vacia)
    assert len(resultado) == 0
    assert list(resultado.columns) == ["asignadas", "pendientes", "cerradas"]


# ---------------------------------------------------------------- indicadores
def test_analisis_indicadores(tabla):
    assert analisis.indicadores(tabla, HOY) == {
        "total": 8,
        "pendientes": 5,
        "porcentaje_pendientes": 62.5,
        "sin_asignar": 3,
        "dias_medios_resolucion": 2.0,
        "antiguedad_maxima": 24,
    }


def test_analisis_indicadores_tipos(tabla):
    resultado = analisis.indicadores(tabla, HOY)
    for clave in ("total", "pendientes", "sin_asignar", "antiguedad_maxima"):
        assert type(resultado[clave]) is int, clave
    assert type(resultado["porcentaje_pendientes"]) is float
    assert type(resultado["dias_medios_resolucion"]) is float


def test_analisis_indicadores_sin_cerradas_ni_pendientes(tabla, vacia):
    sin_cerradas = analisis.indicadores(tabla[tabla["fecha_cierre"].isna()], HOY)
    assert sin_cerradas["dias_medios_resolucion"] is None
    assert sin_cerradas["total"] == 6
    solo_cerradas = analisis.indicadores(tabla[tabla["estado"] == "cerrada"], HOY)
    assert (solo_cerradas["pendientes"], solo_cerradas["antiguedad_maxima"]) == (0, 0)
    assert analisis.indicadores(vacia, HOY) == {
        "total": 0, "pendientes": 0, "porcentaje_pendientes": 0.0, "sin_asignar": 0,
        "dias_medios_resolucion": None, "antiguedad_maxima": 0,
    }


def test_analisis_indicadores_usa_la_fecha_actual_por_defecto(tabla):
    esperado = (date.today() - date(2026, 11, 3)).days
    assert analisis.indicadores(tabla)["antiguedad_maxima"] == esperado


# ---------------------------------------------------------------- diseño
def test_analisis_no_modifica_la_tabla(tabla):
    copia = tabla.copy()
    analisis.dias_de_resolucion(tabla)
    analisis.tabla_estado_prioridad(tabla)
    analisis.resumen_por_tecnico(tabla)
    analisis.indicadores(tabla, HOY)
    pd.testing.assert_frame_equal(tabla, copia)


def test_analisis_sin_bucles_ni_print():
    codigo = inspect.getsource(analisis)
    assert "print(" not in codigo and "input(" not in codigo
    for nombre in ("dias_de_resolucion", "tabla_estado_prioridad", "resumen_por_tecnico"):
        cuerpo = inspect.getsource(getattr(analisis, nombre)).split('"""')[-1]
        assert "for " not in cuerpo and "iterrows" not in cuerpo, f"{nombre} se resuelve sin recorrer filas"
