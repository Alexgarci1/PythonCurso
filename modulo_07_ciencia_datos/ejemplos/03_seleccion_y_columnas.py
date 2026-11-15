"""Módulo 7 - Ejemplo 3: filtrar, seleccionar, crear columnas y ordenar."""

from pathlib import Path

import numpy as np
import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"
ventas = pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])

# --- Filtrar con máscaras ---------------------------------------------------
del_sur = ventas[ventas["region"] == "Sur"]
print("Ventas del Sur:", len(del_sur))

equipos_del_sur = ventas[(ventas["region"] == "Sur") & (ventas["categoria"] == "Equipos")]
print("Equipos vendidos en el Sur:", len(equipos_del_sur))

baratos = ventas[ventas["producto"].isin(["Ratón", "Teclado"])]
print("Ventas de ratones y teclados:", len(baratos))

marzo = ventas[ventas["fecha"].between("2026-03-01", "2026-03-31")]
print("Ventas de marzo:", len(marzo))
print()

# --- loc e iloc -------------------------------------------------------------
print(ventas.loc[ventas["unidades"] >= 38, ["vendedor", "producto", "unidades"]])
print(ventas.iloc[:3, :4])
print()

# --- Columnas nuevas --------------------------------------------------------
ventas["importe"] = ventas["unidades"] * ventas["precio"]
ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")
ventas["dia_semana"] = ventas["fecha"].dt.day_name()
ventas["tamano"] = np.where(ventas["importe"] >= 1000, "grande", "normal")
print(ventas[["fecha", "importe", "mes", "dia_semana", "tamano"]].head())
print()

# assign devuelve un DataFrame nuevo: el original no cambia.
con_iva = ventas.assign(importe_con_iva=(ventas["importe"] * 1.21).round(2))
print("¿El original tiene la columna nueva?", "importe_con_iva" in ventas.columns)
print()

# --- Ordenar ----------------------------------------------------------------
print(ventas.sort_values(["region", "importe"], ascending=[True, False])
      [["region", "vendedor", "producto", "importe"]].head())
print()
print(ventas.nlargest(3, "unidades")[["vendedor", "producto", "unidades"]])
