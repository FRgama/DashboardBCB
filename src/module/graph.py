import streamlit as st
import plotly.express as px

class Graficos:
    def exibir_grafico_linha(self, df):
        st.subheader('Gráfico de Linha')
        st.text("Gráfico de evolução de todos os indicadores selecionados")
        if df.empty:
            st.error("Não há dados para o gráfico de linha.")
            return
        try:
            fig = px.line(df, x='Data', y=df.columns[1:], title="Evolução dos Indicadores", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de linha: {e}")

    def exibir_grafico_dispersao(self, df):
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

    def exibir_grafico_barras(self, df):
        st.subheader('Gráfico de Barras')
        st.text("Evolução individual do indicador selecionado")
        if df.empty:
            st.error("Não há dados para o gráfico de barras.")
            return
        try:
            col = st.selectbox("Indicador:", df.columns[1:], key="bar")
            fig = px.bar(df, x='Data', y=col, title=f"{col} ao longo do tempo", template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro no gráfico de barras: {e}")

    def exibir_grafico_boxplot(self, df):
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

    def exibir_matriz_correlacao(self, df):
        st.subheader('Matriz de Correlação de Pearson')
        if df.empty or df.shape[1] <= 2:
            st.info("Selecione pelo menos dois indicadores para gerar a matriz de correlação.")
            return
        try:
            df_corr = df.drop(columns=['Data']).corr(method='pearson')
            fig = px.imshow(
                df_corr,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title="Correlação de Pearson entre Indicadores",
                aspect='auto',
                template='plotly_dark'
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao gerar a matriz de correlação: {e}")
