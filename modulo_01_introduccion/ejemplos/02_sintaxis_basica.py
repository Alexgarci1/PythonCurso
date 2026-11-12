"""Módulo 1 - Ejemplo 2: sintaxis básica.

Indentación, variables, comentarios y consulta de tipos.
"""

# Una variable se crea al asignarla. No se declara el tipo.
nombre = "Lucía"
edad = 30
altura = 1.68
es_alumna = True
proyecto_asignado = None

# type() dice de qué tipo es cada valor.
print(type(nombre))             # <class 'str'>
print(type(edad))               # <class 'int'>
print(type(altura))             # <class 'float'>
print(type(es_alumna))          # <class 'bool'>
print(type(proyecto_asignado))  # <class 'NoneType'>

# El tipo pertenece al valor: la misma variable puede apuntar a otro tipo.
dato = 10
print(dato, type(dato))
dato = "diez"
print(dato, type(dato))

# Los bloques se delimitan con dos puntos y sangría de 4 espacios.
if edad >= 18:
    print(f"{nombre} es mayor de edad")
    if es_alumna:
        print("Y además está matriculada en el curso")
else:
    print(f"{nombre} es menor de edad")

# Tipado fuerte: Python no convierte tipos por su cuenta.
# print("Edad: " + edad)       # TypeError: no se puede sumar str e int
print("Edad: " + str(edad))     # conversión explícita
print(f"Edad: {edad}")          # forma idiomática

# Una sentencia larga se parte dentro de paréntesis.
total = (
    100
    + 250
    + 75
)
print(f"Total: {total}")

# Las constantes se escriben en mayúsculas por convención.
IVA_GENERAL = 21
precio = 50
print(f"Precio con IVA: {precio * (1 + IVA_GENERAL / 100):.2f} €")
