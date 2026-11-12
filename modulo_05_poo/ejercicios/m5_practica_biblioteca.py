"""Módulo 5 - Práctica 5: modelo de dominio de una biblioteca.

Clases del modelo:

    Material (abstracta)      lo que se puede prestar
    ├── Libro
    ├── Revista
    └── Dvd
    Socio                     quien toma prestado
    Prestamo                  un material prestado a un socio en una fecha
    Biblioteca                el catálogo, los socios y los préstamos (composición)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, timedelta


class Material(ABC):
    """Clase base abstracta de todo lo que se puede prestar."""

    def __init__(self, codigo: str, titulo: str, anio: int):
        """Guarda ``codigo``, ``titulo`` y ``anio``. El material empieza disponible.

        La disponibilidad se guarda en el atributo interno ``_disponible``.
        """
        raise NotImplementedError

    @property
    def disponible(self) -> bool:
        """Indica si el material se puede prestar. Solo lectura."""
        raise NotImplementedError

    @property
    @abstractmethod
    def dias_prestamo(self) -> int:
        """Días que se puede tener prestado este tipo de material."""

    def prestar(self) -> None:
        """Marca el material como no disponible.

        Lanza ``ValueError`` si ya estaba prestado.
        """
        raise NotImplementedError

    def devolver(self) -> None:
        """Marca el material como disponible.

        Lanza ``ValueError`` si no estaba prestado.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """Devuelve "[codigo] titulo (anio)"."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Devuelve "Clase('codigo', 'titulo')" con el nombre de la clase real."""
        raise NotImplementedError

    def __eq__(self, otro) -> bool:
        """Dos materiales son iguales si tienen el mismo código.

        Si ``otro`` no es un Material, devuelve ``NotImplemented``.
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.codigo)


class Libro(Material):
    """Un libro. Se presta 21 días."""

    def __init__(self, codigo: str, titulo: str, anio: int, autor: str):
        """Inicializa la parte heredada y guarda ``autor``."""
        raise NotImplementedError

    @property
    def dias_prestamo(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        """Añade el autor a la descripción heredada: "[codigo] titulo (anio), de autor"."""
        raise NotImplementedError


class Revista(Material):
    """Una revista. Se presta 7 días."""

    def __init__(self, codigo: str, titulo: str, anio: int, numero: int):
        """Inicializa la parte heredada y guarda ``numero``."""
        raise NotImplementedError

    @property
    def dias_prestamo(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        """Añade el número: "[codigo] titulo (anio), n.º numero"."""
        raise NotImplementedError


class Dvd(Material):
    """Un DVD. Se presta 3 días. No redefine ``__str__``."""

    def __init__(self, codigo: str, titulo: str, anio: int, minutos: int):
        """Inicializa la parte heredada y guarda ``minutos``."""
        raise NotImplementedError

    @property
    def dias_prestamo(self) -> int:
        raise NotImplementedError


@dataclass
class Socio:
    """Una persona que puede tomar materiales en préstamo.

    Campos: ``numero`` (int), ``nombre`` (str) y ``prestados``, la lista de
    materiales que tiene en este momento, que empieza vacía y es propia de
    cada socio.
    """

    MAX_PRESTAMOS = 3

    # TODO: declara aquí los campos numero, nombre y prestados

    def puede_tomar_prestado(self) -> bool:
        """Indica si el socio tiene menos de ``MAX_PRESTAMOS`` materiales."""
        raise NotImplementedError


@dataclass
class Prestamo:
    """Un material prestado a un socio en una fecha.

    Campos: ``material`` (Material), ``socio`` (Socio) y ``fecha`` (date).
    """

    # TODO: declara aquí los campos material, socio y fecha

    @property
    def fecha_devolucion(self) -> date:
        """Fecha límite: la del préstamo más los días que permite el material."""
        raise NotImplementedError

    def dias_de_retraso(self, hoy: date) -> int:
        """Días transcurridos desde la fecha límite. Si no ha vencido, 0."""
        raise NotImplementedError

    def esta_vencido(self, hoy: date) -> bool:
        """Indica si ``hoy`` es posterior a la fecha límite."""
        raise NotImplementedError


class Biblioteca:
    """El catálogo, los socios y los préstamos en curso.

    Usa composición: contiene un diccionario de materiales por código, un
    diccionario de socios por número y una lista de préstamos. Ninguno de
    los tres es accesible directamente desde fuera.
    """

    def __init__(self, nombre: str):
        """Guarda el nombre y crea ``_materiales``, ``_socios`` y ``_prestamos`` vacíos."""
        raise NotImplementedError

    # ------------------------------------------------------------- catálogo
    def anadir_material(self, material: Material) -> None:
        """Añade un material al catálogo.

        Lanza ``ValueError`` si ya hay un material con ese código.
        """
        raise NotImplementedError

    def buscar(self, codigo: str) -> Material | None:
        """Devuelve el material con ese código, o ``None`` si no existe."""
        raise NotImplementedError

    def buscar_por_titulo(self, texto: str) -> list[Material]:
        """Devuelve los materiales cuyo título contiene el texto.

        No distingue mayúsculas de minúsculas. El resultado va ordenado por título.
        """
        raise NotImplementedError

    def disponibles(self) -> list[Material]:
        """Devuelve los materiales disponibles, ordenados por código."""
        raise NotImplementedError

    def __len__(self) -> int:
        """Devuelve el número de materiales del catálogo."""
        raise NotImplementedError

    def __contains__(self, codigo: str) -> bool:
        """Indica si hay un material con ese código."""
        raise NotImplementedError

    def __iter__(self):
        """Recorre los materiales del catálogo en el orden en que se añadieron."""
        raise NotImplementedError

    # --------------------------------------------------------------- socios
    def registrar_socio(self, nombre: str) -> Socio:
        """Crea un socio con el siguiente número libre, lo guarda y lo devuelve.

        Los números empiezan en 1 y son consecutivos.
        """
        raise NotImplementedError

    def socio(self, numero: int) -> Socio | None:
        """Devuelve el socio con ese número, o ``None`` si no existe."""
        raise NotImplementedError

    # ------------------------------------------------------------ préstamos
    def prestar(self, codigo: str, numero_socio: int, fecha: date) -> Prestamo:
        """Presta un material a un socio y devuelve el préstamo creado.

        Lanza ``ValueError`` con uno de estos mensajes, comprobados en este orden:

        - "No existe el material <codigo>"
        - "No existe el socio <numero>"
        - "<nombre> ha alcanzado el máximo de préstamos"
        - el de ``Material.prestar`` si el material ya está prestado

        Si todo es correcto: marca el material como prestado, lo añade a la
        lista del socio y guarda el préstamo.
        """
        raise NotImplementedError

    def devolver(self, codigo: str) -> Prestamo:
        """Registra la devolución de un material y devuelve el préstamo cerrado.

        Lanza ``ValueError`` con el mensaje "No hay ningún préstamo de <codigo>"
        si ese material no está prestado. Si lo está: lo marca como
        disponible, lo quita de la lista del socio y elimina el préstamo.
        """
        raise NotImplementedError

    @property
    def prestamos(self) -> tuple:
        """Tupla con los préstamos en curso, en el orden en que se hicieron."""
        raise NotImplementedError

    def prestamos_vencidos(self, hoy: date) -> list[Prestamo]:
        """Devuelve los préstamos vencidos, del que lleva más retraso al que menos."""
        raise NotImplementedError

    def resumen(self) -> str:
        """Devuelve "nombre: N materiales, D disponibles, S socios"."""
        raise NotImplementedError
