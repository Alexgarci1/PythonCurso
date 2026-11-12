# Práctica 4. Análisis de ventas

El departamento comercial te pasa las ventas de octubre y quiere un informe: cuánto se ha vendido, dónde, de qué y quién lo ha vendido. Los datos están en memoria; en el Módulo 6 los leerás de un fichero CSV con exactamente la misma forma.

Tests: `tests/test_m4_practica.py`

```bash
pytest modulo_04_colecciones -v -k practica
```

## Los datos

Fichero: `m4_datos_ventas.py`, que **ya está hecho**. Define la lista `VENTAS` con 20 registros como este:

```python
{
    "fecha": "2026-10-01",
    "vendedor": "Ada",
    "region": "Norte",
    "producto": "Portátil",
    "categoria": "Equipos",
    "unidades": 2,
    "precio": 950.0,
}
```

## Las funciones

Fichero: `m4_practica_ventas.py`

| Función | Qué hace |
| --- | --- |
| `importe(venta)` | Unidades por precio de una venta, con dos decimales |
| `total_ventas(ventas)` | Suma de los importes |
| `filtrar_ventas(ventas, *, region, categoria, vendedor, desde, hasta)` | Ventas que cumplen todos los criterios indicados |
| `importe_por(ventas, campo)` | Importe total agrupado por un campo |
| `unidades_por_producto(ventas)` | Unidades totales de cada producto |
| `ranking(ventas, campo, cantidad=3)` | Los grupos con mayor importe, como lista de tuplas |
| `producto_mas_vendido(ventas)` | El producto con más unidades |
| `ticket_medio(ventas)` | Importe medio por venta |
| `generar_informe(ventas)` | El informe completo como texto |
| `main()` | **Ya está hecha.** Imprime el informe general y uno filtrado |

Trabaja en ese orden. Cada función se apoya en las anteriores: `total_ventas` usa `importe`, `ranking` usa `importe_por`, `ticket_medio` usa `total_ventas` y `generar_informe` las usa casi todas.

### Detalles

- **Ninguna función modifica** la lista de ventas ni sus diccionarios.
- **`filtrar_ventas`:** todos los criterios son opcionales y solo se pasan por nombre. Un criterio que vale `None` no se aplica. Sin criterios devuelve todas las ventas. Las fechas `desde` y `hasta` están incluidas en el intervalo.
- **Fechas:** las fechas ISO se pueden comparar directamente como cadenas, porque su orden alfabético coincide con el cronológico. No hace falta `datetime`.
- **`ranking`:** ordena de mayor a menor importe y, a igual importe, por orden alfabético de la clave.
- **`producto_mas_vendido`:** en caso de empate a unidades, el primero por orden alfabético. Sin ventas devuelve `None`.
- **Listas vacías:** todas las funciones tienen que funcionar con una lista de ventas vacía.

## El informe

`generar_informe(VENTAS)` devuelve exactamente este texto, sin salto de línea al final:

```
============================================
             INFORME DE VENTAS
============================================
Ventas registradas                        20
Importe total                      21,686.80
Ticket medio                        1,084.34
Producto más vendido               Antivirus
--------------------------------------------
Por región
  Norte                            12,351.30
  Sur                               6,062.00
  Centro                            3,273.50
--------------------------------------------
Por categoría
  Equipos                          14,000.00
  Software                          4,135.00
  Periféricos                       3,551.80
--------------------------------------------
Por vendedor
  Ada                               7,435.30
  Grace                             5,339.50
  Alan                              4,525.00
  Linus                             4,387.00
============================================
```

Formato:

- El ancho total es de 44 caracteres y está en la constante `ANCHO`.
- El título va centrado en ese ancho.
- En las cuatro líneas de resumen, la etiqueta ocupa 30 caracteres alineada a la izquierda y el valor 14 alineado a la derecha.
- En los desgloses, dos espacios, la clave en 28 caracteres a la izquierda y el importe en 14 a la derecha.
- Los importes llevan separador de miles y dos decimales: `{valor:,.2f}`.
- Cada desglose muestra **todos** sus grupos, de mayor a menor importe.
- Sin ventas, el producto más vendido se muestra como un guion y los desgloses no tienen líneas.

Los tests comparan línea a línea sin tener en cuenta los espacios del final de cada línea.

Consejo: acumula las líneas en una lista y únelas con `"\n".join(lineas)`.

## Criterios de evaluación

| Criterio | Peso |
| --- | --- |
| Los tests de la práctica pasan | 50 % |
| Las funciones se reutilizan entre sí, sin fórmulas ni bucles repetidos | 20 % |
| Uso idiomático de las colecciones: comprensiones, `sum()`, `sorted()` con `key`, `get()` | 20 % |
| Legibilidad: nombres, funciones cortas y sin modificar los datos de entrada | 10 % |

## Ampliaciones

1. Añade al informe un desglose «Por semana» usando `datetime.date.fromisoformat(...).isocalendar()`.
2. Escribe `comparar_periodos(ventas, corte)`, que devuelve la variación en porcentaje del importe entre las ventas anteriores y posteriores a una fecha.
3. Añade a `ranking` un parámetro `medida` que permita ordenar por importe o por unidades.
4. Escribe `mejor_vendedor_por_region(ventas)`, que devuelve un diccionario con el vendedor de mayor importe en cada región.
