"""Tests de aceptación del proyecto final: gestor de incidencias."""

import dataclasses
import inspect
import logging
from datetime import date
from pathlib import Path

import pytest

import m7_proyecto_app as app
from incidencias import almacen, excepciones, gestor as modulo_gestor, informes, modelos
from incidencias.excepciones import (
    DatosNoValidos,
    ErrorDeAlmacen,
    ErrorDeIncidencias,
    IncidenciaNoEncontrada,
    TransicionNoValida,
)
from incidencias.gestor import GestorIncidencias
from incidencias.modelos import Incidencia

DATOS = Path(__file__).parent.parent / "datos"
EJEMPLO = DATOS / "incidencias_ejemplo.csv"
HOY = date(2026, 11, 27)
ALTA = date(2026, 11, 2)

INFORME = """\
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
=============================================================================="""


def _lineas(texto):
    return [linea.rstrip() for linea in texto.split("\n")]


@pytest.fixture
def incidencia():
    return Incidencia(7, "No funciona el correo", "Ada", ALTA, "alta")


@pytest.fixture
def gestor():
    """Tres incidencias dadas de alta en días distintos."""
    nuevo = GestorIncidencias()
    nuevo.crear("No funciona el correo", "Ada", "alta", hoy=date(2026, 11, 2))
    nuevo.crear("Instalar Python", "Linus", hoy=date(2026, 11, 3))
    nuevo.crear("Caída del servidor", "Alan", "critica", hoy=date(2026, 11, 10))
    return nuevo


@pytest.fixture
def ejemplo():
    return GestorIncidencias(almacen.cargar(EJEMPLO))


# ---------------------------------------------------------------- excepciones
def test_excepciones_jerarquia():
    assert ErrorDeIncidencias.__bases__ == (Exception,)
    for clase in (DatosNoValidos, IncidenciaNoEncontrada, TransicionNoValida, ErrorDeAlmacen):
        assert clase.__bases__ == (ErrorDeIncidencias,)


def test_excepciones_incidencia_no_encontrada():
    error = IncidenciaNoEncontrada(7)
    assert error.identificador == 7
    assert str(error) == "No existe la incidencia 7"


def test_excepciones_transicion_no_valida():
    error = TransicionNoValida("cerrada", "abierta")
    assert (error.actual, error.nuevo) == ("cerrada", "abierta")
    assert str(error) == "No se puede pasar de cerrada a abierta"


# ----------------------------------------------------------------- Incidencia
def test_incidencia_es_dataclass_con_sus_campos():
    assert dataclasses.is_dataclass(Incidencia)
    assert [campo.name for campo in dataclasses.fields(Incidencia)] == [
        "id", "titulo", "solicitante", "fecha_alta", "prioridad", "estado", "asignada_a",
        "fecha_cierre",
    ]


def test_incidencia_valores_por_defecto():
    nueva = Incidencia(1, "Pantalla rota", "Grace", ALTA)
    assert (nueva.prioridad, nueva.estado, nueva.asignada_a, nueva.fecha_cierre) == (
        "media", "abierta", "", None,
    )
    assert nueva == Incidencia(1, "Pantalla rota", "Grace", ALTA)


def test_incidencia_limpia_espacios():
    nueva = Incidencia(1, "  Pantalla rota ", " Grace  ", ALTA, asignada_a=" Marta ")
    assert (nueva.titulo, nueva.solicitante, nueva.asignada_a) == ("Pantalla rota", "Grace", "Marta")


@pytest.mark.parametrize(
    "cambios, mensaje",
    [
        ({"titulo": ""}, "El título es obligatorio"),
        ({"titulo": "   "}, "El título es obligatorio"),
        ({"solicitante": " "}, "El solicitante es obligatorio"),
        ({"prioridad": "urgente"}, "Prioridad no válida: urgente"),
        ({"prioridad": "ALTA"}, "Prioridad no válida: ALTA"),
        ({"estado": "pendiente"}, "Estado no válido: pendiente"),
    ],
)
def test_incidencia_datos_no_validos(cambios, mensaje):
    datos = {"id": 1, "titulo": "Pantalla rota", "solicitante": "Grace", "fecha_alta": ALTA}
    with pytest.raises(DatosNoValidos) as error:
        Incidencia(**{**datos, **cambios})
    assert str(error.value) == mensaje


@pytest.mark.parametrize(
    "estado, esperado",
    [("abierta", True), ("en_curso", True), ("resuelta", False), ("cerrada", False)],
)
def test_incidencia_pendiente(estado, esperado):
    assert Incidencia(1, "x", "y", ALTA, estado=estado).pendiente is esperado
    assert isinstance(inspect.getattr_static(Incidencia, "pendiente"), property)


@pytest.mark.parametrize(
    "actual, nuevo",
    [
        ("abierta", "en_curso"),
        ("abierta", "cerrada"),
        ("en_curso", "abierta"),
        ("en_curso", "resuelta"),
        ("resuelta", "en_curso"),
        ("resuelta", "cerrada"),
    ],
)
def test_incidencia_transiciones_permitidas(actual, nuevo):
    caso = Incidencia(1, "x", "y", ALTA, estado=actual)
    caso.cambiar_estado(nuevo, HOY)
    assert caso.estado == nuevo
    assert caso.fecha_cierre == (HOY if nuevo == "cerrada" else None)


@pytest.mark.parametrize(
    "actual, nuevo",
    [
        ("abierta", "resuelta"),
        ("abierta", "abierta"),
        ("en_curso", "cerrada"),
        ("resuelta", "abierta"),
        ("cerrada", "abierta"),
        ("cerrada", "en_curso"),
        ("cerrada", "cerrada"),
    ],
)
def test_incidencia_transiciones_no_permitidas(actual, nuevo):
    caso = Incidencia(1, "x", "y", ALTA, estado=actual)
    with pytest.raises(TransicionNoValida) as error:
        caso.cambiar_estado(nuevo, HOY)
    assert (error.value.actual, error.value.nuevo) == (actual, nuevo)
    assert caso.estado == actual
    assert caso.fecha_cierre is None


def test_incidencia_cambiar_a_un_estado_que_no_existe(incidencia):
    with pytest.raises(DatosNoValidos) as error:
        incidencia.cambiar_estado("archivada", HOY)
    assert str(error.value) == "Estado no válido: archivada"
    assert incidencia.estado == "abierta"


def test_incidencia_usa_la_tabla_de_transiciones(monkeypatch, incidencia):
    monkeypatch.setitem(modelos.TRANSICIONES, "abierta", ("resuelta",))
    incidencia.cambiar_estado("resuelta", HOY)
    assert incidencia.estado == "resuelta"


def test_incidencia_dias_abierta(incidencia):
    assert incidencia.dias_abierta(date(2026, 11, 2)) == 0
    assert incidencia.dias_abierta(HOY) == 25
    incidencia.cambiar_estado("cerrada", date(2026, 11, 5))
    assert incidencia.dias_abierta(HOY) == 3


def test_incidencia_a_fila(incidencia):
    assert incidencia.a_fila() == {
        "id": "7",
        "titulo": "No funciona el correo",
        "solicitante": "Ada",
        "prioridad": "alta",
        "estado": "abierta",
        "asignada_a": "",
        "fecha_alta": "2026-11-02",
        "fecha_cierre": "",
    }
    assert list(incidencia.a_fila()) == modelos.CAMPOS
    incidencia.cambiar_estado("cerrada", date(2026, 11, 5))
    assert incidencia.a_fila()["fecha_cierre"] == "2026-11-05"


def test_incidencia_desde_fila(incidencia):
    copia = Incidencia.desde_fila(incidencia.a_fila())
    assert copia == incidencia
    assert isinstance(copia.id, int) and isinstance(copia.fecha_alta, date)
    incidencia.asignada_a = "Marta"
    incidencia.cambiar_estado("cerrada", date(2026, 11, 5))
    cerrada = Incidencia.desde_fila(incidencia.a_fila())
    assert cerrada == incidencia
    assert cerrada.fecha_cierre == date(2026, 11, 5)
    assert isinstance(inspect.getattr_static(Incidencia, "desde_fila"), classmethod)


@pytest.mark.parametrize(
    "cambios, causa",
    [
        ({"id": "siete"}, ValueError),
        ({"fecha_alta": "02/11/2026"}, ValueError),
        ({"fecha_cierre": "ayer"}, ValueError),
        ({"prioridad": "urgente"}, None),
        ({"titulo": ""}, None),
    ],
)
def test_incidencia_desde_fila_no_valida(incidencia, cambios, causa):
    with pytest.raises(DatosNoValidos) as error:
        Incidencia.desde_fila({**incidencia.a_fila(), **cambios})
    if causa is not None:
        assert isinstance(error.value.__cause__, causa), "Falta raise ... from error"


def test_incidencia_desde_fila_sin_una_clave(incidencia):
    fila = incidencia.a_fila()
    del fila["estado"]
    with pytest.raises(DatosNoValidos) as error:
        Incidencia.desde_fila(fila)
    assert isinstance(error.value.__cause__, KeyError)


# --------------------------------------------------------------------- gestor
def test_gestor_vacio():
    vacio = GestorIncidencias()
    assert len(vacio) == 0
    assert list(vacio) == []
    assert vacio.pendientes() == []
    assert vacio.filtrar() == []
    assert vacio.contar_por("estado") == {}


def test_gestor_usa_composicion():
    assert GestorIncidencias.__bases__ == (object,)
    assert len(GestorIncidencias()) == 0
    primero = GestorIncidencias()
    primero.crear("x", "y")
    assert len(GestorIncidencias()) == 0, "Dos gestores comparten las incidencias"


def test_gestor_crear(gestor):
    assert len(gestor) == 3
    assert [caso.id for caso in gestor] == [1, 2, 3]
    nueva = gestor.crear("  VPN lenta ", "Ada", "alta", hoy=HOY)
    assert isinstance(nueva, Incidencia)
    assert (nueva.id, nueva.titulo, nueva.prioridad, nueva.estado, nueva.fecha_alta) == (
        4, "VPN lenta", "alta", "abierta", HOY,
    )
    assert gestor.obtener(2).prioridad == "media"


def test_gestor_crear_usa_la_fecha_actual_por_defecto():
    assert GestorIncidencias().crear("x", "y").fecha_alta == date.today()


@pytest.mark.parametrize("datos", [("", "Ada"), ("Título", ""), ("Título", "Ada", "urgente")])
def test_gestor_crear_con_datos_no_validos(gestor, datos):
    with pytest.raises(DatosNoValidos):
        gestor.crear(*datos)
    assert len(gestor) == 3
    assert gestor.crear("Válida", "Ada").id == 4


def test_gestor_con_incidencias_iniciales():
    iniciales = [Incidencia(5, "a", "x", ALTA), Incidencia(2, "b", "y", ALTA)]
    cargado = GestorIncidencias(iniciales)
    assert [caso.id for caso in cargado] == [2, 5]
    assert cargado.crear("c", "z").id == 6
    assert cargado.obtener(5) is iniciales[0]


def test_gestor_obtener(gestor):
    assert gestor.obtener(3).titulo == "Caída del servidor"
    with pytest.raises(IncidenciaNoEncontrada) as error:
        gestor.obtener(99)
    assert error.value.identificador == 99


def test_gestor_cambiar_estado(gestor):
    devuelta = gestor.cambiar_estado(1, "en_curso")
    assert devuelta is gestor.obtener(1)
    assert devuelta.estado == "en_curso"
    gestor.cambiar_estado(1, "resuelta")
    gestor.cambiar_estado(1, "cerrada", hoy=date(2026, 11, 5))
    assert gestor.obtener(1).fecha_cierre == date(2026, 11, 5)
    gestor.cambiar_estado(2, "cerrada")
    assert gestor.obtener(2).fecha_cierre == date.today()


def test_gestor_cambiar_estado_errores(gestor):
    with pytest.raises(IncidenciaNoEncontrada):
        gestor.cambiar_estado(99, "en_curso")
    with pytest.raises(TransicionNoValida):
        gestor.cambiar_estado(1, "resuelta")
    with pytest.raises(DatosNoValidos):
        gestor.cambiar_estado(1, "archivada")
    assert gestor.obtener(1).estado == "abierta"


def test_gestor_delega_en_la_incidencia(gestor, monkeypatch):
    llamadas = []
    original = Incidencia.cambiar_estado

    def espia(self, nuevo, hoy):
        llamadas.append((self.id, nuevo))
        original(self, nuevo, hoy)

    monkeypatch.setattr(Incidencia, "cambiar_estado", espia)
    gestor.cambiar_estado(2, "en_curso")
    assert llamadas == [(2, "en_curso")], "El gestor tiene que llamar a incidencia.cambiar_estado"


def test_gestor_asignar(gestor):
    devuelta = gestor.asignar(1, "  Marta ")
    assert devuelta is gestor.obtener(1)
    assert (devuelta.asignada_a, devuelta.estado) == ("Marta", "en_curso")
    gestor.cambiar_estado(1, "resuelta")
    gestor.asignar(1, "Pablo")
    assert (gestor.obtener(1).asignada_a, gestor.obtener(1).estado) == ("Pablo", "resuelta")
    with pytest.raises(IncidenciaNoEncontrada):
        gestor.asignar(99, "Marta")


@pytest.mark.parametrize(
    "criterios, esperados",
    [
        ({}, [1, 2, 3, 4, 5, 6, 7, 8]),
        ({"estado": "abierta"}, [3, 5, 7]),
        ({"estado": "cerrada"}, [1, 8]),
        ({"prioridad": "media"}, [2, 5, 7]),
        ({"asignada_a": "Marta"}, [1, 4]),
        ({"asignada_a": ""}, [3, 5, 7, 8]),
        ({"texto": "DE"}, [4, 5, 6, 7]),
        ({"texto": "python"}, [2]),
        ({"estado": "en_curso", "asignada_a": "Pablo"}, [6]),
        ({"prioridad": "media", "estado": "abierta", "texto": "usuario"}, [5]),
        ({"estado": "resuelta", "prioridad": "critica"}, []),
        ({"texto": "no aparece"}, []),
    ],
)
def test_gestor_filtrar(ejemplo, criterios, esperados):
    assert [caso.id for caso in ejemplo.filtrar(**criterios)] == esperados


def test_gestor_filtrar_criterios_solo_por_nombre(ejemplo):
    with pytest.raises(TypeError):
        ejemplo.filtrar("abierta")


def test_gestor_pendientes(ejemplo):
    assert [caso.id for caso in ejemplo.pendientes()] == [4, 6, 5, 7, 3]


def test_gestor_pendientes_desempates():
    cola = GestorIncidencias()
    cola.crear("b", "x", "alta", hoy=date(2026, 11, 5))
    cola.crear("a", "x", "alta", hoy=date(2026, 11, 3))
    cola.crear("c", "x", "alta", hoy=date(2026, 11, 3))
    cola.crear("d", "x", "baja", hoy=date(2026, 11, 1))
    cola.crear("e", "x", "critica", hoy=date(2026, 11, 9))
    assert [caso.id for caso in cola.pendientes()] == [5, 2, 3, 1, 4]
    cola.cambiar_estado(5, "cerrada")
    cola.asignar(1, "Marta")
    assert [caso.id for caso in cola.pendientes()] == [2, 3, 1, 4]


def test_gestor_contar_por(ejemplo):
    assert ejemplo.contar_por("estado") == {"cerrada": 2, "resuelta": 1, "abierta": 3, "en_curso": 2}
    assert ejemplo.contar_por("prioridad") == {"alta": 2, "media": 3, "baja": 2, "critica": 1}
    assert ejemplo.contar_por("asignada_a") == {"Marta": 2, "Pablo": 2, "": 4}
    assert ejemplo.contar_por("solicitante")["Ada"] == 2


def test_gestor_sin_entrada_salida_ni_ficheros():
    codigo = inspect.getsource(modulo_gestor) + inspect.getsource(modelos)
    for prohibido in ("print(", "input(", "open("):
        assert prohibido not in codigo, f"gestor.py y modelos.py no pueden usar {prohibido}...)"


# -------------------------------------------------------------------- almacén
def test_almacen_cargar_ejemplo():
    incidencias = almacen.cargar(EJEMPLO)
    assert len(incidencias) == 8
    assert all(isinstance(caso, Incidencia) for caso in incidencias)
    assert incidencias[0] == Incidencia(
        1, "No funciona el correo", "Ada", date(2026, 11, 2), "alta", "cerrada", "Marta",
        date(2026, 11, 5),
    )
    assert incidencias[3].titulo == "Caída del servidor de ficheros"
    assert incidencias[2].fecha_cierre is None


def test_almacen_fichero_que_no_existe(tmp_path):
    assert almacen.cargar(tmp_path / "no_existe.csv") == []


def test_almacen_guardar_y_cargar(gestor, tmp_path):
    gestor.asignar(1, "Marta")
    gestor.cambiar_estado(3, "cerrada", hoy=date(2026, 11, 12))
    gestor.crear('Monitor de 27", curvo; con eñe', "Íñigo", "baja", hoy=HOY)
    ruta = tmp_path / "datos" / "incidencias.csv"
    almacen.guardar(ruta, gestor)
    assert almacen.cargar(ruta) == list(gestor)
    assert almacen.cargar(str(ruta)) == list(gestor)


def test_almacen_formato_del_fichero(gestor, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    almacen.guardar(ruta, list(gestor))
    contenido = ruta.read_bytes()
    assert b"\r\r\n" not in contenido, 'Falta newline="" al abrir el fichero'
    lineas = contenido.decode("utf-8").splitlines()
    assert lineas[0] == "id,titulo,solicitante,prioridad,estado,asignada_a,fecha_alta,fecha_cierre"
    assert lineas[1] == "1,No funciona el correo,Ada,alta,abierta,,2026-11-02,"
    assert lineas[3] == "3,Caída del servidor,Alan,critica,abierta,,2026-11-10,"
    assert len(lineas) == 4


def test_almacen_guardar_sin_incidencias(tmp_path):
    ruta = tmp_path / "vacio.csv"
    almacen.guardar(ruta, [])
    assert ruta.read_text(encoding="utf-8").splitlines() == [",".join(modelos.CAMPOS)]
    assert almacen.cargar(ruta) == []


def test_almacen_guardar_sustituye_el_contenido(gestor, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    almacen.guardar(ruta, gestor)
    almacen.guardar(ruta, list(gestor)[:1])
    assert len(almacen.cargar(ruta)) == 1


@pytest.mark.parametrize(
    "fila, linea",
    [
        ("x,Título,Ada,media,abierta,,2026-11-02,", 3),
        ("2,Título,Ada,urgente,abierta,,2026-11-02,", 3),
        ("2,Título,Ada,media,abierta,,02/11/2026,", 3),
        ("2,,Ada,media,abierta,,2026-11-02,", 3),
    ],
)
def test_almacen_fila_no_valida(tmp_path, fila, linea):
    ruta = tmp_path / "corrupto.csv"
    ruta.write_text(
        ",".join(modelos.CAMPOS) + "\n1,Correcta,Ada,media,abierta,,2026-11-02,\n" + fila + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ErrorDeAlmacen) as error:
        almacen.cargar(ruta)
    assert str(error.value).startswith(f"Línea {linea}: ")
    assert isinstance(error.value.__cause__, DatosNoValidos), "Falta raise ... from error"


def test_almacen_faltan_columnas(tmp_path):
    ruta = tmp_path / "otro.csv"
    ruta.write_text("id,titulo\n1,Solo dos columnas\n", encoding="utf-8")
    with pytest.raises(ErrorDeAlmacen):
        almacen.cargar(ruta)


def test_almacen_registra_lo_que_hace(gestor, tmp_path, caplog):
    with caplog.at_level(logging.INFO, logger=almacen.__name__):
        almacen.guardar(tmp_path / "incidencias.csv", gestor)
    assert len(caplog.records) == 1
    assert "3" in caplog.records[0].getMessage()
    assert "print(" not in inspect.getsource(almacen)


# ------------------------------------------------------------------- informes
def test_informes_linea(incidencia):
    assert informes.linea(incidencia) == (
        "   7  alta      abierta   -           No funciona el correo"
    )
    incidencia.asignada_a = "Marta"
    incidencia.cambiar_estado("en_curso", HOY)
    assert informes.linea(incidencia) == (
        "   7  alta      en_curso  Marta       No funciona el correo"
    )
    assert informes.linea(Incidencia(1234, "x", "y", ALTA, "critica")).startswith(
        "1234  critica   abierta   -           x"
    )


def test_informes_listado(ejemplo):
    lineas = _lineas(informes.listado(ejemplo.pendientes()))
    assert lineas == [
        "  ID  PRIORIDAD ESTADO    ASIGNADA A  TÍTULO",
        "-" * 78,
        "   4  critica   en_curso  Marta       Caída del servidor de ficheros",
        "   6  alta      en_curso  Pablo       VPN lenta desde casa",
        "   5  media     abierta   -           Alta de usuario nuevo",
        "   7  media     abierta   -           Renovar licencia del antivirus",
        "   3  baja      abierta   -           Pantalla rota",
    ]
    assert len(_lineas(informes.listado(list(ejemplo)))) == 10


def test_informes_listado_vacio():
    assert informes.listado([]) == "No hay incidencias."


def test_informes_listado_reutiliza_linea(monkeypatch, ejemplo):
    monkeypatch.setattr(informes, "linea", lambda incidencia: f"<{incidencia.id}>")
    assert _lineas(informes.listado(ejemplo.pendientes()))[2:] == ["<4>", "<6>", "<5>", "<7>", "<3>"]


def test_informes_resumen(ejemplo):
    assert _lineas(informes.resumen(ejemplo, HOY)) == _lineas(INFORME)
    assert not informes.resumen(ejemplo, HOY).endswith("\n")


def test_informes_resumen_vacio():
    lineas = _lineas(informes.resumen(GestorIncidencias(), HOY))
    assert lineas[4] == "Total de incidencias: 0"
    assert lineas[7:11] == [
        "  abierta        0", "  en_curso       0", "  resuelta       0", "  cerrada        0",
    ]
    assert lineas[13:17] == [
        "  critica        0", "  alta           0", "  media          0", "  baja           0",
    ]
    assert lineas[18] == "Pendiente más antigua: ninguna"
    assert len(lineas) == 20


def test_informes_resumen_cambia_con_los_datos(ejemplo):
    ejemplo.cambiar_estado(3, "cerrada", hoy=HOY)
    ejemplo.crear("Nueva", "Ada", "critica", hoy=HOY)
    lineas = _lineas(informes.resumen(ejemplo, date(2026, 11, 30)))
    assert lineas[3] == "Fecha del informe: 2026-11-30"
    assert lineas[4] == "Total de incidencias: 9"
    assert lineas[7] == "  abierta        3"
    assert lineas[10] == "  cerrada        3"
    assert lineas[13] == "  critica        2"
    assert lineas[16] == "  baja           0"
    assert lineas[18] == "Pendiente más antigua: n.º 4, 20 días"


def test_informes_no_imprimen():
    assert "print(" not in inspect.getsource(informes)


# ------------------------------------------------------------------------ app
def _sesion(monkeypatch, capsys, ruta, respuestas):
    """Ejecuta main() respondiendo a cada input con el siguiente texto de la lista."""
    entradas = iter(respuestas)
    monkeypatch.setattr("builtins.input", lambda _="": next(entradas))
    codigo = app.main(ruta)
    pendientes_de_leer = list(entradas)
    assert pendientes_de_leer == [], f"El menú no ha pedido estos datos: {pendientes_de_leer}"
    return codigo, capsys.readouterr().out


def test_app_salir_guarda(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    codigo, salida = _sesion(monkeypatch, capsys, ruta, ["0"])
    assert codigo == 0
    assert "GESTOR DE INCIDENCIAS" in salida
    assert ruta.exists()
    assert almacen.cargar(ruta) == []


def test_app_alta(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    codigo, salida = _sesion(
        monkeypatch, capsys, ruta,
        ["1", "No funciona el correo", "Ada", "alta", "1", "Pantalla rota", "Grace", "", "0"],
    )
    assert codigo == 0
    assert "Creada la incidencia 1." in salida
    assert "Creada la incidencia 2." in salida
    guardadas = almacen.cargar(ruta)
    assert [(caso.titulo, caso.solicitante, caso.prioridad) for caso in guardadas] == [
        ("No funciona el correo", "Ada", "alta"),
        ("Pantalla rota", "Grace", "media"),
    ]
    assert guardadas[0].fecha_alta == date.today()


def test_app_los_datos_se_conservan_entre_ejecuciones(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    _sesion(monkeypatch, capsys, ruta, ["1", "Primera", "Ada", "", "0"])
    _, salida = _sesion(monkeypatch, capsys, ruta, ["1", "Segunda", "Linus", "baja", "2", "0"])
    assert "Creada la incidencia 2." in salida
    assert "Primera" in salida and "Segunda" in salida
    assert [caso.id for caso in almacen.cargar(ruta)] == [1, 2]


def test_app_listados_busqueda_e_informe(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    ruta.write_bytes(EJEMPLO.read_bytes())
    codigo, salida = _sesion(monkeypatch, capsys, ruta, ["3", "4", "python", "7", "0"])
    assert codigo == 0
    assert "   4  critica   en_curso  Marta       Caída del servidor de ficheros" in salida
    assert "   2  media     resuelta  Pablo       Instalar Python 3.13" in salida
    assert "INFORME DE INCIDENCIAS" in salida
    assert "Total de incidencias: 8" in salida
    assert almacen.cargar(ruta) == almacen.cargar(EJEMPLO)


def test_app_cambiar_estado_y_asignar(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    ruta.write_bytes(EJEMPLO.read_bytes())
    codigo, _ = _sesion(
        monkeypatch, capsys, ruta, ["5", "4", "resuelta", "6", "3", "Marta", "5", " 7 ", "cerrada", "0"]
    )
    assert codigo == 0
    guardadas = {caso.id: caso for caso in almacen.cargar(ruta)}
    assert guardadas[4].estado == "resuelta"
    assert (guardadas[3].asignada_a, guardadas[3].estado) == ("Marta", "en_curso")
    assert (guardadas[7].estado, guardadas[7].fecha_cierre) == ("cerrada", date.today())


def test_app_los_errores_no_detienen_el_programa(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    ruta.write_bytes(EJEMPLO.read_bytes())
    codigo, salida = _sesion(
        monkeypatch, capsys, ruta,
        [
            "9",                          # opción que no existe
            "hola",                       # tampoco
            "5", "99", "cerrada",         # incidencia que no existe
            "5", "1", "abierta",          # transición no permitida
            "5", "3", "archivada",        # estado que no existe
            "5", "abc",                   # el número no es un entero: no se pide el estado
            "1", "", "Ada", "",           # título vacío
            "1", "Título", "Ada", "urgente",   # prioridad que no existe
            "6", "99", "Marta",           # asignar una que no existe
            "0",
        ],
    )
    assert codigo == 0
    assert salida.count("Opción no válida.") == 2
    assert "Error: No existe la incidencia 99" in salida
    assert "Error: No se puede pasar de cerrada a abierta" in salida
    assert "Error: Estado no válido: archivada" in salida
    assert "Error: El título es obligatorio" in salida
    assert "Error: Prioridad no válida: urgente" in salida
    assert salida.count("Error: ") == 7
    assert "Traceback" not in salida
    assert almacen.cargar(ruta) == almacen.cargar(EJEMPLO), "Un error no puede cambiar los datos"


def test_app_fichero_corrupto(monkeypatch, capsys, tmp_path):
    ruta = tmp_path / "incidencias.csv"
    contenido = ",".join(modelos.CAMPOS) + "\nx,Título,Ada,media,abierta,,2026-11-02,\n"
    ruta.write_text(contenido, encoding="utf-8")
    codigo, salida = _sesion(monkeypatch, capsys, ruta, [])
    assert codigo == 1
    assert salida.startswith("Error:")
    assert ruta.read_text(encoding="utf-8") == contenido, "No se puede sobrescribir un fichero corrupto"


def test_app_es_la_unica_capa_con_entrada_y_salida():
    for modulo in (excepciones, modelos, modulo_gestor, almacen, informes):
        codigo = inspect.getsource(modulo)
        assert "input(" not in codigo and "print(" not in codigo, (
            f"{modulo.__name__} no puede usar input ni print"
        )


def test_app_sin_except_generico():
    for modulo in (app, modelos, modulo_gestor, almacen, informes):
        lineas = [linea.strip() for linea in inspect.getsource(modulo).splitlines()]
        assert "except:" not in lineas, f"{modulo.__name__}: no uses except: a secas"
        assert not any(linea.startswith("except Exception") for linea in lineas), (
            f"{modulo.__name__}: captura la excepción concreta, no Exception"
        )
