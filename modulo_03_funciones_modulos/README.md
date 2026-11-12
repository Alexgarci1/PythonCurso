# Módulo 3. Funciones y módulos (6 horas)

Al terminar este módulo sabrás organizar un programa en funciones y módulos reutilizables y documentados, y conocerás las partes de la librería estándar que más se usan a diario.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 3.1 | Definición de funciones | 1 h |
| 3.2 | Parámetros y retorno | 1,5 h |
| 3.3 | Ámbito de variables | 1 h |
| 3.4 | Módulos y paquetes | 1 h |
| 3.5 | Librerías estándar | 0,5 h |
| 3.6 | Práctica 3 | 1 h |

---

## 3.1 Definición de funciones

### Anatomía de una función

```python
def precio_con_iva(precio: float, iva: float = 21) -> float:
    """Devuelve el precio con el IVA aplicado.

    ``iva`` es un porcentaje. El resultado se redondea a dos decimales.
    """
    return round(precio * (1 + iva / 100), 2)
```

| Parte | Qué es |
| --- | --- |
| `def` | Palabra clave que define la función |
| `precio_con_iva` | Nombre, en `snake_case` y con un verbo o una descripción del resultado |
| `precio: float` | Parámetro con anotación de tipo, opcional pero recomendada |
| `iva: float = 21` | Parámetro con valor por defecto |
| `-> float` | Anotación del tipo de retorno |
| `"""..."""` | Docstring: documentación que muestra `help()` |
| `return` | Devuelve el resultado y termina la función |

No hay modificadores de acceso, ni tipo de retorno obligatorio, ni clase contenedora. Una función vive directamente en el módulo.

### return

Una función que termina sin ejecutar `return` devuelve `None`. Es un error frecuente olvidar el `return` y encontrarse un `None` inesperado más adelante.

```python
def saludar(nombre):
    print(f"Hola, {nombre}")      # imprime, pero no devuelve nada


resultado = saludar("Ada")
print(resultado)                  # None
```

Distingue siempre entre **devolver** un valor (`return`) e **imprimirlo** (`print`). Una función que devuelve se puede reutilizar, componer y probar; una que imprime, no.

### Docstrings

La primera cadena del cuerpo de una función es su docstring. Se escribe con triples comillas, en imperativo o describiendo el resultado, y explica **qué** hace la función, no cómo.

```python
def es_bisiesto(anio: int) -> bool:
    """Indica si un año es bisiesto.

    >>> es_bisiesto(2024)
    True
    """
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
```

Los ejemplos que empiezan por `>>>` son *doctests*: documentación que además se puede ejecutar como test con `python -m doctest fichero.py`.

### Las funciones son objetos

En Python una función es un objeto como cualquier otro. Se puede asignar a una variable, guardar en una colección, pasar como argumento y devolver desde otra función.

```python
def doble(x):
    return x * 2


operacion = doble            # sin paréntesis: se refiere a la función
print(operacion(5))          # 10
print(doble.__name__)        # 'doble'

operaciones = {"doble": doble, "absoluto": abs}
print(operaciones["doble"](7))   # 14
```

`doble` es la función; `doble(5)` es el resultado de llamarla. Confundir ambas cosas es el origen de muchos errores.

A una función que recibe o devuelve otras funciones se la llama **función de orden superior**:

```python
def aplicar_dos_veces(funcion, valor):
    return funcion(funcion(valor))


aplicar_dos_veces(doble, 3)      # 12
```

Es lo que en Java se hace con interfaces funcionales y en C# con delegados, pero sin ceremonia: la función se pasa tal cual.

### Qué hace buena a una función

- **Hace una sola cosa.** Si para describirla necesitas la palabra «y», probablemente son dos.
- **Tiene un nombre que dice lo que hace.** `calcular_irpf` mejor que `proceso` o `calc2`.
- **Es corta.** Si no cabe en pantalla, extrae partes a funciones auxiliares.
- **No tiene efectos ocultos.** Recibe datos, devuelve un resultado y no modifica nada por el camino.
- **Separa cálculo de entrada y salida.** Como ya vimos en el Módulo 2.

---

## 3.2 Parámetros y retorno

### Argumentos posicionales y por nombre

```python
def crear_cuenta(titular, saldo, moneda):
    return f"{titular}: {saldo} {moneda}"


crear_cuenta("Ada", 100, "EUR")                           # posicionales
crear_cuenta(titular="Ada", saldo=100, moneda="EUR")      # por nombre
crear_cuenta(moneda="EUR", titular="Ada", saldo=100)      # por nombre, en otro orden
crear_cuenta("Ada", moneda="EUR", saldo=100)              # mezcla: los posicionales van primero
```

Pasar los argumentos por nombre hace la llamada más legible y la protege si cambia el orden de los parámetros. Es una de las costumbres que distinguen al código Python.

### Valores por defecto

```python
def conectar(host, puerto=5432, timeout=30):
    ...


conectar("localhost")
conectar("localhost", 3306)
conectar("localhost", timeout=5)
```

Los parámetros con valor por defecto van después de los que no lo tienen.

### El error del valor por defecto mutable

Este es el error más famoso del lenguaje. Los valores por defecto se evalúan **una sola vez**, cuando se define la función, no en cada llamada.

```python
def anadir(elemento, lista=[]):       # MAL
    lista.append(elemento)
    return lista


print(anadir(1))    # [1]
print(anadir(2))    # [1, 2]   ← la lista se comparte entre llamadas
print(anadir(3))    # [1, 2, 3]
```

Todas las llamadas comparten el mismo objeto lista. La solución es usar `None` como valor por defecto y crear el objeto dentro:

```python
def anadir(elemento, lista=None):     # BIEN
    if lista is None:
        lista = []
    lista.append(elemento)
    return lista
```

Regla: **nunca uses un objeto mutable** (`[]`, `{}`, `set()`) como valor por defecto.

### Número variable de argumentos: *args y **kwargs

`*args` recoge en una tupla los argumentos posicionales sobrantes. `**kwargs` recoge en un diccionario los argumentos por nombre sobrantes.

```python
def sumar(*numeros):
    total = 0
    for numero in numeros:
        total += numero
    return total


sumar()                # 0
sumar(1, 2, 3)         # 6


def crear_etiqueta(nombre, **atributos):
    partes = [f'{clave}="{valor}"' for clave, valor in atributos.items()]
    return f"<{nombre} {' '.join(partes)}>"


crear_etiqueta("a", href="/inicio", title="Inicio")
# '<a href="/inicio" title="Inicio">'
```

Los nombres `args` y `kwargs` son solo una convención; lo que cuenta son los asteriscos.

Los mismos asteriscos sirven en la llamada para **desempaquetar** una colección en argumentos:

```python
medidas = (3, 4)
area_rectangulo(*medidas)                 # equivale a area_rectangulo(3, 4)

opciones = {"puerto": 3306, "timeout": 5}
conectar("localhost", **opciones)         # equivale a conectar("localhost", puerto=3306, timeout=5)
```

### Parámetros solo por nombre

Todo lo que va después de un `*` suelto en la firma solo se puede pasar por nombre. Es muy útil para los parámetros booleanos, que por posición resultan ilegibles:

```python
def exportar(datos, *, comprimir=False, sobrescribir=False):
    ...


exportar(datos, True, False)                        # TypeError
exportar(datos, comprimir=True, sobrescribir=False) # claro en la llamada
```

El orden completo de una firma es: posicionales, `*args`, solo por nombre, `**kwargs`.

```python
def ejemplo(a, b=2, *args, c, d=4, **kwargs):
    ...
```

### Retorno múltiple

Una función puede devolver varios valores separándolos por comas. En realidad devuelve una tupla, que se desempaqueta en la llamada:

```python
def minimo_y_maximo(numeros):
    return min(numeros), max(numeros)


menor, mayor = minimo_y_maximo([4, 8, 15, 16, 23, 42])
```

No hacen falta parámetros de salida ni clases envoltorio.

### Paso de argumentos: por referencia a objeto

Python no pasa «por valor» ni «por referencia» en el sentido de C. Pasa **la referencia al objeto**, que es lo mismo que ocurre en una asignación. Consecuencias:

```python
def reasignar(lista):
    lista = [0]            # el nombre local apunta a otro objeto: fuera no cambia


def modificar(lista):
    lista.append(0)        # se modifica el objeto compartido: fuera sí cambia


numeros = [1, 2]
reasignar(numeros)
print(numeros)             # [1, 2]
modificar(numeros)
print(numeros)             # [1, 2, 0]
```

Buena práctica: una función no debería modificar los argumentos que recibe, salvo que ese sea su propósito declarado. Si necesitas transformarlos, devuelve un objeto nuevo.

### Anotaciones de tipo en las firmas

```python
def buscar(nombre: str, edad: int | None = None) -> list[str]:
    ...
```

`int | None` significa «un entero o `None`». `list[str]` es una lista de cadenas. Las anotaciones no se comprueban al ejecutar, pero el editor las usa para autocompletar y avisar de errores.

---

## 3.3 Ámbito de variables

### La regla LEGB

Cuando usas un nombre, Python lo busca en cuatro ámbitos, en este orden:

| Letra | Ámbito | Qué contiene |
| --- | --- | --- |
| **L** | Local | Los nombres definidos dentro de la función actual |
| **E** | Envolvente (*enclosing*) | Los de la función que contiene a la actual, si la hay |
| **G** | Global | Los definidos a nivel de módulo |
| **B** | Integrado (*built-in*) | Los que trae Python: `print`, `len`, `int`... |

```python
mensaje = "global"


def exterior():
    mensaje = "envolvente"

    def interior():
        mensaje = "local"
        print(mensaje)

    interior()


exterior()     # local
```

Una diferencia importante con Java y C#: **los bloques no crean ámbito**. Solo lo crean las funciones, las clases y los módulos. Una variable definida dentro de un `if` o de un `for` sigue existiendo al salir del bloque.

```python
for i in range(3):
    ultimo = i

print(i, ultimo)     # 2 2: ambas siguen existiendo
```

### Leer es fácil, asignar crea un nombre local

Dentro de una función puedes **leer** una variable global sin hacer nada especial. Pero en cuanto le **asignas** un valor, Python crea una variable local con ese nombre:

```python
contador = 0


def incrementar():
    contador += 1        # UnboundLocalError


incrementar()
```

El error aparece porque la asignación convierte a `contador` en local en toda la función, y se intenta leer antes de tener valor.

### global y nonlocal

`global` declara que un nombre se refiere a la variable del módulo. `nonlocal` hace lo mismo con la variable de la función envolvente.

```python
contador = 0


def incrementar():
    global contador
    contador += 1
```

`global` casi siempre indica un problema de diseño: la función depende de un estado oculto y es difícil de probar. La alternativa es pasar el valor como argumento y devolver el nuevo:

```python
def incrementar(contador):
    return contador + 1


contador = incrementar(contador)
```

Las constantes de módulo, en cambio, se leen desde cualquier función sin problema ni declaración.

### Funciones anidadas y cierres

Una función definida dentro de otra recuerda las variables de la función que la contiene, incluso después de que esta haya terminado. A eso se le llama **cierre** (*closure*).

```python
def crear_multiplicador(factor):
    def multiplicar(numero):
        return numero * factor      # factor viene del ámbito envolvente

    return multiplicar


triple = crear_multiplicador(3)
print(triple(10))                   # 30
```

Con `nonlocal` el cierre puede además modificar esa variable y mantener estado entre llamadas:

```python
def crear_contador():
    cuenta = 0

    def siguiente():
        nonlocal cuenta
        cuenta += 1
        return cuenta

    return siguiente


contador = crear_contador()
print(contador(), contador(), contador())    # 1 2 3
```

### Funciones lambda

Una `lambda` es una función anónima de una sola expresión. No lleva `return`: devuelve el valor de la expresión.

```python
doble = lambda x: x * 2          # equivale a def doble(x): return x * 2
```

Su uso natural es pasar una función corta como argumento, sobre todo como criterio de ordenación:

```python
palabras = ["kiwi", "manzana", "uva"]

sorted(palabras, key=len)                          # ['uva', 'kiwi', 'manzana']
sorted(palabras, key=lambda palabra: palabra[-1])  # por la última letra

empleados = [("Ada", 36), ("Linus", 28), ("Grace", 45)]
max(empleados, key=lambda empleado: empleado[1])   # ('Grace', 45)
```

Si la lambda necesita más de una expresión o un nombre para entenderse, usa `def`.

### No tapes los nombres integrados

Como el ámbito integrado se consulta el último, puedes tapar sin querer una función de Python:

```python
list = [1, 2, 3]        # a partir de aquí, list() ya no funciona
sum = 0
id = 42
```

Evita usar como nombre de variable `list`, `dict`, `str`, `sum`, `max`, `min`, `id`, `type`, `input` o `file`.

---

## 3.4 Módulos y paquetes

### Un módulo es un fichero

Cualquier fichero `.py` es un módulo. Su nombre es el del fichero sin la extensión, y lo que define se usa desde otro fichero con `import`.

```python
# geometria.py
PI = 3.14159


def area_circulo(radio):
    return PI * radio ** 2
```

```python
# principal.py
import geometria

print(geometria.area_circulo(2))
print(geometria.PI)
```

### Formas de importar

| Sentencia | Cómo se usa después | Cuándo |
| --- | --- | --- |
| `import geometria` | `geometria.area_circulo(2)` | La forma por defecto: deja claro de dónde viene cada nombre |
| `from geometria import area_circulo` | `area_circulo(2)` | Cuando usas pocas cosas muchas veces |
| `import geometria as geo` | `geo.area_circulo(2)` | Nombres largos o alias convencionales, como `import numpy as np` |
| `from geometria import *` | `area_circulo(2)` | **Nunca** en código real: no sabes qué nombres estás trayendo |

Los `import` van al principio del fichero, en tres grupos separados por una línea en blanco: librería estándar, paquetes de terceros y módulos propios.

### Qué ocurre al importar

La primera vez que se importa un módulo, Python **ejecuta todo su código** de arriba abajo y guarda el resultado. Las siguientes importaciones reutilizan lo guardado.

Por eso el código suelto a nivel de módulo es peligroso: se ejecuta al importar. Y por eso existe este patrón:

```python
def main():
    print(area_circulo(2))


if __name__ == "__main__":
    main()
```

`__name__` vale `"__main__"` cuando el fichero se ejecuta directamente y vale el nombre del módulo cuando se importa. El bloque solo se ejecuta en el primer caso, de modo que el fichero sirve a la vez como programa y como librería.

### Paquetes

Un paquete es una carpeta que agrupa módulos. Lleva un fichero `__init__.py`, que puede estar vacío y que se ejecuta al importar el paquete.

```
tienda/
├── __init__.py
├── precios.py
└── inventario.py
```

```python
import tienda.precios
from tienda import inventario
from tienda.precios import aplicar_descuento
```

El `__init__.py` se usa a menudo para ofrecer una interfaz cómoda, reexportando lo más importante:

```python
# tienda/__init__.py
from tienda.precios import aplicar_descuento, precio_con_iva

__all__ = ["aplicar_descuento", "precio_con_iva"]
```

Así quien usa el paquete escribe `from tienda import precio_con_iva` sin conocer la organización interna.

Dentro de un paquete, un módulo puede importar a un vecino con una importación relativa: `from . import precios` o `from .precios import precio_con_iva`.

### Dónde busca Python los módulos

Al importar, Python busca en este orden: la carpeta del script que se está ejecutando, las carpetas de la variable de entorno `PYTHONPATH`, la librería estándar y los paquetes instalados en el entorno virtual. La lista completa está en `sys.path`.

Dos consecuencias prácticas:

- No llames a tus ficheros como un módulo de la librería estándar. Un `random.py` o un `math.py` propio tapará al original.
- Si un `import` falla con `ModuleNotFoundError`, casi siempre es porque ejecutas desde otra carpeta o con otro intérprete.

### Estructura de un proyecto pequeño

```
mi_proyecto/
├── README.md
├── requirements.txt
├── .gitignore
├── mi_paquete/
│   ├── __init__.py
│   ├── modelos.py
│   └── servicios.py
├── tests/
│   └── test_servicios.py
└── main.py
```

---

## 3.5 Librerías estándar

Python trae una librería estándar muy amplia. Antes de escribir una utilidad o de instalar un paquete, comprueba si ya existe.

### math

```python
import math

math.sqrt(16)          # 4.0
math.pi                # 3.141592653589793
math.ceil(4.1)         # 5
math.floor(4.9)        # 4
math.hypot(3, 4)       # 5.0
math.isclose(0.1 + 0.2, 0.3)   # True
```

### random

```python
import random

random.randint(1, 6)                    # entero entre 1 y 6, ambos incluidos
random.random()                         # decimal en [0, 1)
random.choice(["rojo", "verde"])        # un elemento al azar
random.shuffle(baraja)                  # desordena la lista en el sitio
random.sample(range(1, 50), 6)          # seis valores distintos

generador = random.Random(42)           # generador propio con semilla: resultados repetibles
generador.randint(1, 6)
```

Para contraseñas, tokens y cualquier cosa relacionada con seguridad se usa el módulo `secrets`, no `random`.

### datetime

```python
from datetime import date, datetime, timedelta

hoy = date.today()
navidad = date(2026, 12, 25)
(navidad - hoy).days                         # días que faltan

ahora = datetime.now()
ahora + timedelta(hours=8)                   # dentro de ocho horas

date.fromisoformat("2026-11-19")             # de texto ISO a fecha
datetime.strptime("19/11/2026", "%d/%m/%Y")  # de texto con formato a fecha y hora
hoy.strftime("%d/%m/%Y")                     # de fecha a texto
hoy.weekday()                                # 0 lunes ... 6 domingo
```

### pathlib

`pathlib` representa rutas como objetos y funciona igual en Windows, macOS y Linux. Sustituye a las funciones antiguas de `os.path`.

```python
from pathlib import Path

ruta = Path("datos") / "ventas" / "enero.csv"    # / une partes de la ruta
ruta.name          # 'enero.csv'
ruta.stem          # 'enero'
ruta.suffix        # '.csv'
ruta.parent        # Path('datos/ventas')
ruta.exists()      # ¿existe en disco?

Path(__file__).parent      # la carpeta del fichero actual
Path.cwd()                 # la carpeta de trabajo
Path.home()                # la carpeta del usuario

for fichero in Path("datos").glob("*.csv"):
    print(fichero)
```

Se usa a fondo en el Módulo 6.

### collections

```python
from collections import Counter, defaultdict, namedtuple

Counter("mississippi").most_common(2)     # [('i', 4), ('s', 4)]

grupos = defaultdict(list)                # diccionario que crea el valor si falta la clave
grupos["frutas"].append("kiwi")

Punto = namedtuple("Punto", ["x", "y"])   # tupla con nombres de campo
p = Punto(3, 4)
p.x, p.y
```

### Otros módulos que conviene conocer

| Módulo | Para qué |
| --- | --- |
| `json` | Leer y escribir JSON |
| `csv` | Leer y escribir CSV |
| `os`, `sys` | Sistema operativo, variables de entorno y argumentos del programa |
| `re` | Expresiones regulares |
| `itertools`, `functools` | Herramientas para iteradores y funciones |
| `logging` | Registro de eventos |
| `argparse` | Argumentos de línea de comandos |
| `unittest` | Tests, incluido en la librería estándar |
| `statistics` | Media, mediana, desviación típica |

La referencia completa está en [docs.python.org/es/3/library](https://docs.python.org/es/3/library/).

---

## 3.6 Práctica 3

Los ejemplos de la carpeta [`ejemplos/`](ejemplos/) recorren el módulo:

| Fichero | Qué muestra |
| --- | --- |
| `01_definicion.py` | Definición, docstrings, `return` frente a `print` y funciones como objetos |
| `02_parametros.py` | Argumentos por nombre, valores por defecto, `*args`, `**kwargs` y retorno múltiple |
| `03_ambito.py` | Regla LEGB, `global`, `nonlocal`, cierres y lambdas |
| `04_usar_paquete.py` y `tienda/` | Un paquete con dos módulos y un programa que lo usa |
| `05_libreria_estandar.py` | `math`, `random`, `datetime`, `pathlib` y `collections` |

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 3, librería de validación: [`ejercicios/PRACTICA_3.md`](ejercicios/PRACTICA_3.md)

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Forma correcta |
| --- | --- | --- |
| Olvidar el `return` | La función devuelve `None` | Devolver el resultado de forma explícita |
| `def f(x, lista=[])` | La lista se comparte entre llamadas | `lista=None` y crearla dentro |
| `resultado = funcion` | Se asigna la función, no su resultado | `resultado = funcion()` |
| Modificar una global sin `global` | `UnboundLocalError` | Pasarla como argumento y devolver el valor nuevo |
| Esperar que un `if` o un `for` cree ámbito | La variable sigue existiendo fuera | Solo las funciones crean ámbito |
| `from modulo import *` | No se sabe de dónde viene cada nombre | Importar nombres concretos |
| Llamar a un fichero `random.py` | Tapa al módulo estándar | Elegir otro nombre |
| Código suelto a nivel de módulo | Se ejecuta al importar | Meterlo en `main()` bajo `if __name__ == "__main__"` |
| Sobrecargar funciones como en Java | La segunda definición sustituye a la primera | Valores por defecto o `*args` |

Sobre el último punto: Python no tiene sobrecarga. Si defines dos funciones con el mismo nombre, la segunda reemplaza a la primera. Lo que en Java resuelves con varias firmas, aquí se resuelve con parámetros opcionales.

## Para saber más

- Definición de funciones en el tutorial oficial: [docs.python.org/es/3/tutorial/controlflow.html#defining-functions](https://docs.python.org/es/3/tutorial/controlflow.html#defining-functions)
- Módulos y paquetes: [docs.python.org/es/3/tutorial/modules.html](https://docs.python.org/es/3/tutorial/modules.html)
- Índice de la librería estándar: [docs.python.org/es/3/library](https://docs.python.org/es/3/library/)
