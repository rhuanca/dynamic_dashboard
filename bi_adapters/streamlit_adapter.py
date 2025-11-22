"""
Streamlit adapter for rendering dashboards.

This adapter implements the BaseAdapter interface for Streamlit,
allowing dashboards to be rendered as Streamlit apps.
"""

from typing import Any, Dict, List, Union
import streamlit as st
import pandas as pd

from bi_adapters.base import BaseAdapter
from core.specs import WidgetType
from core.transform import DashboardConfig, WidgetConfig


class StreamlitAdapter(BaseAdapter):
    """
    Streamlit implementation of the BaseAdapter.
    
    Renders dashboards and widgets using Streamlit components.
    """
    
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
        """Inject custom CSS for professional dashboard styling."""
        st.markdown("""
            <style>
            /* Main container styling */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 100%;
            }
            
            /* Metric styling for scorecards */
            [data-testid="stMetricValue"] {
                font-size: 2.5rem;
                font-weight: 600;
                color: #1f77b4;
            }
            
            [data-testid="stMetricLabel"] {
                font-size: 1.1rem;
                font-weight: 500;
                color: #31333F;
            }
            
            /* Card-like appearance for metrics */
            [data-testid="metric-container"] {
                background-color: #f8f9fa;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 1.5rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            /* Chart container styling */
            .stPlotlyChart, .element-container {
                background-color: white;
                border-radius: 8px;
                padding: 1rem;
            }
            
            /* Title styling */
            h1 {
                color: #1f1f1f;
                font-weight: 700;
                padding-bottom: 0.5rem;
            }
            
            h2, h3 {
                color: #31333F;
                font-weight: 600;
                margin-top: 1rem;
            }
            
            /* Divider styling */
            hr {
                margin: 1.5rem 0;
                border-color: #e0e0e0;
            }
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
        Render a scorecard using st.metric().
        
        Args:
            config: Widget configuration with scorecard data
        """
        # Extract the value from data
        data = config.data_config.get("data")
        value = self._extract_value(data)
        
        # Get display configuration
        number_format = config.display_config.get("number_format", "auto")
        
        # Format the value
        formatted_value = self._format_number(value, number_format)
        
        # Render using st.metric
        st.metric(
            label=config.title,
            value=formatted_value
        )
    
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
            
            # Create line chart
            fig = px.line(
                df,
                title=config.title,
                template="plotly_white",
                height=400
            )
            
            # Customize layout for professional appearance
            fig.update_layout(
                title={
                    'text': config.title,
                    'font': {'size': 18, 'color': '#31333F', 'family': 'Arial, sans-serif'},
                    'x': 0,
                    'xanchor': 'left'
                },
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode='x unified',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    title_font={'size': 12, 'color': '#666'}
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    title_font={'size': 12, 'color': '#666'}
                )
            )
            
            # Update line styling
            fig.update_traces(
                line=dict(width=3, color='#1f77b4'),
                hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except ImportError:
            # Fallback to basic line chart if Plotly not available
            st.subheader(config.title)
            st.line_chart(df, use_container_width=True)
    
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
            
            # Create bar chart
            fig = px.bar(
                df,
                title=config.title,
                template="plotly_white",
                height=400
            )
            
            # Customize layout for professional appearance
            fig.update_layout(
                title={
                    'text': config.title,
                    'font': {'size': 18, 'color': '#31333F', 'family': 'Arial, sans-serif'},
                    'x': 0,
                    'xanchor': 'left'
                },
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode='x unified',
                xaxis=dict(
                    showgrid=False,
                    title_font={'size': 12, 'color': '#666'}
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    title_font={'size': 12, 'color': '#666'}
                )
            )
            
            # Update bar styling
            fig.update_traces(
                marker_color='#1f77b4',
                hovertemplate='<b>%{y:,.0f}</b><extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except ImportError:
            # Fallback to basic bar chart if Plotly not available
            st.subheader(config.title)
            st.bar_chart(df, use_container_width=True)
    
    def render_table(self, config: WidgetConfig) -> None:
        """
        Render a table using st.dataframe() with enhanced styling.
        
        Args:
            config: Widget configuration with table data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        st.subheader(config.title)
        st.dataframe(df, use_container_width=True, height=400)
    
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
