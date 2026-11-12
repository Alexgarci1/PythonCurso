"""Módulo 5 - Ejemplo 4: polimorfismo, duck typing y protocolos."""

from typing import Protocol


class Correo:
    def enviar(self, destinatario, mensaje):
        return f"Correo a {destinatario}: {mensaje}"


class Sms:
    LIMITE = 20

    def enviar(self, destinatario, mensaje):
        return f"SMS a {destinatario}: {mensaje[:self.LIMITE]}"


class CanalDePrueba:
    """Un doble para tests: guarda lo enviado en lugar de enviarlo."""

    def __init__(self):
        self.enviados = []

    def enviar(self, destinatario, mensaje):
        self.enviados.append((destinatario, mensaje))
        return "registrado"


class Canal(Protocol):
    """Lo que avisar() espera de un canal. Nadie hereda de esta clase."""

    def enviar(self, destinatario: str, mensaje: str) -> str: ...


def avisar(canales: list[Canal], destinatario: str, mensaje: str) -> list[str]:
    # No se pregunta de qué clase es cada canal: se le pide que envíe
    return [canal.enviar(destinatario, mensaje) for canal in canales]


class Mazo:
    """Duck typing con el propio lenguaje: basta con __len__ y __getitem__."""

    def __init__(self):
        self._cartas = [f"{valor}{palo}" for palo in "♠♥" for valor in ("A", "K", "Q")]

    def __len__(self):
        return len(self._cartas)

    def __getitem__(self, posicion):
        return self._cartas[posicion]


def main():
    prueba = CanalDePrueba()
    for resultado in avisar([Correo(), Sms(), prueba], "Ada", "Reunión de equipo a las 10:00"):
        print(resultado)
    print(prueba.enviados)

    try:
        avisar([Correo(), "no soy un canal"], "Ada", "hola")
    except AttributeError as error:
        print("AttributeError:", error)          # el error aparece al usarlo

    # --- len(), indexado, slicing, for, in y sorted funcionan con Mazo
    mazo = Mazo()
    print(len(mazo), mazo[0], mazo[-2:], "K♥" in mazo)
    print(sorted(mazo), [carta for carta in mazo if carta.startswith("A")])

    # --- Lo que ya usabas: el mismo código con tipos distintos
    for coleccion in ([1, 2, 3], "abc", {"x": 1}, (4, 5), range(3), mazo):
        print(type(coleccion).__name__, len(coleccion), list(coleccion)[:2])


if __name__ == "__main__":
    main()
