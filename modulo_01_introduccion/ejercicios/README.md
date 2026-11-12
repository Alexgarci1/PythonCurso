# Módulo 1. Ejercicios

Completa cada fichero sustituyendo los `raise NotImplementedError` por tu código. Comprueba tu trabajo con:

```bash
pytest modulo_01_introduccion -v
```

## Ejercicio 0. Entorno (sin tests)

1. Clona el repositorio, crea el entorno virtual, actívalo e instala las dependencias.
2. Selecciona el intérprete de `.venv` en VS Code.
3. Abre el intérprete interactivo y prueba `import this`, `type(3.5)`, `dir("hola")` y `help(print)`.
4. Ejecuta los cuatro ficheros de la carpeta `ejemplos/`.

## Ejercicio 1. Saludo

Fichero: `m1_ej1_saludo.py`

1. Completa `saludar(nombre)` para que devuelva el texto `Hola, <nombre>. ¡Te damos la bienvenida al curso!`.
2. El nombre puede llegar con espacios sobrantes y con cualquier combinación de mayúsculas. Límpialo y ponlo con la inicial de cada palabra en mayúscula. Pista: explora los métodos de `str` con `dir("")`.
3. Si el nombre queda vacío, la función saluda a `Anónimo`.
4. Completa `main()` para que pida el nombre por teclado e imprima el saludo.

## Ejercicio 2. Operaciones con dos números

Fichero: `m1_ej2_operaciones.py`

Python tiene tres operadores que no funcionan igual en otros lenguajes: `/` siempre devuelve un `float`, `//` es la división entera y `**` es la potencia.

1. Completa las funciones `sumar`, `restar`, `multiplicar`, `dividir`, `division_entera`, `resto` y `potencia`.
2. Completa `resumen(a, b)` para que devuelva una única cadena con este formato exacto, con los resultados separados por ` | `:

```
7 + 2 = 9 | 7 - 2 = 5 | 7 * 2 = 14 | 7 / 2 = 3.50 | 7 // 2 = 3 | 7 % 2 = 1 | 7 ** 2 = 49
```

   La división real se muestra siempre con dos decimales.
3. Completa `main()` para que pida dos números enteros e imprima el resumen.

## Ejercicio 3. Código con estilo

Fichero: `m1_ej3_estilo.py`

El fichero contiene una función que funciona, pero está escrita ignorando PEP 8. Reescríbela sin cambiar lo que hace:

1. Renombra la función a `precio_final` y sus parámetros a `precio`, `iva` y `descuento`.
2. Usa 4 espacios de sangría, una sentencia por línea y espacios alrededor de los operadores.
3. Añade un docstring que explique qué hace.
4. Sustituye el número mágico `21` por una constante `IVA_GENERAL`.

Los tests comprueban el resultado, los nombres, el docstring y la constante.

## Práctica 1

El enunciado está en [`PRACTICA_1.md`](PRACTICA_1.md).
