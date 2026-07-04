"""Discovery panel component for displaying music recommendations."""

import streamlit as st
from core.groq_client import generate_discovery


def render_discovery_panel() -> None:
    """Render the right column: 5 discovery picks based on the current taste profile."""
    # Header
    st.markdown(
        "<div style='font-variant: small-caps; color: #888888; font-size: 14px; "
        "font-weight: bold; letter-spacing: 0.05em; margin-bottom: 2px;'>DISCOVERY BRIEF</div>",
        unsafe_allow_html=True
    )
    # Subtitle
    st.markdown(
        "<div style='font-size: 11px; color: #666666; margin-bottom: 10px;'>"
        "5 picks for your taste right now</div>",
        unsafe_allow_html=True
    )
    # Divider
    st.divider()

    # Empty State Check
    if not st.session_state.discovery_picks:
        st.info("Discovery picks appear here once your profile is ready.")
        return

    # Render each pick as a styled card using st.markdown
    for index, pick in enumerate(st.session_state.discovery_picks):
        artist = pick.get("artist", "")
        track = pick.get("track", "")
        why = pick.get("why", "")
        tag = pick.get("tag", "")

        st.markdown(f"""
        <div style="background:#181818; border:1px solid #2a2a2a; border-radius:8px; 
        padding:13px; margin-bottom:8px;">
          <div style="font-size:10px; color:#1DB954; font-family:monospace; margin-bottom:4px;">
            0{index + 1}
          </div>
          <div style="font-size:15px; font-weight:700; color:#FFFFFF; margin-bottom:2px;">
            {artist}
          </div>
          <div style="font-size:12px; color:#6a6a6a; font-style:italic; margin-bottom:8px;">
            {track}
          </div>
          <div style="font-size:12.5px; color:#B3B3B3; line-height:1.45; 
          border-top:1px solid #2a2a2a; padding-top:8px;">
            {why}
          </div>
          <div style="display:inline-block; font-size:9.5px; color:#6a6a6a; 
          background:#2a2a2a; border-radius:4px; padding:2px 7px; margin-top:6px; 
          font-family:monospace;">
            {tag}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Refresh Button
    if st.button("↻ Refresh picks", use_container_width=True):
        with st.spinner("Finding new picks…"):
            try:
                picks = generate_discovery(st.session_state.profile)
                st.session_state.discovery_picks = picks
                st.rerun()
            except Exception as e:
                st.error(str(e))
