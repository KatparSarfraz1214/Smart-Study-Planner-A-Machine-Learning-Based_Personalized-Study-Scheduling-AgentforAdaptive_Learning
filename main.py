# ============================================================
#  Smart Study Planner — app/main.py
#  Streamlit app ka entry point — navigation yahan hai
# ============================================================

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Page config (sabse pehle hona chahiye) ──
st.set_page_config(
    page_title  = "StudyAI — Smart Study Planner",
    page_icon   = "🎓",
    layout      = "wide",
    initial_sidebar_state = "expanded",
)

# ── Custom CSS — Modern Professional Theme ──
st.markdown("""
<style>

/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f0f2f8;
}

/* Hide Streamlit default UI */
#MainMenu, footer, header { visibility: hidden; }

/* ── Fix all form labels — black text, no dark background ── */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stSlider label,
.stForm label,
div[data-testid="stFormSubmitButton"] label,
p, span, label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #111827 !important;
    background: transparent !important;
    font-weight: 500 !important;
}

/* Fix selectbox dropdown text */
[data-baseweb="select"] span,
[data-baseweb="select"] div,
[data-baseweb="menu"] li {
    color: #111827 !important;
    background-color: #ffffff !important;
}

/* Fix number input text */
.stNumberInput input,
.stTextInput input {
    color: #111827 !important;
    background: #ffffff !important;
}

/* Fix slider label and value */
.stSlider p,
.stSlider span,
.stSlider div[data-testid="stTickBarMin"],
.stSlider div[data-testid="stTickBarMax"] {
    color: #111827 !important;
    background: transparent !important;
}

/* Fix column headers / bold labels in form */
.stMarkdown p,
.stMarkdown strong,
.stMarkdown b {
    color: #111827 !important;
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1e1b4b;
    border-right: none;
}

[data-testid="stSidebar"] * {
    color: #c7d2fe !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] strong {
    color: #e0e7ff !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #312e81 !important;
    border: 1px solid #4338ca !important;
    color: #e0e7ff !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #312e81 !important;
    color: #e0e7ff !important;
    border-radius: 10px !important;
}

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid #4338ca !important;
    color: #c7d2fe !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    height: 44px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #4338ca !important;
    color: #ffffff !important;
    border-color: #6366f1 !important;
    transform: none !important;
}

/* ── Main area buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    height: 46px !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Cards ── */
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 18px;
    border: 1px solid #e8eaf6;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.06);
    transition: box-shadow 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 16px rgba(79, 70, 229, 0.1);
}

/* ── Welcome banner ── */
.welcome-banner {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #6d28d9 100%);
    border-radius: 20px;
    padding: 24px 30px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.welcome-banner::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
}

.welcome-banner::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 30%;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: rgba(255,255,255,0.05);
}

.welcome-title {
    color: #ffffff;
    font-size: 22px;
    font-weight: 700;
    margin: 0 0 4px 0;
}

.welcome-sub {
    color: rgba(255,255,255,0.75);
    font-size: 14px;
    margin: 0;
}

/* ── Metric boxes ── */
.metric-box {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid #e8eaf6;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}

.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    border-radius: 16px 16px 0 0;
}

.metric-num {
    font-size: 34px;
    font-weight: 800;
    color: #4f46e5;
    line-height: 1.1;
}

.metric-label {
    color: #6b7280;
    font-size: 13px;
    font-weight: 500;
    margin-top: 6px;
}

/* ── Section headers ── */
.section-header {
    font-size: 20px;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid #ede9fe;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Priority badges ── */
.badge-high {
    background: #fef2f2;
    color: #b91c1c;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #fecaca;
}

.badge-medium {
    background: #fffbeb;
    color: #b45309;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #fde68a;
}

.badge-low {
    background: #f0fdf4;
    color: #15803d;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    border: 1px solid #bbf7d0;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
    border-radius: 999px !important;
}

.stProgress > div > div {
    background: #ede9fe !important;
    border-radius: 999px !important;
    height: 8px !important;
}

/* ── Inputs ── */
.stTextInput input,
.stNumberInput input,
.stSelectbox select {
    border-radius: 12px !important;
    border: 1.5px solid #ddd6fe !important;
    font-size: 14px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

.stSlider > div > div > div {
    background: #4f46e5 !important;
}

/* ── Form ── */
[data-testid="stForm"] {
    background: #ffffff;
    border-radius: 16px;
    padding: 8px 16px;
    border: 1px solid #e8eaf6;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #e8eaf6 !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    box-shadow: 0 4px 12px rgba(5, 150, 105, 0.3) !important;
}

/* ── Alerts ── */
.stSuccess {
    background: #f0fdf4 !important;
    border-left: 4px solid #22c55e !important;
    border-radius: 0 12px 12px 0 !important;
}



.stError {
    background: #fef2f2 !important;
    border-left: 4px solid #ef4444 !important;
    border-radius: 0 12px 12px 0 !important;
}

/* ── Plotly charts ── */
.js-plotly-plot {
    border-radius: 16px;
    overflow: hidden;
}

/* ── Dividers ── */
hr {
    border: none;
    border-top: 1px solid #e8eaf6;
    margin: 18px 0;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border: 1.5px solid #ddd6fe !important;
}

/* ── Sidebar profile section ── */
.sidebar-profile {
    background: rgba(99, 102, 241, 0.15);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)


# ── Session state initialize ──
def init_session():
    if "subjects" not in st.session_state:
        st.session_state.subjects = []
    if "schedule" not in st.session_state:
        st.session_state.schedule = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "student_name" not in st.session_state:
        st.session_state.student_name = "Student"
    if "semester" not in st.session_state:
        st.session_state.semester = "Semester 5"


init_session()


# ── Welcome Banner ──
st.markdown(f"""
<div class="welcome-banner">
    <p class="welcome-title">👋 Welcome back, {st.session_state.student_name}!</p>
    <p class="welcome-sub">Your AI-powered study assistant is ready to help you ace your exams.</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar Navigation ──
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px 0 10px 0; text-align: center;">
        <div style="font-size: 32px; margin-bottom: 4px;">🎓</div>
        <div style="font-size: 18px; font-weight: 700; color: #e0e7ff;">StudyAI</div>
        <div style="font-size: 12px; color: #818cf8; margin-top: 2px;">Smart Study Planner</div>
    </div>
    <hr style="border-color: #312e81; margin: 12px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**👤 Profile**")
    st.session_state.student_name = st.text_input(
        "Your Name",
        value=st.session_state.student_name,
        label_visibility="collapsed",
        placeholder="Enter your name"
    )
    st.session_state.semester = st.selectbox("Semester", [
        "Semester 1","Semester 2","Semester 3","Semester 4",
        "Semester 5","Semester 6","Semester 7","Semester 8"
    ], index=4, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📌 Navigation**")

    pages = {
        "🏠  Dashboard":   "Dashboard",
        "📚  My Subjects":  "Subjects",
        "🤖  AI Planner":   "Planner",
        "📊  Analytics":    "Analytics",
    }

    for label, page_name in pages.items():
        if st.button(label, key=f"nav_{page_name}", use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

    st.markdown("<hr style='border-color:#312e81; margin:16px 0;'>", unsafe_allow_html=True)

    n_subj = len(st.session_state.subjects)
    n_high = sum(1 for s in st.session_state.subjects if s.get("priority") == "high")
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.15); border-radius:12px; padding:14px;">
        <div style="font-size:12px; color:#a5b4fc; font-weight:600; text-transform:uppercase;
                    letter-spacing:0.5px; margin-bottom:10px;">Quick Stats</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:13px; color:#c7d2fe;">📖 Subjects</span>
            <span style="font-size:13px; font-weight:700; color:#e0e7ff;">{n_subj}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="font-size:13px; color:#c7d2fe;">🔴 High Priority</span>
            <span style="font-size:13px; font-weight:700; color:#fca5a5;">{n_high}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Page Routing ──
page = st.session_state.page

if page == "Dashboard":
    from app.dashboard import show_dashboard
    show_dashboard()

elif page == "Subjects":
    from app.planner import show_subjects
    show_subjects()

elif page == "Planner":
    from app.planner import show_planner
    show_planner()

elif page == "Analytics":
    from app.dashboard import show_analytics
    show_analytics()