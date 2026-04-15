"""
Análise Individual de Ativos - Page for individual stock/crypto analysis.

This page provides comprehensive analysis of individual assets with:
- Real-time price data and metrics
- Interactive charts with technical indicators
- Performance analytics
- Data export capabilities

Following professional coding patterns and styling conventions.

Author: Stock Analysis Dashboard
Date: 2024
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Optional, Tuple
import logging

from config import (
    THEME_COLORS,
    DEFAULT_ASSETS,
    TIMEFRAME_OPTIONS,
    TIMEFRAME_DEFAULTS,
    CHART_TYPES,
    EMOJIS,
    SMA_COLORS,
    ASSET_COLORS,
    DEFAULT_CHART_HEIGHT,
    DEFAULT_CHART_WIDTH,
    CHART_TEMPLATE,
)

from utils.data_fetcher import fetch_stock_data, get_ticker_info
from utils.indicators import (
    calculate_sma,
    calculate_bollinger_bands,
)
from utils.metrics import calculate_metrics, calculate_returns
from utils.chart_builders import (
    create_line_chart,
    create_candlestick_chart,
    add_sma_to_chart,
    add_bollinger_bands_to_chart,
    create_bar_chart,
)
from utils.formatters import (
    format_currency,
    format_percentage,
    format_volume,
    format_number,
    format_dataframe_for_display,
)
from utils.validators import validate_ticker, validate_date_range, validate_price_data
from utils.styling import (
    apply_custom_css,
    get_color_palette,
    apply_metric_style,
)

# Configure logging
logger = logging.getLogger(__name__)


def create_price_chart_professional(
    data: pd.DataFrame,
    ticker: str,
    chart_type: str = "Linha",
    show_sma: bool = False,
    show_bollinger: bool = False,
) -> go.Figure:
    """
    Create a professional interactive price chart.
    
    Args:
        data: OHLCV DataFrame with price data
        ticker: Asset ticker symbol
        chart_type: 'Linha' (line) or 'Candlestick' chart type
        show_sma: Whether to show Simple Moving Average overlays
        show_bollinger: Whether to show Bollinger Bands overlay
    
    Returns:
        go.Figure: Plotly figure with price chart
        
    Raises:
        ValueError: If data is invalid or missing required columns
    """
    try:
        # Validate input data
        is_valid, msg = validate_price_data(data)
        if not is_valid:
            logger.error(f"Invalid price data: {msg}")
            raise ValueError(msg)
        
        # Get asset color
        color = ASSET_COLORS.get(ticker, THEME_COLORS["primary"])
        
        # Create base chart
        if chart_type == "Candlestick" and all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
            fig = create_candlestick_chart(
                data,
                title=f"{ticker} - Análise de Preço",
                height=DEFAULT_CHART_HEIGHT,
                width=DEFAULT_CHART_WIDTH,
            )
        else:
            # Use professional line chart builder
            fig = create_line_chart(
                data,
                x_col=data.index.name or 'Data',
                y_col='Close',
                title=f"{ticker} - Análise de Preço",
                xaxis_title="Data",
                yaxis_title="Preço",
                height=DEFAULT_CHART_HEIGHT,
                width=DEFAULT_CHART_WIDTH,
                template=CHART_TEMPLATE,
                colors=[color]
            )
        
        # Add SMA indicators
        if show_sma:
            sma_dict = {}
            for period in [20, 50, 200]:
                try:
                    sma = calculate_sma(data, period)
                    sma_dict[period] = sma
                except Exception as e:
                    logger.warning(f"Could not calculate SMA {period}: {e}")
            
            if sma_dict:
                fig = add_sma_to_chart(
                    fig,
                    data,
                    data.index.name or 'Data',
                    'Close',
                    sma_dict,
                    colors=list(SMA_COLORS.values())
                )
        
        # Add Bollinger Bands
        if show_bollinger:
            try:
                upper, middle, lower = calculate_bollinger_bands(data)
                fig = add_bollinger_bands_to_chart(
                    fig,
                    data,
                    data.index.name or 'Data',
                    upper,
                    middle,
                    lower,
                )
            except Exception as e:
                logger.warning(f"Could not add Bollinger Bands: {e}")
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating price chart: {e}")
        raise


def create_returns_chart_professional(
    data: pd.DataFrame,
    ticker: str,
) -> go.Figure:
    """
    Create a professional cumulative returns chart.
    
    Args:
        data: OHLCV DataFrame
        ticker: Asset ticker symbol
    
    Returns:
        go.Figure: Plotly figure with returns chart
    """
    try:
        returns = calculate_returns(data)
        
        fig = create_line_chart(
            returns,
            x_col=returns.index.name or 'Data',
            y_col='Cumulative_Return',
            title=f"{ticker} - Retorno Cumulativo",
            xaxis_title="Data",
            yaxis_title="Retorno (%)",
            height=400,
            width=DEFAULT_CHART_WIDTH,
            template=CHART_TEMPLATE,
            colors=[THEME_COLORS["secondary"]]
        )
        
        # Add zero reference line
        fig.add_hline(
            y=0,
            line_dash="dash",
            line_color="rgba(255, 255, 255, 0.5)",
            annotation_text="Break-even",
            annotation_position="right"
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating returns chart: {e}")
        raise


def create_volume_chart_professional(
    data: pd.DataFrame,
    ticker: str,
) -> Optional[go.Figure]:
    """
    Create a professional volume chart.
    
    Args:
        data: OHLCV DataFrame with Volume column
        ticker: Asset ticker symbol
    
    Returns:
        go.Figure or None: Plotly figure or None if volume data unavailable
    """
    try:
        if "Volume" not in data.columns or data["Volume"].sum() == 0:
            logger.info(f"No volume data available for {ticker}")
            return None
        
        # Create volume bars with price direction coloring
        volume_colors = [
            THEME_COLORS["up"] if (data["Close"].iloc[i] >= data["Close"].iloc[i - 1])
            else THEME_COLORS["down"]
            for i in range(1, len(data))
        ]
        volume_colors.insert(0, THEME_COLORS["primary"])
        
        fig = create_bar_chart(
            data,
            x_col=data.index.name or 'Data',
            y_col='Volume',
            title=f"{ticker} - Volume de Negociação",
            xaxis_title="Data",
            yaxis_title="Volume",
            height=300,
            width=DEFAULT_CHART_WIDTH,
            template=CHART_TEMPLATE,
        )
        
        # Update bar colors for directional indication
        fig.data[0].marker.color = volume_colors
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating volume chart: {e}")
        return None


def display_metrics_cards(metrics: dict, ticker: str) -> None:
    """
    Display key metrics in professional styled cards.
    
    Args:
        metrics: Dictionary of calculated metrics
        ticker: Asset ticker symbol
    """
    try:
        colors = get_color_palette("professional")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            price_change = metrics.get("Variação %", 0)
            st.metric(
                "Preço Atual",
                format_currency(metrics.get("Preço Atual", 0), show_symbol=False),
                f"{format_percentage(price_change, multiplier=1.0)}",
                delta_color="inverse",
            )
        
        with col2:
            st.metric(
                "Máxima (período)",
                format_currency(metrics.get("Preço Máximo", 0), show_symbol=False),
            )
        
        with col3:
            st.metric(
                "Mínima (período)",
                format_currency(metrics.get("Preço Mínimo", 0), show_symbol=False),
            )
        
        with col4:
            st.metric(
                "Volatilidade",
                format_percentage(metrics.get("Volatilidade %", 0), multiplier=1.0),
            )
        
        with col5:
            st.metric(
                "Sharpe Ratio",
                f"{metrics.get('Sharpe Ratio', 0):.2f}",
            )
    
    except Exception as e:
        logger.error(f"Error displaying metrics: {e}")
        st.error("Erro ao exibir métricas")


def display_detailed_metrics(metrics: dict) -> None:
    """
    Display detailed statistical metrics.
    
    Args:
        metrics: Dictionary of calculated metrics
    """
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Retorno Total",
                format_percentage(metrics.get("Retorno Cumulativo %", 0), multiplier=1.0),
            )
        
        with col2:
            st.metric(
                "Max Drawdown",
                format_percentage(metrics.get("Max Drawdown %", 0), multiplier=1.0),
            )
        
        with col3:
            st.metric(
                "Preço Médio",
                format_currency(metrics.get("Preço Médio", 0), show_symbol=False),
            )
        
        with col4:
            st.metric(
                "Volume Médio",
                format_volume(metrics.get("Volume Médio", 0), decimals=0),
            )
    
    except Exception as e:
        logger.error(f"Error displaying detailed metrics: {e}")


def format_data_for_export(data: pd.DataFrame) -> pd.DataFrame:
    """
    Format DataFrame for CSV export with proper formatting.
    
    Args:
        data: Raw DataFrame from data fetcher
    
    Returns:
        pd.DataFrame: Formatted DataFrame ready for export
    """
    try:
        df_export = data.copy()
        
        # Format price columns
        price_columns = ['Open', 'High', 'Low', 'Close']
        for col in price_columns:
            if col in df_export.columns:
                df_export[col] = df_export[col].apply(lambda x: f"{x:.4f}")
        
        # Format volume
        if 'Volume' in df_export.columns:
            df_export['Volume'] = df_export['Volume'].apply(lambda x: f"{x:,.0f}")
        
        return df_export
    
    except Exception as e:
        logger.error(f"Error formatting data for export: {e}")
        return data


# ==================== PAGE SETUP ====================

# Apply custom styling
apply_custom_css()

# Page configuration
st.set_page_config(
    page_title="Análise Individual",
    page_icon=EMOJIS["individual"],
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title
st.title(f"{EMOJIS['individual']} Análise Individual de Ativos")
st.markdown(
    "Análise detalhada de ativos individuais com gráficos interativos e métricas de desempenho.",
    help="Selecione um ativo na barra lateral para começar a análise"
)

# ==================== SIDEBAR CONTROLS ====================

with st.sidebar:
    st.subheader("⚙️ Configurações")
    
    # Asset selection section
    st.subheader("Seleção de Ativo")
    col1, col2 = st.columns(2)
    
    with col1:
        asset_type = st.selectbox(
            "Tipo de Ativo",
            ["Ações BR", "Ações US", "Criptomoedas", "Índices", "Personalizado"],
            key="asset_type_select"
        )
    
    with col2:
        # Get assets based on type
        asset_map = {
            "Ações BR": DEFAULT_ASSETS["stocks_br"],
            "Ações US": DEFAULT_ASSETS["stocks_us"],
            "Criptomoedas": DEFAULT_ASSETS["crypto"],
            "Índices": DEFAULT_ASSETS["indices"],
        }
        assets = asset_map.get(asset_type, [])
    
    if asset_type == "Personalizado":
        ticker = st.text_input(
            "Digite o símbolo do ativo",
            placeholder="ex: AAPL, BTC-USD, ITUB4.SA",
            help="Use o símbolo do ticker conforme disponível no yfinance"
        ).upper().strip()
    else:
        ticker = st.selectbox(
            "Escolha o ativo",
            assets,
            key="asset_select"
        )
    
    # Validate ticker
    if ticker:
        is_valid, error_msg = validate_ticker(ticker)
        if not is_valid:
            st.warning(f"⚠️ {error_msg}")
    
    # Date range section
    st.subheader("Período de Análise")
    timeframe = st.selectbox(
        "Período Pré-definido",
        list(TIMEFRAME_OPTIONS.keys()),
        index=5,  # Default to 1 year
        help="Selecione um período pré-definido de análise"
    )
    timeframe_value = TIMEFRAME_OPTIONS[timeframe]
    
    use_custom_dates = st.checkbox(
        "Usar datas personalizadas",
        value=False,
        help="Marque para especificar datas customizadas"
    )
    
    if use_custom_dates:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data Inicial")
        with col2:
            end_date = st.date_input("Data Final")
        
        # Validate dates if custom
        if start_date and end_date:
            is_valid, error_msg = validate_date_range(start_date, end_date)
            if not is_valid:
                st.error(f"❌ {error_msg}")
    else:
        start_date = None
        end_date = None
    
    # Chart options section
    st.subheader("Opções de Visualização")
    chart_type = st.selectbox(
        "Tipo de Gráfico",
        CHART_TYPES,
        help="Escolha entre gráfico de linhas ou candlestick"
    )
    
    show_sma = st.checkbox(
        "Mostrar Médias Móveis",
        value=False,
        help="Exibe SMA 20, 50 e 200 no gráfico"
    )
    
    show_bollinger = st.checkbox(
        "Mostrar Bandas de Bollinger",
        value=False,
        help="Exibe volatilidade e níveis de sobre-compra/venda"
    )
    
    # Export section
    st.subheader("Exportar Dados")
    download_data = st.checkbox(
        "Preparar download de dados",
        value=False,
        help="Permite exportar dados em formato CSV"
    )

# ==================== MAIN CONTENT ====================

if ticker:
    try:
        # Fetch data
        with st.spinner(f"📥 Buscando dados para {ticker}..."):
            if use_custom_dates and start_date and end_date:
                data = fetch_stock_data(
                    ticker,
                    start_date=start_date,
                    end_date=end_date
                )
            else:
                data = fetch_stock_data(ticker, period=timeframe_value)
        
        if data.empty:
            st.error(f"❌ Nenhum dado encontrado para {ticker}")
            st.info("Verifique se o símbolo está correto e tente novamente")
        else:
            # Get ticker information
            try:
                info = get_ticker_info(ticker)
            except Exception as e:
                logger.warning(f"Could not fetch ticker info: {e}")
                info = {"name": ticker, "currency": "USD"}
            
            # Ticker info header
            st.markdown("### Informações do Ativo")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Ativo", ticker, help="Símbolo do ticker")
            with col2:
                st.metric("Nome", info.get("name", "N/A")[:25])
            with col3:
                st.metric("Moeda", info.get("currency", "USD"))
            with col4:
                st.metric("Dados", f"{len(data)} dias", help=f"Período: {data.index[0]:%d/%m} a {data.index[-1]:%d/%m}")
            
            st.divider()
            
            # Calculate metrics
            metrics = calculate_metrics(data)
            
            # Display key metrics
            st.markdown("### 📊 Métricas Principais")
            display_metrics_cards(metrics, ticker)
            
            st.divider()
            
            # Charts section
            st.markdown("### 📈 Gráficos de Análise")
            
            # Price chart
            try:
                price_chart = create_price_chart_professional(
                    data,
                    ticker,
                    chart_type=chart_type,
                    show_sma=show_sma,
                    show_bollinger=show_bollinger,
                )
                st.plotly_chart(price_chart, use_container_width=True)
            except Exception as e:
                logger.error(f"Error creating price chart: {e}")
                st.error("Erro ao criar gráfico de preço")
            
            # Returns and volume charts
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    returns_chart = create_returns_chart_professional(data, ticker)
                    st.plotly_chart(returns_chart, use_container_width=True)
                except Exception as e:
                    logger.error(f"Error creating returns chart: {e}")
                    st.error("Erro ao criar gráfico de retornos")
            
            with col2:
                try:
                    volume_chart = create_volume_chart_professional(data, ticker)
                    if volume_chart:
                        st.plotly_chart(volume_chart, use_container_width=True)
                    else:
                        st.info("ℹ️ Dados de volume não disponíveis para este ativo")
                except Exception as e:
                    logger.error(f"Error creating volume chart: {e}")
                    st.error("Erro ao criar gráfico de volume")
            
            # Additional metrics
            st.markdown("### 📋 Estatísticas Detalhadas")
            display_detailed_metrics(metrics)
            
            st.divider()
            
            # Data export section
            if download_data:
                st.markdown("### 📥 Exportar Dados")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Export button
                    df_export = format_data_for_export(data)
                    csv = df_export.to_csv()
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{ticker}_dados_{pd.Timestamp.now():%Y%m%d}.csv",
                        mime="text/csv",
                        help="Baixe os dados em formato CSV"
                    )
                
                with col2:
                    st.info("ℹ️ Os dados serão exportados com formatação de preços e volumes")
                
                # Data preview
                st.markdown("#### Prévia dos Dados (últimas 10 linhas)")
                st.dataframe(
                    data.tail(10),
                    use_container_width=True,
                    height=300
                )

    except Exception as e:
        logger.error(f"Error processing {ticker}: {e}")
        st.error(f"❌ Erro ao processar {ticker}")
        st.info(
            "Possíveis causas:\n"
            "- Símbolo do ticker incorreto\n"
            "- Dados não disponíveis para o período\n"
            "- Problema de conexão\n\n"
            "Tente novamente ou verifique o símbolo (ex: AAPL, BTC-USD, ITUB4.SA)"
        )

else:
    # Initial state
    st.info(
        "👈 **Comece:** Selecione um ativo na barra lateral para análise detalhada\n\n"
        "**Recursos disponíveis:**\n"
        "- 📈 Gráficos interativos de preço\n"
        "- 📊 Métricas de desempenho\n"
        "- 🔧 Indicadores técnicos (SMA, Bollinger)\n"
        "- 📥 Exportação de dados em CSV"
    )
