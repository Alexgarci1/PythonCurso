# Módulo 8. Proyecto práctico y evaluación (4 horas)

En este módulo desarrollas de forma individual una aplicación completa que reúne las dos caras del curso. Por un lado, Python como lenguaje de aplicaciones: funciones, colecciones, clases, ficheros y excepciones. Por otro, Python como lenguaje de datos: un módulo de análisis con pandas sobre la información que gestiona la propia aplicación. **El proyecto es la evaluación práctica del curso.**

| Unidad | Contenido | Tiempo |
| --- | --- | --- |
| 8.1 | Presentación del proyecto y diseño de la solución | 0,5 h |
| 8.2 | Desarrollo de la aplicación | 3 h |
| 8.3 | Evaluación práctica y cierre del curso | 0,5 h |

---

## 8.1 Presentación del proyecto y diseño de la solución

### El encargo

El equipo de soporte de un cliente apunta las incidencias en una hoja de cálculo compartida. Se pierden, nadie sabe cuáles están pendientes ni quién las lleva. Te piden un **gestor de incidencias** de consola que permita:

- Dar de alta una incidencia con título, solicitante y prioridad.
- Listar todas las incidencias y listar las pendientes en el orden en que hay que atenderlas.
- Buscar incidencias por texto.
- Cambiar el estado de una incidencia respetando un flujo de trabajo.
- Asignar una incidencia a un técnico.
- Obtener un informe de situación.
- Conservar los datos entre ejecuciones en un fichero CSV.
- **Analizar el servicio** con pandas: tiempos de resolución, carga por técnico y reparto por estado y prioridad.

### Reglas del dominio

**Prioridades**, de menor a mayor: `baja`, `media`, `alta`, `critica`.

**Estados** y cambios permitidos:

```
              ┌───────────────────────────────┐
              │                               ▼
abierta ◄──► en_curso ◄──► resuelta ──► cerrada
```

| Desde | Se puede pasar a |
| --- | --- |
| `abierta` | `en_curso`, `cerrada` |
| `en_curso` | `abierta`, `resuelta` |
| `resuelta` | `en_curso`, `cerrada` |
| `cerrada` | A ninguno |

- Una incidencia está **pendiente** si está `abierta` o `en_curso`.
- Al pasar a `cerrada` se anota la fecha de cierre.
- Al asignar a un técnico una incidencia `abierta`, pasa a `en_curso`.
- El título y el solicitante son obligatorios.
- Los identificadores son enteros consecutivos que empiezan en 1.

### Arquitectura

La aplicación se organiza en capas, igual que la Práctica 5 y la Práctica 6. Cada capa solo conoce a las que tiene debajo.

```
ejercicios/
├── m8_proyecto_app.py        Menú de consola. ÚNICO sitio con input, print y captura de errores
└── incidencias/              Paquete con la lógica
    ├── __init__.py
    ├── excepciones.py        Errores propios de la aplicación
    ├── modelos.py            Incidencia: los datos y sus reglas
    ├── gestor.py             GestorIncidencias: operaciones sobre el conjunto
    ├── almacen.py            Guardar y cargar en CSV
    ├── informes.py           Textos para mostrar
    └── analisis.py           Análisis del conjunto con pandas
```

| Capa | Responsabilidad | Qué no hace |
| --- | --- | --- |
| `modelos.py` | Una incidencia es siempre válida y solo cambia de estado según las reglas | No sabe que existen ficheros ni pantalla |
| `gestor.py` | Crear, buscar, filtrar, ordenar y contar | No lee ni escribe ficheros; no usa `print` ni `input` |
| `almacen.py` | Convertir entre incidencias y CSV | No decide cuándo se guarda |
| `informes.py` | Construir textos y devolverlos | No usa `print` |
| `analisis.py` | Ver las incidencias como una tabla y calcular indicadores con pandas | No modifica las incidencias ni el gestor; no usa `print` |
| `m8_proyecto_app.py` | Hablar con el usuario y capturar los errores | No contiene reglas de negocio |

Esta separación es la que permite probar toda la lógica con tests automáticos sin teclear nada, y es uno de los criterios de evaluación.

### Qué se te entrega

- La estructura de ficheros con las **firmas y los docstrings** de todas las clases y funciones de la lógica. Los docstrings son la especificación: léelos enteros.
- Las constantes `ESTADOS`, `PRIORIDADES`, `TRANSICIONES`, `CAMPOS`, `ANCHO` y `MENU`.
- Los tests de aceptación en `tests/test_m8_proyecto.py` y `tests/test_m8_analisis.py`.
- Un fichero de ejemplo, `datos/incidencias_ejemplo.csv`, para probar a mano.

Lo que **no** se entrega y diseñas tú: las excepciones, los campos de la dataclass, el contenido del `__init__.py` del paquete y toda la organización interna del menú.

---

## 8.2 Desarrollo de la aplicación

### Plan de trabajo

Tres horas. Trabaja por hitos y **haz un commit al terminar cada uno**. Un proyecto con los hitos 1 a 4 completos y bien hechos puntúa más que uno con todo a medias. Los hitos 5 y 6 son independientes entre sí: si lo tuyo son los datos, puedes hacer el análisis antes que el menú.

| Hito | Fichero | Qué construyes | Tiempo orientativo | Tests |
| --- | --- | --- | --- | --- |
| 1 | `excepciones.py` y `modelos.py` | Las excepciones y la clase `Incidencia` | 35 min | `-k "excepciones or incidencia"` |
| 2 | `gestor.py` | `GestorIncidencias` | 35 min | `-k gestor` |
| 3 | `almacen.py` | `guardar` y `cargar` | 20 min | `-k almacen` |
| 4 | `informes.py` | `linea`, `listado` y `resumen` | 25 min | `-k informes` |
| 5 | `m8_proyecto_app.py` | El menú | 30 min | `-k app` |
| 6 | `analisis.py` | El análisis con pandas | 25 min | `-k analisis` |
| 7 | Todo | Revisión, limpieza y entrega | 10 min | Todos |

```bash
pytest modulo_08_proyecto -v                          # todos
pytest modulo_08_proyecto -v -k gestor                # un hito
pytest modulo_08_proyecto -x                          # se detiene en el primer fallo
```

Hasta que no definas las cinco excepciones, `pytest` no puede importar el paquete y muestra un único error de importación. Es lo esperado: empieza por ahí.

### Hito 1. Excepciones y modelo

`excepciones.py`: la jerarquía está descrita en el docstring del fichero. Todas heredan de `ErrorDeIncidencias`, lo que permite al menú capturar cualquier error de la aplicación con un solo `except`.

`modelos.py`: `Incidencia` es una dataclass.

- Declara los ocho campos en el orden que indica el docstring.
- `__post_init__` limpia y valida. Una incidencia no puede existir con datos incorrectos.
- `cambiar_estado` consulta `TRANSICIONES`. No escribas una cadena de `if`.
- `a_fila` y `desde_fila` convierten entre el objeto y el diccionario de cadenas que se escribe y se lee del CSV. Son inversas: `Incidencia.desde_fila(i.a_fila()) == i`.

### Hito 2. Gestor

`GestorIncidencias` guarda las incidencias en un diccionario interno por identificador. Recuerda de la Práctica 5: el gestor **delega** en la incidencia. Para cambiar un estado llama a `incidencia.cambiar_estado(...)`; no modifica `incidencia.estado` por su cuenta.

Los métodos que necesitan la fecha actual reciben un parámetro `hoy` opcional, por la razón de siempre: los tests pasan una fecha fija.

`pendientes()` devuelve la cola de trabajo: primero las de mayor prioridad y, a igual prioridad, las más antiguas. Es una ordenación por varios criterios como las del Módulo 4. La posición de cada prioridad en la tupla `PRIORIDADES` te da su peso.

### Hito 3. Almacén

Lo que hiciste en la Práctica 6, en pequeño:

- `guardar` usa `csv.DictWriter` con `CAMPOS` y `a_fila()`.
- `cargar` usa `csv.DictReader` y `desde_fila()`.
- Si el fichero no existe, `cargar` devuelve una lista vacía: es la primera ejecución, no un error.
- Si una fila no vale, `cargar` lanza `ErrorDeAlmacen` indicando la línea. Aquí, a diferencia del importador, un fichero corrupto **sí** detiene la carga: son los datos propios de la aplicación y no se puede seguir con la mitad.

### Hito 4. Informes

`linea` y `listado` producen la tabla:

```
  ID  PRIORIDAD ESTADO    ASIGNADA A  TÍTULO
------------------------------------------------------------------------------
   4  critica   en_curso  Marta       Caída del servidor de ficheros
   6  alta      en_curso  Pablo       VPN lenta desde casa
   5  media     abierta   -           Alta de usuario nuevo
```

`resumen(gestor, hoy)` produce el informe. Con `datos/incidencias_ejemplo.csv` y la fecha 27/11/2026:

```
==============================================================================
                            INFORME DE INCIDENCIAS
==============================================================================
Fecha del informe: 2026-11-27
Total de incidencias: 8

Por estado
  abierta        3
  en_curso       2
  resuelta       1
  cerrada        2

Pendientes por prioridad
  critica        1
  alta           1
  media          2
  baja           1

Pendiente más antigua: n.º 3, 24 días
==============================================================================
```

Formato:

- Ancho de 78 caracteres, en la constante `ANCHO`. El título va centrado en ese ancho.
- «Por estado» muestra **los cuatro** estados en el orden de `ESTADOS`, aunque valgan cero.
- «Pendientes por prioridad» cuenta solo las pendientes y muestra **las cuatro** prioridades de mayor a menor.
- En las dos listas: dos espacios, el nombre en 12 caracteres a la izquierda y la cantidad en 4 a la derecha.
- La pendiente más antigua es la que más días lleva abierta; a igualdad de días, la de menor identificador. Sin pendientes, la línea es `Pendiente más antigua: ninguna`.
- Sin salto de línea al final. Los tests ignoran los espacios del final de cada línea.

### Hito 5. Menú

`main(ruta)` en `m8_proyecto_app.py`. Su docstring describe el contrato exacto: qué pide cada opción y en qué orden, y qué imprime cuando algo falla. Respétalo, porque los tests simulan a un usuario tecleando.

Dentro de ese contrato, la organización es tuya. Recomendaciones:

- Una función pequeña por opción del menú.
- Un diccionario que asocie cada opción con su función, en lugar de una cadena de `if`/`elif`. Las funciones son objetos: Módulo 3.
- **Un único `try`/`except ErrorDeIncidencias`** alrededor de la ejecución de la opción elegida. Ninguna opción necesita su propio `try`.
- Los datos se guardan al salir con la opción 0.

Ejemplo de sesión:

```
GESTOR DE INCIDENCIAS
1. Alta de incidencia
...
0. Guardar y salir

Opción: 1
Título: No funciona el correo
Solicitante: Ada
Prioridad (baja, media, alta, critica) [media]: alta
Creada la incidencia 1.

Opción: 5
Número de incidencia: 1
Nuevo estado (abierta, en_curso, resuelta, cerrada): resuelta
Error: No se puede pasar de abierta a resuelta

Opción: 9
Opción no válida.

Opción: 0
Datos guardados. Hasta luego.
```

Para probar a mano con datos:

```bash
cd modulo_08_proyecto/ejercicios
cp ../datos/incidencias_ejemplo.csv incidencias.csv      # en Windows: copy
python m8_proyecto_app.py
```

### Hito 6. Análisis con pandas

Hasta aquí has tratado las incidencias de una en una, como objetos. `analisis.py` las mira todas a la vez, como una tabla, igual que en el Módulo 7. Son cinco funciones cortas; ninguna necesita un bucle.

| Función | Qué devuelve | Herramienta del Módulo 7 |
| --- | --- | --- |
| `a_tabla(incidencias)` | Un `DataFrame` con una fila por incidencia y las fechas como fechas | `pd.DataFrame`, `astype`, `pd.to_datetime` |
| `dias_de_resolucion(tabla)` | Una `Series` con los días que tardó en cerrarse cada incidencia cerrada | `dropna`, resta de fechas y `.dt.days` |
| `tabla_estado_prioridad(tabla)` | Cuántas incidencias hay de cada estado y prioridad | `pd.crosstab` y `reindex` |
| `resumen_por_tecnico(tabla)` | Asignadas, pendientes y cerradas por técnico | `groupby` con `agg` y `sort_values` |
| `indicadores(tabla, hoy)` | Un diccionario con las cifras principales | Máscaras booleanas, `mean` y `round` |

`a_tabla` es el puente entre los dos mundos: cada incidencia ya sabe convertirse en una fila con `a_fila()`. Con `datos/incidencias_ejemplo.csv` y la fecha 27/11/2026, `indicadores` devuelve:

```python
{'total': 8, 'pendientes': 5, 'porcentaje_pendientes': 62.5, 'sin_asignar': 3,
 'dias_medios_resolucion': 2.0, 'antiguedad_maxima': 24}
```

Para probarlo a mano desde `ejercicios/`:

```python
>>> from incidencias import almacen, analisis
>>> tabla = analisis.a_tabla(almacen.cargar("../datos/incidencias_ejemplo.csv"))
>>> analisis.tabla_estado_prioridad(tabla)
>>> analisis.resumen_por_tecnico(tabla)
```

Cuidado con los tipos al devolver cifras: los tests esperan `int` y `float` de Python, no tipos de NumPy, y las combinaciones sin incidencias valen 0, no un valor ausente.

### Si te sobra tiempo

Las ampliaciones suben nota solo si lo anterior está completo y limpio. Elige una y termínala.

1. **Registro de operaciones:** un `logger.info` por cada alta, cambio de estado y asignación, con salida a `incidencias.log`.
2. **Exportar pendientes:** una opción de menú que escribe las pendientes en un CSV aparte.
3. **Filtro combinado:** una opción que pregunta estado, prioridad y técnico, y aplica los que no se dejen en blanco.
4. **Análisis en el menú:** una opción nueva que muestre los indicadores y la tabla por técnico de `analisis.py`, o un gráfico de barras de pendientes por prioridad guardado en PNG.
5. **Comentarios:** cada incidencia admite una lista de comentarios con fecha. Decide cómo guardarlos.

---

## 8.3 Evaluación práctica y cierre del curso

### Entrega

Antes de la hora límite que indique el profesor:

1. Ejecuta `pytest modulo_08_proyecto` y anota cuántos tests pasan.
2. Comprueba que la aplicación arranca: `python m8_proyecto_app.py`.
3. Completa el fichero `ejercicios/ENTREGA.md`.
4. Haz commit y sube tu rama o tu *fork* según las instrucciones del profesor.

No se entrega nada que no esté en el repositorio a la hora límite. Un commit por hito protege tu trabajo: si el último hito queda a medias, vuelve al commit anterior.

### Rúbrica

El proyecto se puntúa sobre 100.

| Criterio | Puntos | Qué se mira |
| --- | --- | --- |
| Funcionalidad | 40 | Proporción de tests de aceptación superados |
| Aplicación de consola | 5 | El menú funciona de principio a fin, no termina con una traza ante entradas incorrectas y los datos se conservan entre ejecuciones |
| Diseño orientado a objetos | 15 | Dataclass bien definida, estado siempre válido, el gestor delega en la incidencia, composición, propiedades donde procede |
| Colecciones y estilo Python | 10 | Comprensiones, `sorted` con `key`, diccionarios para contar y agrupar, sin bucles con índices |
| Ficheros y excepciones | 10 | `with`, `encoding` y `newline`; jerarquía propia; `try` cortos; captura solo en el menú; `raise ... from` |
| Análisis de datos | 10 | Operaciones vectorizadas de pandas en lugar de bucles sobre las filas, tipos correctos (fechas como fechas, enteros como enteros) y `groupby`, `crosstab` y máscaras donde procede |
| Calidad y entrega | 10 | Nombres claros, funciones cortas, sin código muerto ni duplicado, commits por hito y `ENTREGA.md` completo |

Niveles orientativos:

| Puntos | Nivel |
| --- | --- |
| 90 a 100 | Excelente: todo funciona, el diseño es limpio y hay alguna ampliación terminada |
| 70 a 89 | Notable: funciona completo con detalles de estilo mejorables |
| 50 a 69 | Aprobado: la lógica de los hitos 1 a 3 funciona; faltan informes, menú o análisis |
| Menos de 50 | No superado: la lógica central no funciona |

Lo que resta aunque los tests pasen: validaciones o reglas de negocio dentro del menú, `print` o `input` en el paquete `incidencias`, `except Exception` o `except:` a secas, código copiado y pegado entre funciones, ficheros abiertos sin `with`, y recorrer un `DataFrame` fila a fila con `for` o `iterrows` para lo que resuelve una operación de columna.

El proyecto es individual. Puedes consultar tus apuntes, tus prácticas y la documentación oficial.

### Qué te llevas del curso

| Módulo | Dónde aparece en el proyecto |
| --- | --- |
| 1. Introducción | Entorno virtual, dependencias, `pytest`, Git y un commit por hito |
| 2. Variables y control | Validaciones, bucle del menú y formato de salida |
| 3. Funciones y módulos | Un paquete con seis módulos, parámetros solo por nombre y funciones como valores |
| 4. Colecciones | Diccionario de incidencias, filtros, ordenación por varios criterios y conteos |
| 5. POO | Dataclass con reglas, propiedades, `@classmethod` como constructor alternativo y composición |
| 6. Archivos y excepciones | CSV, jerarquía de excepciones, captura en una sola capa y logging |
| 7. Ciencia de datos | `DataFrame` a partir de los objetos, fechas, `groupby`, tablas cruzadas e indicadores |

### Para seguir

- **Calidad de código:** `ruff` para formato y análisis estático, `mypy` para comprobar las anotaciones de tipo.
- **Tests:** fixtures y parametrización de `pytest`, que ya has visto en los tests del curso, y cobertura con `pytest-cov`.
- **Proyectos:** `pyproject.toml` y gestión de dependencias con `uv` o `pip-tools`.
- **Datos:** `sqlite3`, de la librería estándar, y SQLAlchemy para persistencia; scikit-learn para modelos sobre las tablas que ya sabes preparar con pandas; Polars y DuckDB cuando los datos no caben cómodamente en memoria.
- **Web y API:** `requests` para consumir servicios y FastAPI para construirlos.
- **Lenguaje:** generadores, decoradores, gestores de contexto propios y `asyncio`.

El siguiente curso del itinerario, sobre IA generativa, agentes y LLM, parte de lo que has aprendido aquí: se trabaja en Python con paquetes, clases, JSON, ficheros, excepciones, cuadernos y tablas de datos desde el primer día.
