"""Operaciones sobre el conjunto de incidencias."""

from datetime import date

from .excepciones import IncidenciaNoEncontrada
from .modelos import PRIORIDADES, Incidencia


class GestorIncidencias:
    """Contiene las incidencias y ofrece las operaciones de la aplicación.

    Usa composición: guarda las incidencias en un diccionario interno por
    identificador. No lee ni escribe ficheros y no usa ``print`` ni ``input``.
    """

    def __init__(self, incidencias: list[Incidencia] | None = None):
        """Crea el gestor, vacío o con las incidencias recibidas."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Devuelve el número de incidencias."""
        raise NotImplementedError

    def __iter__(self):
        """Recorre las incidencias por orden de identificador."""
        raise NotImplementedError

    def crear(self, titulo: str, solicitante: str, prioridad: str = "media",
              hoy: date | None = None) -> Incidencia:
        """Da de alta una incidencia y la devuelve.

        El identificador es el mayor que exista más uno, o 1 si no hay
        ninguna. La fecha de alta es ``hoy`` o, si no se indica, la fecha
        actual. Si los datos no valen, ``DatosNoValidos`` sube sin capturar y
        no se guarda nada.
        """
        raise NotImplementedError

    def obtener(self, identificador: int) -> Incidencia:
        """Devuelve la incidencia con ese identificador.

        Lanza ``IncidenciaNoEncontrada`` si no existe.
        """
        raise NotImplementedError

    def cambiar_estado(self, identificador: int, nuevo: str,
                       hoy: date | None = None) -> Incidencia:
        """Cambia el estado de una incidencia y la devuelve.

        Delega en ``Incidencia.cambiar_estado``. ``hoy`` es la fecha actual
        si no se indica.
        """
        raise NotImplementedError

    def asignar(self, identificador: int, tecnico: str) -> Incidencia:
        """Asigna la incidencia a un técnico y la devuelve.

        Guarda el nombre sin espacios alrededor. Si la incidencia estaba
        "abierta", pasa a "en_curso".
        """
        raise NotImplementedError

    def filtrar(self, *, estado: str | None = None, prioridad: str | None = None,
                asignada_a: str | None = None, texto: str | None = None) -> list[Incidencia]:
        """Devuelve las incidencias que cumplen todos los criterios indicados.

        Un criterio que vale ``None`` no se aplica. ``texto`` se busca dentro
        del título sin distinguir mayúsculas de minúsculas. El resultado va
        ordenado por identificador.
        """
        raise NotImplementedError

    def pendientes(self) -> list[Incidencia]:
        """Devuelve las incidencias pendientes en el orden en que hay que atenderlas.

        Primero las de mayor prioridad; a igual prioridad, las más antiguas;
        a igual fecha, por identificador.
        """
        raise NotImplementedError

    def contar_por(self, campo: str) -> dict[str, int]:
        """Cuenta las incidencias por el valor de un campo.

        ``campo`` es el nombre de un atributo, como "estado", "prioridad" o
        "asignada_a". Solo aparecen los valores que tienen alguna incidencia.

        >>> GestorIncidencias().contar_por("estado")
        {}
        """
        raise NotImplementedError
