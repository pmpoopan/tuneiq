# 🎵 TuneIQ — AI-Native Music Taste Profile Manager


---

## What is TuneIQ?

TuneIQ is an AI-powered music discovery tool that solves a problem Spotify's recommendation engine hasn't fully cracked yet: **users can't see what the algorithm believes about their taste, and can't correct it in their own words.**

Traditional recommendation systems (collaborative filtering) optimize what songs get played — but they can't expose their internal state in human terms or accept open-ended natural language correction. TuneIQ puts an AI layer on top that does exactly that.

---

## The Problem It Solves

Spotify's most engaged users — people who follow artists, dislike tracks, and actively try to shape their recommendations — report that:

- There's no direct way to tell the algorithm what they want
- Feedback signals (like/dislike/follow) are slow, indirect, and unconfirmed
- The system never shows what it currently "believes" about their taste
- Repeated low-payoff attempts lead to disengagement and repetitive listening

**TuneIQ gives users two things they've never had: transparency and steerability.**

---

## Features

- **3-question onboarding** — favourite artists, genres/moods, what you're tired of
- **AI-generated Taste Profile** — plain-language trait cards (not just genre tags) built instantly from your answers
- **Conversational steering** — type anything ("I'm in a jazz phase," "less mainstream," "push me somewhere weird") and watch the profile update live
- **Quick-steer chips** — one-tap shortcuts for common corrections
- **Discovery Brief** — 5 real artist/track picks with specific "why this fits you" explanations, refreshed every time your profile changes

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Llama 3.3 70B via Groq API |
| Language | Python 3.10+ |
| Hosting | Streamlit Cloud |
| IDE | Antigravity |

---

## Project Structure

```
tuneiq/
├── app.py                  ← Streamlit entry point
├── requirements.txt
├── .env                    ← Local API key (gitignored)
├── .gitignore
│
├── core/
│   ├── groq_client.py      ← All Groq API calls
│   └── prompts.py          ← System prompts for profile, discovery, steering
│
├── components/
│   ├── onboarding.py       ← 3-question onboarding screen
│   ├── profile_panel.py    ← Left column: taste profile cards
│   ├── chat_panel.py       ← Center column: steering chat
│   └── discovery_panel.py  ← Right column: 5 discovery picks
│
└── utils/
    └── state.py            ← Session state management
```

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/pmpoopan/tuneiq
cd tuneiq
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API key**

Create a `.env` file in the root:
```
GROQ_API_KEY=gsk_your-key-here
```
Get your free key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
streamlit run app.py
```

---

## Deploying on Streamlit Cloud

1. Push repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select repo → branch: `main` → file: `app.py`
4. Under **Advanced settings → Secrets**, add:
```
GROQ_API_KEY = "gsk_your-key-here"
```
5. Click Deploy

---

## Why AI — Not Just a Better Algorithm

| Traditional Recommender | TuneIQ (AI Layer) |
|---|---|
| Optimizes song output silently | Shows users what it believes about their taste |
| Accepts only indirect signals (plays, skips, saves) | Accepts natural language correction ("stay niche, don't average me out") |
| Slow feedback loop (days to weeks) | Instant, confirmed profile updates |
| Black box — no explainability | Each discovery pick explains why it fits |

---

## Project Context

This MVP was built as Part 4 of a NextLeap PM Fellowship graduation project focused on Spotify's music discovery problem. The full project includes:

- **Part 1** — AI-powered review analysis engine (41 tagged excerpts across App Store, Spotify Community, Trustpilot, Product Hunt, and press)
- **Part 2** — 6 user interviews with Active Tuner segment validation
- **Part 3** — Problem definition: root cause, target segment, business case
- **Part 4** — This MVP (TuneIQ), deployed to production

---

## Note on Data

TuneIQ currently simulates the taste profile from user-provided onboarding answers. In a production build, this would be seeded directly from real Spotify listening history via the Spotify Web API, with the same AI reasoning layer on top.

---

