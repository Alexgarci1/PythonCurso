"""Módulo 6 - Ejemplo 1: lectura y escritura de ficheros de texto."""

import tempfile
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent.parent / "datos"     # no depende de la carpeta de trabajo


def main():
    ruta = CARPETA_DATOS / "notas.txt"
    print(ruta.name, ruta.suffix, ruta.exists(), ruta.stat().st_size, "bytes")

    # --- Leer todo de una vez
    with open(ruta, encoding="utf-8") as fichero:
        contenido = fichero.read()
    print(len(contenido), "caracteres;", fichero.closed)     # True: with lo ha cerrado

    # --- Leer línea a línea: solo hay una línea en memoria
    with open(ruta, encoding="utf-8") as fichero:
        for numero, linea in enumerate(fichero, start=1):
            if linea.startswith("-"):
                print(numero, linea.rstrip("\n"))

    # --- Lista de líneas sin el salto final
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    print(len(lineas), "líneas;", len([linea for linea in lineas if linea.strip()]), "no vacías")

    # --- Un fichero abierto se agota como cualquier iterador
    with open(ruta, encoding="utf-8") as fichero:
        primera_vez = len(list(fichero))
        segunda_vez = len(list(fichero))
    print(primera_vez, segunda_vez)

    # --- Escribir: en una carpeta temporal para no ensuciar el repositorio
    with tempfile.TemporaryDirectory() as temporal:
        salida = Path(temporal) / "informes" / "resumen.txt"
        salida.parent.mkdir(parents=True, exist_ok=True)

        with open(salida, "w", encoding="utf-8") as fichero:        # w crea o vacía
            fichero.write("Resumen\n")
            for linea in lineas[:2]:
                fichero.write(linea + "\n")

        with open(salida, "a", encoding="utf-8") as fichero:        # a añade
            print("Línea añadida con print", file=fichero)

        print(salida.read_text(encoding="utf-8"))

        try:
            open(salida, "x", encoding="utf-8")                     # x falla si ya existe
        except FileExistsError as error:
            print("FileExistsError:", error.strerror)

        print(sorted(fichero.name for fichero in salida.parent.iterdir()))

    # --- La codificación importa
    datos = "Añadir contraseña".encode("utf-8")
    print(datos)
    print(datos.decode("utf-8"), "|", datos.decode("latin-1"))


if __name__ == "__main__":
    main()
