"""Módulo 5 - Ejemplo 2: atributos de clase, tipos de método y métodos especiales."""


class Empleado:
    SALARIO_MINIMO = 16576               # atributo de clase: constante compartida
    plantilla = 0

    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario
        Empleado.plantilla += 1

    def salario_mensual(self):
        return round(self.salario / 12, 2)

    @classmethod
    def desde_texto(cls, texto):
        """Constructor alternativo: Empleado.desde_texto("Ada; 52000")."""
        nombre, salario = texto.split(";")
        return cls(nombre.strip(), float(salario))

    @staticmethod
    def es_salario_valido(salario):
        return salario >= Empleado.SALARIO_MINIMO

    def __repr__(self):
        return f"Empleado({self.nombre!r}, {self.salario!r})"


class Dinero:
    def __init__(self, cantidad, moneda="EUR"):
        self.cantidad = cantidad
        self.moneda = moneda

    def __repr__(self):
        return f"Dinero({self.cantidad!r}, {self.moneda!r})"

    def __str__(self):
        return f"{self.cantidad:.2f} {self.moneda}"

    def __eq__(self, otro):
        if not isinstance(otro, Dinero):
            return NotImplemented
        return (self.cantidad, self.moneda) == (otro.cantidad, otro.moneda)

    def __lt__(self, otro):
        return self.cantidad < otro.cantidad

    def __add__(self, otro):
        return Dinero(round(self.cantidad + otro.cantidad, 2), self.moneda)


class Equipo:
    """Un contenedor propio que se comporta como uno integrado."""

    def __init__(self, nombre):
        self.nombre = nombre
        self._miembros = []

    def anadir(self, empleado):
        self._miembros.append(empleado)

    def __len__(self):
        return len(self._miembros)

    def __contains__(self, nombre):
        return any(miembro.nombre == nombre for miembro in self._miembros)

    def __iter__(self):
        return iter(self._miembros)


def main():
    ada = Empleado("Ada", 52000)
    linus = Empleado.desde_texto("Linus; 48000")
    print(ada, linus, Empleado.plantilla)
    print(Empleado.es_salario_valido(12000), ada.SALARIO_MINIMO)

    # --- Asignar a través del objeto crea un atributo de instancia
    ada.SALARIO_MINIMO = 1
    print(ada.SALARIO_MINIMO, linus.SALARIO_MINIMO, Empleado.SALARIO_MINIMO)

    # --- Métodos especiales
    precio = Dinero(19.9)
    print(precio)                                # __str__
    print([precio], repr(precio))                # __repr__
    print(precio == Dinero(19.9), precio == 19.9)
    print(precio + Dinero(0.1))                  # __add__
    print(sorted([Dinero(5), Dinero(2), Dinero(9)]))     # __lt__
    print(max(Dinero(5), Dinero(2)))

    # --- Contenedor
    equipo = Equipo("Plataforma")
    equipo.anadir(ada)
    equipo.anadir(linus)
    print(len(equipo), "Ada" in equipo, "Grace" in equipo)
    print([miembro.nombre for miembro in equipo])
    print(sum(miembro.salario for miembro in equipo))


if __name__ == "__main__":
    main()
