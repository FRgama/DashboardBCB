import pandas as pd
from bcb import sgs

def carregar_dados():
    def obter_dado(codigo, nome):
        try:
            df = sgs.get({nome: codigo}, start='2020-01-01')
            df = df.reset_index()
            df.columns = ['Data', nome]
            df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
            return df
        except Exception as e:
            print(f"Erro ao carregar {nome}: {e}")
            return pd.DataFrame(columns=['Data', nome])

    dfSelic = obter_dado(1178, 'Selic')
    dfIpca = obter_dado(433, 'Ipca')
    dfSMin = obter_dado(1619, 'Salario_Minimo')
    dfIgpm = obter_dado(189, 'Igpm')
    dfInad = obter_dado(21082, 'Inadimplencia')
    dfInadFamilia = obter_dado(29038, 'Inadimplencia_Familia')
    dfCredTotal = obter_dado(20631, 'CredTotal')
    dfDolar = obter_dado(1, 'Dolar')

    # Ajuste Selic para frequência mensal
    if not dfSelic.empty:
        dfSelic = dfSelic.set_index('Data').resample('MS').first().reset_index()

    return dfSelic, dfIpca, dfSMin, dfIgpm, dfInad, dfInadFamilia, dfCredTotal, dfDolar
