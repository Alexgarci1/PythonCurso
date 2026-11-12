"""Tests de la práctica 4: análisis de ventas."""

import copy

import pytest

import m4_practica_ventas as practica
from m4_datos_ventas import VENTAS

INFORME = """\
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
============================================"""

MINI = [
    {"fecha": "2026-01-10", "vendedor": "Zoe", "region": "Este", "producto": "B", "categoria": "X", "unidades": 2, "precio": 10.0},
    {"fecha": "2026-01-20", "vendedor": "Ana", "region": "Oeste", "producto": "A", "categoria": "X", "unidades": 2, "precio": 10.0},
    {"fecha": "2026-01-30", "vendedor": "Zoe", "region": "Este", "producto": "C", "categoria": "Y", "unidades": 1, "precio": 0.1},
]


@pytest.fixture
def ventas():
    return copy.deepcopy(VENTAS)


@pytest.fixture(autouse=True)
def _las_ventas_no_cambian(ventas):
    yield
    assert ventas == VENTAS, "La función ha modificado la lista de ventas"


def _lineas(texto):
    return [linea.rstrip() for linea in texto.split("\n")]


def test_importe():
    assert practica.importe({"unidades": 3, "precio": 19.9}) == 59.7
    assert practica.importe({"unidades": 0, "precio": 950.0}) == 0
    assert practica.importe(VENTAS[0]) == 1900.0


def test_total_ventas(ventas):
    assert practica.total_ventas(ventas) == 21686.8
    assert practica.total_ventas(ventas[:3]) == 2666.0
    assert practica.total_ventas([]) == 0


def test_total_ventas_reutiliza_importe(monkeypatch, ventas):
    monkeypatch.setattr(practica, "importe", lambda venta: 1)
    assert practica.total_ventas(ventas) == 20


def test_filtrar_sin_criterios(ventas):
    assert practica.filtrar_ventas(ventas) == VENTAS
    assert practica.filtrar_ventas([]) == []


@pytest.mark.parametrize(
    "criterios, cantidad, total",
    [
        ({"region": "Norte"}, 7, 12351.3),
        ({"region": "Sur"}, 8, 6062.0),
        ({"categoria": "Software"}, 5, 4135.0),
        ({"vendedor": "Linus"}, 5, 4387.0),
        ({"region": "Sur", "categoria": "Periféricos"}, 4, 1207.0),
        ({"vendedor": "Ada", "region": "Centro"}, 1, 1134.0),
        ({"desde": "2026-10-16"}, 9, 9235.3),
        ({"hasta": "2026-10-05"}, 5, 4271.0),
        ({"desde": "2026-10-05", "hasta": "2026-10-09"}, 4, 5908.0),
        ({"desde": "2026-10-09", "hasta": "2026-10-09"}, 1, 3200.0),
        ({"region": "Sur", "desde": "2026-10-16"}, 4, 3745.0),
        ({"region": "Este"}, 0, 0),
        ({"desde": "2026-11-01"}, 0, 0),
    ],
)
def test_filtrar_ventas(ventas, criterios, cantidad, total):
    resultado = practica.filtrar_ventas(ventas, **criterios)
    assert len(resultado) == cantidad
    assert round(sum(v["unidades"] * v["precio"] for v in resultado), 2) == total


def test_filtrar_criterios_solo_por_nombre(ventas):
    with pytest.raises(TypeError):
        practica.filtrar_ventas(ventas, "Norte")


def test_filtrar_devuelve_lista_nueva(ventas):
    assert practica.filtrar_ventas(ventas) is not ventas


def test_importe_por(ventas):
    assert practica.importe_por(ventas, "region") == {
        "Norte": 12351.3,
        "Sur": 6062.0,
        "Centro": 3273.5,
    }
    assert practica.importe_por(ventas, "categoria") == {
        "Equipos": 14000.0,
        "Periféricos": 3551.8,
        "Software": 4135.0,
    }
    assert practica.importe_por(ventas, "vendedor")["Grace"] == 5339.5
    assert practica.importe_por([], "region") == {}


def test_importe_por_redondea():
    assert practica.importe_por(MINI * 3, "categoria") == {"X": 120.0, "Y": 0.3}


def test_unidades_por_producto(ventas):
    assert practica.unidades_por_producto(ventas) == {
        "Portátil": 8,
        "Ratón": 22,
        "Monitor": 11,
        "Teclado": 23,
        "Licencia ofimática": 30,
        "Servidor": 2,
        "Antivirus": 70,
    }
    assert practica.unidades_por_producto([]) == {}


def test_ranking(ventas):
    assert practica.ranking(ventas, "vendedor") == [
        ("Ada", 7435.3),
        ("Grace", 5339.5),
        ("Alan", 4525.0),
    ]
    assert practica.ranking(ventas, "region", 1) == [("Norte", 12351.3)]
    assert practica.ranking(ventas, "producto", 2) == [("Portátil", 7600.0), ("Servidor", 6400.0)]
    assert len(practica.ranking(ventas, "vendedor", 10)) == 4
    assert practica.ranking([], "vendedor") == []


def test_ranking_desempate_alfabetico():
    assert practica.ranking(MINI, "region") == [("Este", 20.1), ("Oeste", 20.0)]
    assert practica.ranking(MINI, "producto") == [("A", 20.0), ("B", 20.0), ("C", 0.1)]


def test_producto_mas_vendido(ventas):
    assert practica.producto_mas_vendido(ventas) == "Antivirus"
    assert practica.producto_mas_vendido(practica.filtrar_ventas(ventas, categoria="Equipos")) == (
        "Portátil"
    )
    assert practica.producto_mas_vendido(MINI) == "A"
    assert practica.producto_mas_vendido([]) is None


def test_ticket_medio(ventas):
    assert practica.ticket_medio(ventas) == 1084.34
    assert practica.ticket_medio(MINI) == 13.37
    assert practica.ticket_medio([]) == 0.0


def test_informe_completo(ventas):
    assert _lineas(practica.generar_informe(ventas)) == _lineas(INFORME)


def test_informe_sin_salto_final(ventas):
    informe = practica.generar_informe(ventas)
    assert not informe.endswith("\n")
    assert all(len(linea) <= practica.ANCHO for linea in informe.split("\n"))


def test_informe_filtrado(ventas):
    lineas = _lineas(practica.generar_informe(practica.filtrar_ventas(ventas, region="Sur")))
    assert lineas[3] == "Ventas registradas                         8"
    assert lineas[4] == "Importe total                       6,062.00"
    assert lineas[6] == "Producto más vendido               Antivirus"
    assert lineas[8:10] == ["Por región", "  Sur                               6,062.00"]
    assert "  Alan                              4,525.00" in lineas
    assert not any(linea.startswith("  Ada") for linea in lineas)


def test_informe_vacio():
    lineas = _lineas(practica.generar_informe([]))
    assert lineas == [
        "=" * 44,
        "             INFORME DE VENTAS",
        "=" * 44,
        "Ventas registradas                         0",
        "Importe total                           0.00",
        "Ticket medio                            0.00",
        "Producto más vendido                       -",
        "-" * 44,
        "Por región",
        "-" * 44,
        "Por categoría",
        "-" * 44,
        "Por vendedor",
        "=" * 44,
    ]


def test_main_imprime_dos_informes(capsys):
    practica.main()
    salida = capsys.readouterr().out
    assert salida.count("INFORME DE VENTAS") == 2
    assert "21,686.80" in salida
