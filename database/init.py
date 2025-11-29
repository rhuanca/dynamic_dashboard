"""
Database initialization and configuration module.

Centralizes database initialization logic for the application.
"""

from typing import Optional
import streamlit as st

from database.db_manager import db_manager


def initialize_database() -> bool:
    """
    Initialize database on first application run.
    
    Checks if database exists and has data, initializes if needed.
    Uses Streamlit session state to track initialization status.
    
    Returns:
        bool: True if database is ready, False if initialization failed
    """
    if "db_initialized" in st.session_state:
        return True
    
    try:
        # Check if database exists and has data
        count = db_manager.get_equipment_count()
        
        if count == 0:
            # Database exists but is empty
            st.warning("Database is empty. Please run: python database/sample_data.py")
            st.session_state.db_initialized = False
            return False
        
        st.session_state.db_initialized = True
        return True
        
    except Exception as e:
        # Database doesn't exist, try to initialize it
        try:
            db_manager.initialize_database()
            st.session_state.db_initialized = True
            st.info("Database initialized successfully")
            return True
        except Exception as init_error:
            st.error(f"Failed to initialize database: {init_error}")
            st.session_state.db_initialized = False
            return False
