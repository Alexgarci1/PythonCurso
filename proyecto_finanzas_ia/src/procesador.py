# Importamos NumPy para realizar operaciones vectorizadas sobre arrays numericos.
import numpy as np

# Pandas permite leer CSV, transformar datos y representar las transacciones
# como tablas bidimensionales.
import pandas as pd

# Esta excepcion indica que un archivo no tiene la estructura esperada.
from src.excepciones import ErrorFormatoArchivo

# Los modelos representan la cartera completa y cada tipo de movimiento.
from src.modelos import Cartera, Gasto, Ingreso

# Diccionario usado por la clasificacion automatica de conceptos.
# La clave es el nombre de la categoria y la lista contiene palabras clave
# que permiten reconocer un concepto sin depender de espacios o mayusculas.
REGLAS_CATEGORIAS: dict[str, list[str]] = {
    "Vivienda y Suministros": ["alquiler", "luz", "agua", "gas", "internet", "iberdrola"],
    "Alimentación": ["mercadona", "carrefour", "lidl", "supermercado", "cafe", "restaurante", "cena"],
    "Transporte": ["metro", "abono", "gasolina", "repsol", "uber", "coche", "taller", "averia"],
    "Ocio y Suscripciones": ["netflix", "spotify", "cine", "gimnasio", "amazon"],
    "Salud": ["farmacia", "medico", "dentista"],
    "Ingresos": ["nomina", "clase", "venta", "devolucion"],
}


def clasificar_concepto(concepto: str) -> str:
    """Asigna una categoria a un texto describiendo un movimiento.

    Convierte el concepto a minusculas y busca si contiene alguna palabra clave.
    Por ejemplo, "Compra Lidl" coincide con "lidl" y se clasifica como
    "Alimentacion". Si no coincide ninguna regla, se usa "Otros".
    """
    # .lower() normaliza el texto para que la busqueda no dependa de mayusculas.
    texto = concepto.lower()

    # Recorremos todas las categorias, desde la mas concreta hasta "Otros".
    for categoria, palabras in REGLAS_CATEGORIAS.items():
        # any() devuelve True si al menos una palabra esta dentro del texto.
        if any(palabra in texto for palabra in palabras):
            return categoria

    # Categoria segura cuando no existe una coincidencia conocida.
    return "Otros"


def cargar_cartera_desde_csv(ruta_o_buffer) -> Cartera:
    """Carga un archivo CSV y lo convierte en objetos Cartera y transacciones.

    Cada fila del CSV representa una operacion. La funcion valida primero las
    columnas necesarias, clasifica el concepto y crea un Gasto o un Ingreso
    segun el valor de la columna "tipo".
    """
    # pd.read_csv acepta tanto rutas de archivo como objetos tipo buffer.
    # Pandas crea automaticamente un DataFrame con una fila por movimiento.
    df = pd.read_csv(ruta_o_buffer)

    # Definimos las columnas obligatorias. Sin ellas no podemos construir
    # transacciones validas ni continuar con el analisis.
    columnas_requeridas = {"fecha", "concepto", "importe", "tipo"}
    if not columnas_requeridas.issubset(set(df.columns)):
        raise ErrorFormatoArchivo(f"El CSV debe contener: {columnas_requeridas}")

    # Creamos una cartera vacia y la iremos rellenando fila a fila.
    cartera = Cartera()

    # iterrows() recorre el DataFrame y entrega el indice y una Serie con
    # los valores de cada fila. Se usa "_" porque el indice no es necesario.
    for _, fila in df.iterrows():
        # Convertimos concepto a texto antes de clasificarlo por si Pandas
        # interpreta el dato como otro tipo.
        categoria = clasificar_concepto(str(fila["concepto"]))

        # Normalizamos el tipo: quitamos espacios externos y lo pasamos a
        # minusculas para aceptar valores como "Ingreso" o " ingreso ".
        tipo = str(fila["tipo"]).strip().lower()

        # Solo "ingreso" crea un objeto Ingreso. Cualquier otro tipo se trata
        # como gasto para mantener la cartera util incluso con variantes distintas.
        if tipo == "ingreso":
            mov = Ingreso(str(fila["fecha"]), str(fila["concepto"]), float(fila["importe"]), categoria)
        else:
            mov = Gasto(str(fila["fecha"]), str(fila["concepto"]), float(fila["importe"]), categoria)

        # El metodo agregar mantiene todas las transacciones dentro de la cartera.
        cartera.agregar(mov)
    return cartera


def construir_dataframe(cartera: Cartera) -> pd.DataFrame:
    """Convierte una cartera en un DataFrame ordenado y preparado para graficar.

    Cada transaccion se transforma en un diccionario con sus propiedades.
    Luego se crean columnas derivadas que permiten calcular el balance diario
    acumulado y distinguir ingresos de gastos.
    """
    # a_diccionario() proporciona las columnas base de cada movimiento.
    datos = [t.a_diccionario() for t in cartera.transacciones]
    df = pd.DataFrame(datos)
    if df.empty:
        return df

    # Convertimos las cadenas de fecha a tipos datetime reales. Esto permite
    # ordenarlas cronologicamente y usarlas correctamente en los graficos.
    df["fecha"] = pd.to_datetime(df["fecha"])

    # Ordenamos por fecha ascendente y reiniciamos el indice, que comienza
    # nuevamente en cero despues de haber eliminado el orden original.
    df = df.sort_values("fecha").reset_index(drop=True)

    # np.where crea una columna vectorizada:
    # - ingreso: suma su importe
    # - gasto: resta su importe
    df["impacto"] = np.where(df["tipo"] == "ingreso", df["importe"], -df["importe"])

    # cumsum() suma secuencialmente el impacto de cada movimiento.
    # El resultado representa el saldo acumulado despues de cada operacion.
    df["balance_acumulado"] = df["impacto"].cumsum()
    return df


def analizar_estadisticas_numpy(df: pd.DataFrame) -> dict:
    """Calcula ingresos, gastos y posibles gastos anomalos.

    Se separan primero los gastos de los ingresos. Con los importes de gasto
    se calcula la media y la desviacion tipica mediante NumPy. Un gasto se
    considera anomalo cuando supera la media mas 1,5 desviaciones tipicas.
    """
    # Aplicamos un filtro booleano: solo conservamos las filas cuyo tipo es gasto.
    gastos = df[df["tipo"] == "gasto"]
    if gastos.empty:
        return {
            "total_ingresos": 0.0,
            "total_gastos": 0.0,
            "media_gasto": 0.0,
            "umbral_anomalia": 0.0,
            "anomalos": pd.DataFrame(),
        }

    # Extraemos los importes como un array de NumPy para aprovechar sus
    # operaciones numericas vectorizadas y obtener mejores resultados.
    valores = gastos["importe"].to_numpy()
    media = float(np.mean(valores))

    # std calcula la desviacion tipica poblacional del conjunto de gastos.
    desviacion = float(np.std(valores))

    # Esta regla marca como anomalo un gasto claramente superior al conjunto
    # habitual. El factor 1.5 hace el limite menos estricto que usar 2 o 3.
    umbral = media + 1.5 * desviacion

    # Copiamos los gastos que superan el umbral para evitar modificar el
    # DataFrame original al utilizarlo posteriormente en la interfaz.
    anomalos = gastos[gastos["importe"] > umbral].copy()
    return {
        # sum() suma todos los importes de las filas cuyo tipo sea ingreso.
        "total_ingresos": round(float(df[df["tipo"] == "ingreso"]["importe"].sum()), 2),
        # valores.sum() suma directamente el array NumPy de gastos.
        "total_gastos": round(float(valores.sum()), 2),
        "media_gasto": round(media, 2),
        "umbral_anomalia": round(umbral, 2),
        "anomalos": anomalos,
    }


def generar_diagnostico_ia(df: pd.DataFrame, stats: dict, objetivo_ahorro: float) -> str:
    """Genera un informe Markdown con recomendaciones basadas en datos reales.

    Agrupa los gastos por categoria, identifica la categoria con mayor importe,
    compara los ahorros actuales con la meta introducida por el usuario y usa
    las estadisticas NumPy para explicar posibles gastos inusuales.
    """
    # Filtramos los gastos, agrupamos por categoria y sumamos sus importes.
    # sort_values(..., ascending=False) coloca la categoria mas costosa primero.
    gastos_cat = df[df["tipo"] == "gasto"].groupby("categoria")["importe"].sum().sort_values(ascending=False)

    # Si existen gastos, obtenemos su categoria principal y su importe total.
    # Si no existen, usamos valores neutros para que el informe siga funcionando.
    top_cat = gastos_cat.index[0] if not gastos_cat.empty else "N/A"
    top_val = float(gastos_cat.iloc[0]) if not gastos_cat.empty else 0.0

    # El ahorro actual es la diferencia entre todo lo ingresado y todo gastado.
    ahorro_actual = stats["total_ingresos"] - stats["total_gastos"]

    # Una diferencia positiva indica que se ha superado la meta.
    # Una diferencia negativa indica cuanto falta todavia para alcanzarla.
    diferencia = ahorro_actual - objetivo_ahorro

    # Creamos un primer bloque de Markdown que cambia segun si se cumple la meta.
    # El operador ternario permite elegir un mensaje distinto dentro de una sola expresion.
    estado_meta = (
        f"✅ **Objetivo cumplido:** Superas tu meta de ahorro en **{diferencia:,.2f} €**."
        if diferencia >= 0
        else f"⚠️ **Atención a tu meta:** Te faltan **{abs(diferencia):,.2f} €** para alcanzar tu objetivo de **{objetivo_ahorro:,.0f} €**."
    )

    # Devolvemos varias frases con formato Markdown. Los guiones crean una lista
    # y los dobles asteriscos muestran numeros o conceptos destacados en negrita.
    # Los separadores con comas de ,.2f permiten mostrar valores con miles y
    # dos decimales; el ultimo consejo calcula una simulacion de ahorro del 15 %.
    return (
        f"### Diagnóstico de tus Finanzas\n"
        f"- {estado_meta}\n"
        f"- **Mayor foco de gasto:** La categoría **{top_cat}** concentra **{top_val:,.2f} €** del total gastado.\n"
        f"- **Control de gastos puntuales (NumPy):** Tu gasto medio por operación es de **{stats['media_gasto']:,.2f} €** "
        f"y se han detectado **{len(stats['anomalos'])} gastos inusuales** por encima de **{stats['umbral_anomalia']:,.2f} €**.\n"
        f"- **Consejo práctico:** Si reduces un 15 % el gasto en *{top_cat}*, ahorrarías **{(top_val * 0.15):,.2f} €** adicionales."
    )