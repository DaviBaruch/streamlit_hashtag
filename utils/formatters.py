"""
Formatters module - Data formatting and display utilities.

This module provides consistent formatting functions for financial data,
following professional standards for currency, percentages, and numbers.

Functions:
    format_currency: Formats numbers as currency
    format_percentage: Formats numbers as percentages
    format_volume: Formats trading volumes
    format_large_number: Formats large numbers with abbreviations
    format_date: Formats dates consistently
    format_dataframe_for_display: Formats entire DataFrames for display
    
Author: Stock Analysis Dashboard
Date: 2024
"""

import pandas as pd
import numpy as np
from typing import Union, List, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


def format_currency(
    value: Union[int, float, np.number],
    currency: str = "R$",
    decimals: int = 2,
    show_symbol: bool = True
) -> str:
    """
    Format a number as currency.
    
    Args:
        value: Numeric value to format
        currency: Currency symbol (default: "R$" for Brazilian Real)
        decimals: Number of decimal places
        show_symbol: Whether to show currency symbol
        
    Returns:
        str: Formatted currency string
        
    Example:
        >>> format_currency(1234.56)
        'R$ 1.234,56'
        >>> format_currency(999.99, currency="$", decimals=2)
        '$ 999,99'
    """
    try:
        # Handle NaN or None
        if pd.isna(value):
            return "N/A"
        
        # Convert to float
        value = float(value)
        
        # Format with thousands separator and decimal places
        formatted = f"{value:,.{decimals}f}".replace(',', '_').replace('.', ',').replace('_', '.')
        
        if show_symbol:
            return f"{currency} {formatted}"
        return formatted
        
    except (TypeError, ValueError) as e:
        logger.warning(f"Error formatting currency {value}: {e}")
        return "N/A"


def format_percentage(
    value: Union[int, float, np.number],
    decimals: int = 2,
    show_sign: bool = True,
    multiplier: float = 1.0
) -> str:
    """
    Format a number as a percentage.
    
    Args:
        value: Numeric value to format (0-100 or 0-1)
        decimals: Number of decimal places
        show_sign: Whether to show + sign for positive values
        multiplier: Multiply value by this before formatting (default 1.0)
                   Use 100 if value is 0-1 range
        
    Returns:
        str: Formatted percentage string
        
    Example:
        >>> format_percentage(0.1532)  # Default (multiply by 100)
        '+15,32%'
        >>> format_percentage(15.32, show_sign=False)
        '15,32%'
        >>> format_percentage(-5.5, decimals=1)
        '-5,5%'
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        value = float(value) * multiplier
        sign = "+" if (value >= 0 and show_sign) else ""
        
        # Format with correct decimal separator
        formatted = f"{value:.{decimals}f}".replace('.', ',')
        
        return f"{sign}{formatted}%"
        
    except (TypeError, ValueError) as e:
        logger.warning(f"Error formatting percentage {value}: {e}")
        return "N/A"


def format_volume(
    value: Union[int, float, np.number],
    decimals: int = 0
) -> str:
    """
    Format trading volume with abbreviations.
    
    Args:
        value: Volume value (number of shares/coins)
        decimals: Number of decimal places
        
    Returns:
        str: Formatted volume string
        
    Example:
        >>> format_volume(1500000)
        '1.5M'
        >>> format_volume(5000)
        '5K'
        >>> format_volume(250)
        '250'
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        value = float(value)
        
        if abs(value) >= 1e9:
            return f"{value / 1e9:.{decimals}f}B"
        elif abs(value) >= 1e6:
            return f"{value / 1e6:.{decimals}f}M"
        elif abs(value) >= 1e3:
            return f"{value / 1e3:.{decimals}f}K"
        else:
            return f"{value:,.0f}"
            
    except (TypeError, ValueError) as e:
        logger.warning(f"Error formatting volume {value}: {e}")
        return "N/A"


def format_large_number(
    value: Union[int, float, np.number],
    decimals: int = 2,
    abbreviate: bool = True
) -> str:
    """
    Format large numbers with optional abbreviations.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        abbreviate: Whether to use abbreviations (B, M, K)
        
    Returns:
        str: Formatted number string
        
    Example:
        >>> format_large_number(1234567890)
        '1.23B'
        >>> format_large_number(50000)
        '50.00K'
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        value = float(value)
        
        if not abbreviate:
            return f"{value:,.{decimals}f}".replace(',', '_').replace('.', ',').replace('_', '.')
        
        if abs(value) >= 1e9:
            return f"{value / 1e9:.{decimals}f}B"
        elif abs(value) >= 1e6:
            return f"{value / 1e6:.{decimals}f}M"
        elif abs(value) >= 1e3:
            return f"{value / 1e3:.{decimals}f}K"
        else:
            return f"{value:.{decimals}f}"
            
    except (TypeError, ValueError) as e:
        logger.warning(f"Error formatting large number {value}: {e}")
        return "N/A"


def format_date(
    date: Union[str, pd.Timestamp, datetime],
    format_str: str = "%d/%m/%Y"
) -> str:
    """
    Format a date consistently.
    
    Args:
        date: Date value
        format_str: Format string (default: "DD/MM/YYYY")
        
    Returns:
        str: Formatted date string
        
    Example:
        >>> format_date(pd.Timestamp('2024-04-13'))
        '13/04/2024'
    """
    try:
        if pd.isna(date):
            return "N/A"
        
        if isinstance(date, str):
            date = pd.Timestamp(date)
        elif not isinstance(date, (pd.Timestamp, datetime)):
            return "N/A"
        
        return date.strftime(format_str)
        
    except Exception as e:
        logger.warning(f"Error formatting date {date}: {e}")
        return "N/A"


def format_dataframe_for_display(
    df: pd.DataFrame,
    column_formats: Optional[dict] = None,
    hide_columns: Optional[List[str]] = None,
    max_rows: Optional[int] = None
) -> pd.DataFrame:
    """
    Format an entire DataFrame for display in Streamlit.
    
    Args:
        df: DataFrame to format
        column_formats: Dict mapping column names to format functions
                       e.g., {'price': lambda x: format_currency(x),
                              'return': lambda x: format_percentage(x)}
        hide_columns: List of column names to hide
        max_rows: Maximum number of rows to display
        
    Returns:
        pd.DataFrame: Formatted DataFrame
        
    Example:
        >>> formats = {'price': format_currency, 'return': format_percentage}
        >>> df_display = format_dataframe_for_display(df, formats)
    """
    try:
        # Make a copy to avoid modifying original
        df_copy = df.copy()
        
        # Hide columns if specified
        if hide_columns:
            df_copy = df_copy.drop(columns=[col for col in hide_columns if col in df_copy.columns])
        
        # Apply formatting if specified
        if column_formats:
            for col, format_func in column_formats.items():
                if col in df_copy.columns:
                    try:
                        df_copy[col] = df_copy[col].apply(format_func)
                    except Exception as e:
                        logger.warning(f"Error formatting column {col}: {e}")
        
        # Limit rows if specified
        if max_rows:
            df_copy = df_copy.head(max_rows)
        
        return df_copy
        
    except Exception as e:
        logger.error(f"Error formatting DataFrame: {e}")
        return df


def format_metrics_display(
    metrics: dict,
    format_config: Optional[dict] = None
) -> dict:
    """
    Format a dictionary of metrics for display.
    
    Args:
        metrics: Dictionary of metrics {metric_name: value}
        format_config: Dict mapping metric names to format functions
                      
    Returns:
        dict: Formatted metrics dictionary
        
    Example:
        >>> metrics = {'price': 1234.56, 'return': 0.1532}
        >>> config = {'price': format_currency, 'return': format_percentage}
        >>> formatted = format_metrics_display(metrics, config)
    """
    try:
        if not format_config:
            return metrics
        
        formatted = {}
        for key, value in metrics.items():
            if key in format_config:
                try:
                    formatted[key] = format_config[key](value)
                except Exception as e:
                    logger.warning(f"Error formatting metric {key}: {e}")
                    formatted[key] = value
            else:
                formatted[key] = value
        
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting metrics: {e}")
        return metrics


def format_timedelta(
    td: Union[pd.Timedelta, float],
    unit: str = "days"
) -> str:
    """
    Format a timedelta for display.
    
    Args:
        td: Timedelta or number value
        unit: Unit of time ('days', 'hours', 'minutes', etc.)
        
    Returns:
        str: Formatted timedelta string
        
    Example:
        >>> format_timedelta(pd.Timedelta(days=5))
        '5 dias'
    """
    try:
        if isinstance(td, pd.Timedelta):
            days = td.days
            if days == 1:
                return "1 dia"
            else:
                return f"{days} dias"
        else:
            return f"{td} {unit}"
            
    except Exception as e:
        logger.warning(f"Error formatting timedelta: {e}")
        return "N/A"


def format_number(
    value: Union[int, float, np.number],
    decimals: int = 2,
    thousands_sep: str = "."
) -> str:
    """
    Format a number with thousands separator.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
        thousands_sep: Thousands separator (default: "." for Brazilian format)
        
    Returns:
        str: Formatted number string
        
    Example:
        >>> format_number(1234567.89)
        '1.234.567,89'
    """
    try:
        if pd.isna(value):
            return "N/A"
        
        value = float(value)
        # Use Python's format with , then replace for Brazilian format
        formatted = f"{value:,.{decimals}f}"
        # Convert to Brazilian format (1.234.567,89)
        formatted = formatted.replace(',', '_').replace('.', thousands_sep).replace('_', ',')
        return formatted
        
    except (TypeError, ValueError) as e:
        logger.warning(f"Error formatting number {value}: {e}")
        return "N/A"


if __name__ == '__main__':
    logger.info("Formatters module loaded successfully")
