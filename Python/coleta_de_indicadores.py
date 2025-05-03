#Importando a biblioteca bcb e matplotlib para plotar os dados
from bcb import sgs
import matplotlib.pyplot as plt



#Começando pela taxa Selic
def plotar_selic():

    selic = sgs.get({'Selic' : 1178}, start='2010-01-01')
    dfSelic = selic.reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(dfSelic.Date, dfSelic.Selic)
    plt.title('Taxa Selic')
    plt.xlabel('Data')
    plt.ylabel('Taxa Selic')
    plt.title('Evolução da Taxa Selic')
    plt.xlabel('Data')
    plt.ylabel('Taxa Selic')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

plotar_selic()

#Agregando dados do Ipca
def plotar_ipca():
    
    ipca = sgs.get({'Ipca': 4449}, start='2020-01-01')
    dfIpca = ipca.reset_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(dfIpca.Date, dfIpca.Ipca)
    plt.title('IPCA')
    plt.xlabel('Data')
    plt.ylabel('IPCA')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

plotar_ipca()

#Agregando dados do IGP-M
def plotar_igpm():
    
    igpm = sgs.get({'Igpm': 189}, start='2020-01-01')
    dfIgpm = igpm.reset_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(dfIgpm.Date, dfIgpm.Igpm)
    plt.title('IGP-M')
    plt.xlabel('Data')
    plt.ylabel('IGP-M')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

plotar_igpm()

#Agregando dados do Cambio para Dolar
def plotar_cambio():
    
    cambio = sgs.get({'Cambio': 1}, start='2020-01-01')
    dfCambio = cambio.reset_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(dfCambio.Date, dfCambio.Cambio)
    plt.title('Cambio')
    plt.xlabel('Data')
    plt.ylabel('Cambio')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

plotar_cambio()

#Criando uma função que possa plotar qualquer indicador
def plotar_indicador(indicador, nome):
    
    indicador = sgs.get({nome: indicador}, start='2020-01-01')
    dfIndicador = indicador.reset_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(dfIndicador['Date'], dfIndicador[nome])
    plt.title(nome)
    plt.xlabel('Data')
    plt.ylabel(nome)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
#teste com indicador aleatório
plotar_indicador(3691, 'Dolar Anual')
