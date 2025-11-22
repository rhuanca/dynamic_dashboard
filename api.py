"""
Public API for creating dashboards.

This module provides the main entry point for creating dashboards
using the dynamic dashboard library.
"""

from typing import Optional, Union

from core.specs import DashboardSpec, validate_dashboard_spec
from core.transform import transform_dashboard_spec
from bi_adapters.streamlit_adapter import StreamlitAdapter
from themes import Theme


def create_dashboard(
    spec: DashboardSpec,
    adapter: str = "streamlit",
    theme: Optional[Union[str, Theme]] = None
) -> None:
    """
    Create and render a dashboard from a specification.
    
    This is the main entry point for the library. It validates the spec,
    transforms it to a normalized config, and renders it using the specified adapter.
    
    Args:
        spec: Dashboard specification
        adapter: Name of the BI adapter to use ("streamlit", etc.)
        theme: Theme name (str) or Theme object (default: "professional")
        
    Example:
        >>> from api import create_dashboard
        >>> from core.specs import DashboardSpec, WidgetSpec, WidgetType
        >>> 
        >>> dashboard = DashboardSpec(
        ...     dashboard_id="my_dashboard",
        ...     title="My Dashboard",
        ...     widgets=[...]
        ... )
        >>> 
        >>> # Use default professional theme
        >>> create_dashboard(dashboard)
        >>> 
        >>> # Use dark theme
        >>> create_dashboard(dashboard, theme="dark")
        
    Raises:
        ValidationError: If the spec is invalid
        ValueError: If the adapter is not supported
    """
    # Validate the spec
    validate_dashboard_spec(spec)
    
    # Transform to normalized config
    config = transform_dashboard_spec(spec)
    
    # Get the adapter with theme
    if adapter == "streamlit":
        adapter_instance = StreamlitAdapter(theme=theme)
    else:
        raise ValueError(f"Unsupported adapter: {adapter}")
    
    # Render the dashboard
    adapter_instance.render_dashboard(config)
