"""Análisis de las incidencias con pandas.

Esta capa mira el conjunto de incidencias como una tabla. No modifica las
incidencias ni el gestor: recibe datos y devuelve tablas y cifras.
"""

from datetime import date

import pandas as pd

from .modelos import CAMPOS, ESTADOS, PRIORIDADES

PENDIENTES = ("abierta", "en_curso")


def a_tabla(incidencias) -> pd.DataFrame:
    """Convierte un iterable de incidencias en un DataFrame.

    Una fila por incidencia y las columnas de ``CAMPOS``, en ese orden.
    ``id`` es entero y ``fecha_alta`` y ``fecha_cierre`` son fechas; el cierre
    de una incidencia sin cerrar es un valor ausente. Sin incidencias devuelve
    un DataFrame vacío con esas mismas columnas.

    Pista: cada incidencia sabe convertirse en una fila con ``a_fila()``.
    """
    raise NotImplementedError


def dias_de_resolucion(tabla: pd.DataFrame) -> pd.Series:
    """Devuelve los días que tardó en cerrarse cada incidencia cerrada.

    El índice es el ``id`` de la incidencia y el valor un entero: los días
    entre el alta y el cierre. Solo aparecen las que tienen fecha de cierre.
    """
    raise NotImplementedError


def tabla_estado_prioridad(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve cuántas incidencias hay de cada estado y prioridad.

    Filas: los cuatro estados, en el orden de ``ESTADOS``. Columnas: las cuatro
    prioridades, en el orden de ``PRIORIDADES``. Las combinaciones sin
    incidencias valen 0 y todos los valores son enteros.
    """
    raise NotImplementedError


def resumen_por_tecnico(tabla: pd.DataFrame) -> pd.DataFrame:
    """Devuelve una fila por técnico con las columnas asignadas, pendientes y cerradas.

    - ``asignadas``: incidencias que tiene asignadas.
    - ``pendientes``: las que están abiertas o en curso.
    - ``cerradas``: las que están cerradas.

    Las incidencias sin técnico se agrupan bajo "Sin asignar". El índice es el
    técnico; las filas van de más a menos asignadas y, a igualdad, por orden
    alfabético.
    """
    raise NotImplementedError


def indicadores(tabla: pd.DataFrame, hoy: date | None = None) -> dict:
    """Devuelve las cifras principales del servicio.

    Claves:

    - "total": número de incidencias (int).
    - "pendientes": abiertas o en curso (int).
    - "porcentaje_pendientes": float con un decimal; 0.0 si no hay incidencias.
    - "sin_asignar": pendientes que no tienen técnico (int).
    - "dias_medios_resolucion": media de ``dias_de_resolucion`` con un decimal,
      o ``None`` si no hay ninguna cerrada.
    - "antiguedad_maxima": días que lleva abierta la pendiente más antigua,
      contados hasta ``hoy``; 0 si no hay pendientes.

    ``hoy`` es por defecto la fecha actual.
    """
    raise NotImplementedError
