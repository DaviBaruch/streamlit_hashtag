"""
Stock & Crypto Analysis Dashboard - Main Application Entry Point.

Professional multi-page Streamlit application for stock and cryptocurrency analysis
with technical indicators, portfolio simulation, and comparative analysis.

Following professional coding patterns and styling conventions.

Author: Stock Analysis Dashboard
Date: 2024
"""

import streamlit as st
from config import (
    PAGE_ICON,
    PAGE_TITLE,
    LAYOUT,
    THEME_COLORS,
    EMOJIS,
    DEFAULT_ASSETS,
)
from utils.styling import apply_custom_css, get_color_palette

# ==================== PAGE SETUP ====================

# Apply professional styling
apply_custom_css()

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
)

# ==================== SIDEBAR ====================

with st.sidebar:
    # Sidebar header with icon
    st.markdown(f"### {PAGE_ICON} {PAGE_TITLE}")
    
    st.markdown("---")
    
    # About section
    st.subheader("📌 Sobre o Dashboard")
    st.markdown(
        """
        Dashboard profissional para análise técnica de:
        - 📊 Ações Brasileiras
        - 🇺🇸 Ações Americanas  
        - 🪙 Criptomoedas
        - 📈 Índices Econômicos
        
        **Recursos:**
        - Análise individual detalhada
        - Comparação entre múltiplos ativos
        - Simulador de portfólio
        - Indicadores técnicos avançados
        """
    )
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Ativos Disponíveis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Ações BR",
            len(DEFAULT_ASSETS["stocks_br"]),
            help="Ações da Bolsa de Valores do Brasil"
        )
    with col2:
        st.metric(
            "Ações US",
            len(DEFAULT_ASSETS["stocks_us"]),
            help="Ações do mercado americano"
        )
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Criptomoedas",
            len(DEFAULT_ASSETS["crypto"]),
            help="Principais criptomoedas em USD"
        )
    with col2:
        st.metric(
            "Índices",
            len(DEFAULT_ASSETS["indices"]),
            help="Índices econômicos principais"
        )
    
    st.markdown("---")
    
    # Usage tips
    st.subheader("💡 Dicas de Uso")
    with st.expander("Navegação"):
        st.markdown(
            """
            1. Acesse as **4 seções** via menu lateral
            2. Ajuste os **parâmetros** na barra lateral
            3. **Interaja** com os gráficos Plotly
            4. **Exporte** dados em CSV quando necessário
            """
        )
    
    with st.expander("Gráficos Interativos"):
        st.markdown(
            """
            - 🔍 **Zoom**: Arraste para selecionar área
            - 📍 **Pan**: Use dois dedos/Shift+Drag
            - 📋 **Legenda**: Clique para ativar/desativar
            - 💾 **Download**: Ícone de câmera no canto
            - ⚙️ **Opções**: Menu contextual à direita
            """
        )
    
    with st.expander("Indicadores Técnicos"):
        st.markdown(
            """
            - **SMA**: Tendência de curto/longo prazo
            - **Bollinger**: Volatilidade e extremos
            - **RSI**: Momentum e níveis extremos
            - **MACD**: Mudanças de tendência
            """
        )

# ==================== MAIN CONTENT ====================

# Main title
st.markdown(
    f"<h1>{PAGE_ICON} {PAGE_TITLE}</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    ## 🎯 Bem-vindo ao Dashboard de Análise Profissional
    
    Ferramenta completa para análise técnica, fundamentalista e simulação de portfólio
    em tempo real com dados de múltiplas fontes.
    """
)

# ==================== FEATURES SECTION ====================

st.markdown("---")
st.markdown("## 📊 Funcionalidades Principais")

# Feature cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        ### 📈 Análise Individual
        
        - Dados em tempo real
        - Múltiplos indicadores
        - Métricas detalhadas
        - Download de dados
        """
    )

with col2:
    st.markdown(
        """
        ### ⚖️ Comparação
        
        - Compare 2+ ativos
        - Performance relativa
        - Análise de correlação
        - Tabelas detalhadas
        """
    )

with col3:
    st.markdown(
        """
        ### 💼 Portfólio
        
        - Simulação de alocação
        - Métricas agregadas
        - Contribuição por ativo
        - Análise de risco
        """
    )

with col4:
    st.markdown(
        """
        ### 📊 Indicadores
        
        - SMA, Bollinger, RSI
        - MACD e sinais
        - Análise de volume
        - Sinais de trading
        """
    )

# ==================== HOW TO USE SECTION ====================

st.markdown("---")
st.markdown("## 🚀 Como Usar o Dashboard")

with st.expander("1️⃣ Selecionando um Ativo", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Passo a passo:**
            1. Acesse **"Análise Individual"**
            2. Selecione o **tipo de ativo**
            3. Escolha o **símbolo desejado**
            4. Defina o **período de análise**
            5. Ative os **indicadores** desejados
            """
        )
    with col2:
        st.info(
            """
            **Exemplos de tickers:**
            - Ações BR: `ITUB4.SA`, `PETR4.SA`
            - Ações US: `AAPL`, `MSFT`
            - Crypto: `BTC-USD`, `ETH-USD`
            - Índices: `^BVSP`, `^GSPC`
            """
        )

with st.expander("2️⃣ Analisando Dados"):
    st.markdown(
        """
        **Métricas Disponíveis:**
        - 💰 Preço Atual e Histórico
        - 📊 Volume de Negociação
        - 📈 Retorno Cumulativo
        - 🎯 Volatilidade Anualizada
        - ⚡ Sharpe Ratio
        - 📉 Drawdown Máximo
        
        **Gráficos Interativos:**
        - Clique na legenda para alternar séries
        - Arraste para fazer zoom
        - Passe o mouse para ver detalhes
        - Use os ícones para salvar imagens
        """
    )

with st.expander("3️⃣ Comparando Ativos"):
    st.markdown(
        """
        - Selecione **2 ou mais ativos**
        - Visualize **preços normalizados** (base 100)
        - Compare **performance absoluta**
        - Analise **correlação** entre ativos
        - Exporte **métricas detalhadas**
        """
    )

with st.expander("4️⃣ Simulando Portfólio"):
    st.markdown(
        """
        - Defina o **investimento inicial**
        - Adicione **ativos e pesos**
        - Visualize **evolução histórica**
        - Analise **contribuição por ativo**
        - Compare com **índices de referência**
        """
    )

# ==================== TECHNICAL INFO SECTION ====================

st.markdown("---")
st.markdown("## 🛠️ Informações Técnicas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Dados:**")
    st.markdown(
        """
        - Fonte: **yfinance**
        - Atualização: em tempo real
        - Histórico: até 5 anos
        - Intervalo: diário
        """
    )

with col2:
    st.markdown("**Tecnologias:**")
    st.markdown(
        """
        - **Streamlit**: Interface
        - **Plotly**: Visualizações
        - **Pandas**: Processamento
        - **NumPy**: Cálculos numéricos
        """
    )

# ==================== FOOTER ====================

st.markdown("---")

footer_cols = st.columns(3)

with footer_cols[0]:
    st.markdown(
        """
        **🔗 Links Úteis**
        - [Streamlit Docs](https://docs.streamlit.io)
        - [yfinance](https://github.com/ranaroussi/yfinance)
        - [Plotly](https://plotly.com)
        """
    )

with footer_cols[1]:
    st.markdown(
        """
        **📞 Suporte**
        - Verificar nomes de tickers
        - Garantir conexão internet
        - Limpar cache do navegador
        """
    )

with footer_cols[2]:
    st.markdown(
        """
        **📝 Versão**
        - v2.0 - Professional
        - 2024
        - Código melhorado
        """
    )

st.markdown(
    """
    ---
    <div style='text-align: center; color: #888; padding: 1rem;'>
        <p>💡 Dashboard de Análise de Ações e Criptomoedas</p>
        <p>Desenvolvido com Streamlit, Plotly e boas práticas de código</p>
    </div>
    """,
    unsafe_allow_html=True,
)
