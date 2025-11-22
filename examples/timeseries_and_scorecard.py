"""
Dashboard example with time series and scorecard widgets.

This demonstrates:
- Multiple widgets in one dashboard
- Time series chart with date-indexed data
- Scorecard showing a summary metric
- Grid layout with multiple columns
"""

import pandas as pd
from datetime import datetime, timedelta
from core.specs import DashboardSpec, WidgetSpec, WidgetType
from api import create_dashboard


# Generate sample time series data (daily sales for last 30 days)
dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
sales = [15000 + (i * 500) + (i % 7) * 1000 for i in range(30)]  # Trending up with weekly pattern

sales_data = pd.DataFrame({
    'date': dates,
    'sales': sales
})
sales_data.set_index('date', inplace=True)

# Calculate total sales for the scorecard
total_sales = sales_data['sales'].sum()

# Create dashboard with both widgets
dashboard = DashboardSpec(
    dashboard_id="sales_dashboard",
    title="📊 Sales Performance Dashboard",
    description="Track daily sales trends and total revenue over the last 30 days",
    widgets=[
        # Scorecard showing total sales
        WidgetSpec(
            widget_id="total_sales_scorecard",
            widget_type=WidgetType.SCORECARD,
            title="Total Sales (30 days)",
            data={"value": total_sales},
            config={
                "number_format": "auto"
            }
        ),
        # Time series showing daily sales
        WidgetSpec(
            widget_id="daily_sales_timeseries",
            widget_type=WidgetType.TIME_SERIES,
            title="Daily Sales Trend",
            data=sales_data,  # Pass DataFrame directly!
            config={
                "show_legend": True,
                "color_scheme": "blue"
            }
        )
    ],
    layout={
        "type": "grid",
        "columns": 2  # Two columns: scorecard on left, chart on right
    }
)

# Render the dashboard
create_dashboard(dashboard, adapter="streamlit")
