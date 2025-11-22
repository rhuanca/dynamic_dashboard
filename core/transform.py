"""
Transform dashboard specs into BI-agnostic configurations.

This module takes validated DashboardSpec and WidgetSpec objects and transforms
them into normalized, BI-agnostic configuration dictionaries that can be consumed
by different BI adapters.
"""

from dataclasses import dataclass
from typing import Any, Dict, List
from core.specs import DashboardSpec, WidgetSpec, WidgetType, AggregationType


@dataclass
class WidgetConfig:
    """
    Normalized, BI-agnostic widget configuration.
    
    This is the intermediate representation between specs and BI-specific implementations.
    
    Attributes:
        widget_id: Unique identifier
        widget_type: Type of widget
        title: Display title
        data_config: Normalized data configuration (source, fields, aggregations)
        filter_config: Normalized filter configuration
        display_config: Display-related settings (colors, formatting, etc.)
    """
    widget_id: str
    widget_type: WidgetType
    title: str
    data_config: Dict[str, Any]
    filter_config: Dict[str, Any]
    display_config: Dict[str, Any]


@dataclass
class DashboardConfig:
    """
    Normalized, BI-agnostic dashboard configuration.
    
    Attributes:
        dashboard_id: Unique identifier
        title: Display title
        description: Dashboard description
        widgets: List of normalized widget configurations
        layout_config: Layout configuration
        global_filter_config: Global filters that apply to all widgets
        metadata: Additional metadata
    """
    dashboard_id: str
    title: str
    description: str
    widgets: List[WidgetConfig]
    layout_config: Dict[str, Any]
    global_filter_config: Dict[str, Any]
    metadata: Dict[str, Any]


def transform_widget_spec(spec: WidgetSpec) -> WidgetConfig:
    """
    Transform a WidgetSpec into a normalized WidgetConfig.
    
    Args:
        spec: The widget specification to transform
        
    Returns:
        Normalized widget configuration
    """
    # Normalize data configuration
    data_config = {
        "data": spec.data,  # Can be direct data or string reference
        "metrics": spec.metrics,
        "dimensions": spec.dimensions,
        "aggregation": spec.aggregation.value if spec.aggregation else None,
    }
    
    # Normalize filter configuration
    filter_config = {
        "filters": spec.filters,
    }
    
    # Extract display configuration from widget config
    # Separate display concerns from data concerns
    display_config = {
        "show_legend": spec.config.get("show_legend", True),
        "color_scheme": spec.config.get("color_scheme", "default"),
        "number_format": spec.config.get("number_format", "auto"),
        "date_format": spec.config.get("date_format", "auto"),
        # Pass through any other display-related config
        **{k: v for k, v in spec.config.items() 
           if k not in ("show_legend", "color_scheme", "number_format", "date_format")}
    }
    
    return WidgetConfig(
        widget_id=spec.widget_id,
        widget_type=spec.widget_type,
        title=spec.title,
        data_config=data_config,
        filter_config=filter_config,
        display_config=display_config,
    )


def transform_dashboard_spec(spec: DashboardSpec) -> DashboardConfig:
    """
    Transform a DashboardSpec into a normalized DashboardConfig.
    
    Args:
        spec: The dashboard specification to transform
        
    Returns:
        Normalized dashboard configuration
    """
    # Transform all widgets
    widget_configs = [transform_widget_spec(w) for w in spec.widgets]
    
    # Normalize layout configuration
    layout_config = {
        "type": spec.layout.get("type", "grid"),  # default to grid layout
        "columns": spec.layout.get("columns", 12),  # 12-column grid by default
        "widget_positions": spec.layout.get("widget_positions", {}),
        **{k: v for k, v in spec.layout.items() 
           if k not in ("type", "columns", "widget_positions")}
    }
    
    # Normalize global filter configuration
    global_filter_config = {
        "filters": spec.global_filters,
    }
    
    return DashboardConfig(
        dashboard_id=spec.dashboard_id,
        title=spec.title,
        description=spec.description,
        widgets=widget_configs,
        layout_config=layout_config,
        global_filter_config=global_filter_config,
        metadata=spec.metadata,
    )


def apply_global_filters(
    widget_config: WidgetConfig,
    global_filters: Dict[str, Any]
) -> WidgetConfig:
    """
    Apply global dashboard filters to a widget configuration.
    
    Global filters are merged with widget-specific filters. Widget filters
    take precedence in case of conflicts.
    
    Args:
        widget_config: The widget configuration to update
        global_filters: Global filters to apply
        
    Returns:
        Updated widget configuration with merged filters
    """
    # Merge global filters with widget filters (widget filters take precedence)
    merged_filters = {**global_filters, **widget_config.filter_config.get("filters", {})}
    
    # Create a new widget config with merged filters
    updated_filter_config = {
        **widget_config.filter_config,
        "filters": merged_filters,
    }
    
    return WidgetConfig(
        widget_id=widget_config.widget_id,
        widget_type=widget_config.widget_type,
        title=widget_config.title,
        data_config=widget_config.data_config,
        filter_config=updated_filter_config,
        display_config=widget_config.display_config,
    )
