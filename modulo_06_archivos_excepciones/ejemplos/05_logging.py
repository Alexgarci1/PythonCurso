"""Módulo 6 - Ejemplo 5: logging básico.

Prueba a cambiar el nivel de basicConfig a WARNING y a DEBUG y compara la salida.
"""

import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)          # un logger por módulo


def importar(filas):
    validas = []
    for numero, fila in enumerate(filas, start=1):
        logger.debug("Fila %d leída: %r", numero, fila)
        try:
            validas.append(int(fila))
        except ValueError:
            logger.warning("Fila %d descartada: %r no es un número", numero, fila)
    logger.info("Importadas %d filas de %d", len(validas), len(filas))
    return validas


def media(valores):
    try:
        return sum(valores) / len(valores)
    except ZeroDivisionError:
        logger.exception("No se puede calcular la media")      # incluye la traza
        return None


def main():
    with tempfile.TemporaryDirectory() as temporal:
        registro = Path(temporal) / "app.log"

        # La configuración se hace UNA vez, en el punto de entrada
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            handlers=[
                logging.StreamHandler(),                               # a la consola
                logging.FileHandler(registro, encoding="utf-8"),       # y a un fichero
            ],
        )

        logger.info("Inicio")
        valores = importar(["10", "20", "treinta", "40", ""])
        logger.info("Media: %s", media(valores))
        media([])
        logger.error("Ejemplo de error sin traza")

        logging.shutdown()
        print("--- Contenido de app.log ---")
        print(registro.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
