"""
Styling module - Theme and styling utilities for consistent UI.

This module provides functions for consistent styling, theming, and visual
customization across the dashboard, following professional patterns.

Functions:
    get_color_palette: Returns color palettes
    apply_metric_style: Applies styling to metric displays
    create_styled_metric_card: Creates styled metric cards
    get_plotly_template: Returns configured Plotly templates
    apply_custom_css: Applies custom CSS to Streamlit app
    create_gradient_color_list: Creates gradient colors
    
Author: Stock Analysis Dashboard
Date: 2024
"""

import streamlit as st
import plotly.graph_objs as go
from typing import Dict, List, Tuple, Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)


# Color Palettes - Following professional design patterns
COLOR_PALETTES = {
    "professional": {
        "primary": "#1f77b4",
        "secondary": "#ff7f0e",
        "success": "#2ca02c",
        "danger": "#d62728",
        "warning": "#ff9999",
        "info": "#17a2b8",
        "neutral": "#808080",
        "dark": "#1a1a1a",
        "light": "#f8f9fa"
    },
    
    "dark_modern": {
        "primary": "#00d4ff",
        "secondary": "#ff6b9d",
        "success": "#1dd1a1",
        "danger": "#ff5252",
        "warning": "#ffa502",
        "info": "#54a0ff",
        "neutral": "#48484e",
        "dark": "#0f0e17",
        "light": "#1e1e2e"
    },
    
    "financial": {
        "primary": "#1f77b4",      # Blue
        "secondary": "#ff7f0e",    # Orange
        "success": "#2ca02c",      # Green (bullish)
        "danger": "#d62728",       # Red (bearish)
        "warning": "#ff9999",      # Light Red
        "info": "#1f77b4",
        "neutral": "#7f7f7f",
        "dark": "#2b2b2b",
        "light": "#e8e8e8"
    },
    
    "warm": {
        "primary": "#e74c3c",
        "secondary": "#f39c12",
        "success": "#27ae60",
        "danger": "#e74c3c",
        "warning": "#f1c40f",
        "info": "#3498db",
        "neutral": "#95a5a6",
        "dark": "#34495e",
        "light": "#ecf0f1"
    }
}


def get_color_palette(palette_name: str = "professional") -> Dict[str, str]:
    """
    Get a color palette by name.
    
    Args:
        palette_name: Name of palette ('professional', 'dark_modern', 'financial', 'warm')
        
    Returns:
        Dict[str, str]: Dictionary of color names to hex values
        
    Example:
        >>> colors = get_color_palette("professional")
        >>> primary_color = colors['primary']
    """
    return COLOR_PALETTES.get(palette_name, COLOR_PALETTES["professional"])


def get_plotly_template(
    theme: str = "dark",
    font_family: str = "Arial, sans-serif",
    font_size: int = 12,
    font_color: str = "white",
    bg_color: str = "#111111",
    gridcolor: str = "rgba(128, 128, 128, 0.2)"
) -> Dict:
    """
    Get a configured Plotly template configuration.
    
    Args:
        theme: 'dark' or 'light'
        font_family: Font family name
        font_size: Default font size
        font_color: Default font color
        bg_color: Background color
        gridcolor: Grid line color
        
    Returns:
        Dict: Plotly layout configuration
        
    Example:
        >>> template = get_plotly_template(theme='dark')
    """
    
    if theme.lower() == "dark":
        return {
            "font": dict(
                family=font_family,
                size=font_size,
                color=font_color
            ),
            "plot_bgcolor": bg_color,
            "paper_bgcolor": bg_color,
            "gridcolor": gridcolor,
            "xaxis": dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=gridcolor,
                zeroline=False
            ),
            "yaxis": dict(
                showgrid=True,
                gridwidth=1,
                gridcolor=gridcolor,
                zeroline=False
            )
        }
    else:
        return {
            "font": dict(
                family=font_family,
                size=font_size,
                color="#1a1a1a"
            ),
            "plot_bgcolor": "#ffffff",
            "paper_bgcolor": "#f8f9fa",
            "gridcolor": "rgba(200, 200, 200, 0.5)",
            "xaxis": dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200, 200, 200, 0.5)"
            ),
            "yaxis": dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="rgba(200, 200, 200, 0.5)"
            )
        }


def apply_custom_css() -> None:
    """
    Apply custom CSS styling to the Streamlit app.
    
    This function applies professional styling following the patterns
    from the reference repository.
    """
    try:
        custom_css = """
        <style>
            /* Main container and padding */
            .main {
                padding: 2rem;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            /* Typography */
            h1 {
                color: #ffffff;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                font-weight: 700;
            }
            
            h2 {
                color: #e0e0e0;
                font-size: 1.8rem;
                margin-bottom: 1rem;
                margin-top: 1.5rem;
                font-weight: 600;
                border-bottom: 2px solid #1f77b4;
                padding-bottom: 0.5rem;
            }
            
            h3 {
                color: #f0f0f0;
                font-size: 1.3rem;
                margin-top: 1rem;
                font-weight: 500;
            }
            
            /* Metric cards */
            .metric-card {
                background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
                border: 1px solid #404050;
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            
            .metric-card:hover {
                border-color: #1f77b4;
                box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
                transform: translateY(-2px);
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: #a0a0a0;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.5rem;
            }
            
            .metric-value {
                font-size: 1.8rem;
                color: #ffffff;
                font-weight: 700;
                font-family: 'Courier New', monospace;
            }
            
            .metric-change {
                font-size: 0.9rem;
                margin-top: 0.5rem;
            }
            
            .metric-change.positive {
                color: #2ca02c;
            }
            
            .metric-change.negative {
                color: #d62728;
            }
            
            /* Cards */
            .content-card {
                background: rgba(30, 30, 46, 0.6);
                border: 1px solid #404050;
                border-radius: 6px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            
            /* Sidebar */
            .sidebar-content {
                background: #1a1a2e;
                padding: 1rem;
                border-radius: 6px;
                border-left: 3px solid #1f77b4;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(90deg, #1f77b4 0%, #1a5fa0 100%);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            .stButton > button:hover {
                background: linear-gradient(90deg, #2485c0 0%, #1a5fa0 100%);
                box-shadow: 0 4px 8px rgba(31, 119, 180, 0.3);
                transform: translateY(-1px);
            }
            
            /* Input fields */
            .stSelectbox, .stTextInput, .stDateInput {
                border-radius: 4px;
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background: rgba(30, 30, 46, 0.8);
                border: 1px solid #404050;
                border-radius: 4px;
            }
            
            .streamlit-expanderHeader:hover {
                background: rgba(31, 119, 180, 0.1);
            }
            
            /* Tables */
            .stDataFrame {
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            
            /* Info/Warning boxes */
            .stInfo, .stSuccess, .stWarning, .stError {
                border-radius: 4px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            
            /* Divider */
            .divider {
                height: 1px;
                background: rgba(128, 128, 128, 0.2);
                margin: 2rem 0;
            }
            
            /* Responsive adjustments */
            @media screen and (max-width: 768px) {
                .main {
                    padding: 1rem;
                }
                
                h1 {
                    font-size: 1.8rem;
                }
                
                h2 {
                    font-size: 1.3rem;
                }
            }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        logger.info("Custom CSS applied successfully")
        
    except Exception as e:
        logger.error(f"Error applying custom CSS: {e}")


def create_gradient_color_list(
    start_color: str,
    end_color: str,
    num_colors: int = 10
) -> List[str]:
    """
    Create a list of gradient colors between two colors.
    
    Args:
        start_color: Starting color (hex format, e.g., '#FF0000')
        end_color: Ending color (hex format, e.g., '#0000FF')
        num_colors: Number of colors to generate
        
    Returns:
        List[str]: List of hex color strings
        
    Example:
        >>> colors = create_gradient_color_list('#FF0000', '#0000FF', 5)
    """
    try:
        # Convert hex to RGB
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        
        colors = []
        for i in range(num_colors):
            ratio = i / (num_colors - 1) if num_colors > 1 else 0
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            colors.append(f"#{r:02x}{g:02x}{b:02x}")
        
        return colors
        
    except Exception as e:
        logger.error(f"Error creating gradient colors: {e}")
        return [start_color, end_color]


def apply_metric_style(
    value: Union[int, float],
    delta: Optional[Union[int, float]] = None,
    delta_color: str = "normal"
) -> Dict[str, str]:
    """
    Get styling configuration for a metric display.
    
    Args:
        value: Metric value
        delta: Change value (positive or negative)
        delta_color: 'normal' (auto green/red), 'inverse', or specific color
        
    Returns:
        Dict[str, str]: Styling dictionary for metric display
        
    Example:
        >>> style = apply_metric_style(100.50, delta=5.25)
    """
    try:
        color_palette = get_color_palette("professional")
        
        # Determine delta color
        if delta is not None:
            if delta_color == "normal":
                delta_color = color_palette["success"] if delta >= 0 else color_palette["danger"]
            elif delta_color == "inverse":
                delta_color = color_palette["danger"] if delta >= 0 else color_palette["success"]
        
        return {
            "value_color": "#ffffff",
            "label_color": "#a0a0a0",
            "delta_color": delta_color or color_palette["info"]
        }
        
    except Exception as e:
        logger.error(f"Error applying metric style: {e}")
        return {"value_color": "#ffffff", "label_color": "#a0a0a0"}


def get_asset_color(asset: str, palette: Optional[Dict] = None) -> str:
    """
    Get a consistent color for an asset based on its name.
    
    This ensures the same asset always gets the same color across charts.
    
    Args:
        asset: Asset name/symbol
        palette: Optional color palette dictionary
        
    Returns:
        str: Hex color code
        
    Example:
        >>> color = get_asset_color("AAPL")
    """
    try:
        color_list = [
            "#1f77b4",  # Blue
            "#ff7f0e",  # Orange
            "#2ca02c",  # Green
            "#d62728",  # Red
            "#9467bd",  # Purple
            "#8c564b",  # Brown
            "#e377c2",  # Pink
            "#7f7f7f",  # Gray
            "#bcbd22",  # Olive
            "#17becf"   # Cyan
        ]
        
        # Use hash of asset name to get consistent index
        asset_hash = hash(asset.upper()) % len(color_list)
        return color_list[asset_hash]
        
    except Exception as e:
        logger.error(f"Error getting asset color: {e}")
        return "#1f77b4"


def create_styled_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: Optional[str] = None,
    icon: Optional[str] = None
) -> str:
    """
    Create HTML for a styled metric card.
    
    Args:
        label: Metric label
        value: Metric value (already formatted)
        delta: Change value text (already formatted)
        delta_color: Color for delta ('green', 'red', etc.)
        icon: Optional emoji or icon
        
    Returns:
        str: HTML string for the metric card
        
    Example:
        >>> html = create_styled_metric_card("Preço Atual", "R$ 100,50", "+5%", "green", "📈")
    """
    try:
        icon_html = f"<span style='font-size: 1.5rem; margin-right: 0.5rem;'>{icon}</span>" if icon else ""
        delta_html = ""
        
        if delta:
            delta_color = delta_color or "green" if "+" in delta else "red"
            delta_color_code = {
                "green": "#2ca02c",
                "red": "#d62728",
                "gray": "#808080"
            }.get(delta_color, "#808080")
            
            delta_html = f"""
            <div style='font-size: 0.9rem; color: {delta_color_code}; margin-top: 0.3rem;'>
                {delta}
            </div>
            """
        
        html = f"""
        <div class='metric-card'>
            <div style='display: flex; align-items: center;'>
                {icon_html}
                <div>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                    {delta_html}
                </div>
            </div>
        </div>
        """
        
        return html
        
    except Exception as e:
        logger.error(f"Error creating styled metric card: {e}")
        return f"<div>{label}: {value}</div>"


if __name__ == '__main__':
    logger.info("Styling module loaded successfully")
