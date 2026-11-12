# Módulo 4. Colecciones y manejo de datos (8 horas)

Al terminar este módulo sabrás elegir la colección adecuada para cada problema y transformar datos con código conciso: filtrar, agrupar, ordenar y resumir sin escribir bucles innecesarios.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 4.1 | Listas | 1,5 h |
| 4.2 | Tuplas | 0,5 h |
| 4.3 | Diccionarios | 1 h |
| 4.4 | Conjuntos | 0,5 h |
| 4.5 | Comprensiones | 1 h |
| 4.6 | Iteración y funciones integradas | 1 h |
| 4.7 | Manipulación de cadenas | 0,5 h |
| 4.8 | Búsqueda, filtrado y ordenación | 0,5 h |
| 4.9 | Ejercicios y Práctica 4 | 1,5 h |

## Qué colección usar

| Colección | Literal | Ordenada | Mutable | Duplicados | Úsala para |
| --- | --- | --- | --- | --- | --- |
| `list` | `[1, 2, 3]` | Sí | Sí | Sí | Secuencias de elementos del mismo tipo que cambian |
| `tuple` | `(1, 2, 3)` | Sí | No | Sí | Registros de tamaño fijo y valores que no deben cambiar |
| `dict` | `{"a": 1}` | Sí, por inserción | Sí | Claves únicas | Buscar un valor a partir de una clave |
| `set` | `{1, 2, 3}` | No | Sí | No | Pertenencia, duplicados y operaciones de conjuntos |

Equivalencias aproximadas: `list` es `ArrayList`, `dict` es `HashMap`, `set` es `HashSet` y `tuple` no tiene equivalente directo en Java.

---

## 4.1 Listas

### Creación y acceso

```python
vacia = []
numeros = [4, 8, 15, 16, 23, 42]
mezcla = [1, "dos", 3.0, None]          # se puede, pero rara vez conviene
letras = list("abc")                    # ['a', 'b', 'c']
ceros = [0] * 5                         # [0, 0, 0, 0, 0]

numeros[0]        # 4      primer elemento
numeros[-1]       # 42     último elemento
numeros[-2]       # 23     penúltimo
len(numeros)      # 6
numeros[10]       # IndexError
```

Los índices negativos cuentan desde el final. No hace falta escribir `numeros[len(numeros) - 1]`.

### Slicing

`lista[inicio:fin:paso]` devuelve una **lista nueva** con los elementos desde `inicio` hasta `fin` sin incluirlo.

```python
numeros = [4, 8, 15, 16, 23, 42]

numeros[1:4]      # [8, 15, 16]
numeros[:3]       # [4, 8, 15]         los tres primeros
numeros[3:]       # [16, 23, 42]       del cuarto en adelante
numeros[-2:]      # [23, 42]           los dos últimos
numeros[::2]      # [4, 15, 23]        uno de cada dos
numeros[::-1]     # [42, 23, 16, 15, 8, 4]   al revés
numeros[:]        # copia completa
numeros[2:100]    # [15, 16, 23, 42]   un slice nunca da IndexError
```

El slicing funciona igual con cadenas y tuplas.

### Modificación

```python
tareas = ["diseñar", "programar"]

tareas.append("probar")                 # añade al final
tareas.insert(0, "analizar")            # inserta en una posición
tareas.extend(["desplegar", "medir"])   # añade varios elementos
tareas[1] = "prototipar"                # sustituye
tareas[1:3] = ["a", "b", "c"]           # sustituye un tramo por otro

ultima = tareas.pop()                   # quita y devuelve el último
primera = tareas.pop(0)                 # quita y devuelve el de la posición 0
tareas.remove("a")                      # quita la primera aparición; ValueError si no está
del tareas[0]                           # borra por posición
tareas.clear()                          # vacía la lista
```

`append` añade **un** elemento; `extend` añade **cada elemento** de otra colección:

```python
a = [1, 2]
a.append([3, 4])      # [1, 2, [3, 4]]
b = [1, 2]
b.extend([3, 4])      # [1, 2, 3, 4]
```

### Búsqueda y consulta

```python
numeros = [4, 8, 15, 16, 23, 42, 8]

8 in numeros          # True
numeros.index(15)     # 2; ValueError si no está
numeros.count(8)      # 2
min(numeros), max(numeros), sum(numeros)
```

### Ordenar: sort() frente a sorted()

```python
numeros = [23, 4, 42, 8]

ordenados = sorted(numeros)       # devuelve una lista NUEVA; numeros no cambia
numeros.sort()                    # ordena EN EL SITIO y devuelve None
numeros.sort(reverse=True)        # de mayor a menor
numeros.reverse()                 # invierte en el sitio
```

El error más repetido del módulo:

```python
numeros = numeros.sort()          # MAL: numeros pasa a valer None
```

Regla general de la librería estándar: un método que **modifica** el objeto devuelve `None`; una función que **crea** uno nuevo lo devuelve. `sort`, `reverse`, `append`, `extend` y `shuffle` devuelven `None`.

### Copias y referencias

Asignar una lista no la copia. Lo vimos en el Módulo 2 y aquí tiene consecuencias:

```python
original = [1, 2, 3]
alias = original              # el mismo objeto
copia = original.copy()       # otro objeto con los mismos elementos; también original[:] o list(original)

alias.append(4)
print(original)               # [1, 2, 3, 4]
print(copia)                  # [1, 2, 3]
```

`copy()` hace una **copia superficial**: copia la lista, pero no los objetos que contiene. Con listas anidadas, las listas interiores siguen compartidas:

```python
import copy

matriz = [[1, 2], [3, 4]]
superficial = matriz.copy()
profunda = copy.deepcopy(matriz)

matriz[0].append(99)
print(superficial[0])         # [1, 2, 99]   comparte la lista interior
print(profunda[0])            # [1, 2]
```

La misma trampa aparece al crear una matriz con `*`:

```python
mal = [[0] * 3] * 2           # dos referencias a LA MISMA fila
mal[0][0] = 1                 # [[1, 0, 0], [1, 0, 0]]

bien = [[0] * 3 for _ in range(2)]    # dos filas independientes
```

### No modifiques una lista mientras la recorres

```python
numeros = [1, 2, 2, 3]
for numero in numeros:
    if numero == 2:
        numeros.remove(numero)       # MAL: se salta elementos
print(numeros)                       # [1, 2, 3]
```

Construye una lista nueva con lo que quieres conservar:

```python
numeros = [numero for numero in numeros if numero != 2]
```

---

## 4.2 Tuplas

Una tupla es una secuencia **inmutable**. Lo que la define es la coma, no los paréntesis.

```python
punto = (3, 4)
tambien = 3, 4                # los paréntesis son opcionales
uno = (5,)                    # tupla de un elemento: la coma es obligatoria
no_es_tupla = (5)             # esto es el entero 5
vacia = ()

punto[0]                      # 3
punto[0] = 10                 # TypeError: no se puede modificar
```

### Desempaquetado

```python
x, y = punto                          # x = 3, y = 4
a, b = b, a                           # intercambio sin variable auxiliar

nombre, *apellidos = ["Ada", "Byron", "Lovelace"]     # el resto, a una lista
primero, *medio, ultimo = [1, 2, 3, 4, 5]             # medio = [2, 3, 4]

for nombre, edad in [("Ada", 36), ("Linus", 28)]:     # desempaquetado en el for
    print(nombre, edad)

cociente, resto = divmod(17, 5)                       # retorno múltiple
```

El guion bajo se usa por convención para las partes que no interesan: `nombre, _, ciudad = registro`.

### Cuándo usar una tupla

- **Como registro de tamaño fijo:** `("Ada", 36, "Londres")`. Cada posición tiene un significado distinto.
- **Como valor que no debe cambiar:** coordenadas, colores RGB, opciones de configuración.
- **Como clave de diccionario o elemento de un conjunto:** las listas no pueden serlo porque son mutables.
- **Para devolver varios valores** desde una función.

```python
distancias = {("Madrid", "Sevilla"): 530, ("Madrid", "Bilbao"): 400}
distancias[("Madrid", "Sevilla")]     # 530
```

Si un registro tiene más de tres o cuatro campos, usa una `namedtuple`, un diccionario o una clase: `empleado[4]` no se entiende al leerlo.

Una tupla es inmutable, pero no necesariamente lo que contiene: en `([1, 2], 3)` la lista interior se puede modificar.

---

## 4.3 Diccionarios

Un diccionario asocia claves con valores. La búsqueda por clave es inmediata, sea cual sea el tamaño.

### Creación y acceso

```python
empleado = {"nombre": "Ada", "edad": 36, "activo": True}
vacio = {}
desde_pares = dict([("a", 1), ("b", 2)])
con_nombres = dict(nombre="Ada", edad=36)

empleado["nombre"]                    # 'Ada'
empleado["salario"]                   # KeyError: la clave no existe
empleado.get("salario")               # None, sin error
empleado.get("salario", 0)            # 0 como valor por defecto
"edad" in empleado                    # True: in comprueba las CLAVES
len(empleado)                         # 3
```

Usa los corchetes cuando la clave **tiene que estar** y un `KeyError` es lo correcto si falta. Usa `get()` cuando la ausencia es un caso normal.

Las claves deben ser inmutables: cadenas, números, tuplas. Los valores pueden ser cualquier cosa.

### Modificación

```python
empleado["salario"] = 42000                       # añade o sustituye
empleado.update({"edad": 37, "ciudad": "Madrid"}) # varias claves a la vez
del empleado["activo"]                            # borra; KeyError si no está
ciudad = empleado.pop("ciudad")                   # quita y devuelve
nada = empleado.pop("no_existe", None)            # con valor por defecto no falla

fusion = {"a": 1, "b": 2} | {"b": 20, "c": 3}     # {'a': 1, 'b': 20, 'c': 3}
```

### Recorrido

```python
precios = {"teclado": 45.0, "raton": 19.9, "monitor": 189.0}

for producto in precios:                          # recorre las claves
    print(producto)

for precio in precios.values():                   # los valores
    print(precio)

for producto, precio in precios.items():          # pares clave y valor
    print(f"{producto}: {precio:.2f} €")
```

La forma `for clave in d: valor = d[clave]` funciona, pero `items()` es la idiomática. Desde Python 3.7 los diccionarios conservan el orden de inserción.

### Patrones: contar y agrupar

Los dos usos más frecuentes de un diccionario en el trabajo diario.

```python
# Contar apariciones
texto = "el gato y el perro"
conteo = {}
for palabra in texto.split():
    conteo[palabra] = conteo.get(palabra, 0) + 1
# {'el': 2, 'gato': 1, 'y': 1, 'perro': 1}

# Agrupar elementos por un criterio
empleados = [("Ada", "IT"), ("Grace", "IT"), ("Linus", "Ventas")]
por_departamento = {}
for nombre, departamento in empleados:
    por_departamento.setdefault(departamento, []).append(nombre)
# {'IT': ['Ada', 'Grace'], 'Ventas': ['Linus']}
```

`setdefault(clave, valor)` devuelve el valor de la clave y, si no existía, la crea antes con ese valor. Los mismos patrones con `collections`, que vimos en el Módulo 3:

```python
from collections import Counter, defaultdict

conteo = Counter(texto.split())

por_departamento = defaultdict(list)
for nombre, departamento in empleados:
    por_departamento[departamento].append(nombre)
```

### Diccionarios anidados

Es la forma natural de representar un JSON. Casi todas las API con las que trabajarás devuelven esto.

```python
pedido = {
    "id": 1042,
    "cliente": {"nombre": "Ada", "ciudad": "Madrid"},
    "lineas": [
        {"producto": "teclado", "unidades": 2, "precio": 45.0},
        {"producto": "raton", "unidades": 1, "precio": 19.9},
    ],
}

pedido["cliente"]["ciudad"]                       # 'Madrid'
pedido["lineas"][0]["producto"]                   # 'teclado'
pedido.get("descuento", {}).get("codigo")         # None, sin KeyError

total = sum(linea["unidades"] * linea["precio"] for linea in pedido["lineas"])
```

---

## 4.4 Conjuntos

Un conjunto es una colección **sin duplicados y sin orden**. Comprobar si un elemento está es inmediato.

```python
lenguajes = {"python", "java", "sql"}
vacio = set()                         # {} es un diccionario vacío, no un conjunto
unicos = set([1, 2, 2, 3, 3, 3])      # {1, 2, 3}

lenguajes.add("go")
lenguajes.discard("cobol")            # no falla si no está
lenguajes.remove("java")              # KeyError si no está
"python" in lenguajes                 # True
```

### Operaciones

```python
backend = {"python", "java", "sql"}
datos = {"python", "sql", "r"}

backend | datos       # unión:               {'python', 'java', 'sql', 'r'}
backend & datos       # intersección:        {'python', 'sql'}
backend - datos       # diferencia:          {'java'}
backend ^ datos       # diferencia simétrica: {'java', 'r'}

{"python"} <= backend         # ¿es subconjunto?  True
backend.isdisjoint({"go"})    # ¿no comparten nada?  True
```

### Usos habituales

```python
# Eliminar duplicados (se pierde el orden)
unicos = list(set(correos))

# Eliminar duplicados conservando el orden
unicos = list(dict.fromkeys(correos))

# Pertenencia rápida: con muchos datos, un conjunto en lugar de una lista
bloqueados = {"spam@x.com", "robot@y.com"}
if correo in bloqueados:
    ...

# Comparar dos colecciones
faltan = requeridos - instalados
```

Los elementos de un conjunto deben ser inmutables, igual que las claves de un diccionario. `frozenset` es la versión inmutable del propio conjunto.

---

## 4.5 Comprensiones

Una comprensión construye una colección a partir de otra en una sola expresión. Es la construcción más característica de Python y la que más vas a leer en código ajeno.

### Comprensión de lista

```python
# Con bucle
cuadrados = []
for n in range(6):
    cuadrados.append(n ** 2)

# Con comprensión
cuadrados = [n ** 2 for n in range(6)]            # [0, 1, 4, 9, 16, 25]
```

La forma general es `[expresión for elemento in iterable if condición]`:

```python
pares = [n for n in range(10) if n % 2 == 0]              # filtrar
mayusculas = [nombre.upper() for nombre in nombres]       # transformar
largos = [n.upper() for n in nombres if len(n) > 3]       # las dos cosas
```

Se lee como la definición matemática: «el cuadrado de n, para cada n del rango, si n es par».

Con expresión condicional, que va **delante** del `for` porque forma parte de la expresión:

```python
etiquetas = ["par" if n % 2 == 0 else "impar" for n in range(4)]
```

### Comprensión de diccionario y de conjunto

```python
longitudes = {palabra: len(palabra) for palabra in ["uva", "kiwi"]}   # {'uva': 3, 'kiwi': 4}
invertido = {valor: clave for clave, valor in original.items()}
caros = {p: precio for p, precio in precios.items() if precio > 40}

iniciales = {nombre[0] for nombre in nombres}                         # conjunto
```

### Expresiones generadoras

Con paréntesis en lugar de corchetes no se crea la lista: los valores se producen uno a uno a medida que se piden. Es lo adecuado cuando el resultado se consume una sola vez.

```python
total = sum(linea["importe"] for linea in lineas)         # sin lista intermedia
hay_negativos = any(n < 0 for n in numeros)
todos_validos = all(es_email(c) for c in correos)
texto = ", ".join(str(n) for n in numeros)
```

### Comprensiones anidadas

```python
matriz = [[1, 2, 3], [4, 5, 6]]

plana = [valor for fila in matriz for valor in fila]          # [1, 2, 3, 4, 5, 6]
traspuesta = [[fila[i] for fila in matriz] for i in range(3)] # [[1, 4], [2, 5], [3, 6]]
```

Los `for` se escriben en el mismo orden que tendrían como bucles anidados.

### Cuándo no usar una comprensión

- Cuando no cabe cómodamente en una o dos líneas.
- Cuando necesita más de dos `for` o condiciones enrevesadas.
- Cuando solo interesa el efecto secundario: `[print(x) for x in datos]` es un bucle mal escrito.

Una comprensión es para **construir una colección**. Si no vas a usar el resultado, escribe un `for`.

---

## 4.6 Iteración y funciones integradas

### enumerate y zip

```python
lenguajes = ["Python", "Java", "C#"]
anios = [1991, 1995, 2000]

for posicion, lenguaje in enumerate(lenguajes, start=1):
    print(posicion, lenguaje)

for lenguaje, anio in zip(lenguajes, anios):          # recorre dos colecciones en paralelo
    print(lenguaje, anio)

por_lenguaje = dict(zip(lenguajes, anios))            # {'Python': 1991, ...}
pares = list(zip(lenguajes, anios))                   # [('Python', 1991), ...]
```

`zip` se detiene al acabar la colección más corta. Con `zip(a, b, strict=True)` lanza un error si las longitudes no coinciden.

### Funciones de resumen

```python
notas = [7.5, 4.0, 9.0, 6.5]

len(notas)                    # 4
sum(notas)                    # 27.0
min(notas), max(notas)        # 4.0 9.0
sum(notas) / len(notas)       # media: 6.75
any(nota < 5 for nota in notas)       # True: ¿alguna cumple?
all(nota >= 5 for nota in notas)      # False: ¿todas cumplen?
```

`min()` y `max()` lanzan `ValueError` con una colección vacía. El parámetro `default` lo evita: `max(notas, default=0)`.

### sorted con key

`key` recibe una función que se aplica a cada elemento para obtener el valor por el que se ordena. También lo aceptan `min()`, `max()` y `list.sort()`.

```python
palabras = ["kiwi", "Manzana", "uva"]

sorted(palabras)                          # ['Manzana', 'kiwi', 'uva']: las mayúsculas van antes
sorted(palabras, key=str.lower)           # ['kiwi', 'Manzana', 'uva']
sorted(palabras, key=len, reverse=True)   # ['Manzana', 'kiwi', 'uva']
max(palabras, key=len)                    # 'Manzana'
```

### Otras funciones útiles

```python
list(reversed(lenguajes))                 # recorre al revés sin modificar
list(range(0, 10, 2))                     # [0, 2, 4, 6, 8]
list(map(str.upper, lenguajes))           # equivale a [l.upper() for l in lenguajes]
list(filter(str.isdigit, ["1", "a"]))     # equivale a [x for x in ... if x.isdigit()]
```

`map` y `filter` existen y los verás en código ajeno, pero en Python se prefieren las comprensiones.

### Iterables e iteradores

Todo lo que se puede recorrer con `for` es un **iterable**: listas, tuplas, cadenas, diccionarios, conjuntos, rangos, ficheros. Funciones como `zip`, `enumerate`, `map` y `reversed` devuelven **iteradores**: producen los valores bajo demanda y **se agotan** tras recorrerlos una vez.

```python
pares = zip([1, 2], ["a", "b"])
print(list(pares))        # [(1, 'a'), (2, 'b')]
print(list(pares))        # []: ya se ha consumido
```

Si necesitas recorrerlo más de una vez, conviértelo en lista.

---

## 4.7 Manipulación de cadenas

Una cadena es una secuencia inmutable de caracteres. Todo lo visto sobre índices y slicing se aplica igual. Los métodos nunca modifican la cadena: devuelven una nueva.

```python
texto = "  Programación en Python  "

texto.strip()                     # 'Programación en Python'; también lstrip() y rstrip()
texto.lower(), texto.upper()
texto.strip().title()             # 'Programación En Python'
texto.replace("Python", "Java")
texto.strip().startswith("Pro")   # True
texto.strip().endswith(".py")     # False
"Python" in texto                 # True
texto.find("Python")              # 18: posición, o -1 si no está
texto.count("o")                  # 2: la «ó» con tilde es otro carácter
texto.strip()[::-1]               # al revés
```

### split y join

Son la pareja más usada para procesar texto.

```python
linea = "Ada;Lovelace;36;Londres"
campos = linea.split(";")                 # ['Ada', 'Lovelace', '36', 'Londres']
";".join(campos)                          # de vuelta a la cadena

"uno  dos   tres".split()                 # sin argumento: parte por cualquier espacio en blanco
"a,b,,c".split(",")                       # ['a', 'b', '', 'c']
"clave=valor=x".split("=", 1)             # ['clave', 'valor=x']: como mucho un corte
"linea 1\nlinea 2".splitlines()           # ['linea 1', 'linea 2']
clave, _, valor = "puerto=8080".partition("=")
```

`join` es un método **del separador**, no de la lista, y solo acepta cadenas:

```python
", ".join(["a", "b"])                     # 'a, b'
", ".join(str(n) for n in [1, 2, 3])      # hay que convertir los números
```

### Construir cadenas

No concatenes con `+=` dentro de un bucle: cada vuelta crea una cadena nueva. Acumula las partes en una lista y únelas al final.

```python
lineas = []
for producto, precio in precios.items():
    lineas.append(f"{producto:<12}{precio:>8.2f}")
informe = "\n".join(lineas)
```

### Comprobaciones

```python
"12345".isdigit()         # True
"abc".isalpha()           # True
"abc123".isalnum()        # True
"   ".isspace()           # True
"Hola".islower()          # False
```

### Formato

Repaso del Módulo 2, que aquí se usa mucho para generar informes:

```python
f"{nombre:<10}|"          # alineado a la izquierda en 10 caracteres
f"{importe:>10.2f}"       # a la derecha, dos decimales
f"{titulo:^20}"           # centrado
f"{total:,.2f}"           # separador de miles: 1,234.50
f"{ratio:.1%}"            # porcentaje: 12.5%
f"{numero:05d}"           # ceros a la izquierda: 00042
"-" * 30                  # una línea de guiones
```

---

## 4.8 Búsqueda, filtrado y ordenación

La estructura de datos más común en un proyecto real es una **lista de diccionarios**: es lo que se obtiene al leer un CSV, consultar una base de datos o llamar a una API.

```python
empleados = [
    {"nombre": "Ada", "departamento": "IT", "salario": 52000},
    {"nombre": "Linus", "departamento": "IT", "salario": 48000},
    {"nombre": "Grace", "departamento": "Ventas", "salario": 45000},
    {"nombre": "Alan", "departamento": "Ventas", "salario": 39000},
]
```

### Buscar un elemento

```python
ada = next((e for e in empleados if e["nombre"] == "Ada"), None)
```

`next()` devuelve el primer elemento que produce el generador y se detiene ahí. El segundo argumento es lo que devuelve si no hay ninguno.

Si vas a buscar muchas veces por el mismo campo, construye un índice una sola vez:

```python
por_nombre = {e["nombre"]: e for e in empleados}
por_nombre["Grace"]["salario"]        # 45000, sin recorrer la lista
```

### Filtrar

```python
de_it = [e for e in empleados if e["departamento"] == "IT"]
bien_pagados = [e["nombre"] for e in empleados if e["salario"] > 45000]
```

### Ordenar

```python
por_salario = sorted(empleados, key=lambda e: e["salario"], reverse=True)

# Por varios criterios: una tupla como clave
por_dep_y_nombre = sorted(empleados, key=lambda e: (e["departamento"], e["nombre"]))

# Un criterio ascendente y otro descendente: el signo menos en los numéricos
por_dep_y_salario = sorted(empleados, key=lambda e: (e["departamento"], -e["salario"]))
```

`operator.itemgetter` hace lo mismo que la lambda y se lee bien:

```python
from operator import itemgetter

sorted(empleados, key=itemgetter("salario"))
sorted(empleados, key=itemgetter("departamento", "nombre"))
```

La ordenación de Python es **estable**: los elementos con la misma clave conservan su orden relativo. Eso permite ordenar en dos pasadas, primero por el criterio secundario y después por el principal.

### Los primeros N

```python
top_2 = sorted(empleados, key=itemgetter("salario"), reverse=True)[:2]
```

### Agrupar y resumir

```python
from collections import defaultdict

masa_salarial = defaultdict(int)
for e in empleados:
    masa_salarial[e["departamento"]] += e["salario"]
# {'IT': 100000, 'Ventas': 84000}

plantilla = defaultdict(list)
for e in empleados:
    plantilla[e["departamento"]].append(e["nombre"])
# {'IT': ['Ada', 'Linus'], 'Ventas': ['Grace', 'Alan']}

media = {dep: masa_salarial[dep] / len(nombres) for dep, nombres in plantilla.items()}
```

Con estas cuatro operaciones, buscar, filtrar, ordenar y agrupar, se resuelve la mayor parte del tratamiento de datos que no necesita una base de datos. Es también lo que hace por dentro una consulta SQL:

| SQL | Python |
| --- | --- |
| `WHERE departamento = 'IT'` | `[e for e in empleados if e["departamento"] == "IT"]` |
| `SELECT nombre` | `[e["nombre"] for e in empleados]` |
| `ORDER BY salario DESC` | `sorted(empleados, key=itemgetter("salario"), reverse=True)` |
| `LIMIT 2` | `[:2]` |
| `GROUP BY departamento` | Diccionario o `defaultdict` con la clave de agrupación |
| `COUNT(*)`, `SUM(salario)` | `len(...)`, `sum(e["salario"] for e in ...)` |

---

## 4.9 Ejercicios y Práctica 4

Los ejemplos de la carpeta [`ejemplos/`](ejemplos/) recorren el módulo:

| Fichero | Qué muestra |
| --- | --- |
| `01_listas.py` | Slicing, métodos, `sort` frente a `sorted`, copias y la trampa de `[[0] * 3] * 2` |
| `02_tuplas.py` | Desempaquetado, tuplas como registros y como claves |
| `03_diccionarios.py` | Acceso con `get`, recorrido, contar, agrupar y anidados |
| `04_conjuntos.py` | Operaciones de conjuntos y eliminación de duplicados |
| `05_comprensiones.py` | Comprensiones de lista, diccionario y conjunto, y generadores |
| `06_iteracion.py` | `enumerate`, `zip`, funciones de resumen y `sorted` con `key` |
| `07_cadenas.py` | `split`, `join`, limpieza y formato de informes |
| `08_lista_de_diccionarios.py` | Buscar, filtrar, ordenar y agrupar registros |

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 4, análisis de ventas: [`ejercicios/PRACTICA_4.md`](ejercicios/PRACTICA_4.md)

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Forma correcta |
| --- | --- | --- |
| `lista = lista.sort()` | `lista` pasa a valer `None` | `lista.sort()` o `lista = sorted(lista)` |
| `copia = original` | Las dos variables son la misma lista | `original.copy()` |
| `[[0] * 3] * 2` | Todas las filas son la misma lista | `[[0] * 3 for _ in range(2)]` |
| Borrar elementos mientras se recorre | Se saltan elementos | Construir una lista nueva con una comprensión |
| `d[clave]` sin saber si existe | `KeyError` | `d.get(clave, por_defecto)` |
| `vacio = {}` esperando un conjunto | Es un diccionario | `set()` |
| `(5)` esperando una tupla | Es el entero 5 | `(5,)` |
| `lista.join(", ")` | `AttributeError` | `", ".join(lista)` |
| `", ".join([1, 2])` | `TypeError` | `", ".join(str(n) for n in [1, 2])` |
| `texto.strip()` sin asignar | La cadena original no cambia | `texto = texto.strip()` |
| `for i in range(len(a)): a[i], b[i]` | Funciona, pero no es idiomático | `for x, y in zip(a, b)` |
| Recorrer dos veces un `zip` o un `map` | La segunda vez está vacío | Convertirlo antes en lista |
| `if clave in d.keys()` | Funciona, pero sobra | `if clave in d` |

## Para saber más

- Estructuras de datos en el tutorial oficial: [docs.python.org/es/3/tutorial/datastructures.html](https://docs.python.org/es/3/tutorial/datastructures.html)
- Métodos de las cadenas: [docs.python.org/es/3/library/stdtypes.html#string-methods](https://docs.python.org/es/3/library/stdtypes.html#string-methods)
- Cómo ordenar: [docs.python.org/es/3/howto/sorting.html](https://docs.python.org/es/3/howto/sorting.html)
- Módulo `collections`: [docs.python.org/es/3/library/collections.html](https://docs.python.org/es/3/library/collections.html)
