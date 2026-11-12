# Módulo 2. Ejercicios

Cada fichero contiene funciones con su firma y su docstring. El docstring dice exactamente qué debe hacer la función e incluye un ejemplo. Sustituye cada `raise NotImplementedError` por tu código y comprueba el resultado con:

```bash
pytest modulo_02_variables_control -v
```

Para ejecutar solo los tests de un ejercicio:

```bash
pytest modulo_02_variables_control -v -k ej1
```

## Ejercicio 1. Tipos de datos y conversiones

Fichero: `m2_ej1_tipos.py`

| Función | Qué practica |
| --- | --- |
| `nombre_del_tipo(valor)` | `isinstance()` y la relación entre `bool` e `int` |
| `a_entero(texto)` | Validar antes de convertir con `int()` |
| `casi_iguales(a, b, tolerancia)` | Comparación de decimales |
| `media(a, b, c)` | División real y `round()` |
| `partir_euros(importe)` | Errores de coma flotante y `divmod()` |

Pista para `nombre_del_tipo`: el orden en que compruebas los tipos importa. Prueba `isinstance(True, int)` en el intérprete.

Pista para `partir_euros`: calcula `12.34 * 100` en el intérprete antes de escribir nada.

## Ejercicio 2. Operadores

Fichero: `m2_ej2_operadores.py`

| Función | Qué practica |
| --- | --- |
| `es_bisiesto(anio)` | Operadores lógicos y resto |
| `segundos_a_hms(segundos)` | División entera, resto y formato con ceros |
| `nombre_o_anonimo(nombre)` | Valores falsos y `or` |
| `en_rango(valor, minimo, maximo)` | Comparaciones encadenadas |
| `es_par(numero)` | Resto con números negativos |
| `reparto(total, personas)` | División entera y resto |

Reto: resuelve `es_bisiesto`, `en_rango` y `es_par` con una sola línea `return`, sin ningún `if`.

## Ejercicio 3. Condicionales

Fichero: `m2_ej3_condicionales.py`

| Función | Qué practica |
| --- | --- |
| `calificacion(nota)` | `if` / `elif` / `else` y validación de rango |
| `precio_entrada(edad, es_festivo)` | Cláusulas de guarda y expresión condicional |
| `describir_http(codigo)` | `match` con alternativas |
| `mayor_de_tres(a, b, c)` | Comparaciones, sin usar `max()` |
| `tipo_triangulo(a, b, c)` | Condiciones compuestas |

## Ejercicio 4. Bucles

Fichero: `m2_ej4_bucles.py`

| Función | Qué practica |
| --- | --- |
| `factorial(n)` | `for` con `range()` y acumulador |
| `es_primo(n)` | Salida anticipada de un bucle |
| `invertir(texto)` | Recorrer una cadena |
| `contar_vocales(texto)` | Recorrer con condición y `in` |
| `suma_digitos(numero)` | `while` |
| `fizzbuzz(n)` | `for` con `if` / `elif` |
| `tabla_multiplicar(numero)` | Formato de columnas con f-strings |
| `primer_multiplo_comun(a, b)` | `while` con condición compuesta |

En `invertir` y `factorial` usa un bucle aunque conozcas otra forma: el objetivo es practicar la estructura.

## Práctica 2

El enunciado está en [`PRACTICA_2.md`](PRACTICA_2.md).

## Para quien termine antes

- Reescribe `fizzbuzz` sin usar el operador `%` más de dos veces por vuelta.
- Añade a `es_primo` una versión que use la cláusula `else` del bucle `for`.
- Ejecuta `python -m doctest -v modulo_02_variables_control/ejercicios/m2_ej2_operadores.py`. Los ejemplos de los docstrings también son tests.
