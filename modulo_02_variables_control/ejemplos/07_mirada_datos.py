"""Módulo 2 - Ejemplo 7: mirada de datos.

Lo mismo que has visto en el módulo, aplicado a una serie de medidas:
valores ausentes, precisión de los flotantes y formato de cifras.
"""

import math

# Lecturas de un sensor. None marca una lectura que no llegó.
LECTURAS = [21.5, 22.1, None, 19.8, None, 23.4]


def main():
    # --- Recorrer saltando los valores ausentes
    total = 0.0
    validas = 0
    for lectura in LECTURAS:
        if lectura is None:              # None se compara con is, no con ==
            continue
        total += lectura
        validas += 1

    media = total / validas
    print(f"Lecturas válidas: {validas} de {len(LECTURAS)} ({validas / len(LECTURAS):.1%})")
    print(f"Media: {media:.2f} °C")

    # --- Los flotantes son aproximados: nunca se comparan con ==
    print(0.1 + 0.2 == 0.3)                      # False
    print(math.isclose(0.1 + 0.2, 0.3))          # True

    # --- NaN: el "valor ausente" de los datos numéricos
    nan = float("nan")
    print(nan == nan)                            # False: NaN no es igual ni a sí mismo
    print(math.isnan(nan))                       # True: así se pregunta

    # --- Formato de cifras para un informe
    ingresos = 1234567.891
    print(f"{ingresos:,.2f}")                    # 1,234,567.89
    print(f"{ingresos:.3e}")                     # 1.235e+06
    print(f"{0.0734:.1%}")                       # 7.3%


if __name__ == "__main__":
    main()
