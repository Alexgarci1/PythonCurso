"""Módulo 3 - Ejemplo 2: parámetros y retorno."""


def crear_cuenta(titular, saldo=0, moneda="EUR"):
    return f"{titular}: {saldo} {moneda}"


def anadir_mal(elemento, lista=[]):          # MAL: valor por defecto mutable
    lista.append(elemento)
    return lista


def anadir_bien(elemento, lista=None):       # BIEN
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista


def sumar(*numeros):
    """Acepta cualquier cantidad de argumentos posicionales."""
    total = 0
    for numero in numeros:
        total += numero
    return total


def crear_etiqueta(nombre, **atributos):
    """Acepta cualquier cantidad de argumentos por nombre."""
    partes = [f'{clave}="{valor}"' for clave, valor in atributos.items()]
    return f"<{nombre} {' '.join(partes)}>"


def exportar(datos, *, comprimir=False, sobrescribir=False):
    """Los parámetros que siguen al * solo se pueden pasar por nombre."""
    return f"{len(datos)} registros, comprimir={comprimir}, sobrescribir={sobrescribir}"


def minimo_y_maximo(numeros):
    """Devuelve dos valores: en realidad, una tupla."""
    return min(numeros), max(numeros)


def reasignar(lista):
    lista = [0]                # el nombre local apunta a otro objeto


def modificar(lista):
    lista.append(0)            # se modifica el objeto compartido


def main():
    # --- Posicionales, por nombre y valores por defecto
    print(crear_cuenta("Ada"))
    print(crear_cuenta("Ada", 100))
    print(crear_cuenta("Ada", moneda="USD"))
    print(crear_cuenta(moneda="GBP", titular="Grace", saldo=50))

    # --- El error del valor por defecto mutable
    print(anadir_mal(1), anadir_mal(2))      # [1, 2] [1, 2]: la misma lista
    print(anadir_bien(1), anadir_bien(2))    # [1] [2]
    print(anadir_mal.__defaults__)           # ahí está guardada la lista

    # --- *args y **kwargs
    print(sumar(), sumar(1, 2, 3))
    print(crear_etiqueta("a", href="/inicio", title="Inicio"))

    # --- Desempaquetado en la llamada
    valores = [10, 20, 30]
    print(sumar(*valores))
    opciones = {"saldo": 500, "moneda": "USD"}
    print(crear_cuenta("Linus", **opciones))

    # --- Solo por nombre
    print(exportar([1, 2, 3], comprimir=True))
    try:
        exportar([1, 2, 3], True)
    except TypeError as error:
        print("TypeError:", error)

    # --- Retorno múltiple
    menor, mayor = minimo_y_maximo([4, 8, 15, 16, 23, 42])
    print(menor, mayor)

    # --- Paso de argumentos
    numeros = [1, 2]
    reasignar(numeros)
    print(numeros)             # [1, 2]
    modificar(numeros)
    print(numeros)             # [1, 2, 0]


if __name__ == "__main__":
    main()
