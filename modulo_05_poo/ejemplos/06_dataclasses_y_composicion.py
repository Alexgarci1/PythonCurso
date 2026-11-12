"""Módulo 5 - Ejemplo 6: dataclasses y composición."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Punto:
    x: float
    y: float


@dataclass(order=True)
class Version:
    mayor: int
    menor: int = 0

    def __str__(self):
        return f"{self.mayor}.{self.menor}"


@dataclass
class LineaPedido:
    producto: str
    unidades: int
    precio: float
    descuento: float = 0.0

    def __post_init__(self):                 # validación tras el __init__ generado
        if self.unidades <= 0:
            raise ValueError("Las unidades deben ser positivas")

    @property
    def importe(self) -> float:
        return round(self.unidades * self.precio * (1 - self.descuento / 100), 2)


@dataclass
class Cliente:
    nombre: str
    ciudad: str = "Madrid"


@dataclass
class Pedido:
    """Composición: un pedido TIENE un cliente y TIENE líneas."""

    numero: int
    cliente: Cliente
    lineas: list[LineaPedido] = field(default_factory=list)

    def anadir(self, producto, unidades, precio, descuento=0.0):
        self.lineas.append(LineaPedido(producto, unidades, precio, descuento))

    @property
    def total(self) -> float:
        return round(sum(linea.importe for linea in self.lineas), 2)

    def __len__(self):
        return len(self.lineas)


def main():
    # --- __init__, __repr__ y __eq__ generados
    linea = LineaPedido("Teclado", 2, 45.0)
    print(linea, linea.importe)
    print(linea == LineaPedido("Teclado", 2, 45.0))

    try:
        LineaPedido("Ratón", 0, 19.9)
    except ValueError as error:
        print("ValueError:", error)

    # --- frozen: inmutable y utilizable como clave
    origen = Punto(0, 0)
    try:
        origen.x = 5
    except AttributeError as error:
        print(type(error).__name__, error)
    print({origen: "origen", Punto(1, 1): "diagonal"}[Punto(0, 0)])

    # --- order: comparación campo a campo
    versiones = [Version(3, 12), Version(3, 9), Version(2, 7)]
    print([str(version) for version in sorted(versiones)], max(versiones))

    # --- Composición y default_factory: cada pedido tiene su propia lista
    pedido = Pedido(1042, Cliente("Ada"))
    otro = Pedido(1043, Cliente("Linus", "Helsinki"))
    pedido.anadir("Teclado", 2, 45.0)
    pedido.anadir("Monitor", 1, 189.0, descuento=10)
    print(len(pedido), pedido.total, len(otro), otro.total)
    print(pedido.cliente.ciudad, otro.cliente.ciudad)
    print(pedido)


if __name__ == "__main__":
    main()
