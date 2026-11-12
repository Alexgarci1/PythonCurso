"""Módulo 4 - Ejercicio 6: buscar, filtrar, ordenar y agrupar.

Todas las funciones trabajan con una lista de diccionarios como esta:

    empleados = [
        {"id": 1, "nombre": "Ada", "departamento": "IT", "salario": 52000},
        {"id": 2, "nombre": "Linus", "departamento": "IT", "salario": 48000},
        {"id": 3, "nombre": "Grace", "departamento": "Ventas", "salario": 45000},
    ]

Ninguna función modifica la lista que recibe.
"""


def buscar_por_id(registros: list[dict], identificador: int) -> dict | None:
    """Devuelve el registro cuyo campo "id" coincide, o ``None`` si no existe."""
    raise NotImplementedError


def nombres(registros: list[dict]) -> list[str]:
    """Devuelve la lista con el campo "nombre" de cada registro, en el mismo orden."""
    raise NotImplementedError


def filtrar(registros: list[dict], campo: str, valor) -> list[dict]:
    """Devuelve los registros en los que ``campo`` vale ``valor``."""
    raise NotImplementedError


def ordenar_por(registros: list[dict], campo: str, descendente: bool = False) -> list[dict]:
    """Devuelve una lista nueva con los registros ordenados por ``campo``."""
    raise NotImplementedError


def mejor_pagados(registros: list[dict], cantidad: int = 3) -> list[str]:
    """Devuelve los nombres de los ``cantidad`` empleados con mayor salario.

    De mayor a menor salario. A igual salario, por orden alfabético de nombre.
    """
    raise NotImplementedError


def agrupar_por(registros: list[dict], campo: str) -> dict[str, list[dict]]:
    """Agrupa los registros por el valor de ``campo``.

    Devuelve un diccionario que asocia cada valor distinto del campo con la
    lista de registros que lo tienen, en su orden original.
    """
    raise NotImplementedError


def salario_medio_por_departamento(registros: list[dict]) -> dict[str, float]:
    """Devuelve el salario medio de cada departamento, con dos decimales."""
    raise NotImplementedError


def emparejar(claves: list[str], filas: list[list]) -> list[dict]:
    """Convierte filas de valores en diccionarios usando ``claves`` como nombres de campo.

    Es lo que hace un lector de CSV con la cabecera y las filas.

    >>> emparejar(["id", "nombre"], [[1, "Ada"], [2, "Linus"]])
    [{'id': 1, 'nombre': 'Ada'}, {'id': 2, 'nombre': 'Linus'}]
    """
    raise NotImplementedError
