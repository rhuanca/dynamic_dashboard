"""
Inventory Data Analyst Assistant - Main Application Entry Point

This is the main Streamlit application that orchestrates the chat interface
and dynamic dashboard rendering.

Run with: streamlit run app.py
"""

import streamlit as st
from ui_layout import render_main_layout


def main() -> None:
    """
    Main application entry point.
    
    Sets up Streamlit page configuration and renders the main layout.
    """
    # Configure Streamlit page
    st.set_page_config(
        page_title="Inventory Data Analyst Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom CSS for better styling
    st.markdown(
        """
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Improve chat input styling */
        .stTextInput > div > div > input {
            border-radius: 20px;
        }
        
        /* Improve button styling */
        .stButton > button {
            border-radius: 20px;
            height: 38px;
        }
        
        /* Reduce padding for better space usage */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Render the main UI layout
    render_main_layout()


if __name__ == "__main__":
    main()
