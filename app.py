import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindPulse — Employee Well-being",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
[data-testid="stAppViewContainer"] { background:#0a0c12; color:#e2e8f0; }
[data-testid="stSidebar"]          { display:none; }
[data-testid="stHeader"]           { display:none; }
html, body, [class*="css"]         { font-family:'DM Sans',sans-serif; }

/* ── Welcome screen ── */
.welcome-wrap {
    text-align:center;
    padding: 48px 24px 40px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    min-height:100vh;
}
.welcome-logo {
    width:64px; height:64px; border-radius:20px;
    background:#1e2235; border:1px solid rgba(139,92,246,.35);
    display:inline-flex; align-items:center; justify-content:center;
    margin-bottom:24px;
}
.welcome-title {
    font-family:'DM Serif Display',serif;
    font-size:2.4rem; font-weight:400; color:#fff;
    margin-bottom:10px; line-height:1.2;
}
.welcome-title span { color:#818cf8; }
.welcome-sub {
    font-size:1rem; color:#94a3b8;
    max-width:440px; margin:0 auto 32px; line-height:1.7; text-align:center;
}
.pill-row {
    display:flex; justify-content:center; gap:10px; flex-wrap:wrap;
    margin-bottom:36px;
}
.pill {
    background:#1e2235; border:1px solid rgba(255,255,255,.1);
    border-radius:999px; padding:6px 14px;
    font-size:.8rem; color:#94a3b8;
}
.pill strong { color:#c4b5fd; }
.stat-strip {
    display:flex; justify-content:center; gap:32px; flex-wrap:wrap;
    margin-bottom:36px;
}
.stat-item { text-align:center; }
.stat-num  { font-size:1.6rem; font-weight:600; color:#818cf8; }
.stat-lbl  { font-size:.75rem; color:#64748b; margin-top:2px; }

/* ── Progress stepper ── */
.stepper {
    display:flex; align-items:center;
    padding:0 8px; margin-bottom:28px;
}
.step-node {
    width:30px; height:30px; border-radius:50%;
    border:2px solid #1e2235;
    display:flex; align-items:center; justify-content:center;
    font-size:.75rem; font-weight:600; color:#475569;
    background:#0a0c12; flex-shrink:0; position:relative; z-index:1;
    transition:all .3s;
}
.step-node.done  { background:#1e2235; border-color:#818cf8; color:#818cf8; }
.step-node.active{ background:#818cf8; border-color:#818cf8; color:#fff; }
.step-line {
    flex:1; height:2px; background:#1e2235; margin:0 4px;
    transition:background .3s;
}
.step-line.done { background:#818cf8; }
.step-meta {
    display:flex; justify-content:space-between;
    font-size:.72rem; color:#475569;
    padding:0 8px; margin-top:4px; margin-bottom:20px;
}
.step-meta span.cur  { color:#818cf8; font-weight:600; }
.step-meta span.done { color:#4ade80; }

/* ── Section header ── */
.sec-header {
    display:flex; align-items:center; gap:12px;
    margin-bottom:20px;
}
.sec-icon {
    width:38px; height:38px; border-radius:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.1rem; flex-shrink:0;
}
.sec-name  { font-size:1.1rem; font-weight:600; color:#e2e8f0; }
.sec-desc  { font-size:.8rem; color:#64748b; margin-top:1px; }

/* ── Field card ── */
.field-grid { display:grid; gap:10px; margin-bottom:10px; }

/* ── Slider live value ── */
.slider-header {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-bottom:2px;
}
.slider-lbl  { font-size:.85rem; font-weight:500; color:#d1d5db; }
.slider-val  { font-size:1.3rem; font-weight:600; color:#818cf8; }
.slider-tag  { font-size:.75rem; color:#64748b; margin-left:4px; }
.slider-endpoints {
    display:flex; justify-content:space-between;
    font-size:.72rem; color:#475569; margin-top:2px;
}

/* ── Inputs global style ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    color:#94a3b8 !important; font-size:.82rem !important; font-weight:500 !important;
}
div[data-baseweb="select"] {
    background:#111827 !important; border-color:rgba(255,255,255,.1) !important;
    border-radius:8px !important;
}
input[type="number"] {
    background:#111827 !important; color:#e2e8f0 !important;
    border-color:rgba(255,255,255,.1) !important; border-radius:8px !important;
}

/* ── Nav buttons ── */
div.stButton > button {
    font-family:'DM Sans',sans-serif;
    background:transparent; color:#e2e8f0;
    border:1px solid rgba(255,255,255,.15); border-radius:10px;
    padding:12px 28px; font-size:.95rem; font-weight:500;
    width:100%; transition:all .2s; cursor:pointer;
}
div.stButton > button:hover {
    background:rgba(129,140,248,.12); border-color:#818cf8; color:#818cf8;
}

/* ── CTA button ── */
.cta-btn-wrap { margin-top:8px; }
div.stButton > button.cta {
    background:#818cf8; border-color:#818cf8; color:#fff;
    font-weight:600; font-size:1rem; padding:14px;
    border-radius:12px;
}
div.stButton > button.cta:hover {
    background:#6366f1; border-color:#6366f1; color:#fff;
}

/* ── Cards ── */
.card {
    background:#111827; border:1px solid rgba(255,255,255,.08);
    border-radius:14px; padding:22px 24px; margin-bottom:14px;
}
.card-label {
    font-size:.7rem; font-weight:600; letter-spacing:.08em;
    text-transform:uppercase; color:#475569; margin-bottom:10px;
}

/* ── Result condition badge ── */
.condition-hero { text-align:center; padding:28px 20px 20px; }
.condition-icon { font-size:2.8rem; margin-bottom:12px; }
.condition-name {
    font-family:'DM Serif Display',serif;
    font-size:2rem; font-weight:400; margin-bottom:6px;
}
.condition-sub  { font-size:.9rem; color:#94a3b8; margin-bottom:16px; }
.badge {
    display:inline-block; padding:5px 20px; border-radius:999px;
    font-size:.82rem; font-weight:600; letter-spacing:.04em;
}

/* ── Confidence bar ── */
.prob-row    { margin-bottom:10px; }
.prob-head   { display:flex; justify-content:space-between; margin-bottom:4px; }
.prob-cls    { font-size:.82rem; color:#94a3b8; }
.prob-pct    { font-size:.82rem; font-weight:600; }
.prob-track  { background:rgba(255,255,255,.07); border-radius:4px; height:6px; }
.prob-fill   { height:6px; border-radius:4px; transition:width .8s ease; }

/* ── Metric pills ── */
.metric-strip { display:flex; gap:8px; flex-wrap:wrap; margin:14px 0; }
.metric-pill  {
    background:#1e2235; border:1px solid rgba(255,255,255,.08);
    border-radius:10px; padding:10px 14px; text-align:center; flex:1; min-width:90px;
}
.metric-pill .mv { font-size:1.2rem; font-weight:600; color:#c4b5fd; }
.metric-pill .ml { font-size:.7rem; color:#64748b; margin-top:2px; }

/* ── Risk factors ── */
.risk-item {
    display:flex; align-items:flex-start; gap:10px;
    background:#1e2235; border-radius:8px;
    padding:10px 14px; margin-bottom:8px;
}
.risk-dot { width:8px; height:8px; border-radius:50%; margin-top:4px; flex-shrink:0; }
.risk-txt  { font-size:.85rem; color:#94a3b8; line-height:1.6; }

/* ── Tip boxes ── */
.tip-item {
    display:flex; gap:10px; align-items:flex-start;
    padding:11px 14px; border-radius:8px; margin-bottom:8px;
    font-size:.85rem; line-height:1.6;
}
.tip-dot { width:6px; height:6px; border-radius:50%; margin-top:5px; flex-shrink:0; }

/* ── Warning box ── */
.warn-banner {
    border-radius:0 10px 10px 0; padding:12px 16px;
    font-size:.85rem; margin-bottom:12px; line-height:1.6;
}

/* ── Disclaimer ── */
.disclaimer {
    text-align:center; font-size:.75rem; color:#374151;
    margin-top:28px; padding-top:16px;
    border-top:1px solid rgba(255,255,255,.05);
}

/* ── Rerun link ── */
.rerun-wrap { text-align:center; margin-top:20px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# LOAD MODEL ARTIFACTS
# ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts():
    model         = joblib.load("mental_health_rf_model.pkl")
    le            = joblib.load("label_encoder.pkl")
    expected_cols = joblib.load("expected_columns.pkl")
    return model, le, expected_cols

try:
    model, le, EXPECTED_COLS = load_artifacts()
    ARTIFACTS_OK = True
except Exception as e:
    ARTIFACTS_OK = False
    ARTIFACT_ERR = str(e)


# ─────────────────────────────────────────────────────────────────
# SESSION STATE — tracks which screen we are on
# screen: "welcome" | "step1" | "step2" | "result"
# ─────────────────────────────────────────────────────────────────
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"

# Store answers across steps
for key, default in {
    "work_location": "Remote",
    "hours_worked": 40,
    "virtual_meetings": 5,
    "stress_level": "Medium",
    "productivity_change": "No Change",
    "satisfaction": "Neutral",
    "work_life_balance": 3,
    "company_support": 3,
    "physical_activity": "Daily",
    "sleep_quality": "Average",
    "access_resources": "Yes",
    "social_isolation": 3,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────────────────────────
# CONDITION META
# ─────────────────────────────────────────────────────────────────
CONDITION_META = {
    "Anxiety": {
        "icon": "😰",
        "color": "#fbbf24",
        "badge_style": "background:rgba(251,191,36,.15);color:#fbbf24;border:1px solid rgba(251,191,36,.4);",
        "label": "Anxiety Detected",
        "sub": "Your profile shows elevated anxiety indicators.",
        "warning": "Consider speaking with a counsellor if anxiety is affecting your daily life.",
        "warn_style": "background:rgba(251,191,36,.08);border-left:3px solid #fbbf24;color:#fde68a;",
        "tip_color": "#fbbf24",
        "tip_bg": "rgba(251,191,36,.06)",
        "tips": [
            "Try 10-minute breathing or mindfulness breaks during your workday.",
            "Set clear work hours and switch off notifications after hours.",
            "Break large projects into smaller, manageable daily wins.",
        ],
    },
    "Burnout": {
        "icon": "🔥",
        "color": "#ef4444",
        "badge_style": "background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.4);",
        "label": "Burnout Detected",
        "sub": "Your profile shows strong burnout indicators.",
        "warning": "Burnout is serious. Please speak to HR or a mental health professional.",
        "warn_style": "background:rgba(239,68,68,.08);border-left:3px solid #ef4444;color:#fca5a5;",
        "tip_color": "#ef4444",
        "tip_bg": "rgba(239,68,68,.06)",
        "tips": [
            "Take at least 1-2 days of complete disconnection from all work devices.",
            "Delegate tasks and communicate your workload limits to your manager.",
            "Review your weekly hours — sustained 45h+ is a key burnout driver.",
        ],
    },
    "Depression": {
        "icon": "🌧️",
        "color": "#818cf8",
        "badge_style": "background:rgba(129,140,248,.15);color:#818cf8;border:1px solid rgba(129,140,248,.4);",
        "label": "Depression Indicators",
        "sub": "Your profile shows signs worth taking seriously.",
        "warning": "Depression is treatable. Please reach out to a healthcare professional or crisis line.",
        "warn_style": "background:rgba(129,140,248,.08);border-left:3px solid #818cf8;color:#c4b5fd;",
        "tip_color": "#818cf8",
        "tip_bg": "rgba(129,140,248,.06)",
        "tips": [
            "Stay connected — schedule regular check-ins with colleagues or friends.",
            "Aim for 30 minutes of physical activity at least 3× per week.",
            "Maintain a consistent sleep schedule and reduce screen time before bed.",
        ],
    },
    "Healthy": {
        "icon": "✅",
        "color": "#34d399",
        "badge_style": "background:rgba(52,211,153,.15);color:#34d399;border:1px solid rgba(52,211,153,.4);",
        "label": "Healthy Profile",
        "sub": "Your profile shows a positive well-being balance.",
        "warning": None,
        "warn_style": "",
        "tip_color": "#34d399",
        "tip_bg": "rgba(52,211,153,.06)",
        "tips": [
            "Keep up your current work-life balance habits — they are working.",
            "Continue regular physical activity and good sleep hygiene.",
            "Stay connected socially and maintain open communication at work.",
        ],
    },
}

SLIDER_LABELS = {
    "work_life_balance": {1:"Very poor",2:"Poor",3:"Balanced",4:"Good",5:"Excellent"},
    "company_support":   {1:"None",2:"Minimal",3:"Moderate",4:"Good",5:"Excellent"},
    "social_isolation":  {1:"Very connected",2:"Connected",3:"Neutral",4:"Isolated",5:"Very isolated"},
}


# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def render_stepper(current_step):
    """current_step: 1 or 2"""
    nodes, lines = [], []
    for i in [1, 2]:
        if i < current_step:
            nodes.append(f'<div class="step-node done">✓</div>')
            if i < 2:
                lines.append('<div class="step-line done"></div>')
        elif i == current_step:
            nodes.append(f'<div class="step-node active">{i}</div>')
            if i < 2:
                lines.append('<div class="step-line"></div>')
        else:
            nodes.append(f'<div class="step-node">{i}</div>')
            if i < 2:
                lines.append('<div class="step-line"></div>')

    html = '<div class="stepper">'
    for j, node in enumerate(nodes):
        html += node
        if j < len(lines):
            html += lines[j]
    html += '</div>'

    labels = ['<div class="step-meta">']
    meta = [
        ("Work life", current_step > 1),
        ("Lifestyle", False),
    ]
    for name, done in meta:
        if done:
            labels.append(f'<span class="done">✓ {name}</span>')
        elif name == ("Work life" if current_step == 1 else "Lifestyle"):
            labels.append(f'<span class="cur">{name}</span>')
        else:
            labels.append(f'<span>{name}</span>')
    labels.append('</div>')

    st.markdown(html + "".join(labels), unsafe_allow_html=True)


def slider_with_label(label, key, min_val, max_val, labels_map, left_tip, right_tip):
    val = st.slider(label, min_value=min_val, max_value=max_val,
                    value=st.session_state[key], key=f"_sl_{key}",
                    label_visibility="collapsed")
    st.session_state[key] = val
    tag = labels_map.get(val, "")
    st.markdown(
        f'<div class="slider-header">'
        f'<span class="slider-lbl">{label}</span>'
        f'<span><span class="slider-val">{val}</span>'
        f'<span class="slider-tag">— {tag}</span></span>'
        f'</div>'
        f'<div class="slider-endpoints"><span>{left_tip}</span><span>{right_tip}</span></div>',
        unsafe_allow_html=True,
    )
    return val


def build_input_df(inputs):
    row = {
        "Hours_Worked_Per_Week":          inputs["hours_worked"],
        "Number_of_Virtual_Meetings":     inputs["virtual_meetings"],
        "Work_Life_Balance_Rating":       inputs["work_life_balance"],
        "Social_Isolation_Rating":        inputs["social_isolation"],
        "Company_Support_for_Remote_Work":inputs["company_support"],
        "Work_Location_Onsite":           int(inputs["work_location"] == "Onsite"),
        "Work_Location_Remote":           int(inputs["work_location"] == "Remote"),
        "Stress_Level_Low":               int(inputs["stress_level"] == "Low"),
        "Stress_Level_Medium":            int(inputs["stress_level"] == "Medium"),
        "Access_to_Mental_Health_Resources_Yes": int(inputs["access_resources"] == "Yes"),
        "Productivity_Change_Increase":   int(inputs["productivity_change"] == "Increase"),
        "Productivity_Change_No Change":  int(inputs["productivity_change"] == "No Change"),
        "Satisfaction_with_Remote_Work_Satisfied":  int(inputs["satisfaction"] == "Satisfied"),
        "Satisfaction_with_Remote_Work_Unsatisfied":int(inputs["satisfaction"] == "Unsatisfied"),
        "Physical_Activity_Unknown":      int(inputs["physical_activity"] == "Unknown"),
        "Physical_Activity_Weekly":       int(inputs["physical_activity"] == "Weekly"),
        "Sleep_Quality_Good":             int(inputs["sleep_quality"] == "Good"),
        "Sleep_Quality_Poor":             int(inputs["sleep_quality"] == "Poor"),
    }
    df = pd.DataFrame([row])
    for col in EXPECTED_COLS:
        if col not in df.columns:
            df[col] = 0
    return df[EXPECTED_COLS]


# ─────────────────────────────────────────────────────────────────
# SCREEN 0 — WELCOME
# ─────────────────────────────────────────────────────────────────
if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-logo">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <circle cx="14" cy="14" r="10" stroke="#818cf8" stroke-width="1.8"/>
                <path d="M9 14c0-2.8 2.2-5 5-5s5 2.2 5 5" stroke="#818cf8" stroke-width="1.8" stroke-linecap="round"/>
                <circle cx="14" cy="17" r="2" fill="#818cf8"/>
            </svg>
        </div>
        <div class="welcome-title">Mind<span>Pulse</span></div>
        <p class="welcome-sub">
            An AI-powered employee well-being screener. Answer 12 quick questions
            across 2 steps and get an instant mental health assessment with
            personalised HR recommendations.
        </p>
        <div class="pill-row">
            <div class="pill">2 steps &nbsp;·&nbsp; <strong>~2 minutes</strong></div>
            <div class="pill">Random Forest model &nbsp;·&nbsp; <strong>95%+ accuracy</strong></div>
            <div class="pill"><strong>4</strong> conditions detected</div>
            <div class="pill">Instant result</div>
        </div>
        <div class="stat-strip">
            <div class="stat-item"><div class="stat-num">5,000</div><div class="stat-lbl">employees in training data</div></div>
            <div class="stat-item"><div class="stat-num">95%+</div><div class="stat-lbl">F1-score (weighted)</div></div>
            <div class="stat-item"><div class="stat-num">&lt;8s</div><div class="stat-lbl">prediction time</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not ARTIFACTS_OK:
        st.error(f"Could not load model files: {ARTIFACT_ERR}")
        st.stop()

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button("Start my well-being check-in →", use_container_width=True):
            st.session_state.screen = "step1"
            st.rerun()

    st.markdown("""
    <p class="disclaimer">
        This tool is for research and awareness purposes only.<br>
        It is not a clinical diagnosis. Please consult a mental health professional for any medical concerns.
    </p>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SCREEN 1 — STEP 1: WORK LIFE
# ─────────────────────────────────────────────────────────────────
elif st.session_state.screen == "step1":
    render_stepper(1)

    st.markdown("""
    <div class="sec-header">
        <div class="sec-icon" style="background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.2);">
            <span style="font-size:18px;">💼</span>
        </div>
        <div>
            <div class="sec-name">Work life</div>
            <div class="sec-desc">Your schedule, stress, and remote work experience</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Row 1 — location, hours, meetings
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.work_location = st.selectbox(
            "Work location", ["Remote", "Onsite", "Hybrid"],
            index=["Remote","Onsite","Hybrid"].index(st.session_state.work_location))
    with c2:
        st.session_state.hours_worked = st.number_input(
            "Hours worked / week", min_value=0, max_value=168,
            value=st.session_state.hours_worked, step=1)
    with c3:
        st.session_state.virtual_meetings = st.number_input(
            "Virtual meetings / week", min_value=0, max_value=100,
            value=st.session_state.virtual_meetings, step=1)

    st.write("")

    # Row 2 — stress, productivity, satisfaction
    c4, c5, c6 = st.columns(3)
    with c4:
        st.session_state.stress_level = st.selectbox(
            "Stress level", ["Low", "Medium", "High"],
            index=["Low","Medium","High"].index(st.session_state.stress_level))
    with c5:
        st.session_state.productivity_change = st.selectbox(
            "Productivity change", ["Decrease", "No Change", "Increase"],
            index=["Decrease","No Change","Increase"].index(st.session_state.productivity_change))
    with c6:
        st.session_state.satisfaction = st.selectbox(
            "Remote work satisfaction", ["Unsatisfied", "Neutral", "Satisfied"],
            index=["Unsatisfied","Neutral","Satisfied"].index(st.session_state.satisfaction))

    st.write("")

    # Sliders with live value display
    sc1, sc2 = st.columns(2)
    with sc1:
        with st.container(border=True):
            slider_with_label(
                "Work-life balance", "work_life_balance",
                1, 5, SLIDER_LABELS["work_life_balance"],
                "Poor", "Excellent")
    with sc2:
        with st.container(border=True):
            slider_with_label(
                "Company support for remote work", "company_support",
                1, 5, SLIDER_LABELS["company_support"],
                "None", "Excellent")

    st.write("")

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.screen = "welcome"
            st.rerun()
    with col_next:
        if st.button("Continue to lifestyle →", use_container_width=True):
            st.session_state.screen = "step2"
            st.rerun()


# ─────────────────────────────────────────────────────────────────
# SCREEN 2 — STEP 2: LIFESTYLE
# ─────────────────────────────────────────────────────────────────
elif st.session_state.screen == "step2":
    render_stepper(2)

    st.markdown("""
    <div class="sec-header">
        <div class="sec-icon" style="background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.2);">
            <span style="font-size:18px;">🌿</span>
        </div>
        <div>
            <div class="sec-name">Lifestyle</div>
            <div class="sec-desc">Your physical activity, sleep, and social connection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Row — activity, sleep, resources
    c7, c8, c9 = st.columns(3)
    with c7:
        st.session_state.physical_activity = st.selectbox(
            "Physical activity", ["Daily", "Weekly", "Rarely", "Unknown"],
            index=["Daily","Weekly","Rarely","Unknown"].index(st.session_state.physical_activity))
    with c8:
        st.session_state.sleep_quality = st.selectbox(
            "Sleep quality", ["Poor", "Average", "Good"],
            index=["Poor","Average","Good"].index(st.session_state.sleep_quality))
    with c9:
        st.session_state.access_resources = st.selectbox(
            "Access to mental health resources", ["Yes", "No"],
            index=["Yes","No"].index(st.session_state.access_resources))

    st.write("")

    # Social isolation slider full width
    with st.container(border=True):
        slider_with_label(
            "Social isolation level", "social_isolation",
            1, 5, SLIDER_LABELS["social_isolation"],
            "Very connected", "Very isolated")

    st.write("")

    # Input summary preview before submitting
    with st.expander("Review your answers before submitting", expanded=False):
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Work location",  st.session_state.work_location)
        r2.metric("Hours / week",   st.session_state.hours_worked)
        r3.metric("Stress level",   st.session_state.stress_level)
        r4.metric("Sleep quality",  st.session_state.sleep_quality)

    st.write("")

    col_back, col_submit = st.columns([1, 2])
    with col_back:
        if st.button("← Back", use_container_width=True):
            st.session_state.screen = "step1"
            st.rerun()
    with col_submit:
        if st.button("Reveal my well-being result →", use_container_width=True):
            with st.spinner("Analysing your profile…"):
                time.sleep(4)
            st.session_state.screen = "result"
            st.rerun()


# ─────────────────────────────────────────────────────────────────
# SCREEN 3 — RESULTS
# ─────────────────────────────────────────────────────────────────
elif st.session_state.screen == "result":

    if not ARTIFACTS_OK:
        st.error(f"Model not loaded: {ARTIFACT_ERR}")
        st.stop()

    # ── Run prediction ──
    inputs = {k: st.session_state[k] for k in [
        "work_location","hours_worked","virtual_meetings",
        "stress_level","productivity_change","satisfaction",
        "work_life_balance","company_support",
        "physical_activity","sleep_quality","access_resources","social_isolation",
    ]}
    input_df    = build_input_df(inputs)
    proba       = model.predict_proba(input_df)[0]
    pred_idx    = int(np.argmax(proba))
    label       = le.inverse_transform([pred_idx])[0]
    confidence  = float(proba[pred_idx]) * 100
    meta        = CONDITION_META[label]

    # ── Condition hero card ──
    st.markdown(f"""
    <div class="card" style="text-align:center; padding:32px 24px 24px;">
        <div style="font-size:3rem; margin-bottom:12px;">{meta["icon"]}</div>
        <div style="font-family:'DM Serif Display',serif; font-size:2rem; color:{meta["color"]}; margin-bottom:6px;">
            {meta["label"]}
        </div>
        <div style="font-size:.9rem; color:#94a3b8; margin-bottom:18px;">{meta["sub"]}</div>
        <span class="badge" style="{meta["badge_style"]}">
            AI Confidence: {confidence:.1f}%
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Probability breakdown + Input summary ──
    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="card"><div class="card-label">Probability Breakdown</div>', unsafe_allow_html=True)
        for i, cls in enumerate(le.classes_):
            pct   = proba[i] * 100
            clr   = CONDITION_META[cls]["color"]
            bold  = "font-weight:600;" if cls == label else ""
            st.markdown(f"""
            <div class="prob-row">
                <div class="prob-head">
                    <span class="prob-cls" style="{bold}color:#e2e8f0 if cls==label else ''">{cls}</span>
                    <span class="prob-pct" style="color:{clr};">{pct:.1f}%</span>
                </div>
                <div class="prob-track">
                    <div class="prob-fill" style="width:{pct:.1f}%;background:{clr};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card"><div class="card-label">Your Key Inputs</div>', unsafe_allow_html=True)
        metrics = [
            (inputs["hours_worked"],      "Hrs / Week"),
            (inputs["virtual_meetings"],  "Meetings / Week"),
            (f"{inputs['work_life_balance']}/5", "Work-Life Balance"),
            (f"{inputs['social_isolation']}/5",  "Social Isolation"),
            (f"{inputs['company_support']}/5",   "Company Support"),
            (inputs["stress_level"],      "Stress Level"),
        ]
        for val, lbl in metrics:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        padding:7px 0;border-bottom:1px solid rgba(255,255,255,.05);">
                <span style="font-size:.82rem;color:#64748b;">{lbl}</span>
                <span style="font-size:.82rem;font-weight:600;color:#c4b5fd;">{val}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Risk factors ──
    risk_factors = []
    if inputs["hours_worked"] >= 45:
        risk_factors.append(("🔴", "#ef4444", f"High hours worked ({inputs['hours_worked']}h/week) — above 45h threshold"))
    if inputs["social_isolation"] >= 4:
        risk_factors.append(("🔴", "#ef4444", f"High social isolation ({inputs['social_isolation']}/5)"))
    if inputs["work_life_balance"] <= 2:
        risk_factors.append(("🟡", "#fbbf24", f"Low work-life balance ({inputs['work_life_balance']}/5)"))
    if inputs["stress_level"] == "High":
        risk_factors.append(("🔴", "#ef4444", "Stress level reported as High"))
    if inputs["sleep_quality"] == "Poor":
        risk_factors.append(("🟡", "#fbbf24", "Poor sleep quality reported"))
    if inputs["access_resources"] == "No":
        risk_factors.append(("🟡", "#fbbf24", "No access to mental health resources"))
    if inputs["social_isolation"] >= 3 and inputs["work_location"] == "Remote":
        risk_factors.append(("🟡", "#fbbf24", "Remote work combined with moderate-high isolation"))

    if risk_factors:
        st.markdown('<div class="card"><div class="card-label">Key Risk Factors Detected</div>', unsafe_allow_html=True)
        for icon, clr, txt in risk_factors:
            st.markdown(f"""
            <div class="risk-item">
                <div class="risk-dot" style="background:{clr};"></div>
                <div class="risk-txt">{txt}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Recommendations ──
    st.markdown('<div class="card"><div class="card-label">Personalised Recommendations</div>', unsafe_allow_html=True)

    if meta["warning"]:
        st.markdown(f"""
        <div class="warn-banner" style="{meta["warn_style"]}">
            ⚠️ {meta["warning"]}
        </div>""", unsafe_allow_html=True)

    for tip in meta["tips"]:
        st.markdown(f"""
        <div class="tip-item" style="background:{meta['tip_bg']};">
            <div class="tip-dot" style="background:{meta['tip_color']};"></div>
            <div style="color:#cbd5e1;">{tip}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Start over ──
    st.write("")
    col_l2, col_c2, col_r2 = st.columns([1, 2, 1])
    with col_c2:
        if st.button("← Run another assessment", use_container_width=True):
            st.session_state.screen = "welcome"
            st.rerun()

    st.markdown("""
    <p class="disclaimer">
        ⚠️ This prediction is generated by a machine learning model for research purposes only.<br>
        Please consult a qualified mental health professional for any clinical concerns.
    </p>
    """, unsafe_allow_html=True)
