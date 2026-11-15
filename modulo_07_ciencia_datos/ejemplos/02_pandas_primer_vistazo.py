"""Módulo 7 - Ejemplo 2: cargar un CSV con pandas y mirarlo."""

from pathlib import Path

import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"

# --- Series -----------------------------------------------------------------
importes = pd.Series([1900.0, 199.0, 567.0], index=["Ada", "Linus", "Grace"])
print(importes)
print("Linus:", importes["Linus"], "  mayores de 500:", list(importes[importes > 500].index))
print()

# --- Cargar -----------------------------------------------------------------
ventas = pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])

# --- Primer vistazo ---------------------------------------------------------
print("Forma:", ventas.shape)
print()
print(ventas.head())
print()
ventas.info()
print()
print(ventas.describe().round(2))
print()
print("Vendedores:", sorted(ventas["vendedor"].unique()))
print()
print(ventas["region"].value_counts())
print()

# --- Operar con columnas ----------------------------------------------------
print("Unidades vendidas:", ventas["unidades"].sum())
print("Importe total:", (ventas["unidades"] * ventas["precio"]).sum().round(2))
print("Periodo:", ventas["fecha"].min().date(), "a", ventas["fecha"].max().date())
