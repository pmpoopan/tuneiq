"""Chat panel component for steering the user's taste profile."""

import streamlit as st
from core.groq_client import steer_profile


def render_chat_panel() -> None:
    """Render the center chat column for steering the taste profile."""
    # Header
    st.markdown(
        "<div style='font-variant: small-caps; color: #888888; font-size: 14px; "
        "font-weight: bold; letter-spacing: 0.05em; margin-bottom: 2px;'>TASTE STEERING</div>",
        unsafe_allow_html=True
    )
    # Subtitle
    st.markdown(
        "<div style='font-size: 11px; color: #666666; margin-bottom: 10px;'>"
        "Tell it what to change — it updates your profile and discovery picks</div>",
        unsafe_allow_html=True
    )
    # Divider
    st.divider()

    # Quick-steer chips
    chips = [
        "I'm in a different mood than usual",
        "Push me somewhere unexpected",
        "More lo-fi, less mainstream",
        "I want deeper cuts, not popular tracks",
        "Less of what I usually listen to",
        "Something new for tonight",
    ]

    # Use st.columns(3) to lay out 2 rows of 3 chips
    cols_row1 = st.columns(3)
    for i in range(3):
        with cols_row1[i]:
            if st.button(chips[i], use_container_width=True, key=f"chip_btn_{i}"):
                st.session_state.chip_input = chips[i]
                st.rerun()

    cols_row2 = st.columns(3)
    for i in range(3):
        with cols_row2[i]:
            if st.button(chips[i + 3], use_container_width=True, key=f"chip_btn_{i + 3}"):
                st.session_state.chip_input = chips[i + 3]
                st.rerun()

    st.write("")  # spacing

    # Chat message history
    # Render all messages in st.session_state.chat_history using st.chat_message()
    for message in st.session_state.chat_history:
        role = message.get("role", "assistant")
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message.get("content", ""))
        else:
            with st.chat_message("assistant", avatar="🎵"):
                st.markdown(message.get("content", ""))

    # Chat input parsing
    user_input = None
    # Check if st.session_state has "chip_input"
    if "chip_input" in st.session_state and st.session_state.chip_input:
        user_input = st.session_state.chip_input
        st.session_state.chip_input = None  # clear immediately

    chat_input_val = st.chat_input("e.g. I'm in a jazz phase right now…")
    if chat_input_val:
        user_input = chat_input_val

    # On user_input submit
    if user_input:
        # 1. Add user message to chat_history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # 2. Show st.spinner while updating
        with st.spinner("Updating your profile…"):
            try:
                # 3. Call steer_profile from core.groq_client
                result = steer_profile(
                    user_message=user_input,
                    profile=st.session_state.profile,
                    chat_history=st.session_state.chat_history
                )
                
                # 4. Add assistant reply to chat_history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result.get("reply", "")
                })
                
                # 5. If result.profile_updated is True:
                if result.get("profile_updated"):
                    st.session_state.profile = result.get("new_profile")
                    st.toast("✦ Taste profile updated", icon="🎵")
                    
                # 6. If result.new_picks is not None:
                if result.get("new_picks") is not None:
                    st.session_state.discovery_picks = result.get("new_picks")
                    
                # 7. Call st.rerun()
                st.rerun()
            except Exception as e:
                st.error(f"Error updating profile: {str(e)}")
