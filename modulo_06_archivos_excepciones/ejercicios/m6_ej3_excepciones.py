"""Módulo 6 - Ejercicio 3: excepciones."""


def a_entero(texto, por_defecto=None):
    """Convierte a entero con ``int()``. Si no se puede, devuelve ``por_defecto``.

    Es la versión con ``try``/``except`` de la función del módulo 2. Tiene que
    funcionar también si ``texto`` es ``None``.

    >>> a_entero("42"), a_entero("abc"), a_entero(None, 0)
    (42, None, 0)
    """
    raise NotImplementedError


def dividir(a: float, b: float) -> float | None:
    """Devuelve ``a / b``, o ``None`` si ``b`` es cero.

    Solo captura la división por cero: cualquier otro error tiene que subir.
    """
    raise NotImplementedError


def leer_o_vacio(ruta) -> str:
    """Devuelve el contenido del fichero, o la cadena vacía si no existe."""
    raise NotImplementedError


def validar_edad(edad) -> int:
    """Devuelve la edad si es válida y, si no, lanza una excepción.

    - ``TypeError`` si no es un ``int`` (un ``bool`` tampoco vale).
    - ``ValueError`` si no está entre 0 y 130, ambos incluidos. El mensaje
      tiene que contener el valor recibido.

    >>> validar_edad(36)
    36
    """
    raise NotImplementedError


# TODO: define aquí las excepciones ErrorDeCuenta, ImporteNoValido y SaldoInsuficiente


def retirar(saldo: float, importe: float) -> float:
    """Devuelve el saldo que queda tras retirar el importe.

    Lanza ``ImporteNoValido`` si el importe no es positivo y
    ``SaldoInsuficiente`` si supera el saldo.

    >>> retirar(100, 30)
    70
    """
    raise NotImplementedError


def convertir_todos(textos: list[str]) -> tuple[list[float], list[str]]:
    """Convierte cada texto a ``float`` y separa los que no se pueden convertir.

    Devuelve una tupla (números, textos rechazados). Un texto no válido no
    interrumpe el proceso de los siguientes.

    >>> convertir_todos(["1.5", "x", "2"])
    ([1.5, 2.0], ['x'])
    """
    raise NotImplementedError


def ejecutar(accion, registro: list[str]):
    """Llama a ``accion()`` anotando lo que ocurre en la lista ``registro``.

    Añade "inicio" antes de llamar; después "ok" si termina bien o "error"
    si lanza cualquier excepción; y "fin" en todos los casos. Devuelve lo que
    devuelva la acción. Si la acción falla, la excepción tiene que seguir
    subiendo después de anotar "error" y "fin".
    """
    raise NotImplementedError


# TODO: define aquí la excepción ErrorDeConfiguracion


def puerto_configurado(configuracion: dict) -> int:
    """Devuelve el puerto de la configuración como entero.

    Si falta la clave "puerto" o su valor no se puede convertir a entero,
    lanza ``ErrorDeConfiguracion`` encadenada con la excepción original
    mediante ``raise ... from``.

    >>> puerto_configurado({"puerto": "8080"})
    8080
    """
    raise NotImplementedError
