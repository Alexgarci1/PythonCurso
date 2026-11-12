"""Tests de la práctica 2: adivina el número y calculadora de nómina."""

import pytest

import m2_practica_adivina as adivina
import m2_practica_nomina as nomina


def simular_teclado(monkeypatch, respuestas):
    """Hace que input() devuelva, una a una, las respuestas indicadas."""
    pendientes = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda *args: next(pendientes))


# ------------------------------------------------------------------- Parte A
def test_a_constantes():
    assert (adivina.MINIMO, adivina.MAXIMO, adivina.MAX_INTENTOS) == (1, 100, 7)


def test_a_evaluar_intento():
    assert adivina.evaluar_intento(50, 50) == "acierto"
    assert adivina.evaluar_intento(50, 30) == "mayor"
    assert adivina.evaluar_intento(50, 80) == "menor"


@pytest.mark.parametrize("texto", ["1", "50", "100", " 42 "])
def test_a_intento_valido(texto):
    assert adivina.es_intento_valido(texto) is True


@pytest.mark.parametrize("texto", ["0", "101", "abc", "", "  ", "4.5", "-3"])
def test_a_intento_no_valido(texto):
    assert adivina.es_intento_valido(texto) is False


def test_a_acierta_a_la_primera(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["42"])
    assert adivina.jugar(42) is True
    assert "¡Correcto! Lo has adivinado en 1 intentos." in capsys.readouterr().out


def test_a_da_pistas_y_cuenta_los_intentos(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["50", "25", "42"])
    assert adivina.jugar(42) is True
    salida = capsys.readouterr().out
    assert "El número secreto es menor." in salida
    assert "El número secreto es mayor." in salida
    assert "¡Correcto! Lo has adivinado en 3 intentos." in salida


def test_a_la_entrada_no_valida_no_consume_intento(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["hola", "500", "10", "42"])
    assert adivina.jugar(42, max_intentos=2) is True
    salida = capsys.readouterr().out
    assert salida.count("Escribe un número entre 1 y 100.") == 2
    assert "Lo has adivinado en 2 intentos." in salida


def test_a_agota_los_intentos(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["1", "2", "3"])
    assert adivina.jugar(42, max_intentos=3) is False
    assert "Has agotado los intentos. El número era 42." in capsys.readouterr().out


def test_a_usa_siete_intentos_por_defecto(monkeypatch):
    simular_teclado(monkeypatch, ["1", "2", "3", "4", "5", "6", "42"])
    assert adivina.jugar(42) is True
    simular_teclado(monkeypatch, ["1", "2", "3", "4", "5", "6", "7"])
    assert adivina.jugar(42) is False


def test_a_main_genera_un_secreto_en_el_rango(monkeypatch):
    secretos = []
    monkeypatch.setattr(adivina, "jugar", lambda secreto, *args, **kwargs: secretos.append(secreto))
    for _ in range(50):
        adivina.main()
    assert all(1 <= secreto <= 100 for secreto in secretos)
    assert len(set(secretos)) > 1, "El secreto debe generarse al azar"


# ------------------------------------------------------------------- Parte B
def test_b_constantes():
    assert nomina.SEGURIDAD_SOCIAL == 6.35
    assert nomina.PAGAS == 12


@pytest.mark.parametrize(
    "bruto, esperado",
    [
        (0, 0.0),
        (10000, 1900.0),
        (12450, 2365.5),
        (20200, 4225.5),
        (30000, 7165.5),
        (35200, 8725.5),
        (60000, 17901.5),
        (70000, 22401.5),
    ],
)
def test_b_irpf_progresivo(bruto, esperado):
    assert nomina.calcular_irpf(bruto) == pytest.approx(esperado)


def test_b_seguridad_social():
    assert nomina.calcular_seguridad_social(30000) == pytest.approx(1905.0)
    assert nomina.calcular_seguridad_social(18500.5) == pytest.approx(1174.78)


def test_b_neto_anual():
    assert nomina.calcular_neto_anual(30000) == pytest.approx(20929.5)
    assert nomina.calcular_neto_anual(12450) == pytest.approx(9293.92)


def test_b_tipo_efectivo():
    assert nomina.tipo_efectivo(30000) == pytest.approx(23.89)
    assert nomina.tipo_efectivo(10000) == pytest.approx(19.0)
    assert nomina.tipo_efectivo(0) == 0.0
    assert nomina.tipo_efectivo(-500) == 0.0


def test_b_formatear_nomina():
    esperado = (
        "Bruto anual            30,000.00\n"
        "IRPF (23.89 %)         -7,165.50\n"
        "Seguridad Social       -1,905.00\n"
        "Neto anual             20,929.50\n"
        "Neto mensual            1,744.12"
    )
    assert nomina.formatear_nomina(30000) == esperado


def test_b_formatear_nomina_todas_las_lineas_miden_lo_mismo():
    lineas = nomina.formatear_nomina(85000).split("\n")
    assert len(lineas) == 5
    assert {len(linea) for linea in lineas} == {32}


def test_b_main_muestra_la_nomina(monkeypatch, capsys):
    simular_teclado(monkeypatch, ["30000"])
    nomina.main()
    assert "Neto mensual            1,744.12" in capsys.readouterr().out


@pytest.mark.parametrize("entrada", ["abc", "", "-100"])
def test_b_main_importe_no_valido(monkeypatch, capsys, entrada):
    simular_teclado(monkeypatch, [entrada])
    nomina.main()
    assert "Importe no válido" in capsys.readouterr().out
