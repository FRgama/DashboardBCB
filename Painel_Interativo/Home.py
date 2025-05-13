import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from PreparacaoDeDados import carregar_dados
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import mean_absolute_error, mean_squared_error


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

        df_base = self.df_selic.copy()
        df_base['Data'] = pd.to_datetime(df_base['Data'], errors='coerce')
        data_minima = df_base['Data'].min().replace(day=1)
        data_maxima = df_base['Data'].max().replace(day=1)

        data_inicial = st.sidebar.date_input("A partir de:", data_minima, min_value=data_minima, max_value=data_maxima)


        if selecionados:
            data_inicial = pd.to_datetime(data_inicial).replace(day=1)
            df = self._preparar_comparacao(selecionados, data_inicial)
            self._exibir_grafico_linha(df)
            self._exibir_grafico_dispersao(df)
            self._exibir_grafico_barras(df)
            self._exibir_grafico_boxplot(df)
            self._exibir_matriz_correlacao(df)
            self._exibir_regressao_linear(df)

    
    def _preparar_comparacao(self, selecionados, data_inicial):
        df_base = self.df_selic.copy()
        df_base['Data'] = pd.to_datetime(df_base['Data'], errors='coerce')
        df_base = df_base.dropna(subset=['Data']).set_index('Data')
        df_base = df_base[df_base.index >= data_inicial]

        df_comparado = pd.DataFrame(index=df_base.index)

        if SELIC in selecionados:
            df_comparado['Selic'] = df_base['Selic']

        def join_df(indicador, df, coluna):
            if indicador in selecionados and not df.empty:
                temp = df.copy()
                temp['Data'] = pd.to_datetime(temp['Data'], errors='coerce')
                temp.set_index('Data', inplace=True)

                temp = temp[temp.index >= data_inicial]
                
                return df_comparado.join(temp[[coluna]], how='outer')
            return df_comparado

        df_comparado = join_df(IPCA, self.df_ipca, 'Ipca')
        df_comparado = join_df(SALARIO_MINIMO, self.df_salario, 'Salario Mínimo')
        df_comparado = join_df(IGPM, self.df_igpm, 'Igpm')
        df_comparado = join_df(INADIMPLENCIA, self.df_inad, 'Inadimplência')
        df_comparado = join_df(INADIMPLENCIA_FAMILIA, self.df_inad_familia, 'Inadimplência Familiar')
        df_comparado = join_df(CREDITO_TOTAL, self.df_cred_total, 'Crédito Total')
        df_comparado = join_df(DOLAR, self.df_dolar, 'Dólar')

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
    def _exibir_matriz_correlacao(self, df):
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

    def _exibir_regressao_linear(self, df):
        st.subheader("Regressão Linear Múltipla")

        if df.shape[1] > 2:
            target = st.selectbox("Selecione o indicador a ser previsto (variável dependente):", df.columns[1:], key="reg_target")
            features = st.multiselect("Selecione as variáveis preditoras (independentes):", [col for col in df.columns[1:] if col != target], key="reg_features")

            if features and st.button("Executar Regressão"):
                df_modelo = df.dropna(subset=[target] + features)
                X = df_modelo[features]
                y = df_modelo[target]

                # Padronização dos dados
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                # Verificação de multicolinearidade (VIF)
                st.markdown("### Verificação de Multicolinearidade (VIF)")
                vif_data = pd.DataFrame()
                vif_data["Variável"] = features
                vif_data["VIF"] = [variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape[1])]
                st.dataframe(vif_data)

                # Correlação entre features selecionadas
                st.markdown("### Correlação entre Variáveis Preditivas")
                fig_corr = px.imshow(pd.DataFrame(X, columns=features).corr(), text_auto=True, color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
                st.plotly_chart(fig_corr, use_container_width=True)

                # Treinamento do modelo
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                modelo = LinearRegression()
                modelo.fit(X_train, y_train)
                y_pred = modelo.predict(X_test)

                # Avaliação do modelo
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                rmse = mean_squared_error(y_test, y_pred, squared=False)

                st.markdown(f"### Avaliação do Modelo")
                st.write(f"**R² (coeficiente de determinação):** {r2:.2f}")
                st.write(f"**MAE (erro absoluto médio):** {mae:.2f}")
                st.write(f"**RMSE (raiz do erro quadrático médio):** {rmse:.2f}")

                # Coeficientes
                st.markdown("### Coeficientes do Modelo")
                for var, coef in zip(features, modelo.coef_):
                    st.write(f"- {var}: {coef:.4f}")

                # Previsão para o futuro (exemplo: daqui 1 ano)
                futuro_data = pd.to_datetime(df['Data'].max()) + pd.DateOffset(years=1)
                st.markdown(f"### Previsão para o Ano de {futuro_data.year}")
                
                # Gerar valores futuros para as variáveis independentes
                # Aqui você teria que definir como "futurizar" as variáveis independentes
                # Exemplo, apenas avançando um ano na variável 'Data'
                features_futuras = X.iloc[-1:].copy()
                features_futuras['Data'] = futuro_data

                # Padronização das variáveis para o modelo
                X_futuro_scaled = scaler.transform(features_futuras[features])

                # Realizando a previsão
                y_futuro = modelo.predict(X_futuro_scaled)
                st.write(f"**Previsão do {target} para {futuro_data.year}:** {y_futuro[0]:.2f}")

                # Gráfico de previsão
                fig_pred = px.scatter(
                    x=y_test,
                    y=y_pred,
                    labels={"x": "Valores Reais", "y": "Valores Previsto"},
                    title="Valores Reais vs. Previsto",
                    template="plotly_dark"
                )
                fig_pred.add_shape(
                    type="line",
                    x0=min(y_test),
                    y0=min(y_test),
                    x1=max(y_test),
                    y1=max(y_test),
                    line=dict(color="red", dash="dash")
                )
                st.plotly_chart(fig_pred, use_container_width=True)



if __name__ == '__main__':
    app = AppStreamlit()
    app.exibir()
