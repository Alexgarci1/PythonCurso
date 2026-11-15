# Módulo 7. Python para ciencia de datos (8 horas)

Hasta aquí has usado Python para construir aplicaciones. En este módulo lo usas para lo otro que ha hecho famoso al lenguaje: analizar datos. Al terminar sabrás cargar un fichero de datos, limpiarlo, resumirlo, representarlo en un gráfico y dejar el análisis en un cuaderno o en un script que cualquiera pueda volver a ejecutar.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 7.1 | El ecosistema de datos y los cuadernos Jupyter | 0,5 h |
| 7.2 | NumPy: arrays y operaciones vectorizadas | 1,5 h |
| 7.3 | pandas: Series, DataFrame y carga de datos | 1,5 h |
| 7.4 | Selección, filtrado y columnas nuevas | 1 h |
| 7.5 | Limpieza de datos | 1 h |
| 7.6 | Agrupar, agregar y combinar | 1 h |
| 7.7 | Visualización con Matplotlib | 1 h |
| 7.8 | Ejercicios prácticos y práctica 7 | 0,5 h |

Los datos del módulo son las ventas que ya conoces: en el Módulo 4 eran una lista de diccionarios, en el Módulo 6 un CSV leído fila a fila y aquí son un `DataFrame`. Verás el mismo problema resuelto con una herramienta distinta.

---

## 7.1 El ecosistema de datos y los cuadernos Jupyter

### Aplicaciones y datos: dos formas de trabajar

| | Desarrollo de aplicaciones | Análisis de datos |
| --- | --- | --- |
| Objetivo | Un programa que otros usan | Una respuesta a una pregunta |
| Forma de trabajar | Diseñar, escribir, probar | Explorar, probar, corregir, volver a mirar |
| Unidad de trabajo | Módulos, clases y funciones | Tablas y columnas |
| Herramienta habitual | Editor, tests y control de versiones | Cuaderno interactivo |
| Resultado | Código que se mantiene | Tablas, gráficos y conclusiones |

No son mundos separados. Un análisis que se repite cada mes acaba convertido en un script con funciones y tests, y una aplicación acaba necesitando un informe. Por eso en este módulo las funciones de análisis se prueban con `pytest`, igual que todo lo anterior.

### Las librerías

| Librería | Para qué sirve | Se importa como |
| --- | --- | --- |
| NumPy | Arrays numéricos y cálculo vectorizado. Es la base de todas las demás | `import numpy as np` |
| pandas | Tablas de datos: leer, limpiar, filtrar, agrupar y combinar | `import pandas as pd` |
| Matplotlib | Gráficos | `import matplotlib.pyplot as plt` |
| Jupyter | Cuadernos que mezclan código, resultados y texto | |
| scikit-learn | Aprendizaje automático. Fuera del alcance de este curso | |

Los alias `np`, `pd` y `plt` son una convención universal. Úsalos siempre: todo el código y la documentación que encuentres los usa.

Ninguna viene con Python. Se instalan en el entorno virtual:

```bash
pip install -r requirements.txt
```

El fichero `requirements.txt` del repositorio ya incluye `numpy`, `pandas`, `matplotlib` y `jupyter`.

### Cuadernos Jupyter

Un cuaderno es un fichero `.ipynb` formado por celdas. Cada celda contiene código o texto en Markdown, y el resultado de cada celda de código queda guardado debajo de ella. VS Code los abre directamente con la extensión Jupyter.

| Acción | Atajo |
| --- | --- |
| Ejecutar la celda y pasar a la siguiente | `Mayús + Intro` |
| Ejecutar la celda y quedarse en ella | `Ctrl + Intro` |
| Celda nueva debajo | `Esc`, `B` |
| Convertir en Markdown o en código | `Esc`, `M` o `Y` |

La última expresión de una celda se muestra sin necesidad de `print`, como en el intérprete.

El cuaderno de ejemplo es [`ejemplos/07_cuaderno_exploracion.ipynb`](ejemplos/07_cuaderno_exploracion.ipynb).

### Cuaderno o script

| Usa un cuaderno para | Usa un script `.py` para |
| --- | --- |
| Explorar unos datos que no conoces | Un proceso que se repite |
| Probar ideas y ver gráficos al momento | Código que otros van a importar |
| Enseñar un análisis con sus explicaciones | Todo lo que necesite tests |

El peligro del cuaderno es el **estado oculto**: las celdas se pueden ejecutar en cualquier orden, y una variable puede tener un valor que ya no corresponde al código que se ve. Antes de dar por bueno un cuaderno, usa «Reiniciar y ejecutar todo». Si no funciona de arriba abajo, no funciona.

---

## 7.2 NumPy: arrays y operaciones vectorizadas

### Por qué no basta con las listas

Una lista de Python guarda referencias a objetos de cualquier tipo. Es flexible, pero lenta para calcular y no sabe de aritmética:

```python
>>> precios = [100, 200, 300]
>>> precios * 2
[100, 200, 300, 100, 200, 300]
>>> [p * 1.21 for p in precios]
[121.0, 242.0, 363.0]
```

Un array de NumPy guarda números del mismo tipo en un bloque continuo de memoria, y las operaciones se aplican a todos los elementos a la vez:

```python
>>> import numpy as np
>>> precios = np.array([100, 200, 300])
>>> precios * 2
array([200, 400, 600])
>>> precios * 1.21
array([121., 242., 363.])
```

A esto se le llama **vectorizar**: escribir la operación sobre el array completo en lugar de recorrerlo. El bucle existe, pero lo ejecuta código compilado en C. Con millones de elementos la diferencia va de varias veces a decenas de veces, según la operación: el ejemplo `01_numpy.py` lo mide en tu equipo.

La regla del módulo: si escribes un `for` para recorrer un array o una columna, casi seguro que hay una forma mejor.

### Crear arrays

```python
>>> np.array([1, 2, 3])
array([1, 2, 3])
>>> np.arange(0, 10, 2)            # como range, pero devuelve un array
array([0, 2, 4, 6, 8])
>>> np.linspace(0, 1, 5)           # 5 valores repartidos entre 0 y 1, los dos incluidos
array([0.  , 0.25, 0.5 , 0.75, 1.  ])
>>> np.zeros(3)
array([0., 0., 0.])
>>> np.ones((2, 3))                # 2 filas y 3 columnas
array([[1., 1., 1.],
       [1., 1., 1.]])
```

Tres atributos describen un array:

```python
>>> matriz = np.array([[1, 2, 3], [4, 5, 6]])
>>> matriz.shape                   # forma: 2 filas, 3 columnas
(2, 3)
>>> matriz.ndim                    # número de dimensiones
2
>>> matriz.dtype                   # tipo de los elementos
dtype('int64')
```

Todos los elementos tienen el mismo tipo. Si mezclas enteros y decimales, todo pasa a decimal:

```python
>>> np.array([1, 2.5, 3])
array([1. , 2.5, 3. ])
```

### Operaciones elemento a elemento

Los operadores aritméticos y de comparación actúan elemento a elemento, entre un array y un número o entre dos arrays de la misma forma:

```python
>>> unidades = np.array([2, 10, 3])
>>> precios = np.array([950.0, 19.9, 189.0])
>>> unidades * precios
array([1900.,  199.,  567.])
>>> precios > 100
array([ True, False,  True])
>>> np.round(precios * 1.21, 2)
array([1149.5 ,   24.08,  228.69])
```

Las funciones matemáticas de NumPy también: `np.sqrt`, `np.log`, `np.abs`, `np.round`.

### Agregaciones y ejes

```python
>>> importes = np.array([1900.0, 199.0, 567.0])
>>> importes.sum()
np.float64(2666.0)
>>> importes.mean()
np.float64(888.6666666666666)
>>> importes.max(), importes.argmax()        # el valor mayor y su posición
(np.float64(1900.0), np.int64(0))
```

Los resultados son escalares de NumPy, no `float` de Python. Se comportan igual en los cálculos; cuando necesites el tipo de Python, por ejemplo para escribir un JSON, conviértelo con `float()` o `int()`.

En una matriz, `axis` indica la dirección en la que se opera:

```python
>>> matriz = np.array([[1, 2, 3], [4, 5, 6]])
>>> matriz.sum()                   # todo
np.int64(21)
>>> matriz.sum(axis=0)             # a lo largo de las filas: un resultado por columna
array([5, 7, 9])
>>> matriz.sum(axis=1)             # a lo largo de las columnas: un resultado por fila
array([ 6, 15])
```

### Selección: índices, cortes y máscaras

Los índices y los cortes funcionan como en las listas, con una dimensión por cada coma:

```python
>>> matriz = np.array([[1, 2, 3], [4, 5, 6]])
>>> matriz[0, 2]                   # fila 0, columna 2
np.int64(3)
>>> matriz[:, 1]                   # todas las filas, columna 1
array([2, 5])
```

Lo nuevo es la **máscara booleana**: un array de `True` y `False` usado como índice selecciona los elementos donde hay `True`.

```python
>>> importes = np.array([1900.0, 199.0, 567.0, 45.0])
>>> importes > 500
array([ True, False,  True, False])
>>> importes[importes > 500]
array([1900.,  567.])
>>> importes[(importes > 100) & (importes < 1000)]
array([199., 567.])
```

Para combinar condiciones se usan `&`, `|` y `~`, con cada condición entre paréntesis. `and`, `or` y `not` no sirven aquí: trabajan con un único valor de verdad, y un array tiene muchos.

`np.where` elige entre dos valores según una condición:

```python
>>> np.where(importes > 500, "grande", "pequeña")
array(['grande', 'pequeña', 'grande', 'pequeña'], dtype='<U7')
```

### Vistas y copias

Un corte de un array no copia los datos: es una **vista** sobre los mismos. Es la diferencia más importante con las listas.

```python
>>> original = np.array([1, 2, 3, 4])
>>> trozo = original[:2]
>>> trozo[0] = 99
>>> original
array([99,  2,  3,  4])
```

Si necesitas una copia independiente, pídela: `original[:2].copy()`. La selección con una máscara, en cambio, siempre devuelve una copia.

---

## 7.3 pandas: Series, DataFrame y carga de datos

### Series y DataFrame

pandas añade a NumPy dos estructuras con etiquetas:

- Una **Series** es una columna: un array con un índice que da nombre a cada elemento.
- Un **DataFrame** es una tabla: un conjunto de Series que comparten índice. Cada columna tiene su nombre y su tipo.

```python
>>> import pandas as pd
>>> importes = pd.Series([1900.0, 199.0, 567.0], index=["Ada", "Linus", "Grace"])
>>> importes
Ada      1900.0
Linus     199.0
Grace     567.0
dtype: float64
>>> importes["Linus"]
np.float64(199.0)
>>> importes[importes > 500]
Ada      1900.0
Grace     567.0
dtype: float64
```

Una Series se parece a un diccionario ordenado en el que además se puede operar como con un array.

Un DataFrame se puede crear a partir de la lista de diccionarios del Módulo 4:

```python
>>> ventas = pd.DataFrame([
...     {"vendedor": "Ada", "producto": "Portátil", "unidades": 2, "precio": 950.0},
...     {"vendedor": "Linus", "producto": "Ratón", "unidades": 10, "precio": 19.9},
...     {"vendedor": "Grace", "producto": "Monitor", "unidades": 3, "precio": 189.0},
... ])
>>> ventas
  vendedor  producto  unidades  precio
0      Ada  Portátil         2   950.0
1    Linus     Ratón        10    19.9
2    Grace   Monitor         3   189.0
```

La columna de la izquierda es el **índice**. Si no se indica otro, es la posición de la fila.

### Leer un CSV

En el Módulo 6 leíste este fichero con `csv.DictReader` y convertiste cada campo a mano. Con pandas es una línea:

```python
>>> ventas = pd.read_csv("datos/ventas_2026.csv", parse_dates=["fecha"])
>>> ventas.shape
(320, 7)
```

`read_csv` deduce el tipo de cada columna. Las fechas hay que pedírselas con `parse_dates`. Otros parámetros que se usan a diario:

| Parámetro | Para qué |
| --- | --- |
| `sep=";"` | Separador distinto de la coma, habitual en los CSV exportados por Excel en español |
| `decimal=","` | Coma decimal |
| `encoding="utf-8"` | Codificación del fichero |
| `dtype=str` | Leer todo como texto, sin interpretar nada |
| `usecols=[...]` | Cargar solo algunas columnas |
| `nrows=1000` | Cargar solo las primeras filas |

pandas lee también Excel con `pd.read_excel`, JSON con `pd.read_json` y bases de datos con `pd.read_sql`. Para escribir, los métodos son `to_csv`, `to_excel` y `to_json`.

### Primer vistazo

Lo primero que se hace con unos datos nuevos es mirarlos. Siempre.

```python
>>> ventas.head(3)
       fecha vendedor  region   producto    categoria  unidades  precio
0 2026-01-05      Ada   Norte      Ratón  Periféricos         6    19.9
1 2026-01-05    Grace  Centro    Teclado  Periféricos         6    45.0
2 2026-01-05    Linus     Sur  Antivirus     Software         9    29.5
>>> list(ventas.columns)
['fecha', 'vendedor', 'region', 'producto', 'categoria', 'unidades', 'precio']
```

| Método o atributo | Qué muestra |
| --- | --- |
| `df.head(n)`, `df.tail(n)` | Las primeras o las últimas filas |
| `df.shape` | Número de filas y de columnas |
| `df.columns`, `df.dtypes` | Nombres y tipos de las columnas |
| `df.info()` | Resumen: tipos, valores no nulos y memoria |
| `df.describe()` | Estadísticas de las columnas numéricas |
| `df["col"].unique()`, `.nunique()` | Valores distintos y cuántos son |
| `df["col"].value_counts()` | Cuántas veces aparece cada valor |

```python
>>> ventas["region"].value_counts()
region
Sur       99
Norte     80
Centro    73
Este      68
Name: count, dtype: int64
>>> ventas["unidades"].describe().round(1)
count    320.0
mean       8.0
std        8.9
min        1.0
25%        1.8
50%        4.0
75%       10.2
max       44.0
Name: unidades, dtype: float64
```

### Columnas y operaciones

Una columna es una Series y se opera con ella como con un array:

```python
>>> ventas["unidades"].sum()
np.int64(2556)
>>> ventas["precio"].max()
np.float64(3200.0)
>>> (ventas["unidades"] * ventas["precio"]).sum().round(2)
np.float64(438848.9)
```

Para seleccionar varias columnas se pasa una lista. El resultado es otro DataFrame:

```python
>>> ventas[["vendedor", "unidades"]].head(2)
  vendedor  unidades
0      Ada         6
1    Grace         6
```

---

## 7.4 Selección, filtrado y columnas nuevas

### Filtrar filas con máscaras

Igual que en NumPy: una condición sobre una columna produce una Series de booleanos, y esa Series selecciona filas.

```python
>>> grandes = ventas[ventas["unidades"] >= 38]
>>> grandes[["vendedor", "producto", "unidades"]]
    vendedor   producto  unidades
194    Grace  Antivirus        39
294      Ada  Antivirus        44
318      Ada  Antivirus        39
>>> len(ventas[(ventas["region"] == "Sur") & (ventas["categoria"] == "Equipos")])
29
>>> len(ventas[ventas["producto"].isin(["Ratón", "Teclado"])])
72
```

Recuerda: `&`, `|` y `~`, y cada condición entre paréntesis.

Métodos útiles para construir condiciones:

| Método | Condición |
| --- | --- |
| `.isin([...])` | El valor está en la lista |
| `.between(a, b)` | El valor está entre `a` y `b`, los dos incluidos |
| `.str.contains("texto")` | El texto contiene una subcadena |
| `.str.startswith("A")` | El texto empieza por |
| `.isna()`, `.notna()` | El valor está ausente o no |

### loc e iloc

Para seleccionar filas y columnas a la vez:

- `df.loc[filas, columnas]` selecciona por **etiqueta**.
- `df.iloc[filas, columnas]` selecciona por **posición**.

```python
>>> ventas.loc[0, "vendedor"]
'Ada'
>>> ventas.loc[ventas["unidades"] >= 38, ["vendedor", "unidades"]]
    vendedor  unidades
194    Grace        39
294      Ada        44
318      Ada        39
>>> ventas.iloc[0, 1]
'Ada'
>>> ventas.iloc[:2, :3]
       fecha vendedor  region
0 2026-01-05      Ada   Norte
1 2026-01-05    Grace  Centro
```

Un detalle que sorprende: los cortes de `loc` incluyen el extremo final, porque son etiquetas y no posiciones. `ventas.loc[0:2]` devuelve tres filas; `ventas.iloc[0:2]`, dos.

### Columnas nuevas

Una columna se crea asignándola:

```python
>>> ventas["importe"] = ventas["unidades"] * ventas["precio"]
>>> ventas["mes"] = ventas["fecha"].dt.strftime("%Y-%m")
>>> ventas[["fecha", "unidades", "precio", "importe", "mes"]].head(2)
       fecha  unidades  precio  importe      mes
0 2026-01-05         6    19.9    119.4  2026-01
1 2026-01-05         6    45.0    270.0  2026-01
```

Los accesores dan métodos específicos del tipo de la columna: `.dt` para fechas (`.dt.year`, `.dt.month`, `.dt.day_name()`) y `.str` para texto (`.str.upper()`, `.str.strip()`, `.str.replace()`).

`assign` hace lo mismo pero devuelve un DataFrame nuevo y deja el original como estaba. Es la forma que conviene dentro de una función:

```python
def con_importe(df):
    return df.assign(importe=df["unidades"] * df["precio"])
```

Para una columna que depende de una condición, `np.where`:

```python
>>> import numpy as np
>>> ventas["tamano"] = np.where(ventas["importe"] >= 1000, "grande", "normal")
>>> ventas["tamano"].value_counts()
tamano
normal    183
grande    137
Name: count, dtype: int64
```

### Ordenar

```python
>>> ventas.sort_values("importe", ascending=False)[["vendedor", "producto", "importe"]].head(3)
     vendedor  producto  importe
312       Ada  Servidor   6400.0
316  Margaret  Servidor   6400.0
319     Grace  Servidor   6400.0
>>> ventas.nlargest(2, "unidades")[["vendedor", "unidades"]]
    vendedor  unidades
294      Ada        44
194    Grace        39
```

`sort_values` admite una lista de columnas, como la clave de tupla de `sorted` en el Módulo 4: `df.sort_values(["region", "importe"], ascending=[True, False])`.

### No modifiques lo que recibes

Casi todos los métodos de pandas devuelven un objeto nuevo en lugar de cambiar el original: `sort_values`, `drop_duplicates`, `fillna`, `assign`. Es lo que permite encadenarlos.

Lo que sí modifica es la asignación: `df["columna"] = ...`. Dentro de una función, eso cambiaría el DataFrame de quien te llama, el mismo problema de las listas mutables del Módulo 2. Dos formas de evitarlo:

```python
def preparar(df):
    limpio = df.copy()                 # trabaja sobre una copia
    limpio["importe"] = limpio["unidades"] * limpio["precio"]
    return limpio
```

O usar `assign`, que ya devuelve una copia.

---

## 7.5 Limpieza de datos

Los datos reales llegan sucios. El fichero `datos/ventas_sucias.csv` tiene los defectos de siempre: celdas vacías, texto con espacios o en mayúsculas, números escritos con coma, fechas en otro formato y filas repetidas. En un análisis real, limpiar ocupa más tiempo que analizar.

### Leer sin interpretar

Cuando no te fías de un fichero, léelo todo como texto y convierte tú:

```python
>>> bruto = pd.read_csv("datos/ventas_sucias.csv", dtype=str)
>>> bruto.shape
(63, 7)
>>> bruto.iloc[2:5, :4]
        fecha vendedor  region       producto
2  2026-01-05     ada      Sur      Antivirus
3  2026-01-07    Grace  Centro  Soporte anual
4  2026-01-07    Grace  Centro  Soporte anual
```

### Valores ausentes

pandas representa un dato que falta con `NaN`, que significa *not a number*. En las fechas se llama `NaT`.

```python
>>> bruto.isna().sum()
fecha        1
vendedor     1
region       2
producto     0
categoria    0
unidades     1
precio       0
dtype: int64
```

`NaN` no es igual a nada, ni a sí mismo. Nunca se compara con `==`: se usa `isna()` o `notna()`.

Hay tres cosas que hacer con un valor ausente, y elegir es una decisión de negocio, no técnica:

| Decisión | Código |
| --- | --- |
| Descartar la fila | `df.dropna(subset=["fecha", "vendedor"])` |
| Rellenar con un valor fijo | `df["region"].fillna("Sin región")` |
| Rellenar con un valor calculado | `df["precio"].fillna(df["precio"].median())` |

Las agregaciones ignoran los ausentes: `sum()` y `mean()` operan solo con los valores que existen.

### Texto

```python
>>> bruto["vendedor"].str.strip().str.capitalize().dropna().unique().tolist()
['Ada', 'Grace', 'Margaret', 'Alan', 'Linus']
```

`.str` aplica el método de cadena a toda la columna y deja los ausentes como estaban. Aquí se usa `capitalize` y no `title` porque hay nombres de varias palabras: `title` convertiría «Licencia ofimática» en «Licencia Ofimática».

### Tipos

`pd.to_numeric` y `pd.to_datetime` convierten una columna. Con `errors="coerce"`, lo que no se puede convertir pasa a ser un valor ausente en lugar de detener el programa:

```python
>>> pd.to_numeric(pd.Series(["6", "tres", "-4"]), errors="coerce")
0    6.0
1    NaN
2   -4.0
dtype: float64
>>> pd.to_numeric(pd.Series(["29,5", "19.9"]).str.replace(",", "."))
0    29.5
1    19.9
dtype: float64
>>> pd.to_datetime(pd.Series(["2026-01-05", "15/02/2026"]), format="%Y-%m-%d", errors="coerce")
0   2026-01-05
1          NaT
dtype: datetime64[us]
```

Fíjate en el primer resultado: una columna de enteros con un ausente pasa a ser decimal, porque `NaN` es un valor decimal. Cuando ya no queden ausentes se devuelve a entero con `astype(int)`.

Indica siempre el `format` de las fechas. Sin él, pandas intenta adivinarlo, y «03/04/2026» puede acabar siendo el 3 de abril o el 4 de marzo.

### Duplicados

```python
>>> bruto.duplicated().sum()
np.int64(3)
>>> len(bruto.drop_duplicates())
60
```

El orden de los pasos importa: normaliza el texto antes de buscar duplicados, o «Ada» y «  ada » contarán como personas distintas.

### Encadenar la limpieza

Una limpieza se escribe como una función que recibe los datos en bruto y devuelve los limpios, sin tocar el original:

```python
def limpiar(df):
    limpio = df.copy()
    limpio["vendedor"] = limpio["vendedor"].str.strip().str.capitalize()
    limpio = limpio.drop_duplicates()
    limpio["unidades"] = pd.to_numeric(limpio["unidades"], errors="coerce")
    limpio = limpio.dropna(subset=["vendedor", "unidades"])
    limpio = limpio[limpio["unidades"] > 0]
    return limpio.astype({"unidades": int}).reset_index(drop=True)
```

`reset_index(drop=True)` renumera las filas desde cero después de haber descartado algunas.

Compara con el importador del Módulo 6: allí validabas fila a fila y anotabas cada error con su número de línea. Las dos formas son válidas. La de pandas es más corta y más rápida; la del Módulo 6 da mejores mensajes de error. En un proceso de carga serio se cuenta, como mínimo, cuántas filas se descartan y por qué.

---

## 7.6 Agrupar, agregar y combinar

### groupby

En el Módulo 4 agrupabas con un diccionario y un bucle: para cada venta, sumar su importe al total de su región. `groupby` hace eso en una línea y en tres pasos, que conviene tener en la cabeza: **dividir** las filas en grupos, **aplicar** un cálculo a cada grupo y **combinar** los resultados.

```python
>>> ventas.groupby("region")["importe"].sum()
region
Centro    102068.6
Este       91287.4
Norte     112002.5
Sur       133490.4
Name: importe, dtype: float64
```

Se lee de izquierda a derecha: agrupa por región, quédate con el importe, suma. El resultado es una Series cuyo índice son los grupos.

```python
>>> ventas.groupby("vendedor")["importe"].sum().sort_values(ascending=False).round(2)
vendedor
Ada         111944.0
Grace       107132.2
Margaret     88130.4
Alan         69360.4
Linus        62281.9
Name: importe, dtype: float64
>>> ventas.groupby("categoria")["unidades"].mean().round(1)
categoria
Equipos         1.9
Periféricos     7.2
Servicios       3.1
Software       18.8
Name: unidades, dtype: float64
```

Las agregaciones habituales: `sum`, `mean`, `median`, `min`, `max`, `count`, `nunique`, `std`.

### Varias agregaciones a la vez

`agg` calcula varias medidas y les da nombre. Cada argumento es `nombre=(columna, función)`:

```python
>>> resumen = ventas.groupby("vendedor").agg(
...     ventas=("importe", "count"),
...     unidades=("unidades", "sum"),
...     importe=("importe", "sum"),
... )
>>> resumen.sort_values("importe", ascending=False)
          ventas  unidades   importe
vendedor
Ada           75       541  111944.0
Grace         76       640  107132.2
Margaret      66       491   88130.4
Alan          54       485   69360.4
Linus         49       399   62281.9
```

Los grupos quedan en el índice. `reset_index()` los devuelve a una columna normal, que es lo que suele hacer falta antes de exportar.

### Agrupar por fechas

Con la columna `mes` creada en la unidad 7.4, la evolución mensual es un `groupby` más:

```python
>>> ventas.groupby("mes")["importe"].sum().round(2).tail(3)
mes
2026-08    36720.9
2026-09    72526.9
2026-10    58001.0
Name: importe, dtype: float64
```

### Tablas dinámicas

`pivot_table` es la tabla dinámica de Excel: una variable en las filas, otra en las columnas y una medida en las celdas.

```python
>>> ventas.pivot_table(index="region", columns="categoria", values="importe", aggfunc="sum", fill_value=0)
categoria  Equipos  Periféricos  Servicios  Software
region
Centro     51700.0      12518.1    22080.0   15770.5
Este       50400.0      10360.9    19680.0   10846.5
Norte      68450.0      14177.0    17760.0   11615.5
Sur        81150.0      11029.4    13920.0   27391.0
```

### Combinar tablas con merge

`merge` une dos tablas por una columna común. Es el `JOIN` de SQL.

```python
>>> objetivos = pd.read_csv("datos/objetivos.csv")
>>> totales = ventas.groupby("vendedor")["importe"].sum().reset_index()
>>> combinado = totales.merge(objetivos, on="vendedor", how="left")
>>> combinado["cumplido"] = combinado["importe"] >= combinado["objetivo"]
>>> combinado
   vendedor   importe  objetivo  cumplido
0       Ada  111944.0    100000      True
1      Alan   69360.4     85000     False
2     Grace  107132.2    115000     False
3     Linus   62281.9     60000      True
4  Margaret   88130.4     90000     False
```

| `how` | Filas del resultado | En SQL |
| --- | --- | --- |
| `"inner"` (por defecto) | Las que tienen pareja en las dos tablas | `INNER JOIN` |
| `"left"` | Todas las de la izquierda | `LEFT JOIN` |
| `"right"` | Todas las de la derecha | `RIGHT JOIN` |
| `"outer"` | Todas las de las dos | `FULL OUTER JOIN` |

Con `how="left"`, un vendedor sin objetivo se conserva con el objetivo ausente. Con el valor por defecto desaparecería del resultado sin avisar: después de un `merge`, comprueba siempre el número de filas.

Para apilar tablas con las mismas columnas, por ejemplo un fichero por mes, se usa `pd.concat([enero, febrero])`.

### De SQL a pandas

| SQL | pandas |
| --- | --- |
| `SELECT a, b FROM t` | `t[["a", "b"]]` |
| `WHERE x > 10 AND y = 'A'` | `t[(t["x"] > 10) & (t["y"] == "A")]` |
| `ORDER BY x DESC` | `t.sort_values("x", ascending=False)` |
| `GROUP BY g` con `SUM(x)` | `t.groupby("g")["x"].sum()` |
| `JOIN u ON t.k = u.k` | `t.merge(u, on="k")` |
| `LIMIT 5` | `t.head(5)` |
| `COUNT(DISTINCT x)` | `t["x"].nunique()` |

---

## 7.7 Visualización con Matplotlib

### Figura y ejes

Un gráfico de Matplotlib tiene dos piezas:

- La **figura** (`Figure`) es el lienzo completo, lo que se guarda en un fichero.
- Los **ejes** (`Axes`) son cada uno de los gráficos que hay dentro. Sobre ellos se dibuja.

`plt.subplots()` crea las dos cosas:

```python
import matplotlib.pyplot as plt

por_vendedor = ventas.groupby("vendedor")["importe"].sum().sort_values(ascending=False)

figura, ejes = plt.subplots(figsize=(8, 4.5))
ejes.bar(por_vendedor.index, por_vendedor.values)
ejes.set_title("Importe por vendedor")
ejes.set_ylabel("Importe (€)")
figura.tight_layout()
plt.show()
```

Encontrarás mucho código que llama directamente a `plt.bar()`, `plt.title()` y demás. Funciona, pero dibuja sobre «el gráfico actual», un estado global difícil de controlar en cuanto hay más de un gráfico. La forma con `figura, ejes` es explícita y es la que se usa en el curso.

### Qué gráfico para qué pregunta

| Pregunta | Gráfico | Método |
| --- | --- | --- |
| Comparar categorías | Barras | `ejes.bar(x, y)`, `ejes.barh(y, x)` |
| Ver una evolución en el tiempo | Líneas | `ejes.plot(x, y, marker="o")` |
| Ver cómo se reparten unos valores | Histograma | `ejes.hist(valores, bins=10)` |
| Relacionar dos variables numéricas | Dispersión | `ejes.scatter(x, y)` |

Los gráficos de tarta casi nunca son la mejor opción: comparar ángulos es más difícil que comparar longitudes. Unas barras ordenadas se leen mejor.

```python
mensual = ventas.groupby("mes")["importe"].sum()

figura, ejes = plt.subplots(figsize=(8, 4.5))
ejes.plot(mensual.index, mensual.values, marker="o")
ejes.set_title("Evolución mensual")
ejes.set_ylabel("Importe (€)")
ejes.grid(True, alpha=0.3)
ejes.tick_params(axis="x", rotation=45)
figura.tight_layout()
```

### Un gráfico que se entiende

- Título que dice qué se ve, y etiquetas con unidades en los ejes.
- Barras ordenadas por valor, salvo que la categoría tenga un orden propio, como los meses.
- El eje de un gráfico de barras empieza en cero.
- Un color, salvo que el color signifique algo.
- `figura.tight_layout()` para que no se corten las etiquetas.

### Varios gráficos en una figura

```python
figura, (izquierda, derecha) = plt.subplots(1, 2, figsize=(13, 4.5))
izquierda.bar(por_vendedor.index, por_vendedor.values)
izquierda.set_title("Por vendedor")
derecha.plot(mensual.index, mensual.values, marker="o")
derecha.set_title("Evolución mensual")
figura.suptitle("Ventas de 2026")
figura.tight_layout()
```

`plt.subplots(filas, columnas)` devuelve la figura y un array con los ejes.

### Guardar y cerrar

```python
figura.savefig("importe_por_vendedor.png", dpi=150)
plt.close(figura)
```

En un script que genera muchos gráficos, cierra cada figura después de guardarla. Si no, todas siguen ocupando memoria hasta que termina el programa.

En un cuaderno el gráfico aparece debajo de la celda sin llamar a `plt.show()`. En un script, `plt.show()` abre una ventana y detiene el programa hasta que se cierra: por eso las funciones del curso **devuelven la figura** y dejan que quien las llama decida si la muestra o la guarda. Es la misma separación entre lógica y presentación del resto del curso, y es lo que permite probarlas con tests.

### Gráficos directos desde pandas

Las Series y los DataFrame tienen un método `plot` que llama a Matplotlib por dentro. Para explorar en un cuaderno es lo más rápido:

```python
por_vendedor.plot(kind="bar", title="Importe por vendedor")
mensual.plot(marker="o", title="Evolución mensual")
```

Devuelve los ejes, de modo que se pueden seguir ajustando con los mismos métodos.

---

## 7.8 Ejercicios prácticos

Los ejemplos de la carpeta [`ejemplos/`](ejemplos/) recorren el módulo:

| Fichero | Qué muestra |
| --- | --- |
| `01_numpy.py` | Arrays, vectorización, ejes, máscaras y la comparación de tiempos con un bucle |
| `02_pandas_primer_vistazo.py` | Cargar el CSV e inspeccionarlo |
| `03_seleccion_y_columnas.py` | Filtros, `loc`, `iloc`, columnas nuevas y ordenación |
| `04_limpieza.py` | El fichero sucio, paso a paso |
| `05_agrupar_y_combinar.py` | `groupby`, `agg`, `pivot_table` y `merge` |
| `06_graficos.py` | Barras, líneas y un panel, guardados en PNG |
| `07_cuaderno_exploracion.ipynb` | El mismo análisis en un cuaderno |

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 7, análisis de las ventas del año: [`ejercicios/PRACTICA_7.md`](ejercicios/PRACTICA_7.md)

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Forma correcta |
| --- | --- | --- |
| Recorrer un DataFrame con `for` e `iterrows()` | Funciona, pero cien veces más lento | Operar con las columnas enteras |
| `df[df["a"] > 1 and df["b"] < 5]` | `ValueError`: el valor de verdad de una Series es ambiguo | `df[(df["a"] > 1) & (df["b"] < 5)]` |
| `df[df["a"] > 1 & df["b"] < 5]` | Resultado erróneo o error: `&` tiene más prioridad que `>` | Paréntesis en cada condición |
| `if valor == np.nan` | Siempre `False` | `pd.isna(valor)` |
| `df.sort_values("x")` sin asignar | No pasa nada: devuelve un DataFrame nuevo | `df = df.sort_values("x")` |
| `df[df["x"] > 0]["y"] = 1` | No modifica `df`: asigna sobre una copia temporal | `df.loc[df["x"] > 0, "y"] = 1` |
| Leer números con coma decimal | La columna queda como texto | `decimal=","` o `str.replace` y `to_numeric` |
| `merge` sin revisar el resultado | Filas que desaparecen o se duplican | Comprobar `len()` antes y después |
| `plt.show()` dentro de una función | El programa se detiene y no se puede probar | Devolver la figura |
| Dar por bueno un cuaderno ejecutado a saltos | Resultados que no se pueden reproducir | «Reiniciar y ejecutar todo» |

## Para saber más

- NumPy para principiantes: [numpy.org/doc/stable/user/absolute_beginners.html](https://numpy.org/doc/stable/user/absolute_beginners.html)
- 10 minutos con pandas: [pandas.pydata.org/docs/user_guide/10min.html](https://pandas.pydata.org/docs/user_guide/10min.html)
- pandas para quien viene de SQL: [pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html)
- Galería de Matplotlib: [matplotlib.org/stable/gallery](https://matplotlib.org/stable/gallery/index.html)
- Cuadernos en VS Code: [code.visualstudio.com/docs/datascience/jupyter-notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
