"""
Public API for the dynamic dashboard library.

This module provides the main entry points for creating and managing dashboards.
"""

from typing import Optional

from core.specs import DashboardSpec, validate_dashboard_spec
from core.transform import transform_dashboard_spec
from bi_adapters.base import BaseAdapter
from bi_adapters.streamlit_adapter import StreamlitAdapter


def create_dashboard(
    spec: DashboardSpec,
    adapter: str = "streamlit"
) -> None:
    """
    Create and render a dashboard from a specification.
    
    This is the main entry point for the library. It validates the spec,
    transforms it to a normalized config, and renders it using the specified adapter.
    
    Args:
        spec: Dashboard specification
        adapter: Name of the BI adapter to use ("streamlit", etc.)
        
    Raises:
        ValidationError: If the spec is invalid
        ValueError: If the adapter is not supported
    """
    # Validate the spec
    validate_dashboard_spec(spec)
    
    # Transform to normalized config
    config = transform_dashboard_spec(spec)
    
    # Get the adapter
    adapter_instance = _get_adapter(adapter)
    
    # Render the dashboard
    adapter_instance.render_dashboard(config)


def _get_adapter(adapter_name: str) -> BaseAdapter:
    """
    Get an adapter instance by name.
    
    Args:
        adapter_name: Name of the adapter
        
    Returns:
        Adapter instance
        
    Raises:
        ValueError: If adapter is not supported
    """
    adapters = {
        "streamlit": StreamlitAdapter,
    }
    
    adapter_class = adapters.get(adapter_name.lower())
    if not adapter_class:
        supported = ", ".join(adapters.keys())
        raise ValueError(
            f"Unsupported adapter: {adapter_name}. "
            f"Supported adapters: {supported}"
        )
    
    return adapter_class()
