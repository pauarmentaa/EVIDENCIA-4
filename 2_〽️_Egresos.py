# Librerías 
import pandas as pd 
import streamlit as st 
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(
    page_title="Egresos",
    page_icon="〽️",
    layout="wide")
# Título del Dasboard 
st.title("Egresos 〽️")

totalgastos=pd.read_csv("totalgastos.csv")
totalgastos2 = totalgastos.copy()

# Subpágina de Gastos
if st.sidebar.selectbox("Sección", ["Gastos", "Costos"]) == "Gastos":
    # Código para la subpágina de Gastos
    st.header("Gastos")

    #TOTALES DE TIPO GASTO
    # Mostrar el widget de entrada de fecha
    start_date = pd.to_datetime(st.date_input("Fecha de inicio:"))
    end_date = pd.to_datetime(st.date_input("Fecha de fin:"))

    # Validar que la fecha de inicio sea menor que la fecha de fin
    if start_date < end_date:
       # Filtrar el dataframe por el rango de fechas
       totalgastos2["FECHA"] = pd.to_datetime(totalgastos2["FECHA"])
       mask = (totalgastos2["FECHA"] > start_date) & (totalgastos2["FECHA"] <= end_date)
       totalgastos2 = totalgastos2.loc[mask]

    else:
       # Mostrar un mensaje de error
       st.error("Error: La fecha de fin debe ser mayor que la fecha de inicio.")

    # Crear primera fila de KPI´s
    # Definimos una función que formatea el número con comas
    def format_number_with_commas(number):
        return "{:,.2f}".format(number)
    

    # create 4 columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # Filtrar el DataFrame y aplicar cálculos

    GASTOS_FIN=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(["ARRENDAMIENTO FINANCIERO","COMISION BANCARIA","CREDITO"])]
    GASTOS_ADMI=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(["ANTICIPO","CALIBRACIONES","ENERGIA ELECTRICA","GASTOS IMPORTACION","INSTALACION", "ELECTRICA","MAQUILAS","MAQUILAS GIC","MAQUINARIA","MTTO LOCAL","MTTO MAQUINARIA","PAQUETERIA","REPARACIONES ELECTRICAS","SUELDOS PRODUCCION"])]
    GASTOS_ADMI.loc[GASTOS_ADMI['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.4

    GASTOS_VENTAS=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(['CASETAS', 'COMBUSTIBLE', 'COMBUSTIBLE ', 'COMISION VENTA', 'COMPRA AUTO', 'GASOLINA', 'GERENCIA VTAS', 'HOSPEDAJE', 'HOSPEDAJE ', 'MTTO TRANSPORTE', 'PEAJES', 'SUELDOS VENTAS','VALES DESPENSA','IMSS/INFONAVIT','COMISION MIXTA','ATENCION CLIENTES'])]
    GASTOS_VENTAS.loc[GASTOS_VENTAS['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.2

    total = pd.concat([GASTOS_FIN, GASTOS_ADMI, GASTOS_VENTAS])['TOTAL MX'].sum()

    kpi1.metric(
        label="Total de Gastos",
        value=format_number_with_commas(total))
    
    kpi2.metric(
        label="Gastos de Ventas",
        value= format_number_with_commas(GASTOS_VENTAS['TOTAL MX'].sum()))

    kpi3.metric(
        label="Gastos de Administracion",
        value= format_number_with_commas(GASTOS_FIN['TOTAL MX'].sum()))
    
    kpi4.metric(
        label="Gastos de Financiamiento",
        value= format_number_with_commas(GASTOS_ADMI['TOTAL MX'].sum()))
    
    # **GASTOS DE VENTAS*
    GASTOS_VENTAS=totalgastos.loc[totalgastos['TIPO GASTO'].isin(['CASETAS', 'COMBUSTIBLE', 'COMBUSTIBLE ', 'COMISION VENTA', 'COMPRA AUTO', 'GASOLINA', 'GERENCIA VTAS', 'HOSPEDAJE', 'HOSPEDAJE ', 'MTTO TRANSPORTE', 'PEAJES', 'SUELDOS VENTAS','VALES DESPENSA','IMSS/INFONAVIT','COMISION MIXTA','ATENCION CLIENTES'])]
    GASTOS_VENTAS.loc[GASTOS_VENTAS['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.2
    #GRAF1
    st.markdown("<h4 style='text-align: center'> Gastos y costos 2020 al 2023 </h4>", unsafe_allow_html=True)
    fig = px.bar(totalgastos, x='FECHA', y='TOTAL MX',hover_name='TIPO GASTO',color="TOTAL MX", height=400, width=1500)
    fig.update_layout(xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1 año",
                     step="year",
                     stepmode="backward"),
                     dict(count=3,
                          label="3 años",
                          step="year",
                          stepmode="backward"),
                          dict(count=5,
                               label="5 años",
                               step="year",
                               stepmode="backward"),
                               dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ))
    fig

    #GRAF2
    # Crear el gráfico con los datos originales y agregar un título
    st.title("Gastos de ventas")
    st.markdown("<h4 style='text-align: center'> Gastos 2020 al 2023 </h4>", unsafe_allow_html=True)
    fig = px.bar(GASTOS_VENTAS, x='FECHA', y='TOTAL MX', color="TIPO GASTO", hover_name='PROVEEDOR', height=400, width=1500)
    # Agregar la suma de la columna TOTAL MX al lado del título del gráfico
    fig.update_layout(
        title={
            'text': 'Gastos de Ventas 20-23<br><span style="font-size: 14px;">Total: $' + str(GASTOS_VENTAS['TOTAL MX'].sum()) + '</span>',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1 año",
                             step="year",
                             stepmode="backward"),
                        dict(count=3,
                             label="3 años",
                             step="year",
                             stepmode="backward"),
                        dict(count=5,
                             label="5 años",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
    )
    fig

    #GRAF 3
    # Agrupar los datos por "TIPO GASTO" y sumar los valores de "TOTAL MX"
    df_grouped = GASTOS_VENTAS.groupby('TIPO GASTO')['TOTAL MX'].sum().reset_index()
    # Ordenar los resultados por "IMPORTE" y seleccionar solo los 4 tipos de gastos más altos
    df_top4 = df_grouped.nlargest(6, 'TOTAL MX')
    # Filtrar el dataframe original para incluir solo los 4 tipos de gastos más altos
    GASTOS_VENTAS_top4 = GASTOS_VENTAS[GASTOS_VENTAS['TIPO GASTO'].isin(df_top4['TIPO GASTO'])]
    # Crear el gráfico con solo los 4 tipos de gastos más altos y agregar un título
    st.markdown("<h4 style='text-align: center'> Distribución por gasto de ventas </h4>", unsafe_allow_html=True)
    fig = px.histogram(GASTOS_VENTAS_top4, x='FECHA', y='TOTAL MX', hover_name='PROVEEDOR', color='TIPO GASTO',
                       facet_col='TIPO GASTO', height=400, width=2000)

    fig.update_xaxes(tickangle=90)
    fig.update_layout(xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1 año",
                     step="year",
                     stepmode="backward"),
                dict(count=2,
                     label="2 años",
                     step="year",
                     stepmode="backward"),
                dict(count=3,
                     label="3 años",
                     step="year",
                     stepmode="backward"),
                dict(count=5,
                     label="5 años",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ) ,
    height=600,
    width=1200
    )
    fig
    # **GASTOS ADMINISTRATIVOS**
    st.title("Gastos administrativos")
    #Verificar los valores sin repetirse de una columna
    unico = np.unique(totalgastos['TIPO GASTO'])

    #Convierto una variable a dicotómica 
    totalgastos['TIPO GASTO']= totalgastos['TIPO GASTO'].replace(['FLETE'], 'FLETES')
    totalgastos['TIPO GASTO']= totalgastos['TIPO GASTO'].replace(['UNIFORME'], 'UNIFORMES')
    totalgastos['TIPO GASTO']= totalgastos['TIPO GASTO'].replace(['MTT OFICINA'], 'MTTO OFICINA')

    #COPIA EN LA QUE VAMOS A TRABAJAR
    totalgastos_copia = totalgastos.copy()
    # Filtrar las filas correspondientes a las variables deseadas y ajustar el valor de 'TOTAL MX' al 40%
    totalgastos_copia.loc[totalgastos_copia['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.4

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['HONORARIOS ADMON','HONORARIOS CONTABLES','HONORARIOS JURIDICOS','HONORARIOS PF','HONORARIOS PM'], "ASESORES Y HONORARIOS EXTERNOS")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['COMISION MIXTA','GERENCIA ADMON'], "BONIFICACIONES")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['DERECHOS','IMSS/INFONAVIT'], "COSTOS PATRONALES")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['ALIMENTOS', 'BOTIQUIN',
       'FLETES','MEDICOS', 'MENSAJERIA',
       'MOBILIARIO', 'MONITOREO CAMARAS ADT',
       'NO DEDUCIBLE','PUBLICIDAD', 'SANITIZACION', 
       'SEGUROS', 'SERV FUNERARIO', 'SUBCONTRATOS',
       'SUSCRIPCIONES', 'TRANSPORTE',
       'UNIFORMES', 'VALES DESPENSA','VARIOS'], "GASTOS VARIOS Y NO DEDUCIBLES")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['ARRENDAMIENTO LOCAL','MTTO OFICINA ',
                                                                          'RENTA AUTO', 'RENTA COPIADORA',
                                                                          'RENTA OFICINA '], "RENTA")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['CAPACITACION'], "RH")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['COMPRA COMPUTADORA ','COMPRA TABLET ',
                                                                          'MTTO COMPUTO', 'MTTO EQUIPO COMPUTO',], "SISTEMAS")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['SUELDOS DIRECCION'], "SUELDOS")

    totalgastos_copia['TIPO GASTO']= totalgastos_copia['TIPO GASTO'].replace(['TELEFONO'], "TELEFONIA")

    #Verificar los valores sin repetirse de una columna
    unico2 = np.unique(totalgastos_copia['TIPO GASTO'])

    #CONOCEMOS TODOS LOS GASTOS ADMINISTRATIVOS
    admin = ['ASESORES Y HONORARIOS EXTERNOS', 'BONIFICACIONES', 
         'COSTOS PATRONALES', 'GASTOS VARIOS Y NO DEDUCIBLES',
         'PAPELERIA', 'RENTA', 'RH', 'SISTEMAS','SUELDOS','TELEFONIA']

    # Filtrar los datos para las categorías de administración
    filtered_data = totalgastos_copia[totalgastos_copia['TIPO GASTO'].isin(admin)]
    # Convertir la columna 'FECHA' a tipo datetime
    filtered_data['FECHA'] = pd.to_datetime(filtered_data['FECHA'])
    # Extraer el año de la columna 'FECHA' y crear la columna 'Año'
    filtered_data['Año'] = filtered_data['FECHA'].dt.year
    # Calcular el total de cada categoría por año
    category_totals = filtered_data.groupby(['Año', 'TIPO GASTO'])['TOTAL MX'].sum().reset_index()
    #GRAF1
    st.markdown("<h4 style='text-align: center'> Distribución de gastos administrativos por categoría y año </h4>", unsafe_allow_html=True)
    fig = px.sunburst(category_totals, path=['Año', 'TIPO GASTO'], values='TOTAL MX',
                  color='Año', height=1000, width=1000)
    fig
    #GRAF2
    st.markdown("<h4 style='text-align: center'> Evolución de gastos administrativos por categoría y año </h4>", unsafe_allow_html=True)
    fig4 = px.area(category_totals, x='Año', y='TOTAL MX', color='TIPO GASTO', height=400, width=1500)
    fig4

    # **GASTOS FINANCIEROS**
    st.title("Gastos financieros")
    gastos = totalgastos.copy()
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['ARRENDAMIENTO FINANCIERO'], "ARRENDAMIENTO FINANCIERO")
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['COMISION BANCARIA'], "COMISION BANCARIA")
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['CREDITO '], "CREDITO")
    # GRAFICAMOS
    finanzas = ['ARRENDAMIENTO FINANCIERO','COMISION BANCARIA','CREDITO']
    op = gastos[gastos['TIPO GASTO'].isin(finanzas)]
    op['FECHA'] = pd.to_datetime(op['FECHA'])
    op['Año'] = op['FECHA'].dt.year
    total = op.groupby(['Año', 'TIPO GASTO'])['TOTAL MX'].sum().reset_index()

    st.markdown("<h4 style='text-align: center'> Gastos financieros por año </h4>", unsafe_allow_html=True)
    fin = px.sunburst(total, path=['Año','TIPO GASTO'], values='TOTAL MX',
                  color='Año', height=1000, width=1000)

    fin

    #GRAFICO 2
    st.markdown("<h4 style='text-align: center'> Evolución de gastos financieros por categoría y año</h4>", unsafe_allow_html=True)
    fin2 = px.area(total, x='Año', y='TOTAL MX', color="TIPO GASTO", height=400, width=1500)
    fin2

else:
    # Código para la subpágina de Costos
    st.header("Costos")
    # Mostrar el widget de entrada de fecha
    start_date = pd.to_datetime(st.date_input("Fecha de inicio:"))
    end_date = pd.to_datetime(st.date_input("Fecha de fin:"))

    # Validar que la fecha de inicio sea menor que la fecha de fin
    if start_date < end_date:
       # Filtrar el dataframe por el rango de fechas
       totalgastos2["FECHA"] = pd.to_datetime(totalgastos2["FECHA"])
       mask = (totalgastos2["FECHA"] > start_date) & (totalgastos2["FECHA"] <= end_date)
       totalgastos2 = totalgastos2.loc[mask]

    else:
       # Mostrar un mensaje de error
       st.error("Error: La fecha de fin debe ser mayor que la fecha de inicio.")

    # Crear primera fila de KPI´s
    # Definimos una función que formatea el número con comas
    def format_number_with_commas(number):
        return "{:,.2f}".format(number)
    

    # create 4 columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    #DF DE MATERIA PRIMA
    MATERIA_PRIMA=pd.read_csv("Detalle precios y productos fabricados 2022.csv")
    MATERIA_PRIMA['COSTO_TOTAL_CALCULADO'] = MATERIA_PRIMA['COSTO_TOTAL_CALCULADO'].replace({'\$': '', ',': ''}, regex=True)
    MATERIA_PRIMA["COSTO_TOTAL_CALCULADO"] =MATERIA_PRIMA["COSTO_TOTAL_CALCULADO"].astype(float)
    EQUI=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(['CALIBRACIONES','MTTO MAQUINARIA','MTTO LOCAL','REPARACIONES ELECTRICAS','INSTALACION ELECTRICA'])]

    GASTOS_OPE=totalgastos2['TIPO GASTO']= totalgastos2['TIPO GASTO'].replace(['PAQUETERIA'], "PAQUETERIA")
    GASTOS_OPE=totalgastos2['TIPO GASTO']= totalgastos2['TIPO GASTO'].replace(['UNIFORME','UNIFORMES'], "UNIFORMES Y EQUIPO")
    GASTOS_OPE=totalgastos2['TIPO GASTO']= totalgastos2['TIPO GASTO'].replace(['ENERGIA ELECTRICA','SUELDOS PRODUCCION','COMISION MIXTA','IMSS/INFONAVIT','VALES DESPENSA'], "VARIOS")
    GASTOS_OPE=totalgastos2.loc[totalgastos2['TIPO GASTO'].isin(['PAQUETERIA','UNIFORMES Y EQUIPO','VARIOS'])]
    GASTOS_OPE.loc[GASTOS_OPE['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.4

    MATERIALES = MATERIA_PRIMA['COSTO_TOTAL_CALCULADO'].sum()
    

    total_cos = pd.concat([EQUI, GASTOS_OPE])['TOTAL MX'].sum() + MATERIALES
    
    kpi1.metric(
        label="Total de Costos",
        value=format_number_with_commas(total_cos))
    
    kpi2.metric(
        label="Total de Materiales",
        value= format_number_with_commas(MATERIALES))

    kpi3.metric(
        label="Gastos de Gastos Operativos",
        value=format_number_with_commas(GASTOS_OPE['TOTAL MX'].sum()))
  
    kpi4.metric(
        label="Total de Equipo y Maquinaría",
        value=format_number_with_commas(EQUI['TOTAL MX'].sum()))
    
    # **MATERIALES**

    st.title("Materia prima")

    # Convertir la columna 'FECHA_DOC' a tipo datetime
    MATERIA_PRIMA['FECHA_DOC'] = pd.to_datetime(MATERIA_PRIMA['FECHA_DOC'], format="%d/%m/%Y %H:%M")
    # Extraer el mes de la columna 'FECHA_DOC' y crear una nueva columna 'MES'
    MATERIA_PRIMA['MES'] = MATERIA_PRIMA['FECHA_DOC'].dt.month
    # Calcular la suma total del costo total calculado por mes
    costo_total_por_mes = MATERIA_PRIMA.groupby('MES').agg({'COSTO_TOTAL_CALCULADO': 'sum'}).reset_index()
    # Graficar la suma total del costo total calculado por mes
    st.markdown("<h4 style='text-align: center'> Operativos </h4>", unsafe_allow_html=True)
    fig = px.line(costo_total_por_mes, x='MES', y='COSTO_TOTAL_CALCULADO', height=400, width=1500)
    fig.update_traces(line_width=5)
    fig.update_xaxes(title='Mes', dtick=1) 
    fig.update_yaxes(title='Suma total del costo total calculado por mes en 2022')
    fig

    # **GASTOS OPERATIVOS**

    gastos = totalgastos.copy()
    #40% para 3 tipos de gasto
    gastos.loc[gastos['TIPO GASTO'].isin(['COMISION MIXTA', 'IMSS/INFONAVIT', 'VALES DESPENSA']), 'TOTAL MX'] *= 0.4
    #Cambiamos
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['PAQUETERIA'], "PAQUETERIA")
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['UNIFORME','UNIFORMES'], "UNIFORMES Y EQUIPO")
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['ENERGIA ELECTRICA','SUELDOS PRODUCCION','COMISION MIXTA','IMSS/INFONAVIT','VALES DESPENSA'], "VARIOS")
    #GRAF1
    operativos = ['PAQUETERIA','UNIFORMES Y EQUIPO','VARIOS']
    op = gastos[gastos['TIPO GASTO'].isin(operativos)]
    op['FECHA'] = pd.to_datetime(op['FECHA'])
    op['Año'] = op['FECHA'].dt.year
    total = op.groupby(['Año', 'TIPO GASTO'])['TOTAL MX'].sum().reset_index()
    st.title("Gastos Operativos")

    oper = px.sunburst(total, path=['Año','TIPO GASTO'], values='TOTAL MX',
                  color='Año', title='Gastos Operativos por año')

    oper.update_layout(height=800, width=800, title_font=dict(size=24))
    
    oper

    #GRAF1.1
    st.markdown("<h4 style='text-align: center'> Evolución de Gastos Operativos por categoría y año </h4>", unsafe_allow_html=True)
    oper2 = px.area(total, x='Año', y='TOTAL MX', color='TIPO GASTO', height=400, width=1500)
    oper2

    #GRAF2
    st.title("Equipo y maquinaria")
    gastos['TIPO GASTO']= gastos['TIPO GASTO'].replace(['CALIBRACIONES','MTTO MAQUINARIA','MTTO LOCAL','REPARACIONES ELECTRICAS','INSTALACION ELECTRICA'], "MTTO MAQUINARIA Y EDIF")
    manto = ['MTTO MAQUINARIA Y EDIF']
    op = gastos[gastos['TIPO GASTO'].isin(manto)]
    op['FECHA'] = pd.to_datetime(op['FECHA'])
    op['Año'] = op['FECHA'].dt.year
    op['Mes'] = op['FECHA'].dt.month
    total = op.groupby(['Año', 'TIPO GASTO'])['TOTAL MX'].sum().reset_index()

    eq = px.sunburst(total, path=['Año','TIPO GASTO'], values='TOTAL MX',
                  color='Año', title='Costo de Equipo y Maquinaria por año')
    
    eq.update_layout(height=800, width=800, title_font=dict(size=24))
    eq

    #GRAF2.1
    st.markdown("<h4 style='text-align: center'> Evolución de costos en Equipo y Maquinaria por categoría y año'</h4>", unsafe_allow_html=True)
    eq2 = px.area(total, x='Año', y='TOTAL MX', color='TIPO GASTO', height=400, width=1500)
    eq2