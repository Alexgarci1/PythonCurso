"""Módulo 7 - Ejemplo 4: limpiar un fichero con defectos, paso a paso."""

from pathlib import Path

import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "datos"

# 1. Leer sin interpretar: todo como texto.
bruto = pd.read_csv(DATOS / "ventas_sucias.csv", dtype=str)
print("Filas leídas:", len(bruto))
print()
print("Valores ausentes por columna:")
print(bruto.isna().sum())
print()
print("Vendedores tal como vienen:", sorted(bruto["vendedor"].dropna().unique()))
print()

# 2. Texto: sin espacios y con la inicial en mayúscula.
limpio = bruto.copy()
for columna in ["vendedor", "region", "producto", "categoria"]:
    limpio[columna] = limpio[columna].str.strip().str.capitalize()
print("Vendedores normalizados:", sorted(limpio["vendedor"].dropna().unique()))

# 3. Duplicados. Después de normalizar, no antes.
print("Filas duplicadas:", limpio.duplicated().sum())
limpio = limpio.drop_duplicates()

# 4. Tipos. Lo que no se puede convertir queda ausente.
limpio["fecha"] = pd.to_datetime(limpio["fecha"], format="%Y-%m-%d", errors="coerce")
limpio["unidades"] = pd.to_numeric(limpio["unidades"], errors="coerce")
limpio["precio"] = pd.to_numeric(limpio["precio"].str.replace(",", "."), errors="coerce")
print()
print("Ausentes después de convertir:")
print(limpio.isna().sum())

# 5. Decidir qué hacer con lo que falta.
limpio["region"] = limpio["region"].fillna("Sin región")
limpio = limpio.dropna(subset=["fecha", "vendedor", "unidades", "precio"])
limpio = limpio[(limpio["unidades"] > 0) & (limpio["precio"] > 0)]

# 6. Rematar: tipos definitivos e índice renumerado.
limpio = limpio.astype({"unidades": int}).reset_index(drop=True)

print()
print(f"Filas válidas: {len(limpio)} de {len(bruto)}")
print(limpio.dtypes)
