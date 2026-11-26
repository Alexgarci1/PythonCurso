from src.excepciones import ImporteInvalidoError


class Transaccion:
    """Clase base que representa un movimiento económico."""

    def __init__(self, fecha: str, concepto: str, importe: float, categoria: str = "Otros"):
        if importe <= 0:
            raise ImporteInvalidoError(f"El importe debe ser positivo: {importe}")
        self.fecha = fecha
        self.concepto = concepto.strip()
        self.importe = round(float(importe), 2)
        self.categoria = categoria

    @property
    def tipo(self) -> str:
        return "transaccion"

    def impacto_balance(self) -> float:
        return 0.0

    def a_diccionario(self) -> dict:
        return {
            "fecha": self.fecha,
            "concepto": self.concepto,
            "importe": self.importe,
            "tipo": self.tipo,
            "categoria": self.categoria,
        }

    def __str__(self) -> str:
        return f"[{self.fecha}] {self.concepto} ({self.categoria}): {self.importe:.2f} €"


class Ingreso(Transaccion):
    @property
    def tipo(self) -> str:
        return "ingreso"

    def impacto_balance(self) -> float:
        return self.importe


class Gasto(Transaccion):
    @property
    def tipo(self) -> str:
        return "gasto"

    def impacto_balance(self) -> float:
        return -self.importe


class Cartera:
    """Gestiona una colección de transacciones y calcula métricas básicas."""

    def __init__(self, titular: str = "Usuario"):
        self.titular = titular
        self.transacciones: list[Transaccion] = []

    def agregar(self, transaccion: Transaccion) -> None:
        self.transacciones.append(transaccion)

    def calcular_balance(self) -> float:
        return round(sum(t.impacto_balance() for t in self.transacciones), 2)

    def categorias_unicas(self) -> set[str]:
        return {t.categoria for t in self.transacciones}

    def __len__(self) -> int:
        return len(self.transacciones)