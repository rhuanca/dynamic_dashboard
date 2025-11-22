"""
Base adapter interface for BI platforms.

All BI adapters must inherit from BaseAdapter and implement its abstract methods.
"""

from abc import ABC, abstractmethod
from core.transform import DashboardConfig, WidgetConfig


class BaseAdapter(ABC):
    """
    Abstract base class for BI platform adapters.
    
    Adapters are responsible for rendering dashboards and widgets
    on specific BI platforms (Streamlit, Looker Studio, etc.).
    """
    
    @abstractmethod
    def render_dashboard(self, config: DashboardConfig) -> None:
        """
        Render a complete dashboard.
        
        Args:
            config: Normalized dashboard configuration
        """
        pass
    
    @abstractmethod
    def render_widget(self, config: WidgetConfig) -> None:
        """
        Render a single widget based on its type.
        
        Args:
            config: Normalized widget configuration
        """
        pass
    
    @abstractmethod
    def render_scorecard(self, config: WidgetConfig) -> None:
        """
        Render a scorecard widget.
        
        Args:
            config: Widget configuration with scorecard data
        """
        pass
    
    @abstractmethod
    def render_time_series(self, config: WidgetConfig) -> None:
        """
        Render a time series chart widget.
        
        Args:
            config: Widget configuration with time series data
        """
        pass
    
    @abstractmethod
    def render_bar_chart(self, config: WidgetConfig) -> None:
        """
        Render a bar chart widget.
        
        Args:
            config: Widget configuration with bar chart data
        """
        pass
    
    @abstractmethod
    def render_table(self, config: WidgetConfig) -> None:
        """
        Render a table widget.
        
        Args:
            config: Widget configuration with table data
        """
        pass
