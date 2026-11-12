"""Módulo 3 - Ejemplo 3: ámbito de variables, cierres y lambdas."""

IVA = 21                 # constante de módulo: se lee desde cualquier función
visitas = 0


def precio_final(precio):
    return precio * (1 + IVA / 100)      # leer una global no necesita nada


def registrar_visita_mal():
    visitas += 1                         # UnboundLocalError: asignar la hace local


def registrar_visita_con_global():
    global visitas                       # funciona, pero es estado oculto
    visitas += 1


def registrar_visita(contador):
    return contador + 1                  # mejor: entra un valor, sale otro


def exterior():
    mensaje = "envolvente"

    def interior():
        return mensaje                   # se busca en L, luego en E

    return interior()


def crear_multiplicador(factor):
    def multiplicar(numero):
        return numero * factor           # cierre: recuerda factor

    return multiplicar


def crear_contador():
    cuenta = 0

    def siguiente():
        nonlocal cuenta                  # modifica la variable envolvente
        cuenta += 1
        return cuenta

    return siguiente


def main():
    global visitas

    print(precio_final(100))

    try:
        registrar_visita_mal()
    except UnboundLocalError as error:
        print("UnboundLocalError:", error)

    registrar_visita_con_global()
    visitas = registrar_visita(visitas)
    print("Visitas:", visitas)

    print(exterior())

    # --- Los bloques no crean ámbito
    for i in range(3):
        ultimo = i
    print(i, ultimo)                     # 2 2

    # --- Cierres
    triple = crear_multiplicador(3)
    print(triple(10))
    contador = crear_contador()
    otro = crear_contador()              # cada cierre tiene su propio estado
    print(contador(), contador(), contador(), otro())

    # --- Lambdas como criterio de ordenación
    palabras = ["kiwi", "manzana", "uva"]
    print(sorted(palabras, key=len))
    print(sorted(palabras, key=lambda palabra: palabra[-1]))

    empleados = [("Ada", 36), ("Linus", 28), ("Grace", 45)]
    print(max(empleados, key=lambda empleado: empleado[1]))
    print(sorted(empleados, key=lambda empleado: empleado[1], reverse=True))


if __name__ == "__main__":
    main()
