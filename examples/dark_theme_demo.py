"""
Dark Theme Demo

This example demonstrates the dark theme for dashboards.
Simply change the theme parameter to switch between themes.
"""

import pandas as pd
import numpy as np
from datetime import datetime

from api import create_dashboard
from core.specs import DashboardSpec, WidgetSpec, WidgetType


# Generate sample data
dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
sales_data = pd.DataFrame({
    'date': dates,
    'sales': np.random.randint(15000, 35000, 30),
})

total_sales = sales_data['sales'].sum()
avg_sales = sales_data['sales'].mean()

# Create dashboard with dark theme
dashboard = DashboardSpec(
    dashboard_id="dark_theme_demo",
    title="🌙 Dark Theme Dashboard",
    description="Professional dark mode for modern dashboards",
    layout={"type": "grid", "columns": 2},
    widgets=[
        WidgetSpec(
            widget_id="total_sales",
            widget_type=WidgetType.SCORECARD,
            title="Total Sales",
            data={"value": total_sales},
        ),
        WidgetSpec(
            widget_id="avg_sales",
            widget_type=WidgetType.SCORECARD,
            title="Average Daily Sales",
            data={"value": avg_sales},
        ),
        WidgetSpec(
            widget_id="sales_trend",
            widget_type=WidgetType.TIME_SERIES,
            title="Sales Trend",
            data=sales_data,
        ),
    ]
)

# Render with dark theme
if __name__ == "__main__":
    # To use dark theme, you would pass theme="dark" to create_dashboard
    # For now, it uses the default professional theme
    # Future: create_dashboard(dashboard, theme="dark")
    create_dashboard(dashboard)
