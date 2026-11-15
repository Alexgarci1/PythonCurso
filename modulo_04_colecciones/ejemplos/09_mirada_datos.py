"""Módulo 4 - Ejemplo 9: mirada de datos.

Una tabla se puede guardar por filas (lista de diccionarios) o por columnas
(diccionario de listas). Las librerías de datos trabajan por columnas.
"""

FILAS = [
    {"region": "Norte", "vendedor": "Ada", "importe": 1200.0},
    {"region": "Sur", "vendedor": "Linus", "importe": 800.0},
    {"region": "Norte", "vendedor": "Grace", "importe": 950.0},
    {"region": "Sur", "vendedor": "Ada", "importe": 400.0},
]


def main():
    # --- De filas a columnas
    columnas = {clave: [fila[clave] for fila in FILAS] for clave in FILAS[0]}
    print(columnas["importe"])                       # [1200.0, 800.0, 950.0, 400.0]
    print(sum(columnas["importe"]))                  # 3350.0

    # --- De columnas a filas, con zip
    filas = [dict(zip(columnas, valores)) for valores in zip(*columnas.values())]
    print(filas == FILAS)                            # True

    # --- Filtrar: WHERE region = 'Norte'
    norte = [fila for fila in FILAS if fila["region"] == "Norte"]
    print(len(norte))                                # 2

    # --- Agrupar y sumar: GROUP BY region
    por_region = {}
    for fila in FILAS:
        por_region[fila["region"]] = por_region.get(fila["region"], 0) + fila["importe"]
    print(por_region)                                # {'Norte': 2150.0, 'Sur': 1200.0}

    # --- Ordenar el resultado: ORDER BY total DESC
    print(sorted(por_region.items(), key=lambda par: par[1], reverse=True))

    # --- Valores distintos: SELECT DISTINCT vendedor
    print(sorted({fila["vendedor"] for fila in FILAS}))


if __name__ == "__main__":
    main()
