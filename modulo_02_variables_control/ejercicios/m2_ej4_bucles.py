"""Módulo 2 - Ejercicio 4: bucles."""


def factorial(n: int) -> int:
    """Devuelve el factorial de ``n`` (n >= 0) usando un bucle.

    >>> factorial(5), factorial(0)
    (120, 1)
    """
    if n < 0:
        raise ValueError("n debe ser mayor o igual que cero")
    resultado = 1
    for factor in range(2, n + 1):
        resultado *= factor
    return resultado


def es_primo(n: int) -> bool:
    """Indica si ``n`` es un número primo.

    >>> es_primo(13), es_primo(15), es_primo(1)
    (True, False, False)
    """
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def invertir(texto: str) -> str:
    """Devuelve ``texto`` del revés usando un bucle.

    >>> invertir("Python")
    'nohtyP'
    """
    resultado = ""
    for caracter in texto:
        resultado = caracter + resultado
    return resultado


def contar_vocales(texto: str) -> int:
    """Cuenta las vocales de ``texto``, sin distinguir mayúsculas ni tildes.

    >>> contar_vocales("Programación")
    5
    """
    vocales = "aeiouáéíóúü"
    contador = 0
    for caracter in texto.lower():
        if caracter in vocales:
            contador += 1
    return contador


def suma_digitos(numero: int) -> int:
    """Suma los dígitos de un entero, ignorando el signo. Usa un while.

    >>> suma_digitos(1234), suma_digitos(-905)
    (10, 14)
    """
    numero = abs(numero)
    suma = 0
    while numero > 0:
        suma += numero % 10
        numero //= 10
    return suma


def fizzbuzz(n: int) -> str:
    """Devuelve la secuencia FizzBuzz de 1 a ``n`` separada por espacios.

    Los múltiplos de 3 se sustituyen por "Fizz", los de 5 por "Buzz" y los de
    ambos por "FizzBuzz".

    >>> fizzbuzz(5)
    '1 2 Fizz 4 Buzz'
    """
    secuencia = []
    for numero in range(1, n + 1):
        if numero % 3 == 0 and numero % 5 == 0:
            secuencia.append("FizzBuzz")
        elif numero % 3 == 0:
            secuencia.append("Fizz")
        elif numero % 5 == 0:
            secuencia.append("Buzz")
        else:
            secuencia.append(str(numero))
    return " ".join(secuencia)


def tabla_multiplicar(numero: int) -> str:
    """Devuelve la tabla de multiplicar del 1 al 10, una línea por producto.

    >>> print(tabla_multiplicar(7).splitlines()[2])
    7 x  3 =  21
    """
    lineas = []
    for multiplicador in range(1, 11):
        producto = numero * multiplicador
        lineas.append(f"{numero} x {multiplicador:2} = {producto:3}")
    return "\n".join(lineas)


def primer_multiplo_comun(a: int, b: int) -> int:
    """Devuelve el mínimo común múltiplo de dos enteros positivos con un while.

    >>> primer_multiplo_comun(4, 6)
    12
    """
    if a <= 0 or b <= 0:
        raise ValueError("a y b deben ser enteros positivos")
    multiplo = max(a, b)
    while multiplo % a != 0 or multiplo % b != 0:
        multiplo += max(a, b)
    return multiplo
