"""Tests del ejercicio 3 del Módulo 7: limpieza de datos."""

from pathlib import Path

import pandas as pd
import pytest

import m7_ej3_limpieza as ej

DATOS = Path(__file__).parent.parent / "datos"


@pytest.fixture
def bruto():
    return pd.read_csv(DATOS / "ventas_sucias.csv", dtype=str)


@pytest.fixture
def mini():
    return pd.DataFrame({
        "fecha": ["2026-01-05", "15/02/2026", None, "2026-03-01"],
        "vendedor": ["  ada ", "GRACE", "linus", None],
        "region": [" norte", None, "Sur", "Este"],
        "producto": ["Ratón", " monitor", "Teclado", "Antivirus"],
        "categoria": ["Periféricos", "Periféricos", "Periféricos", "Software"],
        "unidades": ["6", "tres", "-4", None],
        "precio": ["19.9", "189.0", "45,0", "29,5"],
    })


def test_cargar_en_bruto():
    df = ej.cargar_en_bruto(DATOS / "ventas_sucias.csv")
    assert df.shape == (63, 7)
    assert not pd.api.types.is_numeric_dtype(df["unidades"]), "Todas las columnas se leen como texto"
    assert "tres" in set(df["unidades"].dropna())
    assert "  ada " in set(df["vendedor"].dropna()), "No limpies nada todavía"


def test_contar_ausentes(bruto, mini):
    assert ej.contar_ausentes(bruto) == {"fecha": 1, "vendedor": 1, "region": 2, "unidades": 1}
    assert ej.contar_ausentes(mini) == {"fecha": 1, "vendedor": 1, "region": 1, "unidades": 1}
    assert ej.contar_ausentes(mini[["producto"]]) == {}
    assert all(type(n) is int for n in ej.contar_ausentes(bruto).values())


def test_normalizar_texto(mini):
    resultado = ej.normalizar_texto(mini)
    assert resultado["vendedor"].tolist()[:3] == ["Ada", "Grace", "Linus"]
    assert pd.isna(resultado.loc[3, "vendedor"])
    assert resultado["region"].tolist()[0] == "Norte" and pd.isna(resultado.loc[1, "region"])
    assert resultado["producto"].tolist() == ["Ratón", "Monitor", "Teclado", "Antivirus"]
    assert mini.loc[0, "vendedor"] == "  ada ", "No modifiques el DataFrame original"


def test_normalizar_texto_columnas_elegidas(mini):
    resultado = ej.normalizar_texto(mini, ["vendedor"])
    assert resultado.loc[0, "vendedor"] == "Ada"
    assert resultado.loc[0, "region"] == " norte"


def test_normalizar_texto_conserva_nombres_compuestos(bruto):
    productos = set(ej.normalizar_texto(bruto)["producto"])
    assert "Licencia ofimática" in productos and "Soporte anual" in productos
    assert len(productos) == 8


def test_convertir_tipos(mini):
    resultado = ej.convertir_tipos(mini)
    assert pd.api.types.is_datetime64_any_dtype(resultado["fecha"])
    assert resultado["fecha"].isna().tolist() == [False, True, True, False]
    assert resultado.loc[0, "fecha"].month == 1
    assert pd.api.types.is_numeric_dtype(resultado["unidades"])
    assert resultado["unidades"].isna().tolist() == [False, True, False, True]
    assert resultado.loc[2, "unidades"] == -4
    assert resultado["precio"].tolist() == [19.9, 189.0, 45.0, 29.5]
    assert mini.loc[3, "precio"] == "29,5", "No modifiques el DataFrame original"


def test_quitar_duplicados(bruto):
    assert len(ej.quitar_duplicados(bruto)) == 60
    df = pd.DataFrame({"a": [1, 1, 2, 1], "b": ["x", "x", "y", "z"]})
    resultado = ej.quitar_duplicados(df)
    assert resultado.to_dict("list") == {"a": [1, 2, 1], "b": ["x", "y", "z"]}
    assert len(df) == 4


def test_rellenar_region(mini):
    assert ej.rellenar_region(mini)["region"].tolist() == [" norte", "Sin región", "Sur", "Este"]
    assert ej.rellenar_region(mini, "?")["region"].tolist()[1] == "?"
    assert pd.isna(mini.loc[1, "region"]), "No modifiques el DataFrame original"


def test_limpiar_mini(mini):
    resultado = ej.limpiar(mini)
    assert len(resultado) == 1
    fila = resultado.iloc[0]
    assert (fila["vendedor"], fila["region"], fila["unidades"], fila["precio"]) == ("Ada", "Norte", 6, 19.9)


def test_limpiar(bruto):
    resultado = ej.limpiar(bruto)
    assert len(resultado) == 54
    assert resultado.index.tolist() == list(range(54))
    assert resultado.isna().sum().sum() == 0
    assert pd.api.types.is_integer_dtype(resultado["unidades"])
    assert pd.api.types.is_float_dtype(resultado["precio"])
    assert pd.api.types.is_datetime64_any_dtype(resultado["fecha"])
    assert sorted(resultado["vendedor"].unique()) == ["Ada", "Alan", "Grace", "Linus", "Margaret"]
    assert sorted(resultado["region"].unique()) == ["Centro", "Este", "Norte", "Sin región", "Sur"]
    assert (resultado["region"] == "Sin región").sum() == 2
    assert (resultado["unidades"] > 0).all() and (resultado["precio"] > 0).all()
    assert (resultado["unidades"] * resultado["precio"]).sum() == pytest.approx(54097.6)


def test_limpiar_no_modifica(bruto):
    copia = bruto.copy()
    ej.limpiar(bruto)
    pd.testing.assert_frame_equal(bruto, copia)


def test_limpiar_un_fichero_limpio_no_pierde_filas():
    limpio = pd.read_csv(DATOS / "ventas_2026.csv", dtype=str)
    assert len(ej.limpiar(limpio)) == 320
