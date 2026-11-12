# Práctica 6. Importador de ventas en CSV

Cada mes llega un CSV de ventas tecleado a mano y cada mes trae errores: fechas con otro formato, cantidades con letras, campos vacíos. El importador tiene que **aprovechar las filas buenas, apartar las malas explicando por qué** y dejar un resumen. Lo que no puede hacer es detenerse en la primera fila incorrecta ni cargar datos erróneos sin avisar.

Es el tipo de programa que más se escribe en un proyecto de integración de datos.

Fichero: `m6_practica_importador.py`
Tests: `tests/test_m6_practica.py`
Datos: `datos/ventas_con_errores.csv`, con 18 filas de las que 6 son incorrectas

```bash
pytest modulo_06_archivos_excepciones -v -k practica
```

## Excepciones

Defínelas tú. No están en la plantilla.

```
ErrorDeImportacion (Exception)     base de los errores del importador
├── FicheroNoValido                el fichero no existe o le faltan columnas
└── FilaNoValida                   una fila tiene un dato incorrecto
```

La diferencia entre las dos es el centro de la práctica:

- `FilaNoValida` es un error **recuperable**: se anota y se sigue con la fila siguiente.
- `FicheroNoValido` es un error **no recuperable**: no hay nada que procesar y tiene que subir hasta `main()`.

## Funciones

| Función | Qué hace |
| --- | --- |
| `validar_fila(fila)` | Devuelve la venta con los tipos convertidos o lanza `FilaNoValida` |
| `importar_ventas(ruta)` | Devuelve `(ventas, errores)` o lanza `FicheroNoValido` |
| `resumen_por_region(ventas)` | Agrupa por región |
| `exportar_resumen(ruta, ventas)` | Escribe el resumen en CSV |
| `escribir_errores(ruta, errores)` | Escribe los errores en un fichero de texto |
| `procesar(entrada, carpeta_salida)` | Lo coordina todo y devuelve las cantidades |
| `main()` | **Ya está hecha.** Captura `ErrorDeImportacion` y configura el logging |

### `validar_fila(fila)`

Recibe un diccionario tal como lo entrega `csv.DictReader`, con todos los valores como cadenas, y devuelve un diccionario **nuevo** con los campos de `CAMPOS`, sin espacios alrededor, `unidades` como `int` y `precio` como `float`.

Lanza `FilaNoValida` con el primer problema que encuentre, en este orden:

| Comprobación | Mensaje |
| --- | --- |
| Algún campo de `CAMPOS` falta o está vacío | `falta el campo vendedor` |
| La fecha no es una fecha ISO válida | `fecha no válida: 03/10/2026` |
| Las unidades no son un entero mayor que cero | `unidades no válidas: tres` |
| El precio no es un número mayor que cero | `precio no válido: 29,5` |

Los campos se comprueban en el orden de `CAMPOS` y se informa del primero que falte.

Para validar la fecha y convertir los números, intenta la conversión y captura el `ValueError`: `date.fromisoformat()`, `int()` y `float()`. No escribas comprobaciones con `isdigit()`.

### `importar_ventas(ruta)`

Devuelve una tupla con la lista de ventas válidas y la lista de errores. Cada error es un texto con el número de línea del fichero, contando la cabecera como línea 1:

```
Línea 3: unidades no válidas: tres
```

Además, por cada fila descartada registra un aviso con `logger.warning`.

Lanza `FicheroNoValido` en dos casos:

- El fichero no existe: mensaje `No existe el fichero <ruta>`, encadenado con el `FileNotFoundError` original mediante `raise ... from`.
- A la cabecera le falta alguna columna de `CAMPOS`: mensaje `Faltan columnas: region, precio`, con los nombres en el orden de `CAMPOS`.

Fíjate en dónde va cada `try`: el que captura `FilaNoValida` está **dentro** del bucle y protege una sola fila; el que captura `FileNotFoundError` está **fuera** y protege la apertura.

### `resumen_por_region(ventas)` y `exportar_resumen(ruta, ventas)`

El resumen es una lista de diccionarios con las claves de `CAMPOS_RESUMEN`, ordenada de mayor a menor importe. Con `datos/ventas_con_errores.csv` el fichero exportado queda así:

```
region,ventas,unidades,importe
Norte,5,23,8413.8
Sur,4,40,2317.0
Centro,3,19,1959.5
```

### `escribir_errores(ruta, errores)`

Un error por línea. Con el fichero de ejemplo:

```
Línea 3: unidades no válidas: tres
Línea 5: fecha no válida: 03/10/2026
Línea 8: falta el campo vendedor
Línea 10: unidades no válidas: -2
Línea 13: precio no válido: 29,5
Línea 15: precio no válido: 0
```

### `procesar(entrada, carpeta_salida)`

1. Importa el fichero. Si lanza `FicheroNoValido`, **no la captura** y no escribe nada.
2. Crea la carpeta de salida si no existe.
3. Escribe en ella `resumen.csv` y `errores.txt`.
4. Registra con `logger.info` un mensaje final con las cantidades.
5. Devuelve `{"leidas": 18, "validas": 12, "descartadas": 6}`.

## Ejecutar el programa

```bash
cd modulo_06_archivos_excepciones/ejercicios
python m6_practica_importador.py
python m6_practica_importador.py ../datos/ventas.csv salida_octubre
python m6_practica_importador.py no_existe.csv
```

Sin argumentos importa `datos/ventas_con_errores.csv` y deja el resultado en `salida_practica_6/`. La salida por pantalla es:

```
WARNING Línea 3 descartada: unidades no válidas: tres
WARNING Línea 5 descartada: fecha no válida: 03/10/2026
WARNING Línea 8 descartada: falta el campo vendedor
WARNING Línea 10 descartada: unidades no válidas: -2
WARNING Línea 13 descartada: precio no válido: 29,5
WARNING Línea 15 descartada: precio no válido: 0
INFO Importación terminada: 12 válidas y 6 descartadas
Leídas 18 filas: 12 válidas y 6 descartadas. Resultados en salida_practica_6
```

Lee `main()` aunque esté hecha: es el único lugar del programa que captura `ErrorDeImportacion`, que configura el logging y que usa `print`. Todas las demás funciones lanzan o devuelven.

## Criterios de evaluación

| Criterio | Peso |
| --- | --- |
| Los tests de la práctica pasan | 50 % |
| Cada `try` protege solo la operación que puede fallar y captura la excepción concreta | 20 % |
| Excepciones propias bien usadas: jerarquía, mensajes con el valor y `raise ... from` | 15 % |
| Ficheros con `with`, `encoding` y `newline`; logging en lugar de `print` | 15 % |

## Ampliaciones

1. Acepta también el delimitador punto y coma y la coma decimal: `29,5` pasaría a ser válido.
2. Detecta filas duplicadas y descártalas con el motivo `fila repetida`.
3. Añade a `main()` la opción `--log fichero` para enviar el registro a un fichero.
4. Conecta el importador con la Práctica 4: después de importar, genera el informe con `generar_informe(ventas)`.
