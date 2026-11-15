# Módulo 5. Programación Orientada a Objetos (6 horas)

Al terminar este módulo sabrás modelar un dominio con clases de Python y aplicar las convenciones del lenguaje, que en varios puntos son distintas de las de Java y C#.

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 5.1 | Clases y objetos | 0,5 h |
| 5.2 | Constructores: `__init__` y `self` | 0,5 h |
| 5.3 | Atributos y métodos | 1 h |
| 5.4 | Herencia | 1 h |
| 5.5 | Polimorfismo y duck typing | 0,75 h |
| 5.6 | Encapsulación | 0,75 h |
| 5.7 | Buenas prácticas y Práctica 5 | 1,5 h |

## Lo que cambia respecto a Java y C#

Ya conoces la orientación a objetos. Estas son las diferencias que conviene tener presentes desde el principio:

| En Java o C# | En Python |
| --- | --- |
| Todo vive dentro de una clase | Las funciones sueltas son normales; se usa una clase cuando hay estado y comportamiento que van juntos |
| `this` implícito | `self` explícito, como primer parámetro de cada método |
| Los atributos se declaran en la clase | Se crean al asignarlos, normalmente en `__init__` |
| `private`, `protected`, `public` | Todo es público; la privacidad es una convención de nombres |
| Getters y setters | Atributos públicos y, si hace falta lógica, `@property` |
| Sobrecarga de constructores y métodos | No existe: valores por defecto y métodos de clase |
| Interfaces | Duck typing, clases abstractas o `Protocol` |
| `toString()`, `equals()`, `compareTo()` | Métodos especiales: `__str__`, `__eq__`, `__lt__` |
| `new Clase()` | `Clase()` |

---

## 5.1 Clases y objetos

### Definir una clase y crear objetos

```python
class Empleado:
    """Una persona que trabaja en la empresa."""

    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def subir_sueldo(self, porcentaje):
        self.salario = round(self.salario * (1 + porcentaje / 100), 2)


ada = Empleado("Ada", 52000)          # sin new
linus = Empleado("Linus", 48000)

ada.subir_sueldo(10)
print(ada.nombre, ada.salario)        # Ada 57200.0
print(type(ada))                      # <class '__main__.Empleado'>
print(isinstance(ada, Empleado))      # True
```

Los nombres de clase se escriben en `PascalCase`; los de métodos y atributos, en `snake_case`.

### Todo es un objeto

Los enteros, las cadenas, las listas, las funciones y las propias clases son objetos. `"hola".upper()` y `[1, 2].append(3)` son llamadas a métodos, igual que `ada.subir_sueldo(10)`.

### Los objetos son dinámicos

Los atributos de un objeto se guardan en un diccionario y se pueden añadir en cualquier momento:

```python
print(ada.__dict__)           # {'nombre': 'Ada', 'salario': 57200.0}
ada.departamento = "IT"       # se puede, pero no se debe
```

Que el lenguaje lo permita no significa que sea buena idea. La norma es **crear todos los atributos en `__init__`**, para que cualquiera que lea la clase sepa qué contiene un objeto.

### Identidad e igualdad

```python
a = Empleado("Ada", 52000)
b = Empleado("Ada", 52000)
c = a

a is c        # True: el mismo objeto
a is b        # False: dos objetos distintos
a == b        # False: por defecto, == compara identidad
```

Para que dos objetos con los mismos datos sean iguales hay que definir `__eq__`, que veremos en la unidad 5.3.

### ¿Clase, diccionario o función?

- Si solo necesitas **agrupar datos**, un diccionario o una `dataclass` bastan.
- Si solo necesitas **comportamiento**, escribe funciones en un módulo.
- Si tienes **datos y operaciones que mantienen esos datos coherentes**, usa una clase.

Una clase con un único método además de `__init__` suele ser una función disfrazada.

---

## 5.2 Constructores: `__init__` y `self`

### self

`self` es el objeto sobre el que se llama al método. Python lo pasa automáticamente como primer argumento:

```python
ada.subir_sueldo(10)
Empleado.subir_sueldo(ada, 10)        # exactamente lo mismo
```

Se llama `self` por convención, no porque sea una palabra reservada. Dos consecuencias:

- En la definición de cada método hay que escribir `self` como primer parámetro.
- Dentro del método, a los atributos y a otros métodos se accede siempre con `self.`: `self.salario`, `self.calcular()`.

Olvidar `self` en la definición produce uno de los errores más desconcertantes para quien empieza:

```python
class Saludo:
    def hola():                       # falta self
        print("hola")


Saludo().hola()
# TypeError: Saludo.hola() takes 0 positional arguments but 1 was given
```

### `__init__`

`__init__` es el inicializador: se ejecuta justo después de crear el objeto y su trabajo es dejarlo en un estado válido. No devuelve nada.

```python
class Cuenta:
    def __init__(self, titular, saldo=0.0, moneda="EUR"):
        self.titular = titular
        self.saldo = saldo
        self.moneda = moneda
        self.movimientos = []         # atributo que no viene de un parámetro


cuenta = Cuenta("Ada")
otra = Cuenta("Linus", 500, moneda="USD")
```

Como no hay sobrecarga, las distintas formas de construir un objeto se resuelven con valores por defecto y, cuando no basta, con métodos de clase (unidad 5.3).

El aviso del Módulo 3 se aplica igual: **nunca un valor por defecto mutable**.

```python
def __init__(self, titular, movimientos=[]):      # MAL: lista compartida entre objetos
def __init__(self, titular, movimientos=None):    # BIEN
    self.movimientos = movimientos if movimientos is not None else []
```

### Validar en el constructor

Un objeto no debería poder crearse en un estado incorrecto. Lo habitual es lanzar una excepción con `raise`, que veremos a fondo en el Módulo 6:

```python
class Cuenta:
    def __init__(self, titular, saldo=0.0):
        if saldo < 0:
            raise ValueError("El saldo inicial no puede ser negativo")
        self.titular = titular
        self.saldo = saldo
```

---

## 5.3 Atributos y métodos

### Atributos de instancia y de clase

Un atributo de instancia pertenece a cada objeto. Un atributo de clase se define en el cuerpo de la clase y lo comparten todos los objetos.

```python
class Empleado:
    empresa = "Consultora S.A."       # atributo de clase
    plantilla = 0

    def __init__(self, nombre):
        self.nombre = nombre          # atributo de instancia
        Empleado.plantilla += 1


ada = Empleado("Ada")
linus = Empleado("Linus")
print(ada.empresa, Empleado.empresa, Empleado.plantilla)     # Consultora S.A. Consultora S.A. 2
```

Al leer `ada.empresa`, Python busca primero en el objeto y después en la clase. Al **asignar** `ada.empresa = "Otra"`, en cambio, se crea un atributo de instancia que tapa al de clase solo para ese objeto. Para modificar el atributo de clase hay que hacerlo a través de la clase: `Empleado.empresa = "Otra"`.

Los atributos de clase se usan para constantes y valores comunes. Cuidado con los mutables: una lista como atributo de clase es compartida por todos los objetos.

### Métodos de instancia, de clase y estáticos

```python
from datetime import date


class Empleado:
    SALARIO_MINIMO = 16576

    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def salario_mensual(self):                    # de instancia: recibe el objeto
        return round(self.salario / 12, 2)

    @classmethod
    def desde_texto(cls, texto):                  # de clase: recibe la clase
        nombre, salario = texto.split(";")
        return cls(nombre.strip(), float(salario))

    @staticmethod
    def es_salario_valido(salario):               # estático: no recibe ni objeto ni clase
        return salario >= Empleado.SALARIO_MINIMO


ada = Empleado.desde_texto("Ada; 52000")
Empleado.es_salario_valido(12000)                 # False
```

| Tipo | Primer parámetro | Para qué |
| --- | --- | --- |
| De instancia | `self` | Leer o modificar el estado del objeto. Es el caso normal |
| `@classmethod` | `cls` | **Constructores alternativos** y operaciones sobre la clase |
| `@staticmethod` | Ninguno | Funciones de utilidad relacionadas con la clase |

Los métodos de clase son la respuesta de Python a la sobrecarga de constructores: `date.today()`, `date.fromisoformat("2026-11-25")` y `dict.fromkeys(...)` son ejemplos de la librería estándar. Se usa `cls(...)` y no el nombre de la clase para que funcionen también en las subclases.

Si un método estático no tiene una relación clara con la clase, es mejor una función de módulo.

### Métodos especiales

Los métodos con doble guion bajo a cada lado, llamados *dunder*, son los que Python invoca cuando usas un operador o una función integrada con tus objetos. No se llaman directamente.

```python
class Dinero:
    def __init__(self, cantidad, moneda="EUR"):
        self.cantidad = cantidad
        self.moneda = moneda

    def __repr__(self):
        return f"Dinero({self.cantidad!r}, {self.moneda!r})"

    def __str__(self):
        return f"{self.cantidad:.2f} {self.moneda}"

    def __eq__(self, otro):
        if not isinstance(otro, Dinero):
            return NotImplemented
        return (self.cantidad, self.moneda) == (otro.cantidad, otro.moneda)

    def __lt__(self, otro):
        return self.cantidad < otro.cantidad

    def __add__(self, otro):
        return Dinero(self.cantidad + otro.cantidad, self.moneda)


precio = Dinero(19.9)
print(precio)                         # 19.90 EUR            usa __str__
print([precio])                       # [Dinero(19.9, 'EUR')] usa __repr__
print(precio == Dinero(19.9))         # True                 usa __eq__
print(precio + Dinero(0.1))           # 20.00 EUR            usa __add__
print(sorted([Dinero(5), Dinero(2)])) # usa __lt__
```

| Método | Se invoca con | Equivalente en Java |
| --- | --- | --- |
| `__init__` | `Clase(...)` | Constructor |
| `__str__` | `str(x)`, `print(x)`, f-strings | `toString()` |
| `__repr__` | `repr(x)`, el REPL, el depurador, listas | No tiene |
| `__eq__` | `x == y` | `equals()` |
| `__lt__`, `__le__`, `__gt__`, `__ge__` | `<`, `<=`, `>`, `>=`, `sorted()` | `compareTo()` |
| `__hash__` | `hash(x)`, claves de diccionario y conjuntos | `hashCode()` |
| `__len__` | `len(x)` | `size()` |
| `__contains__` | `elemento in x` | `contains()` |
| `__iter__` | `for elemento in x` | `Iterable` |
| `__getitem__` | `x[clave]` | `get()` |
| `__add__`, `__sub__`, `__mul__` | `+`, `-`, `*` | No tiene |
| `__bool__` | `if x:` | No tiene |

Recomendaciones:

- **Define siempre `__repr__`.** Es lo que ves al depurar. La convención es que parezca el código que crearía el objeto.
- `__str__` es la versión para el usuario. Si no existe, se usa `__repr__`.
- En `__eq__`, devuelve `NotImplemented` si el otro objeto no es del tipo esperado. Python probará entonces otras alternativas.
- Si defines `__eq__`, el objeto deja de poder usarse en conjuntos y como clave, salvo que definas también `__hash__`. Solo tiene sentido en objetos inmutables.
- Sobrecarga operadores solo cuando el significado sea evidente. `pedido + linea` no lo es.

Un contenedor propio se comporta como uno integrado con tres métodos:

```python
class Equipo:
    def __init__(self):
        self._miembros = []

    def anadir(self, nombre):
        self._miembros.append(nombre)

    def __len__(self):
        return len(self._miembros)

    def __contains__(self, nombre):
        return nombre in self._miembros

    def __iter__(self):
        return iter(self._miembros)


equipo = Equipo()
equipo.anadir("Ada")
len(equipo), "Ada" in equipo, [nombre.upper() for nombre in equipo]
```

---

## 5.4 Herencia

### Herencia simple y super()

```python
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def salario_mensual(self):
        return round(self.salario / 12, 2)

    def descripcion(self):
        return f"{self.nombre} ({type(self).__name__})"


class Comercial(Empleado):
    def __init__(self, nombre, salario, comision):
        super().__init__(nombre, salario)         # inicializa la parte heredada
        self.comision = comision

    def salario_mensual(self):                    # sobrescritura
        return round(super().salario_mensual() + self.comision, 2)


grace = Comercial("Grace", 36000, 400)
grace.salario_mensual()                           # 3400.0
grace.descripcion()                               # 'Grace (Comercial)': método heredado
isinstance(grace, Empleado)                       # True
issubclass(Comercial, Empleado)                   # True
```

Puntos clave:

- La clase base va entre paréntesis. Si no se indica ninguna, se hereda de `object`.
- `super()` da acceso a la implementación de la clase base. **Si defines `__init__` en la subclase, tienes que llamar a `super().__init__(...)`**: Python no lo hace por ti, a diferencia de Java.
- Sobrescribir es definir un método con el mismo nombre. No hay `@Override` ni `virtual`: todos los métodos son virtuales.
- Si la subclase no necesita atributos nuevos, no definas `__init__`: se hereda.

### Clases abstractas

Una clase abstracta define qué métodos deben tener sus subclases y no se puede instanciar. Se construye con el módulo `abc`.

```python
from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def area(self):
        """Devuelve el área de la figura."""

    def descripcion(self):                        # método concreto que usa el abstracto
        return f"{self.nombre} de área {self.area():.2f}"


class Cuadrado(Figura):
    def __init__(self, lado):
        super().__init__("Cuadrado")
        self.lado = lado

    def area(self):
        return self.lado ** 2


Figura("x")       # TypeError: Can't instantiate abstract class Figura
Cuadrado(2).descripcion()     # 'Cuadrado de área 4.00'
```

Una subclase que no implementa todos los métodos abstractos tampoco se puede instanciar. El error aparece al crear el objeto, no al definir la clase.

### Herencia múltiple

Python permite heredar de varias clases. El orden en que se buscan los métodos se llama MRO (*method resolution order*) y se consulta con `Clase.__mro__`.

```python
class Registrable:
    def registrar(self, mensaje):
        print(f"[{type(self).__name__}] {mensaje}")


class Serializable:
    def a_diccionario(self):
        return dict(self.__dict__)


class Pedido(Registrable, Serializable):
    def __init__(self, numero):
        self.numero = numero
```

El uso razonable es el de este ejemplo: clases pequeñas que aportan una capacidad concreta y no tienen estado propio, llamadas *mixins*. Las jerarquías en rombo con estado conviene evitarlas.

---

## 5.5 Polimorfismo y duck typing

### Polimorfismo por herencia

```python
plantilla = [Empleado("Ada", 52000), Comercial("Grace", 36000, 400)]

for persona in plantilla:
    print(persona.nombre, persona.salario_mensual())      # cada objeto usa su versión

coste = sum(persona.salario_mensual() for persona in plantilla)
```

### Duck typing

En Python el polimorfismo **no necesita herencia**. Lo que importa es que el objeto tenga el método que se le pide, no de qué clase sea: «si camina como un pato y grazna como un pato, es un pato».

```python
class Correo:
    def enviar(self, destinatario, mensaje):
        return f"Correo a {destinatario}: {mensaje}"


class Sms:
    def enviar(self, destinatario, mensaje):
        return f"SMS a {destinatario}: {mensaje[:160]}"


def avisar(canales, destinatario, mensaje):
    return [canal.enviar(destinatario, mensaje) for canal in canales]


avisar([Correo(), Sms()], "Ada", "Reunión a las 10")
```

`Correo` y `Sms` no comparten clase base ni interfaz. Basta con que tengan `enviar`. Es lo mismo que ya has usado sin saberlo: `len()` funciona con cualquier objeto que tenga `__len__`, y `for` con cualquiera que tenga `__iter__`.

Consecuencias prácticas:

- No compruebes tipos con `isinstance` para decidir qué hacer. Llama al método y deja que cada objeto responda.
- Una cadena de `if isinstance(...) elif isinstance(...)` suele indicar que falta un método polimórfico.
- Para probar una función puedes pasarle un objeto falso con los métodos necesarios, sin frameworks.

### Protocolos

Si quieres documentar y comprobar con herramientas qué métodos espera una función, `typing.Protocol` define una interfaz que se cumple **por estructura**, sin heredar de ella:

```python
from typing import Protocol


class Canal(Protocol):
    def enviar(self, destinatario: str, mensaje: str) -> str: ...


def avisar(canales: list[Canal], destinatario: str, mensaje: str) -> list[str]:
    return [canal.enviar(destinatario, mensaje) for canal in canales]
```

`Correo` y `Sms` cumplen el protocolo sin saber que existe. El editor y `mypy` lo comprueban; en ejecución no cambia nada.

### Clase abstracta o protocolo

| | Clase abstracta (`ABC`) | Protocolo |
| --- | --- | --- |
| La subclase debe heredar | Sí | No |
| Puede aportar código común | Sí | No es su propósito |
| El error aparece | Al instanciar | En el editor o con `mypy` |
| Úsalo cuando | Controlas la jerarquía y hay comportamiento compartido | Solo necesitas describir qué métodos esperas |

---

## 5.6 Encapsulación

### Convenciones de privacidad

Python no tiene `private`. La visibilidad se expresa con el nombre:

| Nombre | Significado |
| --- | --- |
| `saldo` | Público: forma parte de la interfaz de la clase |
| `_saldo` | Interno: «no lo toques desde fuera». Es una convención; el lenguaje no lo impide |
| `__saldo` | Python cambia el nombre a `_Clase__saldo` para evitar choques en subclases. No es seguridad y se usa poco |
| `__init__` | Método especial definido por el lenguaje. No inventes los tuyos |

La cultura del lenguaje es «somos adultos responsables»: el guion bajo avisa de que algo es un detalle interno y quien lo use lo hace por su cuenta y riesgo.

### Propiedades

En Java se escriben getters y setters por si en el futuro hace falta añadir lógica. En Python **se empieza con un atributo público** y, si un día hace falta lógica, se convierte en una propiedad sin cambiar el código que lo usa.

```python
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio                  # pasa por el setter

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

    @property
    def precio_con_iva(self):                 # propiedad calculada, solo lectura
        return round(self._precio * 1.21, 2)


teclado = Producto("Teclado", 45.0)
teclado.precio = 49.0                         # sintaxis de atributo; ejecuta el setter
print(teclado.precio_con_iva)                 # 59.29, sin paréntesis
teclado.precio = -1                           # ValueError
teclado.precio_con_iva = 10                   # AttributeError: no tiene setter
```

Usos de `@property`:

- **Validar** al asignar.
- **Calcular** un valor a partir de otros atributos, de modo que nunca quede desfasado.
- **Solo lectura:** una propiedad sin setter no se puede asignar.

No escribas `get_precio()` y `set_precio()`. Y no conviertas en propiedad lo que es costoso o tiene efectos secundarios: de un atributo se espera que sea inmediato.

### Proteger el estado interno

Encapsular es garantizar que el objeto está siempre en un estado válido, y eso incluye no entregar referencias a sus colecciones internas:

```python
class Cuenta:
    def __init__(self, titular):
        self.titular = titular
        self._saldo = 0.0
        self._movimientos = []

    @property
    def saldo(self):
        return self._saldo

    @property
    def movimientos(self):
        return tuple(self._movimientos)       # copia inmutable: desde fuera no se puede alterar

    def ingresar(self, importe):
        if importe <= 0:
            raise ValueError("El importe debe ser positivo")
        self._saldo += importe
        self._movimientos.append(importe)
```

El saldo solo cambia a través de `ingresar` y `retirar`, que aplican las reglas del negocio.

---

## 5.7 Buenas prácticas y Práctica 5

### Dataclasses

Para las clases cuyo trabajo principal es guardar datos, `@dataclass` genera `__init__`, `__repr__` y `__eq__` a partir de los campos anotados.

```python
from dataclasses import dataclass, field


@dataclass
class LineaPedido:
    producto: str
    unidades: int
    precio: float
    descuento: float = 0.0                    # los campos con valor por defecto van al final

    @property
    def importe(self) -> float:
        return round(self.unidades * self.precio * (1 - self.descuento / 100), 2)


linea = LineaPedido("Teclado", 2, 45.0)
print(linea)                                  # LineaPedido(producto='Teclado', unidades=2, ...)
linea == LineaPedido("Teclado", 2, 45.0)      # True
```

Opciones que conviene conocer:

```python
@dataclass(frozen=True)                       # inmutable y utilizable como clave
class Punto:
    x: float
    y: float


@dataclass(order=True)                        # genera <, <=, >, >= comparando campo a campo
class Version:
    mayor: int
    menor: int


@dataclass
class Pedido:
    numero: int
    lineas: list[LineaPedido] = field(default_factory=list)    # lista nueva por objeto
```

`field(default_factory=list)` es la forma correcta de dar un valor por defecto mutable: `lineas: list = []` produce un error precisamente para evitar la lista compartida.

Una dataclass es una clase normal: puede tener métodos, propiedades y herencia. Con `__post_init__` se añade validación tras el `__init__` generado.

### Composición frente a herencia

La herencia expresa **«es un»**; la composición, **«tiene un»**. Un `Comercial` es un `Empleado`. Un `Pedido` tiene líneas, no es una lista.

```python
class Pedido(list):                # MAL: hereda append, sort, pop, reverse...
    ...


class Pedido:                      # BIEN: contiene una lista y expone solo lo que tiene sentido
    def __init__(self, numero):
        self.numero = numero
        self._lineas = []

    def anadir(self, linea):
        self._lineas.append(linea)

    @property
    def total(self):
        return round(sum(linea.importe for linea in self._lineas), 2)

    def __len__(self):
        return len(self._lineas)
```

Regla práctica: **prefiere la composición**. Hereda solo cuando la subclase pueda sustituir a la base en cualquier sitio y además haya comportamiento que compartir. Las jerarquías de más de dos niveles son raras en Python.

### Principios de diseño

- **Responsabilidad única.** Una clase tiene un motivo para cambiar. `Pedido` calcula totales; no envía correos ni escribe ficheros.
- **Cohesión.** Los métodos usan los atributos de la clase. Un método que no usa `self` es una función.
- **Estado siempre válido.** Se valida en el constructor y en los métodos que modifican; el resto del código puede confiar.
- **Interfaz pequeña.** Lo que no hace falta desde fuera lleva guion bajo.
- **Depende de comportamientos, no de tipos.** Es lo que da el duck typing.
- **No te anticipes.** No crees una jerarquía para un único caso ni una clase abstracta con una sola subclase.

### Organización en módulos

No hay regla de una clase por fichero. Un módulo agrupa las clases y funciones que tratan de lo mismo:

```
biblioteca/
├── __init__.py
├── modelos.py        Material, Libro, Revista, Socio, Prestamo
├── servicios.py      Biblioteca: las operaciones
└── informes.py       funciones que generan texto
```

### Material del módulo

Los ejemplos de la carpeta [`ejemplos/`](ejemplos/) recorren el módulo:

| Fichero | Qué muestra |
| --- | --- |
| `01_clases_y_objetos.py` | Clase, `__init__`, `self`, identidad y atributos dinámicos |
| `02_atributos_y_metodos.py` | Atributos de clase, `@classmethod`, `@staticmethod` y métodos especiales |
| `03_herencia.py` | `super()`, sobrescritura, clase abstracta y mixins |
| `04_polimorfismo.py` | Polimorfismo por herencia, duck typing y `Protocol` |
| `05_encapsulacion.py` | Convenciones de nombres y `@property` |
| `06_dataclasses_y_composicion.py` | `@dataclass`, `field`, `frozen` y composición |
| `07_mirada_datos.py` | De objetos a filas con `asdict`, y una tabla mínima con métodos especiales |

- Ejercicios del módulo: [`ejercicios/README.md`](ejercicios/README.md)
- Práctica 5, modelo de una biblioteca: [`ejercicios/PRACTICA_5.md`](ejercicios/PRACTICA_5.md)

---

## Mirada de datos

### Objetos para las reglas, tablas para el análisis

Una clase garantiza que **cada** dato es válido y sabe comportarse: una `Venta` no puede tener unidades negativas y sabe calcular su importe. Una tabla responde preguntas sobre **todos** los datos a la vez: cuánto se vendió por región. Las aplicaciones reales usan las dos cosas, y el puente entre ellas es corto:

```python
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Venta:
    region: str
    unidades: int
    precio: float

    @property
    def importe(self) -> float:
        return round(self.unidades * self.precio, 2)
```

```python
>>> ventas = [Venta("Norte", 3, 19.9), Venta("Sur", 1, 250.0)]
>>> [asdict(venta) | {"importe": venta.importe} for venta in ventas]
[{'region': 'Norte', 'unidades': 3, 'precio': 19.9, 'importe': 59.7}, {'region': 'Sur', 'unidades': 1, 'precio': 250.0, 'importe': 250.0}]
```

Esa lista de diccionarios es justo lo que acepta `pd.DataFrame(...)`. En el proyecto del Módulo 8 harás este recorrido completo: objetos `Incidencia` con sus reglas y un módulo de análisis que los convierte en tabla.

### La sintaxis de pandas no es magia

Cuando en el Módulo 7 escribas `len(tabla)`, `tabla["importe"]`, `tabla.shape` o `tabla_a + tabla_b`, estarás usando lo que has aprendido aquí:

| Lo que escribes | Lo que hay detrás |
| --- | --- |
| `len(tabla)` | `__len__` |
| `tabla["importe"]` | `__getitem__` |
| `tabla.shape`, `tabla.columns` | Propiedades |
| `serie * 1.21`, `serie > 100` | `__mul__`, `__gt__` |
| `tabla` en el intérprete | `__repr__` |
| `pd.DataFrame.from_records(...)` | Un `@classmethod` como constructor alternativo |

Un `DataFrame` es un objeto con atributos, métodos y métodos especiales. El ejemplo `ejemplos/07_mirada_datos.py` construye una tabla mínima con cuatro de ellos.

---

## Errores típicos de quien viene de otro lenguaje

| Error | Qué pasa | Forma correcta |
| --- | --- | --- |
| Olvidar `self` en la definición del método | `TypeError: takes 0 positional arguments but 1 was given` | `def metodo(self):` |
| Escribir `salario` en lugar de `self.salario` | `NameError`, o se crea una variable local que se pierde | Siempre `self.` |
| No llamar a `super().__init__()` | `AttributeError`: faltan los atributos de la clase base | Llamarlo al principio del `__init__` de la subclase |
| Lista como atributo de clase | Todos los objetos comparten la lista | Crearla en `__init__` |
| `def __init__(self, items=[])` | Lista compartida entre objetos | `items=None` |
| `get_x()` y `set_x()` | Funciona, pero no es idiomático | Atributo público o `@property` |
| `objeto.metodo` sin paréntesis | Se obtiene el método, no su resultado | `objeto.metodo()` |
| Propiedad llamada con paréntesis | `TypeError: 'float' object is not callable` | `objeto.propiedad` |
| En el setter, `self.precio = valor` | Recursión infinita | `self._precio = valor` |
| Esperar que `==` compare los datos | Compara identidad | Definir `__eq__` o usar `@dataclass` |
| `print(objeto)` muestra `<... object at 0x...>` | Falta `__repr__` | Definirlo siempre |
| Sobrecargar `__init__` | La segunda definición sustituye a la primera | Valores por defecto y `@classmethod` |
| `if type(x) == Clase` | Falla con subclases | `isinstance(x, Clase)`, o mejor, polimorfismo |
| Heredar de `list` o `dict` para reutilizar | La clase expone métodos que rompen sus reglas | Composición |

## Para saber más

- Clases en el tutorial oficial: [docs.python.org/es/3/tutorial/classes.html](https://docs.python.org/es/3/tutorial/classes.html)
- Modelo de datos y métodos especiales: [docs.python.org/es/3/reference/datamodel.html](https://docs.python.org/es/3/reference/datamodel.html)
- `dataclasses`: [docs.python.org/es/3/library/dataclasses.html](https://docs.python.org/es/3/library/dataclasses.html)
- `abc`: [docs.python.org/es/3/library/abc.html](https://docs.python.org/es/3/library/abc.html)
