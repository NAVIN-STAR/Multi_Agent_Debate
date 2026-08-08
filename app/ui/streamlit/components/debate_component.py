import time
from typing import Generator
import streamlit as st

THINKING_DELAYS = {
    "optimist": 1.2,
    "critic": 1.2,
    "judge": 2.0,
}

SPEAKER_META = {
    "optimist": {
        "emoji": "🟢",
        "label": "Optimist",
        "color": "#10b981",
        "bg": "rgba(16, 185, 129, 0.08)",
    },
    "critic": {
        "emoji": "🔴",
        "label": "Critic",
        "color": "#ef4444",
        "bg": "rgba(239, 68, 68, 0.08)",
    },
    "judge": {
        "emoji": "⚖️",
        "label": "Judge",
        "color": "#f59e0b",
        "bg": "rgba(245, 158, 11, 0.08)",
    },
}


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        /* Modern Header Layout inside the container */
        .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 12px;
            margin-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        }

        .speaker-title {
            font-weight: 700;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .speaker-pill {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 3px 10px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: rgba(255, 255, 255, 0.8);
        }

        .verdict-header {
            color: #f59e0b;
            font-size: 1.2rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Target the Streamlit native border container to style it per speaker */
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px !important;
            margin-bottom: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_debate_event(event: dict) -> None:
    inject_custom_css()

    event_type = event["event_type"]
    speaker = event["speaker"]
    content = event.get("content", "")

    if event_type == "started":
        _render_started(speaker)
    elif event_type == "response":
        _render_response(speaker, content)
    elif event_type == "finished":
        _render_finished(speaker, content)


def _render_started(speaker: str) -> None:
    meta = SPEAKER_META.get(speaker, {"emoji": "💬", "label": speaker.title()})
    delay = THINKING_DELAYS.get(speaker, 1.2)

    with st.status(f"{meta['emoji']} {meta['label']} is thinking...", expanded=False) as status:
        time.sleep(delay)
        status.update(label=f"{meta['emoji']} {meta['label']} completed thinking.", state="complete")


def _stream_text(content: str, delay: float = 0.012) -> Generator[str, None, None]:
    words = content.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(delay)


def _render_response(speaker: str, content: str) -> None:
    meta = SPEAKER_META.get(speaker, {"emoji": "💬", "label": speaker.title()})

    # st.container(border=True) keeps everything enclosed together reliably
    with st.container(border=True):
        # Header with separator line
        st.markdown(
            f'<div class="card-header">'
            f'  <div class="speaker-title">{meta["emoji"]} {meta["label"]}</div>'
            f'  <span class="speaker-pill">{speaker.upper()}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Streamed body text directly inside the same container box
        st.write_stream(_stream_text(content))


def _render_finished(speaker: str, content: str) -> None:
    meta = SPEAKER_META.get(speaker, {"emoji": "⚖️", "label": "Judge"})

    with st.container(border=True):
        st.markdown(
            f'<div class="card-header">'
            f'  <div class="verdict-header">🏆 Final Verdict ({meta["label"]})</div>'
            f'  <span class="speaker-pill">DECISION</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.write_stream(_stream_text(content))