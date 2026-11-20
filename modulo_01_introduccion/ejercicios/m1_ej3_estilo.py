"""Módulo 1 - Ejercicio 3: código con estilo.

La función de abajo funciona, pero ignora PEP 8. Reescríbela siguiendo las
indicaciones del enunciado sin cambiar su comportamiento.
"""
DESCUENTO = 0
IVA_GENERAL = 21


def precio_final(precio, iva=IVA_GENERAL, descuento=DESCUENTO):
    """Calcula el precio con IVA después de aplicar el descuento."""
    subtotal = precio - precio * descuento / 100
    total = subtotal + subtotal * iva / 100
    return round(total, 2)
