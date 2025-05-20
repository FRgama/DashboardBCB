import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.metrics import root_mean_squared_error

class Regressao:
    def exibir_regressao_linear(self, df):
        st.subheader("Regressão Linear Múltipla")
    
        if df.shape[1] > 2:
            target = st.selectbox("Selecione o indicador a ser previsto (variável dependente):", df.columns[1:], key="reg_target")
            features = st.multiselect("Selecione as variáveis preditoras (independentes):", [col for col in df.columns[1:] if col != target], key="reg_features")
        
            
            if len(features) < 2:
                st.warning("Selecione pelo menos dois indicadores (independentes) para análise de regressão")
            else:
                if st.button("Executar Regressão"):

                    df_modelo = df.dropna(subset=[target] + features)
                    X = df_modelo[features]
                    y = df_modelo[target]

                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)

                    st.markdown("### Verificação de Multicolinearidade (VIF)")
                    vif_data = pd.DataFrame()
                    vif_data["Variável"] = features
                    vif_data["VIF"] = [variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape[1])]
                    st.dataframe(vif_data)

                    st.markdown("### Correlação entre Variáveis Preditivas")
                    fig_corr = px.imshow(pd.DataFrame(X, columns=features).corr(), text_auto=True, color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
                    st.plotly_chart(fig_corr, use_container_width=True)

                    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
                    modelo = LinearRegression()
                    modelo.fit(X_train, y_train)
                    y_pred = modelo.predict(X_test)

                    r2 = r2_score(y_test, y_pred)
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = root_mean_squared_error(y_test, y_pred)

                    st.markdown(f"### Avaliação do Modelo")
                    st.write(f"**R² (coeficiente de determinação):** {r2:.2f}")
                    st.write(f"**MAE (erro absoluto médio):** {mae:.2f}")
                    st.write(f"**RMSE (raiz do erro quadrático médio):** {rmse:.2f}")

                    st.markdown("### Coeficientes do Modelo")
                    for var, coef in zip(features, modelo.coef_):
                        st.write(f"- {var}: {coef:.4f}")

                    futuro_data = pd.to_datetime(df['Data'].max()) + pd.DateOffset(years=1)
                    st.markdown(f"### Previsão para o Ano de {futuro_data.year}")
                    
                    features_futuras = X.iloc[-1:].copy()
                    features_futuras['Data'] = futuro_data

                    X_futuro_scaled = scaler.transform(features_futuras[features])
                    y_futuro = modelo.predict(X_futuro_scaled)
                    st.write(f"**Previsão do {target} para {futuro_data.year}:** {y_futuro[0]:.2f}")

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
