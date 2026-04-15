"""Módulo para cálculo de indicadores técnicos."""

import logging
from typing import Optional, Tuple

import pandas as pd
import numpy as np
from config import INDICATORS_CONFIG

logger = logging.getLogger(__name__)


def calculate_sma(
    data: pd.DataFrame, period: int = 20, column: str = "Close"
) -> pd.Series:
    """
    Calculate Simple Moving Average.

    Args:
        data: DataFrame with OHLCV data
        period: Period for SMA
        column: Column to calculate SMA on

    Returns:
        Series with SMA values
    """
    return data[column].rolling(window=period).mean()


def calculate_bollinger_bands(
    data: pd.DataFrame, period: int = 20, std_dev: int = 2, column: str = "Close"
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate Bollinger Bands.

    Args:
        data: DataFrame with OHLCV data
        period: Period for moving average
        std_dev: Number of standard deviations
        column: Column to calculate on

    Returns:
        Tuple of (upper_band, middle_band, lower_band)
    """
    sma = data[column].rolling(window=period).mean()
    std = data[column].rolling(window=period).std()

    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)

    return upper, sma, lower


def calculate_rsi(data: pd.DataFrame, period: int = 14, column: str = "Close") -> pd.Series:
    """
    Calculate Relative Strength Index.

    Args:
        data: DataFrame with OHLCV data
        period: Period for RSI
        column: Column to calculate on

    Returns:
        Series with RSI values
    """
    delta = data[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(
    data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, column: str = "Close"
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """
    Calculate MACD (Moving Average Convergence Divergence).

    Args:
        data: DataFrame with OHLCV data
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line EMA period
        column: Column to calculate on

    Returns:
        Tuple of (macd, signal_line, histogram)
    """
    ema_fast = data[column].ewm(span=fast).mean()
    ema_slow = data[column].ewm(span=slow).mean()

    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line

    return macd, signal_line, histogram


def add_all_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add all technical indicators to the DataFrame.

    Args:
        data: DataFrame with OHLCV data

    Returns:
        DataFrame with indicators added
    """
    df = data.copy()

    # SMA
    config = INDICATORS_CONFIG["sma"]
    for period in config["periods"]:
        df[f"SMA_{period}"] = calculate_sma(df, period)

    # Bollinger Bands
    config = INDICATORS_CONFIG["bollinger"]
    upper, middle, lower = calculate_bollinger_bands(
        df, config["period"], config["std_dev"]
    )
    df["BB_Upper"] = upper
    df["BB_Middle"] = middle
    df["BB_Lower"] = lower

    # RSI
    config = INDICATORS_CONFIG["rsi"]
    df["RSI"] = calculate_rsi(df, config["period"])

    # MACD
    config = INDICATORS_CONFIG["macd"]
    macd, signal, hist = calculate_macd(
        df, config["fast"], config["slow"], config["signal"]
    )
    df["MACD"] = macd
    df["MACD_Signal"] = signal
    df["MACD_Histogram"] = hist

    return df


def get_trading_signals(data: pd.DataFrame, method: str = "sma_crossover") -> pd.DataFrame:
    """
    Generate trading signals.

    Args:
        data: DataFrame with indicators
        method: Method for signal generation ('sma_crossover', 'rsi')

    Returns:
        DataFrame with signal column added
    """
    df = data.copy()

    if method == "sma_crossover":
        # SMA crossover: SMA20 crosses above SMA50
        if "SMA_20" not in df.columns or "SMA_50" not in df.columns:
            df = add_all_indicators(df)

        df["Signal"] = 0
        df.loc[df["SMA_20"] > df["SMA_50"], "Signal"] = 1  # Buy signal
        df.loc[df["SMA_20"] < df["SMA_50"], "Signal"] = -1  # Sell signal

    elif method == "rsi":
        if "RSI" not in df.columns:
            df = add_all_indicators(df)

        df["Signal"] = 0
        df.loc[df["RSI"] < 30, "Signal"] = 1  # Oversold - Buy
        df.loc[df["RSI"] > 70, "Signal"] = -1  # Overbought - Sell

    return df
