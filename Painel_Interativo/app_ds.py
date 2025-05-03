import streamlit as st
import plotly.express as px
import pandas as pd
from PreparacaoDeDados import carregar_dados

class AppStreamlit:
    def __init__(self):
        # Carregar dados
        self.dfSelic, self.dfIpca, self.dfSMin, self.dfIgpm, self.dfInad, self.df_indicadores = carregar_dados()

    def exibir(self):
        st.set_page_config(layout='wide')
        st.title('Painel de Indicadores Econômicos')

        st.sidebar.title("Seleção de Indicadores")
        indicadores = ['Selic', 'IPCA', 'Salario Mínimo', 'IGPM', 'Inadimplência', 'Indicadores Derivados']
        indicadores_selecionados = st.sidebar.multiselect("Escolha os Indicadores para comparação", indicadores)

        if indicadores_selecionados:
            df_comparacao = self._preparar_comparacao(indicadores_selecionados)
            self._exibir_grafico_linha(df_comparacao)
            self._exibir_grafico_dispersao(df_comparacao)
            self._exibir_grafico_barras(df_comparacao)
            self._exibir_grafico_boxplot(df_comparacao)

    def _preparar_comparacao(self, indicadores_selecionados):
        df_comparado = pd.DataFrame()

        if 'Selic' in indicadores_selecionados:
            df_comparado['Data'] = self.dfSelic['Data']
            df_comparado['Selic'] = self.dfSelic['Selic']

        if 'IPCA' in indicadores_selecionados:
            df_comparado['Ipca'] = self.dfIpca['Ipca']

        if 'Salario Mínimo' in indicadores_selecionados:
            if 'Data' in self.dfSMin.columns:  # Verifique se a coluna 'Data' existe
                df_comparado['Data'] = self.dfSMin['Data']  # Caso não tenha sido adicionado anteriormente
            df_comparado['Salario_Minimo'] = self.dfSMin['Salario_Minimo']

        if 'IGPM' in indicadores_selecionados:
            df_comparado['Igpm'] = self.dfIgpm['Igpm']

        if 'Inadimplência' in indicadores_selecionados:
            df_comparado['Inadimplencia'] = self.dfInad['Inadimplencia']

        if 'Indicadores Derivados' in indicadores_selecionados:
            df_comparado = pd.concat([df_comparado, self.df_indicadores], axis=1)

        # Verificar se 'Data' está presente em df_comparado e garantir que seja convertido para datetime
        if 'Data' in df_comparado.columns:
            df_comparado['Data'] = pd.to_datetime(df_comparado['Data'], errors='coerce')
        else:
            st.warning("A coluna 'Data' não está presente em todos os DataFrames. Verifique seus dados.")

        df_comparado = df_comparado.dropna(subset=['Data'])

        return df_comparado

    def _exibir_grafico_linha(self, df):
        st.subheader('Gráfico de Linha')
        
        if df.empty:
            st.error("Não há dados suficientes para exibir o gráfico de linha.")
            return

        try:
            fig = px.line(
                df, x='Data', y=df.columns[1:],  # Usar todas as colunas exceto 'Data'
                title="Evolução dos Indicadores ao Longo do Tempo",
                labels={'Data': 'Data', 'value': 'Valor'},
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de linha: {e}")

    def _exibir_grafico_dispersao(self, df):
        st.subheader('Gráfico de Dispersão')
        
        if df.empty:
            st.error("Não há dados suficientes para exibir o gráfico de dispersão.")
            return

        try:
            indicador_1 = st.selectbox("Escolha o primeiro indicador para dispersão:", df.columns[1:])
            indicador_2 = st.selectbox("Escolha o segundo indicador para dispersão:", df.columns[1:])

            fig = px.scatter(
                df, x=indicador_1, y=indicador_2,
                title=f"Dispersão entre {indicador_1} e {indicador_2}",
                labels={indicador_1: indicador_1, indicador_2: indicador_2},
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de dispersão: {e}")

    def _exibir_grafico_barras(self, df):
        st.subheader('Gráfico de Barras')
        
        if df.empty:
            st.error("Não há dados suficientes para exibir o gráfico de barras.")
            return

        try:
            indicador_comparacao = st.selectbox("Escolha o indicador para barras:", df.columns[1:])

            fig = px.bar(
                df, x='Data', y=indicador_comparacao,
                title=f"Comparação de {indicador_comparacao} ao longo do tempo",
                labels={'Data': 'Data', indicador_comparacao: indicador_comparacao},
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de barras: {e}")

    def _exibir_grafico_boxplot(self, df):
        st.subheader('Gráfico de Boxplot')
        
        if df.empty:
            st.error("Não há dados suficientes para exibir o gráfico de boxplot.")
            return

        try:
            indicador_boxplot = st.selectbox("Escolha o indicador para Boxplot:", df.columns[1:])

            fig = px.box(
                df, y=indicador_boxplot,
                title=f"Distribuição de {indicador_boxplot}",
                labels={indicador_boxplot: indicador_boxplot},
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de boxplot: {e}")

# Execução do App
if __name__ == '__main__':
    app = AppStreamlit()
    app.exibir()
