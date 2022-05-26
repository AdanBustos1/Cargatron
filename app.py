import pandas as pd
import streamlit as st
import funciones as ft

st.set_page_config(page_icon="cat", layout='wide')

pagina = st.sidebar.selectbox('Página', ('Home', 'Datos'))

if pagina == 'Home':
    ft.home()
elif pagina == 'Datos':
    ft.datos()





