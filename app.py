from __future__ import annotations

from typing import Dict, List

import streamlit as st
import streamlit.components.v1 as components

from src.pipeline import run_pipeline
from src.soundcloud_client import is_soundcloud_configured


st.set_page_config(
    page_title="NeuroBeat",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed",
)


EXAMPLE_INPUTS: List[Dict[str, str]] = [
    {
        "label": "Stress relief",
        "text": "I feel drained after work and need something peaceful to slow down.",
        "time_of_day": "evening",
        "activity": "relaxing",
        "weather": "rainy",
    },
    {
        "label": "Focus mode",
        "text": "I need to concentrate deeply for coding and stay calm.",
        "time_of_day": "night",
        "activity": "working",
        "weather": "cool",
    },
    {
        "label": "Workout boost",
        "text": "I am pumped and need high-energy music for the gym.",
        "time_of_day": "morning",
        "activity": "workout",
        "weather": "sunny",
    },
]


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=DM+Sans:wght@400;500;700&display=swap');

        html, body, [class*="css"]  {
            font-family: "DM Sans", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 18%, rgba(248, 200, 120, 0.18), transparent 22%),
                radial-gradient(circle at 88% 14%, rgba(120, 168, 212, 0.16), transparent 20%),
                radial-gradient(circle at 82% 78%, rgba(154, 205, 176, 0.12), transparent 18%),
                linear-gradient(135deg, #f4efe6 0%, #edf4f8 42%, #f6f2ea 100%);
            color: #14213d;
        }

        .block-container {
            max-width: 1240px;
            padding-top: 0.9rem;
            padding-bottom: 2rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        .stDeployButton,
        #MainMenu,
        footer,
        [data-testid="stToolbar"] {
            display: none !important;
        }

        .stHeading a,
        .stMarkdown a[href^="#"],
        [data-testid="stHeaderActionElements"] {
            display: none !important;
        }

        h1, h2, h3 {
            font-family: "Space Grotesk", sans-serif;
            letter-spacing: -0.02em;
        }

        .section-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.65rem;
            line-height: 1.1;
            font-weight: 700;
            color: #1d3557;
            margin: 0 0 0.7rem 0;
        }

        .hero-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.88), rgba(255,247,237,0.94));
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 24px;
            padding: 1.6rem 1.8rem;
            box-shadow: 0 18px 45px rgba(20, 33, 61, 0.08);
            margin-bottom: 0.75rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .hero-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 22px 50px rgba(20, 33, 61, 0.11);
            border-color: rgba(29, 53, 87, 0.16);
        }

        .hero-title {
            font-size: 3rem;
            line-height: 1;
            margin: 0;
            color: #1d3557;
        }

        .hero-copy {
            margin-top: 1rem;
            font-size: 1rem;
            line-height: 1.7;
            color: #3d4f67;
            max-width: 900px;
            text-align: justify;
            text-justify: inter-word;
            margin-bottom: 0.9rem;
        }

        .hero-subcopy {
            max-width: 900px;
            color: #51647c;
            line-height: 1.72;
            text-align: justify;
            text-justify: inter-word;
            margin-bottom: 1rem;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 20px;
            padding: 1.1rem 1.15rem;
            box-shadow: 0 12px 32px rgba(20, 33, 61, 0.05);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .glass-panel:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 34px rgba(20, 33, 61, 0.08);
            border-color: rgba(29, 53, 87, 0.14);
        }

        .sidebar-card {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 20px;
            padding: 0.65rem 0.65rem 0.65rem 1.05rem;
            box-shadow: 0 12px 32px rgba(20, 33, 61, 0.05);
            min-height: 445px;
            display: flex;
            flex-direction: column;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .sidebar-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 38px rgba(20, 33, 61, 0.09);
            border-color: rgba(29, 53, 87, 0.14);
        }

        .side-copy {
            color: #4a5b72;
            line-height: 1.8;
            margin-bottom: 0.4rem;
            text-align: justify;
            text-justify: inter-word;
            font-size: 0.95rem;
        }

        .bullet-note {
            padding: 0.88rem 0.95rem;
            border-radius: 18px;
            background: #f8fafc;
            border: 1px solid rgba(20, 33, 61, 0.06);
            margin-bottom: 0.7rem;
            color: #334155;
            font-size: 0.95rem;
            line-height: 1.58;
            text-align: left;
            transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
        }

        .bullet-note:last-child {
            margin-bottom: 0;
        }

        .bullet-note:hover {
            transform: translateY(-1px);
            background: #ffffff;
            border-color: rgba(29, 53, 87, 0.14);
        }

        .status-pill {
            display: inline-block;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            background: #ecfdf3;
            color: #166534;
            font-size: 0.85rem;
            font-weight: 700;
            margin-right: 0.5rem;
            margin-top: 0.25rem;
        }

        .status-pill.alt {
            background: #edf4ff;
            color: #1d4ed8;
        }

        .metric-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 18px;
            padding: 1rem;
            min-height: 116px;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 28px rgba(20, 33, 61, 0.08);
            border-color: rgba(29, 53, 87, 0.14);
        }

        .metric-label {
            color: #6b7280;
            font-size: 0.85rem;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            color: #1d3557;
            font-size: 1.9rem;
            font-family: "Space Grotesk", sans-serif;
            font-weight: 700;
        }

        .track-card {
            display: flex;
            flex-direction: column;
            background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(250,250,248,0.96));
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 20px;
            padding: 1.15rem;
            box-shadow: 0 12px 24px rgba(20, 33, 61, 0.05);
            height: 335px;
            overflow: hidden;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .track-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 18px 34px rgba(20, 33, 61, 0.10);
            border-color: rgba(29, 53, 87, 0.16);
        }

        .example-card {
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 12px 24px rgba(20, 33, 61, 0.04);
            min-height: 180px;
            margin-bottom: 0.7rem;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .example-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 18px 32px rgba(20, 33, 61, 0.08);
            border-color: rgba(29, 53, 87, 0.15);
        }

        .example-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.1rem;
            font-weight: 700;
            color: #1d3557;
            margin-bottom: 0.55rem;
        }

        .example-copy {
            color: #66758a;
            line-height: 1.6;
            min-height: 78px;
            margin-bottom: 0;
            text-align: justify;
        }

        .quickstart-wrap {
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            height: 100%;
        }

        .quickstart-wrap .stButton > button {
            width: 100%;
            height: 3rem;
            border-radius: 14px;
            font-weight: 700;
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, border-color 0.18s ease;
        }

        .quickstart-wrap .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 18px rgba(20, 33, 61, 0.10);
        }

        .track-rank {
            width: 34px;
            height: 34px;
            line-height: 34px;
            text-align: center;
            border-radius: 50%;
            background: #1d3557;
            color: white;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .track-name {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #1d3557;
            margin-bottom: 0.2rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            line-height: 1.3;
            min-height: 2.8rem;
        }

        .track-meta {
            color: #6b7280;
            font-size: 0.92rem;
            margin-bottom: 0.7rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .chip {
            display: inline-block;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            padding: 0.28rem 0.55rem;
            border-radius: 999px;
            background: #f3f4f6;
            color: #334155;
            font-size: 0.78rem;
            font-weight: 700;
        }

        .reason {
            color: #445469;
            line-height: 1.55;
            font-size: 0.92rem;
            margin-top: 0.8rem;
            text-align: justify;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
            flex-grow: 1;
        }

        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.82);
            border: 1px solid rgba(20, 33, 61, 0.08);
            border-radius: 24px;
            padding: 1rem 1rem 0.9rem 1rem;
            box-shadow: 0 14px 34px rgba(20, 33, 61, 0.05);
            min-height: 445px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        div[data-testid="stForm"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 38px rgba(20, 33, 61, 0.08);
            border-color: rgba(29, 53, 87, 0.14);
        }

        div[data-testid="stForm"] button[kind="formSubmit"] {
            margin-top: 0.75rem;
            height: 3rem;
            border-radius: 14px;
            font-weight: 700;
            border: 1.5px solid rgba(29, 53, 87, 0.24) !important;
            transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, border-color 0.18s ease;
        }

        div[data-testid="stForm"] button[kind="formSubmit"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 18px rgba(20, 33, 61, 0.10);
            border-color: rgba(29, 53, 87, 0.4) !important;
        }

        div[data-baseweb="select"] > div,
        .stTextArea div[data-baseweb="textarea"] {
            border-radius: 14px !important;
        }

        .stTextArea label p {
            font-size: 1.55rem !important;
            font-weight: 700 !important;
            color: #1d3557 !important;
            line-height: 1.3 !important;
            margin-bottom: 0.2rem !important;
        }

        .stTextArea div[data-baseweb="textarea"] {
            border: 1.5px solid rgba(29, 53, 87, 0.22) !important;
            box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.4);
            transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
            background-color: transparent;
        }

        .stTextArea {
            margin-bottom: 0.5rem;
        }

        .stTextArea [data-testid="InputInstructions"] {
            display: none !important;
        }

        .stTextArea div[data-baseweb="textarea"]:hover {
            border-color: rgba(29, 53, 87, 0.36) !important;
            background: rgba(255, 255, 255, 0.98) !important;
        }

        .stTextArea div[data-baseweb="textarea"]:focus-within {
            border-color: #1d3557 !important;
            box-shadow: 0 0 0 3px rgba(29, 53, 87, 0.12) !important;
            background: #ffffff !important;
        }

        .stTextArea textarea {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }

        div[data-baseweb="select"] > div {
            border: 1.5px solid rgba(29, 53, 87, 0.15) !important;
            transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: rgba(29, 53, 87, 0.28) !important;
            transform: translateY(-1px);
        }

        .stCheckbox:hover {
            transform: translateY(-1px);
            transition: transform 0.18s ease;
        }

        .stCheckbox label {
            display: flex !important;
            align-items: flex-start !important;
            gap: 0.55rem !important;
        }

        .stCheckbox p {
            margin: 0 !important;
            line-height: 1.45 !important;
            white-space: normal !important;
            word-break: keep-all !important;
        }

        .top-grid {
            align-items: stretch;
        }

        .top-grid > div {
            display: flex;
            flex-direction: column;
        }

        .title-wrap {
            min-height: 3rem;
            display: flex;
            align-items: flex-end;
        }

        .right-panel-wrap {
            padding-left: 0.35rem;
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.15rem;
            }
            .block-container {
                padding-top: 0.75rem;
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
            .sidebar-card {
                min-height: auto;
            }
            .example-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _apply_example(example_index: int) -> None:
    example = EXAMPLE_INPUTS[example_index]
    st.session_state["input_text"] = example["text"]
    st.session_state["time_of_day"] = example["time_of_day"]
    st.session_state["activity"] = example["activity"]
    st.session_state["weather"] = example["weather"]
    st.session_state["auto_generate"] = True


def _init_state() -> None:
    st.session_state.setdefault("input_text", "")
    st.session_state.setdefault("time_of_day", "evening")
    st.session_state.setdefault("activity", "relaxing")
    st.session_state.setdefault("weather", "cloudy")
    st.session_state.setdefault("use_soundcloud", False)
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("auto_generate", False)
    st.session_state.setdefault("visible_tracks", 6)
    st.session_state.setdefault("languages", [])


def _render_header() -> None:
    soundcloud_ready = "SoundCloud ready" if is_soundcloud_configured() else "Local mode"
    model_mode = "Fast local inference"
    st.markdown(
        f"""
        <div class="hero-card">
            <h1 class="hero-title">NeuroBeat</h1>
            <p class="hero-copy">
                Describe how you feel, add your context, and get mood-aligned music recommendations instantly.
                The app fuses NLP-based emotion detection with time, activity, and weather signals to produce
                explainable recommendations that feel usable in the moment.
            </p>
            <span class="status-pill">{soundcloud_ready}</span>
            <span class="status-pill alt">{model_mode}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_examples() -> None:
    st.markdown('<div class="title-wrap"><div class="section-title">Quick starts</div></div>', unsafe_allow_html=True)
    cols = st.columns(len(EXAMPLE_INPUTS), gap="medium")
    for idx, col in enumerate(cols):
        example = EXAMPLE_INPUTS[idx]
        with col:
            st.markdown('<div class="quickstart-wrap">', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="example-card">
                    <div class="example-title">{example['label']}</div>
                    <div class="example-copy">{example['text']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.button(
                f"Use {example['label']}",
                key=f"example_{idx}",
                use_container_width=True,
                on_click=_apply_example,
                args=(idx,),
            )
            st.markdown("</div>", unsafe_allow_html=True)


def _render_controls() -> None:
    st.markdown(
        '<div class="title-wrap"><div class="section-title">Live recommendation console</div></div>',
        unsafe_allow_html=True,
    )
    with st.form("recommendation_form", clear_on_submit=False):
        st.text_area(
            "How are you feeling right now?",
            key="input_text",
            placeholder="Example: I feel mentally overloaded and need music that helps me recover.",
            height=150,
        )

        st.multiselect(
            "Preferred Languages (Optional)",
            options=["English", "Spanish", "French", "Korean", "Hindi", "Japanese", "Telugu", "Tamil", "German"],
            key="languages",
            help="Filter recommendations by language (including dubbed versions when available)."
        )

        st.markdown("<div style='margin-bottom: 0.00rem;'></div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.15])
        with col1:
            st.selectbox(
                "Time of day",
                ["morning", "afternoon", "evening", "night"],
                key="time_of_day",
            )
        with col2:
            st.selectbox(
                "Activity",
                ["studying", "working", "relaxing", "workout", "commuting", "sleeping"],
                key="activity",
            )
        with col3:
            st.selectbox(
                "Weather",
                ["sunny", "rainy", "cloudy", "cool"],
                key="weather",
            )
        with col4:
            st.checkbox(
                "Use SoundCloud if available",
                key="use_soundcloud",
                help="Falls back to the local catalog if SoundCloud credentials are not configured.",
            )

        submitted = st.form_submit_button("Generate Recommendations", use_container_width=True)

    should_run = submitted or st.session_state.get("auto_generate", False)
    if should_run:
        if st.session_state.get("auto_generate", False):
            st.session_state["auto_generate"] = False
            
        if not st.session_state["input_text"].strip():
            st.warning("Enter a short mood or situation so the app can infer your emotional state.")
        else:
            with st.spinner("Analyzing emotion and ranking tracks..."):
                st.session_state["result"] = run_pipeline(
                    text=st.session_state["input_text"],
                    time_of_day=st.session_state["time_of_day"],
                    activity=st.session_state["activity"],
                    weather=st.session_state["weather"],
                    languages=st.session_state.get("languages", []),
                    use_soundcloud=st.session_state["use_soundcloud"],
                )
                st.session_state["just_submitted"] = True
                st.session_state["visible_tracks"] = 6


def _render_live_panel() -> None:
    st.markdown(
        '<div class="right-panel-wrap"><div class="title-wrap"><div class="section-title">Real-time behavior</div></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="sidebar-card right-panel-wrap">
            <p class="side-copy">
                Watch how our NLP recommendation engine interprets your mood and applies contextual constraints in real-time below:
            </p>
            <div class="bullet-note"><strong>1.</strong> Detect emotion from free-form text.</div>
            <div class="bullet-note"><strong>2.</strong> Adjust the mood profile using time, activity, and weather.</div>
            <div class="bullet-note"><strong>3.</strong> Rank the strongest matching tracks and explain each choice.</div>
            <div class="bullet-note"><strong>4.</strong> Optionally switch to SoundCloud when credentials are configured.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metrics(result: Dict[str, object]) -> None:
    top_labels = ", ".join(item["label"].title() for item in result["top_emotions"][:2])
    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("Detected Emotion", result["emotion"].title()),
        ("Confidence", f"{result['confidence']:.2f}"),
        ("Top Signals", top_labels or "N/A"),
        ("Source", result["recommendation_source"].title()),
    ]

    for col, (label, value) in zip((col1, col2, col3, col4), cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_tracks(result: Dict[str, object]) -> None:
    st.markdown('<div class="title-wrap"><div class="section-title">Your live recommendations</div></div>', unsafe_allow_html=True)
    recommendations = result["recommendations"]
    
    visible_count = st.session_state.get("visible_tracks", 6)
    tracks_to_show = recommendations[:visible_count]
    
    columns = st.columns(2)

    for idx, track in enumerate(tracks_to_show):
        with columns[idx % 2]:
            chips = (
                f'<span class="chip">{str(track["genre"]).title()}</span>'
                f'<span class="chip">Score {track.get("score", 0):.2f}</span>'
                f'<span class="chip">Tempo {int(track.get("tempo", 0))}</span>'
            )
            soundcloud_link = ""
            if track.get("url"):
                soundcloud_link = f'<p><a href="{track["url"]}" target="_blank">Open in SoundCloud</a></p>'

            st.markdown(
                f"""
                <div class="track-card">
                    <div class="track-rank">{idx + 1}</div>
                    <div class="track-name">{track['track_name']}</div>
                    <div class="track-meta">by {track['artist']}</div>
                    <div>{chips}</div>
                    <div class="reason">{track['reason']}</div>
                    {soundcloud_link}
                </div>
                """,
                unsafe_allow_html=True,
            )
            
    if visible_count < len(recommendations):
        def _load_more():
            st.session_state["visible_tracks"] += 6
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Load More Tracks", on_click=_load_more, use_container_width=True)


def main() -> None:
    _init_state()
    _inject_styles()
    _render_header()

    left, right = st.columns([1.34, 0.66], gap="medium")
    with left:
        st.markdown('<div class="top-grid">', unsafe_allow_html=True)
        _render_controls()
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="top-grid">', unsafe_allow_html=True)
        _render_live_panel()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("")
    _render_examples()

    result = st.session_state.get("result")
    if result:
        st.markdown('<div id="recommendations-section"></div>', unsafe_allow_html=True)
        st.markdown("---")
        _render_metrics(result)
        st.markdown("")
        _render_tracks(result)
        st.markdown("")
        
        if st.session_state.get("just_submitted"):
            st.session_state["just_submitted"] = False
            import time
            # st.components.v1.html deprecated, using st.html for script execution if available
            try:
                st.html(
                    f"""
                    <script>
                        // Execution ID: {time.time()}
                        setTimeout(() => {{
                            const target = window.parent.document.getElementById("recommendations-section");
                            if (target) {{
                                target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                            }}
                        }}, 100);
                    </script>
                    """
                )
            except AttributeError:
                components.html(
                    f"""
                    <script>
                        // Execution ID: {time.time()}
                        setTimeout(() => {{
                            const target = window.parent.document.getElementById("recommendations-section");
                            if (target) {{
                                target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                            }}
                        }}, 100);
                    </script>
                    """,
                    height=0,
                )
    else:
        st.info("Submit a mood and context combination to see real-time emotion detection and recommendations.")


if __name__ == "__main__":
    main()
