"""Módulo 3 - Ejemplo 4: uso de un paquete propio.

Ejecuta este fichero desde su carpeta para que Python encuentre ``tienda``:

    cd modulo_03_funciones_modulos/ejemplos
    python 04_usar_paquete.py
"""

import sys

import tienda
import tienda.inventario as inventario
from tienda import aplicar_descuento             # reexportado en __init__.py
from tienda.precios import IVA_GENERAL


def main():
    print("Paquete:", tienda.__name__, "| exporta:", tienda.__all__)
    print("IVA general:", IVA_GENERAL)

    for producto in inventario.productos():
        precio = inventario.precio_venta(producto)
        estado = "disponible" if inventario.hay_existencias(producto) else "agotado"
        print(f"{producto:<10}{precio:>8.2f} €  {estado}")

    print("Monitor rebajado:", aplicar_descuento(inventario.precio_venta("monitor"), 10))

    # --- Dónde busca Python los módulos: la primera entrada es esta carpeta
    print("Primera entrada de sys.path:", sys.path[0])
    print("__name__ de este fichero:", __name__)
    print("__name__ del módulo importado:", inventario.__name__)


if __name__ == "__main__":
    main()
