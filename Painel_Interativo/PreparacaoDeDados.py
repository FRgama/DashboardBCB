import pandas as pd
from bcb import sgs

# Função para carregar dados
def carregar_dados():
    # Carregando os dados
    dfSelic = sgs.get({'Selic': 1178}, start='2020-01-01')
    dfIpca = sgs.get({'Ipca': 433}, start='2020-01-01')
    dfSMin = sgs.get({'Salario_Minimo': 1619}, start='2020-01-01')
    dfIgpm = sgs.get({'Igpm': 189}, start='2020-01-01')
    dfInad = sgs.get({'Inadimplencia': 21082}, start='2020-01-01')
    dfInadFamilia = sgs.get({'Inadimplencia_Familia': 2074}, start='2020-01-01')
    dfCredTotal = sgs.get({'CredTotal': 20631}, start='2020-01-01')
    dfDolar = sgs.get({'Dolar': 1}, start='2020-01-01')

    # Função para ajustar colunas e renomear
    def ajuste_colunas(df, nome_coluna):
        df = df.reset_index()
        df = df.rename(columns={df.columns[0]: 'Data', df.columns[1]: nome_coluna})
        return df

    # Ajustando as colunas dos DataFrames
    dfSelic = ajuste_colunas(dfSelic, 'Selic')
    dfIpca = ajuste_colunas(dfIpca, 'Ipca')
    dfSMin = ajuste_colunas(dfSMin, 'Salario_Minimo')
    dfIgpm = ajuste_colunas(dfIgpm, 'Igpm')
    dfInad = ajuste_colunas(dfInad, 'Inadimplencia')
    dfInadFamilia = ajuste_colunas(dfInadFamilia, 'Inadimplencia_Familia')
    dfCredTotal = ajuste_colunas(dfCredTotal, 'CredTotal')
    dfDolar = ajuste_colunas(dfDolar, 'Dolar')


    # Ajustando as datas
    def ajuste_data(df):
        df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
        return df

    # Aplicando o ajuste de datas
    dfSelic = ajuste_data(dfSelic)
    dfIpca = ajuste_data(dfIpca)
    dfSMin = ajuste_data(dfSMin)
    dfIgpm = ajuste_data(dfIgpm)
    dfInad = ajuste_data(dfInad)
    dfInadFamilia = ajuste_data(dfInadFamilia)
    dfCredTotal = ajuste_data(dfCredTotal)
    dfDolar = ajuste_data(dfDolar)

    # Transformando a taxa Selic para mensal
    dfSelic = dfSelic.set_index('Data').resample('MS').first().reset_index()

    # Derivando as variações
    def variacao(df, coluna_valor, nome_variacao):
        df[nome_variacao] = df[coluna_valor].pct_change() * 100
        return df

    dfSelic = variacao(dfSelic, 'Selic', 'Variacao_Selic')
    dfIpca = variacao(dfIpca, 'Ipca', 'Variacao_Ipca')
    dfSMin = variacao(dfSMin, 'Salario_Minimo', 'Variacao_Salario')
    dfIgpm = variacao(dfIgpm, 'Igpm', 'Variacao_Igpm')
    dfInad = variacao(dfInad, 'Inadimplencia', 'Variacao_Inad')
    dfInadFamilia = variacao(dfInadFamilia, 'Inadimplencia_Familia', 'Variacao_Inad_Familia')
    dfCredTotal = variacao(dfCredTotal, 'CredTotal', 'Variacao_CredTotal')
    dfDolar = variacao(dfDolar, 'Dolar', 'Variacao_Dolar')
    # Integrando os dados
    df_geral = dfSelic.merge(dfIpca, on='Data', how='inner') \
                      .merge(dfSMin, on='Data', how='inner') \
                      .merge(dfIgpm, on='Data', how='inner') \
                      .merge(dfInad, on='Data', how='inner')

    # Indicadores derivados
    df_geral['Salario_Real'] = df_geral['Salario_Minimo'] / (1 + df_geral['Ipca'] / 100)
    df_geral['Diferenca_Inflacao'] = df_geral['Igpm'] - df_geral['Ipca']

    
    # Retornando os DataFrames processados
    return dfSelic, dfIpca, dfSMin, dfIgpm, dfInad, dfInadFamilia, dfCredTotal, dfDolar
