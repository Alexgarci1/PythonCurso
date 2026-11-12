"""Módulo 6 - Práctica 6: importador de ventas en CSV.

Lee un CSV de ventas, valida cada fila, registra las que no valen y exporta
un resumen por región.
"""

import csv
import logging
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

CAMPOS = ["fecha", "vendedor", "region", "producto", "categoria", "unidades", "precio"]
CAMPOS_RESUMEN = ["region", "ventas", "unidades", "importe"]


# TODO: define aquí las excepciones ErrorDeImportacion, FicheroNoValido y FilaNoValida


def validar_fila(fila: dict) -> dict:
    """Devuelve la venta de una fila con los tipos convertidos.

    Recibe un diccionario de cadenas y devuelve uno NUEVO con los mismos
    campos sin espacios alrededor, ``unidades`` como ``int`` y ``precio``
    como ``float``. Lanza ``FilaNoValida`` con uno de estos mensajes,
    comprobados en este orden:

    - "falta el campo <nombre>" si algún campo de ``CAMPOS`` está vacío
    - "fecha no válida: <valor>" si la fecha no es una fecha ISO
    - "unidades no válidas: <valor>" si no es un entero mayor que cero
    - "precio no válido: <valor>" si no es un número mayor que cero
    """
    raise NotImplementedError


def importar_ventas(ruta) -> tuple[list[dict], list[str]]:
    """Lee el CSV y devuelve una tupla (ventas válidas, errores).

    Cada error es un texto "Línea N: motivo", donde N es el número de línea
    en el fichero (la cabecera es la línea 1) y el motivo es el mensaje de
    ``FilaNoValida``. Por cada fila descartada se registra además un aviso
    con ``logger.warning``.

    Lanza ``FicheroNoValido``:

    - "No existe el fichero <ruta>" si no se encuentra, encadenada con el
      ``FileNotFoundError`` original
    - "Faltan columnas: <nombres separados por coma y espacio>" si a la
      cabecera le falta alguna de ``CAMPOS``, en el orden de ``CAMPOS``
    """
    raise NotImplementedError


def resumen_por_region(ventas: list[dict]) -> list[dict]:
    """Agrupa las ventas por región.

    Devuelve una lista de diccionarios con las claves de ``CAMPOS_RESUMEN``:
    la región, el número de ventas, las unidades totales y el importe total
    con dos decimales. Ordenada de mayor a menor importe.
    """
    raise NotImplementedError


def exportar_resumen(ruta, ventas: list[dict]) -> None:
    """Escribe en un CSV el resumen por región, con la cabecera ``CAMPOS_RESUMEN``."""
    raise NotImplementedError


def escribir_errores(ruta, errores: list[str]) -> None:
    """Escribe los errores en un fichero de texto, uno por línea."""
    raise NotImplementedError


def procesar(entrada, carpeta_salida) -> dict:
    """Importa el fichero y deja los resultados en la carpeta de salida.

    Crea la carpeta si no existe y escribe en ella ``resumen.csv`` y
    ``errores.txt``. Registra con ``logger.info`` un mensaje final con las
    cantidades. Devuelve un diccionario con las claves "leidas", "validas"
    y "descartadas".

    Si el fichero de entrada no vale, ``FicheroNoValido`` sube sin capturar
    y no se escribe nada.
    """
    raise NotImplementedError


def main(argumentos: list[str] | None = None) -> int:
    """Punto de entrada. Se entrega hecho: es el único sitio donde se capturan
    los errores del importador y donde se configura el logging.

    Uso: python m6_practica_importador.py [entrada.csv] [carpeta_salida]
    """
    import sys

    argumentos = sys.argv[1:] if argumentos is None else argumentos
    datos = Path(__file__).parent.parent / "datos"
    entrada = argumentos[0] if argumentos else datos / "ventas_con_errores.csv"
    salida = argumentos[1] if len(argumentos) > 1 else Path("salida_practica_6")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        cantidades = procesar(entrada, salida)
    except ErrorDeImportacion as error:
        logger.error("No se ha podido importar: %s", error)
        return 1
    print(f"Leídas {cantidades['leidas']} filas: {cantidades['validas']} válidas "
          f"y {cantidades['descartadas']} descartadas. Resultados en {salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
