"""Textos para mostrar por pantalla.

Las funciones de este módulo devuelven cadenas: no usan ``print``.
"""

from datetime import date

from .gestor import GestorIncidencias
from .modelos import ESTADOS, PRIORIDADES, Incidencia

ANCHO = 78


def linea(incidencia: Incidencia) -> str:
    """Devuelve una incidencia en una línea de columnas alineadas.

    Columnas: id a la derecha en 4; dos espacios; prioridad a la izquierda en
    10; estado en 10; asignada_a en 12, o un guion si está vacía; y el título
    al final sin relleno.

    >>> from datetime import date
    >>> linea(Incidencia(7, "No funciona el correo", "Ada", date(2026, 11, 2), "alta"))
    '   7  alta      abierta   -           No funciona el correo'
    """
    raise NotImplementedError


def listado(incidencias: list[Incidencia]) -> str:
    """Devuelve una tabla con cabecera, una línea de guiones y una línea por incidencia.

    La cabecera usa los mismos anchos que ``linea`` con los rótulos "ID",
    "PRIORIDAD", "ESTADO", "ASIGNADA A" y "TÍTULO". La línea de guiones mide
    ``ANCHO``. Si no hay incidencias devuelve "No hay incidencias.".
    """
    raise NotImplementedError


def resumen(gestor: GestorIncidencias, hoy: date) -> str:
    """Devuelve el informe de situación con el formato del enunciado.

    La pendiente más antigua es la que más días lleva abierta a fecha de
    ``hoy``; a igualdad de días, la de menor identificador.
    """
    raise NotImplementedError
