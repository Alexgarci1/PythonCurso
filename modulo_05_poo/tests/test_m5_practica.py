"""Tests de la práctica 5: modelo de dominio de una biblioteca."""

import dataclasses
import inspect
from datetime import date

import pytest

import m5_practica_biblioteca as bib

HOY = date(2026, 11, 2)


@pytest.fixture
def libro():
    return bib.Libro("L001", "Clean Code", 2008, "Robert C. Martin")


@pytest.fixture
def biblioteca():
    central = bib.Biblioteca("Central")
    central.anadir_material(bib.Libro("L001", "Clean Code", 2008, "Robert C. Martin"))
    central.anadir_material(bib.Libro("L002", "El programador pragmático", 1999, "Hunt y Thomas"))
    central.anadir_material(bib.Revista("R001", "Byte", 1984, 42))
    central.anadir_material(bib.Dvd("D001", "Matrix", 1999, 136))
    central.anadir_material(bib.Dvd("D002", "El código Enigma", 2014, 114))
    central.registrar_socio("Ada")
    central.registrar_socio("Linus")
    return central


# ------------------------------------------------------------------- Material
def test_material_es_abstracta():
    with pytest.raises(TypeError):
        bib.Material("X001", "Genérico", 2000)


def test_material_jerarquia():
    for clase in (bib.Libro, bib.Revista, bib.Dvd):
        assert issubclass(clase, bib.Material)
        assert "super().__init__" in inspect.getsource(clase.__init__)


def test_material_atributos(libro):
    assert (libro.codigo, libro.titulo, libro.anio, libro.autor) == (
        "L001", "Clean Code", 2008, "Robert C. Martin",
    )
    assert bib.Revista("R001", "Byte", 1984, 42).numero == 42
    assert bib.Dvd("D001", "Matrix", 1999, 136).minutos == 136


def test_material_dias_prestamo(libro):
    assert libro.dias_prestamo == 21
    assert bib.Revista("R001", "Byte", 1984, 42).dias_prestamo == 7
    assert bib.Dvd("D001", "Matrix", 1999, 136).dias_prestamo == 3
    assert isinstance(inspect.getattr_static(bib.Libro, "dias_prestamo"), property)


def test_material_disponible_prestar_y_devolver(libro):
    assert libro.disponible is True
    libro.prestar()
    assert libro.disponible is False
    libro.devolver()
    assert libro.disponible is True


def test_material_no_se_presta_dos_veces(libro):
    libro.prestar()
    with pytest.raises(ValueError):
        libro.prestar()
    assert libro.disponible is False


def test_material_no_se_devuelve_sin_prestar(libro):
    with pytest.raises(ValueError):
        libro.devolver()
    assert libro.disponible is True


def test_material_disponible_solo_lectura(libro):
    with pytest.raises(AttributeError):
        libro.disponible = False


def test_material_str(libro):
    assert str(libro) == "[L001] Clean Code (2008), de Robert C. Martin"
    assert str(bib.Revista("R001", "Byte", 1984, 42)) == "[R001] Byte (1984), n.º 42"
    assert str(bib.Dvd("D001", "Matrix", 1999, 136)) == "[D001] Matrix (1999)"
    assert "__str__" not in vars(bib.Dvd), "Dvd hereda __str__: no lo redefinas"


def test_material_str_reutiliza_el_heredado(monkeypatch, libro):
    monkeypatch.setattr(bib.Material, "__str__", lambda self: "BASE")
    assert str(libro) == "BASE, de Robert C. Martin"
    assert str(bib.Revista("R001", "Byte", 1984, 42)) == "BASE, n.º 42"


def test_material_repr(libro):
    assert repr(libro) == "Libro('L001', 'Clean Code')"
    assert repr(bib.Dvd("D001", "Matrix", 1999, 136)) == "Dvd('D001', 'Matrix')"
    assert "__repr__" not in vars(bib.Libro), "__repr__ se define una sola vez, en Material"


def test_material_igualdad(libro):
    assert libro == bib.Libro("L001", "Otro título", 2020, "Otra autora")
    assert libro != bib.Libro("L002", "Clean Code", 2008, "Robert C. Martin")
    assert libro == bib.Dvd("L001", "Mismo código", 2000, 90)
    assert libro != "L001"
    assert len({libro, bib.Libro("L001", "Copia", 2008, "x")}) == 1


# ---------------------------------------------------------------------- Socio
def test_socio_dataclass():
    assert dataclasses.is_dataclass(bib.Socio)
    ada = bib.Socio(1, "Ada")
    assert (ada.numero, ada.nombre, ada.prestados) == (1, "Ada", [])
    assert ada == bib.Socio(1, "Ada")
    assert [campo.name for campo in dataclasses.fields(bib.Socio)] == [
        "numero", "nombre", "prestados",
    ]


def test_socios_no_comparten_lista():
    ada, linus = bib.Socio(1, "Ada"), bib.Socio(2, "Linus")
    ada.prestados.append("algo")
    assert linus.prestados == []


def test_socio_puede_tomar_prestado():
    ada = bib.Socio(1, "Ada")
    assert bib.Socio.MAX_PRESTAMOS == 3
    for cantidad in range(3):
        assert ada.puede_tomar_prestado() is True
        ada.prestados.append(f"material {cantidad}")
    assert ada.puede_tomar_prestado() is False


def test_socio_usa_la_constante(monkeypatch):
    monkeypatch.setattr(bib.Socio, "MAX_PRESTAMOS", 1)
    ada = bib.Socio(1, "Ada")
    ada.prestados.append("uno")
    assert ada.puede_tomar_prestado() is False


# ------------------------------------------------------------------- Prestamo
def test_prestamo_dataclass(libro):
    assert dataclasses.is_dataclass(bib.Prestamo)
    ada = bib.Socio(1, "Ada")
    prestamo = bib.Prestamo(libro, ada, HOY)
    assert prestamo.material is libro
    assert prestamo.socio is ada
    assert prestamo.fecha == HOY


@pytest.mark.parametrize(
    "clase, dato, esperada",
    [
        ("Libro", "autora", date(2026, 11, 23)),
        ("Revista", 1, date(2026, 11, 9)),
        ("Dvd", 90, date(2026, 11, 5)),
    ],
)
def test_prestamo_fecha_devolucion(clase, dato, esperada):
    material = getattr(bib, clase)("X001", "título", 2000, dato)
    prestamo = bib.Prestamo(material, bib.Socio(1, "Ada"), HOY)
    assert prestamo.fecha_devolucion == esperada
    assert isinstance(inspect.getattr_static(bib.Prestamo, "fecha_devolucion"), property)


@pytest.mark.parametrize(
    "hoy, retraso, vencido",
    [
        (date(2026, 11, 2), 0, False),
        (date(2026, 11, 22), 0, False),
        (date(2026, 11, 23), 0, False),
        (date(2026, 11, 24), 1, True),
        (date(2026, 11, 30), 7, True),
        (date(2026, 12, 23), 30, True),
    ],
)
def test_prestamo_retraso(libro, hoy, retraso, vencido):
    prestamo = bib.Prestamo(libro, bib.Socio(1, "Ada"), HOY)
    assert prestamo.dias_de_retraso(hoy) == retraso
    assert prestamo.esta_vencido(hoy) is vencido


# ----------------------------------------------------------------- Biblioteca
def test_biblioteca_vacia():
    nueva = bib.Biblioteca("Barrio")
    assert nueva.nombre == "Barrio"
    assert len(nueva) == 0
    assert list(nueva) == []
    assert nueva.prestamos == ()
    assert nueva.disponibles() == []
    assert nueva.resumen() == "Barrio: 0 materiales, 0 disponibles, 0 socios"


def test_biblioteca_no_hereda_de_colecciones():
    assert bib.Biblioteca.__bases__ == (object,), "Biblioteca usa composición, no herencia"


def test_biblioteca_catalogo(biblioteca):
    assert len(biblioteca) == 5
    assert "L001" in biblioteca
    assert "X999" not in biblioteca
    assert biblioteca.buscar("R001").titulo == "Byte"
    assert biblioteca.buscar("X999") is None
    assert [material.codigo for material in biblioteca] == ["L001", "L002", "R001", "D001", "D002"]


def test_biblioteca_codigo_repetido(biblioteca):
    with pytest.raises(ValueError):
        biblioteca.anadir_material(bib.Dvd("L001", "Repetido", 2020, 90))
    assert len(biblioteca) == 5
    assert biblioteca.buscar("L001").titulo == "Clean Code"


def test_biblioteca_bibliotecas_independientes(biblioteca):
    assert len(bib.Biblioteca("Otra")) == 0


def test_biblioteca_buscar_por_titulo(biblioteca):
    assert [m.codigo for m in biblioteca.buscar_por_titulo("CÓDIGO")] == ["D002"]
    assert [m.codigo for m in biblioteca.buscar_por_titulo("MA")] == ["L002", "D001"]
    assert [m.codigo for m in biblioteca.buscar_por_titulo("e")] == [
        "R001", "L001", "D002", "L002",
    ]
    assert biblioteca.buscar_por_titulo("python") == []


def test_biblioteca_socios(biblioteca):
    assert biblioteca.socio(1).nombre == "Ada"
    assert biblioteca.socio(2).nombre == "Linus"
    assert biblioteca.socio(99) is None
    grace = biblioteca.registrar_socio("Grace")
    assert isinstance(grace, bib.Socio)
    assert grace.numero == 3
    assert biblioteca.socio(3) is grace


def test_biblioteca_prestar(biblioteca):
    prestamo = biblioteca.prestar("L001", 1, HOY)
    assert isinstance(prestamo, bib.Prestamo)
    assert prestamo.material is biblioteca.buscar("L001")
    assert prestamo.socio is biblioteca.socio(1)
    assert prestamo.fecha == HOY
    assert biblioteca.buscar("L001").disponible is False
    assert biblioteca.socio(1).prestados == [biblioteca.buscar("L001")]
    assert biblioteca.prestamos == (prestamo,)
    assert [m.codigo for m in biblioteca.disponibles()] == ["D001", "D002", "L002", "R001"]
    assert biblioteca.resumen() == "Central: 5 materiales, 4 disponibles, 2 socios"


@pytest.mark.parametrize(
    "codigo, socio, mensaje",
    [
        ("X999", 1, "No existe el material X999"),
        ("L001", 99, "No existe el socio 99"),
        ("X999", 99, "No existe el material X999"),
    ],
)
def test_biblioteca_prestar_no_existe(biblioteca, codigo, socio, mensaje):
    with pytest.raises(ValueError) as error:
        biblioteca.prestar(codigo, socio, HOY)
    assert str(error.value) == mensaje
    assert biblioteca.prestamos == ()


def test_biblioteca_prestar_material_ya_prestado(biblioteca):
    biblioteca.prestar("L001", 1, HOY)
    with pytest.raises(ValueError):
        biblioteca.prestar("L001", 2, HOY)
    assert len(biblioteca.prestamos) == 1
    assert biblioteca.socio(2).prestados == []


def test_biblioteca_prestar_maximo(biblioteca):
    for codigo in ("L001", "L002", "R001"):
        biblioteca.prestar(codigo, 1, HOY)
    with pytest.raises(ValueError) as error:
        biblioteca.prestar("D001", 1, HOY)
    assert str(error.value) == "Ada ha alcanzado el máximo de préstamos"
    assert biblioteca.buscar("D001").disponible is True
    assert len(biblioteca.socio(1).prestados) == 3
    biblioteca.prestar("D001", 2, HOY)
    assert len(biblioteca.prestamos) == 4


def test_biblioteca_prestar_delega_en_el_material(biblioteca, monkeypatch):
    llamadas = []
    original = bib.Material.prestar

    def espia(self):
        llamadas.append(self.codigo)
        original(self)

    monkeypatch.setattr(bib.Material, "prestar", espia)
    biblioteca.prestar("D001", 1, HOY)
    assert llamadas == ["D001"], "Biblioteca.prestar tiene que llamar a material.prestar()"


def test_biblioteca_devolver(biblioteca):
    prestamo = biblioteca.prestar("L001", 1, HOY)
    biblioteca.prestar("D001", 1, HOY)
    cerrado = biblioteca.devolver("L001")
    assert cerrado is prestamo
    assert biblioteca.buscar("L001").disponible is True
    assert [m.codigo for m in biblioteca.socio(1).prestados] == ["D001"]
    assert [p.material.codigo for p in biblioteca.prestamos] == ["D001"]
    biblioteca.prestar("L001", 2, HOY)
    assert biblioteca.buscar("L001").disponible is False


@pytest.mark.parametrize("codigo", ["L002", "X999"])
def test_biblioteca_devolver_sin_prestamo(biblioteca, codigo):
    biblioteca.prestar("L001", 1, HOY)
    with pytest.raises(ValueError) as error:
        biblioteca.devolver(codigo)
    assert str(error.value) == f"No hay ningún préstamo de {codigo}"
    assert len(biblioteca.prestamos) == 1


def test_biblioteca_prestamos_es_una_tupla(biblioteca):
    biblioteca.prestar("L001", 1, HOY)
    assert isinstance(biblioteca.prestamos, tuple)
    with pytest.raises(AttributeError):
        biblioteca.prestamos = ()


def test_biblioteca_prestamos_vencidos(biblioteca):
    biblioteca.prestar("L001", 1, HOY)                  # vence el 23/11
    biblioteca.prestar("R001", 1, HOY)                  # vence el 9/11
    biblioteca.prestar("D001", 2, date(2026, 11, 4))    # vence el 7/11
    biblioteca.prestar("D002", 2, date(2026, 11, 20))   # vence el 23/11
    assert biblioteca.prestamos_vencidos(date(2026, 11, 5)) == []
    assert [p.material.codigo for p in biblioteca.prestamos_vencidos(date(2026, 11, 8))] == ["D001"]
    assert [p.material.codigo for p in biblioteca.prestamos_vencidos(date(2026, 11, 15))] == [
        "D001", "R001",
    ]
    assert [p.material.codigo for p in biblioteca.prestamos_vencidos(date(2026, 11, 30))] == [
        "D001", "R001", "L001", "D002",
    ]
    assert len(biblioteca.prestamos) == 4


def test_biblioteca_admite_un_material_nuevo(biblioteca):
    class Audiolibro(bib.Material):
        @property
        def dias_prestamo(self):
            return 14

    biblioteca.anadir_material(Audiolibro("A001", "Dune", 2021))
    prestamo = biblioteca.prestar("A001", 2, HOY)
    assert prestamo.fecha_devolucion == date(2026, 11, 16)
    assert repr(biblioteca.buscar("A001")) == "Audiolibro('A001', 'Dune')"
    assert biblioteca.resumen() == "Central: 6 materiales, 5 disponibles, 2 socios"
