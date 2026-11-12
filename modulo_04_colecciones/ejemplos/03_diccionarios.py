"""Módulo 4 - Ejemplo 3: diccionarios."""

from collections import Counter, defaultdict

empleado = {"nombre": "Ada", "edad": 36, "activo": True}

# --- Acceso
print(empleado["nombre"], empleado.get("salario"), empleado.get("salario", 0))
print("edad" in empleado, "Ada" in empleado)     # in comprueba claves

# --- Modificación
empleado["salario"] = 42000
empleado.update({"edad": 37, "ciudad": "Madrid"})
ciudad = empleado.pop("ciudad")
print(empleado, ciudad)
print({"a": 1, "b": 2} | {"b": 20, "c": 3})

# --- Recorrido
precios = {"teclado": 45.0, "raton": 19.9, "monitor": 189.0}
for producto, precio in precios.items():
    print(f"{producto:<10}{precio:>8.2f} €")
print(list(precios), list(precios.values()), sum(precios.values()))

# --- Contar
texto = "el gato y el perro y el loro"
conteo = {}
for palabra in texto.split():
    conteo[palabra] = conteo.get(palabra, 0) + 1
print(conteo)
print(Counter(texto.split()).most_common(2))

# --- Agrupar
empleados = [("Ada", "IT"), ("Grace", "IT"), ("Linus", "Ventas")]
por_departamento = {}
for nombre, departamento in empleados:
    por_departamento.setdefault(departamento, []).append(nombre)
print(por_departamento)

agrupados = defaultdict(list)
for nombre, departamento in empleados:
    agrupados[departamento].append(nombre)
print(dict(agrupados))

# --- Anidados: la forma de un JSON
pedido = {
    "id": 1042,
    "cliente": {"nombre": "Ada", "ciudad": "Madrid"},
    "lineas": [
        {"producto": "teclado", "unidades": 2, "precio": 45.0},
        {"producto": "raton", "unidades": 1, "precio": 19.9},
    ],
}
print(pedido["cliente"]["ciudad"], pedido["lineas"][0]["producto"])
print(pedido.get("descuento", {}).get("codigo"))
total = sum(linea["unidades"] * linea["precio"] for linea in pedido["lineas"])
print(f"Total del pedido: {total:.2f} €")
