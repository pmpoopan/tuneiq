"""Session state management utilities."""

from typing import Dict, List, Any, Optional
import streamlit as st


def init_session_state() -> None:
    """Initialize all Streamlit session state keys with their default values.

    Session state keys:
        - profile: dict | None (default: None)
        - chat_history: list (default: [])
        - discovery_picks: list (default: [])
        - onboarding_done: bool (default: False)
        - is_loading: bool (default: False)
    """
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "discovery_picks" not in st.session_state:
        st.session_state.discovery_picks = []
    if "onboarding_done" not in st.session_state:
        st.session_state.onboarding_done = False
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False


def reset_state() -> None:
    """Clear and reset all Streamlit session state keys back to default values."""
    st.session_state.profile = None
    st.session_state.chat_history = []
    st.session_state.discovery_picks = []
    st.session_state.onboarding_done = False
    st.session_state.is_loading = False
    st.rerun()
