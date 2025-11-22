"""
Dashboard and widget specification types and validation.

This module defines the core data structures for describing dashboards
and widgets in a BI-agnostic way.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class WidgetType(Enum):
    """Supported widget types."""
    SCORECARD = "scorecard"
    TIME_SERIES = "time_series"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    TABLE = "table"
    FILTER = "filter"
    TEXT = "text"


class AggregationType(Enum):
    """Aggregation functions for metrics."""
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinct_count"


@dataclass
class WidgetSpec:
    """
    Specification for a single dashboard widget.
    
    Attributes:
        widget_id: Unique identifier for this widget
        widget_type: Type of widget (scorecard, chart, etc.)
        title: Display title for the widget
        data: Data for the widget - can be:
            - Direct data: dict, list, pandas DataFrame, or scalar value
            - String reference: name of a data source (for future use)
        metrics: List of metric field names to display (optional for direct data)
        dimensions: List of dimension field names (for grouping/filtering)
        filters: Optional filter conditions
        aggregation: Aggregation type for metrics
        config: Additional widget-specific configuration
    """
    widget_id: str
    widget_type: WidgetType
    title: str
    data: Union[str, Dict, List, Any]
    metrics: List[str] = field(default_factory=list)
    dimensions: List[str] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    aggregation: Optional[AggregationType] = None
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardSpec:
    """
    Specification for a complete dashboard.
    
    Attributes:
        dashboard_id: Unique identifier for this dashboard
        title: Display title for the dashboard
        description: Optional description
        widgets: List of widget specifications
        layout: Optional layout configuration
        global_filters: Filters that apply to all widgets
        metadata: Additional metadata (tags, owner, etc.)
    """
    dashboard_id: str
    title: str
    description: str = ""
    widgets: List[WidgetSpec] = field(default_factory=list)
    layout: Dict[str, Any] = field(default_factory=dict)
    global_filters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ValidationError(Exception):
    """Raised when a dashboard or widget spec is invalid."""
    pass


def validate_widget_spec(spec: WidgetSpec) -> None:
    """
    Validate a widget specification.
    
    Args:
        spec: The widget spec to validate
        
    Raises:
        ValidationError: If the spec is invalid
    """
    if not spec.widget_id:
        raise ValidationError("widget_id is required")
    
    if not spec.title:
        raise ValidationError(f"Widget {spec.widget_id}: title is required")
    
    if spec.data is None:
        raise ValidationError(f"Widget {spec.widget_id}: data is required")
    
    # For string data references (not direct data), validate metrics/dimensions
    is_direct_data = not isinstance(spec.data, str)
    
    # Validate that metrics or dimensions are provided for data widgets with string references
    if spec.widget_type not in (WidgetType.TEXT, WidgetType.FILTER):
        if not is_direct_data and not spec.metrics and not spec.dimensions:
            raise ValidationError(
                f"Widget {spec.widget_id}: at least one metric or dimension is required "
                f"when using string data references"
            )
    
    # Validate aggregation is set for metric-based widgets (when metrics are explicitly specified)
    if spec.metrics and spec.widget_type != WidgetType.TABLE:
        if not spec.aggregation:
            raise ValidationError(
                f"Widget {spec.widget_id}: aggregation is required when metrics are specified"
            )


def validate_dashboard_spec(spec: DashboardSpec) -> None:
    """
    Validate a dashboard specification.
    
    Args:
        spec: The dashboard spec to validate
        
    Raises:
        ValidationError: If the spec is invalid
    """
    if not spec.dashboard_id:
        raise ValidationError("dashboard_id is required")
    
    if not spec.title:
        raise ValidationError("Dashboard title is required")
    
    # Validate each widget
    for widget in spec.widgets:
        validate_widget_spec(widget)
    
    # Check for duplicate widget IDs
    widget_ids = [w.widget_id for w in spec.widgets]
    if len(widget_ids) != len(set(widget_ids)):
        duplicates = [wid for wid in widget_ids if widget_ids.count(wid) > 1]
        raise ValidationError(f"Duplicate widget IDs found: {set(duplicates)}")
