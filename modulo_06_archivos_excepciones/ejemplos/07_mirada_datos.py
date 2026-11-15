"""Módulo 6 - Ejemplo 7: mirada de datos.

Cargar un fichero de datos reales: convertir tipos, apartar las filas que
no valen sin detener la carga y dejar un resumen en JSON.
"""

import csv
import json
import tempfile
from pathlib import Path

CARPETA_DATOS = Path(__file__).parent.parent / "datos"


def cargar(ruta):
    """Devuelve (filas válidas, rechazos). Cada rechazo es (número de línea, motivo)."""
    validas, rechazos = [], []
    with open(ruta, encoding="utf-8", newline="") as fichero:
        for numero, fila in enumerate(csv.DictReader(fichero), start=2):
            try:
                fila["unidades"] = int(fila["unidades"])
                fila["precio"] = float(fila["precio"])
            except (ValueError, TypeError) as error:      # TypeError: falta la columna y llega None
                rechazos.append((numero, str(error)))
                continue
            validas.append(fila)
    return validas, rechazos


def main():
    validas, rechazos = cargar(CARPETA_DATOS / "ventas_con_errores.csv")
    print(f"Filas válidas: {len(validas)}. Rechazadas: {len(rechazos)}")
    for numero, motivo in rechazos:
        print(f"  línea {numero}: {motivo}")

    # --- Un resumen del proceso, en JSON
    resumen = {
        "fichero": "ventas_con_errores.csv",
        "validas": len(validas),
        "rechazadas": len(rechazos),
        "importe_total": round(sum(f["unidades"] * f["precio"] for f in validas), 2),
        "lineas_rechazadas": [numero for numero, _ in rechazos],
    }
    with tempfile.TemporaryDirectory() as carpeta:
        salida = Path(carpeta) / "resumen.json"
        with open(salida, "w", encoding="utf-8") as fichero:
            json.dump(resumen, fichero, ensure_ascii=False, indent=2)
        print(salida.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
