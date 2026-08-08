import time

import streamlit as st

THINKING_DELAYS = {
    "optimist": 1.5,
    "critic": 1.5,
    "judge": 2.5,
}

SPEAKER_META = {
    "optimist": {"emoji": "🟢", "label": "Optimist"},
    "critic": {"emoji": "🔴", "label": "Critic"},
    "judge": {"emoji": "⚖️", "label": "Judge"},
}


def render_debate_event(event: dict) -> None:
    event_type = event["event_type"]
    speaker = event["speaker"]
    content = event["content"]

    if event_type == "started":
        _render_started(speaker)

    elif event_type == "response":
        _render_response(speaker, content)

    elif event_type == "finished":
        _render_finished(speaker, content)


def _render_started(speaker: str) -> None:
    messages = {
        "optimist": "🟢 Optimist is thinking...",
        "critic": "🔴 Critic is thinking...",
        "judge": "⚖️ Judge is evaluating the debate...",
    }

    delay = THINKING_DELAYS.get(speaker, 1.5)

    with st.spinner(messages.get(speaker, "Thinking...")):
        time.sleep(delay)


def _type_text(placeholder, content: str, delay: float = 0.01) -> None:
    displayed_text = ""

    for character in content:
        displayed_text += character
        placeholder.markdown(displayed_text + "▌")
        time.sleep(delay)

    placeholder.markdown(displayed_text)


def _render_response(speaker: str, content: str) -> None:
    meta = SPEAKER_META.get(speaker, {"emoji": "💬", "label": speaker.title()})

    st.markdown(
        f'<div class="speaker-card {speaker}">'
        f'<div class="speaker-name">{meta["emoji"]} {meta["label"]}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    placeholder = st.empty()

    _type_text(
        placeholder,
        content,
        delay=0.005,
    )


def _render_finished(speaker: str, content: str) -> None:
    meta = SPEAKER_META.get(
        speaker,
        {"emoji": "💬", "label": speaker.title()},
    )

    st.markdown(
        f'<div class="speaker-card {speaker}">'
        f'<div class="speaker-name">'
        f'{meta["emoji"]} {meta["label"]}'
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### 🏆 Final Verdict")

    placeholder = st.empty()

    _type_text(
        placeholder,
        content,
        delay=0.005,
    )