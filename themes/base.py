"""
Theme system for dynamic dashboards.

This module provides theme configurations for consistent styling across dashboards.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ThemeColors:
    """Color palette for a theme."""
    # Background colors
    background: str
    card_background: str
    
    # Border and divider colors
    border: str
    divider: str
    
    # Text colors
    text_primary: str
    text_secondary: str
    text_muted: str
    
    # Chart colors
    chart_primary: str
    chart_grid: str
    chart_axis: str
    
    # Status colors
    positive: str
    negative: str


@dataclass
class ThemeTypography:
    """Typography settings for a theme."""
    font_family: str
    
    # Font sizes
    title_size: str
    subtitle_size: str
    body_size: str
    caption_size: str
    metric_size: str
    
    # Font weights
    title_weight: str
    subtitle_weight: str
    body_weight: str


@dataclass
class ThemeSpacing:
    """Spacing settings for a theme."""
    card_padding: str
    card_margin: str
    card_border_radius: str
    
    # Shadows
    card_shadow: str


@dataclass
class Theme:
    """Complete theme configuration."""
    name: str
    colors: ThemeColors
    typography: ThemeTypography
    spacing: ThemeSpacing
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary for easy access."""
        return {
            "name": self.name,
            "colors": self.colors.__dict__,
            "typography": self.typography.__dict__,
            "spacing": self.spacing.__dict__,
        }


# Default professional business theme
PROFESSIONAL_THEME = Theme(
    name="professional",
    colors=ThemeColors(
        background="#f9fafb",
        card_background="white",
        border="#e5e7eb",
        divider="#e5e7eb",
        text_primary="#111827",
        text_secondary="#374151",
        text_muted="#6b7280",
        chart_primary="#3b82f6",
        chart_grid="#f3f4f6",
        chart_axis="#e5e7eb",
        positive="#10b981",
        negative="#ef4444",
    ),
    typography=ThemeTypography(
        font_family="Arial, sans-serif",
        title_size="16px",
        subtitle_size="14px",
        body_size="13px",
        caption_size="12px",
        metric_size="32px",
        title_weight="600",
        subtitle_weight="600",
        body_weight="400",
    ),
    spacing=ThemeSpacing(
        card_padding="20px",
        card_margin="16px",
        card_border_radius="8px",
        card_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
    ),
)


# Dark theme for modern dashboards
DARK_THEME = Theme(
    name="dark",
    colors=ThemeColors(
        background="#0f172a",  # Dark slate background
        card_background="#1e293b",  # Slightly lighter card background
        border="#334155",  # Subtle border
        divider="#334155",
        text_primary="#f1f5f9",  # Light text
        text_secondary="#cbd5e1",  # Slightly muted light text
        text_muted="#94a3b8",  # Muted text
        chart_primary="#60a5fa",  # Bright blue for charts
        chart_grid="#334155",  # Subtle grid
        chart_axis="#475569",  # Axis lines
        positive="#34d399",  # Green for positive
        negative="#f87171",  # Red for negative
    ),
    typography=ThemeTypography(
        font_family="Arial, sans-serif",
        title_size="16px",
        subtitle_size="14px",
        body_size="13px",
        caption_size="12px",
        metric_size="32px",
        title_weight="600",
        subtitle_weight="600",
        body_weight="400",
    ),
    spacing=ThemeSpacing(
        card_padding="20px",
        card_margin="16px",
        card_border_radius="8px",
        card_shadow="0 4px 6px rgba(0, 0, 0, 0.3)",
    ),
)


# Ocean theme - blue/teal color scheme
OCEAN_THEME = Theme(
    name="ocean",
    colors=ThemeColors(
        background="#f0f9ff",  # Very light blue background
        card_background="#ffffff",  # White cards
        border="#bae6fd",  # Light blue border
        divider="#bae6fd",
        text_primary="#0c4a6e",  # Deep blue text
        text_secondary="#075985",  # Medium blue text
        text_muted="#0891b2",  # Cyan muted text
        chart_primary="#0ea5e9",  # Sky blue for charts
        chart_grid="#e0f2fe",  # Very light blue grid
        chart_axis="#bae6fd",  # Light blue axis
        positive="#14b8a6",  # Teal for positive
        negative="#f43f5e",  # Rose for negative
    ),
    typography=ThemeTypography(
        font_family="Arial, sans-serif",
        title_size="16px",
        subtitle_size="14px",
        body_size="13px",
        caption_size="12px",
        metric_size="32px",
        title_weight="600",
        subtitle_weight="600",
        body_weight="400",
    ),
    spacing=ThemeSpacing(
        card_padding="20px",
        card_margin="16px",
        card_border_radius="8px",
        card_shadow="0 1px 3px rgba(14, 165, 233, 0.1)",
    ),
)


# Registry of available themes
THEMES: Dict[str, Theme] = {
    "professional": PROFESSIONAL_THEME,
    "dark": DARK_THEME,
    "ocean": OCEAN_THEME,
}


def get_theme(name: str = "professional") -> Theme:
    """
    Get a theme by name.
    
    Args:
        name: Theme name (default: "professional")
        
    Returns:
        Theme configuration
        
    Raises:
        ValueError: If theme name is not found
    """
    if name not in THEMES:
        raise ValueError(f"Theme '{name}' not found. Available themes: {list(THEMES.keys())}")
    return THEMES[name]


def register_theme(theme: Theme) -> None:
    """
    Register a custom theme.
    
    Args:
        theme: Theme configuration to register
    """
    THEMES[theme.name] = theme
