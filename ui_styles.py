"""
UI styling module for the Inventory Data Analyst Assistant.

This module contains HTML generation for UI components.
"""


def get_welcome_screen_html() -> str:
    """
    Generate HTML for the dashboard welcome screen.
    
    Returns:
        HTML string for the welcome screen with sample commands
    """
    return """
        <div style="
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border: 2px dashed #667eea40;
            border-radius: 16px;
            padding: 48px 32px;
            text-align: center;
            margin-top: 2rem;
        ">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin: 0 auto 16px;">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="#667eea" stroke-width="2"/>
                <line x1="3" y1="9" x2="21" y2="9" stroke="#667eea" stroke-width="2"/>
                <line x1="9" y1="9" x2="9" y2="21" stroke="#667eea" stroke-width="2"/>
            </svg>
            <h3 style="color: #374151; margin-bottom: 12px; border: none;">Your Dashboard Will Appear Here</h3>
            <p style="color: #6b7280; font-size: 14px; line-height: 1.6;">
                Start by asking a question in the chat, and I'll create visualizations for you.
            </p>
            <div style="
                background: white;
                border-radius: 12px;
                padding: 20px;
                margin-top: 24px;
                text-align: left;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <p style="font-weight: 600; color: #374151; margin-bottom: 12px; font-size: 14px;">
                    Try these commands:
                </p>
                <ul style="color: #6b7280; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;">
                    <li><code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">add us population</code> - Scorecard widget</li>
                    <li><code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">add sales chart</code> - Bar chart widget</li>
                    <li><code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">add sales trend</code> - Time series widget</li>
                    <li><code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px;">add products table</code> - Table widget</li>
                </ul>
            </div>
        </div>
    """
