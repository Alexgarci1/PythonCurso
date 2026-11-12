# Módulo 6. Ejercicios

Sustituye cada `raise NotImplementedError` por tu código y comprueba el resultado con:

```bash
pytest modulo_06_archivos_excepciones -v
pytest modulo_06_archivos_excepciones -v -k ej2        # solo un ejercicio
```

Los tests crean sus ficheros en una carpeta temporal y la borran al terminar: no tienes que preparar nada ni limpiar después. Los datos de ejemplo para tus propias pruebas están en la carpeta `datos/` del módulo.

Dos normas para todo el módulo:

- Todos los ficheros se abren con `with` y con `encoding="utf-8"`.
- Los CSV se abren además con `newline=""`.

## Ejercicio 1. Ficheros de texto

Fichero: `m6_ej1_ficheros.py`

| Función | Qué practica |
| --- | --- |
| `contar_lineas(ruta)` | Recorrer un fichero línea a línea |
| `leer_lineas_utiles(ruta)` | `strip()` y filtrado de líneas |
| `escribir_lineas(ruta, lineas)` | Modo `"w"`, saltos de línea y creación de carpetas |
| `anadir_linea(ruta, linea)` | Modo `"a"` |
| `buscar(ruta, texto)` | `enumerate` sobre un fichero |
| `numerar(origen, destino)` | Dos ficheros abiertos a la vez |
| `ficheros_por_extension(carpeta, extension)` | `Path.glob()` |

Pruébalas en el intérprete con `datos/notas.txt`.

## Ejercicio 2. CSV

Fichero: `m6_ej2_csv.py`

| Función | Qué practica |
| --- | --- |
| `leer_csv(ruta, delimitador)` | `csv.DictReader` |
| `cabecera(ruta)` | `csv.reader` y `next()` |
| `escribir_csv(ruta, registros, campos)` | `csv.DictWriter` |
| `leer_ventas(ruta)` | Conversión de tipos |
| `total_columna(ruta, columna)` | Reutilizar `leer_csv` |
| `filtrar_csv(origen, destino, columna, valor)` | Leer, filtrar y escribir |
| `convertir_delimitador(origen, destino, de, a)` | `csv.reader` y `csv.writer` con delimitador |

`leer_ventas(datos/ventas.csv)` devuelve exactamente la lista `VENTAS` de la Práctica 4. Compruébalo: importa tus funciones de `m4_practica_ventas` y genera el informe con los datos leídos del fichero.

## Ejercicio 3. Excepciones

Fichero: `m6_ej3_excepciones.py`

| Función o clase | Qué practica |
| --- | --- |
| `a_entero(texto, por_defecto)` | `try`/`except` con dos tipos de excepción |
| `dividir(a, b)` | Capturar solo lo que se sabe manejar |
| `leer_o_vacio(ruta)` | `FileNotFoundError` |
| `validar_edad(edad)` | `raise` con `TypeError` y `ValueError` |
| `ErrorDeCuenta`, `ImporteNoValido`, `SaldoInsuficiente` | Jerarquía de excepciones propias con atributos |
| `retirar(saldo, importe)` | Lanzar excepciones propias |
| `convertir_todos(textos)` | `try` dentro de un bucle: un fallo no detiene el resto |
| `ejecutar(accion, registro)` | `else`, `finally` y volver a lanzar con `raise` |
| `ErrorDeConfiguracion`, `puerto_configurado(configuracion)` | `raise ... from` |

Las excepciones propias no están en la plantilla: las defines tú.

- `ErrorDeCuenta` hereda de `Exception`.
- `ImporteNoValido` y `SaldoInsuficiente` heredan de `ErrorDeCuenta`.
- `SaldoInsuficiente(saldo, importe)` guarda los dos valores en atributos con esos nombres y su mensaje los contiene.
- `ErrorDeConfiguracion` hereda de `Exception`.

## Ejercicio 4. Depurar

Fichero: `ejemplos/06_para_depurar.py`. No tiene tests.

El programa tiene tres errores. Uno lo detiene con una excepción; los otros dos hacen que termine con un resultado incorrecto, que son los difíciles. Encuéntralos con el depurador de VS Code siguiendo las instrucciones del propio fichero. La salida correcta es:

```
Ventas leídas: 20
Importe total: 21686.80
Mejor vendedor: Ada (7435.30)
```

Para cada error, anota en qué línea estaba, cómo lo has localizado y qué has cambiado.

## Si terminas antes

1. Añade logging a `convertir_todos`: un `warning` por cada texto rechazado. Configura el nivel desde un pequeño `main()`.
2. Escribe `guardar_json(ruta, datos)` y `cargar_json(ruta)`, y convierte `datos/ventas.csv` en un fichero JSON.
3. Vuelve a la Práctica 5 y sustituye los `ValueError` por excepciones propias: `MaterialNoDisponible`, `SocioNoEncontrado` y `LimiteDePrestamos`, con una base común `ErrorDeBiblioteca`.
