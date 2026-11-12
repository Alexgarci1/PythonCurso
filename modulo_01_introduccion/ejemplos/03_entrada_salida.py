"""Módulo 1 - Ejemplo 3: entrada y salida.

input() siempre devuelve una cadena. Para operar hay que convertirla.
"""


def main():
    nombre = input("¿Cómo te llamas? ")
    anio_nacimiento = int(input("¿En qué año naciste? "))
    horas_semana = float(input("¿Cuántas horas programas a la semana? "))

    edad_aproximada = 2026 - anio_nacimiento

    # print acepta varios argumentos y los separa con un espacio.
    print("Hola,", nombre)

    # sep y end cambian el separador y el final de línea.
    print("Python", "Java", "C#", sep=" | ")
    print("Cargando", end="...\n")

    # Las f-strings permiten incrustar expresiones y dar formato.
    print(f"{nombre}, tienes unos {edad_aproximada} años")
    print(f"Programas {horas_semana:.1f} horas a la semana")
    print(f"Eso son {horas_semana * 52:,.0f} horas al año")
    print(f"{'Concepto':<12}{'Valor':>8}")
    print(f"{'Semana':<12}{horas_semana:>8.1f}")
    print(f"{'Año':<12}{horas_semana * 52:>8.1f}")


if __name__ == "__main__":
    main()
