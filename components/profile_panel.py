"""Profile panel component for displaying user taste profile cards."""

import streamlit as st


def render_profile_panel(profile: dict) -> None:
    """Render the user's current taste profile as styled cards in the left panel.

    Args:
        profile: The user taste profile dictionary.
    """
    # Section header
    st.markdown(
        "<div style='font-variant: small-caps; color: #888888; font-size: 14px; "
        "font-weight: bold; letter-spacing: 0.05em; margin-bottom: 2px;'>YOUR TASTE PROFILE</div>",
        unsafe_allow_html=True
    )
    # Subtitle
    st.markdown(
        "<div style='font-size: 10px; color: #666666; margin-bottom: 10px;'>"
        "Updates when you correct it in chat</div>",
        unsafe_allow_html=True
    )
    # Divider
    st.divider()

    # Profile cards mapping
    cards = [
        ("current_vibe", "Current Vibe"),
        ("core_artists", "Artist Signals"),
        ("genre_lean", "Genre & Mood"),
        ("avoid_zone", "Avoid Zone"),
        ("discovery_appetite", "Discovery Appetite"),
        ("open_to", "Open To"),
    ]

    for key, label in cards:
        value = profile.get(key, "")
        if value is None:
            value = ""
        else:
            value = str(value)

        # Discovery Appetite highlight coloring rules
        if key == "discovery_appetite":
            if value.startswith("High"):
                value = f"<span style='color:#1DB954; font-weight:bold;'>High</span>{value[4:]}"
            elif value.startswith("Medium"):
                value = f"<span style='color:#E8A33D; font-weight:bold;'>Medium</span>{value[6:]}"
            elif value.startswith("Low"):
                value = f"<span style='color:#B3B3B3; font-weight:bold;'>Low</span>{value[3:]}"

        # Card HTML template injection
        st.markdown(f"""
        <div style="background:#181818; border:1px solid #2a2a2a; border-radius:8px; 
        padding:12px 14px; margin-bottom:8px;">
          <div style="font-size:10px; color:#1DB954; letter-spacing:0.1em; 
          text-transform:uppercase; font-family:monospace; margin-bottom:4px;">
            {label}
          </div>
          <div style="font-size:13px; color:#e0e0e0; line-height:1.5;">
            {value}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Start over button
    if st.button("← Start over", use_container_width=True):
        from utils.state import reset_state
        reset_state()
