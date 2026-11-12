"""Módulo 2 - Ejemplo 2: una variable es un nombre que apunta a un objeto."""

# --- Dos nombres, un solo objeto
a = [1, 2, 3]
b = a
b.append(4)
print(a)                 # [1, 2, 3, 4]: a y b son la misma lista
print(a is b)            # True
print(id(a) == id(b))    # True

# --- Para tener una copia independiente hay que pedirla
c = a.copy()
c.append(5)
print(a, c)              # a no cambia
print(a == c, a is c)    # False False

# --- Con inmutables no se nota: cada operación crea un objeto nuevo
x = 10
y = x
y += 1
print(x, y)              # 10 11

# --- Igualdad frente a identidad
lista_1 = [1, 2]
lista_2 = [1, 2]
print(lista_1 == lista_2)   # True: mismo valor
print(lista_1 is lista_2)   # False: objetos distintos

# --- Asignación múltiple e intercambio
alto, ancho = 1080, 1920
alto, ancho = ancho, alto
print(alto, ancho)

# --- Anotaciones de tipo: documentan, no obligan
edad: int = 30
nombre: str = "Lucía"

# --- Constantes: convención de mayúsculas
IVA_GENERAL = 21
MAX_INTENTOS = 3


def precio_con_iva(precio: float, iva: float = IVA_GENERAL) -> float:
    """Devuelve el precio con IVA redondeado a dos decimales."""
    return round(precio * (1 + iva / 100), 2)


print(precio_con_iva(100))
