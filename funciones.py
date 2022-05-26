import pandas as pd
import streamlit as st

def home():
    st.title('Cargatron')
    st.image('cargador-de-cable-gordo.jpg')

    with st.expander('Descripcion'):
        st.markdown('Esto es una aplicacion para encontrar el cargador mas cercano a tu casa')

def datos():
    path = 'red_recarga_acceso_publico _2021.csv'

    uploaded_file = st.file_uploader('Tienes otros datos?', type=['csv'])

    df = cargar_datos(path, uploaded_file)

    df, checkbox_distrito = filtros(df)

    if df.shape[0] == 0:
        st.warning('Tu filtro no ha devuelto ningún resultado')
        st.stop()


    with st.echo():
        st.dataframe(df)

    if checkbox_distrito:
        st.map(df, zoom=13)
    else:
        st.map(df, zoom=11)

    df_bar = df.groupby('DISTRITO')['Nº CARGADORES'].sum()
    st.bar_chart(df_bar)

    df_bar = df.groupby('OPERADOR')['Nº CARGADORES'].sum()
    st.bar_chart(df_bar)

def filtros(df):
    distritos = df['DISTRITO'].unique()
    operadores = df['OPERADOR'].unique()

    checkbox_distrito = st.sidebar.checkbox('Filtro por distrito')
    selected_distrito = st.sidebar.selectbox('Distritos', distritos)

    checkbox_operador = st.sidebar.checkbox('Filtro por operador')
    selected_operador = st.sidebar.selectbox('Operadores', operadores)

    checkbox_n_cargadores = st.sidebar.checkbox('Filtro por nº de cargadores')
    min_n_cargadores = int(df['Nº CARGADORES'].min())
    max_n_cargadores = int(df['Nº CARGADORES'].max())
    selected_n_cargadores = st.sidebar.slider('Nº de cargadores', min_n_cargadores, max_n_cargadores, 1)

    if checkbox_distrito:
        df = df[df['DISTRITO'] == selected_distrito]

    if checkbox_operador:
        df = df[df['OPERADOR'] == selected_operador]

    if checkbox_n_cargadores:
        df = df[df['Nº CARGADORES'] == selected_n_cargadores]

    return df, checkbox_distrito

@st.cache(suppress_st_warning=True)
def cargar_datos(path, datos_cargados):
    if datos_cargados is not None:
        df = pd.read_csv(datos_cargados)
        st.balloons()
    else:
        df = pd.read_csv(path, sep=';')
        df = df.rename(columns={"longitud": "lon", "latidtud": "lat"})

    return df