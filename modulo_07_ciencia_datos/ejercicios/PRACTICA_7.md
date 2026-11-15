# Práctica 7. Análisis de las ventas del año

La dirección comercial quiere saber cómo va el año: cuánto se ha vendido, quién cumple su objetivo y cómo evoluciona el importe mes a mes. Lo quiere cada mes, con el fichero que llegue, así que no vale un análisis hecho a mano en una hoja de cálculo: hace falta un proceso que se ejecute igual todas las veces.

Vas a escribir ese proceso completo: **cargar, limpiar, calcular, representar y exportar**.

Fichero: `m7_practica_analisis.py`
Tests: `tests/test_m7_practica.py`
Datos: `datos/ventas_2026.csv` (320 ventas), `datos/ventas_sucias.csv` (63 filas con defectos) y `datos/objetivos.csv`

```bash
pytest modulo_07_ciencia_datos -v -k practica
```

## Funciones

| Función | Qué hace |
| --- | --- |
| `cargar(ruta)` | Lee el CSV con todo como texto |
| `preparar(df)` | Limpia, convierte los tipos y añade `importe` y `mes` |
| `indicadores(df)` | Devuelve un diccionario con las seis cifras principales |
| `ranking_vendedores(df, objetivos)` | Una fila por vendedor con su objetivo y su cumplimiento |
| `evolucion_mensual(df)` | Una fila por mes con el importe y la variación |
| `generar_graficos(df, carpeta)` | Guarda dos PNG y devuelve sus rutas |
| `exportar(tabla, ruta)` | Escribe una tabla en CSV |
| `main()` | **Ya está hecha.** Encadena todo e imprime los resultados |

Los docstrings son la especificación: léelos enteros antes de empezar. `preparar` es la función central; las demás dan por hecho que reciben lo que ella devuelve.

## El mismo código para un fichero limpio y uno sucio

`preparar` tiene que funcionar con los dos ficheros. Con `ventas_2026.csv` no descarta nada; con `ventas_sucias.csv` se queda con 54 de las 63 filas:

| Defecto | Qué se hace |
| --- | --- |
| Texto con espacios o en mayúsculas | Se normaliza |
| Filas repetidas | Se quitan |
| Precio con coma decimal | Se convierte |
| Región vacía | Pasa a ser «Sin región» |
| Fecha vacía o en otro formato | Se descarta la fila |
| Vendedor vacío | Se descarta la fila |
| Unidades vacías, con letras o negativas | Se descarta la fila |

Es la limpieza del Ejercicio 3. Puedes partir de tu solución.

## Resultado esperado

Con `datos/ventas_2026.csv`, `python m7_practica_analisis.py` imprime:

```
INDICADORES
  ventas                320
  importe_total         438848.9
  ticket_medio          1371.4
  mejor_vendedor        Ada
  mejor_mes             2026-09
  producto_mas_vendido  Antivirus

RANKING DE VENDEDORES
vendedor  ventas  importe  objetivo  cumplimiento  cumplido
     Ada      75 111944.0    100000         111.9      True
   Grace      76 107132.2    115000          93.2     False
Margaret      66  88130.4     90000          97.9     False
    Alan      54  69360.4     85000          81.6     False
   Linus      49  62281.9     60000         103.8      True

EVOLUCIÓN MENSUAL
    mes  importe  variacion
2026-01  35982.5        NaN
2026-02  18936.9      -47.4
2026-03  42354.9      123.7
2026-04  47667.5       12.5
2026-05  33559.7      -29.6
2026-06  44101.4       31.4
2026-07  48997.2       11.1
2026-08  36720.9      -25.1
2026-09  72526.9       97.5
2026-10  58001.0      -20.0
```

Y deja en la carpeta `salida_practica_7`:

```
salida_practica_7/
├── ranking_vendedores.csv
├── evolucion_mensual.csv
├── importe_por_vendedor.png
└── evolucion_mensual.png
```

Abre los dos gráficos. Un gráfico que pasa los tests pero no se entiende no está terminado.

## Pistas

- `variacion`: busca el método `pct_change` de las Series.
- `mejor_vendedor`, `mejor_mes` y `producto_mas_vendido`: `idxmax` devuelve la etiqueta del valor mayor.
- `ranking_vendedores`: `groupby`, `agg`, `reset_index`, `merge` y `sort_values`, en ese orden.
- Los valores del diccionario de `indicadores` son tipos de Python: usa `float()`, `round()` y `len()`.

## Criterios de evaluación

| Criterio | Peso |
| --- | --- |
| Los tests de la práctica pasan | 50 % |
| Operaciones vectorizadas: ningún bucle sobre filas | 20 % |
| Las funciones no modifican lo que reciben y no usan `print` ni `plt.show()` | 15 % |
| Gráficos legibles: título, etiquetas, orden y figuras cerradas | 15 % |

## Ampliaciones

1. Añade a `indicadores` la región con mayor ticket medio y el día de la semana con más ventas.
2. Genera un tercer gráfico con un panel de dos ejes: importe por categoría y por región.
3. Exporta los resultados a un único fichero Excel con una hoja por tabla: `pd.ExcelWriter` y `to_excel`. Necesitas `pip install openpyxl`.
4. Haz que `preparar` devuelva además cuántas filas ha descartado por cada motivo, como hacía el importador de la Práctica 6.
5. Conecta las dos prácticas: usa `importar_ventas` de la Práctica 6 para validar el fichero y construye el DataFrame a partir de la lista de ventas que devuelve.
