"""Módulo 7 - Ejemplo 5: groupby, agg, pivot_table y merge."""

from pathlib import Path

import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"
ventas = pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])
ventas["importe"] = ventas["unidades"] * ventas["precio"]
ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")

# --- groupby: dividir, aplicar, combinar ------------------------------------
print(ventas.groupby("region")["importe"].sum().sort_values(ascending=False))
print()

# Lo mismo, como en el Módulo 4, para comparar:
totales = {}
for region, importe in zip(ventas["region"], ventas["importe"]):
    totales[region] = totales.get(region, 0) + importe
print("Con un diccionario:", {r: round(t, 2) for r, t in totales.items()})
print()

# --- Varias medidas con nombre ----------------------------------------------
resumen = ventas.groupby("vendedor").agg(
    ventas=("importe", "count"),
    unidades=("unidades", "sum"),
    importe=("importe", "sum"),
    ticket_medio=("importe", "mean"),
).round(2).sort_values("importe", ascending=False)
print(resumen)
print()

# --- Por mes ----------------------------------------------------------------
mensual = ventas.groupby("mes")["importe"].sum()
print(mensual)
print("Mejor mes:", mensual.idxmax())
print()

# --- Tabla dinámica ---------------------------------------------------------
print(ventas.pivot_table(index="region", columns="categoria", values="importe",
                         aggfunc="sum", fill_value=0))
print()

# --- merge: el JOIN de SQL --------------------------------------------------
objetivos = pd.read_csv(DATOS / "objetivos.csv")
combinado = resumen.reset_index().merge(objetivos, on="vendedor", how="left")
combinado["cumplimiento"] = (combinado["importe"] / combinado["objetivo"] * 100).round(1)
combinado["cumplido"] = combinado["importe"] >= combinado["objetivo"]
print(combinado[["vendedor", "importe", "objetivo", "cumplimiento", "cumplido"]])
print("Filas antes y después del merge:", len(resumen), len(combinado))
