"""
Dashboard rendering logic with auto-organization.

This module handles the rendering of dashboard widgets with intelligent layout.
"""

import streamlit as st
from typing import List

from bi_adapters.streamlit_adapter import StreamlitAdapter
from core.specs import WidgetType
from core.transform import transform_dashboard_spec, WidgetConfig


def organize_widgets_by_type(widgets: List[WidgetConfig]) -> tuple:
    """
    Organize widgets by type for better layout.
    
    Args:
        widgets: List of widget configurations
        
    Returns:
        Tuple of (scorecards, charts, tables)
    """
    scorecards = []
    charts = []
    tables = []
    
    for widget_config in widgets:
        if widget_config.widget_type == WidgetType.SCORECARD:
            scorecards.append(widget_config)
        elif widget_config.widget_type in [
            WidgetType.TIME_SERIES, 
            WidgetType.BAR_CHART, 
            WidgetType.PIE_CHART
        ]:
            charts.append(widget_config)
        elif widget_config.widget_type == WidgetType.TABLE:
            tables.append(widget_config)
    
    return scorecards, charts, tables


def render_scorecards(adapter: StreamlitAdapter, scorecards: List[WidgetConfig]) -> None:
    """
    Render scorecards in rows of up to 4.
    
    Args:
        adapter: Streamlit adapter instance
        scorecards: List of scorecard widget configurations
    """
    if not scorecards:
        return
    
    for i in range(0, len(scorecards), 4):
        row_scorecards = scorecards[i:i+4]
        cols = st.columns(len(row_scorecards))
        for j, widget_config in enumerate(row_scorecards):
            with cols[j]:
                adapter.render_widget(widget_config)


def render_charts(adapter: StreamlitAdapter, charts: List[WidgetConfig]) -> None:
    """
    Render charts in rows of 2 for better visibility.
    
    Args:
        adapter: Streamlit adapter instance
        charts: List of chart widget configurations
    """
    if not charts:
        return
    
    for i in range(0, len(charts), 2):
        row_charts = charts[i:i+2]
        if len(row_charts) == 1:
            # Single chart - full width
            adapter.render_widget(row_charts[0])
        else:
            # Two charts side by side
            cols = st.columns(2)
            for j, widget_config in enumerate(row_charts):
                with cols[j]:
                    adapter.render_widget(widget_config)


def render_tables(adapter: StreamlitAdapter, tables: List[WidgetConfig]) -> None:
    """
    Render tables at full width.
    
    Args:
        adapter: Streamlit adapter instance
        tables: List of table widget configurations
    """
    if not tables:
        return
    
    for widget_config in tables:
        adapter.render_widget(widget_config)


def render_dashboard_widgets(dashboard_spec) -> None:
    """
    Render dashboard widgets with auto-organization.
    
    Organizes widgets by type:
    - Scorecards at top (up to 4 per row)
    - Charts in middle (2 per row)
    - Tables at bottom (full width)
    
    Args:
        dashboard_spec: Dashboard specification
    """
    # Create adapter with dark theme
    adapter = StreamlitAdapter(theme="dark")
    
    # Transform the dashboard spec to config
    config = transform_dashboard_spec(dashboard_spec)
    
    # Organize widgets by type
    scorecards, charts, tables = organize_widgets_by_type(config.widgets)
    
    # Render scorecards at the top
    render_scorecards(adapter, scorecards)
    
    # Add spacing after scorecards
    if scorecards and (charts or tables):
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Render charts in the middle
    render_charts(adapter, charts)
    
    # Add spacing after charts
    if charts and tables:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # Render tables at the bottom
    render_tables(adapter, tables)
