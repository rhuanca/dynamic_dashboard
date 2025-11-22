"""
Simple scorecard example showing US population.

This demonstrates the basic usage of the dynamic dashboard library
with direct data passing.
"""

from core.specs import DashboardSpec, WidgetSpec, WidgetType
from api import create_dashboard


# Create a simple dashboard with one scorecard
dashboard = DashboardSpec(
    dashboard_id="us_population_dashboard",
    title="🇺🇸 United States Population Dashboard",
    description="A simple dashboard showing the current US population estimate",
    widgets=[
        WidgetSpec(
            widget_id="population_scorecard",
            widget_type=WidgetType.SCORECARD,
            title="Total Population",
            data={"value": 331900000},  # Direct data passing!
            config={
                "number_format": "auto"
            }
        )
    ],
    layout={
        "type": "grid",
        "columns": 1
    }
)

# Render the dashboard
create_dashboard(dashboard, adapter="streamlit")
