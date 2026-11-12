"""Módulo 4 - Ejemplo 6: iteración y funciones integradas."""

lenguajes = ["Python", "Java", "C#"]
anios = [1991, 1995, 2000]

for posicion, lenguaje in enumerate(lenguajes, start=1):
    print(posicion, lenguaje)

for lenguaje, anio in zip(lenguajes, anios):
    print(f"{lenguaje} nació en {anio}")

print(dict(zip(lenguajes, anios)))

# --- zip se detiene en la colección más corta
print(list(zip([1, 2, 3], "ab")))
try:
    list(zip([1, 2, 3], "ab", strict=True))
except ValueError as error:
    print("ValueError:", error)

# --- Los iteradores se agotan
pares = zip([1, 2], ["a", "b"])
print(list(pares), list(pares))

# --- Funciones de resumen
notas = [7.5, 4.0, 9.0, 6.5]
print(len(notas), sum(notas), min(notas), max(notas), sum(notas) / len(notas))
print(any(nota < 5 for nota in notas), all(nota >= 5 for nota in notas))
print(max([], default=0))

# --- key en sorted, min y max
palabras = ["kiwi", "Manzana", "uva"]
print(sorted(palabras))
print(sorted(palabras, key=str.lower))
print(sorted(palabras, key=len, reverse=True))
print(max(palabras, key=len), min(palabras, key=len))

# --- map y filter existen, pero se prefieren las comprensiones
print(list(map(str.upper, lenguajes)), [lenguaje.upper() for lenguaje in lenguajes])
print(list(reversed(lenguajes)))
