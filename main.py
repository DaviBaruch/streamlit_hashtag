import pandas as pd 
import streamlit as st      
import yfinance as yf

st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos
""")

def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    precos_acao = dados_acao.history(
    period='1y'
)
    # precos_acao = pd.read_csv("BaseItau.csv")
    # precos_acao["Date"] = pd.to_datetime(precos_acao["Date"])
    # precos_acao = precos_acao.set_index("Date")
    precos_acao = precos_acao[["Close"]]
    return precos_acao

dados  = carregar_dados("ITUB4.SA")
print(dados)
grafico = st.line_chart(dados)

st.write("""
# Fim do app
""")

