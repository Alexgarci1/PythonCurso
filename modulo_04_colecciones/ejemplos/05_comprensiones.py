"""Módulo 4 - Ejemplo 5: comprensiones."""

nombres = ["ada", "linus", "grace", "alan", "guido"]

# --- De bucle a comprensión
cuadrados = []
for n in range(6):
    cuadrados.append(n ** 2)
print(cuadrados, [n ** 2 for n in range(6)])

# --- Transformar, filtrar y las dos cosas
print([nombre.capitalize() for nombre in nombres])
print([nombre for nombre in nombres if len(nombre) > 4])
print([nombre.upper() for nombre in nombres if nombre.startswith("g")])
print(["par" if n % 2 == 0 else "impar" for n in range(4)])

# --- Diccionario y conjunto
print({nombre: len(nombre) for nombre in nombres})
print(sorted({nombre[0] for nombre in nombres}))

precios = {"teclado": 45.0, "raton": 19.9, "monitor": 189.0}
print({producto: precio for producto, precio in precios.items() if precio > 40})
print({precio: producto for producto, precio in precios.items()})

# --- Expresiones generadoras: sin lista intermedia
numeros = [3, -1, 4, -1, 5]
print(sum(n * n for n in numeros))
print(any(n < 0 for n in numeros), all(n < 10 for n in numeros))
print(", ".join(str(n) for n in numeros))

# --- Anidadas
matriz = [[1, 2, 3], [4, 5, 6]]
print([valor for fila in matriz for valor in fila])
print([[fila[i] for fila in matriz] for i in range(3)])
