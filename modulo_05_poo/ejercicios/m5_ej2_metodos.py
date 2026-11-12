"""Módulo 5 - Ejercicio 2: atributos de clase y métodos especiales."""


class Dinero:
    """Una cantidad de dinero en una moneda."""

    MONEDAS = ("EUR", "USD", "GBP")

    def __init__(self, cantidad: float, moneda: str = "EUR"):
        """Guarda la cantidad redondeada a dos decimales y la moneda."""
        raise NotImplementedError

    @staticmethod
    def es_moneda_valida(moneda: str) -> bool:
        """Indica si la moneda está en ``MONEDAS``.

        >>> Dinero.es_moneda_valida("EUR"), Dinero.es_moneda_valida("XXX")
        (True, False)
        """
        raise NotImplementedError

    @classmethod
    def desde_texto(cls, texto: str) -> "Dinero":
        """Crea un objeto a partir de un texto como "12.50 EUR".

        >>> Dinero.desde_texto("12.50 EUR")
        Dinero(12.5, 'EUR')
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """Devuelve la representación para depurar: Dinero(12.5, 'EUR')."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Devuelve la representación para el usuario: "12.50 EUR"."""
        raise NotImplementedError

    def __eq__(self, otro) -> bool:
        """Dos objetos Dinero son iguales si coinciden cantidad y moneda.

        Si ``otro`` no es un Dinero, devuelve ``NotImplemented``.
        """
        raise NotImplementedError

    def __lt__(self, otro: "Dinero") -> bool:
        """Compara por cantidad."""
        raise NotImplementedError

    def __add__(self, otro: "Dinero") -> "Dinero":
        """Devuelve un Dinero NUEVO con la suma, en la moneda del primero."""
        raise NotImplementedError


class Playlist:
    """Una lista de canciones que se comporta como una colección integrada.

    Lleva además la cuenta de cuántas playlists se han creado, en el
    atributo de clase ``creadas``.
    """

    creadas = 0

    def __init__(self, nombre: str):
        """Guarda el nombre, crea la lista interna y suma uno a ``creadas``."""
        raise NotImplementedError

    def anadir(self, cancion: str) -> None:
        """Añade una canción al final."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Devuelve el número de canciones."""
        raise NotImplementedError

    def __contains__(self, cancion: str) -> bool:
        """Indica si la canción está, sin distinguir mayúsculas de minúsculas."""
        raise NotImplementedError

    def __iter__(self):
        """Permite recorrer las canciones con un ``for``."""
        raise NotImplementedError

    def __getitem__(self, posicion: int) -> str:
        """Devuelve la canción de la posición indicada."""
        raise NotImplementedError

    def __str__(self) -> str:
        """Devuelve "nombre (N canciones)"."""
        raise NotImplementedError
