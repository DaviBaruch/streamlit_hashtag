"""Módulo para fetching de dados de mercado com yfinance."""

import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple, List

import pandas as pd
import yfinance as yf
import streamlit as st
from config import DEFAULT_ASSETS, MAX_DATA_POINTS, DEFAULT_PERIOD_YEARS

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data(ttl=3600)
def fetch_stock_data(
    ticker: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    period: str = "1y",
    interval: str = "1d",
) -> pd.DataFrame:
    """
    Fetch stock/crypto data using yfinance.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'BTC-USD')
        start_date: Start date for data fetch
        end_date: End date for data fetch
        period: Period string if start_date/end_date not provided ('1d', '5d', '1mo', '3mo', '6mo', '1y', '5y')
        interval: Data interval ('1m', '5m', '15m', '30m', '60m', '1d', '1wk', '1mo')

    Returns:
        DataFrame with OHLCV data

    Raises:
        ValueError: If ticker is invalid or no data available
    """
    try:
        logger.info(f"Fetching data for {ticker} with period={period}")

        if start_date is None or end_date is None:
            data = yf.download(
                ticker, period=period, interval=interval, progress=False
            )
        else:
            data = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
            )

        if data.empty:
            raise ValueError(f"Nenhum dado encontrado para {ticker}")

        # Manter apenas as últimas MAX_DATA_POINTS linhas
        if len(data) > MAX_DATA_POINTS:
            data = data.tail(MAX_DATA_POINTS)

        logger.info(f"Successfully fetched {len(data)} data points for {ticker}")
        return data

    except Exception as e:
        logger.error(f"Erro ao buscar dados para {ticker}: {str(e)}")
        raise ValueError(f"Erro ao buscar dados para {ticker}: {str(e)}")


@st.cache_data(ttl=3600)
def fetch_multiple_tickers(
    tickers: List[str],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    period: str = "1y",
) -> dict:
    """
    Fetch data for multiple tickers.

    Args:
        tickers: List of ticker symbols
        start_date: Start date
        end_date: End date
        period: Period string

    Returns:
        Dictionary with ticker as key and DataFrame as value
    """
    data_dict = {}
    errors = []

    for ticker in tickers:
        try:
            data = fetch_stock_data(ticker, start_date, end_date, period)
            data_dict[ticker] = data
        except ValueError as e:
            logger.warning(f"Erro para {ticker}: {str(e)}")
            errors.append((ticker, str(e)))

    if errors:
        logger.warning(f"Erros ao buscar dados: {errors}")

    return data_dict


def get_ticker_info(ticker: str) -> dict:
    """
    Get basic info about a ticker.

    Args:
        ticker: Ticker symbol

    Returns:
        Dictionary with ticker info
    """
    try:
        info = yf.Ticker(ticker)
        return {
            "name": info.info.get("longName", ticker),
            "sector": info.info.get("sector", "N/A"),
            "industry": info.info.get("industry", "N/A"),
            "currency": info.info.get("currency", "USD"),
        }
    except Exception as e:
        logger.error(f"Erro ao buscar info de {ticker}: {str(e)}")
        return {"name": ticker, "sector": "N/A", "industry": "N/A", "currency": "USD"}


def get_all_available_tickers() -> dict:
    """
    Get all available tickers from config.

    Returns:
        Dictionary with grouped tickers
    """
    return DEFAULT_ASSETS


def validate_ticker(ticker: str) -> Tuple[bool, str]:
    """
    Validate if a ticker exists.

    Args:
        ticker: Ticker symbol

    Returns:
        Tuple of (is_valid, message)
    """
    try:
        data = yf.download(ticker, period="1d", progress=False)
        if data.empty:
            return False, f"Ticker {ticker} não encontrado ou sem dados"
        return True, "OK"
    except Exception as e:
        return False, f"Erro ao validar {ticker}: {str(e)}"
