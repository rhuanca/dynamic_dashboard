"""
CSS Builder for theme-based styling.

This module converts theme data into CSS strings, separating styling logic
from rendering logic.
"""

from typing import Dict
from themes.base import Theme


class CSSBuilder:
    """
    Builds CSS from theme configuration.
    
    This class is responsible for converting theme data (colors, typography, spacing)
    into CSS strings that can be injected into the dashboard.
    """
    
    def __init__(self, theme: Theme):
        """
        Initialize CSS builder with a theme.
        
        Args:
            theme: Theme configuration
        """
        self.theme = theme
        self.colors = theme.colors
        self.typography = theme.typography
        self.spacing = theme.spacing
    
    def build_global_css(self) -> str:
        """
        Build global CSS for the entire dashboard.
        
        Returns:
            CSS string with global styles
        """
        return f"""
            <style>
            /* Main container styling */
            .main .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 100%;
                background-color: {self.colors.background} !important;
            }}
            
            /* Streamlit app background */
            .stApp {{
                background-color: {self.colors.background} !important;
            }}
            
            /* Title styling */
            h1 {{
                color: {self.colors.text_primary} !important;
                font-weight: 700;
                padding-bottom: 0.5rem;
                font-size: 28px;
            }}
            
            h2, h3 {{
                color: {self.colors.text_secondary} !important;
                font-weight: 600;
                margin-top: 1rem;
            }}
            
            /* Caption styling */
            .caption, [data-testid="stCaptionContainer"] {{
                color: {self.colors.text_muted} !important;
            }}
            
            /* Divider styling */
            hr {{
                margin: 1.5rem 0;
                border-color: {self.colors.divider} !important;
                background-color: {self.colors.divider} !important;
            }}
            
            {self.build_dataframe_css()}
            
            /* Remove default Streamlit padding */
            .element-container {{
                margin-bottom: 0;
            }}
            </style>
        """
    
    def build_dataframe_css(self) -> str:
        """
        Build CSS specifically for dataframes/tables.
        
        Returns:
            CSS string for dataframe styling
        """
        return f"""
            /* Dataframe styling for theme consistency */
            [data-testid="stDataFrame"] {{
                background-color: {self.colors.card_background} !important;
            }}
            
            .dataframe {{
                background-color: {self.colors.card_background} !important;
                color: {self.colors.text_primary} !important;
                border: 1px solid {self.colors.border} !important;
            }}
            
            .dataframe thead tr {{
                background-color: {self.colors.card_background} !important;
            }}
            
            .dataframe thead th {{
                background-color: {self.colors.card_background} !important;
                color: {self.colors.text_secondary} !important;
                font-weight: 600 !important;
                border-bottom: 2px solid {self.colors.border} !important;
                padding: 12px !important;
            }}
            
            .dataframe tbody tr {{
                background-color: {self.colors.card_background} !important;
                border-bottom: 1px solid {self.colors.border} !important;
            }}
            
            .dataframe tbody tr:hover {{
                background-color: {self.colors.background} !important;
            }}
            
            .dataframe tbody td {{
                color: {self.colors.text_primary} !important;
                padding: 10px 12px !important;
                border-color: {self.colors.border} !important;
            }}
            
            /* Streamlit dataframe container */
            .stDataFrame {{
                background-color: {self.colors.card_background} !important;
                border-radius: 8px !important;
            }}
        """
    
    def get_card_styles(self) -> Dict[str, str]:
        """
        Get card wrapper styles as a dictionary.
        
        Returns:
            Dictionary of CSS properties for card styling
        """
        return {
            "background": self.colors.card_background,
            "border": f"1px solid {self.colors.border}",
            "border-radius": self.spacing.card_border_radius,
            "padding": self.spacing.card_padding,
            "box-shadow": self.spacing.card_shadow,
            "margin-bottom": self.spacing.card_margin,
        }
    
    def get_title_styles(self) -> Dict[str, str]:
        """
        Get title styles as a dictionary.
        
        Returns:
            Dictionary of CSS properties for title styling
        """
        return {
            "font-size": self.typography.subtitle_size,
            "font-weight": self.typography.subtitle_weight,
            "color": self.colors.text_primary,
        }
