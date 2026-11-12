# Práctica 1. Conversor de unidades

Fichero: `m1_practica_conversor.py`
Tests: `tests/test_m1_practica.py`

Vas a construir un pequeño programa de consola que convierte unidades. Es tu primer programa completo: funciones, entrada, salida con formato y tests.

## Requisitos

### 1. Constantes

Define estas constantes al principio del fichero:

| Constante | Valor |
| --- | --- |
| `KM_POR_MILLA` | `1.609344` |
| `KG_POR_LIBRA` | `0.45359237` |

### 2. Funciones de conversión

Todas reciben un número y devuelven un `float` sin redondear.

| Función | Conversión |
| --- | --- |
| `celsius_a_fahrenheit(grados)` | °F = °C × 9 / 5 + 32 |
| `fahrenheit_a_celsius(grados)` | °C = (°F − 32) × 5 / 9 |
| `km_a_millas(km)` | millas = km / `KM_POR_MILLA` |
| `millas_a_km(millas)` | km = millas × `KM_POR_MILLA` |
| `kg_a_libras(kg)` | libras = kg / `KG_POR_LIBRA` |
| `libras_a_kg(libras)` | kg = libras × `KG_POR_LIBRA` |

### 3. Formato del resultado

`formatear(valor, unidad_origen, resultado, unidad_destino)` devuelve una cadena con ambos valores a dos decimales:

```python
formatear(100, "°C", 212.0, "°F")   # '100.00 °C = 212.00 °F'
```

### 4. Programa principal

`main()` muestra este menú, pide una opción y un valor, e imprime el resultado formateado:

```
Conversor de unidades
1. Celsius a Fahrenheit
2. Fahrenheit a Celsius
3. Kilómetros a millas
4. Millas a kilómetros
5. Kilogramos a libras
6. Libras a kilogramos
Elige una opción (1-6):
```

Después pide el valor con el texto `Valor a convertir: `.

Usa estas abreviaturas de unidad al formatear: `°C`, `°F`, `km`, `mi`, `kg` y `lb`. Por ejemplo, con la opción 3 y el valor 10 el programa imprime `10.00 km = 6.21 mi`.

Si la opción no está entre 1 y 6, el programa imprime `Opción no válida` y termina sin pedir el valor.

## Entrega

1. Todos los tests de `tests/test_m1_practica.py` pasan.
2. El programa se puede ejecutar con `python modulo_01_introduccion/ejercicios/m1_practica_conversor.py`.
3. El código sigue PEP 8 y cada función tiene docstring.
4. Sube tu trabajo con un commit cuyo mensaje sea `Práctica 1: conversor de unidades`.

## Ampliación opcional

- Haz que el menú se repita hasta que el usuario elija `0` para salir.
- Añade una conversión de metros a pies.
