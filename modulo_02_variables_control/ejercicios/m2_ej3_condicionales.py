"""Módulo 2 - Ejercicio 3: condicionales."""


def calificacion(nota: float) -> str:
    """Traduce una nota de 0 a 10 a su calificación.

    Menos de 5 "Suspenso", de 5 a menos de 7 "Aprobado", de 7 a menos de 9
    "Notable" y de 9 a 10 "Sobresaliente". Fuera de rango, "Nota no válida".

    >>> calificacion(7.5)
    'Notable'
    """
    raise NotImplementedError


def precio_entrada(edad: int, es_festivo: bool = False) -> float:
    """Calcula el precio de una entrada de cine.

    Menores de 4 años: gratis. De 4 a 12: 5 €. De 13 a 64: 9 €. Desde 65: 6 €.
    En festivo se suma un recargo de 2 € a las entradas de pago.

    >>> precio_entrada(30), precio_entrada(30, es_festivo=True), precio_entrada(2, True)
    (9, 11, 0)
    """
    raise NotImplementedError


def describir_http(codigo: int) -> str:
    """Describe un código de estado HTTP.

    200 "Correcto", 201 "Creado", 301 y 302 "Redirección", 400 "Petición
    incorrecta", 401 y 403 "Sin autorización", 404 "No encontrado", cualquier
    otro entre 500 y 599 "Error del servidor" y el resto "Desconocido".

    >>> describir_http(302), describir_http(503)
    ('Redirección', 'Error del servidor')
    """
    raise NotImplementedError


def mayor_de_tres(a: float, b: float, c: float) -> float:
    """Devuelve el mayor de tres números sin usar max().

    >>> mayor_de_tres(3, 9, 5)
    9
    """
    raise NotImplementedError


def tipo_triangulo(a: float, b: float, c: float) -> str:
    """Clasifica un triángulo por sus lados.

    Devuelve "no es un triángulo" si algún lado no es positivo o si no se
    cumple la desigualdad triangular; si no, "equilátero", "isósceles" o
    "escaleno".

    >>> tipo_triangulo(3, 3, 3), tipo_triangulo(3, 4, 5), tipo_triangulo(1, 2, 3)
    ('equilátero', 'escaleno', 'no es un triángulo')
    """
    raise NotImplementedError
