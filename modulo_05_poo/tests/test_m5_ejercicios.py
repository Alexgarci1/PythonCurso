"""Tests de los ejercicios del módulo 5."""

import dataclasses
import inspect

import pytest

import m5_ej1_clases as ej1
import m5_ej2_metodos as ej2
import m5_ej3_herencia as ej3
import m5_ej4_polimorfismo as ej4
import m5_ej5_encapsulacion as ej5
import m5_ej6_dataclasses as ej6


# ---------------------------------------------------------------- Ejercicio 1
def test_ej1_rectangulo_atributos():
    rectangulo = ej1.Rectangulo(3, 4)
    assert (rectangulo.base, rectangulo.altura) == (3, 4)


def test_ej1_rectangulo_area_y_perimetro():
    assert ej1.Rectangulo(3, 4).area() == 12
    assert ej1.Rectangulo(3, 4).perimetro() == 14
    assert ej1.Rectangulo(2.5, 2).area() == 5.0


def test_ej1_rectangulo_es_cuadrado():
    assert ej1.Rectangulo(3, 3).es_cuadrado() is True
    assert ej1.Rectangulo(3, 4).es_cuadrado() is False


def test_ej1_rectangulo_escalar_devuelve_uno_nuevo():
    original = ej1.Rectangulo(3, 4)
    doble = original.escalar(2)
    assert isinstance(doble, ej1.Rectangulo)
    assert (doble.base, doble.altura) == (6, 8)
    assert (original.base, original.altura) == (3, 4), "El original no puede cambiar"
    assert doble is not original


def test_ej1_objetos_independientes():
    a = ej1.Rectangulo(1, 1)
    b = ej1.Rectangulo(5, 5)
    a.base = 10
    assert b.base == 5


def test_ej1_contador():
    contador = ej1.Contador()
    assert contador.valor == 0
    assert [contador.incrementar(), contador.incrementar(), contador.incrementar()] == [1, 2, 3]
    assert contador.valor == 3


def test_ej1_contador_inicio_y_paso():
    contador = ej1.Contador(10, paso=5)
    assert contador.incrementar() == 15
    assert contador.incrementar() == 20
    contador.reiniciar()
    assert contador.valor == 10
    assert contador.incrementar() == 15


def test_ej1_contadores_independientes():
    uno, otro = ej1.Contador(), ej1.Contador()
    uno.incrementar()
    uno.incrementar()
    assert otro.incrementar() == 1


def test_ej1_tarea():
    tarea = ej1.Tarea("  Comprar pan ")
    assert tarea.titulo == "Comprar pan"
    assert tarea.completada is False
    assert tarea.etiquetas == []
    assert tarea.resumen() == "[ ] Comprar pan"
    tarea.completar()
    assert tarea.completada is True
    assert tarea.resumen() == "[x] Comprar pan"


def test_ej1_tarea_etiquetar():
    tarea = ej1.Tarea("Informe", ["trabajo"])
    tarea.etiquetar("Urgente")
    tarea.etiquetar("urgente")
    tarea.etiquetar("TRABAJO")
    assert tarea.etiquetas == ["trabajo", "urgente"]


def test_ej1_tareas_no_comparten_etiquetas():
    a = ej1.Tarea("a")
    b = ej1.Tarea("b")
    a.etiquetar("casa")
    assert b.etiquetas == [], "Las dos tareas comparten la misma lista de etiquetas"


def test_ej1_tarea_no_modifica_la_lista_recibida():
    etiquetas = ["trabajo"]
    tarea = ej1.Tarea("Informe", etiquetas)
    tarea.etiquetar("urgente")
    assert etiquetas == ["trabajo"]


# ---------------------------------------------------------------- Ejercicio 2
def test_ej2_dinero_constructor():
    dinero = ej2.Dinero(12.345)
    assert dinero.cantidad == 12.35 or dinero.cantidad == 12.34
    assert ej2.Dinero(12.5).cantidad == 12.5
    assert dinero.moneda == "EUR"
    assert ej2.Dinero(5, "USD").moneda == "USD"


def test_ej2_dinero_es_moneda_valida():
    assert ej2.Dinero.es_moneda_valida("EUR") is True
    assert ej2.Dinero.es_moneda_valida("GBP") is True
    assert ej2.Dinero.es_moneda_valida("XXX") is False
    assert isinstance(inspect.getattr_static(ej2.Dinero, "es_moneda_valida"), staticmethod)


def test_ej2_dinero_desde_texto():
    dinero = ej2.Dinero.desde_texto("12.50 EUR")
    assert isinstance(dinero, ej2.Dinero)
    assert (dinero.cantidad, dinero.moneda) == (12.5, "EUR")
    assert ej2.Dinero.desde_texto("  7 USD ").moneda == "USD"
    assert isinstance(inspect.getattr_static(ej2.Dinero, "desde_texto"), classmethod)


def test_ej2_dinero_desde_texto_funciona_en_subclases():
    class Euros(ej2.Dinero):
        pass

    assert type(Euros.desde_texto("1 EUR")) is Euros, "Usa cls(...) y no Dinero(...)"


def test_ej2_dinero_repr_y_str():
    dinero = ej2.Dinero(12.5)
    assert repr(dinero) == "Dinero(12.5, 'EUR')"
    assert str(dinero) == "12.50 EUR"
    assert f"{ej2.Dinero(3, 'USD')}" == "3.00 USD"
    assert str([ej2.Dinero(1)]) == "[Dinero(1, 'EUR')]"


def test_ej2_dinero_igualdad():
    assert ej2.Dinero(5) == ej2.Dinero(5)
    assert ej2.Dinero(5) != ej2.Dinero(6)
    assert ej2.Dinero(5, "EUR") != ej2.Dinero(5, "USD")
    assert ej2.Dinero(5) != 5
    assert ej2.Dinero(5).__eq__("5 EUR") is NotImplemented


def test_ej2_dinero_orden_y_suma():
    assert ej2.Dinero(2) < ej2.Dinero(5)
    assert not ej2.Dinero(5) < ej2.Dinero(2)
    cantidades = [ej2.Dinero(5), ej2.Dinero(2), ej2.Dinero(9)]
    assert [d.cantidad for d in sorted(cantidades)] == [2, 5, 9]
    assert max(cantidades) == ej2.Dinero(9)
    a, b = ej2.Dinero(0.1), ej2.Dinero(0.2)
    suma = a + b
    assert suma == ej2.Dinero(0.3)
    assert suma is not a and a.cantidad == 0.1
    assert sum(cantidades, ej2.Dinero(0)) == ej2.Dinero(16)


def test_ej2_playlist_coleccion():
    lista = ej2.Playlist("Rock")
    assert len(lista) == 0
    lista.anadir("Thunderstruck")
    lista.anadir("Paranoid")
    assert len(lista) == 2
    assert "Paranoid" in lista
    assert "paranoid" in lista
    assert "Hey Jude" not in lista
    assert list(lista) == ["Thunderstruck", "Paranoid"]
    assert [cancion.upper() for cancion in lista] == ["THUNDERSTRUCK", "PARANOID"]
    assert lista[0] == "Thunderstruck"
    assert lista[-1] == "Paranoid"
    assert str(lista) == "Rock (2 canciones)"


def test_ej2_playlist_listas_independientes():
    a, b = ej2.Playlist("a"), ej2.Playlist("b")
    a.anadir("x")
    assert len(b) == 0


def test_ej2_playlist_creadas():
    antes = ej2.Playlist.creadas
    uno = ej2.Playlist("uno")
    ej2.Playlist("dos")
    assert ej2.Playlist.creadas == antes + 2
    assert uno.creadas == antes + 2
    assert "creadas" not in vars(uno), "creadas es de la clase: usa Playlist.creadas += 1"


# ---------------------------------------------------------------- Ejercicio 3
def test_ej3_empleado_es_abstracta():
    with pytest.raises(TypeError):
        ej3.Empleado("Ada")


def test_ej3_jerarquia():
    assert issubclass(ej3.Fijo, ej3.Empleado)
    assert issubclass(ej3.PorHoras, ej3.Empleado)
    assert issubclass(ej3.Comercial, ej3.Fijo)
    assert not issubclass(ej3.PorHoras, ej3.Fijo)


def test_ej3_fijo():
    ada = ej3.Fijo("Ada", 36000)
    assert ada.nombre == "Ada"
    assert ada.salario_anual == 36000
    assert ada.salario_mensual() == 3000.0
    assert ej3.Fijo("x", 40000).salario_mensual() == 3333.33


def test_ej3_por_horas():
    linus = ej3.PorHoras("Linus", 100, 20)
    assert (linus.nombre, linus.horas, linus.tarifa) == ("Linus", 100, 20)
    assert linus.salario_mensual() == 2000
    assert ej3.PorHoras("x", 10.5, 15.5).salario_mensual() == 162.75


def test_ej3_comercial():
    grace = ej3.Comercial("Grace", 24000, ventas=10000)
    assert (grace.nombre, grace.salario_anual, grace.ventas, grace.comision) == (
        "Grace", 24000, 10000, 5,
    )
    assert grace.salario_mensual() == 2500.0
    assert ej3.Comercial("x", 24000, 10000, comision=10).salario_mensual() == 3000.0
    assert ej3.Comercial("x", 24000, 0).salario_mensual() == 2000.0


def test_ej3_comercial_reutiliza_el_calculo_de_fijo(monkeypatch):
    monkeypatch.setattr(ej3.Fijo, "salario_mensual", lambda self: 1000.0)
    assert ej3.Comercial("Grace", 24000, ventas=10000).salario_mensual() == 1500.0, (
        "Comercial tiene que llamar a super().salario_mensual()"
    )


def test_ej3_subclases_usan_super_init():
    for clase in (ej3.Fijo, ej3.PorHoras, ej3.Comercial):
        assert "super().__init__" in inspect.getsource(clase.__init__), (
            f"{clase.__name__}.__init__ tiene que llamar a super().__init__"
        )


def test_ej3_descripcion():
    assert ej3.Fijo("Ada", 36000).descripcion() == "Ada (Fijo): 3000.00 €"
    assert ej3.PorHoras("Linus", 100, 20).descripcion() == "Linus (PorHoras): 2000.00 €"
    assert ej3.Comercial("Grace", 24000, 10000).descripcion() == "Grace (Comercial): 2500.00 €"
    assert "descripcion" not in vars(ej3.Fijo), "descripcion se hereda: no la repitas"


def test_ej3_coste_mensual_y_mejor_pagado():
    plantilla = [
        ej3.Fijo("Ada", 36000),
        ej3.PorHoras("Linus", 100, 20),
        ej3.Comercial("Grace", 24000, 30000),
    ]
    assert ej3.coste_mensual(plantilla) == 8500.0
    assert ej3.coste_mensual([]) == 0
    assert ej3.mejor_pagado(plantilla).nombre == "Grace"
    assert ej3.mejor_pagado(plantilla[:2]).nombre == "Ada"
    assert ej3.mejor_pagado([]) is None


def test_ej3_funciona_con_una_subclase_nueva():
    class Directivo(ej3.Empleado):
        def salario_mensual(self):
            return 9000.0

    jefa = Directivo("Barbara")
    assert jefa.descripcion() == "Barbara (Directivo): 9000.00 €"
    assert ej3.coste_mensual([jefa, ej3.Fijo("Ada", 12000)]) == 10000.0


# ---------------------------------------------------------------- Ejercicio 4
REGISTROS = [{"id": 1, "nombre": "Ada"}, {"id": 2, "nombre": "Linus"}]


class ExportadorDePrueba:
    """Un exportador que los alumnos no han visto: no hereda de nada."""

    extension = "prueba"

    def exportar(self, registros):
        return f"{len(registros)} registros"


def test_ej4_sin_clase_base_comun():
    for clase in (ej4.ExportadorCsv, ej4.ExportadorTexto, ej4.ExportadorMarkdown):
        assert clase.__bases__ == (object,), "Los exportadores no heredan de ninguna clase"


def test_ej4_extensiones():
    assert ej4.ExportadorCsv.extension == "csv"
    assert ej4.ExportadorTexto.extension == "txt"
    assert ej4.ExportadorMarkdown.extension == "md"


def test_ej4_csv():
    assert ej4.ExportadorCsv().exportar(REGISTROS) == "id;nombre\n1;Ada\n2;Linus"
    assert ej4.ExportadorCsv().exportar([]) == ""


def test_ej4_texto():
    assert ej4.ExportadorTexto().exportar(REGISTROS) == "id=1, nombre=Ada\nid=2, nombre=Linus"
    assert ej4.ExportadorTexto().exportar([]) == ""


def test_ej4_markdown():
    assert ej4.ExportadorMarkdown().exportar(REGISTROS) == (
        "| id | nombre |\n| --- | --- |\n| 1 | Ada |\n| 2 | Linus |"
    )
    assert ej4.ExportadorMarkdown().exportar([]) == ""


def test_ej4_exportar_con():
    assert ej4.exportar_con(ej4.ExportadorCsv(), REGISTROS).startswith("id;nombre")
    assert ej4.exportar_con(ExportadorDePrueba(), REGISTROS) == "2 registros"


def test_ej4_nombre_de_fichero():
    assert ej4.nombre_de_fichero(ej4.ExportadorCsv(), "ventas") == "ventas.csv"
    assert ej4.nombre_de_fichero(ej4.ExportadorMarkdown(), "informe") == "informe.md"
    assert ej4.nombre_de_fichero(ExportadorDePrueba(), "x") == "x.prueba"


def test_ej4_exportar_a_todos():
    resultado = ej4.exportar_a_todos(
        [ej4.ExportadorCsv(), ej4.ExportadorTexto(), ExportadorDePrueba()], REGISTROS
    )
    assert list(resultado) == ["csv", "txt", "prueba"]
    assert resultado["prueba"] == "2 registros"
    assert resultado["txt"].count("\n") == 1
    assert ej4.exportar_a_todos([], REGISTROS) == {}


def test_ej4_puede_exportar():
    class ConAtributoQueNoEsMetodo:
        exportar = "no soy un método"

    assert ej4.puede_exportar(ej4.ExportadorCsv()) is True
    assert ej4.puede_exportar(ExportadorDePrueba()) is True
    assert ej4.puede_exportar("texto") is False
    assert ej4.puede_exportar(None) is False
    assert ej4.puede_exportar(ConAtributoQueNoEsMetodo()) is False


@pytest.mark.parametrize(
    "nombre", ["exportar_con", "nombre_de_fichero", "exportar_a_todos", "puede_exportar"]
)
def test_ej4_sin_comprobar_tipos(nombre):
    codigo = inspect.getsource(getattr(ej4, nombre))
    cuerpo = codigo.split('"""')[-1]
    assert "isinstance" not in cuerpo and "type(" not in cuerpo, (
        f"{nombre} no puede comprobar el tipo del exportador"
    )


# ---------------------------------------------------------------- Ejercicio 5
def test_ej5_cuenta_inicial():
    cuenta = ej5.CuentaBancaria("Ada")
    assert cuenta.titular == "Ada"
    assert cuenta.saldo == 0
    assert cuenta.movimientos == ()
    assert ej5.CuentaBancaria("Linus", 100).saldo == 100
    with pytest.raises(ValueError):
        ej5.CuentaBancaria("x", -1)


def test_ej5_cuenta_operaciones():
    cuenta = ej5.CuentaBancaria("Ada", 50)
    cuenta.ingresar(100)
    cuenta.retirar(30)
    assert cuenta.saldo == 120
    assert cuenta.movimientos == (100, -30)
    cuenta.retirar(120)
    assert cuenta.saldo == 0


@pytest.mark.parametrize("importe", [0, -5])
def test_ej5_cuenta_importes_no_validos(importe):
    cuenta = ej5.CuentaBancaria("Ada", 50)
    with pytest.raises(ValueError):
        cuenta.ingresar(importe)
    with pytest.raises(ValueError):
        cuenta.retirar(importe)
    assert cuenta.saldo == 50
    assert cuenta.movimientos == ()


def test_ej5_cuenta_saldo_insuficiente():
    cuenta = ej5.CuentaBancaria("Ada", 50)
    with pytest.raises(ValueError):
        cuenta.retirar(50.01)
    assert cuenta.saldo == 50


def test_ej5_cuenta_saldo_solo_lectura():
    cuenta = ej5.CuentaBancaria("Ada", 50)
    assert isinstance(inspect.getattr_static(ej5.CuentaBancaria, "saldo"), property)
    with pytest.raises(AttributeError):
        cuenta.saldo = 1_000_000
    with pytest.raises(AttributeError):
        cuenta.movimientos = ()


def test_ej5_cuenta_movimientos_protegidos():
    cuenta = ej5.CuentaBancaria("Ada")
    cuenta.ingresar(10)
    assert isinstance(cuenta.movimientos, tuple)
    otra = ej5.CuentaBancaria("Linus")
    assert otra.movimientos == ()


def test_ej5_producto():
    teclado = ej5.Producto("Teclado", 100)
    assert teclado.nombre == "Teclado"
    assert teclado.precio == 100
    assert teclado.precio_con_iva == 121.0
    teclado.precio = 50
    assert teclado.precio == 50
    assert teclado.precio_con_iva == 60.5
    assert ej5.Producto("Gratis", 0).precio_con_iva == 0


def test_ej5_producto_validacion():
    teclado = ej5.Producto("Teclado", 100)
    with pytest.raises(ValueError):
        teclado.precio = -1
    assert teclado.precio == 100
    with pytest.raises(ValueError):
        ej5.Producto("Malo", -5)
    with pytest.raises(AttributeError):
        teclado.precio_con_iva = 10


def test_ej5_producto_usa_el_iva_de_la_clase(monkeypatch):
    monkeypatch.setattr(ej5.Producto, "IVA", 10)
    assert ej5.Producto("Libro", 100).precio_con_iva == 110.0


def test_ej5_temperatura():
    temperatura = ej5.Temperatura()
    assert temperatura.celsius == 0
    assert temperatura.fahrenheit == 32.0
    assert ej5.Temperatura(100).fahrenheit == 212.0
    assert ej5.Temperatura(-40).fahrenheit == -40.0
    assert ej5.Temperatura(36.6).fahrenheit == 97.88


def test_ej5_temperatura_setters():
    temperatura = ej5.Temperatura(20)
    temperatura.fahrenheit = 212
    assert temperatura.celsius == 100.0
    temperatura.celsius = 0
    assert temperatura.fahrenheit == 32.0
    temperatura.fahrenheit = 98.6
    assert temperatura.celsius == 37.0


def test_ej5_temperatura_cero_absoluto():
    with pytest.raises(ValueError):
        ej5.Temperatura(-300)
    temperatura = ej5.Temperatura(20)
    with pytest.raises(ValueError):
        temperatura.celsius = -273.16
    with pytest.raises(ValueError):
        temperatura.fahrenheit = -500
    assert temperatura.celsius == 20
    assert ej5.Temperatura(-273.15).celsius == -273.15


# ---------------------------------------------------------------- Ejercicio 6
def test_ej6_son_dataclasses():
    for nombre in ("Punto", "LineaPedido", "Pedido"):
        assert dataclasses.is_dataclass(getattr(ej6, nombre)), f"{nombre} no es una dataclass"


def test_ej6_punto():
    assert ej6.Punto() == ej6.Punto(0.0, 0.0)
    punto = ej6.Punto(3, 4)
    assert (punto.x, punto.y) == (3, 4)
    assert punto == ej6.Punto(3, 4)
    assert ej6.Punto().distancia(punto) == 5.0
    assert punto.distancia(ej6.Punto(4, 5)) == 1.41
    assert repr(punto) == "Punto(x=3, y=4)"


def test_ej6_punto_inmutable():
    punto = ej6.Punto(1, 2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        punto.x = 5
    assert {punto: "a"}[ej6.Punto(1, 2)] == "a"


def test_ej6_linea_pedido():
    linea = ej6.LineaPedido("Teclado", 2, 45.0)
    assert (linea.producto, linea.unidades, linea.precio) == ("Teclado", 2, 45.0)
    assert linea.importe == 90.0
    assert ej6.LineaPedido("x", 3, 0.1).importe == 0.3
    assert linea == ej6.LineaPedido("Teclado", 2, 45.0)
    assert isinstance(inspect.getattr_static(ej6.LineaPedido, "importe"), property)


@pytest.mark.parametrize("unidades", [0, -1])
def test_ej6_linea_pedido_unidades_no_validas(unidades):
    with pytest.raises(ValueError):
        ej6.LineaPedido("Teclado", unidades, 45.0)


def test_ej6_pedido():
    pedido = ej6.Pedido(1042, "Ada")
    assert (pedido.numero, pedido.cliente, pedido.lineas) == (1042, "Ada", [])
    assert pedido.total == 0
    assert len(pedido) == 0
    linea = pedido.anadir("Teclado", 2, 45.0)
    assert linea == ej6.LineaPedido("Teclado", 2, 45.0)
    pedido.anadir("Ratón", 1, 19.9)
    pedido.anadir("Teclado", 1, 45.0)
    assert len(pedido) == 3
    assert pedido.total == 154.9
    assert pedido.productos() == ["Ratón", "Teclado"]
    assert isinstance(inspect.getattr_static(ej6.Pedido, "total"), property)


def test_ej6_pedidos_no_comparten_lineas():
    a = ej6.Pedido(1, "Ada")
    b = ej6.Pedido(2, "Linus")
    a.anadir("Teclado", 1, 45.0)
    assert len(b) == 0
    assert a.lineas is not b.lineas


def test_ej6_pedido_rechaza_lineas_no_validas():
    pedido = ej6.Pedido(1, "Ada")
    with pytest.raises(ValueError):
        pedido.anadir("Teclado", 0, 45.0)
    assert len(pedido) == 0
