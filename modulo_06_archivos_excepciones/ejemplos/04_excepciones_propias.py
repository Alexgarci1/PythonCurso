"""Módulo 6 - Ejemplo 4: lanzar excepciones y definir las propias."""

import json


class ErrorDeBanco(Exception):
    """Base de todos los errores de la aplicación."""


class ImporteNoValido(ErrorDeBanco):
    pass


class SaldoInsuficiente(ErrorDeBanco):
    def __init__(self, saldo, importe):
        super().__init__(f"Saldo insuficiente: hay {saldo:.2f} y se piden {importe:.2f}")
        self.saldo = saldo
        self.importe = importe

    @property
    def falta(self):
        return round(self.importe - self.saldo, 2)


class ErrorDeConfiguracion(ErrorDeBanco):
    pass


def retirar(saldo, importe):
    if importe <= 0:
        raise ImporteNoValido(f"El importe debe ser positivo: {importe}")
    if importe > saldo:
        raise SaldoInsuficiente(saldo, importe)
    return saldo - importe


def cargar_configuracion(texto):
    """Traduce un error técnico en uno de la aplicación sin perder la causa."""
    try:
        return json.loads(texto)
    except json.JSONDecodeError as error:
        raise ErrorDeConfiguracion("La configuración no es un JSON válido") from error


def main():
    saldo = 100.0
    for importe in (30, -5, 500):
        try:
            saldo = retirar(saldo, importe)
            print(f"Retirados {importe}. Saldo: {saldo}")
        except SaldoInsuficiente as error:             # la específica, primero
            print(f"{error}. Faltan {error.falta}")    # atributos, no análisis del texto
        except ErrorDeBanco as error:                  # cualquier otro error de la aplicación
            print(f"{type(error).__name__}: {error}")

    print(cargar_configuracion('{"moneda": "EUR"}'))
    try:
        cargar_configuracion("{moneda: EUR}")
    except ErrorDeConfiguracion as error:
        print(error, "| causa:", type(error.__cause__).__name__)

    # --- raise sin argumentos vuelve a lanzar la excepción en curso
    try:
        try:
            retirar(10, 50)
        except SaldoInsuficiente:
            print("Registrado el intento fallido")
            raise
    except ErrorDeBanco as error:
        print("Vuelve a subir:", error)

    print([clase.__name__ for clase in SaldoInsuficiente.__mro__[:4]])


if __name__ == "__main__":
    main()
