"""Consulta del inventario."""

from .precios import precio_con_iva      # importación relativa a un módulo vecino

_EXISTENCIAS = {                          # el guion bajo indica «uso interno»
    "teclado": (45.0, 12),
    "raton": (19.9, 0),
    "monitor": (189.0, 4),
}


def hay_existencias(producto: str) -> bool:
    """Indica si queda alguna unidad del producto."""
    return producto in _EXISTENCIAS and _EXISTENCIAS[producto][1] > 0


def precio_venta(producto: str) -> float:
    """Devuelve el precio de venta al público, con IVA."""
    precio, _ = _EXISTENCIAS[producto]
    return precio_con_iva(precio)


def productos() -> list[str]:
    """Devuelve los nombres de los productos en orden alfabético."""
    return sorted(_EXISTENCIAS)
