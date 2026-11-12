"""Módulo 5 - Ejercicio 1: clases, objetos y constructores."""


class Rectangulo:
    """Un rectángulo definido por su base y su altura."""

    def __init__(self, base: float, altura: float):
        """Guarda la base y la altura en los atributos ``base`` y ``altura``."""
        raise NotImplementedError

    def area(self) -> float:
        """Devuelve el área.

        >>> Rectangulo(3, 4).area()
        12
        """
        raise NotImplementedError

    def perimetro(self) -> float:
        """Devuelve el perímetro.

        >>> Rectangulo(3, 4).perimetro()
        14
        """
        raise NotImplementedError

    def es_cuadrado(self) -> bool:
        """Indica si la base y la altura son iguales."""
        raise NotImplementedError

    def escalar(self, factor: float) -> "Rectangulo":
        """Devuelve un rectángulo NUEVO con las medidas multiplicadas por ``factor``.

        El rectángulo original no cambia.
        """
        raise NotImplementedError


class Contador:
    """Un contador con paso configurable.

    Es la versión con clase del cierre ``crear_contador`` del módulo 3.
    """

    def __init__(self, inicio: int = 0, paso: int = 1):
        """Guarda el valor inicial en ``valor`` y el paso en ``paso``.

        El contador recuerda además su valor inicial para poder reiniciarse.
        """
        raise NotImplementedError

    def incrementar(self) -> int:
        """Suma el paso al valor y devuelve el valor nuevo.

        >>> contador = Contador()
        >>> contador.incrementar(), contador.incrementar()
        (1, 2)
        """
        raise NotImplementedError

    def reiniciar(self) -> None:
        """Devuelve el valor al inicial."""
        raise NotImplementedError


class Tarea:
    """Una tarea pendiente con etiquetas."""

    def __init__(self, titulo: str, etiquetas: list[str] | None = None):
        """Guarda el título sin espacios alrededor y deja la tarea sin completar.

        Atributos: ``titulo``, ``completada`` (empieza en ``False``) y
        ``etiquetas``. Si no se pasan etiquetas, cada tarea tiene su propia
        lista vacía.
        """
        raise NotImplementedError

    def completar(self) -> None:
        """Marca la tarea como completada."""
        raise NotImplementedError

    def etiquetar(self, etiqueta: str) -> None:
        """Añade la etiqueta en minúsculas si la tarea no la tiene ya."""
        raise NotImplementedError

    def resumen(self) -> str:
        """Devuelve "[x] título" si está completada y "[ ] título" si no.

        >>> Tarea("Comprar pan").resumen()
        '[ ] Comprar pan'
        """
        raise NotImplementedError
