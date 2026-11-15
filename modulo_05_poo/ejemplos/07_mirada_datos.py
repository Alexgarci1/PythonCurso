"""Módulo 5 - Ejemplo 7: mirada de datos.

Objetos para las reglas, tablas para el análisis. Y la sintaxis de las
librerías de datos no es magia: son métodos especiales como los de este módulo.
"""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Venta:
    """Una venta: un registro con sus reglas."""

    region: str
    unidades: int
    precio: float

    def __post_init__(self):
        if self.unidades <= 0:
            raise ValueError("Las unidades deben ser positivas")

    @property
    def importe(self) -> float:
        return round(self.unidades * self.precio, 2)


class Tabla:
    """Una tabla mínima por columnas.

    Enseña qué hay detrás de ``len(tabla)``, ``tabla["columna"]`` y
    ``tabla.columnas`` en una librería como pandas.
    """

    def __init__(self, filas):
        self._filas = list(filas)

    @property
    def columnas(self):
        return list(self._filas[0]) if self._filas else []

    def __len__(self):
        return len(self._filas)

    def __getitem__(self, columna):
        return [fila[columna] for fila in self._filas]

    def __repr__(self):
        return f"Tabla({len(self)} filas, columnas={self.columnas})"


def main():
    ventas = [Venta("Norte", 3, 19.9), Venta("Sur", 1, 250.0), Venta("Norte", 2, 45.5)]

    # --- Los objetos garantizan que cada dato es válido
    try:
        Venta("Sur", 0, 10.0)
    except ValueError as error:
        print("Rechazada:", error)

    # --- De objetos a filas: asdict convierte una dataclass en un diccionario
    filas = [asdict(venta) | {"importe": venta.importe} for venta in ventas]
    print(filas[0])

    # --- La tabla responde a len(), a los corchetes y a un atributo calculado
    tabla = Tabla(filas)
    print(tabla)
    print(len(tabla), tabla.columnas)
    print(sum(tabla["importe"]))


if __name__ == "__main__":
    main()
