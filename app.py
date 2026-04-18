import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,60,180,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(30,180,140,0.10) 0%, transparent 60%),
        #0a0a0f;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; margin: auto; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7c5cbf;
    border: 1px solid #7c5cbf44;
    padding: 0.3rem 0.9rem;
    border-radius: 2px;
    margin-bottom: 1.4rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #e8e6f0 30%, #9b78e8 70%, #1ec4a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero p {
    font-size: 0.92rem;
    color: #7a7890;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
    letter-spacing: 0.01em;
}

/* ── Input area ── */
.input-wrapper {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 1.8rem 2rem;
    margin: 2rem 0;
    position: relative;
    transition: border-color 0.3s;
}
.input-wrapper:hover { border-color: rgba(124,92,191,0.4); }
.input-label {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c5cbf;
    margin-bottom: 0.6rem;
    font-family: 'DM Mono', monospace;
}

[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 0 !important;
    color: #e8e6f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.5rem 0 !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextInput"] input:focus {
    border-bottom-color: #7c5cbf !important;
    box-shadow: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3d3b52 !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6c3fbf, #1ec4a0) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.7rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 2rem 0 1.5rem;
}
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 5px;
    padding: 1rem;
    text-align: center;
    transition: all 0.35s;
}
.step-card.active {
    border-color: #7c5cbf;
    background: rgba(124,92,191,0.12);
    box-shadow: 0 0 20px rgba(124,92,191,0.15);
}
.step-card.done {
    border-color: #1ec4a0;
    background: rgba(30,196,160,0.07);
}
.step-icon { font-size: 1.4rem; margin-bottom: 0.4rem; }
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7a7890;
}
.step-card.active .step-title { color: #b49aef; }
.step-card.done .step-title  { color: #1ec4a0; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #7c5cbf;
    border-radius: 0 5px 5px 0;
    padding: 1.4rem 1.6rem;
    margin: 1rem 0;
}
.result-panel.teal  { border-left-color: #1ec4a0; }
.result-panel.amber { border-left-color: #e0a23a; }

.panel-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-header.purple { color: #9b78e8; }
.panel-header.teal   { color: #1ec4a0; }
.panel-header.amber  { color: #e0a23a; }

.panel-body {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #c4c0d8;
    white-space: pre-wrap;
    word-break: break-word;
}
.panel-body h1, .panel-body h2, .panel-body h3 {
    font-family: 'Syne', sans-serif;
    color: #e8e6f0;
    font-weight: 700;
    margin: 1.2rem 0 0.4rem;
}
.panel-body h1 { font-size: 1.3rem; border-bottom: 1px solid rgba(124,92,191,0.3); padding-bottom: 0.3rem; }
.panel-body h2 { font-size: 1.1rem; color: #b49aef; }
.panel-body h3 { font-size: 0.95rem; color: #1ec4a0; }

/* ── Score badge ── */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6c3fbf, #1ec4a0);
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    padding: 0.35rem 1rem;
    border-radius: 3px;
    margin-bottom: 0.8rem;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.fancy-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0;
    color: #2e2c3d;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.fancy-divider::before,
.fancy-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2e2c3d, transparent);
}

/* ── Error box ── */
.error-box {
    background: rgba(220,60,60,0.08);
    border: 1px solid rgba(220,60,60,0.3);
    border-radius: 5px;
    padding: 1rem 1.4rem;
    color: #f08080;
    font-size: 0.88rem;
    margin: 1rem 0;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] > div {
    border-top-color: #7c5cbf !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "current_step" not in st.session_state:
    st.session_state.current_step = 0


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">Multi-Agent Research System</div>
    <h1>ResearchMind AI</h1>
    <p>Four specialized agents working in sequence — searching, reading, writing, and critiquing — to produce publication-ready research reports.</p>
</div>
""", unsafe_allow_html=True)


# ── Pipeline step indicators ──────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search"),
    ("📄", "Read"),
    ("✍️", "Write"),
    ("🔎", "Critique"),
]

def render_steps(current=0, done_up_to=0):
    cards = ""
    for i, (icon, title) in enumerate(STEPS):
        if i < done_up_to:
            cls = "step-card done"
        elif i == current:
            cls = "step-card active"
        else:
            cls = "step-card"
        cards += f"""
        <div class="{cls}">
            <div class="step-icon">{icon}</div>
            <div class="step-title">{title}</div>
        </div>"""
    st.markdown(f'<div class="step-grid">{cards}</div>', unsafe_allow_html=True)

render_steps(current=st.session_state.current_step,
             done_up_to=4 if st.session_state.results else 0)


# ── Input area ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="input-label">Research Topic</div>', unsafe_allow_html=True)
topic = st.text_input(
    label="topic",
    placeholder="e.g. impact of war on global stock markets",
    key="topic_input",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

run_btn = st.button("⚡ Run Research Pipeline", disabled=st.session_state.running)


# ── Pipeline execution ────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.results = None
    st.session_state.running = True

    try:
        # Step 1
        st.session_state.current_step = 0
        with st.spinner("🔍  Search agent scanning the web…"):
            # We run the full pipeline (it's synchronous) but show progress via placeholders
            pass

        progress_placeholder = st.empty()

        step_messages = [
            "🔍  Search agent scanning the web…",
            "📄  Reader agent scraping top sources…",
            "✍️   Writer agent drafting your report…",
            "🔎  Critic agent reviewing quality…",
        ]

        for i, msg in enumerate(step_messages):
            st.session_state.current_step = i
            progress_placeholder.markdown(f"""
            <div class="result-panel">
                <div class="panel-header purple">⚙ Pipeline — Step {i+1} of 4</div>
                <div class="panel-body">{msg}</div>
            </div>""", unsafe_allow_html=True)
            if i < len(step_messages) - 1:
                time.sleep(0.4)   # brief visual pause before real work starts

        # Run actual pipeline
        with st.spinner("Running agents — this may take a minute…"):
            results = run_research_pipeline(topic.strip())

        progress_placeholder.empty()
        st.session_state.results = results
        st.session_state.current_step = 4

    except Exception as e:
        st.session_state.running = False
        st.markdown(f'<div class="error-box">⚠ Pipeline error: {e}</div>',
                    unsafe_allow_html=True)
        st.stop()

    st.session_state.running = False
    st.rerun()

elif run_btn and not topic.strip():
    st.markdown('<div class="error-box">Please enter a research topic before running.</div>',
                unsafe_allow_html=True)


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    st.markdown('<div class="fancy-divider">Results</div>', unsafe_allow_html=True)

    # ── Tabs ──
    tab1, tab2, tab3 = st.tabs(["📋 Full Report", "🔍 Raw Research", "🔎 Critic Feedback"])

# Tab 1 — Report 
with tab1:
    st.markdown(f"""
    <div class="result-panel teal">
        <div class="panel-header teal">✍ Final Research Report</div>
    </div>""", unsafe_allow_html=True)

    # ✅ Use st.markdown so ## headings render as real bold headings
    st.markdown(r.get("report", "No report generated."))

    st.download_button(
        label="⬇ Download Report (.txt)",
        data=r.get("report", ""),
        file_name=f"research_report_{topic[:30].replace(' ','_')}.txt",
        mime="text/plain"
    )

    # Tab 2 — Raw research
    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-panel">
                <div class="panel-header purple">🔍 Search Results</div>
                <div class="panel-body">{r.get("search_results","—").replace(chr(10), "<br>")}</div>

            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="result-panel">
                <div class="panel-header purple">📄 Scraped Content</div>
                <div class="panel-body">{r.get("search_results","—").replace(chr(10), "<br>")}</div>

            </div>""", unsafe_allow_html=True)

    # Tab 3 — Critic
    with tab3:
        feedback = r.get("feedback", "No feedback generated.")

        # Try to extract score for badge
        score_text = ""
        for line in feedback.splitlines():
            if line.strip().lower().startswith("score"):
                score_text = line.split(":", 1)[-1].strip()
                break

        if score_text:
            st.markdown(f'<div class="score-badge">Score: {score_text}</div>',
                        unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-panel amber">
            <div class="panel-header amber">🔎 Critic Analysis</div>
            <div class="panel-body">{feedback.replace(chr(10), "<br>")}</div>
        </div>""", unsafe_allow_html=True)

    # ── Run again ──
    st.markdown('<div class="fancy-divider">New Research</div>', unsafe_allow_html=True)
    if st.button("🔄 Run Another Topic"):
        st.session_state.results = None
        st.session_state.current_step = 0
        st.rerun()