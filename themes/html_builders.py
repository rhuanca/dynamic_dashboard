"""
HTML Builders for themed components.

This module provides builders for generating themed HTML components,
separating HTML generation from rendering logic.
"""

from typing import Dict
import pandas as pd
from themes.base import Theme


class HTMLCardBuilder:
    """
    Builds themed card wrappers for dashboard widgets.
    """
    
    def __init__(self, theme: Theme):
        """
        Initialize HTML card builder with a theme.
        
        Args:
            theme: Theme configuration
        """
        self.theme = theme
        self.colors = theme.colors
        self.typography = theme.typography
        self.spacing = theme.spacing
    
    def build_scorecard(self, title: str, value: str) -> str:
        """
        Build a themed scorecard HTML.
        
        Args:
            title: Scorecard title
            value: Formatted value to display
            
        Returns:
            HTML string for scorecard
        """
        return f'''<div style="background: {self.colors.card_background}; border: 1px solid {self.colors.border}; border-radius: {self.spacing.card_border_radius}; padding: {self.spacing.card_padding}; box-shadow: {self.spacing.card_shadow}; margin-bottom: {self.spacing.card_margin}; height: 100%;">
<div style="font-size: {self.typography.caption_size}; font-weight: {self.typography.subtitle_weight}; color: {self.colors.text_muted}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">{title}</div>
<div style="font-size: {self.typography.metric_size}; font-weight: {self.typography.title_weight}; color: {self.colors.text_primary}; line-height: 1;">{value}</div>
</div>'''


class HTMLTableBuilder:
    """
    Builds themed HTML tables.
    """
    
    def __init__(self, theme: Theme):
        """
        Initialize HTML table builder with a theme.
        
        Args:
            theme: Theme configuration
        """
        self.theme = theme
        self.colors = theme.colors
        self.typography = theme.typography
        self.spacing = theme.spacing
    
    def build_table(self, df: pd.DataFrame, title: str) -> str:
        """
        Build a themed HTML table.
        
        Args:
            df: DataFrame to render
            title: Table title
            
        Returns:
            HTML string for table
        """
        # Build table headers
        headers = ''.join(
            f'<th style="text-align: left; padding: 12px; color: {self.colors.text_secondary}; font-weight: 600;">{col}</th>'
            for col in df.columns
        )
        
        # Build table rows
        rows = ''.join(
            f'<tr style="border-bottom: 1px solid {self.colors.border};">' +
            ''.join(f'<td style="padding: 10px 12px; color: {self.colors.text_primary};">{val}</td>' for val in row) +
            '</tr>'
            for row in df.values
        )
        
        return f'''
        <div style="background: {self.colors.card_background}; border: 1px solid {self.colors.border}; 
                    border-radius: {self.spacing.card_border_radius}; padding: {self.spacing.card_padding}; 
                    box-shadow: {self.spacing.card_shadow}; margin-bottom: {self.spacing.card_margin};">
            <div style="font-size: {self.typography.subtitle_size}; font-weight: {self.typography.subtitle_weight}; 
                        color: {self.colors.text_primary}; margin-bottom: 16px;">{title}</div>
            <div style="overflow-x: auto; max-height: 400px; overflow-y: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: {self.typography.body_size};">
                    <thead>
                        <tr style="border-bottom: 2px solid {self.colors.border};">
                            {headers}
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        '''
