"""Persistencia de las incidencias en un fichero CSV."""

import csv
import logging
from pathlib import Path

from .excepciones import DatosNoValidos, ErrorDeAlmacen
from .modelos import CAMPOS, Incidencia

logger = logging.getLogger(__name__)


def guardar(ruta, incidencias) -> None:
    """Escribe las incidencias en un CSV con la cabecera ``CAMPOS``.

    ``incidencias`` es cualquier iterable de incidencias: una lista o el
    propio gestor. Si la carpeta no existe, se crea. Registra con
    ``logger.info`` cuántas se han guardado.
    """
    raise NotImplementedError


def cargar(ruta) -> list[Incidencia]:
    """Lee las incidencias de un CSV y las devuelve en una lista.

    Si el fichero no existe devuelve una lista vacía: es la primera vez que
    se ejecuta la aplicación. Lanza ``ErrorDeAlmacen`` con el mensaje
    "Línea N: <motivo>" si alguna fila no es válida, encadenando el
    ``DatosNoValidos`` original. La cabecera es la línea 1.
    """
    raise NotImplementedError
