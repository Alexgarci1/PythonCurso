# Práctica 3. Librería de validación de datos

Vas a construir un paquete reutilizable, `m3_validacion`, y un programa que lo usa para dar de alta usuarios. El objetivo no son las validaciones en sí, que son sencillas, sino **organizar el código en módulos, exponer una interfaz limpia y usarla desde fuera**.

Es un caso real: en cualquier proyecto de consultoría hay una librería de utilidades compartida que usan varios programas.

Tests: `tests/test_m3_practica.py`

```bash
pytest modulo_03_funciones_modulos -v -k practica
```

## Estructura

```
ejercicios/
├── m3_validacion/
│   ├── __init__.py        interfaz pública del paquete
│   ├── texto.py           textos: vacío, nombre, correo, DNI
│   ├── numeros.py         números: entero, decimal, conversión, rango
│   └── fechas.py          fechas: validez, edad, mayoría de edad
└── m3_practica_registro.py    programa que usa el paquete
```

Trabaja en este orden: `texto.py`, `numeros.py`, `fechas.py`, `__init__.py` y, al final, `m3_practica_registro.py`.

---

## Parte A. Los módulos del paquete

### `texto.py`

| Función | Qué hace |
| --- | --- |
| `esta_vacio(texto)` | `True` si es `None`, vacío o solo espacios |
| `normalizar_nombre(nombre)` | Quita espacios sobrantes y pone la inicial de cada palabra en mayúscula |
| `es_email(texto)` | Comprobación sencilla de la forma de un correo |
| `es_dni(texto)` | Ocho dígitos y la letra de control correcta |

La letra del DNI se calcula con el resto de dividir el número entre 23. Ese resto es la posición de la letra en la constante `LETRAS_DNI`, que ya está definida en el fichero. Por ejemplo, `12345678 % 23` es 14 y `LETRAS_DNI[14]` es `"Z"`.

### `numeros.py`

| Función | Qué hace |
| --- | --- |
| `es_entero(texto)` | `True` si el texto es un entero, con signo opcional |
| `es_decimal(texto)` | `True` si es un número, con punto o coma decimal |
| `a_decimal(texto, por_defecto=None)` | Convierte a `float` o devuelve el valor por defecto |
| `en_rango(valor, minimo=None, maximo=None)` | Comprueba límites opcionales |

`es_decimal` puede apoyarse en `es_entero`, y `a_decimal` en `es_decimal`. Reutilizar funciones del mismo módulo es parte del ejercicio.

### `fechas.py`

| Función | Qué hace |
| --- | --- |
| `es_fecha(texto)` | **Ya está hecha.** Usa `try`/`except`, que veremos en el Módulo 6 |
| `edad(fecha_nacimiento, hoy=None)` | Años cumplidos |
| `es_mayor_de_edad(fecha_nacimiento, hoy=None)` | Compara la edad con `MAYORIA_DE_EDAD` |

El parámetro `hoy` existe para poder probar la función: los tests pasan una fecha fija y el resultado no depende del día en que se ejecutan. Fíjate en que su valor por defecto es `None` y no `date.today()`. Pregúntate por qué antes de seguir; la respuesta está en el apartado del valor por defecto mutable de los apuntes.

---

## Parte B. La interfaz del paquete

En `m3_validacion/__init__.py`:

1. Reexporta con importaciones relativas las once funciones del paquete, de forma que se pueda escribir `from m3_validacion import es_dni`.
2. Define `__all__` con los nombres de esas once funciones.

`__version__` ya está definido.

Comprueba el resultado en el intérprete, desde la carpeta `ejercicios`:

```python
>>> import m3_validacion
>>> m3_validacion.__version__
'1.0.0'
>>> m3_validacion.es_dni("12345678Z")
True
>>> help(m3_validacion.es_email)
```

---

## Parte C. El programa de alta

Fichero: `m3_practica_registro.py`

| Función | Qué hace |
| --- | --- |
| `validar_registro(nombre, email, dni, fecha_nacimiento, hoy=None)` | Devuelve la lista de mensajes de error, vacía si todo es correcto |
| `crear_ficha(nombre, email, dni, fecha_nacimiento)` | Devuelve un diccionario con los datos normalizados |
| `main()` | Pide los datos por teclado y muestra la ficha o los errores |

Este fichero **no valida nada por sí mismo**: importa las funciones del paquete y las combina. Si te encuentras escribiendo `"@" in email` aquí, vuelve al paquete.

Mensajes de error, en este orden:

1. `El nombre es obligatorio.`
2. `El correo no es válido.`
3. `El DNI no es válido.`
4. `La fecha de nacimiento no es válida.`
5. `Hay que ser mayor de edad.` Solo se comprueba si la fecha es válida.

Ejemplo de ejecución con errores:

```
Nombre: 
Correo: ada@ejemplo
DNI: 12345678Z
Fecha de nacimiento (AAAA-MM-DD): 1990-01-01
No se puede completar el alta:
 - El nombre es obligatorio.
 - El correo no es válido.
```

Ejemplo de ejecución correcta:

```
Nombre:   ada LOVELACE
Correo: Ada@Ejemplo.com
DNI: 12345678z
Fecha de nacimiento (AAAA-MM-DD): 1990-01-01
Alta correcta:
nombre: Ada Lovelace
email: ada@ejemplo.com
dni: 12345678Z
nacimiento: 1990-01-01
```

Ejecuta el programa desde la carpeta `ejercicios` para que Python encuentre el paquete:

```bash
cd modulo_03_funciones_modulos/ejercicios
python m3_practica_registro.py
```

---

## Criterios de evaluación

| Criterio | Peso |
| --- | --- |
| Los tests de la práctica pasan | 50 % |
| El programa de alta solo usa funciones del paquete, sin validaciones propias | 20 % |
| Las funciones del paquete se reutilizan entre sí y no repiten código | 15 % |
| Importaciones ordenadas, nombres claros y `__init__.py` con `__all__` | 15 % |

## Ampliaciones

1. Añade `es_telefono(texto)` a `texto.py`: nueve dígitos que empiezan por 6, 7, 8 o 9, con espacios opcionales entre grupos. Expórtala y escribe sus tests.
2. Añade `es_iban(texto)` para cuentas españolas: `ES` y 22 dígitos, con la comprobación de los dígitos de control.
3. Haz que `main()` vuelva a pedir solo los datos erróneos en lugar de terminar.
