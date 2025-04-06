import streamlit as st
import pandas as pd
import plotly.express as px
from bcb import sgs

# --- CLASSES DO PROJETO ---

class Indicador:
    def __init__(self, nome, codigo):
        self.nome = nome
        self.codigo = codigo

    def obter_dados(self, inicio='2025-01-01'):
        df = sgs.get(self.codigo, start=inicio)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Data', self.nome: 'Valor'}, inplace=True)
        df['Indicador'] = self.nome
        return df

class PainelIndicadores:
    def __init__(self):
        self.indicadores = {
            'Selic': 11,
            'IPCA': 4449,
            'IGP-M': 189,
            'Dólar': 1
        }
        self.df_final = None

    def carregar_dados(self):
        dados = []
        for nome, codigo in self.indicadores.items():
            indicador = Indicador(nome, codigo)
            dados.append(indicador.obter_dados())
        self.df_final = pd.concat(dados)

    def filtrar(self, nome_indicador):
        return self.df_final[self.df_final['Indicador'] == nome_indicador]


class AppStreamlit:
    def __init__(self, painel):
        self.painel = painel

    def exibir(self):
        st.set_page_config(layout='wide')
        st.title(' Painel de Indicadores Econômicos')
        st.write('Fonte: Banco Central do Brasil (BCB)')

        indicadores = self.painel.df_final['Indicador'].unique()
        indicador_escolhido = st.selectbox('Escolha um indicador:', indicadores)

        df_filtrado = self.painel.filtrar(indicador_escolhido)

        self._exibir_grafico(df_filtrado, indicador_escolhido)
        self._exibir_dados(df_filtrado)

    def _exibir_grafico(self, df, nome):
        fig = px.line(
            df, x='Data', y='Valor',
            title=f'Evolução do {nome}',
            labels={'Valor': 'Valor', 'Data': 'Data'},
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)

    def _exibir_dados(self, df):
        st.write(' **Dados Brutos:**')
        st.dataframe(df)


# --- EXECUÇÃO DO APP ---

if __name__ == '__main__':
    painel = PainelIndicadores()
    painel.carregar_dados()

    app_ui = AppStreamlit(painel)
    app_ui.exibir()