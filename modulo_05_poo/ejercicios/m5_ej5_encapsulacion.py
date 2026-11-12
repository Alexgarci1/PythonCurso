"""Módulo 5 - Ejercicio 5: encapsulación y propiedades."""


class CuentaBancaria:
    """Una cuenta cuyo saldo solo cambia con ingresos y retiradas."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        """Guarda el titular y el saldo. Lanza ``ValueError`` si el saldo es negativo.

        El saldo se guarda en ``_saldo`` y los movimientos en ``_movimientos``,
        que empieza vacía.
        """
        raise NotImplementedError

    @property
    def saldo(self) -> float:
        """Saldo actual. Es de solo lectura."""
        raise NotImplementedError

    @property
    def movimientos(self) -> tuple:
        """Tupla con los importes de los movimientos: positivos los ingresos y
        negativos las retiradas."""
        raise NotImplementedError

    def ingresar(self, importe: float) -> None:
        """Suma el importe al saldo. Lanza ``ValueError`` si no es positivo."""
        raise NotImplementedError

    def retirar(self, importe: float) -> None:
        """Resta el importe del saldo.

        Lanza ``ValueError`` si el importe no es positivo o si supera el saldo.
        """
        raise NotImplementedError


class Producto:
    """Un producto con precio validado y precio con IVA calculado."""

    IVA = 21

    def __init__(self, nombre: str, precio: float):
        """Guarda el nombre y el precio. El precio tiene que pasar por el setter."""
        raise NotImplementedError

    @property
    def precio(self) -> float:
        """Precio sin IVA."""
        raise NotImplementedError

    @precio.setter
    def precio(self, valor: float) -> None:
        """Lanza ``ValueError`` si el valor es negativo."""
        raise NotImplementedError

    @property
    def precio_con_iva(self) -> float:
        """Precio con el IVA de la clase aplicado, con dos decimales. Solo lectura.

        >>> Producto("Teclado", 100).precio_con_iva
        121.0
        """
        raise NotImplementedError


class Temperatura:
    """Una temperatura que se puede leer y escribir en dos escalas."""

    CERO_ABSOLUTO = -273.15

    def __init__(self, celsius: float = 0.0):
        """Guarda la temperatura. Tiene que pasar por el setter de ``celsius``."""
        raise NotImplementedError

    @property
    def celsius(self) -> float:
        """Temperatura en grados Celsius."""
        raise NotImplementedError

    @celsius.setter
    def celsius(self, valor: float) -> None:
        """Lanza ``ValueError`` si el valor es menor que ``CERO_ABSOLUTO``."""
        raise NotImplementedError

    @property
    def fahrenheit(self) -> float:
        """Temperatura en grados Fahrenheit: C * 9 / 5 + 32, con dos decimales.

        >>> Temperatura(100).fahrenheit
        212.0
        """
        raise NotImplementedError

    @fahrenheit.setter
    def fahrenheit(self, valor: float) -> None:
        """Convierte a Celsius y asigna a través de la propiedad ``celsius``."""
        raise NotImplementedError
