# Módulo 6. Archivos y gestión de excepciones (3 horas)

Al terminar este módulo sabrás guardar y recuperar datos en archivos de texto, CSV y JSON, y escribir código que falla de forma controlada: que detecta el error, informa de él y deja el programa en un estado correcto.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 6.1 | Lectura y escritura de archivos | 0,75 h |
| 6.2 | CSV | 0,75 h |
| 6.3 | Excepciones | 0,75 h |
| 6.4 | Depuración, logging y Práctica 6 | 0,75 h |

Los archivos de ejemplo están en la carpeta [`datos/`](datos/).

---

## 6.1 Lectura y escritura de archivos

### Abrir con with

```python
with open("notas.txt", encoding="utf-8") as fichero:
    contenido = fichero.read()

# aquí el fichero ya está cerrado
```

`with` es un **gestor de contexto**: garantiza que el fichero se cierra al salir del bloque, también si dentro se produce un error. Es el equivalente al *try-with-resources* de Java y al `using` de C#. No abras ficheros sin `with`.

### Modos

| Modo | Significado | Si el fichero no existe | Si existe |
| --- | --- | --- | --- |
| `"r"` | Leer. Es el modo por defecto | `FileNotFoundError` | Lo lee |
| `"w"` | Escribir | Lo crea | **Lo vacía** |
| `"a"` | Añadir al final | Lo crea | Conserva el contenido |
| `"x"` | Crear | Lo crea | `FileExistsError` |

Con una `b` detrás, `"rb"` o `"wb"`, el fichero se trata como binario: se leen y se escriben `bytes`, no texto. Es lo que se usa para imágenes, PDF o ficheros comprimidos.

### Codificación: siempre UTF-8, siempre explícita

Un fichero de texto son bytes; la codificación es la regla que los convierte en caracteres. Si no la indicas, Python usa la del sistema operativo, que en Windows no suele ser UTF-8. El resultado es el clásico `Ã±` en lugar de `ñ`, o un `UnicodeDecodeError`.

```python
open("datos.txt", encoding="utf-8")          # siempre así
```

Es el error más frecuente al mover un script entre Windows, Linux y macOS. Escribe `encoding="utf-8"` en todos los `open()` de texto.

### Leer

```python
with open("notas.txt", encoding="utf-8") as fichero:
    contenido = fichero.read()               # todo el fichero en una cadena

with open("notas.txt", encoding="utf-8") as fichero:
    lineas = fichero.readlines()             # lista de líneas, cada una con su \n

with open("notas.txt", encoding="utf-8") as fichero:
    lineas = fichero.read().splitlines()     # lista de líneas sin el \n

with open("notas.txt", encoding="utf-8") as fichero:
    for linea in fichero:                    # línea a línea, sin cargar todo en memoria
        print(linea.rstrip("\n"))
```

Un fichero abierto es un iterable de líneas. Recorrerlo con `for` es la forma adecuada para ficheros grandes, porque solo hay una línea en memoria a la vez. Cada línea incluye su salto final: quítalo con `rstrip("\n")` o con `strip()`.

Como todo iterador, un fichero se agota: después de recorrerlo, una segunda lectura no devuelve nada.

### Escribir

```python
lineas = ["primera", "segunda", "tercera"]

with open("salida.txt", "w", encoding="utf-8") as fichero:
    fichero.write("Cabecera\n")              # write no añade el salto de línea
    for linea in lineas:
        fichero.write(linea + "\n")

with open("salida.txt", "a", encoding="utf-8") as fichero:
    fichero.write("una línea más\n")         # añade al final

with open("salida.txt", "w", encoding="utf-8") as fichero:
    print("también con print", file=fichero)    # print sí añade el salto
```

### pathlib

Lo presentamos en el Módulo 3. `Path` representa una ruta y funciona igual en todos los sistemas operativos. Para ficheros pequeños ofrece atajos que abren, leen o escriben y cierran en una sola llamada:

```python
from pathlib import Path

ruta = Path("datos") / "notas.txt"

ruta.exists(), ruta.is_file(), ruta.is_dir()
texto = ruta.read_text(encoding="utf-8")
ruta.write_text("contenido nuevo\n", encoding="utf-8")

with ruta.open(encoding="utf-8") as fichero:         # igual que open(ruta, ...)
    for linea in fichero:
        ...

ruta.parent.mkdir(parents=True, exist_ok=True)       # crea las carpetas que falten
for fichero in Path("datos").glob("*.csv"):          # lista por patrón
    print(fichero.name, fichero.stat().st_size)

ruta.with_suffix(".bak")                             # datos/notas.bak
ruta.rename(ruta.with_name("apuntes.txt"))
ruta.unlink(missing_ok=True)                         # borra
```

### Rutas relativas

Una ruta relativa se resuelve desde la **carpeta de trabajo**, que es desde donde se lanza el programa, no desde donde está el script. Por eso un programa funciona en VS Code y falla en la terminal, o al revés.

Para localizar un fichero que acompaña al código, construye la ruta a partir de `__file__`:

```python
CARPETA_DATOS = Path(__file__).parent / "datos"
ruta = CARPETA_DATOS / "ventas.csv"
```

### JSON

Aunque no es el centro del módulo, lo vas a usar a diario. El módulo `json` convierte entre texto JSON y diccionarios y listas de Python:

```python
import json

with open("config.json", encoding="utf-8") as fichero:
    configuracion = json.load(fichero)               # de fichero a dict o list

with open("salida.json", "w", encoding="utf-8") as fichero:
    json.dump(datos, fichero, ensure_ascii=False, indent=2)

texto = json.dumps(datos)                            # a cadena
datos = json.loads(texto)                            # desde cadena
```

---

## 6.2 CSV

Un CSV es un fichero de texto con una fila por línea y los campos separados por un delimitador. Parece que basta con `linea.split(",")`, pero no: un campo puede contener comas, comillas o saltos de línea. Usa siempre el módulo `csv`.

```
fecha,vendedor,producto,unidades,precio
2026-10-01,Ada,Portátil,2,950.0
2026-10-02,Grace,"Monitor 27"", curvo",3,189.0
```

### Leer con csv.reader

Cada fila es una **lista de cadenas**.

```python
import csv

with open("ventas.csv", encoding="utf-8", newline="") as fichero:
    lector = csv.reader(fichero)
    cabecera = next(lector)                  # la primera fila
    for fila in lector:
        print(fila[1], fila[3])              # acceso por posición
```

### Leer con csv.DictReader

Cada fila es un **diccionario** cuyas claves salen de la cabecera. Es la forma recomendada: el código no depende del orden de las columnas y se lee mejor.

```python
with open("ventas.csv", encoding="utf-8", newline="") as fichero:
    ventas = list(csv.DictReader(fichero))

ventas[0]
# {'fecha': '2026-10-01', 'vendedor': 'Ada', 'producto': 'Portátil', 'unidades': '2', 'precio': '950.0'}
```

El resultado es exactamente la lista de diccionarios con la que trabajaste en el Módulo 4. Todo lo que sabes de filtrar, ordenar y agrupar se aplica sin cambios.

### Todo llega como texto

El CSV no tiene tipos. **Todos los valores son cadenas** y hay que convertirlos:

```python
for venta in ventas:
    venta["unidades"] = int(venta["unidades"])
    venta["precio"] = float(venta["precio"])
```

Olvidarlo produce errores silenciosos: `"2" * 3` es `"222"` y `"10" < "9"` es `True`.

### Escribir

```python
with open("salida.csv", "w", encoding="utf-8", newline="") as fichero:
    escritor = csv.writer(fichero)
    escritor.writerow(["producto", "unidades"])              # una fila
    escritor.writerows([["Teclado", 5], ["Ratón", 12]])      # varias

campos = ["producto", "unidades", "precio"]
with open("salida.csv", "w", encoding="utf-8", newline="") as fichero:
    escritor = csv.DictWriter(fichero, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(lista_de_diccionarios)
```

`DictWriter` lanza `ValueError` si un diccionario tiene una clave que no está en `fieldnames`. Con `extrasaction="ignore"` las descarta.

### Tres detalles que evitan problemas

- **`newline=""`** al abrir, tanto para leer como para escribir. Sin él, en Windows aparece una línea en blanco entre cada fila.
- **El delimitador.** Excel en español exporta con punto y coma: `csv.reader(fichero, delimiter=";")`.
- **`encoding="utf-8-sig"`** al leer ficheros guardados por Excel como «CSV UTF-8». Empiezan con una marca invisible, el BOM, que de otro modo se pega al nombre de la primera columna.

Para análisis de datos con ficheros grandes se usa `pandas`, pero para leer, validar y escribir, el módulo `csv` es suficiente y no añade dependencias.

---

## 6.3 Excepciones

### Qué es una excepción

Cuando Python no puede continuar, **lanza** una excepción. Si nadie la captura, el programa termina y muestra la traza:

```
Traceback (most recent call last):
  File "informe.py", line 12, in <module>
    main()
  File "informe.py", line 8, in main
    total = calcular(ventas)
  File "informe.py", line 3, in calcular
    return sum(v["importe"] for v in ventas)
KeyError: 'importe'
```

La traza se lee **de abajo arriba**: la última línea dice qué ha pasado y la anterior dónde. Las de más arriba cuentan el camino de llamadas hasta llegar ahí.

Ya has visto muchas: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `AttributeError`, `ZeroDivisionError`, `FileNotFoundError`.

### try y except

```python
try:
    edad = int(input("Edad: "))
except ValueError:
    print("Eso no es un número.")
```

Si el código del `try` lanza un `ValueError`, la ejecución salta al `except`. Si lanza otra cosa, la excepción sigue subiendo.

```python
try:
    with open(ruta, encoding="utf-8") as fichero:
        valor = int(fichero.readline())
except FileNotFoundError:
    print(f"No existe {ruta}")
except ValueError as error:                  # as da acceso al objeto de la excepción
    print(f"La primera línea no es un número: {error}")
except (PermissionError, IsADirectoryError):   # varias en una misma rama
    print("No se puede leer")
```

### else y finally

```python
try:
    fichero = open(ruta, encoding="utf-8")
except FileNotFoundError:
    print("No existe")
else:
    # solo si el try ha terminado SIN excepción
    contenido = fichero.read()
    fichero.close()
finally:
    # SIEMPRE: haya excepción o no, se capture o no
    print("Intento terminado")
```

| Bloque | Cuándo se ejecuta | Para qué |
| --- | --- | --- |
| `try` | Siempre | El código que puede fallar. Cuanto más corto, mejor |
| `except` | Si se lanza la excepción indicada | Recuperarse o informar |
| `else` | Si no ha habido excepción | Lo que solo tiene sentido si todo fue bien |
| `finally` | Siempre | Liberar recursos. Con `with` casi nunca hace falta |

### Jerarquía de excepciones

Las excepciones son clases y forman una jerarquía. Un `except` captura la clase indicada **y todas sus subclases**.

```
BaseException
├── KeyboardInterrupt          Ctrl+C
├── SystemExit
└── Exception                  la base de todas las «normales»
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   ├── FileNotFoundError
    │   └── PermissionError
    ├── ValueError
    │   └── UnicodeDecodeError
    ├── TypeError
    └── AttributeError
```

Consecuencia: el orden de los `except` importa. Los más específicos van primero.

### Qué capturar y qué no

```python
try:
    procesar(datos)
except:                        # MAL: captura hasta Ctrl+C
    pass

try:
    procesar(datos)
except Exception:              # MAL casi siempre: esconde errores de programación
    pass
```

Un `except` que lo captura todo y no hace nada convierte un error visible en un resultado incorrecto que nadie detecta. Reglas:

- **Captura solo lo que sabes manejar**, con la clase más específica posible.
- **Nunca `except:` a secas** ni `except Exception: pass`.
- Si no puedes hacer nada útil con la excepción, **no la captures**: que suba hasta quien sí pueda.
- Los errores de programación (`TypeError`, `AttributeError`, `NameError`) no se capturan: se corrigen.
- `except Exception` es aceptable en el nivel más alto de un programa, para registrar el error y terminar con dignidad.

### Pedir perdón, no permiso

En Python es habitual intentar la operación y capturar el fallo, en lugar de comprobar antes todas las condiciones. Se conoce como EAFP, *easier to ask forgiveness than permission*.

```python
# Comprobar antes (LBYL)
if clave in datos and datos[clave].isdigit():
    valor = int(datos[clave])
else:
    valor = 0

# Intentar y capturar (EAFP)
try:
    valor = int(datos[clave])
except (KeyError, ValueError):
    valor = 0
```

Con ficheros, además, comprobar antes no es fiable: el fichero puede desaparecer entre el `exists()` y el `open()`.

### Lanzar excepciones: raise

```python
def retirar(saldo, importe):
    if importe <= 0:
        raise ValueError("El importe debe ser positivo")
    if importe > saldo:
        raise ValueError(f"Saldo insuficiente: hay {saldo} y se piden {importe}")
    return saldo - importe
```

Elige la clase que mejor describa el problema: `ValueError` si el valor es del tipo correcto pero no vale, `TypeError` si el tipo no es el esperado, `KeyError` si falta una clave, `FileNotFoundError` si falta un fichero. El mensaje tiene que decir **qué valor** ha causado el problema.

Para volver a lanzar la excepción que se está manejando, después de registrarla por ejemplo, se usa `raise` sin nada:

```python
try:
    procesar(datos)
except ValueError:
    logger.error("Datos no válidos")
    raise
```

### Excepciones propias

Una aplicación define sus propias excepciones para que quien la usa pueda distinguir sus errores de los demás. Basta con heredar de `Exception`:

```python
class ErrorDeBiblioteca(Exception):
    """Base de todos los errores de la aplicación."""


class MaterialNoDisponible(ErrorDeBiblioteca):
    def __init__(self, codigo):
        super().__init__(f"El material {codigo} ya está prestado")
        self.codigo = codigo


class SocioNoEncontrado(ErrorDeBiblioteca):
    pass
```

```python
try:
    biblioteca.prestar("L001", 7, hoy)
except MaterialNoDisponible as error:
    print(f"Puedes reservar {error.codigo}")
except ErrorDeBiblioteca as error:           # cualquier otro error de la aplicación
    print(f"No se pudo prestar: {error}")
```

Una clase base común permite capturar todos los errores de la aplicación de una vez. Los atributos, como `codigo`, permiten que el código que captura actúe sin tener que analizar el texto del mensaje.

### Encadenar excepciones

Para traducir un error de bajo nivel en uno con significado para la aplicación sin perder la causa original, se usa `raise ... from`:

```python
def cargar_configuracion(ruta):
    try:
        with open(ruta, encoding="utf-8") as fichero:
            return json.load(fichero)
    except FileNotFoundError as error:
        raise ErrorDeConfiguracion(f"Falta el fichero {ruta}") from error
```

La traza mostrará las dos excepciones y la relación entre ellas.

### Dónde se captura

Lo normal es que las capas bajas **lancen** y que la capa que habla con el usuario **capture**:

```python
def main():
    try:
        ventas = importar_ventas(ruta)       # puede lanzar FicheroNoValido
        mostrar_informe(ventas)
    except FicheroNoValido as error:
        print(f"Error: {error}")
        return 1
    return 0
```

Una función de cálculo que captura sus propios errores e imprime un mensaje es difícil de reutilizar y de probar.

---

## 6.4 Depuración, logging y Práctica 6

### Leer la traza

Antes de abrir el depurador, lee la traza. Tres preguntas:

1. **¿Qué excepción y con qué mensaje?** Última línea.
2. **¿En qué línea de tu código?** Sube desde abajo hasta el primer fichero que sea tuyo y no de una librería.
3. **¿Qué valor tenía la variable?** El mensaje suele decirlo; si no, es el momento del depurador.

### Depurar en VS Code

| Acción | Tecla | Qué hace |
| --- | --- | --- |
| Punto de ruptura | `F9`, o clic a la izquierda del número de línea | La ejecución se detiene al llegar a esa línea |
| Iniciar o continuar | `F5` | Ejecuta hasta el siguiente punto de ruptura |
| Paso por encima | `F10` | Ejecuta la línea sin entrar en las funciones que llama |
| Paso adentro | `F11` | Entra en la función llamada |
| Paso afuera | `Mayús+F11` | Termina la función actual y vuelve a quien la llamó |
| Detener | `Mayús+F5` | Termina la sesión |

Con el programa detenido:

- El panel **Variables** muestra las variables locales y globales con su valor.
- En **Inspección** (*Watch*) se añaden expresiones que se recalculan a cada paso: `len(ventas)`, `fila["precio"]`.
- La **Pila de llamadas** (*Call Stack*) muestra el camino hasta la línea actual. Al hacer clic en un nivel se ven sus variables.
- La **Consola de depuración** permite ejecutar código en el contexto actual: consultar un valor o probar una corrección.

Dos recursos que ahorran mucho tiempo:

- **Punto de ruptura condicional:** clic derecho sobre el punto, *Editar punto de interrupción*, y una condición como `fila["unidades"] == ""`. Solo se detiene cuando se cumple.
- **Puntos de ruptura de excepción:** en el panel *Puntos de interrupción*, activar *Excepciones no detectadas*. El depurador se detiene justo donde se lanza, con todas las variables a la vista.

Para depurar un test: icono del matraz en la barra lateral, clic derecho sobre el test y *Depurar prueba*.

Sin VS Code, `breakpoint()` en cualquier línea abre el depurador de consola `pdb`: `n` siguiente, `s` entrar, `c` continuar, `p variable` imprimir, `q` salir.

### Método

1. **Reproduce** el error de forma fiable, a ser posible con un test.
2. **Acota:** ¿cuál es la primera línea en la que el estado deja de ser el esperado?
3. **Formula una hipótesis** y compruébala con el depurador, no cambiando código al azar.
4. **Corrige** la causa, no el síntoma.
5. **Deja el test** que lo reproduce para que no vuelva.

### Logging básico

`print` sirve para explorar. En un programa que se ejecuta sin que nadie mire la pantalla necesitas un registro con fecha, nivel de gravedad y destino configurable. Eso es `logging`.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

logger.debug("Fila leída: %s", fila)                 # detalle para depurar
logger.info("Importadas %d ventas", len(ventas))     # funcionamiento normal
logger.warning("Fila %d descartada: %s", numero, motivo)    # algo raro, pero se sigue
logger.error("No se pudo abrir %s", ruta)            # una operación ha fallado
logger.critical("Sin conexión a la base de datos")   # el programa no puede continuar
```

| Nivel | Cuándo |
| --- | --- |
| `DEBUG` | Información detallada para diagnosticar |
| `INFO` | Confirmación de que las cosas funcionan |
| `WARNING` | Algo inesperado que no impide seguir. Es el nivel por defecto |
| `ERROR` | Una operación no se ha podido completar |
| `CRITICAL` | El programa no puede continuar |

Solo se registran los mensajes del nivel configurado o superior. En desarrollo se usa `DEBUG`; en producción, `INFO` o `WARNING`, sin tocar el código.

Buenas prácticas:

- **Un logger por módulo:** `logger = logging.getLogger(__name__)`.
- **`basicConfig` una sola vez**, en el punto de entrada del programa. Las librerías no configuran el logging; solo lo usan.
- **Pasa los valores como argumentos**, `logger.info("Leídas %d filas", n)`, en lugar de construir el texto con una f-string. El mensaje solo se compone si se va a registrar.
- **`logger.exception("mensaje")`** dentro de un `except` registra el mensaje con la traza completa.
- **A un fichero:** `logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.INFO)`.
- **No registres datos sensibles:** contraseñas, tokens, datos personales.

```python
try:
    ventas = importar_ventas(ruta)
except FicheroNoValido:
    logger.exception("Fallo al importar %s", ruta)
    raise
```

### Material del módulo

| Fichero de [`ejemplos/`](ejemplos/) | Qué muestra |
| --- | --- |
| `01_ficheros_de_texto.py` | Modos, lectura línea a línea, escritura y `pathlib` |
| `02_csv.py` | `reader`, `DictReader`, conversión de tipos, `DictWriter` y delimitadores |
| `03_excepciones.py` | `try`, `except`, `else`, `finally`, jerarquía y EAFP |
| `04_excepciones_propias.py` | `raise`, jerarquía propia y `raise ... from` |
| `05_logging.py` | Niveles, formato, registro en fichero y `logger.exception` |
| `06_para_depurar.py` | Un programa con tres errores para practicar con el depurador |
| `07_mirada_datos.py` | Cargar un CSV con filas incorrectas sin detener la carga y dejar un resumen en JSON |

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 6, importador de CSV: [`ejercicios/PRACTICA_6.md`](ejercicios/PRACTICA_6.md)

---

## Mirada de datos

Cargar un fichero es el primer paso de cualquier análisis, y los problemas de este módulo son los mismos que encontrarás con pandas. Allí aparecen como parámetros de `pd.read_csv`:

| Problema | Con el módulo `csv` | Con pandas (Módulo 7) |
| --- | --- | --- |
| Tildes rotas | `open(..., encoding="utf-8")` | `pd.read_csv(ruta, encoding="utf-8")` |
| Separador punto y coma | `csv.reader(f, delimiter=";")` | `sep=";"` |
| Coma decimal | `float(texto.replace(",", "."))` | `decimal=","` |
| Todo llega como texto | Conversión a mano, fila a fila | Tipos inferidos por columna, y `dtype=` o `parse_dates=` para fijarlos |
| Filas que no valen | `try`/`except` por fila | `pd.to_numeric(columna, errors="coerce")` y `dropna` |

La decisión importante no cambia de una herramienta a otra: **qué se hace con una fila que no vale**. Hay tres políticas, y hay que elegir una a propósito:

1. **Detener la carga.** Para los datos propios de una aplicación, donde seguir con la mitad sería peor. Es lo que hará el almacén del proyecto final.
2. **Apartar la fila y seguir, dejando constancia.** Para datos que vienen de fuera. Es la Práctica 6.
3. **Convertir el dato incorrecto en valor ausente.** Lo habitual en análisis exploratorio, y lo que hace `errors="coerce"`.

El patrón de la segunda política, en pequeño:

```python
validas, rechazos = [], []
for numero, fila in enumerate(csv.DictReader(fichero), start=2):
    try:
        fila["unidades"] = int(fila["unidades"])
        fila["precio"] = float(fila["precio"])
    except ValueError as error:
        rechazos.append((numero, str(error)))
        continue
    validas.append(fila)
```

Lo que nunca se hace es descartar filas en silencio: un análisis sobre el 90 % de los datos, sin saber que falta el 10 %, es un resultado falso. El ejemplo `ejemplos/07_mirada_datos.py` carga `datos/ventas_con_errores.csv`, informa de las dos filas rechazadas y deja un resumen del proceso en JSON.

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Forma correcta |
| --- | --- | --- |
| `open(ruta)` sin `with` | El fichero queda abierto si hay un error | `with open(...) as fichero:` |
| `open(ruta)` sin `encoding` | Tildes y eñes rotas en Windows | `encoding="utf-8"` |
| Abrir con `"w"` para añadir | Se pierde el contenido anterior | `"a"` |
| `fichero.write(linea)` sin `\n` | Todo queda en una sola línea | Añadir el salto |
| Comparar líneas sin quitar el `\n` | `"hola\n" != "hola"` | `linea.strip()` |
| `linea.split(",")` para un CSV | Falla con comas dentro de un campo | Módulo `csv` |
| Abrir un CSV sin `newline=""` | Líneas en blanco entre filas en Windows | `newline=""` |
| Sumar columnas de un CSV sin convertir | Se concatenan cadenas o da `TypeError` | `int()` o `float()` |
| Ruta relativa a la carpeta del script | `FileNotFoundError` según desde dónde se lance | `Path(__file__).parent / ...` |
| `except:` o `except Exception: pass` | Los errores desaparecen sin dejar rastro | Capturar la excepción concreta |
| `try` que envuelve cincuenta líneas | No se sabe qué línea se quería proteger | `try` corto |
| Capturar para devolver `None` o `-1` | El error reaparece más lejos y es más difícil de entender | Dejar que la excepción suba |
| `raise Exception("algo falló")` | Quien llama no puede distinguir el error | Una clase concreta o propia |
| `print` para registrar | Sin fecha, sin nivel y sin forma de desactivarlo | `logging` |
| Declarar las excepciones como en Java | Python no tiene excepciones comprobadas | Documentarlas en el docstring |

## Para saber más

- Entrada y salida en el tutorial oficial: [docs.python.org/es/3/tutorial/inputoutput.html](https://docs.python.org/es/3/tutorial/inputoutput.html)
- Errores y excepciones: [docs.python.org/es/3/tutorial/errors.html](https://docs.python.org/es/3/tutorial/errors.html)
- Módulo `csv`: [docs.python.org/es/3/library/csv.html](https://docs.python.org/es/3/library/csv.html)
- Guía de `logging`: [docs.python.org/es/3/howto/logging.html](https://docs.python.org/es/3/howto/logging.html)
- Depuración en VS Code: [code.visualstudio.com/docs/python/debugging](https://code.visualstudio.com/docs/python/debugging)
