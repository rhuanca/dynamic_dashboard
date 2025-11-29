"""
Equipment Inventory Assistant - Main Application Entry Point

This is the main Streamlit application that orchestrates the chat interface
and dynamic dashboard rendering.

Run with: streamlit run app.py
"""

import streamlit as st

from database.init import initialize_database
from ui_custom_styles import apply_custom_styling
from ui_layout import render_main_layout


def configure_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Equipment Inventory Assistant",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


def main() -> None:
    """
    Main application entry point.
    
    Orchestrates:
    1. Page configuration
    2. Database initialization
    3. Custom styling
    4. Main UI layout rendering
    """
    # Configure page
    configure_page()
    
    # Initialize database
    db_ready = initialize_database()
    
    if not db_ready:
        st.error("⚠️ Database not ready. Please check the error messages above.")
        st.stop()
    
    # Apply custom styling
    apply_custom_styling()
    
    # Render main UI
    render_main_layout()


if __name__ == "__main__":
    main()
