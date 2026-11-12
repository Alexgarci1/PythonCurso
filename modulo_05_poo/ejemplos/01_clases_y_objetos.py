"""Módulo 5 - Ejemplo 1: clases y objetos."""


class Empleado:
    """Una persona que trabaja en la empresa."""

    def __init__(self, nombre, salario=30000):
        self.nombre = nombre
        self.salario = salario

    def subir_sueldo(self, porcentaje):
        self.salario = round(self.salario * (1 + porcentaje / 100), 2)

    def salario_mensual(self):
        return round(self.salario / 12, 2)


class Saludo:
    def hola():                          # MAL: falta self
        print("hola")


def main():
    ada = Empleado("Ada", 52000)
    linus = Empleado("Linus")            # salario por defecto

    ada.subir_sueldo(10)
    print(ada.nombre, ada.salario, ada.salario_mensual())
    print(linus.nombre, linus.salario)

    # --- self es el objeto: las dos llamadas son la misma
    print(ada.salario_mensual(), Empleado.salario_mensual(ada))

    # --- Tipo e instancia
    print(type(ada).__name__, isinstance(ada, Empleado), isinstance(ada, object))

    # --- Los atributos viven en un diccionario
    print(ada.__dict__)
    ada.departamento = "IT"              # se puede, pero no se debe
    print(ada.__dict__, hasattr(linus, "departamento"))

    # --- Identidad e igualdad
    a = Empleado("Ada", 52000)
    b = Empleado("Ada", 52000)
    c = a
    print(a is c, a is b, a == b)        # True False False
    print(a)                             # sin __repr__, poco útil

    # --- Olvidar self
    try:
        Saludo().hola()
    except TypeError as error:
        print("TypeError:", error)


if __name__ == "__main__":
    main()
