"""Módulo 2 - Práctica 2, parte B: calculadora de nómina."""

SEGURIDAD_SOCIAL = 6.35
PAGAS = 12

_TRAMOS_IRPF = (
    (12450, 0.19),
    (20200, 0.24),
    (35200, 0.30),
    (60000, 0.37),
    (None, 0.45),
)


def calcular_irpf(bruto_anual: float) -> float:
    """Calcula la retención anual de IRPF con una escala progresiva.

    Cada tramo se aplica solo a la parte del salario que cae dentro de él.

    >>> calcular_irpf(30000)
    7165.5
    """
    bruto_anual = max(bruto_anual, 0)
    retencion = 0
    limite_inferior = 0
    for limite_superior, tipo in _TRAMOS_IRPF:
        if limite_superior is None:
            importe_tramo = bruto_anual - limite_inferior
        else:
            importe_tramo = min(bruto_anual, limite_superior) - limite_inferior
        if importe_tramo <= 0:
            break
        retencion += importe_tramo * tipo
        if limite_superior is not None:
            limite_inferior = limite_superior
    return round(retencion, 2)


def calcular_seguridad_social(bruto_anual: float) -> float:
    """Calcula la cotización anual del trabajador a la Seguridad Social.

    >>> calcular_seguridad_social(30000)
    1905.0
    """
    return round(bruto_anual * SEGURIDAD_SOCIAL / 100, 2)


def calcular_neto_anual(bruto_anual: float) -> float:
    """Devuelve el salario neto anual: bruto menos IRPF y Seguridad Social.

    >>> calcular_neto_anual(30000)
    20929.5
    """
    return round(
        bruto_anual
        - calcular_irpf(bruto_anual)
        - calcular_seguridad_social(bruto_anual),
        2,
    )


def tipo_efectivo(bruto_anual: float) -> float:
    """Devuelve el porcentaje de IRPF sobre el bruto, con dos decimales.

    Si el bruto es cero o negativo devuelve 0.0.

    >>> tipo_efectivo(30000)
    23.89
    """
    if bruto_anual <= 0:
        return 0.0
    return round(calcular_irpf(bruto_anual) / bruto_anual * 100, 2)


def formatear_nomina(bruto_anual: float) -> str:
    """Devuelve el resumen de la nómina en cinco líneas alineadas.

    >>> print(formatear_nomina(30000))
    Bruto anual            30,000.00
    IRPF (23.89 %)         -7,165.50
    Seguridad Social       -1,905.00
    Neto anual             20,929.50
    Neto mensual            1,744.12
    """
    bruto = f"{bruto_anual:,.2f}"
    irpf = calcular_irpf(bruto_anual)
    etiqueta_irpf = f"IRPF ({tipo_efectivo(bruto_anual):.2f} %)"
    seguridad_social = calcular_seguridad_social(bruto_anual)
    neto = calcular_neto_anual(bruto_anual)
    neto_mensual = neto / PAGAS
    return "\n".join(
        (
            f"{'Bruto anual':<20}{bruto:>12}",
            f"{etiqueta_irpf:<20}{-irpf:>12,.2f}",
            f"{'Seguridad Social':<20}{-seguridad_social:>12,.2f}",
            f"{'Neto anual':<20}{neto:>12,.2f}",
            f"{'Neto mensual':<20}{neto_mensual:>12,.2f}",
        )
    )


def main() -> None:
    """Pide el salario bruto anual y muestra la nómina."""
    try:
        bruto_anual = float(input("Introduce el salario bruto anual: "))
    except ValueError:
        print("Importe no válido")
        return
    if not bruto_anual > 0:
        print("Importe no válido")
        return
    print(formatear_nomina(bruto_anual))


if __name__ == "__main__":
    main()
