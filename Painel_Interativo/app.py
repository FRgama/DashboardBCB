import streamlit as st
import pandas as pd
import plotly.express as px
from PreparacaoDeDados import carregar_dados

class Indicador:
    def __init__(self, nome, codigo):
        self.nome = nome
        self.codigo = codigo

    def obter_dados(self, inicio='2020-01-01'):
        df = sgs.get(self.codigo, start=inicio)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Data', self.nome: 'Valor'}, inplace=True)
        df['Indicador'] = self.nome
        return df

class PainelIndicadores:
    def __init__(self, dfSelic, dfIpca, dfSMin, dfIgpm, dfInad, df_indicadores):
        self.dfSelic = dfSelic
        self.dfIpca = dfIpca
        self.dfSMin = dfSMin
        self.dfIgpm = dfIgpm
        self.dfInad = dfInad
        self.df_indicadores = df_indicadores

    def filtrar(self, nome_indicador):
        # Garantir que a comparação seja feita de forma consistente
        nome_indicador = nome_indicador.strip().lower()
        
        if nome_indicador == 'selic':
            return self.dfSelic[['Data', 'Selic', 'Variacao_Selic']]
        elif nome_indicador == 'ipca':
            return self.dfIpca[['Data', 'Ipca', 'Variacao_Ipca']]
        elif nome_indicador == 'salario mínimo':
            return self.dfSMin[['Data', 'Salario_Minimo', 'Variacao_Salario']]
        elif nome_indicador == 'igpm':
            return self.dfIgpm[['Data', 'Igpm', 'Variacao_Igpm']]
        elif nome_indicador == 'inadimplência':
            return self.dfInad[['Data', 'Inadimplencia', 'Variacao_Inad']]
        elif nome_indicador == 'indicadores derivados':
            return self.df_indicadores
        else:
            raise ValueError(f"Indicador '{nome_indicador}' não encontrado.")

    def obter_indicadores(self):
        return ['Selic', 'IPCA', 'Salario Mínimo', 'IGPM', 'Inadimplência', 'Indicadores Derivados']

class AppStreamlit:
    def __init__(self, painel):
        self.painel = painel

    def exibir(self):
        st.set_page_config(layout='wide')
        st.title('Painel de Indicadores Econômicos')
        st.write('Fonte: Banco Central do Brasil (BCB)')

        indicadores = self.painel.obter_indicadores()
        indicador_escolhido = st.selectbox('Escolha um indicador:', indicadores)

        # Filtro de dados
        df_filtrado = self.painel.filtrar(indicador_escolhido.lower())  # Garantir que o nome seja minúsculo

        self._exibir_grafico(df_filtrado, indicador_escolhido)
        self._exibir_dados(df_filtrado)

    def _exibir_grafico(self, df, nome):
        fig = px.line(
            df, x='Data', y=df.columns[1],
            title=f'Evolução do {nome}',
            labels={df.columns[1]: 'Valor', 'Data': 'Data'},
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)

    def _exibir_dados(self, df):
        st.write('**Dados Brutos:**')
        st.dataframe(df)

# Execução do App
if __name__ == '__main__':
    # Carregar os dados corretamente
    dfSelic, dfIpca, dfSMin, dfIgpm, dfInad, df_indicadores = carregar_dados()

    painel = PainelIndicadores(dfSelic, dfIpca, dfSMin, dfIgpm, dfInad, df_indicadores)
    app_ui = AppStreamlit(painel)
    app_ui.exibir()
