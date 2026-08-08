import streamlit as st

from app.ui.streamlit.api_client import DebateAPIClient
from app.ui.streamlit.components.debate_component import render_debate_event

st.set_page_config(
    page_title="Multi-Agent Debate",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .main .block-container {
        max-width: 850px;
        padding-top: 2rem;
    }

    /* Header */
    .debate-header {
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .debate-subtitle {
        text-align: center;
        color: #8a8f98;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.15);
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }

    /* Speaker cards */
    .speaker-card {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border: 1px solid rgba(128,128,128,0.15);
    }
    .speaker-card.optimist {
        background: rgba(46, 204, 113, 0.06);
        border-left: 4px solid #2ecc71;
    }
    .speaker-card.critic {
        background: rgba(231, 76, 60, 0.06);
        border-left: 4px solid #e74c3c;
    }
    .speaker-card.judge {
        background: rgba(241, 196, 15, 0.07);
        border-left: 4px solid #f1c40f;
    }
    .speaker-name {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.4rem;
    }

    .verdict-card {
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1.25rem 0;
        background: rgba(155, 89, 182, 0.08);
        border: 1px solid rgba(155, 89, 182, 0.3);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown('<h1 class="debate-header">⚔️ Multi-Agent Debate</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="debate-subtitle">Optimist vs. Critic, judged by AI</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Settings")
    topic = st.text_area(
        "Debate Topic",
        placeholder="Enter a topic to debate...",
        height=120,
    )

    max_rounds = st.slider(
        "Number of rounds",
        min_value=1,
        max_value=10,
        value=2,
        step=1,
    )

    st.divider()
    start_clicked = st.button("Start Debate 🚀", type="primary")

    st.divider()
    st.caption("🟢 Optimist  ·  🔴 Critic  ·  ⚖️ Judge")

if start_clicked:
    if not topic.strip():
        st.error("Please enter a debate topic.")
    else:
        client = DebateAPIClient(
            base_url="http://localhost:8000"
        )

        st.subheader(f"⚔️ {topic}")

        with st.container():
            for event in client.stream_debate(
                topic=topic,
                max_rounds=max_rounds,
            ):
                render_debate_event(event)
else:
    st.info("👈 Set a topic and hit **Start Debate** to begin.")