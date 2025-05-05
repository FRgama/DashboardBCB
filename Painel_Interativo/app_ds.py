import streamlit as st
import plotly.express as px
import pandas as pd
from PreparacaoDeDados import carregar_dados

# Constantes para os nomes dos indicadores
IPCA = 'IPCA'
SELIC = 'Selic'
SALARIO_MINIMO = 'Salário Mínimo'
IGPM = 'IGPM'
INADIMPLENCIA = 'Inadimplência'
INADIMPLENCIA_FAMILIA = 'Inadimplência Família'
CREDITO_TOTAL = 'Crédito Total'
DOLAR = 'Dólar'


class AppStreamlit:
    def __init__(self):
        # Carregar dados
        self.df_selic, self.df_ipca, self.df_salario, self.df_igpm, self.df_inad, self.df_inad_familia, self.df_cred_total, self.df_dolar = carregar_dados()

    def exibir(self):
        st.set_page_config(layout='wide')
        st.title('Painel de Indicadores Econômicos')

        st.sidebar.title("Seleção de Indicadores")
        indicadores = [SELIC, IPCA, SALARIO_MINIMO, IGPM, INADIMPLENCIA, INADIMPLENCIA_FAMILIA, CREDITO_TOTAL, DOLAR]
        indicadores_selecionados = st.sidebar.multiselect("Escolha os Indicadores para comparação", indicadores)

        if indicadores_selecionados:
            df_comparacao = self._preparar_comparacao(indicadores_selecionados)
            self._exibir_grafico_linha(df_comparacao)
            self._exibir_grafico_dispersao(df_comparacao)
            self._exibir_grafico_barras(df_comparacao)
            self._exibir_grafico_boxplot(df_comparacao)

    def _preparar_comparacao(self, indicadores_selecionados):
        df_comparado = pd.DataFrame()

        # Base: Selic
        df_base = self.df_selic.copy()
        df_base['Data'] = pd.to_datetime(df_base['Data'], errors='coerce')
        df_base = df_base.dropna(subset=['Data'])
        df_base.set_index('Data', inplace=True)

        if SELIC in indicadores_selecionados:
            df_comparado['Selic'] = df_base['Selic']

        if IPCA in indicadores_selecionados:
            df = self.df_ipca.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Ipca'], how='outer')

        if SALARIO_MINIMO in indicadores_selecionados:
            df = self.df_salario.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Salario_Minimo'], how='outer')

        if IGPM in indicadores_selecionados:
            df = self.df_igpm.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Igpm'], how='outer')

        if INADIMPLENCIA in indicadores_selecionados:
            df = self.df_inad.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Inadimplencia'], how='outer')

        if INADIMPLENCIA_FAMILIA in indicadores_selecionados:
            df = self.df_inad_familia.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Inadimplencia_Familia'], how='outer')

        if CREDITO_TOTAL in indicadores_selecionados:
            df = self.df_cred_total.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['CredTotal'], how='outer')

        if DOLAR in indicadores_selecionados:
            df = self.df_dolar.copy()
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df.set_index('Data', inplace=True)
            df_comparado = df_comparado.join(df['Dolar'], how='outer')

        df_comparado = df_comparado.dropna(how='all')
        df_comparado.reset_index(inplace=True)

        return df_comparado

    def _exibir_grafico_linha(self, df):
        st.subheader('Gráfico de Linha')

        if df.empty:
            st.error("Não há dados suficientes para exibir o gráfico de linha.")
            return

        try:
            fig = px.line(
                df, x='Data', y=df.columns[1:],
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
            indicador = st.selectbox("Escolha o indicador para barras:", df.columns[1:])

            fig = px.bar(
                df, x='Data', y=indicador,
                title=f"Comparação de {indicador} ao longo do tempo",
                labels={'Data': 'Data', indicador: indicador},
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
            indicador = st.selectbox("Escolha o indicador para Boxplot:", df.columns[1:])

            fig = px.box(
                df, y=indicador,
                title=f"Distribuição de {indicador}",
                labels={indicador: indicador},
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao criar o gráfico de boxplot: {e}")


# Execução do App
if __name__ == '__main__':
    app = AppStreamlit()
    app.exibir()
