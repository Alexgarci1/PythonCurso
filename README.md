# Programación en Python - Nivel Inicial

Repositorio de trabajo del curso. Aquí están los apuntes, los ejemplos que se programan en clase, los ejercicios y las prácticas de cada módulo.

Los contenidos también están en HTML: abre [`docs/index.html`](docs/index.html) en el navegador.

## Puesta en marcha

Necesitas Python 3.12 o superior, Visual Studio Code y Git.

```bash
git clone https://github.com/yustech/Curso-Python-IA.git
cd Curso-Python-IA
python -m venv .venv
```

Activa el entorno virtual:

| Sistema | Comando |
| --- | --- |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| macOS o Linux | `source .venv/bin/activate` |

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Estructura

Cada módulo tiene la misma organización:

```
modulo_XX_nombre/
├── README.md      Apuntes del módulo
├── ejemplos/      Código que se explica en clase, listo para ejecutar
├── ejercicios/    Enunciados y ficheros que tienes que completar
└── tests/         Tests que comprueban tus ejercicios y tu práctica
```

## Cómo trabajar los ejercicios

1. Lee el enunciado en `ejercicios/README.md`.
2. Completa el fichero del ejercicio. Sustituye cada `raise NotImplementedError` por tu código.
3. Ejecuta los tests del módulo:

```bash
pytest modulo_01_introduccion
```

4. Un ejercicio está terminado cuando todos sus tests pasan. Para ejecutar solo un fichero de tests o ver más detalle:

```bash
pytest modulo_01_introduccion/tests/test_m1_ejercicios.py -v
```

Al empezar, todos los tests fallan. Es lo esperado: tu trabajo es ponerlos en verde.

## Módulos

| Módulo | Título | Horas |
| --- | --- | --- |
| 1 | [Introducción a Python](modulo_01_introduccion/README.md) | 4 |
| 2 | [Variables, operadores y estructuras de control](modulo_02_variables_control/README.md) | 8 |
| 3 | [Funciones y módulos](modulo_03_funciones_modulos/README.md) | 6 |
| 4 | [Colecciones y manejo de datos](modulo_04_colecciones/README.md) | 8 |
| 5 | [Programación Orientada a Objetos](modulo_05_poo/README.md) | 8 |
| 6 | [Archivos y gestión de excepciones](modulo_06_archivos_excepciones/README.md) | 4 |
| 7 | Proyecto práctico y evaluación | 4 |
