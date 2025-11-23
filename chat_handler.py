"""
Chat message processing and widget creation logic.

This module handles user commands and creates appropriate widget specifications.
"""

import pandas as pd
import streamlit as st
from typing import Optional

from core.specs import DashboardSpec, WidgetSpec, WidgetType


def create_us_population_widget(widget_count: int) -> WidgetSpec:
    """Create a scorecard widget for US population."""
    return WidgetSpec(
        widget_id=f"us_population_{widget_count}",
        widget_type=WidgetType.SCORECARD,
        title="US Population",
        data={"value": 342_000_000}
    )


def create_sales_chart_widget(widget_count: int) -> WidgetSpec:
    """Create a bar chart widget with sample sales data."""
    sales_data = pd.DataFrame({
        'Category': ['Electronics', 'Clothing', 'Food', 'Books', 'Toys'],
        'Sales': [125000, 89000, 156000, 45000, 67000]
    })
    return WidgetSpec(
        widget_id=f"sales_chart_{widget_count}",
        widget_type=WidgetType.BAR_CHART,
        title="Sales by Category",
        data=sales_data
    )


def create_sales_trend_widget(widget_count: int) -> WidgetSpec:
    """Create a time series widget with sample trend data."""
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    trend_data = pd.DataFrame({
        'Date': dates,
        'Sales': [15000 + i * 500 + (i % 7) * 1000 for i in range(30)]
    })
    return WidgetSpec(
        widget_id=f"sales_trend_{widget_count}",
        widget_type=WidgetType.TIME_SERIES,
        title="Sales Trend (30 Days)",
        data=trend_data
    )


def create_products_table_widget(widget_count: int) -> WidgetSpec:
    """Create a table widget with sample product data."""
    products_data = pd.DataFrame({
        'Product': ['Widget A', 'Widget B', 'Widget C', 'Widget D', 'Widget E'],
        'Price': [29.99, 49.99, 19.99, 39.99, 59.99],
        'Stock': [150, 75, 200, 50, 100],
        'Status': ['In Stock', 'Low Stock', 'In Stock', 'Low Stock', 'In Stock']
    })
    return WidgetSpec(
        widget_id=f"products_table_{widget_count}",
        widget_type=WidgetType.TABLE,
        title="Product Inventory",
        data=products_data
    )


def process_user_message(user_input: str) -> str:
    """
    Process user message and update dashboard if needed.
    
    Handles fixed commands and creates appropriate widgets.
    
    Args:
        user_input: User's message text
        
    Returns:
        Assistant's response message
    """
    user_input_lower = user_input.lower().strip()
    
    # Initialize widgets list if it doesn't exist
    if "widgets" not in st.session_state:
        st.session_state.widgets = []
    
    widget_count = len(st.session_state.widgets)
    new_widget: Optional[WidgetSpec] = None
    response: str = ""
    
    # Match command and create appropriate widget
    if "add us population" in user_input_lower:
        new_widget = create_us_population_widget(widget_count)
        response = "✓ Added US Population scorecard widget"
        
    elif "add sales chart" in user_input_lower:
        new_widget = create_sales_chart_widget(widget_count)
        response = "✓ Added Sales by Category bar chart"
        
    elif "add sales trend" in user_input_lower:
        new_widget = create_sales_trend_widget(widget_count)
        response = "✓ Added Sales Trend time series chart"
        
    elif "add products table" in user_input_lower:
        new_widget = create_products_table_widget(widget_count)
        response = "✓ Added Product Inventory table"
        
    else:
        return (
            f"I received your request: '{user_input}'. "
            "Try one of these commands: 'add us population', 'add sales chart', "
            "'add sales trend', or 'add products table'"
        )
    
    # Add widget and update dashboard
    if new_widget:
        st.session_state.widgets.append(new_widget)
        st.session_state.current_dashboard = DashboardSpec(
            dashboard_id="inventory_dashboard",
            title="Inventory Analysis Dashboard",
            widgets=st.session_state.widgets
        )
    
    return response
