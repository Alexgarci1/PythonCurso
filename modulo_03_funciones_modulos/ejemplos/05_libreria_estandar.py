"""Módulo 3 - Ejemplo 5: un paseo por la librería estándar."""

import math
import random
from collections import Counter, defaultdict, namedtuple
from datetime import date, datetime, timedelta
from pathlib import Path


def main():
    # --- math
    print(math.sqrt(16), math.hypot(3, 4), math.ceil(4.1), math.floor(4.9))
    print(math.isclose(0.1 + 0.2, 0.3))

    # --- random: con semilla, el resultado se repite en cada ejecución
    generador = random.Random(42)
    print([generador.randint(1, 6) for _ in range(5)])
    print(generador.choice(["rojo", "verde", "azul"]))
    print(generador.sample(range(1, 50), 6))

    # --- datetime
    inicio = date(2026, 11, 19)
    fin = date(2026, 11, 27)
    print("Días de curso en el calendario:", (fin - inicio).days + 1)
    print(inicio.strftime("%d/%m/%Y"), "| día de la semana:", inicio.weekday())
    print(date.fromisoformat("2026-12-02") - timedelta(days=7))
    print(datetime.strptime("19/11/2026 08:00", "%d/%m/%Y %H:%M"))

    # --- pathlib
    ruta = Path("datos") / "ventas" / "enero.csv"
    print(ruta.name, ruta.stem, ruta.suffix, ruta.parent)
    aqui = Path(__file__).parent
    print(sorted(fichero.name for fichero in aqui.glob("*.py")))

    # --- collections
    print(Counter("mississippi").most_common(2))

    por_inicial = defaultdict(list)
    for nombre in ["Ada", "Alan", "Grace", "Guido", "Linus"]:
        por_inicial[nombre[0]].append(nombre)
    print(dict(por_inicial))

    Punto = namedtuple("Punto", ["x", "y"])
    p = Punto(3, 4)
    print(p, p.x, math.hypot(p.x, p.y))


if __name__ == "__main__":
    main()
