"""Módulo 6 - Ejercicio 1: lectura y escritura de ficheros de texto.

Todas las rutas pueden llegar como ``str`` o como ``Path``. Todos los
ficheros se abren con ``with`` y con ``encoding="utf-8"``.
"""

from pathlib import Path


def contar_lineas(ruta) -> int:
    """Devuelve el número de líneas del fichero.

    Tiene que recorrer el fichero línea a línea, sin cargarlo entero en memoria.
    """
    raise NotImplementedError


def leer_lineas_utiles(ruta) -> list[str]:
    """Devuelve las líneas del fichero sin espacios ni saltos alrededor.

    Descarta las líneas vacías y las que empiezan por ``#``.
    """
    raise NotImplementedError


def escribir_lineas(ruta, lineas: list[str]) -> None:
    """Escribe cada elemento de la lista en una línea del fichero.

    Si el fichero existe, se sustituye su contenido. Si la carpeta no existe,
    se crea. Cada línea, incluida la última, termina en salto de línea.
    """
    raise NotImplementedError


def anadir_linea(ruta, linea: str) -> None:
    """Añade una línea al final del fichero sin borrar lo que hubiera.

    Si el fichero no existe, lo crea.
    """
    raise NotImplementedError


def buscar(ruta, texto: str) -> list[tuple[int, str]]:
    """Devuelve las líneas que contienen el texto, sin distinguir mayúsculas.

    Cada resultado es una tupla (número de línea, línea sin el salto final).
    La primera línea del fichero es la 1.
    """
    raise NotImplementedError


def numerar(origen, destino) -> int:
    """Copia ``origen`` en ``destino`` anteponiendo a cada línea su número.

    El formato de cada línea es "  1: texto", con el número alineado a la
    derecha en tres caracteres. Devuelve el número de líneas copiadas.
    """
    raise NotImplementedError


def ficheros_por_extension(carpeta, extension: str) -> list[str]:
    """Devuelve, ordenados, los nombres de los ficheros de la carpeta con esa extensión.

    ``extension`` se recibe sin punto. No busca en subcarpetas.

    >>> ficheros_por_extension(".", "no_existe")
    []
    """
    raise NotImplementedError
