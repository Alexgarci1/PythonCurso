"""Validación y normalización de textos."""

LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"


def esta_vacio(texto: str | None) -> bool:
    """Indica si el texto es ``None``, está vacío o solo contiene espacios.

    >>> esta_vacio("   ")
    True
    >>> esta_vacio(" a ")
    False
    """
    return texto is None or texto.strip() == ""


def normalizar_nombre(nombre: str) -> str:
    """Quita los espacios sobrantes y pone en mayúscula la inicial de cada palabra.

    >>> normalizar_nombre("  ada   LOVELACE ")
    'Ada Lovelace'
    """
    return " ".join(palabra.capitalize() for palabra in nombre.split())


def es_email(texto: str) -> bool:
    """Comprueba de forma sencilla que el texto tiene forma de correo.

    Reglas: no contiene espacios, tiene exactamente una arroba, hay texto
    antes de la arroba, y el dominio contiene al menos un punto que no está
    ni al principio ni al final.

    >>> es_email("ada@ejemplo.com")
    True
    >>> es_email("ada@ejemplo")
    False
    """
    if " " in texto or texto.count("@") != 1:
        return False

    antes, dominio = texto.split("@")
    return bool(antes) and "." in dominio and not dominio.startswith(".") and not dominio.endswith(".")


def es_dni(texto: str) -> bool:
    """Comprueba que el texto es un DNI válido: ocho dígitos y la letra correcta.

    La letra se obtiene tomando el resto de dividir el número entre 23 y
    usándolo como posición en ``LETRAS_DNI``. Admite la letra en minúscula y
    espacios alrededor.

    >>> es_dni("12345678Z")
    True
    >>> es_dni("12345678A")
    False
    """
    texto = texto.strip()
    if len(texto) != 9 or not texto[:8].isdigit() or not texto[8].isalpha():
        return False

    numero = int(texto[:8])
    return texto[8].upper() == LETRAS_DNI[numero % 23]


def es_telefono(texto: str) -> bool:
    """Comprueba un teléfono español de nueve dígitos."""
    if texto is None:
        return False

    numero = texto.strip().replace(" ", "")
    return (
        len(numero) == 9
        and numero.isdigit()
        and numero[0] in "6789"
    )


def es_iban(texto: str) -> bool:
    """Comprueba la estructura y los dígitos de control de un IBAN español."""
    if texto is None:
        return False

    iban = texto.strip().upper().replace(" ", "")
    if len(iban) != 24 or not iban.startswith("ES") or not iban[2:].isdigit():
        return False

    reorganizado = iban[4:] + iban[:4]
    convertido = "".join(str(ord(letra) - 55) if letra.isalpha() else letra
                         for letra in reorganizado)
    return int(convertido) % 97 == 1
