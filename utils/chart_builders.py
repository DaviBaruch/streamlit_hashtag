"""
Chart builders module - Professional Plotly wrappers and chart creation utilities.

This module provides reusable, professional-grade chart creation functions
following the patterns from the dataviz reference repository.

Functions:
    create_line_chart: Creates a professional line chart
    create_candlestick_chart: Creates a candlestick chart for OHLC data
    create_bar_chart: Creates a bar chart
    create_area_chart: Creates an area chart
    create_heatmap: Creates a correlation heatmap
    add_sma_to_chart: Adds SMA lines to price chart
    add_bollinger_bands_to_chart: Adds Bollinger Bands to chart
    
Author: Stock Analysis Dashboard
Date: 2024
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go
from typing import List, Dict, Tuple, Optional, Union
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)


def create_line_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: Union[str, List[str]],
    title: str = "",
    xaxis_title: str = "Data",
    yaxis_title: str = "Valor",
    height: int = 500,
    width: int = 900,
    show_grid: bool = True,
    template: str = "plotly_dark",
    **kwargs
) -> go.Figure:
    """
    Create a professional line chart.
    
    Args:
        data: DataFrame with chart data
        x_col: Column name for X-axis
        y_col: Column name(s) for Y-axis (str or list)
        title: Chart title
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        height: Chart height in pixels
        width: Chart width in pixels
        show_grid: Whether to show grid
        template: Plotly template name
        **kwargs: Additional arguments passed to go.Scatter
        
    Returns:
        go.Figure: Configured Plotly figure
        
    Example:
        >>> fig = create_line_chart(df, 'date', 'price', title='Price Over Time')
    """
    try:
        # Normalize y_col to list
        y_cols = [y_col] if isinstance(y_col, str) else y_col
        
        # Create traces
        traces = []
        colors = kwargs.get('colors', None)
        color_palette = colors or ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for idx, col in enumerate(y_cols):
            color = color_palette[idx % len(color_palette)]
            trace = go.Scatter(
                x=data[x_col],
                y=data[col],
                name=col,
                mode='lines',
                line=dict(color=color, width=2),
                hovertemplate=f'<b>{col}</b><br>{{x}}<br>{{y:.2f}}<extra></extra>',
                **{k: v for k, v in kwargs.items() if k not in ['colors']}
            )
            traces.append(trace)
        
        # Create layout
        layout = go.Layout(
            title=dict(text=title, font=dict(size=18, color='white')),
            xaxis=dict(
                title=xaxis_title,
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            yaxis=dict(
                title=yaxis_title,
                showgrid=show_grid,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            height=height,
            width=width,
            hovermode='x unified',
            template=template,
            font=dict(family='Arial, sans-serif', size=12, color='white'),
            margin=dict(l=60, r=40, t=80, b=50),
            showlegend=True,
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(0, 0, 0, 0.3)',
                bordercolor='rgba(128, 128, 128, 0.5)',
                borderwidth=1
            )
        )
        
        fig = go.Figure(data=traces, layout=layout)
        return fig
        
    except Exception as e:
        logger.error(f"Error creating line chart: {e}")
        raise


def create_candlestick_chart(
    data: pd.DataFrame,
    date_col: str = 'Date',
    open_col: str = 'Open',
    high_col: str = 'High',
    low_col: str = 'Low',
    close_col: str = 'Close',
    title: str = "OHLC Chart",
    height: int = 600,
    width: int = 900,
    template: str = "plotly_dark",
    volume_df: Optional[pd.DataFrame] = None
) -> go.Figure:
    """
    Create a professional candlestick chart for OHLC data.
    
    Args:
        data: DataFrame with OHLC data
        date_col: Column name for dates
        open_col: Column name for open prices
        high_col: Column name for high prices
        low_col: Column name for low prices
        close_col: Column name for close prices
        title: Chart title
        height: Chart height in pixels
        width: Chart width in pixels
        template: Plotly template name
        volume_df: Optional DataFrame with volume data
        
    Returns:
        go.Figure: Configured Plotly figure
        
    Example:
        >>> fig = create_candlestick_chart(df, title='BTCUSD')
    """
    try:
        # Create candlestick trace
        candlestick = go.Candlestick(
            x=data[date_col],
            open=data[open_col],
            high=data[high_col],
            low=data[low_col],
            close=data[close_col],
            name='OHLC',
            hovertemplate='<b>%{x}</b><br>' +
                         'Open: %{open:.2f}<br>' +
                         'High: %{high:.2f}<br>' +
                         'Low: %{low:.2f}<br>' +
                         'Close: %{close:.2f}<extra></extra>'
        )
        
        # Create layout
        layout = go.Layout(
            title=dict(text=title, font=dict(size=18, color='white')),
            yaxis=dict(title='Price', showgrid=True, gridwidth=1),
            height=height,
            width=width,
            template=template,
            font=dict(family='Arial, sans-serif', size=12, color='white'),
            margin=dict(l=60, r=40, t=80, b=50),
            xaxis_rangeslider_visible=False
        )
        
        fig = go.Figure(data=[candlestick], layout=layout)
        
        # Add volume if provided
        if volume_df is not None:
            volume_trace = go.Bar(
                x=volume_df.index,
                y=volume_df,
                name='Volume',
                marker=dict(color='rgba(128, 128, 128, 0.5)'),
                yaxis='y2',
                hovertemplate='Volume: %{y:,.0f}<extra></extra>'
            )
            fig.add_trace(volume_trace)
            fig.update_layout(
                yaxis2=dict(
                    title='Volume',
                    overlaying='y',
                    side='right'
                )
            )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating candlestick chart: {e}")
        raise


def create_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: Union[str, List[str]],
    title: str = "",
    xaxis_title: str = "Categoria",
    yaxis_title: str = "Valor",
    height: int = 500,
    width: int = 900,
    orientation: str = "v",
    template: str = "plotly_dark",
    **kwargs
) -> go.Figure:
    """
    Create a professional bar chart.
    
    Args:
        data: DataFrame with chart data
        x_col: Column name for X-axis (categories)
        y_col: Column name(s) for Y-axis values
        title: Chart title
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        height: Chart height in pixels
        width: Chart width in pixels
        orientation: 'v' for vertical bars, 'h' for horizontal
        template: Plotly template name
        **kwargs: Additional arguments
        
    Returns:
        go.Figure: Configured Plotly figure
        
    Example:
        >>> fig = create_bar_chart(df, 'category', 'value', title='Sales by Category')
    """
    try:
        y_cols = [y_col] if isinstance(y_col, str) else y_col
        color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        traces = []
        for idx, col in enumerate(y_cols):
            color = color_palette[idx % len(color_palette)]
            trace = go.Bar(
                x=data[x_col] if orientation == 'v' else data[col],
                y=data[col] if orientation == 'v' else data[x_col],
                name=col,
                orientation=orientation,
                marker=dict(color=color),
                hovertemplate=f'<b>{col}</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
            )
            traces.append(trace)
        
        layout = go.Layout(
            title=dict(text=title, font=dict(size=18, color='white')),
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title, showgrid=True),
            height=height,
            width=width,
            template=template,
            font=dict(family='Arial, sans-serif', size=12, color='white'),
            margin=dict(l=60, r=40, t=80, b=50),
            barmode='group',
            hovermode='x unified'
        )
        
        fig = go.Figure(data=traces, layout=layout)
        return fig
        
    except Exception as e:
        logger.error(f"Error creating bar chart: {e}")
        raise


def create_area_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: Union[str, List[str]],
    title: str = "",
    xaxis_title: str = "Data",
    yaxis_title: str = "Valor",
    height: int = 500,
    width: int = 900,
    template: str = "plotly_dark",
    **kwargs
) -> go.Figure:
    """
    Create a professional area chart.
    
    Args:
        data: DataFrame with chart data
        x_col: Column name for X-axis
        y_col: Column name(s) for Y-axis
        title: Chart title
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        height: Chart height in pixels
        width: Chart width in pixels
        template: Plotly template name
        **kwargs: Additional arguments
        
    Returns:
        go.Figure: Configured Plotly figure
    """
    try:
        y_cols = [y_col] if isinstance(y_col, str) else y_col
        color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        traces = []
        for idx, col in enumerate(y_cols):
            color = color_palette[idx % len(color_palette)]
            trace = go.Scatter(
                x=data[x_col],
                y=data[col],
                name=col,
                mode='lines',
                line=dict(width=0.5, color=color),
                fillcolor=color.replace(')', ', 0.3)').replace('rgb', 'rgba'),
                fill='tonexty' if idx > 0 else 'tozeroy',
                hovertemplate=f'<b>{col}</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
            )
            traces.append(trace)
        
        layout = go.Layout(
            title=dict(text=title, font=dict(size=18, color='white')),
            xaxis=dict(title=xaxis_title, showgrid=True),
            yaxis=dict(title=yaxis_title, showgrid=True),
            height=height,
            width=width,
            template=template,
            font=dict(family='Arial, sans-serif', size=12, color='white'),
            margin=dict(l=60, r=40, t=80, b=50),
            hovermode='x unified',
            stackgroup='one'
        )
        
        fig = go.Figure(data=traces, layout=layout)
        return fig
        
    except Exception as e:
        logger.error(f"Error creating area chart: {e}")
        raise


def create_heatmap(
    data: pd.DataFrame,
    title: str = "Correlation Heatmap",
    colorscale: str = "RdBu",
    height: int = 600,
    width: int = 700,
    template: str = "plotly_dark",
    zmin: float = -1.0,
    zmax: float = 1.0
) -> go.Figure:
    """
    Create a professional heatmap (typically for correlation matrices).
    
    Args:
        data: DataFrame with heatmap data (typically correlation matrix)
        title: Chart title
        colorscale: Plotly colorscale name
        height: Chart height in pixels
        width: Chart width in pixels
        template: Plotly template name
        zmin: Minimum value for color scale
        zmax: Maximum value for color scale
        
    Returns:
        go.Figure: Configured Plotly figure
        
    Example:
        >>> corr_matrix = df.corr()
        >>> fig = create_heatmap(corr_matrix, title='Asset Correlations')
    """
    try:
        heatmap = go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index,
            colorscale=colorscale,
            zmid=0,
            zmin=zmin,
            zmax=zmax,
            text=np.round(data.values, 2),
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            hovertemplate='%{y} vs %{x}<br>Correlação: %{z:.3f}<extra></extra>',
            colorbar=dict(title="Correlação")
        )
        
        layout = go.Layout(
            title=dict(text=title, font=dict(size=18, color='white')),
            height=height,
            width=width,
            template=template,
            font=dict(family='Arial, sans-serif', size=11, color='white'),
            margin=dict(l=150, r=100, t=80, b=100),
            xaxis=dict(tickangle=-45)
        )
        
        fig = go.Figure(data=[heatmap], layout=layout)
        return fig
        
    except Exception as e:
        logger.error(f"Error creating heatmap: {e}")
        raise


def add_sma_to_chart(
    fig: go.Figure,
    data: pd.DataFrame,
    x_col: str,
    close_col: str,
    sma_values: Dict[int, pd.Series],
    colors: Optional[List[str]] = None
) -> go.Figure:
    """
    Add Simple Moving Average lines to an existing chart.
    
    Args:
        fig: Existing Plotly figure
        data: Original data DataFrame
        x_col: Column name for X-axis
        close_col: Column name for close prices
        sma_values: Dictionary mapping period -> SMA series {20: sma_20, 50: sma_50}
        colors: Optional list of colors for SMA lines
        
    Returns:
        go.Figure: Updated figure with SMA lines
        
    Example:
        >>> sma_dict = {20: df['SMA_20'], 50: df['SMA_50']}
        >>> fig = add_sma_to_chart(fig, df, 'Date', 'Close', sma_dict)
    """
    try:
        colors = colors or ['#ff9999', '#66b3ff']
        color_palette = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        
        for idx, (period, sma) in enumerate(sma_values.items()):
            color = colors[idx % len(colors)] if colors else color_palette[idx % len(color_palette)]
            fig.add_trace(
                go.Scatter(
                    x=data[x_col],
                    y=sma,
                    name=f'SMA {period}',
                    mode='lines',
                    line=dict(color=color, width=1.5, dash='dash'),
                    hovertemplate=f'<b>SMA {period}</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
                )
            )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error adding SMA to chart: {e}")
        raise


def add_bollinger_bands_to_chart(
    fig: go.Figure,
    data: pd.DataFrame,
    x_col: str,
    upper_band: pd.Series,
    middle_band: pd.Series,
    lower_band: pd.Series,
    band_color: str = 'rgba(100, 150, 200, 0.3)',
    line_color: str = 'rgba(100, 150, 200, 0.6)'
) -> go.Figure:
    """
    Add Bollinger Bands to an existing chart.
    
    Args:
        fig: Existing Plotly figure
        data: Original data DataFrame
        x_col: Column name for X-axis
        upper_band: Upper Bollinger Band series
        middle_band: Middle Bollinger Band (SMA) series
        lower_band: Lower Bollinger Band series
        band_color: Color for the filled band area
        line_color: Color for the band lines
        
    Returns:
        go.Figure: Updated figure with Bollinger Bands
    """
    try:
        # Add upper band
        fig.add_trace(
            go.Scatter(
                x=data[x_col],
                y=upper_band,
                name='Upper Band',
                mode='lines',
                line=dict(color=line_color, width=1),
                showlegend=True,
                hovertemplate='<b>Upper Band</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
            )
        )
        
        # Add lower band with fill between
        fig.add_trace(
            go.Scatter(
                x=data[x_col],
                y=lower_band,
                name='Lower Band',
                mode='lines',
                line=dict(color=line_color, width=1),
                fillcolor=band_color,
                fill='tonexty',
                showlegend=True,
                hovertemplate='<b>Lower Band</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
            )
        )
        
        # Add middle band
        fig.add_trace(
            go.Scatter(
                x=data[x_col],
                y=middle_band,
                name='Middle Band (SMA 20)',
                mode='lines',
                line=dict(color=line_color, width=1.5, dash='dot'),
                showlegend=True,
                hovertemplate='<b>Middle Band</b><br>{{x}}<br>{{y:.2f}}<extra></extra>'
            )
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error adding Bollinger Bands to chart: {e}")
        raise


if __name__ == '__main__':
    # Basic testing
    import sys
    logger.info("Chart builders module loaded successfully")
