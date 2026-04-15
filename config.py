"""Configurações globais da aplicação.

Este módulo centraliza todas as configurações de tema, cores, ativos padrão,
períodos de análise, indicadores técnicos e outras constantes da aplicação.

Seguindo os padrões profissionais do repositório de referência de visualização de dados.
"""

from typing import List, Dict, Optional

# ==================== TEMA E CORES ====================

# Paleta de cores principal - Padrão Profissional
THEME_COLORS = {
    "primary": "#1f77b4",        # Azul profissional
    "secondary": "#ff7f0e",      # Laranja complementar
    "success": "#2ca02c",        # Verde (alta)
    "danger": "#d62728",         # Vermelho (baixa)
    "warning": "#ff9900",        # Aviso
    "info": "#17a2b8",           # Informação
    "light_bg": "#f8f9fa",       # Fundo claro
    "dark_bg": "#1e1e1e",        # Fundo escuro
    "text_light": "#ffffff",     # Texto claro
    "text_dark": "#1a1a1a",      # Texto escuro
    "grid": "#e9ecef",           # Grid
    "up": "#00cc96",             # Alta (Plotly)
    "down": "#ef553b",           # Baixa (Plotly)
}

# Paletas de cores alternativas para diferentes contextos
COLOR_PALETTES = {
    "professional": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e",
        "accent": "#2ca02c",
        "negative": "#d62728",
        "neutral": "#7f7f7f",
    },
    "financial": {
        "bullish": "#00cc96",      # Verde para alta
        "bearish": "#ef553b",      # Vermelho para baixa
        "neutral": "#636ef9",      # Azul neutro
        "positive": "#2ca02c",
        "negative": "#d62728",
    },
    "heatmap": {
        "cold": "#0000ff",         # Azul (correlação negativa)
        "neutral": "#ffffff",      # Branco (sem correlação)
        "hot": "#ff0000",          # Vermelho (correlação positiva)
    }
}

# Cores para linhas de SMA
SMA_COLORS = {
    20: "#ff9999",   # SMA 20 - Rosa claro
    50: "#66b3ff",   # SMA 50 - Azul claro
    200: "#99ff99",  # SMA 200 - Verde claro
}

# Cores para ativos (usadas em comparações)
ASSET_COLORS = {
    "ITUB4.SA": "#1f77b4",
    "PETR4.SA": "#ff7f0e",
    "MGLU3.SA": "#2ca02c",
    "VALE3.SA": "#d62728",
    "AAPL": "#9467bd",
    "MSFT": "#8c564b",
    "GOOGL": "#e377c2",
    "BTC-USD": "#ffa500",
    "ETH-USD": "#4169e1",
}

# ==================== ATIVOS PADRÃO ====================

DEFAULT_ASSETS = {
    "stocks_br": ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "GGBR4.SA", "BBDC4.SA", "ABEV3.SA"],
    "stocks_us": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META"],
    "crypto": ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD"],
    "indices": ["^BVSP", "^GSPC", "^DJI", "^IXIC"],
}

# ==================== PERÍODOS DE ANÁLISE ====================

TIMEFRAME_OPTIONS = {
    "1 Dia": "1d",
    "5 Dias": "5d",
    "1 Mês": "1mo",
    "3 Meses": "3mo",
    "6 Meses": "6mo",
    "1 Ano": "1y",
    "5 Anos": "5y",
}

# Período padrão em dias para cada timeframe
TIMEFRAME_DEFAULTS = {
    "1d": 30,
    "5d": 60,
    "1mo": 365,
    "3mo": 365,
    "6mo": 730,
    "1y": 1825,
    "5y": 1825,
}

# ==================== INDICADORES TÉCNICOS ====================

INDICATORS_CONFIG = {
    "sma": {
        "periods": [20, 50, 200],
        "name": "Média Móvel Simples",
        "description": "Indica tendência de preço a curto/longo prazo"
    },
    "bollinger": {
        "period": 20,
        "std_dev": 2,
        "name": "Bandas de Bollinger",
        "description": "Mede volatilidade e níveis de sobre-compra/venda"
    },
    "rsi": {
        "period": 14,
        "name": "Índice de Força Relativa",
        "description": "Identifica sobre-compra (>70) e sobre-venda (<30)"
    },
    "macd": {
        "fast": 12,
        "slow": 26,
        "signal": 9,
        "name": "MACD",
        "description": "Indica mudanças na tendência e momentum"
    },
}

# ==================== CACHE E PERFORMANCE ====================

CACHE_TTL = 3600  # 1 hora em segundos
MAX_DATA_POINTS = 5000  # Limite máximo de pontos por gráfico
DEFAULT_PERIOD_YEARS = 5  # Período padrão em anos

# ==================== CONFIGURAÇÕES DE LAYOUT ====================

PAGE_ICON = "📊"
PAGE_TITLE = "Stock & Crypto Analysis Dashboard"
LAYOUT = "wide"  # 'centered' ou 'wide'

# ==================== TIPOS DE GRÁFICOS ====================

CHART_TYPES = ["Linha", "Candlestick"]
DEFAULT_CHART_HEIGHT = 500
DEFAULT_CHART_WIDTH = 900
CHART_TEMPLATE = "plotly_dark"  # Tema do Plotly

# ==================== EMOJIS E ÍCONES ====================

EMOJIS = {
    "individual": "📈",      # Análise individual
    "comparison": "⚖️",      # Comparação
    "portfolio": "💼",       # Portfólio
    "indicators": "📊",      # Indicadores
    "metrics": "📉",         # Métricas
    "settings": "⚙️",        # Configurações
    "up": "📈",              # Alta/positivo
    "down": "📉",            # Baixa/negativo
    "neutral": "➡️",         # Neutro/sem mudança
    "warning": "⚠️",         # Aviso
    "success": "✅",         # Sucesso
    "error": "❌",           # Erro
    "info": "ℹ️",            # Informação
}
