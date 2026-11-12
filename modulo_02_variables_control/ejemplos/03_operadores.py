"""Módulo 2 - Ejemplo 3: operadores."""

# --- Aritméticos
print(7 / 2)          # 3.5  división real, siempre float
print(8 / 2)          # 4.0
print(7 // 2)         # 3    división entera
print(-7 // 2)        # -4   redondea hacia abajo (en Java sería -3)
print(7 % 2)          # 1
print(-7 % 2)         # 1    signo del divisor (en Java sería -1)
print(2**10)          # 1024
print(divmod(17, 5))  # (3, 2)

# --- Comparaciones encadenadas
edad = 25
print(18 <= edad < 65)

# --- Lógicos con palabras y en cortocircuito
tiene_entrada = True
print(edad >= 18 and tiene_entrada)
print(not tiene_entrada or edad > 80)

# and y or devuelven uno de sus operandos, no necesariamente un bool
print("Ada" or "Anónimo")   # 'Ada'
print("" or "Anónimo")      # 'Anónimo'
print(0 and 10 / 0)         # 0: la división no llega a evaluarse

# --- Valores falsos
for valor in (0, 0.0, "", [], {}, None, False):
    print(f"{valor!r:>6} es falso: {not valor}")

# --- Identidad y pertenencia
resultado = None
print(resultado is None)
print("py" in "python")
print(3 in (1, 2, 3))
print("z" not in "python")

# --- Expresión condicional
estado = "adulto" if edad >= 18 else "menor"
print(estado)
