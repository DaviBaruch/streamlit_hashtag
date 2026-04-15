"""Módulo para análise e simulação de portfólio."""

import logging
from typing import Dict, Optional, Tuple, List

import pandas as pd
import numpy as np
from utils.metrics import calculate_metrics, calculate_weighted_return, calculate_portfolio_contribution
from utils.data_fetcher import fetch_stock_data

logger = logging.getLogger(__name__)


class Portfolio:
    """
    Portfolio management and analysis class.
    """

    def __init__(self, assets: Dict[str, float]):
        """
        Initialize portfolio.

        Args:
            assets: Dictionary with ticker as key and weight (0-1) as value
        """
        # Validate weights sum to 1
        total_weight = sum(assets.values())
        if abs(total_weight - 1.0) > 0.01:
            # Normalize weights
            assets = {k: v / total_weight for k, v in assets.items()}

        self.assets = assets
        self.data = {}
        self.metrics = {}

    def fetch_data(
        self,
        start_date: Optional[pd.Timestamp] = None,
        end_date: Optional[pd.Timestamp] = None,
        period: str = "1y",
    ):
        """
        Fetch data for all portfolio assets.

        Args:
            start_date: Start date
            end_date: End date
            period: Period string
        """
        for ticker in self.assets.keys():
            try:
                self.data[ticker] = fetch_stock_data(
                    ticker, start_date, end_date, period
                )
            except Exception as e:
                logger.error(f"Error fetching data for {ticker}: {str(e)}")

    def calculate_portfolio_returns(self) -> pd.Series:
        """
        Calculate portfolio returns.

        Returns:
            Series with portfolio returns
        """
        if not self.data:
            return pd.Series()

        # Get aligned dates
        common_index = None
        for ticker, data in self.data.items():
            if common_index is None:
                common_index = data.index
            else:
                common_index = common_index.intersection(data.index)

        # Calculate weighted returns
        portfolio_returns = pd.Series(0, index=common_index)

        for ticker, weight in self.assets.items():
            if ticker in self.data:
                data = self.data[ticker].loc[common_index]
                asset_returns = data["Close"].pct_change() * 100
                portfolio_returns += asset_returns * weight

        return portfolio_returns

    def get_portfolio_metrics(self) -> Dict:
        """
        Get portfolio metrics.

        Returns:
            Dictionary with portfolio metrics
        """
        metrics = {
            "Assets": len(self.assets),
            "Allocation": self.assets.copy(),
        }

        # Get returns for each asset over the period
        returns_dict = {}
        for ticker, data in self.data.items():
            if not data.empty:
                return_pct = ((data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]) * 100
                returns_dict[ticker] = return_pct

        # Calculate weighted return
        weighted_return = calculate_weighted_return(self.assets, returns_dict)
        metrics["Retorno Ponderado %"] = weighted_return

        # Calculate contributions
        contributions = calculate_portfolio_contribution(self.assets, returns_dict)
        metrics["Contribuições"] = contributions

        # Calculate portfolio volatility
        port_returns = self.calculate_portfolio_returns()
        if not port_returns.empty:
            metrics["Volatilidade %"] = port_returns.std() * np.sqrt(252)
            metrics["Retorno Médio Diário %"] = port_returns.mean()

        return metrics

    def get_cumulative_value(self, initial_investment: float = 10000) -> pd.Series:
        """
        Get cumulative portfolio value over time.

        Args:
            initial_investment: Initial investment amount

        Returns:
            Series with portfolio value over time
        """
        port_returns = self.calculate_portfolio_returns()
        cumulative = (1 + port_returns / 100).cumprod() * initial_investment
        return cumulative

    def rebalance(self, new_weights: Dict[str, float]):
        """
        Rebalance portfolio with new weights.

        Args:
            new_weights: Dictionary with new weights
        """
        total_weight = sum(new_weights.values())
        self.assets = {k: v / total_weight for k, v in new_weights.items()}
        logger.info(f"Portfolio rebalanced: {self.assets}")


def simulate_portfolio(
    assets: Dict[str, float],
    start_date: Optional[pd.Timestamp] = None,
    end_date: Optional[pd.Timestamp] = None,
    period: str = "1y",
    initial_investment: float = 10000,
) -> Tuple[Portfolio, pd.Series, Dict]:
    """
    Simulate a portfolio and get results.

    Args:
        assets: Dictionary with ticker and weight
        start_date: Start date
        end_date: End date
        period: Period string
        initial_investment: Initial investment amount

    Returns:
        Tuple of (portfolio, cumulative_value, metrics)
    """
    portfolio = Portfolio(assets)
    portfolio.fetch_data(start_date, end_date, period)
    cumulative_value = portfolio.get_cumulative_value(initial_investment)
    metrics = portfolio.get_portfolio_metrics()

    return portfolio, cumulative_value, metrics
