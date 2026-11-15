"""Módulo 7 - Ejercicio 3: limpieza de datos.

Se trabaja con ``datos/ventas_sucias.csv``, leído con todas las columnas como
texto. Ninguna función modifica el DataFrame que recibe.
"""

from pathlib import Path

import pandas as pd

COLUMNAS_TEXTO = ["vendedor", "region", "producto", "categoria"]


def cargar_en_bruto(ruta: str | Path) -> pd.DataFrame:
    """Lee el CSV con todas las columnas como texto, sin que pandas interprete nada.

    Las celdas vacías quedan como valores ausentes.
    """
    raise NotImplementedError


def contar_ausentes(df: pd.DataFrame) -> dict[str, int]:
    """Devuelve cuántos valores ausentes tiene cada columna. Solo las que tienen alguno."""
    raise NotImplementedError


def normalizar_texto(df: pd.DataFrame, columnas: list[str] = COLUMNAS_TEXTO) -> pd.DataFrame:
    """Devuelve una copia con las columnas indicadas sin espacios sobrantes y con la inicial en mayúscula.

    "  ada " y "ADA" pasan a ser "Ada". Los valores ausentes siguen ausentes.
    """
    raise NotImplementedError


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una copia con ``fecha``, ``unidades`` y ``precio`` convertidos.

    - ``fecha``: fecha a partir del formato "AAAA-MM-DD". Lo que no lo cumple queda ausente.
    - ``unidades``: número. Lo que no es un número queda ausente.
    - ``precio``: número. Admite coma decimal: "29,5" es 29.5.
    """
    raise NotImplementedError


def quitar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el DataFrame sin filas repetidas. Se conserva la primera de cada grupo."""
    raise NotImplementedError


def rellenar_region(df: pd.DataFrame, valor: str = "Sin región") -> pd.DataFrame:
    """Devuelve una copia en la que las regiones ausentes se sustituyen por ``valor``."""
    raise NotImplementedError


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica toda la limpieza y devuelve un DataFrame listo para analizar.

    Pasos, en este orden:

    1. Normalizar el texto.
    2. Quitar duplicados.
    3. Convertir los tipos.
    4. Rellenar las regiones ausentes con "Sin región".
    5. Descartar las filas sin fecha, sin vendedor, sin unidades o sin precio,
       y las que tienen unidades o precio menores o iguales que cero.
    6. Dejar ``unidades`` como entero y renumerar el índice desde 0.
    """
    raise NotImplementedError
