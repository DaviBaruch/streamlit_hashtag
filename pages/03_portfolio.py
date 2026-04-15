"""Página de análise e simulação de portfólio."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict

from config import DEFAULT_ASSETS, EMOJIS, THEME_COLORS
from utils.portfolio import simulate_portfolio
from utils.metrics import calculate_metrics
from utils.formatters import format_currency, format_percentage
from utils.chart_builders import create_bar_chart, create_line_chart
from utils.styling import apply_custom_css


def create_allocation_pie_chart(allocation: Dict[str, float]) -> go.Figure:
    """
    Create pie chart for portfolio allocation.
    
    Args:
        allocation: Dictionary with ticker and weight
    
    Returns:
        Plotly figure
    """
    fig = go.Figure(
        data=[
            go.Pie(
                labels=list(allocation.keys()),
                values=[v * 100 for v in allocation.values()],
                textposition="auto",
                hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Alocação do Portfólio",
        height=400,
        template="plotly_dark",
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


def create_portfolio_growth_chart(
    portfolio_values: pd.Series, initial_investment: float
) -> go.Figure:
    """
    Create portfolio growth chart.
    
    Args:
        portfolio_values: Series with portfolio value over time
        initial_investment: Initial investment amount
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=portfolio_values.index,
            y=portfolio_values,
            mode="lines",
            name="Valor do Portfólio",
            line=dict(color=THEME_COLORS["success"], width=2),
            fill="tozeroy",
            fillcolor="rgba(44, 160, 44, 0.2)",
        )
    )

    # Add initial investment line
    fig.add_hline(
        y=initial_investment,
        line_dash="dash",
        line_color="gray",
        annotation_text="Investimento Inicial",
        annotation_position="right",
    )

    fig.update_layout(
        title="Evolução do Portfólio",
        xaxis_title="Data",
        yaxis_title="Valor (USD)",
        hovermode="x unified",
        template="plotly_dark",
        height=450,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


def create_contribution_chart(contributions: Dict[str, float]) -> go.Figure:
    """
    Create contribution chart.
    
    Args:
        contributions: Dictionary with ticker and contribution value
    
    Returns:
        Plotly figure
    """
    colors = [
        THEME_COLORS["up"] if v >= 0 else THEME_COLORS["down"]
        for v in contributions.values()
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(contributions.keys()),
                y=list(contributions.values()),
                marker_color=colors,
                text=[f"{v:.2f}%" for v in contributions.values()],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Contribuição ao Retorno do Portfólio (%)",
        xaxis_title="Ativo",
        yaxis_title="Contribuição (%)",
        template="plotly_dark",
        height=400,
        showlegend=False,
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig


### Page configuration
##st.set_page_config(
##    page_title="Análise de Portfólio",
##    page_icon=EMOJIS["portfolio"],
##    layout="wide",
##)

apply_custom_css()

st.title(f"{EMOJIS['portfolio']} Simulador e Análise de Portfólio")

# Sidebar controls
with st.sidebar:
    st.subheader("⚙️ Configuração do Portfólio")

    # Investment amount
    initial_investment = st.number_input(
        "Investimento Inicial (USD)",
        value=10000.0,
        min_value=100.0,
        step=100.0,
    )

    # Period
    st.subheader("Período")
    period_options = {
        "1 Mês": "1mo",
        "3 Meses": "3mo",
        "6 Meses": "6mo",
        "1 Ano": "1y",
        "5 Anos": "5y",
    }
    selected_period = st.selectbox("Período para Análise", list(period_options.keys()))
    period = period_options[selected_period]

# Main content
st.subheader("📈 Construir Portfólio")
st.info(
    "Adicione ativos ao seu portfólio abaixo. Os pesos serão normalizados para somar 100%."
)

# Asset selection
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.subheader("Selecione Ativos")
with col2:
    st.subheader("Peso (%)")
with col3:
    st.subheader("Ação")

portfolio_assets = {}
errors = []

# Get all available tickers
all_tickers = []
for asset_type in DEFAULT_ASSETS.values():
    all_tickers.extend(asset_type)
all_tickers = sorted(list(set(all_tickers)))

# Number of assets to add
num_assets = st.number_input(
    "Quantos ativos deseja adicionar?", min_value=1, max_value=10, value=2
)

# Create input fields for each asset
for i in range(num_assets):
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        ticker = st.selectbox(
            f"Ativo {i + 1}",
            all_tickers,
            key=f"ticker_{i}",
        )
    with col2:
        weight = st.number_input(
            f"Peso {i + 1} (%)",
            min_value=0.0,
            max_value=100.0,
            value=100.0 / num_assets,
            step=1.0,
            key=f"weight_{i}",
        )
    with col3:
        st.empty()  # Placeholder for visual alignment

    if ticker:
        portfolio_assets[ticker] = weight

if portfolio_assets:
    st.markdown("---")

    # Simulate portfolio
    col1, col2, col3 = st.columns(3)
    with col1:
        simulate_btn = st.button("▶️ Simular Portfólio", use_container_width=True)
    with col2:
        st.empty()
    with col3:
        st.empty()

    if simulate_btn:
        with st.spinner("Simulando portfólio..."):
            try:
                portfolio, cumulative_value, metrics = simulate_portfolio(
                    portfolio_assets, period=period, initial_investment=initial_investment
                )

                # Display key metrics
                st.subheader("📊 Resumo do Portfólio")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    final_value = cumulative_value.iloc[-1] if not cumulative_value.empty else initial_investment
                    profit = final_value - initial_investment
                    profit_pct = (profit / initial_investment) * 100
                    st.metric(
                        "Valor Final",
                        f"${final_value:,.2f}",
                        f"{profit_pct:.2f}%",
                        delta_color="inverse",
                    )

                with col2:
                    st.metric(
                        "Ganho/Perda",
                        f"${profit:,.2f}",
                    )

                with col3:
                    if "Volatilidade %" in metrics:
                        st.metric(
                            "Volatilidade",
                            f"{metrics['Volatilidade %']:.2f}%",
                        )

                with col4:
                    st.metric(
                        "Assets",
                        f"{metrics['Assets']}",
                    )

                st.markdown("---")

                # Charts
                col1, col2 = st.columns(2)
                with col1:
                    allocation_chart = create_allocation_pie_chart(metrics["Allocation"])
                    st.plotly_chart(allocation_chart, use_container_width=True)

                with col2:
                    if not cumulative_value.empty:
                        growth_chart = create_portfolio_growth_chart(
                            cumulative_value, initial_investment
                        )
                        st.plotly_chart(growth_chart, use_container_width=True)

                # Contribution analysis
                if "Contribuições" in metrics and metrics["Contribuições"]:
                    st.subheader("🎯 Análise de Contribuição")
                    contribution_chart = create_contribution_chart(
                        metrics["Contribuições"]
                    )
                    st.plotly_chart(contribution_chart, use_container_width=True)

                # Detailed allocation table
                st.subheader("📋 Detalhes da Alocação")
                allocation_data = []
                for ticker, weight in metrics["Allocation"].items():
                    contribution = (
                        metrics["Contribuições"].get(ticker, 0) if "Contribuições" in metrics else 0
                    )
                    allocation_data.append(
                        {
                            "Ativo": ticker,
                            "Peso (%)": f"{weight * 100:.2f}%",
                            "Contribuição (%)": f"{contribution:.2f}%",
                        }
                    )

                allocation_df = pd.DataFrame(allocation_data)
                st.dataframe(allocation_df, use_container_width=True)

                # Export functionality
                st.subheader("📥 Exportar Simulação")
                if not cumulative_value.empty:
                    export_df = cumulative_value.reset_index()
                    export_df.columns = ["Data", "Valor_Portfólio"]
                    csv = export_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="portfolio_simulation.csv",
                        mime="text/csv",
                    )

            except Exception as e:
                st.error(f"❌ Erro ao simular portfólio: {str(e)}")
else:
    st.info("👈 Configure seu portfólio na barra lateral")
