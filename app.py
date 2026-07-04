"""Main entry point for the TuneIQ Streamlit application."""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(override=True)

# Import of all components and utils
from components.onboarding import render_onboarding
from components.profile_panel import render_profile_panel
from components.chat_panel import render_chat_panel
from components.discovery_panel import render_discovery_panel
from utils.state import init_session_state, reset_state

# Page config (must be first Streamlit call)
st.set_page_config(
    page_title="TuneIQ",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global CSS injection
CSS_INJECTION = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #121212;
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
    height: 0;
}

div.stButton > button {
    background-color: #1DB954 !important;
    color: #000000 !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    border: none !important;
    transition: background-color 0.2s ease !important;
}

div.stButton > button:hover {
    background-color: #1ed760 !important;
    color: #000000 !important;
}

.stChatInput input {
    background-color: #181818 !important;
    border: 1.5px solid #2a2a2a !important;
    border-radius: 50px !important;
    color: white !important;
}

.stChatInput input:focus {
    border-color: #1DB954 !important;
}

.stSpinner {
    color: #1DB954 !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #2a2a2a;
    border-radius: 3px;
}
</style>
"""


def main() -> None:
    """Main application flow and layout."""
    # 1. Initialize session states
    init_session_state()

    # Apply global CSS injection
    st.markdown(CSS_INJECTION, unsafe_allow_html=True)

    # 2. Check onboarding status
    if not st.session_state.onboarding_done:
        render_onboarding()
        return

    # 3. Main app layout - Topbar
    topbar_html = """
    <div style="display:flex; justify-content:space-between; align-items:center; 
    padding:12px 24px; background:rgba(18,18,18,0.95); border-bottom:1px solid #2a2a2a;
    position:sticky; top:0; z-index:999; margin-bottom: 20px;">
      <span style="font-size:18px; font-weight:700; color:#1DB954;">🎵 TuneIQ</span>
      <span style="font-size:11px; color:#6a6a6a; font-family:monospace;">
        AI TASTE PROFILE MANAGER
      </span>
    </div>
    """
    st.markdown(topbar_html, unsafe_allow_html=True)

    # Columns layout
    left, center, right = st.columns([1, 1.8, 1])

    with left:
        render_profile_panel(st.session_state.profile)

    with center:
        render_chat_panel()

    with right:
        render_discovery_panel()


if __name__ == "__main__":
    main()
