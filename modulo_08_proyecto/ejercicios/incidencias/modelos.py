"""Modelo de dominio: la incidencia y sus reglas."""

from dataclasses import dataclass
from datetime import date

from .excepciones import DatosNoValidos, TransicionNoValida

ESTADOS = ("abierta", "en_curso", "resuelta", "cerrada")
PRIORIDADES = ("baja", "media", "alta", "critica")

# Desde cada estado, a cuáles se puede pasar
TRANSICIONES = {
    "abierta": ("en_curso", "cerrada"),
    "en_curso": ("abierta", "resuelta"),
    "resuelta": ("en_curso", "cerrada"),
    "cerrada": (),
}

CAMPOS = ["id", "titulo", "solicitante", "prioridad", "estado", "asignada_a",
          "fecha_alta", "fecha_cierre"]


@dataclass
class Incidencia:
    """Una incidencia del equipo de soporte.

    Campos, en este orden:

    - ``id`` (int)
    - ``titulo`` (str)
    - ``solicitante`` (str)
    - ``fecha_alta`` (date)
    - ``prioridad`` (str), por defecto "media"
    - ``estado`` (str), por defecto "abierta"
    - ``asignada_a`` (str), por defecto la cadena vacía
    - ``fecha_cierre`` (date o None), por defecto None
    """

    # TODO: declara aquí los ocho campos

    def __post_init__(self):
        """Limpia y valida los datos.

        Quita los espacios de alrededor de ``titulo``, ``solicitante`` y
        ``asignada_a``. Lanza ``DatosNoValidos`` con uno de estos mensajes:

        - "El título es obligatorio"
        - "El solicitante es obligatorio"
        - "Prioridad no válida: <valor>"
        - "Estado no válido: <valor>"
        """
        raise NotImplementedError

    @property
    def pendiente(self) -> bool:
        """Indica si la incidencia está abierta o en curso."""
        raise NotImplementedError

    def cambiar_estado(self, nuevo: str, hoy: date) -> None:
        """Pasa la incidencia al estado ``nuevo``.

        Lanza ``DatosNoValidos`` ("Estado no válido: <valor>") si el estado no
        existe y ``TransicionNoValida`` si ``TRANSICIONES`` no permite el
        cambio desde el estado actual.

        Al pasar a "cerrada" se guarda ``hoy`` en ``fecha_cierre``.
        """
        raise NotImplementedError

    def dias_abierta(self, hoy: date) -> int:
        """Días transcurridos desde el alta hasta el cierre o, si no está cerrada, hasta ``hoy``."""
        raise NotImplementedError

    def a_fila(self) -> dict[str, str]:
        """Devuelve la incidencia como diccionario de cadenas, con las claves de ``CAMPOS``.

        Las fechas van en formato ISO y una fecha de cierre ausente es la
        cadena vacía. Es lo que se escribe en el CSV.
        """
        raise NotImplementedError

    @classmethod
    def desde_fila(cls, fila: dict[str, str]) -> "Incidencia":
        """Crea una incidencia a partir de un diccionario de cadenas como el de ``a_fila``.

        Es lo que se lee del CSV. Lanza ``DatosNoValidos`` si falta alguna
        clave, si el identificador no es un entero o si alguna fecha no es
        una fecha ISO, encadenando la excepción original. La validación de
        ``__post_init__`` se aplica igualmente.
        """
        raise NotImplementedError
