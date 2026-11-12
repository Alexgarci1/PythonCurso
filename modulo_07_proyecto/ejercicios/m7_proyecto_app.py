"""Módulo 7 - Proyecto final: aplicación de consola del gestor de incidencias.

Este fichero es la única parte del proyecto que habla con el usuario: usa
``input`` y ``print``, captura los errores de la aplicación y decide cuándo
se guarda. Toda la lógica está en el paquete ``incidencias``.

Uso: python m7_proyecto_app.py [fichero.csv]
"""

import logging
import sys
from datetime import date
from pathlib import Path

# TODO: importa del paquete incidencias lo que necesites

logger = logging.getLogger(__name__)

RUTA_POR_DEFECTO = Path("incidencias.csv")

MENU = """
GESTOR DE INCIDENCIAS
1. Alta de incidencia
2. Listar todas
3. Listar pendientes
4. Buscar por texto
5. Cambiar estado
6. Asignar a un técnico
7. Informe
0. Guardar y salir
"""

# TODO: escribe aquí las funciones auxiliares de tu menú


def main(ruta=RUTA_POR_DEFECTO) -> int:
    """Ejecuta la aplicación. Devuelve 0 si termina bien y 1 si no puede arrancar.

    Contrato que comprueban los tests:

    1. Carga las incidencias de ``ruta``. Si lanza ``ErrorDeAlmacen``,
       imprime un mensaje que empieza por "Error:" y devuelve 1 sin pedir nada.
    2. Repite: imprime ``MENU`` y pide una opción con ``input``.
    3. Una opción que no existe imprime "Opción no válida." y vuelve al menú.
    4. Si una operación lanza ``ErrorDeIncidencias``, imprime "Error: " y el
       mensaje de la excepción, y vuelve al menú. El programa no termina.
    5. La opción 0 guarda las incidencias en ``ruta`` y devuelve 0.

    Datos que pide cada opción, en este orden y con un ``input`` por dato:

    - 1: título, solicitante y prioridad. Una prioridad vacía es "media".
         Imprime "Creada la incidencia N."
    - 4: el texto que buscar.
    - 5: el número de incidencia y el nuevo estado.
    - 6: el número de incidencia y el nombre del técnico.
    - 2, 3 y 7 no piden nada.

    Un número de incidencia que no es un entero se trata como un error de la
    aplicación: mensaje "Error: ..." y vuelta al menú, sin pedir el dato
    siguiente.
    """
    raise NotImplementedError


if __name__ == "__main__":
    logging.basicConfig(filename="incidencias.log", encoding="utf-8", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    raise SystemExit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else RUTA_POR_DEFECTO))
