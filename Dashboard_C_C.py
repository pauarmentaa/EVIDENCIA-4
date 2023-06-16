# Librerías 
import pandas as pd 
import streamlit as st 
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard Calor y Control",
    page_icon="🔥",
    layout="wide")
# Título del Dasboard 
st.title("Dashboard Calor y Control 🔥")

# Datos a utilizar 
# Facturación 
# Cargar archivos a utilizar 
fac = pd.read_excel("Facturacion.xlsx", sheet_name="FACTURACION")
devo = pd.read_excel("Facturacion.xlsx", sheet_name="DEVOLUCIONES")
notas = pd.read_excel("Facturacion.xlsx", sheet_name="NOTAS DE CREDITO")
total_gastos = pd.read_csv("totalgastos.csv")
detalle = pd.read_csv("Detalle precios y productos fabricados 2022.csv")
# Procesamiento previo para KPI´s 
# Preprocesamiento Facturación 
# Agrupamos por fecha para obtener la cantidad total 
fac_group = fac[["FECHA_DOC", "CAN_TOT", "DES_TOT"]]
fac_group = fac_group.groupby("FECHA_DOC").sum()
fac_group = fac_group.reset_index()

# Preprocesamiento Devoluciones 
devo_group = devo[["FECHA_DOC", "CAN_TOT"]]
devo_group = devo_group.groupby("FECHA_DOC").sum()
devo_group = devo_group.reset_index()

# Procesamiento notas 
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
df_ingresos= df_ingresos.groupby(["FECHA_DOC", "Tipo"]).sum().reset_index()

# Cálculo de ingresos 
# Facturación 
fac_group_f_1 = fac_group_f
fac_group_f_1.rename(columns={"CAN_TOT": "FACT"}, inplace=True)
fac_group_f_1 = fac_group_f_1[["FACT", "FECHA_DOC"]]

# Descuentos 
fac_group_d_1 = fac_group_d
fac_group_d_1.rename(columns={"CAN_TOT": "DES"}, inplace=True)
fac_group_d_1 = fac_group_d_1[["DES", "FECHA_DOC"]]

# Devoluciones 
devo_group_1 = devo_group.copy()
devo_group_1.rename(columns={"CAN_TOT": "DEVO"}, inplace=True)
devo_group_1 = devo_group_1[["DEVO", "FECHA_DOC"]]

# Notas  
notas_group_1 = notas_group
notas_group_1.rename(columns={"CAN_TOT": "NOTAS"}, inplace=True)
notas_group_1 = notas_group_1[["NOTAS", "FECHA_DOC"]]
# Agrupamos 
ingresos_merge = fac_group_f_1.merge(fac_group_d_1, on='FECHA_DOC', how='outer').merge(devo_group_1, on='FECHA_DOC', how='outer').merge(notas_group_1, on='FECHA_DOC', how='outer')
# Procesamiento para gráfica de utilidad 
ingresos_merge_1 = ingresos_merge.copy()
ingresos_merge_2 = ingresos_merge.copy()

ingresos_merge_1['FECHA_DOC'] = ingresos_merge_1['FECHA_DOC'].dt.strftime('%m-%Y')
ingresos_full = ingresos_merge_1.groupby("FECHA_DOC").sum().reset_index()
ingresos_full["FECHA_DOC"] = pd.to_datetime(ingresos_full["FECHA_DOC"], format='%m-%Y')
# Procesamiento gráfica de Ingresos 
ingresos_graf = ingresos_merge_2.groupby("FECHA_DOC").sum().reset_index()
ingresos_graf["FECHA_DOC"] = pd.to_datetime(ingresos_graf["FECHA_DOC"])


# Calculemos los ingresos  gráfica utilidad
ingresos_full["Ingresos"] = ingresos_full["FACT"] - ingresos_full["DES"] - ingresos_full["DEVO"] + ingresos_full["NOTAS"]
ingresos_full["Ingresos"] = ingresos_full["FACT"] - ingresos_full["DES"] - ingresos_full["DEVO"] + ingresos_full["NOTAS"]

# Calculemos los ingresos gráfica ingresos
ingresos_graf["Ingresos"] = ingresos_graf["FACT"] + ingresos_graf["NOTAS"] - (ingresos_graf["DES"] - ingresos_graf["DEVO"])
#ingresos_graf["Ingresos"] = ingresos_graf["FACT"] - ingresos_graf["DES"] - ingresos_graf["DEVO"] + ingresos_graf["NOTAS"]

# Calculos egresos 
# Indicador egresos 
detalle_1 = detalle[["COSTO_TOTAL_CALCULADO", "FECHA_DOC"]]
detalle_1['COSTO_TOTAL_CALCULADO'] = detalle_1['COSTO_TOTAL_CALCULADO'].replace({'\$': '', ',': ''}, regex=True)
detalle_1["COSTO_TOTAL_CALCULADO"] =detalle_1["COSTO_TOTAL_CALCULADO"].astype(float)
detalle_1["FECHA_DOC"] = pd.to_datetime(detalle_1["FECHA_DOC"], format="%d/%m/%Y %H:%M")
detalle_group_1 = detalle_1.groupby("FECHA_DOC").sum().reset_index()

# Detalle de precios 
detalle = detalle[["COSTO_TOTAL_CALCULADO", "FECHA_DOC"]]
# Cambiar tipos de datos
# Nos deshacemos del signo $
detalle['COSTO_TOTAL_CALCULADO'] = detalle['COSTO_TOTAL_CALCULADO'].replace({'\$': '', ',': ''}, regex=True)
detalle["COSTO_TOTAL_CALCULADO"] =detalle["COSTO_TOTAL_CALCULADO"].astype(float)
detalle["FECHA_DOC"] = pd.to_datetime(detalle["FECHA_DOC"], format="%d/%m/%Y %H:%M")
detalle['FECHA_DOC'] = detalle['FECHA_DOC'].dt.strftime('%m-%Y')
detalle_group = detalle.groupby("FECHA_DOC").sum().reset_index()


# Preprocesamiento gráficas Gastos y Costos
# Gastos
totalgastos2 = total_gastos.copy()
GASTOS_FIN=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(["ARRENDAMIENTO FINANCIERO","COMISION BANCARIA","CREDITO"])]
GASTOS_ADMI=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(["ANTICIPO","CALIBRACIONES","ENERGIA ELECTRICA","GASTOS IMPORTACION","INSTALACION", "ELECTRICA","MAQUILAS","MAQUILAS GIC","MAQUINARIA","MTTO LOCAL","MTTO MAQUINARIA","PAQUETERIA","REPARACIONES ELECTRICAS","SUELDOS PRODUCCION"])]
GASTOS_ADMI.loc[GASTOS_ADMI['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.4
GASTOS_VENTAS=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(['CASETAS', 'COMBUSTIBLE', 'COMBUSTIBLE ', 'COMISION VENTA', 'COMPRA AUTO', 'GASOLINA', 'GERENCIA VTAS', 'HOSPEDAJE', 'HOSPEDAJE ', 'MTTO TRANSPORTE', 'PEAJES', 'SUELDOS VENTAS','VALES DESPENSA','IMSS/INFONAVIT','COMISION MIXTA','ATENCION CLIENTES'])]
GASTOS_VENTAS.loc[GASTOS_VENTAS['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.2
total_gastos_graf = pd.concat([GASTOS_FIN, GASTOS_ADMI, GASTOS_VENTAS])
total_gastos_graf["FECHA"] = pd.to_datetime(total_gastos_graf["FECHA"])
total_gastos_graf = total_gastos_graf.groupby("FECHA").sum().reset_index()

# Costos 
total_costos = total_gastos.copy()
costos = ['ANTICIPO', 'CALIBRACIONES', 'ENERGIA ELECTRICA', 'GASTOS IMPORTACION', 'INSTALACION ELECTRICA', 'MAQUILAS', 'MAQUILAS GIC', 'MAQUINARIA', 'MTTO LOCAL', 'MTTO MAQUINARIA', 'PAQUETERIA', 'REPARACIONES ELECTRICAS', 'SUELDOS PRODUCCION']
porcentaje_especial = {
        'COMISION MIXTA': 0.4,
        'IMSS/INFONAVIT': 0.4,
        'VALES DESPENSA': 0.4
    }

total_costos = total_costos[total_costos['TIPO GASTO'].isin(costos)]
total_costos['TOTAL MX'] = total_costos.apply(lambda row: row['TOTAL MX'] * porcentaje_especial[row['TIPO GASTO']] if row['TIPO GASTO'] in porcentaje_especial else row['TOTAL MX'], axis=1)
total_costos["FECHA"] = pd.to_datetime(total_costos["FECHA"])
total_costos = total_costos.groupby("FECHA").sum().reset_index()
# Unimos los costos con la materia prima 

total_costos = total_costos.rename(columns={'FECHA': 'FECHA_DOC'})
detalle_group["FECHA_DOC"] = pd.to_datetime(detalle_group["FECHA_DOC"])
costos_merge = total_costos.merge(detalle_group, on='FECHA_DOC', how ="outer")
costos_merge = costos_merge.fillna(0)
costos_merge["Total_costos"] = costos_merge["TOTAL MX"] + costos_merge["COSTO_TOTAL_CALCULADO"]

# Indicador de gastos
total_gastos_1 = total_gastos.copy()
total_gastos_1["FECHA"] = pd.to_datetime(total_gastos_1["FECHA"])
total_gastos_1.rename(columns={"FECHA": "FECHA_DOC"}, inplace=True)
total_gastos_1['IMPORTE'] = total_gastos_1['TOTAL MX'].abs()
total_gastos_1 = total_gastos_1[["FECHA_DOC", "TOTAL MX", "TIPO GASTO"]]
gastos_group_1 = total_gastos_1.groupby("FECHA_DOC").sum().reset_index()

total_gastos["FECHA"] = pd.to_datetime(total_gastos["FECHA"])
total_gastos.rename(columns={"FECHA": "FECHA_DOC"}, inplace=True)
# Convertimos los gastos a valores positivos 
total_gastos['IMPORTE'] = total_gastos['TOTAL MX'].abs()
total_gastos = total_gastos[["FECHA_DOC", "TOTAL MX"]]
total_gastos['FECHA_DOC'] = total_gastos['FECHA_DOC'].dt.strftime('%m-%Y')
gastos_group = total_gastos.groupby("FECHA_DOC").sum().reset_index()

# Gráfica Gastos y Costos 
costos_graf = costos_merge.copy()
costos_graf["Tipo"] = "Costos"
costos_graf["FECHA_DOC"] = pd.to_datetime(costos_graf["FECHA_DOC"])

gastos_graf = total_gastos_graf.copy()
gastos_graf = gastos_graf.rename(columns={'FECHA': 'FECHA_DOC'})
gastos_graf["Tipo"] = "Gastos"
gastos_graf["FECHA_DOC"] = pd.to_datetime(gastos_graf["FECHA_DOC"])
gastos_costos_merge = costos_graf.merge(gastos_graf, on=['FECHA_DOC', "Tipo", "TOTAL MX"], how ="outer")
#gastos_costos_merge = gastos_costos_merge.groupby(["FECHA_DOC", "Tipo"]).sum().reset_index()
gastos_costos_merge = gastos_costos_merge.fillna(0)

# Unificar formato de fechas
gastos_group["FECHA_DOC"] = pd.to_datetime(gastos_group["FECHA_DOC"])
detalle_group["FECHA_DOC"] = pd.to_datetime(detalle_group["FECHA_DOC"], format='%m-%Y')


# Unir dataframes de gastos 
egresos_merge = detalle_group.merge(gastos_group, on='FECHA_DOC', how ="outer")
egresos_merge = egresos_merge.fillna(0)
egresos_merge["Total_egresos"] = egresos_merge["COSTO_TOTAL_CALCULADO"] + egresos_merge["TOTAL MX"]


# Cáculo utilidad 
utilidad_merge = ingresos_full.merge(egresos_merge, on='FECHA_DOC', how ="outer")
#utilidad_group = utilidad_merge.groupby("FECHA_DOC").sum().reset_index()
utilidad_merge["Utilidad"] = utilidad_merge["Ingresos"] - utilidad_merge["Total_egresos"]
# Ordenar FECHA 
utilidad_merge = utilidad_merge.sort_values(by='FECHA_DOC')
utilidad_merge["FECHA_DOC"] = pd.to_datetime(utilidad_merge["FECHA_DOC"])
utilidad_merge = utilidad_merge.fillna(0)

# Mostrar el widget de entrada de fecha
start_date = pd.to_datetime(st.date_input("Fecha de inicio:"))
end_date = pd.to_datetime(st.date_input("Fecha de fin:"))

# Validar que la fecha de inicio sea menor que la fecha de fin

if start_date < end_date:
    # Filtrar el dataframe por el rango de fechas
    mask = (fac_group["FECHA_DOC"] > start_date) & (fac_group["FECHA_DOC"] <= end_date)
    fac_group = fac_group.loc[mask]
    # Filtrar el segundo dataframe por el rango de fechas
    mask2 = (ingresos_full["FECHA_DOC"] > start_date) & (ingresos_full["FECHA_DOC"] <= end_date)
    ingresos_full = ingresos_full.loc[mask2]
    # Filtrar gráfica de ingresos
    mask2_1 = (ingresos_graf["FECHA_DOC"] > start_date) & (ingresos_graf["FECHA_DOC"] <= end_date)
    ingresos_graf = ingresos_graf.loc[mask2_1]
    # Filtrar el tercer dataframe por el rango de fechas
    mask3 = (df_ingresos["FECHA_DOC"] > start_date) & (df_ingresos["FECHA_DOC"] <= end_date)
    df_ingresos = df_ingresos.loc[mask3]

    mask5 = (gastos_group["FECHA_DOC"] >= start_date) & (gastos_group["FECHA_DOC"] <= end_date)
    gastos_group = gastos_group[mask5]

    mask6 = (detalle_group["FECHA_DOC"] >= start_date) & (detalle_group["FECHA_DOC"] <= end_date)
    detalle_group = detalle_group[mask6]
    # Utilidad 
    mask7 = (utilidad_merge["FECHA_DOC"] >= start_date) & (utilidad_merge["FECHA_DOC"] <= end_date)
    utilidad_merge = utilidad_merge[mask7]
    # Detalle_1
    mask8 = (detalle_group_1["FECHA_DOC"] >= start_date) & (detalle_group_1["FECHA_DOC"] <= end_date)
    detalle_group_1 = detalle_group_1[mask8]
    # Gastos 1
    mask9= (gastos_group_1["FECHA_DOC"] >= start_date) & (gastos_group_1["FECHA_DOC"] <= end_date)
    gastos_group_1 = gastos_group_1[mask9]
    # Gráfica de gastos
    mask10= (total_gastos_graf["FECHA"] >= start_date) & (total_gastos_graf["FECHA"] <= end_date)
    total_gastos_graf = total_gastos_graf[mask10]
    # Gráfica de costos 
    mask11= (costos_merge["FECHA_DOC"] >= start_date) & (costos_merge["FECHA_DOC"] <= end_date)
    costos_merge = costos_merge[mask11]
    # Gráfica de pastel gastos vs costos 
    mask12= (gastos_costos_merge["FECHA_DOC"] >= start_date) & (gastos_costos_merge["FECHA_DOC"] <= end_date)
    gastos_costos_merge = gastos_costos_merge[mask12]

else:
    # Mostrar un mensaje de error
    st.error("Error: La fecha de fin debe ser mayor que la fecha de inicio.")


# Obtenemos la suma de la columna "Ingresos"
total_ingresos = ingresos_full["Ingresos"].sum()


# Crear primera fila de KPI´s
# Definimos una función que formatea el número con comas

def format_number_with_commas(number):
    return "{:,.2f}".format(number)

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    label="Utilidad 💸",
    value=format_number_with_commas(utilidad_merge["Ingresos"].sum() - utilidad_merge["Total_egresos"].sum())
)


kpi2.metric(
    label="Ingresos 🤑",
    value= format_number_with_commas(utilidad_merge["Ingresos"].sum())
)

kpi3.metric(
    label="Egresos 😥",
    value= format_number_with_commas(utilidad_merge["TOTAL MX"].sum() + utilidad_merge["COSTO_TOTAL_CALCULADO"].sum())
)
# utilidad_merge['TOTAL MX'].sum() + utilidad_merge["COSTO_TOTAL_CALCULADO"].sum()

# Gráficas
# Creamos 3 columnas 
fig_col1, fig_col2, fig_col3 = st.columns(3, gap="large")
#fig_col1, fig_col2, fig_col3 = st.columns([0.25, 0.5, 0.25])
with fig_col1:
    st.markdown("<h4 style='text-align: center'>Desglose de ingresos</h4>", unsafe_allow_html=True)
    fig = px.pie(df_ingresos, values='CAN_TOT', names='Tipo', color='Tipo', color_discrete_sequence=["#0e8a7e", "#006c6a", "#4ec8be", "#8efefe"],
              height=300, width=300)
    st.write(fig)
   
with fig_col2:
    st.markdown("<h4 style='text-align: center'>Ingresos</h4>", unsafe_allow_html=True)
    fig1 = px.line(ingresos_graf, x="FECHA_DOC", y="Ingresos", hover_data=['FECHA_DOC', 'Ingresos'], height=300, width=300)
    fig1.update_xaxes(title_text="Fecha")
    fig1.update_yaxes(title_text="Ingresos totales")
    fig1.update_traces(line_color="#0e8a7e")
    st.write(fig1)

with fig_col3:
    st.markdown("<h4 style='text-align: center'>Utilidad</h4>", unsafe_allow_html=True)
    fig3 = px.line(utilidad_merge, x="FECHA_DOC", y="Utilidad", hover_data=['FECHA_DOC', 'Utilidad'], height=300, width=300)
    fig3.update_xaxes(title_text="Fecha")
    fig3.update_yaxes(title_text="Utilidad")
    fig3.update_traces(line_color="#0e8a7e")
    st.write(fig3)

# Creamos otro contenedor con 3 columnas
fig_col4, fig_col5, fig_col6 = st.columns(3, gap="large")
#fig_col4, fig_col5, fig_col6 = st.columns([0.25, 0.5, 0.25])
with fig_col4:
    st.markdown("<h4 style='text-align: center'>Egresos</h4>", unsafe_allow_html=True)
    fig4 = px.pie(gastos_costos_merge, values='TOTAL MX', names='Tipo', color='Tipo', color_discrete_sequence=["#8a0e1a", "#bc4541"],
              height=300, width=300)
    st.write(fig4)

with fig_col5:
    st.markdown("<h4 style='text-align: center'>Gastos</h4>", unsafe_allow_html=True)
    fig5 = px.line(total_gastos_graf, x="FECHA", y="TOTAL MX", hover_data=['FECHA', 'TOTAL MX'], height=300, width=300)
    fig5.update_xaxes(title_text="Fecha")
    fig5.update_yaxes(title_text="Total Gastos")
    fig5.update_traces(line_color="#8a0e1a")
    st.write(fig5)

with fig_col6:
    st.markdown("<h4 style='text-align: center'>Costos</h4>", unsafe_allow_html=True)
    fig6 = px.line(costos_merge, x="FECHA_DOC", y="Total_costos", hover_data=['FECHA_DOC', 'Total_costos'], height=300, width=300)
    fig6.update_xaxes(title_text="Fecha")
    fig6.update_yaxes(title_text="Total Costos")
    fig6.update_traces(line_color="#8a0e1a")
    st.write(fig6)

utilidad_merge