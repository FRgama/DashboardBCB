import streamlit as st
import pandas as pd
from module.PreparacaoDeDados import carregar_dados
from module.graph import Graficos
from module.regression import Regressao

st.set_page_config(
            page_title="Help MEi",
            layout="centered",
            page_icon='../imagens/EconoVisionLogo.png',
            menu_items={}
        )

SELIC = 'Selic'
IPCA = 'IPCA'
REMUNERACAO_DEFLACIONADA = 'Remuneração Média Deflacionada'
IGPM = 'IGPM'
INADIMPLENCIA = 'Inadimplência'
INADIMPLENCIA_FAMILIA = 'Inadimplência Família'
CREDITO_TOTAL = 'Crédito Total'
DOLAR = 'Dólar'

class AppStreamlit:
    def __init__(self):
        self.df_selic, self.df_ipca, self.df_salario, self.df_igpm, self.df_inad, self.df_inad_familia, self.df_cred_total, self.df_dolar = carregar_dados()
        self.graficos = Graficos()
        self.regressao = Regressao()

    def exibir(self):
        
        st.title('Painel de Indicadores Econômicos')
        st.markdown(
            """
            <p> Para informações a respeito dos indicadores e dos gráficos acesse: <a href='pages\Resumo.py' targe='_self' style='color:blue'>Resumo</a></p>
            
            """
        ,unsafe_allow_html=True)
        st.sidebar.image('../imagens/EconoVisionLogo.png')
        st.sidebar.title("Seleção de Indicadores")
        indicadores = [SELIC, IPCA, REMUNERACAO_DEFLACIONADA, IGPM, INADIMPLENCIA, INADIMPLENCIA_FAMILIA, CREDITO_TOTAL, DOLAR]
        selecionados = st.sidebar.multiselect("Escolha os Indicadores para comparação", indicadores)

        if not selecionados:
            st.warning("Selecione pelo menos um indicador para comparação.")

        df_base = self.df_selic.copy()
        df_base['Data'] = pd.to_datetime(df_base['Data'], errors='coerce')
        data_minima = df_base['Data'].min().replace(day=1)
        data_maxima = df_base['Data'].max().replace(day=1)

        data_inicial = st.sidebar.date_input("A partir de:", data_minima, min_value=data_minima, max_value=data_maxima)

        if selecionados:
            data_inicial = pd.to_datetime(data_inicial).replace(day=1)
            df = self._preparar_comparacao(selecionados, data_inicial)

            self.graficos.exibir_grafico_linha(df)
            self.graficos.exibir_grafico_barras(df)
            self.graficos.exibir_grafico_dispersao(df)
            self.graficos.exibir_grafico_boxplot(df)
            self.graficos.exibir_matriz_correlacao(df)

            self.regressao.exibir_regressao_linear(df)

            st.sidebar.markdown(
            """
            <hr style="margin-top: 50px;">
            <div style="text-align: center; font-size: 0.8em;">
                <a href="https://creativecommons.org">EconoVision</a> © 1999 por 
                <a href="https://creativecommons.org">Rodrigo Correa da Gama, Beatriz de Souza Santos Rio Branco, Sátiro Gabriel de Souza Santos, Sabrinna Cristina Gomes Vicente</a> 
                está licenciado sob 
                <a href="https://creativecommons.org/licenses/by-sa/4.0/" style="color:#1f77b4;">CC BY-SA 4.0</a>
                <img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;">
                <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;">
                <img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;">
            </div>
            """,
            unsafe_allow_html=True
        )

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
        df_comparado = join_df(REMUNERACAO_DEFLACIONADA, self.df_salario, 'Remuneração Média Deflacionada')
        df_comparado = join_df(IGPM, self.df_igpm, 'Igpm')
        df_comparado = join_df(INADIMPLENCIA, self.df_inad, 'Inadimplência')
        df_comparado = join_df(INADIMPLENCIA_FAMILIA, self.df_inad_familia, 'Inadimplência Familiar')
        df_comparado = join_df(CREDITO_TOTAL, self.df_cred_total, 'Crédito Total')
        df_comparado = join_df(DOLAR, self.df_dolar, 'Dólar')

        df_comparado = df_comparado.dropna(how='all').reset_index()
        return df_comparado

if __name__ == '__main__':
    app = AppStreamlit()
    app.exibir()
