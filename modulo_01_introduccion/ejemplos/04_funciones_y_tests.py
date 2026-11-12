"""Módulo 1 - Ejemplo 4: una función sencilla y su test.

Los ejercicios del curso se comprueban con tests. Un test llama a tu función
y afirma, con assert, que devuelve lo esperado.

Ejecútalo como script:      python ejemplos/04_funciones_y_tests.py
Ejecútalo como test:        pytest ejemplos/04_funciones_y_tests.py
"""

IVA_GENERAL = 21


def precio_con_iva(precio, iva=IVA_GENERAL):
    """Devuelve el precio con el IVA aplicado, redondeado a dos decimales."""
    return round(precio * (1 + iva / 100), 2)


# pytest ejecuta las funciones cuyo nombre empieza por test_
def test_precio_con_iva_general():
    assert precio_con_iva(100) == 121.0


def test_precio_con_iva_reducido():
    assert precio_con_iva(100, iva=10) == 110.0


def main():
    precio = float(input("Precio sin IVA: "))
    print(f"Precio final: {precio_con_iva(precio):.2f} €")


if __name__ == "__main__":
    main()
