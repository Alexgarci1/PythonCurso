"""Módulo 2 - Ejemplo 4: f-strings con formato y validación de entrada."""


def pedir_entero_positivo(mensaje: str) -> int:
    """Pide un entero positivo y repite la pregunta hasta que sea válido."""
    while True:
        texto = input(mensaje).strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("  Escribe un número entero mayor que cero.")


def mostrar_ticket(unidades: int, precio_unidad: float, iva: float = 21) -> None:
    """Imprime un ticket alineado en columnas."""
    base = unidades * precio_unidad
    cuota = base * iva / 100
    total = base + cuota

    print()
    print(f"{'Concepto':<18}{'Importe':>12}")
    print("-" * 30)
    print(f"{f'{unidades} x {precio_unidad:.2f}':<18}{base:>12.2f}")
    print(f"{f'IVA {iva:.0f} %':<18}{cuota:>12.2f}")
    print("-" * 30)
    print(f"{'TOTAL':<18}{total:>12,.2f}")


def main() -> None:
    # Formatos habituales
    print(f"{3.14159:.2f}")       # 3.14
    print(f"{1234567:,}")         # 1,234,567
    print(f"{0.256:.1%}")         # 25.6%
    print(f"{42:05d}")            # 00042
    print(f"[{'ab':<6}][{'ab':>6}][{'ab':^6}]")
    edad = 36
    print(f"{edad = }")           # edad = 36, útil para depurar

    unidades = pedir_entero_positivo("Unidades: ")
    precio = float(input("Precio por unidad: "))
    mostrar_ticket(unidades, precio)


if __name__ == "__main__":
    main()
