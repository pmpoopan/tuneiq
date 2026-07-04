"""Onboarding component for TuneIQ."""

import streamlit as st
from core.groq_client import generate_profile, generate_discovery


def render_onboarding() -> None:
    """Render the user onboarding wizard/interface."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Header area
        st.markdown(
            "<h1 style='color: #1DB954; text-align: center; margin-bottom: 0px;'>🎵 TuneIQ</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<h3 style='text-align: center; margin-top: 5px; margin-bottom: 15px;'>"
            "Your taste, made visible. And finally steerable.</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; font-size: 0.95em; color: #7f8c8d; margin-bottom: 25px;'>"
            "Answer three questions. TuneIQ builds a plain-language taste "
            "profile, then lets you correct it in your own words.</p>",
            unsafe_allow_html=True
        )
        
        # Form
        with st.form("onboarding_form"):
            q1 = st.text_area(
                label="Who are your top 3–5 artists right now?",
                placeholder="e.g. Arctic Monkeys, Cigarettes After Sex, Ruelle…",
                height=80
            )
            q2 = st.text_area(
                label="What genres or moods do you gravitate toward?",
                placeholder="e.g. indie, atmospheric, late-night driving music…",
                height=80
            )
            q3 = st.text_area(
                label="What are you currently tired of hearing?",
                placeholder="e.g. overplayed pop, the same 3 Drake songs…",
                height=80
            )
            
            submitted = st.form_submit_button("Build my taste profile →", use_container_width=True)
            
            if submitted:
                # Validate all 3 fields are non-empty
                if not q1.strip() or not q2.strip() or not q3.strip():
                    st.error("Please fill in all three fields.")
                else:
                    st.session_state.is_loading = True
                    
                    # Show st.spinner while is_loading is True
                    with st.spinner("Building your taste profile…"):
                        try:
                            # Call generate_profile from core.groq_client
                            profile = generate_profile(q1, q2, q3)
                            st.session_state.profile = profile
                            
                            # Call generate_discovery(profile) and store
                            picks = generate_discovery(profile)
                            st.session_state.discovery_picks = picks
                            
                            # Add first AI message to chat_history
                            ai_message = (
                                f"Got it. Here's what I understand about your taste right now:\n\n"
                                f"'{profile['profile_summary']}'\n\n"
                                "You can correct anything — just tell me in your own words."
                            )
                            st.session_state.chat_history.append({"role": "assistant", "content": ai_message})
                            
                            # Mark onboarding done and reset loading status
                            st.session_state.onboarding_done = True
                            st.session_state.is_loading = False
                            
                            # Call st.rerun() to load the main app
                            st.rerun()
                        except Exception as e:
                            st.session_state.is_loading = False
                            st.error(f"Error: {str(e)}")
