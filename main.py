import pandas as pd 
import streamlit as st      
import yfinance as yf

st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos
""")

def carregar_dados(empresa):
    texto_tickers = " ".join(empresa)
    dados_acao = yf.Tickers(texto_tickers)
    precos_acao = dados_acao.history(start='2016-01-01')
    # verifica se veio vazio
    return precos_acao

# cria lista de carteiras
acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "GGBR4", "BBDC4.SA", "ABEV3.SA", "BITCOIN-USD"]


#variável para armazenar a ação selecionada
dados = carregar_dados(acoes)
# filtro correto


lista_acoes = st.multiselect("Selecione as ações para exibir o gráfico:", acoes)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

    dados = yf.download(lista_acoes, start='2016-01-01')

    dados = dados["Close"]

    # 🔥 GARANTE QUE SEMPRE SEJA DATAFRAME
    if isinstance(dados, pd.Series):
        dados = dados.to_frame()

    dados.reset_index(inplace=True)

st.line_chart(dados["Close"])

