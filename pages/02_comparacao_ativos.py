"""
Comparação de Ativos - Multi-asset comparison and performance analysis.

This page enables comparison of multiple assets with:
- Normalized price comparison
- Performance metrics
- Correlation analysis
- Detailed metrics table

Following professional coding patterns from reference repository.

Author: Stock Analysis Dashboard
Date: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional
import logging

from config import (
    THEME_COLORS,
    DEFAULT_ASSETS,
    TIMEFRAME_OPTIONS,
    TIMEFRAME_DEFAULTS,
    EMOJIS,
    ASSET_COLORS,
    DEFAULT_CHART_HEIGHT,
    DEFAULT_CHART_WIDTH,
    CHART_TEMPLATE,
)

from utils.data_fetcher import fetch_multiple_tickers
from utils.metrics import (
    normalize_price,
    calculate_metrics,
    calculate_correlation_matrix,
    calculate_returns,
)
from utils.chart_builders import (
    create_line_chart,
    create_bar_chart,
    create_heatmap,
)
from utils.formatters import format_percentage, format_currency
from utils.validators import validate_ticker, validate_date_range
from utils.styling import apply_custom_css, get_asset_color

logger = logging.getLogger(__name__)


def create_normalized_comparison_chart(
    data_dict: Dict[str, pd.DataFrame],
    base: float = 100,
) -> go.Figure:
    """
    Create normalized price comparison chart.
    
    Args:
        data_dict: Dictionary mapping ticker -> DataFrame
        base: Base value for normalization (default: 100)
    
    Returns:
        go.Figure: Plotly figure with normalized prices
    """
    try:
        # Normalize all data
        normalized_data = {}
        for ticker, df in data_dict.items():
            if not df.empty and 'Close' in df.columns:
                normalized_data[ticker] = normalize_price(df, base=base)
        
        if not normalized_data:
            return None
        
        # Create DataFrame with all normalized prices
        df_normalized = pd.DataFrame(normalized_data)
        
        fig = create_line_chart(
            df_normalized,
            x_col=df_normalized.index.name or 'Data',
            y_col=list(df_normalized.columns),
            title="Comparação de Preços Normalizados (Base 100)",
            xaxis_title="Data",
            yaxis_title="Preço Normalizado",
            height=DEFAULT_CHART_HEIGHT,
            width=DEFAULT_CHART_WIDTH,
            template=CHART_TEMPLATE,
            colors=[get_asset_color(ticker) for ticker in df_normalized.columns]
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating normalized comparison chart: {e}")
        return None


def create_correlation_heatmap(data_dict: Dict[str, pd.DataFrame]) -> Optional[go.Figure]:
    """
    Create correlation heatmap for selected assets.
    
    Args:
        data_dict: Dictionary mapping ticker -> DataFrame
    
    Returns:
        go.Figure: Plotly heatmap or None if error
    """
    try:
        if len(data_dict) < 2:
            return None
        
        # Extract close prices
        close_prices = {}
        for ticker, df in data_dict.items():
            if not df.empty and 'Close' in df.columns:
                close_prices[ticker] = df['Close']
        
        if len(close_prices) < 2:
            return None
        
        # Create correlation matrix
        corr_matrix = calculate_correlation_matrix(pd.DataFrame(close_prices))
        
        fig = create_heatmap(
            corr_matrix,
            title="Matriz de Correlação",
            height=500,
            width=600,
            template=CHART_TEMPLATE,
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating correlation heatmap: {e}")
        return None


def create_performance_comparison_chart(
    data_dict: Dict[str, pd.DataFrame],
) -> Optional[go.Figure]:
    """
    Create bar chart comparing total returns.
    
    Args:
        data_dict: Dictionary mapping ticker -> DataFrame
    
    Returns:
        go.Figure: Plotly bar chart or None if error
    """
    try:
        returns_data = {}
        for ticker, df in data_dict.items():
            if not df.empty and 'Close' in df.columns:
                first_price = df['Close'].iloc[0]
                last_price = df['Close'].iloc[-1]
                return_pct = ((last_price - first_price) / first_price) * 100
                returns_data[ticker] = return_pct
        
        if not returns_data:
            return None
        
        # Create DataFrame for bar chart
        df_returns = pd.DataFrame(
            {'Retorno': list(returns_data.values())},
            index=list(returns_data.keys())
        )
        
        fig = create_bar_chart(
            df_returns.reset_index().rename(columns={'index': 'Ativo'}),
            x_col='Ativo',
            y_col='Retorno',
            title="Retorno Total por Ativo",
            xaxis_title="Ativo",
            yaxis_title="Retorno (%)",
            height=400,
            width=DEFAULT_CHART_WIDTH,
            template=CHART_TEMPLATE,
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating performance chart: {e}")
        return None


def display_comparison_metrics(data_dict: Dict[str, pd.DataFrame]) -> None:
    """
    Display comparison metrics for selected assets.
    
    Args:
        data_dict: Dictionary mapping ticker -> DataFrame
    """
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        # Count available assets
        with col1:
            st.metric("Ativos Carregados", len([d for d in data_dict.values() if not d.empty]))
        
        # Calculate average price
        with col2:
            avg_prices = []
            for df in data_dict.values():
                if not df.empty and 'Close' in df.columns:
                    avg_prices.append(df['Close'].mean())
            
            if avg_prices:
                st.metric("Preço Médio Geral", f"${np.mean(avg_prices):.2f}")
        
        # Best performer
        with col3:
            best_ticker = None
            best_return = -float('inf')
            for ticker, df in data_dict.items():
                if not df.empty and 'Close' in df.columns:
                    ret = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                    if ret > best_return:
                        best_return = ret
                        best_ticker = ticker
            
            if best_ticker:
                st.metric("Melhor Ativo", best_ticker, f"{best_return:.2f}%")
        
        # Worst performer
        with col4:
            worst_ticker = None
            worst_return = float('inf')
            for ticker, df in data_dict.items():
                if not df.empty and 'Close' in df.columns:
                    ret = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
                    if ret < worst_return:
                        worst_return = ret
                        worst_ticker = ticker
            
            if worst_ticker:
                st.metric("Pior Ativo", worst_ticker, f"{worst_return:.2f}%")
    
    except Exception as e:
        logger.error(f"Error displaying comparison metrics: {e}")


def create_metrics_table(data_dict: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Create detailed metrics table for all assets.
    
    Args:
        data_dict: Dictionary mapping ticker -> DataFrame
    
    Returns:
        pd.DataFrame: Metrics table or None if error
    """
    try:
        metrics_list = []
        
        for ticker, df in data_dict.items():
            if not df.empty:
                metrics = calculate_metrics(df)
                metrics_list.append({
                    'Ativo': ticker,
                    'Preço Atual': format_currency(metrics.get('Preço Atual', 0), show_symbol=False),
                    'Máxima': format_currency(metrics.get('Preço Máximo', 0), show_symbol=False),
                    'Mínima': format_currency(metrics.get('Preço Mínimo', 0), show_symbol=False),
                    'Retorno': format_percentage(metrics.get('Variação %', 0), multiplier=1.0),
                    'Volatilidade': format_percentage(metrics.get('Volatilidade %', 0), multiplier=1.0),
                    'Sharpe Ratio': f"{metrics.get('Sharpe Ratio', 0):.2f}",
                })
        
        return pd.DataFrame(metrics_list) if metrics_list else None
    
    except Exception as e:
        logger.error(f"Error creating metrics table: {e}")
        return None


# ==================== PAGE SETUP ====================

apply_custom_css()

st.set_page_config(
    page_title="Comparação de Ativos",
    page_icon=EMOJIS["comparison"],
    layout="wide",
)

st.title(f"{EMOJIS['comparison']} Comparação de Ativos")
st.markdown("Compare múltiplos ativos com análise de performance e correlação")

# ==================== SIDEBAR CONTROLS ====================

with st.sidebar:
    st.subheader("⚙️ Configurações")
    
    # Asset selection
    st.subheader("Seleção de Ativos")
    
    col1, col2 = st.columns(2)
    with col1:
        asset_type = st.selectbox(
            "Tipo de Ativo",
            ["Múltiplos", "Ações BR", "Ações US", "Criptomoedas", "Personalizado"],
        )
    
    # Asset list selection
    asset_map = {
        "Ações BR": DEFAULT_ASSETS["stocks_br"],
        "Ações US": DEFAULT_ASSETS["stocks_us"],
        "Criptomoedas": DEFAULT_ASSETS["crypto"],
        "Índices": DEFAULT_ASSETS["indices"],
    }
    
    if asset_type == "Personalizado":
        tickers_input = st.text_input(
            "Digite símbolos separados por vírgula",
            placeholder="AAPL,GOOGL,MSFT",
        )
        tickers = [t.strip().upper() for t in tickers_input.split(",")] if tickers_input else []
    elif asset_type == "Múltiplos":
        tickers = st.multiselect(
            "Selecione ativos",
            DEFAULT_ASSETS["stocks_us"][:5] + DEFAULT_ASSETS["stocks_br"][:5],
            default=DEFAULT_ASSETS["stocks_us"][:2],
        )
    else:
        tickers = st.multiselect(
            "Selecione ativos",
            asset_map.get(asset_type, []),
            default=asset_map.get(asset_type, [])[:2],
        )
    
    # Timeframe
    st.subheader("Período")
    timeframe = st.selectbox(
        "Período",
        list(TIMEFRAME_OPTIONS.keys()),
        index=5,  # Default to 1 year
    )
    timeframe_value = TIMEFRAME_OPTIONS[timeframe]
    
    use_custom_dates = st.checkbox("Usar datas personalizadas")
    if use_custom_dates:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Data Inicial")
        with col2:
            end_date = st.date_input("Data Final")
    else:
        start_date = None
        end_date = None

# ==================== MAIN CONTENT ====================

if tickers and len(tickers) > 0:
    try:
        # Fetch data for all tickers
        with st.spinner(f"📥 Carregando dados para {len(tickers)} ativo(s)..."):
            if use_custom_dates and start_date and end_date:
                data_dict = fetch_multiple_tickers(
                    tickers,
                    start_date=start_date,
                    end_date=end_date,
                )
            else:
                data_dict = fetch_multiple_tickers(tickers, period=timeframe_value)
        
        # Filter empty results
        successful_tickers = [t for t, d in data_dict.items() if not d.empty]
        
        if not successful_tickers:
            st.error("❌ Nenhum dado encontrado para os ativos selecionados")
        else:
            st.success(f"✅ Dados carregados para {len(successful_tickers)} ativo(s)")
            
            st.divider()
            
            # Display metrics
            st.markdown("### 📊 Resumo Comparativo")
            display_comparison_metrics(data_dict)
            
            st.divider()
            
            # Charts
            st.markdown("### 📈 Análise Gráfica")
            
            # Normalized comparison
            norm_chart = create_normalized_comparison_chart(data_dict)
            if norm_chart:
                st.plotly_chart(norm_chart, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            # Performance bars
            with col1:
                perf_chart = create_performance_comparison_chart(data_dict)
                if perf_chart:
                    st.plotly_chart(perf_chart, use_container_width=True)
            
            # Correlation heatmap
            with col2:
                corr_chart = create_correlation_heatmap(data_dict)
                if corr_chart:
                    st.plotly_chart(corr_chart, use_container_width=True)
                else:
                    st.info("ℹ️ Correlação disponível com 2+ ativos")
            
            st.divider()
            
            # Detailed metrics table
            st.markdown("### 📋 Métricas Detalhadas")
            metrics_df = create_metrics_table(data_dict)
            if metrics_df is not None:
                st.dataframe(metrics_df, use_container_width=True)
    
    except Exception as e:
        logger.error(f"Error processing assets: {e}")
        st.error("❌ Erro ao processar ativos")
        st.info("Verifique os símbolos dos tickers e tente novamente")

else:
    st.info("👈 Selecione pelo menos um ativo na barra lateral para começar")
