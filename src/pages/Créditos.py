import streamlit as st

st.title("Sobre o Projeto")
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
st.markdown("""
## Grupo de Análise Econômica



### Integrantes:
- **Beatriz de Souza Santos Rio Branco**  
- **Sátiro Gabriel de Souza Santos**  
- **Sabrinna Cristina Gomes Vicente**  
- **Rodrigo Correa da Gama**  
---

Este painel foi desenvolvido como parte de um trabalho acadêmico para explorar indicadores econômicos usando Python e Streamlit.
""")
