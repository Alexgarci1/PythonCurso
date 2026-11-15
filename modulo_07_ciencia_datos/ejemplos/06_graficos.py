"""Módulo 7 - Ejemplo 6: gráficos con Matplotlib.

Guarda tres imágenes en la carpeta ``graficos_ejemplo`` junto a este fichero.
Quita el comentario de la última línea para verlas además en una ventana.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

AQUI = Path(__file__).resolve().parent
DATOS = AQUI.parent / "datos"
SALIDA = AQUI / "graficos_ejemplo"
SALIDA.mkdir(exist_ok=True)

ventas = pd.read_csv(DATOS / "ventas_2026.csv", parse_dates=["fecha"])
ventas["importe"] = ventas["unidades"] * ventas["precio"]
ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")

por_vendedor = ventas.groupby("vendedor")["importe"].sum().sort_values(ascending=False)
mensual = ventas.groupby("mes")["importe"].sum()

# --- Barras: comparar categorías --------------------------------------------
figura, ejes = plt.subplots(figsize=(8, 4.5))
barras = ejes.bar(por_vendedor.index, por_vendedor.values, color="#2b6cb0")
ejes.bar_label(barras, fmt="{:,.0f}")                  # el valor encima de cada barra
ejes.set_title("Importe por vendedor")
ejes.set_ylabel("Importe (€)")
figura.tight_layout()
figura.savefig(SALIDA / "barras.png", dpi=150)

# --- Líneas: evolución en el tiempo -----------------------------------------
figura, ejes = plt.subplots(figsize=(8, 4.5))
ejes.plot(mensual.index, mensual.values, marker="o", color="#2b6cb0")
ejes.set_title("Evolución mensual")
ejes.set_ylabel("Importe (€)")
ejes.grid(True, alpha=0.3)
ejes.tick_params(axis="x", rotation=45)
figura.tight_layout()
figura.savefig(SALIDA / "lineas.png", dpi=150)

# --- Panel: varios gráficos en una figura -----------------------------------
figura, (izquierda, centro, derecha) = plt.subplots(1, 3, figsize=(16, 4.5))
izquierda.bar(por_vendedor.index, por_vendedor.values, color="#2b6cb0")
izquierda.set_title("Por vendedor")
centro.plot(mensual.index, mensual.values, marker="o", color="#f2b33d")
centro.set_title("Evolución mensual")
centro.tick_params(axis="x", rotation=45)
derecha.hist(ventas["importe"], bins=15, color="#2f9e6b", edgecolor="white")
derecha.set_title("Reparto del importe por venta")
figura.suptitle("Ventas de 2026")
figura.tight_layout()
figura.savefig(SALIDA / "panel.png", dpi=150)

print("Gráficos guardados en", SALIDA)
# plt.show()
