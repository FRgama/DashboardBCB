from module.PreparacaoDeDados import carregar_dados
import streamlit as st
import pandas as pd
import plotly.express as px

dfs = carregar_dados()

df_merged = dfs[0]
for df in dfs[1:]:
    df_merged = pd.merge(df_merged, df, on="Data", how="inner")

st.title("Resumo e Interpretações de Indicadores Econômicos")
st.sidebar.image('https://raw.githubusercontent.com/FRgama/EconoVision/main/imagens/EconoVisionLogo.png'
        )
st.sidebar.markdown(
            """
            <hr style="margin-top: 20px;">
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


def show_analysis(title, desc, x, y):
    st.markdown(f"### {title}")
    st.markdown(desc)
    fig = px.scatter(df_merged, x=x, y=y, trendline="ols", title=f"{x} vs {y}")
    st.plotly_chart(fig)
    st.markdown("---")
st.markdown("""
## 🧾 Descrição dos Indicadores Econômicos

### 🏦 Selic (Taxa Básica de Juros)
A Selic é a taxa básica de juros da economia brasileira, definida pelo Banco Central. Ela influencia diretamente todas as outras taxas de juros do país, como as cobradas em empréstimos, financiamentos e rendimentos de investimentos. Quando a Selic aumenta, o crédito tende a ficar mais caro, o que reduz o consumo e ajuda a conter a inflação.

### 📈 IPCA (Índice de Preços ao Consumidor Amplo)
É o índice oficial de inflação do Brasil, calculado pelo IBGE. Mede a variação de preços de um conjunto de produtos e serviços consumidos pelas famílias. É usado como referência para metas de inflação do governo.

### 💼 Remuneração Média Deflacionada
Refere-se ao rendimento médio real dos trabalhadores, já descontada a inflação. Um aumento neste indicador significa que o poder de compra da população está aumentando, o que pode impactar o consumo, endividamento e capacidade de pagamento.

### 📊 IGP-M (Índice Geral de Preços – Mercado)
É um índice de inflação calculado pela FGV e amplamente utilizado para reajustes de contratos (como aluguel). Ele reflete a variação de preços em diferentes estágios da economia, como atacado, construção civil e consumidor final.

### ❗ Inadimplência
Mede o percentual de operações de crédito em atraso no sistema financeiro. Altas taxas de inadimplência indicam dificuldades generalizadas da população ou empresas em manter os pagamentos em dia.

### 👨‍👩‍👧‍👦 Inadimplência das Famílias
É um recorte da inadimplência que considera exclusivamente pessoas físicas. Está relacionada com o endividamento familiar, desemprego, inflação e variações na renda.

### 💳 Crédito Total
Representa o total de crédito concedido pelo sistema financeiro, incluindo pessoas físicas e jurídicas. Esse indicador mostra a disponibilidade de capital na economia e o grau de atividade financeira.

### 💵 Dólar
Cotação da moeda americana em relação ao real. O dólar afeta importações, exportações, inflação, investimentos e expectativas do mercado. Seu comportamento está ligado a fatores internos (como política econômica) e externos (como juros dos EUA).

---
""")



# Análises de interesse
show_analysis(
    "📉 Selic vs IGP-M",
    "**Correlação negativa forte (-0.54)**: Alta da Selic tende a conter inflação medida pelo IGP-M.",
    "Selic", "Igpm"
)

show_analysis(
    "💳 Selic vs Inadimplência",
    "**Correlação positiva (0.64)**: Juros maiores tornam o crédito mais caro, aumentando inadimplência.",
    "Selic", "Inadimplência"
)

show_analysis(
    "🏦 Crédito Total vs Inadimplência Familiar",
    "**Correlação fortíssima (0.90)**: Mais crédito disponível aumenta o risco de inadimplência nas famílias.",
    "Crédito Total", "Inadimplência Familiar"
)

show_analysis(
    "💼 Remuneração Média vs Crédito Total",
    "**Correlação moderada (0.29)**: Melhora na renda pode estimular o aumento do crédito.",
    "Remuneração Média Deflacionada", "Crédito Total"
)

show_analysis(
    "💼 Remuneração Média vs Inadimplência Familiar",
    "**Correlação fraca (0.15)**: Pode haver impacto, mas outros fatores como juros e desemprego pesam mais.",
    "Remuneração Média Deflacionada", "Inadimplência Familiar"
)
