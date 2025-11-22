"""
Streamlit adapter for rendering dashboards.

This adapter implements the BaseAdapter interface for Streamlit,
allowing dashboards to be rendered as Streamlit apps.
"""

from typing import Any, Dict, List, Union, Optional
import streamlit as st
import pandas as pd

from bi_adapters.base import BaseAdapter
from core.specs import WidgetType
from core.transform import DashboardConfig, WidgetConfig
from themes import get_theme, Theme


class StreamlitAdapter(BaseAdapter):
    """
    Streamlit implementation of the BaseAdapter.
    
    Renders dashboards and widgets using Streamlit components with theme support.
    """
    
    def __init__(self, theme: Optional[Union[str, Theme]] = None):
        """
        Initialize the Streamlit adapter.
        
        Args:
            theme: Theme name (str) or Theme object. Defaults to "professional".
        """
        if theme is None:
            self.theme = get_theme("professional")
        elif isinstance(theme, str):
            self.theme = get_theme(theme)
        else:
            self.theme = theme
    
    def render_dashboard(self, config: DashboardConfig) -> None:
        """
        Render a complete dashboard in Streamlit.
        
        Args:
            config: Normalized dashboard configuration
        """
        # Configure page for wide layout and professional appearance
        st.set_page_config(
            page_title=config.title,
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Add custom CSS for professional styling
        self._inject_custom_css()
        
        # Set page title and description
        st.title(config.title)
        if config.description:
            st.markdown(f"*{config.description}*")
        
        # Add spacing
        st.markdown("---")
        
        # Apply global filters if any
        # TODO: Implement global filter UI
        
        # Render widgets based on layout
        layout_type = config.layout_config.get("type", "grid")
        
        if layout_type == "grid":
            self._render_grid_layout(config)
        else:
            # Default: render widgets sequentially
            for widget_config in config.widgets:
                self.render_widget(widget_config)
    
    def _inject_custom_css(self) -> None:
        """Inject custom CSS for professional dashboard styling using theme."""
        colors = self.theme.colors
        st.markdown(f"""
            <style>
            /* Main container styling */
            .main .block-container {{
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 100%;
                background-color: {colors.background};
            }}
            
            /* Title styling */
            h1 {{
                color: {colors.text_primary};
                font-weight: 700;
                padding-bottom: 0.5rem;
                font-size: 28px;
            }}
            
            h2, h3 {{
                color: {colors.text_secondary};
                font-weight: 600;
                margin-top: 1rem;
            }}
            
            /* Divider styling */
            hr {{
                margin: 1.5rem 0;
                border-color: {colors.divider};
            }}
            
            /* Remove default Streamlit padding */
            .element-container {{
                margin-bottom: 0;
            }}
            </style>
        """, unsafe_allow_html=True)
    
    def _render_grid_layout(self, config: DashboardConfig) -> None:
        """
        Render widgets in a grid layout using Streamlit columns.
        
        Args:
            config: Dashboard configuration
        """
        columns_count = config.layout_config.get("columns", 3)
        widget_positions = config.layout_config.get("widget_positions", {})
        
        # If no explicit positions, render in rows of N columns
        if not widget_positions:
            widgets = config.widgets
            for i in range(0, len(widgets), columns_count):
                cols = st.columns(columns_count)
                for j, widget_config in enumerate(widgets[i:i + columns_count]):
                    with cols[j]:
                        self.render_widget(widget_config)
        else:
            # TODO: Implement explicit positioning
            # For now, fall back to sequential rendering
            for widget_config in config.widgets:
                self.render_widget(widget_config)
    
    def render_widget(self, config: WidgetConfig) -> None:
        """
        Render a widget based on its type.
        
        Args:
            config: Widget configuration
        """
        widget_type = config.widget_type
        
        if widget_type == WidgetType.SCORECARD:
            self.render_scorecard(config)
        elif widget_type == WidgetType.TIME_SERIES:
            self.render_time_series(config)
        elif widget_type == WidgetType.BAR_CHART:
            self.render_bar_chart(config)
        elif widget_type == WidgetType.TABLE:
            self.render_table(config)
        else:
            st.warning(f"Widget type {widget_type} not yet implemented")
    
    def render_scorecard(self, config: WidgetConfig) -> None:
        """
        Render a professional scorecard with clean business styling.
        
        Args:
            config: Widget configuration with scorecard data
        """
        # Extract the value from data
        data = config.data_config.get("data")
        value = self._extract_value(data)
        
        # Format the value professionally
        formatted_value = self._format_large_number(value)
        
        # Get theme settings
        colors = self.theme.colors
        typography = self.theme.typography
        spacing = self.theme.spacing
        
        # Create clean, professional scorecard HTML using theme
        scorecard_html = f'''<div style="background: {colors.card_background}; border: 1px solid {colors.border}; border-radius: {spacing.card_border_radius}; padding: {spacing.card_padding}; box-shadow: {spacing.card_shadow}; margin-bottom: {spacing.card_margin}; height: 100%;">
<div style="font-size: {typography.caption_size}; font-weight: {typography.subtitle_weight}; color: {colors.text_muted}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px;">{config.title}</div>
<div style="font-size: {typography.metric_size}; font-weight: {typography.title_weight}; color: {colors.text_primary}; line-height: 1;">{formatted_value}</div>
</div>'''
        
        # Render using st.markdown
        st.markdown(scorecard_html, unsafe_allow_html=True)
    
    def render_time_series(self, config: WidgetConfig) -> None:
        """
        Render a time series chart using Plotly for better interactivity.
        
        Args:
            config: Widget configuration with time series data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        # Use Plotly for better-looking charts
        try:
            import plotly.express as px
            
            # Get column names - assume first column is x-axis, rest are y-axis
            columns = df.columns.tolist()
            x_col = columns[0] if len(columns) > 0 else None
            y_cols = columns[1:] if len(columns) > 1 else columns
            
            # Create line chart with explicit x and y
            fig = px.line(
                df,
                x=x_col,
                y=y_cols,
                title=config.title,
                template="plotly_white",
                height=380
            )
            
            # Customize layout for professional appearance using theme
            colors = self.theme.colors
            fig.update_layout(
                title={
                    'text': config.title,
                    'font': {'size': 16, 'color': colors.text_primary, 'family': self.theme.typography.font_family, 'weight': 600},
                    'x': 0,
                    'xanchor': 'left',
                    'y': 0.98,
                    'yanchor': 'top'
                },
                plot_bgcolor=colors.card_background,
                paper_bgcolor=colors.card_background,
                margin=dict(l=10, r=10, t=50, b=10),
                hovermode='x unified',
                xaxis=dict(
                    showgrid=True,
                    gridcolor=colors.chart_grid,
                    title_font={'size': 11, 'color': colors.text_muted},
                    tickfont={'size': 10, 'color': colors.text_muted},
                    showline=True,
                    linecolor=colors.chart_axis
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor=colors.chart_grid,
                    title_font={'size': 11, 'color': colors.text_muted},
                    tickfont={'size': 10, 'color': colors.text_muted},
                    showline=True,
                    linecolor=colors.chart_axis
                ),
                showlegend=True,
                legend=dict(
                    font={'size': 10, 'color': colors.text_muted},
                    orientation='h',
                    yanchor='bottom',
                    y=1.02,
                    xanchor='right',
                    x=1
                )
            )
            
            # Update line styling
            fig.update_traces(
                line=dict(width=2.5, color=colors.chart_primary),
                hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
            )
            
            # Add border styling via Plotly
            fig.update_xaxes(mirror=True)
            fig.update_yaxes(mirror=True)
            
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            
        except ImportError:
            # Fallback to basic line chart if Plotly not available
            st.subheader(config.title)
            st.line_chart(df, width='stretch')
    
    def render_bar_chart(self, config: WidgetConfig) -> None:
        """
        Render a bar chart using Plotly for better interactivity.
        
        Args:
            config: Widget configuration with bar chart data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        # Use Plotly for better-looking charts
        try:
            import plotly.express as px
            
            # Get column names - assume first column is x-axis, second is y-axis
            columns = df.columns.tolist()
            x_col = columns[0] if len(columns) > 0 else None
            y_col = columns[1] if len(columns) > 1 else columns[0]
            
            # Create bar chart with explicit x and y
            fig = px.bar(
                df,
                x=x_col,
                y=y_col,
                title=config.title,
                template="plotly_white",
                height=380
            )
            
            # Customize layout for professional appearance using theme
            colors = self.theme.colors
            fig.update_layout(
                title={
                    'text': config.title,
                    'font': {'size': 16, 'color': colors.text_primary, 'family': self.theme.typography.font_family, 'weight': 600},
                    'x': 0,
                    'xanchor': 'left',
                    'y': 0.98,
                    'yanchor': 'top'
                },
                plot_bgcolor=colors.card_background,
                paper_bgcolor=colors.card_background,
                margin=dict(l=10, r=10, t=50, b=10),
                hovermode='x unified',
                xaxis=dict(
                    showgrid=False,
                    title_font={'size': 11, 'color': colors.text_muted},
                    tickfont={'size': 10, 'color': colors.text_muted},
                    showline=True,
                    linecolor=colors.chart_axis
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor=colors.chart_grid,
                    title_font={'size': 11, 'color': colors.text_muted},
                    tickfont={'size': 10, 'color': colors.text_muted},
                    showline=True,
                    linecolor=colors.chart_axis
                )
            )
            
            # Update bar styling
            fig.update_traces(
                marker_color=colors.chart_primary,
                hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
            )
            
            # Add border styling
            fig.update_xaxes(mirror=True)
            fig.update_yaxes(mirror=True)
            
            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            
        except ImportError:
            # Fallback to basic bar chart if Plotly not available
            st.subheader(config.title)
            st.bar_chart(df, width='stretch')
    
    def render_table(self, config: WidgetConfig) -> None:
        """
        Render a table using st.dataframe() with enhanced styling.
        
        Args:
            config: Widget configuration with table data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        # Use container for consistent styling
        with st.container():
            st.markdown(f'<div style="font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 8px;">{config.title}</div>', unsafe_allow_html=True)
            st.dataframe(df, width='stretch', height=400)
    
    # Helper methods
    
    def _extract_value(self, data: Any) -> Union[int, float, str]:
        """
        Extract a single value from various data formats.
        
        Args:
            data: Data in various formats (scalar, dict, list, DataFrame)
            
        Returns:
            Extracted value
        """
        # If it's already a scalar, return it
        if isinstance(data, (int, float, str)):
            return data
        
        # If it's a dict, try to get 'value' key or first value
        if isinstance(data, dict):
            if "value" in data:
                return data["value"]
            # Return first value
            return next(iter(data.values())) if data else 0
        
        # If it's a list, return first element
        if isinstance(data, list):
            return data[0] if data else 0
        
        # If it's a DataFrame, get the first value
        if isinstance(data, pd.DataFrame):
            return data.iloc[0, 0] if not data.empty else 0
        
        # Default
        return str(data)
    
    def _format_number(self, value: Union[int, float, str], format_type: str) -> str:
        """
        Format a number according to the specified format.
        
        Args:
            value: Value to format
            format_type: Format type ("auto", "decimal", "percent", etc.)
            
        Returns:
            Formatted string
        """
        if format_type == "auto":
            # Auto-detect format based on value
            if isinstance(value, (int, float)):
                # Add thousand separators for large numbers
                if abs(value) >= 1000:
                    return f"{value:,.0f}"
                return str(value)
        
        # For now, just return string representation
        return str(value)
    
    def _format_large_number(self, value: Union[int, float]) -> str:
        """
        Format large numbers with K, M, B suffixes.
        
        Args:
            value: Numeric value to format
            
        Returns:
            Formatted string (e.g., "1.5K", "2.3M", "1.2B")
        """
        if not isinstance(value, (int, float)):
            return str(value)
        
        abs_value = abs(value)
        sign = "-" if value < 0 else ""
        
        if abs_value >= 1_000_000_000:
            return f"{sign}${abs_value / 1_000_000_000:.1f}B"
        elif abs_value >= 1_000_000:
            return f"{sign}${abs_value / 1_000_000:.1f}M"
        elif abs_value >= 1_000:
            return f"{sign}${abs_value / 1_000:.1f}K"
        else:
            return f"{sign}${abs_value:,.0f}"
    
    def _render_sparkline_svg(self, data: List[float]) -> str:
        """
        Render a mini sparkline chart as SVG.
        
        Args:
            data: List of numeric values
            
        Returns:
            SVG string for the sparkline
        """
        if not data or len(data) < 2:
            return ""
        
        # Normalize data to 0-1 range
        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val if max_val != min_val else 1
        
        normalized = [(v - min_val) / range_val for v in data]
        
        # SVG dimensions
        width = 120
        height = 30
        
        # Calculate points for polyline
        x_step = width / (len(data) - 1)
        points = []
        for i, val in enumerate(normalized):
            x = i * x_step
            y = height - (val * height)  # Invert Y axis
            points.append(f"{x},{y}")
        
        points_str = " ".join(points)
        
        # Create SVG
        svg = f"""
        <svg width="{width}" height="{height}" style="display: block;">
            <polyline
                points="{points_str}"
                fill="none"
                stroke="rgba(255, 255, 255, 0.8)"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
        </svg>
        """
        
        return svg
    
    def _to_dataframe(self, data: Any) -> pd.DataFrame:
        """
        Convert various data formats to pandas DataFrame.
        
        Args:
            data: Data in various formats
            
        Returns:
            DataFrame representation
        """
        if isinstance(data, pd.DataFrame):
            return data
        
        if isinstance(data, dict):
            return pd.DataFrame(data)
        
        if isinstance(data, list):
            return pd.DataFrame(data)
        
        # Default: create a simple DataFrame
        return pd.DataFrame([data])

