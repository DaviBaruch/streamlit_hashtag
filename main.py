import pandas as pd 
import streamlit as st      
import yfinance as yf

def carregar_dados(empresa):
    try:
        dados_acao = yf.Ticker(empresa)
        precos_acao = dados_acao.history(start='2016-01-01')

        # verifica se veio vazio
        if precos_acao is None or precos_acao.empty:
            st.error("Não foi possível carregar os dados da ação.")
            return None

        precos_acao.reset_index(inplace=True)
        return precos_acao

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return None

dados = carregar_dados("ITUB4.SA")

if dados is not None:
    st.line_chart(dados.set_index("Date")["Close"])