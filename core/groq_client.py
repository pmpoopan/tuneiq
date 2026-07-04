"""Groq client module for interacting with LLM models to manage profiles and music recommendations."""

import json
import os
import re
from typing import Any, Dict, List, Optional
import streamlit as st
from groq import Groq
from core.prompts import PROFILE_SYSTEM_PROMPT, DISCOVERY_SYSTEM_PROMPT, STEER_SYSTEM_PROMPT


def _clean_and_parse_json(text: str) -> Any:
    """Helper to strip markdown code block fences and parse JSON.

    If direct parsing fails, tries to extract the JSON string within curly braces or brackets.
    """
    text_stripped = text.strip()
    
    # Strip markdown code fences like ```json and ```
    if text_stripped.startswith("```"):
        newline_idx = text_stripped.find("\n")
        if newline_idx != -1:
            text_stripped = text_stripped[newline_idx:].strip()
        if text_stripped.endswith("```"):
            text_stripped = text_stripped[:-3].strip()
            
    try:
        return json.loads(text_stripped)
    except json.JSONDecodeError:
        # If it still fails, let's extract substring from first { or [ to last } or ]
        first_curly = text_stripped.find("{")
        first_bracket = text_stripped.find("[")
        
        start_idx = -1
        end_char = ""
        if first_curly != -1 and (first_bracket == -1 or first_curly < first_bracket):
            start_idx = first_curly
            end_char = "}"
        elif first_bracket != -1:
            start_idx = first_bracket
            end_char = "]"
            
        if start_idx != -1:
            end_idx = text_stripped.rfind(end_char)
            if end_idx != -1 and end_idx > start_idx:
                json_str = text_stripped[start_idx : end_idx + 1]
                return json.loads(json_str)
                
        raise


def call_groq(messages: list, system: str, max_tokens: int = 900, response_format: Optional[dict] = None) -> str:
    """Call the Groq LLM API with the provided messages and system prompt.

    Args:
        messages: A list of message dictionaries (role and content).
        system: The system prompt to guide the model.
        max_tokens: The maximum number of tokens to generate.
        response_format: Optional dictionary specifying response format (e.g. {"type": "json_object"}).

    Returns:
        The text response from the Groq API.

    Raises:
        ValueError: If the GROQ_API_KEY is not found.
        RuntimeError: If the API call fails.
    """
    api_key = None
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please configure it in Streamlit secrets or as an environment variable."
        )

    # Build the messages list
    full_messages = [{"role": "system", "content": system}] + messages

    try:
        client = Groq(api_key=api_key)
        kwargs = {
            "model": "llama-3.3-70b-versatile",
            "messages": full_messages,
            "max_tokens": max_tokens,
        }
        if response_format:
            kwargs["response_format"] = response_format
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(
            f"Failed to communicate with Groq LLM API: {str(e)}"
        ) from e


def generate_profile(artists: str, genres: str, tired_of: str) -> dict:
    """Generate a structured taste profile from user preferences.

    Args:
        artists: A string describing the artists the user loves.
        genres: A string describing the genres/moods the user gravitates toward.
        tired_of: A string describing what the user is tired of.

    Returns:
        A dictionary containing the taste profile.

    Raises:
        ValueError: If the API response cannot be parsed as JSON.
    """
    user_msg = (
        f"Artists I love right now: {artists}\n"
        f"Genres/moods I gravitate toward: {genres}\n"
        f"What I'm tired of: {tired_of}"
    )
    messages = [{"role": "user", "content": user_msg}]
    
    response_content = call_groq(messages, PROFILE_SYSTEM_PROMPT, response_format={"type": "json_object"})
    
    try:
        print("DEBUG RAW PROFILE RESPONSE:", repr(response_content))
        clean = response_content.replace("```json", "").replace("```", "").strip()
        if not clean.startswith("{"):
            clean = "{" + clean + "}"
        data = json.loads(clean)
        if not isinstance(data, dict):
            raise ValueError("Parsed JSON is not a dictionary.")
        return data
    except Exception as e:
        print("DEBUG PROFILE PARSE ERROR:", e)
        raise ValueError(f"Could not parse profile from AI response: {response_content[:200]}") from e


def generate_discovery(profile: dict) -> list:
    """Generate exactly 5 music recommendations based on a taste profile.

    Args:
        profile: The user taste profile dictionary.

    Returns:
        A list of exactly 5 recommendation dictionaries.

    Raises:
        ValueError: If parsing fails or the list length is not exactly 5.
    """
    user_msg = f"Taste profile: {json.dumps(profile)}"
    messages = [{"role": "user", "content": user_msg}]
    
    response_content = call_groq(messages, DISCOVERY_SYSTEM_PROMPT, max_tokens=800, response_format={"type": "json_object"})
    
    try:
        data = _clean_and_parse_json(response_content)
        if not isinstance(data, list) or len(data) != 5:
            raise ValueError("Parsed JSON must be a list containing exactly 5 items.")
        return data
    except Exception as e:
        raise ValueError("Could not parse discovery from AI response") from e


def steer_profile(user_message: str, profile: dict, chat_history: list) -> dict:
    """Conversational assistant to steer the user's profile and discovery recommendations.

    Args:
        user_message: The new message from the user.
        profile: The current user taste profile.
        chat_history: The list of prior messages in the chat session.

    Returns:
        A dictionary with the following keys:
            - reply: str (clean conversational reply only)
            - profile_updated: bool
            - new_profile: dict | None
            - new_picks: list | None
    """
    # Build messages list from chat_history + new user message appended (if not already the last message)
    if chat_history and chat_history[-1].get("role") == "user" and chat_history[-1].get("content") == user_message:
        new_messages = list(chat_history)
    else:
        new_messages = list(chat_history) + [{"role": "user", "content": user_message}]
    
    # Inject current profile into system prompt
    system_prompt = f"{STEER_SYSTEM_PROMPT}\n\nCurrent profile: {json.dumps(profile)}"
    
    response_content = call_groq(new_messages, system_prompt, max_tokens=1000)
    
    # Check if [PROFILE_UPDATED] is present
    profile_updated = "[PROFILE_UPDATED]" in response_content
    
    # Extract <PROFILE_JSON>...</PROFILE_JSON> block if present, parse as dict
    new_profile = None
    profile_match = re.search(r'<PROFILE_JSON>(.*?)</PROFILE_JSON>', response_content, re.DOTALL)
    if profile_match:
        try:
            new_profile = _clean_and_parse_json(profile_match.group(1))
        except Exception:
            pass
            
    # Extract <DISCO_JSON>...</DISCO_JSON> block if present, parse as list
    new_picks = None
    disco_match = re.search(r'<DISCO_JSON>(.*?)</DISCO_JSON>', response_content, re.DOTALL)
    if disco_match:
        try:
            new_picks = _clean_and_parse_json(disco_match.group(1))
        except Exception:
            pass
            
    # Extract conversational reply (strip [PROFILE_UPDATED] token and any JSON blocks)
    clean_reply = response_content
    clean_reply = re.sub(r'<PROFILE_JSON>.*?</PROFILE_JSON>', '', clean_reply, flags=re.DOTALL)
    clean_reply = re.sub(r'<DISCO_JSON>.*?</DISCO_JSON>', '', clean_reply, flags=re.DOTALL)
    clean_reply = clean_reply.replace("[PROFILE_UPDATED]", "")
    clean_reply = clean_reply.strip()
    
    return {
        "reply": clean_reply,
        "profile_updated": profile_updated,
        "new_profile": new_profile,
        "new_picks": new_picks
    }
