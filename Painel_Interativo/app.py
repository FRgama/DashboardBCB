#obs: para rodar o painel, digite 'streamlit run app.py' no terminal

import pandas as pd
import plotly.express as px
import streamlit as st
from bcb import sgs

#Dicionário de Indicadores Macroeconômicos
indicadores = {
    'Selic': 11,
    'IPCA': 4449,
    'IGP-M': 189,
    'Dólar': 1
}

#Baixando os dados a partir de 2000
dados = {nome: sgs.get(codigo, start='2020-01-01') for nome, codigo in indicadores.items()}

#Convertendo para dataframe e resetando o índice
for nome, df in dados.items():
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Data', nome: 'Valor'}, inplace=True)
    #df["Data"] = pd.to_datetime(df["Data"], format='%Y-%m-%d')
    #df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce')
    #df.dropna(subset=["Valor"], inplace=True)
    df['Indicador'] = nome

df_final = pd.concat(dados.values())

st.set_page_config(layout='wide')
st.title('📊 Painel de Indicadores Econômicos')
st.write('Fonte: Banco Central do Brasil (BCB)')

indicador_escolhido = st.selectbox('Escolha um indicador:', df_final['Indicador'].unique())

df_filtrado = df_final[df_final['Indicador'] == indicador_escolhido]

#Gráfico interativo com plotly dash
fig = px.line(df_filtrado, x='Date', y='Indicador', title=f'Evolução do {indicador_escolhido}',
              labels={'Indicador': 'Valor', 'Date': 'Data'}, template='plotly_dark')

st.plotly_chart(fig, use_container_width=True)

#Exibindo a tela de dados
st.write('📅 **Dados Brutos:**')
st.dataframe(df_filtrado)