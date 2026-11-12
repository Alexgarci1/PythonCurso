"""Módulo 6 - Ejercicio 2: CSV.

Todos los ficheros se abren con ``encoding="utf-8"`` y ``newline=""``.
"""

import csv


def leer_csv(ruta, delimitador: str = ",") -> list[dict]:
    """Devuelve las filas del CSV como lista de diccionarios.

    Las claves son los nombres de la cabecera y todos los valores son cadenas.
    """
    raise NotImplementedError


def cabecera(ruta) -> list[str]:
    """Devuelve la lista de nombres de columna. Con el fichero vacío, lista vacía."""
    raise NotImplementedError


def escribir_csv(ruta, registros: list[dict], campos: list[str]) -> None:
    """Escribe los registros en un CSV con la cabecera indicada en ``campos``.

    Las claves de los registros que no estén en ``campos`` se ignoran.
    """
    raise NotImplementedError


def leer_ventas(ruta) -> list[dict]:
    """Lee un CSV de ventas y convierte ``unidades`` a ``int`` y ``precio`` a ``float``.

    El resto de los campos se dejan como cadenas.
    """
    raise NotImplementedError


def total_columna(ruta, columna: str) -> float:
    """Devuelve la suma de los valores de una columna numérica, con dos decimales."""
    raise NotImplementedError


def filtrar_csv(origen, destino, columna: str, valor: str) -> int:
    """Copia en ``destino`` las filas de ``origen`` en las que ``columna`` vale ``valor``.

    El fichero de destino conserva la cabecera y el orden de las columnas.
    Devuelve el número de filas copiadas.
    """
    raise NotImplementedError


def convertir_delimitador(origen, destino, de: str = ";", a: str = ",") -> None:
    """Reescribe un CSV cambiando el delimitador.

    Tiene que funcionar aunque algún campo contenga cualquiera de los dos
    delimitadores: usa ``csv.reader`` y ``csv.writer``, no ``replace``.
    """
    raise NotImplementedError
