"""Página de análise de indicadores técnicos."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import (
    DEFAULT_ASSETS,
    TIMEFRAME_OPTIONS,
    INDICATORS_CONFIG,
    EMOJIS,
    THEME_COLORS,
)
from utils.data_fetcher import fetch_stock_data
from utils.indicators import (
    add_all_indicators,
    calculate_sma,
    calculate_bollinger_bands,
    calculate_rsi,
    calculate_macd,
    get_trading_signals,
)


def create_price_with_sma_chart(
    data: pd.DataFrame, ticker: str, periods: list = [20, 50, 200]
) -> go.Figure:
    """
    Create price chart with SMA lines.
    
    Args:
        data: OHLCV data
        ticker: Ticker symbol
        periods: SMA periods
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()

    # Price line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Preço",
            line=dict(color=THEME_COLORS["primary"], width=2),
        )
    )

    # SMA lines
    colors = ["#EF553B", "#00CC96", "#AB63FA"]
    for idx, period in enumerate(periods):
        sma = calculate_sma(data, period)
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=sma,
                mode="lines",
                name=f"SMA {period}",
                line=dict(width=1, dash="dash", color=colors[idx % len(colors)]),
            )
        )

    fig.update_layout(
        title=f"{ticker} - Preço com Médias Móveis",
        xaxis_title="Data",
        yaxis_title="Preço (USD)",
        hovermode="x unified",
        template="plotly_dark",
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


def create_bollinger_bands_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Create Bollinger Bands chart.
    
    Args:
        data: OHLCV data
        ticker: Ticker symbol
    
    Returns:
        Plotly figure
    """
    upper, middle, lower = calculate_bollinger_bands(data)

    fig = go.Figure()

    # Upper band
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=upper,
            fill=None,
            mode="lines",
            line_color="rgba(255, 255, 255, 0)",
            showlegend=False,
        )
    )

    # Lower band
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=lower,
            fill="tonexty",
            mode="lines",
            line_color="rgba(255, 255, 255, 0)",
            name="Bandas de Bollinger",
            fillcolor="rgba(100, 100, 100, 0.2)",
        )
    )

    # Middle band (SMA)
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=middle,
            mode="lines",
            name="Média (SMA 20)",
            line=dict(color=THEME_COLORS["warning"], width=1),
        )
    )

    # Price
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Preço",
            line=dict(color=THEME_COLORS["primary"], width=2),
        )
    )

    fig.update_layout(
        title=f"{ticker} - Bandas de Bollinger",
        xaxis_title="Data",
        yaxis_title="Preço (USD)",
        hovermode="x unified",
        template="plotly_dark",
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


def create_rsi_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Create RSI chart.
    
    Args:
        data: OHLCV data
        ticker: Ticker symbol
    
    Returns:
        Plotly figure
    """
    rsi = calculate_rsi(data)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=rsi,
            mode="lines",
            name="RSI (14)",
            line=dict(color=THEME_COLORS["info"], width=2),
        )
    )

    # Add reference lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrevenda")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobrevenda")
    fig.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_layout(
        title=f"{ticker} - Índice de Força Relativa (RSI)",
        xaxis_title="Data",
        yaxis_title="RSI",
        yaxis=dict(range=[0, 100]),
        hovermode="x unified",
        template="plotly_dark",
        height=350,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


def create_macd_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Create MACD chart.
    
    Args:
        data: OHLCV data
        ticker: Ticker symbol
    
    Returns:
        Plotly figure
    """
    macd, signal, histogram = calculate_macd(data)

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Preço", "MACD"),
        vertical_spacing=0.1,
    )

    # Price
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Preço",
            line=dict(color=THEME_COLORS["primary"], width=2),
        ),
        row=1,
        col=1,
    )

    # MACD
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=macd,
            mode="lines",
            name="MACD",
            line=dict(color=THEME_COLORS["secondary"], width=1),
        ),
        row=2,
        col=1,
    )

    # Signal line
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=signal,
            mode="lines",
            name="Signal",
            line=dict(color=THEME_COLORS["warning"], width=1),
        ),
        row=2,
        col=1,
    )

    # Histogram
    colors = [
        THEME_COLORS["up"] if h >= 0 else THEME_COLORS["down"] for h in histogram
    ]
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=histogram,
            name="Histogram",
            marker_color=colors,
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        title=f"{ticker} - MACD",
        height=600,
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


### Page configuration
##st.set_page_config(
##    page_title="Indicadores Técnicos",
##    page_icon=EMOJIS["indicators"],
##    layout="wide",
##)

apply_custom_css()

st.title(f"{EMOJIS['indicators']} Análise de Indicadores Técnicos")

# Sidebar controls
with st.sidebar:
    st.subheader("⚙️ Configurações")

    # Ticker selection
    st.subheader("Seleção de Ativo")
    col1, col2 = st.columns(2)
    with col1:
        asset_type = st.selectbox(
            "Tipo de Ativo",
            ["Ações BR", "Ações US", "Criptomoedas", "Índices"],
            key="ind_asset_type",
        )
    with col2:
        if asset_type == "Ações BR":
            assets = DEFAULT_ASSETS["stocks_br"]
        elif asset_type == "Ações US":
            assets = DEFAULT_ASSETS["stocks_us"]
        elif asset_type == "Criptomoedas":
            assets = DEFAULT_ASSETS["crypto"]
        else:
            assets = DEFAULT_ASSETS["indices"]

    ticker = st.selectbox("Escolha o ativo", assets, key="ind_ticker")

    # Timeframe
    st.subheader("Período")
    timeframe = st.selectbox(
        "Período Pré-definido",
        list(TIMEFRAME_OPTIONS.keys()),
        key="ind_timeframe",
        index=3,  # Default to 3 months
    )
    timeframe_value = TIMEFRAME_OPTIONS[timeframe]

    # Indicator selection
    st.subheader("Indicadores")
    show_sma = st.checkbox("Médias Móveis (SMA)", value=True)
    show_bollinger = st.checkbox("Bandas de Bollinger", value=False)
    show_rsi = st.checkbox("RSI (Força Relativa)", value=False)
    show_macd = st.checkbox("MACD", value=False)

# Main content
if ticker:
    try:
        with st.spinner(f"Buscando dados para {ticker}..."):
            data = fetch_stock_data(ticker, period=timeframe_value)

        if data.empty:
            st.error(f"Nenhum dado encontrado para {ticker}")
        else:
            st.subheader(f"📈 Indicadores Técnicos para {ticker}")

            # SMA Chart
            if show_sma:
                sma_chart = create_price_with_sma_chart(data, ticker)
                st.plotly_chart(sma_chart, use_container_width=True)

            # Bollinger Bands Chart
            if show_bollinger:
                bb_chart = create_bollinger_bands_chart(data, ticker)
                st.plotly_chart(bb_chart, use_container_width=True)

            # RSI Chart
            if show_rsi:
                rsi_chart = create_rsi_chart(data, ticker)
                st.plotly_chart(rsi_chart, use_container_width=True)

            # MACD Chart
            if show_macd:
                macd_chart = create_macd_chart(data, ticker)
                st.plotly_chart(macd_chart, use_container_width=True)

            if not any([show_sma, show_bollinger, show_rsi, show_macd]):
                st.info(
                    "👈 Selecione pelo menos um indicador na barra lateral para visualizar"
                )

            # Trading Signals
            st.subheader("🎯 Sinais de Negociação")
            signals = get_trading_signals(data, method="sma_crossover")
            last_signal = signals["Signal"].iloc[-1]
            signal_text = (
                "🟢 COMPRA" if last_signal == 1 else "🔴 VENDA" if last_signal == -1 else "⚪ NEUTRO"
            )
            st.metric("Sinal Atual (SMA Crossover)", signal_text)

            # Information
            st.subheader("📚 Informações sobre os Indicadores")
            with st.expander("ℹ️ O que significam os indicadores?"):
                st.markdown(
                    f"""
                    ### Médias Móveis (SMA)
                    - Suavizam os dados de preço para identificar tendências
                    - **SMA 20**: Curto prazo
                    - **SMA 50**: Médio prazo
                    - **SMA 200**: Longo prazo
                    
                    ### Bandas de Bollinger
                    - Indicam volatilidade do ativo
                    - Preço próximo à banda superior = sobrecomprado
                    - Preço próximo à banda inferior = sobrevendido
                    
                    ### RSI (Relative Strength Index)
                    - Varia de 0 a 100
                    - **RSI > 70**: Sobrecomprado (sinal de venda)
                    - **RSI < 30**: Sobrevendido (sinal de compra)
                    - **Período**: {INDICATORS_CONFIG['rsi']['period']} dias
                    
                    ### MACD
                    - Linha MACD cruza acima da Signal = Sinal de Compra
                    - Linha MACD cruza abaixo da Signal = Sinal de Venda
                    - Histogram mostra a diferença entre MACD e Signal
                    """
                )

    except Exception as e:
        st.error(f"❌ Erro ao processar {ticker}: {str(e)}")
else:
    st.info("👈 Selecione um ativo na barra lateral para começar")
