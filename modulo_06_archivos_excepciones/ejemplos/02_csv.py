"""Módulo 6 - Ejemplo 2: lectura y escritura de CSV."""

import csv
import tempfile
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent.parent / "datos"


def leer_ventas(ruta):
    """Lee el CSV y devuelve una lista de diccionarios con los tipos convertidos."""
    with open(ruta, encoding="utf-8", newline="") as fichero:
        ventas = list(csv.DictReader(fichero))
    for venta in ventas:                       # todo llega como texto
        venta["unidades"] = int(venta["unidades"])
        venta["precio"] = float(venta["precio"])
    return ventas


def main():
    ruta = CARPETA_DATOS / "ventas.csv"

    # --- reader: cada fila es una lista de cadenas
    with open(ruta, encoding="utf-8", newline="") as fichero:
        lector = csv.reader(fichero)
        cabecera = next(lector)
        primera = next(lector)
    print(cabecera)
    print(primera, type(primera[5]).__name__)

    # --- DictReader: cada fila es un diccionario
    ventas = leer_ventas(ruta)
    print(len(ventas), "ventas;", ventas[0])

    # --- A partir de aquí, es el Módulo 4
    total = sum(venta["unidades"] * venta["precio"] for venta in ventas)
    por_region = {}
    for venta in ventas:
        importe = venta["unidades"] * venta["precio"]
        por_region[venta["region"]] = por_region.get(venta["region"], 0) + importe
    print(f"Total: {total:,.2f}")
    for region, importe in sorted(por_region.items(), key=lambda par: -par[1]):
        print(f"  {region:<8}{importe:>12,.2f}")

    # --- Escribir con DictWriter
    with tempfile.TemporaryDirectory() as temporal:
        salida = Path(temporal) / "por_region.csv"
        with open(salida, "w", encoding="utf-8", newline="") as fichero:
            escritor = csv.DictWriter(fichero, fieldnames=["region", "importe"])
            escritor.writeheader()
            for region, importe in por_region.items():
                escritor.writerow({"region": region, "importe": round(importe, 2)})
        print(salida.read_text(encoding="utf-8"))

    # --- Un CSV exportado por Excel en español: punto y coma y coma decimal
    with open(CARPETA_DATOS / "excel.csv", encoding="utf-8-sig", newline="") as fichero:
        for fila in csv.DictReader(fichero, delimiter=";"):
            precio = float(fila["precio"].replace(",", "."))
            print(fila["producto"], int(fila["unidades"]), precio)

    # --- Por qué no vale split: un campo puede contener el delimitador
    linea = '"Monitor 27""; curvo";3;189,00'
    print(linea.split(";"))
    print(next(csv.reader([linea], delimiter=";")))


if __name__ == "__main__":
    main()
