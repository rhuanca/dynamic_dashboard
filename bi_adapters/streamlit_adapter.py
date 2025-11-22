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
        # Set page title and description
        st.title(config.title)
        if config.description:
            st.markdown(config.description)
        
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
        Render a time series chart using st.line_chart().
        
        Args:
            config: Widget configuration with time series data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        st.subheader(config.title)
        st.line_chart(df)
    
    def render_bar_chart(self, config: WidgetConfig) -> None:
        """
        Render a bar chart using st.bar_chart().
        
        Args:
            config: Widget configuration with bar chart data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        st.subheader(config.title)
        st.bar_chart(df)
    
    def render_table(self, config: WidgetConfig) -> None:
        """
        Render a table using st.dataframe().
        
        Args:
            config: Widget configuration with table data
        """
        data = config.data_config.get("data")
        
        # Convert to DataFrame if needed
        df = self._to_dataframe(data)
        
        st.subheader(config.title)
        st.dataframe(df)
    
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
