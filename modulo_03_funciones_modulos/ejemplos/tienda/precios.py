"""Cálculo de precios."""

IVA_GENERAL = 21


def precio_con_iva(precio: float, iva: float = IVA_GENERAL) -> float:
    """Devuelve el precio con el IVA aplicado, redondeado a dos decimales."""
    return round(precio * (1 + iva / 100), 2)


def aplicar_descuento(precio: float, porcentaje: float) -> float:
    """Devuelve el precio tras aplicar un descuento en porcentaje."""
    return round(precio * (1 - porcentaje / 100), 2)

