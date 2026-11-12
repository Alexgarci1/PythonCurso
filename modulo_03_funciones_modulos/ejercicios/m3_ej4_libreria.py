"""Módulo 3 - Ejercicio 4: módulos de la librería estándar."""

import math
import random
from collections import Counter
from datetime import date
from pathlib import Path


def hipotenusa(cateto_a: float, cateto_b: float) -> float:
    """Devuelve la hipotenusa de un triángulo rectángulo, con dos decimales.

    >>> hipotenusa(3, 4)
    5.0
    """
    raise NotImplementedError


def dias_entre(fecha_inicio: str, fecha_fin: str) -> int:
    """Devuelve los días que hay entre dos fechas en formato ISO (AAAA-MM-DD).

    El resultado es siempre positivo, sea cual sea el orden de las fechas.

    >>> dias_entre("2026-11-19", "2026-11-27")
    8
    """
    raise NotImplementedError


def es_fin_de_semana(fecha_iso: str) -> bool:
    """Indica si una fecha en formato ISO cae en sábado o domingo.

    >>> es_fin_de_semana("2026-11-21")
    True
    >>> es_fin_de_semana("2026-11-23")
    False
    """
    raise NotImplementedError


def extension(ruta: str) -> str:
    """Devuelve la extensión de un fichero en minúsculas y sin el punto.

    Si el fichero no tiene extensión devuelve la cadena vacía.

    >>> extension("informes/Ventas.CSV")
    'csv'
    >>> extension("LEEME")
    ''
    """
    raise NotImplementedError


def palabra_mas_frecuente(texto: str) -> str | None:
    """Devuelve la palabra que más se repite en el texto, en minúsculas.

    No distingue mayúsculas de minúsculas. En caso de empate devuelve la que
    aparece primero. Con un texto sin palabras devuelve ``None``.

    >>> palabra_mas_frecuente("el gato y el perro")
    'el'
    """
    raise NotImplementedError


def tirar_dados(cantidad: int, caras: int = 6, semilla: int | None = None) -> list[int]:
    """Devuelve una lista con el resultado de tirar ``cantidad`` dados.

    Cada resultado es un entero entre 1 y ``caras``. Si se indica ``semilla``,
    se usa un generador ``random.Random(semilla)`` para que la tirada sea
    repetible: la misma semilla produce siempre la misma lista.

    >>> len(tirar_dados(3))
    3
    """
    raise NotImplementedError
