"""Módulo 7 - Ejercicio 4: agrupar, agregar y combinar.

Todas las funciones reciben un DataFrame de ventas limpio que ya tiene la
columna ``importe``.
"""

import pandas as pd


def importe_por(df: pd.DataFrame, columna: str) -> pd.Series:
    """Devuelve el importe total por cada valor de ``columna``, de mayor a menor."""
    raise NotImplementedError


def cuota(df: pd.DataFrame, columna: str) -> pd.Series:
    """Devuelve el porcentaje del importe total que supone cada valor de ``columna``.

    De mayor a menor y redondeado a un decimal. La suma es 100, salvo redondeo.
    """
    raise NotImplementedError


def resumen_por_vendedor(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por vendedor con las columnas ventas, unidades, importe y ticket_medio.

    - ``ventas``: número de ventas.
    - ``unidades``: unidades vendidas.
    - ``importe``: importe total.
    - ``ticket_medio``: importe medio por venta, redondeado a dos decimales.

    El índice es el vendedor y las filas van de mayor a menor importe.
    """
    raise NotImplementedError


def importe_mensual(df: pd.DataFrame) -> pd.Series:
    """Devuelve el importe total de cada mes. El índice es el mes como texto "AAAA-MM", en orden."""
    raise NotImplementedError


def tabla_region_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una tabla con las regiones en filas, las categorías en columnas y el importe total.

    Las combinaciones sin ventas valen 0.
    """
    raise NotImplementedError


def producto_estrella(df: pd.DataFrame) -> pd.Series:
    """Devuelve, para cada categoría, el producto con más unidades vendidas.

    El índice es la categoría y el valor el nombre del producto.
    """
    raise NotImplementedError


def con_objetivos(resumen: pd.DataFrame, objetivos: pd.DataFrame) -> pd.DataFrame:
    """Añade a un resumen por vendedor su objetivo y si lo ha cumplido.

    ``resumen`` es el resultado de ``resumen_por_vendedor``. ``objetivos`` tiene
    las columnas vendedor y objetivo. El resultado conserva el orden y el índice
    de ``resumen`` y añade las columnas:

    - ``objetivo``: el objetivo del vendedor. Ausente si no tiene.
    - ``cumplimiento``: importe entre objetivo, en porcentaje con un decimal.
    - ``cumplido``: ``True`` si el importe alcanza el objetivo.
    """
    raise NotImplementedError
