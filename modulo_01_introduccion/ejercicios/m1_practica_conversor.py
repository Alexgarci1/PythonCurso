"""Módulo 1 - Práctica 1: conversor de unidades.

Lee el enunciado en PRACTICA_1.md.
"""

KM_POR_MILLA = 1.609344
KG_POR_LIBRA = 0.45359237


def celsius_a_fahrenheit(grados):
    """Convierte grados Celsius a Fahrenheit."""
    return grados * 9 / 5 + 32


def fahrenheit_a_celsius(grados):
    """Convierte grados Fahrenheit a Celsius."""
    return (grados - 32) * 5 / 9


def km_a_millas(km):
    """Convierte kilómetros a millas."""
    return km / KM_POR_MILLA


def millas_a_km(millas):
    """Convierte millas a kilómetros."""
    return millas * KM_POR_MILLA


def kg_a_libras(kg):
    """Convierte kilogramos a libras."""
    return kg / KG_POR_LIBRA


def libras_a_kg(libras):
    """Convierte libras a kilogramos."""
    return libras * KG_POR_LIBRA


def formatear(valor, unidad_origen, resultado, unidad_destino):
    """Devuelve el texto de la conversión con dos decimales.

    >>> formatear(100, "°C", 212.0, "°F")
    '100.00 °C = 212.00 °F'
    """
    return (
        f"{valor:.2f} {unidad_origen} = "
        f"{resultado:.2f} {unidad_destino}"
    )


def main():
    """Muestra el menú, pide los datos e imprime el resultado."""
    print(
        "Conversor de unidades\n"
        "1. Celsius a Fahrenheit\n"
        "2. Fahrenheit a Celsius\n"
        "3. Kilómetros a millas\n"
        "4. Millas a kilómetros\n"
        "5. Kilogramos a libras\n"
        "6. Libras a kilogramos"
    )
    opcion = input("Elige una opción (1-6): ")

    if opcion not in ("1", "2", "3", "4", "5", "6"):
        print("Opción no válida")
        return

    valor = float(input("Valor a convertir: "))

    if opcion == "1":
        unidad_origen, unidad_destino = "°C", "°F"
        resultado = celsius_a_fahrenheit(valor)
    elif opcion == "2":
        unidad_origen, unidad_destino = "°F", "°C"
        resultado = fahrenheit_a_celsius(valor)
    elif opcion == "3":
        unidad_origen, unidad_destino = "km", "mi"
        resultado = km_a_millas(valor)
    elif opcion == "4":
        unidad_origen, unidad_destino = "mi", "km"
        resultado = millas_a_km(valor)
    elif opcion == "5":
        unidad_origen, unidad_destino = "kg", "lb"
        resultado = kg_a_libras(valor)
    else:
        unidad_origen, unidad_destino = "lb", "kg"
        resultado = libras_a_kg(valor)

    print(formatear(valor, unidad_origen, resultado, unidad_destino))


if __name__ == "__main__":
    main()
