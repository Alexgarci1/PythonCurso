"""Paquete de ejemplo: una tienda mínima.

El ``__init__.py`` reexporta lo más usado para que quien importe el paquete
no tenga que conocer su organización interna.
"""

from tienda.precios import aplicar_descuento, precio_con_iva

__all__ = ["aplicar_descuento", "precio_con_iva"]
