import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from src.excepciones import ErrorFinanzas
from src.modelos import Gasto, Ingreso
from src.procesador import (
    analizar_estadisticas_numpy,
    cargar_cartera_desde_csv,
    clasificar_concepto,
    construir_dataframe,
    generar_diagnostico_ia,
)

# Configuracion general de la aplicacion web.
st.set_page_config(
    page_title="Mi Cartera | Control de Gastos",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Iconos que identifican visualmente las categorias en la interfaz.
ICONOS_CATEGORIA = {
    "Vivienda y Suministros": "🏠",
    "Alimentación": "🛒",
    "Transporte": "🚇",
    "Ocio y Suscripciones": "🎬",
    "Salud": "💊",
    "Ingresos": "💶",
    "Otros": "📌",
}

# --- BARRA LATERAL ---
# El panel lateral reúne las entradas principales: movimientos manuales,
# objetivo de ahorro y carga de un extracto CSV.
with st.sidebar:
    st.title("💳 Mi Cartera")
    st.caption("Tu control de gastos diario")

    st.subheader("➕ Apuntar movimiento")
    with st.form("form_nuevo_movimiento", clear_on_submit=True):
        concepto_nuevo = st.text_input("¿En qué has gastado o ingresado?", placeholder="Ej. Compra Mercadona")
        col_imp, col_tipo = st.columns([1.2, 1])
        importe_nuevo = col_imp.number_input("Importe (€)", min_value=0.01, step=5.0, value=15.0)
        tipo_nuevo = col_tipo.selectbox(
            "Tipo", ["gasto", "ingreso"], format_func=lambda x: "Gasto" if x == "gasto" else "Ingreso"
        )
        fecha_nueva = st.date_input("Fecha")

        # Al enviar el formulario, valida el concepto, clasifica el movimiento,
        # crea el modelo correspondiente y lo conserva en la sesion de Streamlit.
        if st.form_submit_button("Guardar", type="primary", use_container_width=True):
            if concepto_nuevo.strip():
                try:
                    cat = clasificar_concepto(concepto_nuevo)
                    mov = (
                        Ingreso(str(fecha_nueva), concepto_nuevo, importe_nuevo, cat)
                        if tipo_nuevo == "ingreso"
                        else Gasto(str(fecha_nueva), concepto_nuevo, importe_nuevo, cat)
                    )
                    st.session_state.cartera.agregar(mov)
                    st.success(f"Guardado en {ICONOS_CATEGORIA.get(cat, '📌')} {cat}")
                except ErrorFinanzas as e:
                    st.error(str(e))
            else:
                st.warning("Escribe un concepto antes de guardar.")

    st.divider()
    objetivo_ahorro = st.slider("🎯 Meta de ahorro (€)", min_value=50, max_value=2000, value=300, step=50)

    st.divider()
    archivo_subido = st.file_uploader("📂 Importar extracto (.csv)", type=["csv"])

# Detectamos cambios en el origen de datos para importar el archivo solo cuando
# se selecciona uno nuevo. Si no se sube un CSV, se carga el fichero por defecto.
origen_actual = archivo_subido.name if archivo_subido is not None else "por_defecto"

# La cartera se conserva en session_state entre reejecuciones. Ante un error de
# lectura se muestra el motivo y se detiene la pagina para evitar datos parciales.
if "cartera" not in st.session_state or st.session_state.get("origen_datos") != origen_actual:
    try:
        origen = archivo_subido if archivo_subido is not None else "datos/movimientos.csv"
        st.session_state.cartera = cargar_cartera_desde_csv(origen)
        st.session_state.origen_datos = origen_actual
    except ErrorFinanzas as e:
        st.error(f"No se pudo leer el archivo: {e}")
        st.stop()

# --- PREPARACION DE DATOS Y FILTRO POR PERIODO ---
# Transformamos la cartera en un DataFrame y añadimos una etiqueta año-mes
# para que el usuario pueda analizar todos los datos o un mes concreto.
cartera = st.session_state.cartera
df_completo = construir_dataframe(cartera)
df_completo["mes"] = df_completo["fecha"].dt.strftime("%Y-%m")

# --- CABECERA Y SELECTOR DE PERIODO ---
col_tit, col_mes = st.columns([3, 1])
col_tit.header("Resumen financiero")
meses_disponibles = ["Todos los meses"] + sorted(df_completo["mes"].unique().tolist(), reverse=True)
mes_elegido = col_mes.selectbox("Periodo", meses_disponibles)

# Aplicamos el periodo seleccionado sobre una copia de los datos. Cuando se
# elige un mes, el saldo acumulado se recalcula dentro de ese mes.
if mes_elegido == "Todos los meses":
    df = df_completo.copy()
else:
    df = df_completo[df_completo["mes"] == mes_elegido].copy().reset_index(drop=True)
    df["balance_acumulado"] = df["impacto"].cumsum()

# Las métricas se calculan siempre sobre el periodo visible.
stats = analizar_estadisticas_numpy(df)
balance_periodo = round(float(df["impacto"].sum()), 2)

# --- KPIs SUPERIORES ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Saldo del periodo", f"{balance_periodo:,.2f} €")
c2.metric("Ingresos", f"{stats['total_ingresos']:,.2f} €")
c3.metric("Gastos", f"{stats['total_gastos']:,.2f} €")

# La diferencia con la meta indica cuánto se ha superado o cuánto falta.
dif_meta = balance_periodo - objetivo_ahorro
c4.metric(
    "Meta de ahorro",
    f"{objetivo_ahorro:,.0f} €",
    delta=f"{dif_meta:+,.2f} € vs meta",
)

# La barra representa el avance hacia la meta y se limita al rango 0–100 %.
progreso = max(0.0, min(balance_periodo / objetivo_ahorro, 1.0)) if objetivo_ahorro > 0 else 1.0
porcentaje_meta = int(progreso * 100)
st.progress(progreso, text=f"Progreso hacia tu meta de ahorro ({objetivo_ahorro:,.0f} €): **{porcentaje_meta}%**")

# Si hay gastos inusuales, destacamos el de mayor importe.
if not stats["anomalos"].empty:
    mayor = stats["anomalos"].sort_values("importe", ascending=False).iloc[0]
    st.info(
        f"💡 **Aviso:** Se ha detectado un gasto puntual más alto de lo habitual en **{mayor['concepto']}** ({mayor['importe']:.2f} €)."
    )

st.write("")

# --- PESTAÑAS PRINCIPALES ---
# Separamos el análisis gráfico, el historial filtrable y las recomendaciones.
tab_resumen, tab_movimientos, tab_consejos = st.tabs(
    ["📊 ¿En qué se va mi dinero?", "🧾 Últimos movimientos", "✨ Consejos de ahorro"]
)

with tab_resumen:
    # Agrupamos los gastos por categoría para alimentar los dos gráficos.
    gastos_df = df[df["tipo"] == "gasto"].copy()
    por_cat = gastos_df.groupby("categoria")["importe"].sum().sort_values(ascending=True)
    colores_suaves = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#64748B"]

    # Distribuimos el desglose por categoría en dos gráficos comparativos.
    col_izq, col_der = st.columns([1.15, 1])

    with col_izq:
        st.subheader("Gasto por categoría")
        fig1, ax1 = plt.subplots(figsize=(6.5, 4), facecolor="white")
        ax1.set_facecolor("white")

        # Las barras comparan importes; se simplifica el eje y se muestran
        # etiquetas con la cantidad exacta al final de cada una.
        barras = ax1.barh(por_cat.index, por_cat.values, color="#3B82F6", height=0.55)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["left"].set_color("#CBD5E1")
        ax1.xaxis.set_visible(False)
        ax1.tick_params(axis="y", labelsize=10, colors="#1E293B")

        max_val = por_cat.max() if not por_cat.empty else 100
        ax1.set_xlim(0, max_val * 1.24)

        for barra in barras:
            ancho = barra.get_width()
            ax1.text(
                ancho + (max_val * 0.02),
                barra.get_y() + barra.get_height() / 2,
                f"{ancho:,.2f} €",
                va="center",
                ha="left",
                fontsize=9.5,
                fontweight="bold",
                color="#334155",
            )

        plt.tight_layout()
        st.pyplot(fig1)

    with col_der:
        # El gráfico de anillo muestra la proporción de cada categoría y el
        # total gastado en el centro.
        st.subheader("Reparto del gasto")
        por_cat_desc = por_cat.sort_values(ascending=False)
        fig2, ax2 = plt.subplots(figsize=(5.5, 4), facecolor="white")
        ax2.set_facecolor("white")

        wedges, texts, autotexts = ax2.pie(
            por_cat_desc.values,
            labels=por_cat_desc.index,
            autopct="%1.0f%%",
            startangle=90,
            colors=colores_suaves[: len(por_cat_desc)],
            pctdistance=0.78,
            wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 2.5},
        )

        for t in texts:
            t.set_fontsize(9.5)
            t.set_color("#334155")
        for at in autotexts:
            at.set_fontsize(8.5)
            at.set_fontweight("bold")
            at.set_color("white")

        ax2.text(
            0,
            0,
            f"Total gastado\n{stats['total_gastos']:,.0f} €",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color="#0F172A",
        )
        plt.tight_layout()
        st.pyplot(fig2)

    # El gráfico temporal muestra la evolución del balance y la meta de ahorro.
    st.subheader("Evolución de tu saldo")
    fig3, ax3 = plt.subplots(figsize=(11, 2.8), facecolor="white")
    ax3.set_facecolor("white")

    ax3.plot(df["fecha"], df["balance_acumulado"], color="#10B981", linewidth=2.5, marker="o", markersize=4.5)
    ax3.fill_between(df["fecha"], df["balance_acumulado"], color="#10B981", alpha=0.10)

    ax3.axhline(objetivo_ahorro, color="#F59E0B", linestyle="--", linewidth=1.5, label=f"Meta de ahorro ({objetivo_ahorro} €)")

    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_color("#CBD5E1")
    ax3.spines["bottom"].set_color("#CBD5E1")
    ax3.tick_params(colors="#475569", labelsize=8.5)
    ax3.grid(axis="y", linestyle=":", alpha=0.5, color="#CBD5E1")
    ax3.legend(frameon=False, loc="upper right", fontsize=9)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig3)

with tab_movimientos:
    # En esta pestaña se puede filtrar el historial por categoría y por texto,
    # y descargar exactamente los resultados que quedan visibles.
    col_f1, col_f2, col_f3 = st.columns([1, 1.5, 0.8])

    categorias_disp = ["Todas"] + sorted(list(cartera.categorias_unicas()))
    filtro_cat = col_f1.selectbox("Filtrar por categoría", categorias_disp)
    busqueda = col_f2.text_input("Buscar movimiento", placeholder="Escribe Mercadona, Netflix, Nómina...")

    df_vista = df.sort_values("fecha", ascending=False).copy()

    if filtro_cat != "Todas":
        df_vista = df_vista[df_vista["categoria"] == filtro_cat]

    if busqueda.strip():
        df_vista = df_vista[df_vista["concepto"].str.contains(busqueda, case=False, na=False)]

    # Preparamos la descarga en CSV con fechas ISO y construimos aparte una
    # tabla más cómoda de leer en pantalla.
    csv_exportar = df_vista[["fecha", "concepto", "importe", "tipo"]].copy()

    csv_exportar["fecha"] = csv_exportar["fecha"].dt.strftime("%Y-%m-%d")
    col_f3.write("")

    col_f3.download_button(
        label="📥 Exportar CSV",
        data=csv_exportar.to_csv(index=False).encode("utf-8"),
        file_name="mis_movimientos.csv",
        mime="text/csv",
        use_container_width=True,
    )

    df_limpio = pd.DataFrame({
        "Fecha": df_vista["fecha"].dt.strftime("%d/%m/%Y"),
        "Concepto": df_vista["concepto"],
        "Categoría": df_vista["categoria"].map(lambda c: f"{ICONOS_CATEGORIA.get(c, '📌')} {c}"),
        "Importe": df_vista.apply(
            lambda r: f"+{r['importe']:,.2f} €" if r["tipo"] == "ingreso" else f"-{r['importe']:,.2f} €",
            axis=1,
        ),
    })

    st.dataframe(df_limpio, use_container_width=True, hide_index=True)

with tab_consejos:
    # El informe se genera bajo demanda con los datos del periodo y la meta
    # seleccionados, y puede mostrarse y descargarse en formato Markdown.
    st.write("Obtén un resumen personalizado de tus hábitos de gasto y recomendaciones para llegar a tu meta.")

    if st.button("Analizar mis gastos", type="primary"):
        informe = generar_diagnostico_ia(df, stats, objetivo_ahorro)

        st.markdown(informe)

        st.download_button(
            label="Descargar resumen",
            data=informe,
            file_name="resumen_mensual.md",
            mime="text/markdown",
        )