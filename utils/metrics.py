"""Módulo para cálculo de métricas financeiras."""

import logging
from typing import Dict, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def calculate_returns(data: pd.DataFrame, column: str = "Close") -> pd.DataFrame:
    """
    Calculate daily and cumulative returns.

    Args:
        data: DataFrame with OHLCV data
        column: Column to calculate returns on

    Returns:
        DataFrame with returns added
    """
    df = data.copy()
    df["Daily_Return"] = df[column].pct_change() * 100
    df["Cumulative_Return"] = (1 + df[column].pct_change()).cumprod() - 1
    df["Cumulative_Return"] = df["Cumulative_Return"] * 100
    return df


def calculate_log_returns(data: pd.DataFrame, column: str = "Close") -> pd.Series:
    """
    Calculate log returns.

    Args:
        data: DataFrame with OHLCV data
        column: Column to calculate on

    Returns:
        Series with log returns
    """
    return np.log(data[column] / data[column].shift(1)) * 100


def calculate_metrics(data: pd.DataFrame, column: str = "Close") -> Dict[str, float]:
    """
    Calculate key financial metrics.

    Args:
        data: DataFrame with OHLCV data
        column: Column to calculate metrics on

    Returns:
        Dictionary with metrics
    """
    if data.empty:
        return {}

    returns = data[column].pct_change()

    metrics = {
        "Preço Atual": data[column].iloc[-1],
        "Preço Máximo": data[column].max(),
        "Preço Mínimo": data[column].min(),
        "Preço Médio": data[column].mean(),
        "Variação %": ((data[column].iloc[-1] - data[column].iloc[0]) / data[column].iloc[0] * 100),
        "Volume Médio": data["Volume"].mean() if "Volume" in data.columns else 0,
        "Volatilidade %": returns.std() * np.sqrt(252) * 100,  # Annualized
        "Retorno Cumulativo %": ((data[column].iloc[-1] - data[column].iloc[0]) / data[column].iloc[0] * 100),
        "Dias de Dados": len(data),
    }

    # Adicionar Sharpe Ratio (assumindo taxa livre de risco de 2% a.a.)
    risk_free_rate = 0.02 / 252
    excess_returns = returns - risk_free_rate
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() > 0 else 0
    metrics["Sharpe Ratio"] = sharpe_ratio

    # Max Drawdown
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    metrics["Max Drawdown %"] = drawdown.min() * 100

    return metrics


def normalize_price(data: pd.DataFrame, column: str = "Close", base: float = 100) -> pd.Series:
    """
    Normalize price to base 100.

    Args:
        data: DataFrame with OHLCV data
        column: Column to normalize
        base: Base value (default 100)

    Returns:
        Series with normalized prices
    """
    return (data[column] / data[column].iloc[0]) * base


def calculate_correlation_matrix(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Calculate correlation matrix between multiple assets.

    Args:
        data_dict: Dictionary with ticker as key and DataFrame as value

    Returns:
        Correlation matrix DataFrame
    """
    close_prices = pd.DataFrame()
    for ticker, data in data_dict.items():
        close_prices[ticker] = data["Close"]

    return close_prices.corr()


def calculate_weighted_return(
    portfolio: Dict[str, float], returns_dict: Dict[str, float]
) -> float:
    """
    Calculate weighted portfolio return.

    Args:
        portfolio: Dictionary with ticker as key and weight as value (0-1)
        returns_dict: Dictionary with ticker as key and return % as value

    Returns:
        Weighted return percentage
    """
    weighted_return = 0
    for ticker, weight in portfolio.items():
        if ticker in returns_dict:
            weighted_return += weight * returns_dict[ticker]
    return weighted_return


def calculate_portfolio_contribution(portfolio: Dict[str, float], returns_dict: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate each asset's contribution to portfolio return.

    Args:
        portfolio: Dictionary with ticker as key and weight as value
        returns_dict: Dictionary with ticker as key and return % as value

    Returns:
        Dictionary with contribution % for each asset
    """
    contributions = {}
    total_return = calculate_weighted_return(portfolio, returns_dict)

    for ticker, weight in portfolio.items():
        if ticker in returns_dict:
            contribution = (weight * returns_dict[ticker])
            contributions[ticker] = contribution

    return contributions
