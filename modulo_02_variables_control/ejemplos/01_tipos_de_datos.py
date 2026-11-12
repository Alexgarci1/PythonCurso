"""Módulo 2 - Ejemplo 1: tipos de datos básicos."""

import math
from decimal import Decimal

# --- Enteros: precisión arbitraria, no desbordan
grande = 2**100
print(grande)
print(1_000_000)             # el guion bajo solo mejora la lectura
print(0b1010, 0o17, 0xFF)    # binario, octal, hexadecimal

# --- Flotantes: doble precisión IEEE 754, con sus limitaciones
print(0.1 + 0.2)                          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)                   # False
print(math.isclose(0.1 + 0.2, 0.3))       # True
print(Decimal("0.1") + Decimal("0.2"))    # 0.3 exacto, para dinero

# --- Booleanos: subclase de int
print(True + True)                        # 2
print(isinstance(True, int))              # True

# --- Cadenas: secuencias inmutables de caracteres Unicode
nombre = "Ada Lovelace"
print(len(nombre), nombre[0], nombre[-1])
print(nombre.upper())    # devuelve una cadena nueva
print(nombre)            # la original no cambia
print("Love" in nombre)

# --- None: ausencia de valor. Se compara con is
resultado = None
print(resultado is None)

# --- Conversiones explícitas
print(int("42") + 1)
print(int(3.99))         # 3: trunca
print(float("3.5"))
print(str(42) + "0")     # '420'
print(bool(0), bool(""), bool("0"), bool([]))   # False False True False

# --- Comprobar tipos
for valor in (42, 3.14, True, "hola", None):
    print(f"{valor!r:>8} -> {type(valor).__name__}")
