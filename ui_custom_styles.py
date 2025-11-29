"""
UI Styling Module

Centralizes all custom CSS styling for the Streamlit application.
Separates presentation concerns from application logic.
"""


def get_custom_css() -> str:
    """
    Get custom CSS styles for the application.
    
    Returns:
        str: CSS styles as a string
    """
    return """
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
    """


def apply_custom_styling() -> None:
    """Apply custom CSS styling to the Streamlit app."""
    import streamlit as st
    st.markdown(get_custom_css(), unsafe_allow_html=True)
