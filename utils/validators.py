"""
Validators module - Input and data validation utilities.

This module provides validation functions for user input, data integrity,
and business logic following the whitelist pattern from the reference repository.

Functions:
    validate_ticker: Validates if a ticker symbol is valid
    validate_date_range: Validates date range inputs
    validate_number_in_range: Validates numeric values
    validate_portfolio_weights: Validates portfolio asset weights
    validate_indicator_config: Validates technical indicator parameters
    whitelist_filter: Applies whitelist filtering to dictionaries
    
Author: Stock Analysis Dashboard
Date: 2024
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta
import logging

# Configure logging
logger = logging.getLogger(__name__)


def validate_ticker(ticker: str, max_length: int = 10) -> Tuple[bool, str]:
    """
    Validate if a ticker symbol is properly formatted.
    
    Args:
        ticker: Ticker symbol string
        max_length: Maximum allowed length (default: 10)
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_ticker("AAPL")
        (True, "")
        >>> validate_ticker("")
        (False, "Ticker cannot be empty")
    """
    # Check if empty
    if not ticker or not isinstance(ticker, str):
        return False, "Ticker must be a non-empty string"
    
    # Check length
    ticker = ticker.strip().upper()
    if len(ticker) == 0 or len(ticker) > max_length:
        return False, f"Ticker must be between 1 and {max_length} characters"
    
    # Check for valid characters (alphanumeric and dash)
    if not all(c.isalnum() or c in ['-', '.'] for c in ticker):
        return False, "Ticker can only contain letters, numbers, dashes, and dots"
    
    return True, ""


def validate_date_range(
    start_date: Union[str, datetime, pd.Timestamp],
    end_date: Union[str, datetime, pd.Timestamp],
    min_days: int = 1,
    max_days: Optional[int] = None
) -> Tuple[bool, str]:
    """
    Validate if a date range is valid.
    
    Args:
        start_date: Start date
        end_date: End date
        min_days: Minimum number of days required
        max_days: Maximum number of days allowed (None = no limit)
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_date_range('2024-01-01', '2024-12-31')
        (True, "")
    """
    try:
        # Convert to Timestamp if string
        if isinstance(start_date, str):
            start_date = pd.Timestamp(start_date)
        if isinstance(end_date, str):
            end_date = pd.Timestamp(end_date)
        
        # Check if start before end
        if start_date >= end_date:
            return False, "Start date must be before end date"
        
        # Check minimum days
        days_diff = (end_date - start_date).days
        if days_diff < min_days:
            return False, f"Date range must be at least {min_days} day(s)"
        
        # Check maximum days
        if max_days and days_diff > max_days:
            return False, f"Date range cannot exceed {max_days} days"
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid date format: {str(e)}"


def validate_number_in_range(
    value: Union[int, float],
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allow_negative: bool = True,
    allow_zero: bool = True
) -> Tuple[bool, str]:
    """
    Validate if a number is within an acceptable range.
    
    Args:
        value: Numeric value to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_negative: Whether negative values are allowed
        allow_zero: Whether zero is allowed
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_number_in_range(50, min_value=0, max_value=100)
        (True, "")
        >>> validate_number_in_range(-5, allow_negative=False)
        (False, "Negative values are not allowed")
    """
    try:
        # Type check
        if not isinstance(value, (int, float)):
            return False, "Value must be a number"
        
        # Check for NaN
        if np.isnan(value):
            return False, "Value cannot be NaN"
        
        # Check negative
        if value < 0 and not allow_negative:
            return False, "Negative values are not allowed"
        
        # Check zero
        if value == 0 and not allow_zero:
            return False, "Zero is not allowed"
        
        # Check minimum
        if min_value is not None and value < min_value:
            return False, f"Value must be at least {min_value}"
        
        # Check maximum
        if max_value is not None and value > max_value:
            return False, f"Value cannot exceed {max_value}"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating number: {str(e)}"


def validate_portfolio_weights(
    weights: Dict[str, float],
    tolerance: float = 0.01
) -> Tuple[bool, str]:
    """
    Validate if portfolio weights are valid (sum to ~100% or ~1.0).
    
    Args:
        weights: Dictionary of {asset: weight}
        tolerance: Tolerance for sum validation (default: 0.01)
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> weights = {'AAPL': 0.5, 'GOOGL': 0.5}
        >>> validate_portfolio_weights(weights)
        (True, "")
    """
    try:
        if not weights or not isinstance(weights, dict):
            return False, "Weights must be a non-empty dictionary"
        
        if len(weights) == 0:
            return False, "At least one asset is required"
        
        # Check each weight
        total = 0
        for asset, weight in weights.items():
            # Validate weight value
            is_valid, msg = validate_number_in_range(
                weight, 
                min_value=0, 
                max_value=1, 
                allow_negative=False
            )
            if not is_valid:
                return False, f"Weight for {asset}: {msg}"
            
            total += weight
        
        # Check total sum
        if abs(total - 1.0) > tolerance:
            return False, f"Weights must sum to 1.0 (currently: {total:.2f})"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating portfolio weights: {str(e)}"


def validate_indicator_config(
    indicator: str,
    params: Dict[str, Any],
    valid_indicators: Optional[List[str]] = None
) -> Tuple[bool, str]:
    """
    Validate technical indicator configuration.
    
    Args:
        indicator: Indicator name (e.g., 'SMA', 'RSI', 'MACD')
        params: Dictionary of parameters
        valid_indicators: List of valid indicator names
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_indicator_config('SMA', {'period': 20})
        (True, "")
    """
    valid_indicators = valid_indicators or ['SMA', 'EMA', 'RSI', 'MACD', 'Bollinger']
    
    # Check indicator name
    if indicator not in valid_indicators:
        return False, f"Invalid indicator: {indicator}. Must be one of {valid_indicators}"
    
    # Validate period for indicators that use it
    if indicator in ['SMA', 'EMA', 'RSI']:
        period = params.get('period')
        is_valid, msg = validate_number_in_range(
            period,
            min_value=2,
            max_value=500,
            allow_negative=False,
            allow_zero=False
        )
        if not is_valid:
            return False, f"Period: {msg}"
    
    # Validate MACD parameters
    if indicator == 'MACD':
        fast = params.get('fast', 12)
        slow = params.get('slow', 26)
        signal = params.get('signal', 9)
        
        if not (fast < slow):
            return False, "MACD: fast period must be less than slow period"
        if signal >= slow:
            return False, "MACD: signal period must be less than slow period"
    
    # Validate Bollinger Bands
    if indicator == 'Bollinger':
        period = params.get('period', 20)
        std_dev = params.get('std_dev', 2)
        
        is_valid, msg = validate_number_in_range(period, min_value=2, max_value=200)
        if not is_valid:
            return False, f"Bollinger period: {msg}"
        
        is_valid, msg = validate_number_in_range(std_dev, min_value=0.5, max_value=5)
        if not is_valid:
            return False, f"Bollinger std_dev: {msg}"
    
    return True, ""


def whitelist_filter(
    data: Dict[str, Any],
    allowed_keys: List[str],
    case_sensitive: bool = False
) -> Dict[str, Any]:
    """
    Filter a dictionary to only include whitelisted keys.
    
    This pattern is used in the reference repository for security and
    data validation when handling user input.
    
    Args:
        data: Dictionary to filter
        allowed_keys: List of allowed key names
        case_sensitive: Whether key matching is case-sensitive
        
    Returns:
        Dict[str, Any]: Filtered dictionary with only allowed keys
        
    Example:
        >>> data = {'name': 'John', 'age': 30, 'password': 'secret'}
        >>> allowed = ['name', 'age']
        >>> whitelist_filter(data, allowed)
        {'name': 'John', 'age': 30}
    """
    try:
        if not isinstance(data, dict):
            logger.warning(f"whitelist_filter received non-dict input: {type(data)}")
            return {}
        
        if case_sensitive:
            return {k: v for k, v in data.items() if k in allowed_keys}
        else:
            # Create lowercase mapping for case-insensitive matching
            allowed_lower = {k.lower(): k for k in allowed_keys}
            filtered = {}
            for k, v in data.items():
                if k.lower() in allowed_lower:
                    filtered[k] = v
            return filtered
        
    except Exception as e:
        logger.error(f"Error in whitelist_filter: {e}")
        return {}


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[List[str]] = None,
    min_rows: int = 1,
    check_nulls: bool = True
) -> Tuple[bool, str]:
    """
    Validate a DataFrame structure and content.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        min_rows: Minimum number of rows required
        check_nulls: Whether to check for null values
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_dataframe(df, required_columns=['date', 'close'])
    """
    try:
        if not isinstance(df, pd.DataFrame):
            return False, "Input must be a DataFrame"
        
        # Check minimum rows
        if len(df) < min_rows:
            return False, f"DataFrame must have at least {min_rows} row(s)"
        
        # Check required columns
        if required_columns:
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                return False, f"Missing required columns: {', '.join(missing)}"
        
        # Check for nulls in required columns
        if check_nulls and required_columns:
            for col in required_columns:
                if col in df.columns and df[col].isnull().any():
                    null_count = df[col].isnull().sum()
                    logger.warning(f"Column '{col}' has {null_count} null values")
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating DataFrame: {str(e)}"


def validate_price_data(
    df: pd.DataFrame,
    required_columns: Optional[List[str]] = None
) -> Tuple[bool, str]:
    """
    Validate price/OHLCV data specifically.
    
    Args:
        df: DataFrame with price data
        required_columns: List of required columns (default: OHLCV)
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
        
    Example:
        >>> validate_price_data(df)
    """
    required_columns = required_columns or ['Open', 'High', 'Low', 'Close', 'Volume']
    
    # Validate basic structure
    is_valid, msg = validate_dataframe(df, required_columns)
    if not is_valid:
        return False, msg
    
    try:
        # Validate price relationships
        for idx, row in df.iterrows():
            if not (row['Low'] <= row['Close'] <= row['High']):
                return False, f"Invalid OHLC relationship at row {idx}"
            
            if not (row['Low'] <= row['Open'] <= row['High']):
                return False, f"Invalid OHLC relationship at row {idx}"
            
            if row['Volume'] < 0:
                return False, f"Volume cannot be negative at row {idx}"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating price data: {str(e)}"


if __name__ == '__main__':
    logger.info("Validators module loaded successfully")
