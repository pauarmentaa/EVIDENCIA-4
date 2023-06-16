# Librerías 
import pandas as pd 
import streamlit as st 
import plotly.express as px
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(
    page_title="Ingresos",
    page_icon="💸",
    layout="wide")
# Título del Dasboard 
st.title("Ingresos 💸")


# Facturación 
# Cargar archivos a utilizar 
df = px.data.gapminder().query("country == 'Mexico'")
fac = pd.read_excel("Facturacion.xlsx", sheet_name="FACTURACION")
devo = pd.read_excel("Facturacion.xlsx", sheet_name="DEVOLUCIONES")
notas = pd.read_excel("Facturacion.xlsx", sheet_name="NOTAS DE CREDITO")

# Preprocesamiento Facturación 
# Agrupamos por fecha para obtener la cantidad total 
fac_group = fac[["FECHA_DOC", "CAN_TOT", "DES_TOT", "CVE_VEND"]]
fac_group = fac_group.groupby("FECHA_DOC").sum()
fac_group = fac_group.reset_index()

# Preprocesamiento Devoluciones 
# Preprocesamiento Devoluciones 
devo_group = devo[["FECHA_DOC", "CAN_TOT"]]
devo_group = devo_group.groupby("FECHA_DOC").sum()
devo_group = devo_group.reset_index()

# Procesamiento Notas de crédito 
notas_group = notas[["FECHA_DOC", "CAN_TOT"]]
notas_group = notas_group.groupby("FECHA_DOC").sum()
notas_group = notas_group.reset_index()

# Procesamiento gráfica de pastel 
# Facturación 
fac_group_f = fac_group[["FECHA_DOC","CAN_TOT"]]
# Formato fechas 
fac_group_f["FECHA_DOC"] = pd.to_datetime(fac_group_f["FECHA_DOC"])
fac_group_f["Tipo"] = "Facturación"

# Descuentos 
fac_group_d = fac_group[["FECHA_DOC","DES_TOT"]]
fac_group_d["Tipo"] = "Descuento"
fac_group_d["CAN_TOT"] = fac_group_d["DES_TOT"]
fac_group_d = fac_group_d[["FECHA_DOC","CAN_TOT", "Tipo"]]
# Devoluciones 
devo_group_2 = devo_group[["FECHA_DOC","CAN_TOT"]]
devo_group_2["Tipo"] = "Devolucion"
# Notas 
notas_group_2 = notas_group[["FECHA_DOC","CAN_TOT"]]
notas_group_2["Tipo"] = "Notas"

# Unión de dataframes 
# Los concatenas verticalmente con axis=0
dfs = [fac_group_f, fac_group_d, devo_group_2, notas_group_2]
df_ingresos = pd.concat(dfs, axis=0)
df_ingresos["FECHA_DOC"] = pd.to_datetime(df_ingresos["FECHA_DOC"])

# Desempeño por vendedor 
fac_group_1 = fac[["FECHA_DOC", "CAN_TOT", "DES_TOT", "CVE_VEND"]]
vendedores = {1: "Alfredo Canela", 2: "Leticia Ramírez", 3: "Diego Armando", 5: "Atención C" , 6: "Aaron Nulo"}
fac_group_1["CVE_VEND"] = fac_group_1["CVE_VEND"].map(vendedores)
# Eliminar los valores que no se encuentren en el diccionario
fac_group_1 = fac_group_1.dropna()

# Mostrar el widget de entrada de fecha
start_date = pd.to_datetime(st.date_input("Fecha de inicio:"))
end_date = pd.to_datetime(st.date_input("Fecha de fin:"))

# Validar que la fecha de inicio sea menor que la fecha de fin
if start_date < end_date:
    # Filtrar el dataframe por el rango de fechas
    # Facturación / Descuentos
    mask = (fac_group["FECHA_DOC"] > start_date) & (fac_group["FECHA_DOC"] <= end_date)
    fac_group = fac_group.loc[mask]
    # Devoluciones 
    mask1 = (devo_group["FECHA_DOC"] > start_date) & (devo_group["FECHA_DOC"] <= end_date)
    devo_group = devo_group.loc[mask1]
    # Notas de crédito 
    mask2 = (notas_group["FECHA_DOC"] > start_date) & (notas_group["FECHA_DOC"] <= end_date)
    notas_group = notas_group.loc[mask2]
    # DF_ingresos
    # Filtrar el tercer dataframe por el rango de fechas
    mask3 = (df_ingresos["FECHA_DOC"] > start_date) & (df_ingresos["FECHA_DOC"] <= end_date)
    df_ingresos = df_ingresos.loc[mask3]
    # Desempeño por vendedor
    # Filtrar el tercer dataframe por el rango de fechas
    mask4 = (fac_group_1["FECHA_DOC"] > start_date) & (fac_group_1["FECHA_DOC"] <= end_date)
    fac_group_1 = fac_group_1.loc[mask4]



else:
    # Mostrar un mensaje de error
    st.error("Error: La fecha de fin debe ser mayor que la fecha de inicio.")

# Preprocesamiento para KPI´s 
# Facturación 
total_fac = fac_group["CAN_TOT"].sum()
# Descuentos 
total_des = fac_group["DES_TOT"].sum()
# Devoluciones
total_devo = devo_group["CAN_TOT"].sum()
# Notas de crédito 
total_notas = notas_group["CAN_TOT"].sum()


# KPI´S 
# Crear primera fila de KPI´s
# Definimos una función que formatea el número con comas
def format_number_with_commas(number):
    return "{:,.2f}".format(number)
# create three columns
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    label="Facturación",
    value= format_number_with_commas(total_fac),
)


kpi2.metric(
    label="Descuentos",
    value= format_number_with_commas(total_des)
)

kpi3.metric(
    label="Devoluciones",
    value= format_number_with_commas(total_devo)
)

kpi4.metric(
    label="Notas de crédito",
    value = format_number_with_commas(total_notas)
)


# Gráficas
# Creamos 3 columnas 
fig_col1, fig_col2, fig_col3 = st.columns(3, gap="large")
with fig_col1:
    st.markdown("<h4 style='text-align: center'>Desglose de ingresos</h4>", unsafe_allow_html=True)
    fig = px.pie(df_ingresos, values='CAN_TOT', names='Tipo', color='Tipo', color_discrete_sequence=["#0e8a7e", "#006c6a", "#4ec8be", "#8efefe"],
              height=300, width=300)
    st.write(fig)
with fig_col2:
    st.markdown("<h4 style='text-align: center'>Descuentos</h4>", unsafe_allow_html=True)
    fig2 = px.line(fac_group, x="FECHA_DOC", y="DES_TOT", hover_data=['FECHA_DOC', 'DES_TOT'], height=300, width=300)
    fig2.update_xaxes(title_text="Fecha")
    fig2.update_yaxes(title_text="Descuento total")
    fig2.update_traces(line_color="#0e8a7e")
    fig2.update_layout(width=400)
    st.write(fig2)
with fig_col3:
    st.markdown("<h4 style='text-align: center'>Devoluciones</h4>", unsafe_allow_html=True)
    fig3 = px.line(devo_group, x="FECHA_DOC", y="CAN_TOT", hover_data=['FECHA_DOC', 'CAN_TOT'], height=300, width=300)
    fig3.update_xaxes(title_text="Fecha")
    fig3.update_yaxes(title_text="Devoluciones totales")
    fig3.update_traces(line_color="#0e8a7e")
    st.write(fig3)

# Creamos otro contenedor con 3 columnas
fig_col4, fig_col5, fig_col6 = st.columns(3, gap="large")
with fig_col4:
    st.markdown("<h4 style='text-align: center'>Facturación</h4>", unsafe_allow_html=True)
    fig4 = px.line(fac_group, x="FECHA_DOC", y="CAN_TOT", hover_data=['FECHA_DOC', 'CAN_TOT'], height=300, width=500)
    fig4.update_traces(line_color="#0e8a7e")
    fig4.update_xaxes(title_text="Fecha")
    fig4.update_yaxes(title_text="Cantidad facturada")
    # Crear una figura con la línea de tendencia
    fig7 = px.scatter(fac_group, x="FECHA_DOC", y="CAN_TOT", trendline="expanding")
    # Agregar la traza de la línea de tendencia a la figura original
    fig4.add_trace(go.Scatter(x=fig7.data[1].x, y=fig7.data[1].y, mode="lines", name="Tendencia"))
    st.write(fig4)

with fig_col5:
    st.markdown("<h4 style='text-align: center'>Notas de crédito</h4>", unsafe_allow_html=True)
    fig5 = px.line(notas_group, x="FECHA_DOC", y="CAN_TOT", hover_data=['FECHA_DOC', 'CAN_TOT'], height=300, width=300)
    fig5.update_xaxes(title_text="Fecha")
    fig5.update_yaxes(title_text="Notas de crédito emitidas")
    fig5.update_traces(line_color="#0e8a7e")
    st.write(fig5)

with fig_col6:
    st.markdown("<h4 style='text-align: center'>Facturación por vendedor</h4>", unsafe_allow_html=True)
    fig6 = fig = px.pie(fac_group_1, values='CAN_TOT', names='CVE_VEND', color='CVE_VEND', color_discrete_sequence=["#006c6a", "#002c2a", "#0e8a7e", "#4ec8be", "#8efefe", "#cfffff"] , height=300, width=300)
    st.write(fig6)