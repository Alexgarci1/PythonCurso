# Práctica 5. Modelo de dominio de una biblioteca

Vas a modelar con clases el préstamo de materiales de una biblioteca. La práctica reúne todo el módulo: una jerarquía con clase abstracta, propiedades, métodos especiales, dataclasses y una clase que coordina a las demás por composición.

Fichero: `m5_practica_biblioteca.py`
Tests: `tests/test_m5_practica.py`

```bash
pytest modulo_05_poo -v -k practica
```

## El modelo

```
Material (abstracta)          lo que se puede prestar
├── Libro                     21 días de préstamo
├── Revista                    7 días
└── Dvd                        3 días

Socio                         quien toma prestado; como mucho 3 materiales a la vez
Prestamo                      un material, un socio y una fecha
Biblioteca                    el catálogo, los socios y los préstamos en curso
```

`Biblioteca` **no hereda** de nada: contiene un diccionario de materiales, un diccionario de socios y una lista de préstamos. Es composición.

Trabaja en este orden: `Material`, las tres subclases, `Socio`, `Prestamo` y `Biblioteca`. Los tests están en el mismo orden, así que puedes ir ejecutándolos por partes:

```bash
pytest modulo_05_poo -v -k "practica and material"
pytest modulo_05_poo -v -k "practica and socio"
pytest modulo_05_poo -v -k "practica and prestamo"
pytest modulo_05_poo -v -k "practica and biblioteca"
```

---

## Parte A. Material y sus subclases

### `Material`

| Miembro | Qué hace |
| --- | --- |
| `__init__(codigo, titulo, anio)` | Guarda los tres datos y deja el material disponible, en `_disponible` |
| `disponible` | Propiedad de solo lectura |
| `dias_prestamo` | Propiedad **abstracta**. Ya está declarada |
| `prestar()` | Lo marca como no disponible. `ValueError` si ya estaba prestado |
| `devolver()` | Lo marca como disponible. `ValueError` si no estaba prestado |
| `__str__` | `[L001] Clean Code (2008)` |
| `__repr__` | `Libro('L001', 'Clean Code')`, con el nombre de la clase real del objeto |
| `__eq__` | Dos materiales son iguales si tienen el mismo código |

`__hash__` ya está escrito: al definir `__eq__` hace falta para poder usar los materiales en conjuntos y como claves.

### Subclases

| Clase | Atributo propio | `dias_prestamo` | `__str__` |
| --- | --- | --- | --- |
| `Libro` | `autor` | 21 | `[L001] Clean Code (2008), de Robert C. Martin` |
| `Revista` | `numero` | 7 | `[R001] Byte (1984), n.º 42` |
| `Dvd` | `minutos` | 3 | El heredado |

Las tres llaman a `super().__init__(...)`. `Libro` y `Revista` construyen su `__str__` a partir del heredado, con `super().__str__()`, sin repetir el formato.

---

## Parte B. Socio y Prestamo

Las dos son dataclasses. El decorador ya está puesto: te toca declarar los campos y completar los métodos.

### `Socio`

- Campos: `numero` (`int`), `nombre` (`str`) y `prestados`, una lista de materiales que empieza vacía y es propia de cada socio.
- `MAX_PRESTAMOS = 3` es un atributo de clase y ya está definido.
- `puede_tomar_prestado()` devuelve `True` si tiene menos de `MAX_PRESTAMOS` materiales.

### `Prestamo`

- Campos: `material`, `socio` y `fecha`, que es un `datetime.date`.
- `fecha_devolucion`: propiedad que suma a la fecha los días de préstamo del material.
- `dias_de_retraso(hoy)`: días transcurridos desde la fecha límite, o 0 si no ha vencido.
- `esta_vencido(hoy)`: `True` si `hoy` es posterior a la fecha límite.

Un libro prestado el 2 de noviembre se devuelve como tarde el 23. El día 23 no está vencido; el 24 lleva un día de retraso.

`hoy` se recibe como parámetro por la misma razón que en la Práctica 3: para que los tests no dependan del día en que se ejecutan.

---

## Parte C. Biblioteca

| Miembro | Qué hace |
| --- | --- |
| `__init__(nombre)` | Crea `_materiales` (diccionario), `_socios` (diccionario) y `_prestamos` (lista) vacíos |
| `anadir_material(material)` | Lo guarda por su código. `ValueError` si el código ya existe |
| `buscar(codigo)` | El material, o `None` |
| `buscar_por_titulo(texto)` | Materiales cuyo título contiene el texto, sin distinguir mayúsculas, ordenados por título |
| `disponibles()` | Materiales disponibles, ordenados por código |
| `len(biblioteca)` | Número de materiales |
| `codigo in biblioteca` | Si existe ese código |
| `for material in biblioteca` | Recorre el catálogo |
| `registrar_socio(nombre)` | Crea el socio con el siguiente número, empezando en 1, y lo devuelve |
| `socio(numero)` | El socio, o `None` |
| `prestar(codigo, numero_socio, fecha)` | Realiza el préstamo y lo devuelve |
| `devolver(codigo)` | Registra la devolución y devuelve el préstamo cerrado |
| `prestamos` | Propiedad: tupla con los préstamos en curso |
| `prestamos_vencidos(hoy)` | Préstamos vencidos, del más retrasado al menos |
| `resumen()` | `Central: 5 materiales, 3 disponibles, 2 socios` |

### Reglas de `prestar`

Se comprueban en este orden y cada una lanza `ValueError` con su mensaje:

1. `No existe el material X999`
2. `No existe el socio 99`
3. `Ada ha alcanzado el máximo de préstamos`
4. Si el material ya está prestado, el error que lanza `Material.prestar()`.

Si todo es correcto, el material queda como no disponible, se añade a `prestados` del socio y el préstamo se guarda en la biblioteca.

`Biblioteca.prestar` **no** comprueba por su cuenta si el material está disponible: llama a `material.prestar()` y deja que sea el material quien proteja su propio estado. Cada objeto es responsable de sus reglas.

### Reglas de `devolver`

Si no hay ningún préstamo en curso de ese código, lanza `ValueError` con el mensaje `No hay ningún préstamo de X999`. Si lo hay, el material vuelve a estar disponible, desaparece de `prestados` del socio y el préstamo se elimina de la biblioteca.

---

## Ejemplo de uso

```python
>>> from datetime import date
>>> biblioteca = Biblioteca("Central")
>>> biblioteca.anadir_material(Libro("L001", "Clean Code", 2008, "Robert C. Martin"))
>>> biblioteca.anadir_material(Dvd("D001", "Matrix", 1999, 136))
>>> ada = biblioteca.registrar_socio("Ada")
>>> prestamo = biblioteca.prestar("L001", ada.numero, date(2026, 11, 2))
>>> prestamo.fecha_devolucion
datetime.date(2026, 11, 23)
>>> biblioteca.disponibles()
[Dvd('D001', 'Matrix')]
>>> print(biblioteca.buscar("L001"))
[L001] Clean Code (2008), de Robert C. Martin
>>> biblioteca.prestamos_vencidos(date(2026, 11, 30))[0].dias_de_retraso(date(2026, 11, 30))
7
>>> biblioteca.resumen()
'Central: 2 materiales, 1 disponibles, 1 socios'
```

## Criterios de evaluación

| Criterio | Peso |
| --- | --- |
| Los tests de la práctica pasan | 50 % |
| Uso correcto de `super()`, sin repetir código de la clase base | 15 % |
| Encapsulación: el estado interno solo cambia a través de los métodos | 15 % |
| Cada clase aplica sus propias reglas y `Biblioteca` delega en ellas | 10 % |
| Legibilidad: nombres, métodos cortos y `__repr__` útiles | 10 % |

## Ampliaciones

1. Añade la subclase `Audiolibro`, con 14 días de préstamo. Si el diseño es bueno, no hay que tocar `Biblioteca`.
2. Añade a `Biblioteca` el método `multa(codigo, hoy)`, que devuelve 0,20 € por día de retraso.
3. Permite reservar un material prestado: una cola de socios en espera por material.
4. Mueve las clases a un paquete `biblioteca/` con `modelos.py` y `servicios.py`, como en la Práctica 3.
