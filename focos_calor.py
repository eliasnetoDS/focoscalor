#importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import altair as alt
import os
import numpy as np
import folium
from folium.plugins import HeatMap
from PIL import Image
from streamlit_folium import folium_static

#adicionando o logotipo
with st.container():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        image = Image.open("logo eco.png")
        st.image(image, width=200)

# Cria um título para a aplicação
st.title("MONITORAMENTO DOS FOCOS DE CALOR")

# Extraindo os dados de Focos de Calor do site Queimadas, mantido pelo Instituto Nacional de Pesquisas Espaciais - INPE
CSV_URL = 'https://queimadas.dgi.inpe.br/home/downloadfile?path=%2Fapp%2Fapi%2Fdata%2Fdados_abertos%2Ffocos%2FDiario%2Ffocos_abertos_24h_20230326.csv'
df = pd.read_csv(CSV_URL, parse_dates=['data_hora_gmt'])  #O parâmetro parse_dates=['datahora'] faz com que a coluna 'data_hora_gmt' seja parseadas para o tipo datetime

#Criando um filtro apenas com dados amazônicos
focos_amazonia = df.query('bioma=="Amazônia"')
#dados = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")


m = folium.Map(location = [-3.12500, -54.14000], zoom_start = 8)

ALTERDOCHAO = 'C:/Users/netoeli/OneDrive - CREATHUS INSTITUTO DE TECNOLOGIA DA AMAZONIA/Documentos/Creathus/Projetos/ECOCITIZEN/Dashboard Monitoramento/APA_ALTER_DO_CHAO.geojson'

import geopandas as gpd

with open('APA_ALTER_DO_CHAO.geojson', 'r', encoding='utf-8') as f:
    gdf = gpd.read_file(f)

# Remove geometrias faltantes
gdf = gdf.dropna(subset=['geometry'])

# Converte para json e adiciona ao mapa com folium
folium.GeoJson(gdf.to_json()).add_to(m)

#adicionando os pontos de focos de calor, no formato de mapa e calor

locais = focos_amazonia[['lat','lon']].values.tolist()

HeatMap(locais, 0.5 ).add_to(m)  #gerando o mapa de calor e adicionando no mapa

folium_static(m)

