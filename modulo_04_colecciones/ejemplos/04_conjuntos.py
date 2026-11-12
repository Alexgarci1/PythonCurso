"""Módulo 4 - Ejemplo 4: conjuntos."""

backend = {"python", "java", "sql"}
datos = {"python", "sql", "r"}

# sorted() solo para que la salida sea siempre la misma: un conjunto no tiene orden
print("unión:              ", sorted(backend | datos))
print("intersección:       ", sorted(backend & datos))
print("diferencia:         ", sorted(backend - datos))
print("diferencia simétrica:", sorted(backend ^ datos))
print({"python"} <= backend, backend.isdisjoint({"go"}))

print(type({}).__name__, type(set()).__name__)       # {} es un diccionario

# --- Duplicados
correos = ["ada@x.com", "linus@x.com", "ada@x.com", "grace@x.com", "linus@x.com"]
print(len(correos), len(set(correos)))
print(list(dict.fromkeys(correos)))                  # sin duplicados y en orden
print(len(correos) != len(set(correos)))             # ¿hay duplicados?

# --- Comparar colecciones
requeridos = {"pytest", "requests", "pandas"}
instalados = {"pytest", "pip", "requests"}
print("Faltan:", sorted(requeridos - instalados))

# --- Pertenencia: misma sintaxis que en una lista, pero inmediata
bloqueados = {"spam@x.com", "robot@y.com"}
print("spam@x.com" in bloqueados)
