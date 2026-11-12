"""Configuración común de los tests del curso.

Por defecto los tests importan el código de la carpeta ``ejercicios`` de cada
módulo, es decir, tu trabajo. Si existe la variable de entorno
``CURSO_SOLUCIONES`` (uso del profesor), se importan las soluciones de esa
carpeta en su lugar.
"""

import os
import sys
from pathlib import Path

RAIZ = Path(__file__).parent
CARPETA_SOLUCIONES = os.environ.get("CURSO_SOLUCIONES")

for modulo in sorted(RAIZ.glob("modulo_*")):
    if CARPETA_SOLUCIONES:
        origen = Path(CARPETA_SOLUCIONES).resolve() / modulo.name / "soluciones"
    else:
        origen = modulo / "ejercicios"
    if origen.is_dir():
        sys.path.insert(0, str(origen))
