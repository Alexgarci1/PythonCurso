"""Módulo 2 - Ejemplo 5: condicionales."""


def calificacion(nota: float) -> str:
    """Traduce una nota numérica a su calificación."""
    if nota >= 9:
        return "Sobresaliente"
    elif nota >= 7:
        return "Notable"
    elif nota >= 5:
        return "Aprobado"
    else:
        return "Suspenso"


def precio_entrada(edad: int) -> float | None:
    """Precio de una entrada. Usa cláusulas de guarda en lugar de anidar."""
    if edad < 0:
        return None
    if edad < 4:
        return 0
    if edad < 65:
        return 12
    return 8


def tipo_de_dia(dia: str) -> str:
    """Comprueba la pertenencia con in, en lugar de encadenar or."""
    return "fin de semana" if dia.lower() in ("sábado", "domingo") else "laborable"


def describir_codigo(codigo: int) -> str:
    """Ejemplo de match con alternativas y caso por defecto."""
    match codigo:
        case 200:
            return "Correcto"
        case 301 | 302:
            return "Redirección"
        case 404:
            return "No encontrado"
        case _:
            return "Otro"


if __name__ == "__main__":
    for nota in (9.5, 7, 5, 3.2):
        print(nota, calificacion(nota))

    for edad in (-1, 2, 30, 70):
        print(edad, precio_entrada(edad))

    print(tipo_de_dia("Sábado"), "|", tipo_de_dia("martes"))

    for codigo in (200, 302, 404, 500):
        print(codigo, describir_codigo(codigo))

    # Condiciones idiomáticas
    nombre = ""
    if not nombre:
        print("El nombre está vacío")

    edad = 30
    if 18 <= edad < 65:
        print("En edad laboral")
