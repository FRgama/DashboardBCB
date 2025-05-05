import streamlit as st
import plotly.express as px
import pandas as pd
from PreparacaoDeDados import carregar_dados

SELIC = 'Selic'
IPCA = 'IPCA'
SALARIO_MINIMO = 'Salário Mínimo'
IGPM = 'IGPM'
INADIMPLENCIA = 'Inadimplência'
INADIMPLENCIA_FAMILIA = 'Inadimplência Família'
CREDITO_TOTAL = 'Crédito Total'
DOLAR = 'Dólar'

class AppStreamlit:
    def __init__(self):
        self.df_selic, self.df_ipca, self.df_salario, self.df_igpm, self.df_inad, self.df_inad_familia, self.df_cred_total, self.df_dolar = carregar_dados()

    def exibir(self):
        st.set_page_config(layout='wide')
        st.title('Painel de Indicadores Econômicos')

        st.sidebar.title("Seleção de Indicadores")
        indicadores = [SELIC, IPCA, SALARIO_MINIMO, IGPM, INADIMPLENCIA, INADIMPLENCIA_FAMILIA, CREDITO_TOTAL, DOLAR]
        selecionados = st.sidebar.multiselect("Escolha os Indicadores para comparação", indicadores)

        if selecionados:
            df = self._preparar_comparacao(selecionados)
            self._exibir_grafico_linha(df)
            self._exibir_grafico_dispersao(df)
            self._exibir_grafico_barras(df)
            self._exibir_grafico_boxplot(df)

    def _preparar_comparacao(self, selecionados):
        df_base = self.df_selic.copy()
        df_base['Data'] = pd.to_datetime(df_base['Data'], errors='coerce')
        df_base = df_base.dropna(subset=['Data']).set_index('Data')

        df_comparado = pd.DataFrame(index=df_base.index)

        if SELIC in selecionados and not self.df_selic.empty:
            df_comparado['Selic'] = df_base['Selic']

        def join_df(indicador, df, coluna):
            if indicador in selecionados and not df.empty:
                temp = df.copy()
                temp['Data'] = pd.to_datetime(temp['Data'], errors='coerce')
                temp.set_index('Data', inplace=True)
                return df_comparado.join(temp[[coluna]], how='outer')
            return df_comparado

        df_comparado = join_df(IPCA, self.df_ipca, 'Ipca')
        df_comparado = join_df(SALARIO_MINIMO, self.df_salario, 'Salario_Minimo')
        df_comparado = join_df(IGPM, self.df_igpm, 'Igpm')
        df_comparado = join_df(INADIMPLENCIA, self.df_inad, 'Inadimplencia')
        df_comparado = join_df(INADIMPLENCIA_FAMILIA, self.df_inad_familia, 'Inadimplencia_Familia')
        df_comparado = join_df(CREDITO_TOTAL, self.df_cred_total, 'CredTotal')
        df_comparado = join_df(DOLAR, self.df_dolar, 'Dolar')

        df_comparado = df_comparado.dropna(how='all').reset_index()
        return df_comparado

    def _exibir_grafico_linha(self, df):
        st.subheader('Gráfico de Linha')
        if df.empty:
            st.error("Não há dados para o gráfico de linha.")
            return
        try:
            fig = px.line(df, x='Data', y=df.columns[1:], title="Evolução dos Indicadores", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de linha: {e}")

    def _exibir_grafico_dispersao(self, df):
        st.subheader('Gráfico de Dispersão')
        if df.empty:
            st.error("Não há dados para o gráfico de dispersão.")
            return
        try:
            col1 = st.selectbox("Indicador X:", df.columns[1:], key="disp1")
            col2 = st.selectbox("Indicador Y:", df.columns[1:], key="disp2")
            fig = px.scatter(df, x=col1, y=col2, title=f"Dispersão: {col1} vs {col2}", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de dispersão: {e}")

    def _exibir_grafico_barras(self, df):
        st.subheader('Gráfico de Barras')
        if df.empty:
            st.error("Não há dados para o gráfico de barras.")
            return
        try:
            col = st.selectbox("Indicador:", df.columns[1:], key="bar")
            fig = px.bar(df, x='Data', y=col, title=f"{col} ao longo do tempo", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de barras: {e}")

    def _exibir_grafico_boxplot(self, df):
        st.subheader('Gráfico de Boxplot')
        if df.empty:
            st.error("Não há dados para o gráfico de boxplot.")
            return
        try:
            col = st.selectbox("Indicador:", df.columns[1:], key="box")
            fig = px.box(df, y=col, title=f"Distribuição de {col}", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de boxplot: {e}")


if __name__ == '__main__':
    app = AppStreamlit()
    app.exibir()
