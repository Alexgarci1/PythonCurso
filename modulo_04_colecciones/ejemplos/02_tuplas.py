"""Módulo 4 - Ejemplo 2: tuplas."""

punto = (3, 4)
uno = (5,)
no_es_tupla = (5)
print(type(punto).__name__, type(uno).__name__, type(no_es_tupla).__name__)

try:
    punto[0] = 10
except TypeError as error:
    print("TypeError:", error)

# --- Desempaquetado
x, y = punto
x, y = y, x                              # intercambio
print(x, y)

nombre, *apellidos = ["Ada", "Byron", "Lovelace"]
primero, *medio, ultimo = [1, 2, 3, 4, 5]
print(nombre, apellidos, primero, medio, ultimo)

empleados = [("Ada", 36, "Londres"), ("Linus", 28, "Helsinki")]
for nombre, edad, _ in empleados:        # _ para lo que no interesa
    print(f"{nombre} tiene {edad} años")

cociente, resto = divmod(17, 5)          # retorno múltiple
print(cociente, resto)

# --- Tuplas como claves de diccionario
distancias = {("Madrid", "Sevilla"): 530, ("Madrid", "Bilbao"): 400}
print(distancias[("Madrid", "Sevilla")])

try:
    {[1, 2]: "no vale"}
except TypeError as error:
    print("TypeError:", error)           # una lista no puede ser clave

# --- Inmutable no significa que su contenido lo sea
mixta = ([1, 2], 3)
mixta[0].append(99)
print(mixta)
