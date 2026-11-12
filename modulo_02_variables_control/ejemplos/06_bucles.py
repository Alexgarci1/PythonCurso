"""Módulo 2 - Ejemplo 6: bucles."""

lenguajes = ["Python", "Java", "C#"]

# --- for recorre elementos
for lenguaje in lenguajes:
    print(lenguaje)

# --- Con posición: enumerate, no range(len(...))
for posicion, lenguaje in enumerate(lenguajes, start=1):
    print(f"{posicion}. {lenguaje}")

# --- range genera enteros sin crear una lista
print(list(range(5)))            # [0, 1, 2, 3, 4]
print(list(range(2, 6)))         # [2, 3, 4, 5]
print(list(range(0, 10, 2)))     # [0, 2, 4, 6, 8]
print(list(range(5, 0, -1)))     # [5, 4, 3, 2, 1]

# --- Acumulador
total = 0
for numero in range(1, 101):
    total += numero
print(total, sum(range(1, 101)))  # 5050 con bucle y con la función integrada

# --- while: no se sabe cuántas vueltas habrá
numero = 27
pasos = 0
while numero != 1:               # conjetura de Collatz
    numero = numero // 2 if numero % 2 == 0 else 3 * numero + 1
    pasos += 1
print(f"Collatz(27) llega a 1 en {pasos} pasos")

# --- break y continue
for numero in range(1, 11):
    if numero % 2 == 0:
        continue                 # se salta los pares
    if numero > 7:
        break                    # se detiene al pasar de 7
    print(numero, end=" ")
print()


# --- else de bucle: se ejecuta si no hubo break
def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            break
    else:
        return True
    return False


print([n for n in range(30) if es_primo(n)])

# --- Bucles anidados: tabla de multiplicar
for fila in range(1, 6):
    for columna in range(1, 6):
        print(f"{fila * columna:>4}", end="")
    print()
