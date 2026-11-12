"""Módulo 6 - Ejemplo 3: captura de excepciones."""

from pathlib import Path

CARPETA_DATOS = Path(__file__).parent.parent / "datos"


def a_entero(texto, por_defecto=None):
    """EAFP: intentar la conversión y capturar el fallo."""
    try:
        return int(texto)
    except ValueError:
        return por_defecto


def primera_linea_como_numero(ruta):
    try:
        with open(ruta, encoding="utf-8") as fichero:
            valor = int(fichero.readline())
    except FileNotFoundError:
        return f"No existe {Path(ruta).name}"
    except ValueError as error:                    # as da acceso al objeto de la excepción
        return f"No es un número: {error}"
    else:
        return f"Leído {valor}"                    # solo si no ha habido excepción
    finally:
        print("  (finally se ejecuta siempre)")


def dividir_todos(valores, divisor):
    """El try protege una sola operación, no el bucle entero."""
    resultados, errores = [], []
    for valor in valores:
        try:
            resultados.append(valor / divisor)
        except TypeError:
            errores.append(valor)
    return resultados, errores


def main():
    print(a_entero("42"), a_entero("4.2"), a_entero("abc", 0))

    print(primera_linea_como_numero(CARPETA_DATOS / "no_existe.txt"))
    print(primera_linea_como_numero(CARPETA_DATOS / "notas.txt"))

    print(dividir_todos([10, "x", 4, None], 2))

    # --- La jerarquía: una clase base captura a todas sus subclases
    for accion in (lambda: [1, 2][5], lambda: {"a": 1}["b"]):
        try:
            accion()
        except LookupError as error:
            print(type(error).__name__, "es un LookupError:", error)

    print(FileNotFoundError.__mro__[1:4])
    print(issubclass(KeyError, LookupError), issubclass(KeyboardInterrupt, Exception))

    # --- El orden importa: la rama general, al final
    try:
        open(CARPETA_DATOS / "no_existe.txt", encoding="utf-8")
    except FileNotFoundError:
        print("Rama específica")
    except OSError:
        print("Rama general")

    # --- Lo que no se captura sigue subiendo
    try:
        dividir_todos([1, 2], 0)                   # ZeroDivisionError no se captura dentro
    except ZeroDivisionError as error:
        print("Ha subido hasta main:", error)


if __name__ == "__main__":
    main()
