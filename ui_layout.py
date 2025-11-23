"""
UI Layout module for the Inventory Data Analyst Assistant.

This module orchestrates the main UI components with clean separation of concerns.
Handles session state, chat interface, dashboard rendering, and overall page layout.
"""

import streamlit as st

from chat_handler import process_user_message
from dashboard_renderer import render_dashboard_widgets
from ui_styles import get_welcome_screen_html


# Constants
INITIAL_WELCOME_MESSAGE = (
    "Hello! I'm your Inventory Data Analyst Assistant. "
    "Try commands like 'add us population', 'add sales chart', "
    "'add sales trend', or 'add products table' to see different visualizations."
)


def initialize_session_state() -> None:
    """
    Initialize session state variables on first run.
    
    Sets up:
    - messages: Chat message history with initial welcome message
    - current_dashboard: Dashboard specification (None initially)
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": INITIAL_WELCOME_MESSAGE
            }
        ]
    
    if "current_dashboard" not in st.session_state:
        st.session_state.current_dashboard = None


def render_chat_interface() -> None:
    """
    Render the chat interface with message history and input.
    
    Uses Streamlit's native chat components for better UX:
    - st.container(height=500): Fixed-height scrollable message area
    - st.chat_message(): Native chat message bubbles with avatars
    - st.chat_input(): Sticky input at bottom with auto-submit
    
    Automatically scrolls to latest message and handles message submission.
    """
    # Use a container with fixed height for the chat history
    chat_container = st.container(height=500)
    
    with chat_container:
        # Display all messages using Streamlit's native chat components
        for message in st.session_state.messages:
            with st.chat_message(
                name="assistant" if message["role"] == "assistant" else "user",
                avatar="🤖" if message["role"] == "assistant" else "👤"
            ):
                st.write(message["content"])
    
    # Use Streamlit's native chat input (always at bottom, outside container)
    if user_input := st.chat_input("Ask me about your inventory data..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Process message and get response
        response = process_user_message(user_input)
        
        # Add assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.rerun()


def render_dashboard_area() -> None:
    """
    Render the dashboard area with widgets or welcome screen.
    
    Displays:
    - Welcome screen with sample commands if no dashboard exists
    - Dashboard widgets organized by type if dashboard is created
    """
    if st.session_state.current_dashboard is None:
        # Show welcome screen
        welcome_html = get_welcome_screen_html()
        st.markdown(welcome_html, unsafe_allow_html=True)
    else:
        # Render dashboard widgets
        render_dashboard_widgets(st.session_state.current_dashboard)


def render_main_layout() -> None:
    """Main orchestration function for the UI layout."""
    # Initialize session state
    initialize_session_state()
    
    # Inject enhanced global styles
    st.markdown(
        """
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* Global styling */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main container */
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }
        
        /* Page background */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Column styling */
        [data-testid="column"] {
            background: white;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Section headers */
        h3 {
            font-weight: 600;
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 0.75rem;
            margin-top: 0;
            padding-bottom: 0.5rem;
            border-bottom: none;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Chat container adjustments */
        [data-testid="stVerticalBlock"] > [style*="height: 500px"] {
            border-radius: 6px;
            border: 1px solid #e5e7eb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Minimal clean business header
    st.markdown(
        """
        <div style="
            background: white;
            padding: 12px 0;
            border-bottom: 2px solid #f1f5f9;
            margin-bottom: 1.25rem;
        ">
            <span style="
                color: #1f2937;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: -0.01em;
            ">Inventory Data Analyst Assistant</span>
            <span style="
                color: #cbd5e0;
                font-size: 14px;
                margin: 0 10px;
            ">|</span>
            <span style="
                color: #64748b;
                font-size: 11px;
            ">Ask questions in natural language</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create two-column layout with better proportions
    col1, col2 = st.columns([4.5, 7.5], gap="large")
    
    with col1:
        st.markdown("### Chat")
        render_chat_interface()
    
    with col2:
        st.markdown("### Dashboard")
        render_dashboard_area()
