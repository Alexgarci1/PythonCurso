# Módulo 1. Introducción a Python (4 horas)

Al terminar este módulo tendrás un entorno profesional funcionando y sabrás escribir, ejecutar y probar tus primeros programas en Python.

Ya sabes programar, así que este módulo no explica qué es una variable ni qué es un bucle. Explica cómo se trabaja en Python y en qué se diferencia de los lenguajes que ya conoces.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 1.1 | Qué es Python y dónde se usa | 0,5 h |
| 1.2 | Instalación de Python y Visual Studio Code | 0,5 h |
| 1.3 | Entorno de desarrollo | 1 h |
| 1.4 | Sintaxis básica | 1 h |
| 1.5 | Primeros programas y práctica 1 | 1 h |

---

## 1.1 Qué es Python y dónde se usa

Python es un lenguaje de propósito general, interpretado, de tipado dinámico y fuerte, creado por Guido van Rossum y publicado en 1991. Su diseño prioriza la legibilidad: el código se lee casi como pseudocódigo.

### Características que te van a llamar la atención

| Característica | Qué significa | Comparación con Java o C# |
| --- | --- | --- |
| Interpretado | No hay paso de compilación explícito. Ejecutas el fichero fuente directamente | En Java compilas a bytecode con `javac` y luego ejecutas |
| Tipado dinámico | El tipo pertenece al valor, no a la variable. No declaras tipos | `int x = 5;` frente a `x = 5` |
| Tipado fuerte | No hay conversiones implícitas peligrosas. `"3" + 4` es un error | En JavaScript `"3" + 4` da `"34"` |
| Indentación significativa | Los bloques se delimitan con sangría, no con llaves | `{ ... }` desaparece |
| Todo es un objeto | Números, funciones, clases y módulos son objetos | En Java los tipos primitivos no lo son |
| Baterías incluidas | La librería estándar cubre ficheros, fechas, JSON, HTTP, tests y mucho más | Similar al JDK o a .NET |

Una aclaración técnica: Python sí compila, pero lo hace solo. El intérprete traduce tu código a bytecode (los ficheros `.pyc` de la carpeta `__pycache__`) y lo ejecuta en su máquina virtual. La implementación de referencia se llama CPython y es la que vamos a usar.

### Dónde se usa

- **Automatización y scripting:** tareas de sistemas, procesado de ficheros, integración entre herramientas.
- **Desarrollo web y APIs:** Django, Flask y FastAPI.
- **Datos:** pandas, NumPy, análisis y visualización.
- **Inteligencia artificial:** es el lenguaje de referencia para machine learning, IA generativa y agentes. Los siguientes cursos del itinerario se apoyan en lo que aprendas aquí.
- **Testing y DevOps:** pytest, Ansible, scripts de despliegue.

### Dos formas de trabajar con Python

En una consultora te vas a encontrar Python en dos papeles, y este curso cubre los dos:

| | Python para aplicaciones | Python para ciencia de datos |
| --- | --- | --- |
| Qué se construye | Servicios, API, automatizaciones, herramientas de consola | Análisis, informes, cuadros de mando, modelos |
| Cómo se trabaja | Proyecto con paquetes, tests y control de versiones | Exploración interactiva en cuadernos y, después, código probado |
| Estructura central | Clases, funciones y colecciones | Tablas y arrays: se opera con la columna entera |
| Librerías | Librería estándar, FastAPI, Django, SQLAlchemy, pytest | NumPy, pandas, Matplotlib, Jupyter, scikit-learn |
| En este curso | Módulos 2 a 6 y la aplicación del Módulo 8 | Módulo 7 y el análisis del Módulo 8 |

No son dos lenguajes ni dos perfiles separados: el análisis que funciona en un cuaderno acaba convertido en funciones, módulos y tests, y las aplicaciones acaban cargando y resumiendo datos. Los módulos 2 a 6 incluyen un apartado «Mirada de datos» que conecta cada tema con el trabajo con datos.

### El mapa de librerías

| Necesidad | Librería | Dónde se ve |
| --- | --- | --- |
| Ficheros, fechas, JSON, CSV, expresiones regulares | Librería estándar | Módulos 3 y 6 |
| Tests | pytest | Todo el curso |
| Cálculo numérico con arrays | NumPy | Módulo 7 |
| Tablas: cargar, limpiar, agrupar y combinar | pandas | Módulos 7 y 8 |
| Gráficos | Matplotlib | Módulo 7 |
| Cuadernos interactivos | Jupyter | Módulo 7 |
| Modelos de machine learning | scikit-learn | Curso siguiente |
| API web | FastAPI | Fuera del curso |

### Python 2 y Python 3

Python 2 dejó de tener soporte en 2020. Todo el curso usa Python 3.12 o superior. Si encuentras por internet código con `print "hola"` sin paréntesis, es Python 2: no lo copies.

### La filosofía del lenguaje

Abre un intérprete y escribe `import this`. Verás el *Zen de Python*, una lista de principios de diseño. Los tres que más vas a notar:

- Explícito es mejor que implícito.
- La legibilidad cuenta.
- Debería haber una forma obvia de hacerlo, y preferiblemente solo una.

Al código que sigue esas convenciones se le llama *pythonic* o idiomático. Buena parte del curso consiste en aprender a escribir así, y no Java con sintaxis de Python.

---

## 1.2 Instalación de Python y Visual Studio Code

### Instalar Python

1. Descarga el instalador desde [python.org/downloads](https://www.python.org/downloads/).
2. En Windows, marca la casilla **Add python.exe to PATH** antes de pulsar *Install Now*.
3. Comprueba la instalación desde una terminal nueva:

```bash
python --version
```

Debe mostrar `Python 3.12.x` o superior. En macOS y Linux el comando suele ser `python3`. En Windows también puedes usar el lanzador `py`.

### Instalar Visual Studio Code

1. Descarga VS Code desde [code.visualstudio.com](https://code.visualstudio.com/).
2. Instala la extensión **Python** de Microsoft desde el panel de extensiones (`Ctrl+Shift+X`). Incluye Pylance (autocompletado y análisis) y el depurador.

### Instalar Git

Descárgalo de [git-scm.com](https://git-scm.com/) si no lo tienes y comprueba con `git --version`.

---

## 1.3 Entorno de desarrollo

### El intérprete interactivo (REPL)

Escribe `python` en la terminal y obtendrás un intérprete interactivo. Lee una expresión, la evalúa, imprime el resultado y vuelve a esperar. Es la calculadora y el banco de pruebas de cualquier desarrollador de Python.

```python
>>> 2 + 3
5
>>> nombre = "Ada"
>>> nombre.upper()
'ADA'
>>> type(nombre)
<class 'str'>
>>> help(str.upper)
```

Tres funciones que conviene conocer desde el primer día:

| Función | Para qué sirve |
| --- | --- |
| `type(x)` | Dice de qué tipo es un objeto |
| `dir(x)` | Lista los atributos y métodos de un objeto |
| `help(x)` | Muestra la documentación |

Sales del intérprete con `exit()` o con `Ctrl+Z` y Enter en Windows (`Ctrl+D` en macOS y Linux).

### Cuadernos Jupyter

Hay una tercera forma de ejecutar Python, a medio camino entre el REPL y el script: el cuaderno. Es un fichero `.ipynb` dividido en celdas de código y de texto, en el que el resultado de cada celda queda guardado debajo de ella. Es la herramienta habitual para explorar datos, y VS Code los abre directamente.

| Herramienta | Úsala para |
| --- | --- |
| REPL | Probar una expresión o consultar `help` en diez segundos |
| Cuaderno | Explorar datos paso a paso, con tablas y gráficos a la vista |
| Script y módulos `.py` | Todo lo que se va a reutilizar, probar o desplegar |

Durante los módulos 1 a 6 trabajamos con el REPL y con ficheros `.py`. Los cuadernos llegan en el Módulo 7.

### Ejecutar un script

Un programa de Python es un fichero de texto con extensión `.py`. Se ejecuta pasándoselo al intérprete:

```bash
python ejemplos/01_hola_mundo.py
```

No hay método `main` obligatorio ni clase contenedora. El intérprete ejecuta el fichero de arriba abajo.

### Entornos virtuales

Un entorno virtual es una carpeta con una copia aislada del intérprete y sus paquetes. Cada proyecto tiene el suyo, de modo que las dependencias de un proyecto no interfieren con las de otro. Es el equivalente a tener un `node_modules` por proyecto, o a las dependencias que Maven resuelve por proyecto.

```bash
python -m venv .venv
```

Ese comando crea la carpeta `.venv`. Después hay que activarlo:

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| macOS o Linux | `source .venv/bin/activate` |

Cuando está activo, el nombre del entorno aparece al principio del prompt: `(.venv)`. Se desactiva con `deactivate`.

Si PowerShell bloquea la activación por la política de ejecución, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Reglas prácticas:

- Un entorno virtual por proyecto, en la carpeta `.venv` de la raíz.
- La carpeta `.venv` nunca se sube a Git. Va en el `.gitignore`.
- Activa el entorno antes de instalar nada.

### Instalar paquetes con pip

`pip` es el gestor de paquetes. Descarga las librerías desde PyPI, el repositorio público de paquetes de Python.

```bash
pip install pytest            # instala un paquete
pip list                      # muestra lo instalado
pip install -r requirements.txt   # instala todo lo que lista el fichero
pip freeze > requirements.txt     # guarda las versiones instaladas
```

El fichero `requirements.txt` cumple el papel del `pom.xml` o del `package.json`: declara de qué depende el proyecto para que otra persona pueda reproducir el entorno.

### Configurar VS Code

1. Abre la carpeta del repositorio con *File > Open Folder*.
2. Pulsa `Ctrl+Shift+P`, escribe **Python: Select Interpreter** y elige el de `.venv`.
3. Abre una terminal integrada con `` Ctrl+` ``. VS Code activa el entorno automáticamente.
4. Ejecuta un fichero con el botón de *play* o con `python fichero.py` en la terminal.

### El repositorio del curso

```bash
git clone https://github.com/yustech/Curso-Python-IA.git
cd Curso-Python-IA
python -m venv .venv
# activa el entorno
pip install -r requirements.txt
pytest
```

Si `pytest` se ejecuta y muestra tests fallidos, el entorno está bien: fallan porque todavía no has resuelto los ejercicios.

---

## 1.4 Sintaxis básica

### La indentación define los bloques

En Python no hay llaves. Un bloque empieza con dos puntos y se delimita con la sangría.

```python
temperatura = 31

if temperatura > 30:
    print("Hace calor")
    print("Bebe agua")
else:
    print("Temperatura agradable")

print("Fin")
```

- La convención es usar **4 espacios** por nivel. No uses tabuladores ni mezcles ambos.
- Todas las líneas de un mismo bloque llevan exactamente la misma sangría.
- Una sangría incorrecta no es un problema estético: es un `IndentationError` o, peor, un programa que hace otra cosa.

### Sentencias, líneas y comentarios

```python
# Esto es un comentario de línea

total = 10 + 20   # no hay punto y coma al final

# Una sentencia larga se puede partir dentro de paréntesis
resultado = (
    10
    + 20
    + 30
)

"""
Una cadena entre triples comillas puede ocupar varias líneas.
Colocada al principio de un módulo, función o clase es su docstring,
la documentación que muestra help().
"""
```

### Variables y nombres

Una variable se crea al asignarle un valor. No se declara ni se le pone tipo.

```python
edad = 30
nombre = "Lucía"
altura = 1.68
es_alumna = True
sin_valor = None
```

Reglas y convenciones para los nombres:

| Elemento | Convención | Ejemplo |
| --- | --- | --- |
| Variables y funciones | `snake_case` | `precio_final`, `calcular_total()` |
| Constantes | `MAYUSCULAS_CON_GUIONES` | `IVA_GENERAL = 21` |
| Clases | `PascalCase` | `CuentaBancaria` |
| Módulos y ficheros | `snake_case` corto | `utilidades.py` |

Python distingue mayúsculas de minúsculas y no permite usar palabras reservadas (`if`, `for`, `class`, `def`...) como nombres.

### Salida y entrada

```python
print("Hola, mundo")
print("Total:", 42, "euros")          # separa con espacios
print("a", "b", "c", sep="-")         # a-b-c

nombre = input("¿Cómo te llamas? ")   # input siempre devuelve un str
edad = int(input("¿Cuántos años tienes? "))
```

Las *f-strings* son la forma idiomática de construir texto:

```python
nombre = "Ada"
edad = 36
print(f"{nombre} tiene {edad} años")
print(f"El año que viene tendrá {edad + 1}")
print(f"Precio: {19.5:.2f} €")        # dos decimales: 19.50
```

### Una función mínima

Las funciones tienen su propio módulo, pero necesitas lo básico desde hoy porque los ejercicios se comprueban llamando a funciones.

```python
def area_rectangulo(base, altura):
    """Devuelve el área de un rectángulo."""
    return base * altura


print(area_rectangulo(3, 4))   # 12
```

`def` define la función, los dos puntos abren el bloque y `return` devuelve el resultado.

### El punto de entrada de un script

```python
def main():
    print("Programa principal")


if __name__ == "__main__":
    main()
```

Ese `if` hace que `main()` se ejecute solo cuando lanzas el fichero directamente, y no cuando otro fichero lo importa. Es el patrón habitual de todo script de Python y es lo que permite que los tests importen tus funciones sin lanzar el programa.

### PEP 8: la guía de estilo

PEP 8 es la guía de estilo oficial. En la práctica nadie la aplica a mano: se usa un formateador. Lo esencial:

- 4 espacios de sangría.
- Líneas de 79 a 100 caracteres como máximo, según el acuerdo del equipo.
- Espacios alrededor de los operadores: `x = a + b`, no `x=a+b`.
- Dos líneas en blanco entre funciones de nivel superior.
- Nombres descriptivos en `snake_case`.
- Los `import` van al principio del fichero.

Compara:

```python
# Mal
def Calc(P,i):
  R=P+P*i/100;return R

# Bien
def precio_con_iva(precio, iva):
    """Devuelve el precio con el IVA aplicado."""
    return precio + precio * iva / 100
```

### Resumen de diferencias con Java y C#

| Concepto | Java o C# | Python |
| --- | --- | --- |
| Bloques | `{ }` | Dos puntos y sangría |
| Fin de sentencia | `;` | Salto de línea |
| Declaración | `int x = 5;` | `x = 5` |
| Imprimir | `System.out.println(x)` | `print(x)` |
| Nulo | `null` | `None` |
| Booleanos | `true`, `false` | `True`, `False` |
| Operadores lógicos | `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| Comentario | `//` | `#` |
| Punto de entrada | `public static void main` | `if __name__ == "__main__":` |

---

## 1.5 Primeros programas

Los ejemplos de la carpeta [`ejemplos/`](ejemplos/) recorren lo visto. Ejecútalos, léelos y modifícalos.

| Fichero | Qué muestra |
| --- | --- |
| `01_hola_mundo.py` | El programa mínimo y el punto de entrada |
| `02_sintaxis_basica.py` | Indentación, variables, comentarios y tipos |
| `03_entrada_salida.py` | `input()`, conversión de tipos y f-strings |
| `04_funciones_y_tests.py` | Una función sencilla y cómo la comprueba un test |

### Tu primer test

Un test es una función cuyo nombre empieza por `test_` y que usa `assert` para afirmar algo. `pytest` busca esas funciones, las ejecuta e informa de cuáles fallan.

```python
from m1_ej1_saludo import saludar


def test_saludar_devuelve_el_saludo():
    assert saludar("Ada") == "Hola, Ada. ¡Te damos la bienvenida al curso!"
```

```bash
pytest modulo_01_introduccion -v
```

Trabajaremos así todo el curso: cada ejercicio trae sus tests y está terminado cuando pasan.

### Ejercicios y práctica

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 1, conversor de unidades: [`ejercicios/PRACTICA_1.md`](ejercicios/PRACTICA_1.md)

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Solución |
| --- | --- | --- |
| Instalar paquetes sin activar el entorno | Se instalan en el Python global | Comprueba que ves `(.venv)` en el prompt |
| VS Code usa otro intérprete | `ModuleNotFoundError` aunque el paquete esté instalado | *Python: Select Interpreter* y elegir `.venv` |
| Mezclar tabuladores y espacios | `TabError` o `IndentationError` | Configura el editor para insertar espacios |
| Olvidar los dos puntos | `SyntaxError: expected ':'` | Todo `if`, `for`, `while`, `def` y `class` termina en `:` |
| Tratar `input()` como número | `TypeError` al operar | Convierte con `int()` o `float()` |
| Escribir `true`, `false` o `null` | `NameError` | Son `True`, `False` y `None` |

## Para saber más

- Tutorial oficial: [docs.python.org/es/3/tutorial](https://docs.python.org/es/3/tutorial/)
- PEP 8: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)
- Documentación de pytest: [docs.pytest.org](https://docs.pytest.org/)
