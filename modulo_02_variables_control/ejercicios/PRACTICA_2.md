# Práctica 2. Adivina el número y calculadora de nómina

La práctica tiene dos partes independientes. La parte A trabaja bucles, validación de entrada y condicionales. La parte B trabaja aritmética, condicionales por tramos y formato de salida.

Tests: `tests/test_m2_practica.py`

---

## Parte A. Adivina el número

Fichero: `m2_practica_adivina.py`

El programa elige un número secreto entre 1 y 100 y el jugador tiene 7 intentos para adivinarlo. Tras cada fallo, el programa dice si el secreto es mayor o menor.

Las constantes `MINIMO`, `MAXIMO` y `MAX_INTENTOS` ya están definidas en el fichero.

### Funciones

| Función | Qué hace |
| --- | --- |
| `evaluar_intento(secreto, intento)` | Devuelve `"acierto"`, `"mayor"` si el secreto es mayor que el intento o `"menor"` si es menor |
| `es_intento_valido(texto)` | Devuelve `True` si el texto es un entero entre `MINIMO` y `MAXIMO`. Admite espacios alrededor |
| `jugar(secreto, max_intentos)` | Dirige una partida y devuelve `True` si el jugador acierta |
| `main()` | Genera el secreto con `random.randint()` y llama a `jugar` |

### Comportamiento de `jugar`

1. En cada turno pide un número con `input()`.
2. Si la entrada no es válida, imprime `Escribe un número entre 1 y 100.` y vuelve a preguntar **sin consumir intento**.
3. Si acierta, imprime `¡Correcto! Lo has adivinado en N intentos.` y devuelve `True`.
4. Si falla, imprime `El número secreto es mayor.` o `El número secreto es menor.`
5. Si agota los intentos, imprime `Has agotado los intentos. El número era S.` y devuelve `False`.

Ejemplo de partida con el secreto 42:

```
Intento 1 de 7: 50
El número secreto es menor.
Intento 2 de 7: hola
Escribe un número entre 1 y 100.
Intento 2 de 7: 25
El número secreto es mayor.
Intento 3 de 7: 42
¡Correcto! Lo has adivinado en 3 intentos.
```

`jugar` recibe el secreto como parámetro en lugar de generarlo. Así los tests pueden jugar partidas con un secreto conocido.

---

## Parte B. Calculadora de nómina

Fichero: `m2_practica_nomina.py`

A partir del salario bruto anual, el programa calcula la retención de IRPF, la cotización a la Seguridad Social y el salario neto.

> Los tramos y porcentajes de esta práctica son una simplificación didáctica. No sirven para calcular una nómina real.

### Constantes

Define al principio del fichero:

| Constante | Valor | Significado |
| --- | --- | --- |
| `SEGURIDAD_SOCIAL` | `6.35` | Porcentaje de cotización del trabajador |
| `PAGAS` | `12` | Número de pagas al año |

### Escala de IRPF

El impuesto es progresivo: cada porcentaje se aplica solo a la parte del salario que cae dentro de su tramo.

| Tramo del salario bruto anual | Tipo |
| --- | --- |
| Hasta 12.450 € | 19 % |
| De 12.450 € a 20.200 € | 24 % |
| De 20.200 € a 35.200 € | 30 % |
| De 35.200 € a 60.000 € | 37 % |
| Más de 60.000 € | 45 % |

Ejemplo con 30.000 €:

| Tramo | Importe gravado | Tipo | Retención |
| --- | --- | --- | --- |
| Hasta 12.450 | 12.450 | 19 % | 2.365,50 |
| 12.450 a 20.200 | 7.750 | 24 % | 1.860,00 |
| 20.200 a 30.000 | 9.800 | 30 % | 2.940,00 |
| Total | 30.000 | | 7.165,50 |

El error habitual es aplicar el 30 % a los 30.000 € completos.

### Funciones

Todas redondean su resultado a dos decimales con `round()`.

| Función | Qué devuelve |
| --- | --- |
| `calcular_irpf(bruto_anual)` | La retención anual según la escala |
| `calcular_seguridad_social(bruto_anual)` | El bruto por `SEGURIDAD_SOCIAL` entre 100 |
| `calcular_neto_anual(bruto_anual)` | Bruto menos IRPF menos Seguridad Social |
| `tipo_efectivo(bruto_anual)` | Porcentaje que supone el IRPF sobre el bruto. Con bruto cero o negativo devuelve `0.0` |
| `formatear_nomina(bruto_anual)` | El resumen en cinco líneas, descrito abajo |
| `main()` | Pide el bruto con `input()` e imprime el resumen |

### Formato del resumen

Cinco líneas separadas por saltos de línea, sin salto al final. La etiqueta ocupa 20 caracteres alineada a la izquierda y el importe 12 caracteres alineado a la derecha, con separador de miles y dos decimales. IRPF y Seguridad Social se muestran en negativo.

```
Bruto anual            30,000.00
IRPF (23.89 %)         -7,165.50
Seguridad Social       -1,905.00
Neto anual             20,929.50
Neto mensual            1,744.12
```

Pista: construye primero la etiqueta del IRPF en una variable y después alinéala.

En `main()`, si lo que escribe el usuario no es un número positivo, el programa imprime `Importe no válido` y termina.

---

## Entrega

1. Todos los tests de `tests/test_m2_practica.py` pasan.
2. Los dos programas se pueden ejecutar desde la terminal.
3. No hay números mágicos repetidos: usa las constantes.
4. Ninguna función de cálculo llama a `input()` ni a `print()`.
5. Commit con el mensaje `Práctica 2: adivina el número y nómina`.

## Ampliación opcional

- Parte A: al terminar la partida, pregunta si se quiere jugar otra vez.
- Parte A: añade un modo en el que el ordenador adivina un número que piensa el usuario, usando búsqueda binaria.
- Parte B: admite 14 pagas como segundo dato de entrada.
