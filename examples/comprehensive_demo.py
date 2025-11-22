"""
Comprehensive Dashboard Example

This example demonstrates all available widget types:
- Scorecard
- Time Series Chart
- Bar Chart
- Table
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from api import create_dashboard
from core.specs import DashboardSpec, WidgetSpec, WidgetType


# Generate sample data
def generate_sample_data():
    """Generate comprehensive sample data for all widget types."""
    
    # Time series data (30 days)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    sales_data = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(15000, 35000, 30),
        'revenue': np.random.randint(50000, 100000, 30),
    })
    
    # Category data for bar chart
    category_data = pd.DataFrame({
        'category': ['Electronics', 'Clothing', 'Food', 'Books', 'Home'],
        'sales': [45000, 32000, 28000, 15000, 22000]
    })
    
    # Product performance table
    product_data = pd.DataFrame({
        'Product': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Watch'],
        'Units Sold': [1250, 2340, 890, 3200, 1560],
        'Revenue': ['$1.25M', '$2.34M', '$890K', '$320K', '$1.56M'],
        'Growth': ['+12%', '+8%', '-3%', '+25%', '+15%']
    })
    
    return sales_data, category_data, product_data


# Generate data
sales_data, category_data, product_data = generate_sample_data()

# Calculate metrics for scorecards
total_sales = sales_data['sales'].sum()
total_revenue = sales_data['revenue'].sum()
avg_daily_sales = sales_data['sales'].mean()
total_products = len(product_data)

# Create dashboard specification
dashboard = DashboardSpec(
    dashboard_id="comprehensive_demo",
    title="📊 Comprehensive Dashboard Demo",
    description="Demonstrating all available widget types with professional styling",
    layout={
        "type": "grid",
        "columns": 3,
        "gap": "medium"
    },
    widgets=[
        # Row 1: Scorecards
        WidgetSpec(
            widget_id="total_sales",
            widget_type=WidgetType.SCORECARD,
            title="Total Sales (30 days)",
            data={"value": total_sales},
            config={"number_format": "auto"}
        ),
        WidgetSpec(
            widget_id="total_revenue",
            widget_type=WidgetType.SCORECARD,
            title="Total Revenue",
            data={"value": total_revenue},
            config={"number_format": "auto"}
        ),
        WidgetSpec(
            widget_id="avg_daily_sales",
            widget_type=WidgetType.SCORECARD,
            title="Avg Daily Sales",
            data={"value": avg_daily_sales},
            config={"number_format": "auto"}
        ),
        
        # Row 2: Time Series Charts
        WidgetSpec(
            widget_id="sales_trend",
            widget_type=WidgetType.TIME_SERIES,
            title="Daily Sales Trend",
            data=sales_data.copy(),  # Pass full dataframe
            config={"show_legend": True}
        ),
        WidgetSpec(
            widget_id="revenue_trend",
            widget_type=WidgetType.TIME_SERIES,
            title="Daily Revenue Trend",
            data=sales_data[['date', 'revenue']].copy(),  # Only date and revenue
            config={"show_legend": True}
        ),
        
        # Row 3: Bar chart and Table
        WidgetSpec(
            widget_id="category_sales",
            widget_type=WidgetType.BAR_CHART,
            title="Sales by Category",
            data=category_data,
            config={"show_legend": False}
        ),
        WidgetSpec(
            widget_id="product_performance",
            widget_type=WidgetType.TABLE,
            title="Top Products Performance",
            data=product_data,
            config={}
        ),
    ]
)

# Render the dashboard
if __name__ == "__main__":
    create_dashboard(dashboard)
