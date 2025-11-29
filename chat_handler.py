"""
Chat Message Processing Module

Integrates the LangGraph multi-agent system with the Streamlit chat interface.
Handles message processing and dashboard state management.
"""

from typing import List

import streamlit as st

from core.specs import DashboardSpec, WidgetSpec
from agents.orchestrator import orchestrator


def initialize_session_state() -> None:
    """Initialize session state for widgets if not already present."""
    if "widgets" not in st.session_state:
        st.session_state.widgets = []


def update_dashboard(widgets: List[WidgetSpec]) -> None:
    """
    Update the dashboard with new widgets.
    
    Args:
        widgets: List of widget specifications to add to dashboard
    """
    if not widgets:
        return
    
    st.session_state.widgets.extend(widgets)
    st.session_state.current_dashboard = DashboardSpec(
        dashboard_id="equipment_dashboard",
        title="Equipment Inventory Dashboard",
        widgets=st.session_state.widgets
    )


def process_user_message(user_input: str) -> str:
    """
    Process user message using multi-agent system.
    
    Routes the query through NLU → Database → Response Generator agents
    and updates the dashboard with generated widgets.
    
    Args:
        user_input: User's message text
        
    Returns:
        str: Assistant's response message
    """
    # Ensure session state is initialized
    initialize_session_state()
    
    try:
        # Process query through multi-agent workflow
        result = orchestrator.process_query(user_input)
        
        # Extract results
        new_widgets = result.get("widgets", [])
        message = result.get("message", "✓ Query processed")
        success = result.get("success", True)
        
        # Update dashboard if we have new widgets
        if new_widgets:
            update_dashboard(new_widgets)
        
        return message
        
    except Exception as e:
        return f"❌ Error processing query: {str(e)}"
