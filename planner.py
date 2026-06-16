# ============================================================
#  Smart Study Planner — app/planner.py
#  Subject input form + AI schedule generator page
# ============================================================

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import joblib
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scheduler import generate_schedule, reschedule_missed
from src.utils import (
    format_hours, days_left_badge, get_study_tip,
    validate_subject_input, compute_urgency_score, priority_color
)
from config import (
    SUBJECTS, DIFFICULTY_LEVELS,
    REGRESSION_MODEL_PATH, CLASSIFIER_MODEL_PATH
)

PRIORITY_COLOR  = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
PRIORITY_BG     = {"high": "#fef2f2", "medium": "#fffbeb", "low": "#f0fdf4"}
PRIORITY_BORDER = {"high": "#fecaca", "medium": "#fde68a", "low": "#bbf7d0"}
PRIORITY_EMOJI  = {"high": "🔴", "medium": "🟡", "low": "🟢"}


# ── Load ML models ──
@st.cache_resource
def load_models():
    models = {}
    try:
        models["regression"]  = joblib.load(REGRESSION_MODEL_PATH)
        models["classifier"]  = joblib.load(CLASSIFIER_MODEL_PATH)
        models["loaded"] = True
    except Exception as e:
        models["loaded"] = False
        models["error"]  = str(e)
    return models


def predict_with_ml(models, subject_data: dict) -> dict:
    """Using ML to predict hours and prority."""
    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}

    total_ch  = int(subject_data["total_chapters"])
    done_ch   = int(subject_data["chapters_done"])
    remaining = total_ch - done_ch
    comp_ratio = done_ch / max(total_ch, 1)
    urgency   = compute_urgency_score(remaining, int(subject_data["days_until_exam"]))

    features_reg = {
        "difficulty_enc":     difficulty_map.get(subject_data["difficulty"], 1),
        "total_chapters":     total_ch,
        "remaining_chapters": remaining,
        "completion_ratio":   comp_ratio,
        "days_until_exam":    int(subject_data["days_until_exam"]),
        "daily_free_hours":   float(subject_data["daily_free_hours"]),
        "mid_score":          int(subject_data.get("mid_score", 70)),
        "urgency_score":      urgency,
    }
    features_clf = {**features_reg, "study_hours_needed": 10.0}

    reg_model = models["regression"]
    clf_model = models["classifier"]

    import pandas as pd
    X_reg = pd.DataFrame([features_reg])
    X_clf = pd.DataFrame([features_clf])

    hours    = round(max(0.5, float(reg_model.predict(X_reg)[0])), 1)
    pri_enc  = clf_model.predict(X_clf)[0]
    priority = {0: "low", 1: "medium", 2: "high"}.get(int(pri_enc), "medium")

    return {
        "study_hours_needed": hours,
        "priority":           priority,
        "completion_ratio":   comp_ratio,
        "remaining_chapters": remaining,
    }


# ══════════════════════════════════════════════════════════
#  PAGE 1 — My Subjects
# ══════════════════════════════════════════════════════════

def show_subjects():
    subjects = st.session_state.get("subjects", [])
    st.markdown('<div class="section-header">📚 My Subjects</div>', unsafe_allow_html=True)

    if not subjects:
        st.markdown("""
        <div class="card" style="text-align:center; padding:48px 24px; border:2px dashed #ddd6fe;">
            <div style="font-size:56px; margin-bottom:16px;">📭</div>
            <h3 style="color:#1e1b4b; font-size:20px; margin:0 0 8px 0;">No subject is Found</h3>
            <p style="color:#6b7280; margin:0 0 24px 0; font-size:14px;">
                Go to AI planner and add subjects.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🤖 Open AI planner", use_container_width=True):
            st.session_state.page = "Planner"
            st.rerun()
        return

    # ── Stats row ──
    c1, c2, c3 = st.columns(3)
    avg_comp = sum(s.get("completion_ratio", 0) for s in subjects) / len(subjects)
    high_count = sum(1 for s in subjects if s.get("priority") == "high")

    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-num">{len(subjects)}</div>
            <div class="metric-label">📖 Total Subjects</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-num" style="color:#06b6d4;">{avg_comp*100:.0f}%</div>
            <div class="metric-label">✅ Avg Completion</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-num" style="color:#ef4444;">{high_count}</div>
            <div class="metric-label">🔴 High Priority</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Subject cards ──
    for i, subj in enumerate(subjects):
        comp  = float(subj.get("completion_ratio", 0.5))
        pct   = int(comp * 100)
        pri   = subj.get("priority", "medium")
        days  = int(subj.get("days_until_exam", 14))
        hrs   = float(subj.get("study_hours_needed", 5))
        diff  = subj.get("difficulty", "medium").capitalize()
        exam_date = (date.today() + timedelta(days=days)).strftime("%b %d, %Y")

        pcolor = PRIORITY_COLOR.get(pri, "#6b7280")
        pbg    = PRIORITY_BG.get(pri, "#f9fafb")
        pborder= PRIORITY_BORDER.get(pri, "#e5e7eb")

        with st.container():
            st.markdown(f"""
            <div style="background:{pbg}; border:1px solid {pborder}; border-left:4px solid {pcolor};
                        border-radius:14px; padding:18px 20px; margin-bottom:6px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div style="font-size:17px; font-weight:700; color:#1e1b4b;">
                            📘 {subj['name']}
                        </div>
                        <div style="font-size:12px; color:#6b7280; margin-top:6px; display:flex; gap:14px; flex-wrap:wrap;">
                            <span>🎯 <b style="color:#374151;">{diff}</b></span>
                            <span>📅 <b style="color:#374151;">{exam_date}</b> ({days}d)</span>
                            <span>⏱️ <b style="color:#374151;">{format_hours(hrs)}</b> needed</span>
                            <span>📖 <b style="color:#374151;">{subj.get('chapters_done',0)}/{subj.get('total_chapters',10)}</b> chapters</span>
                        </div>
                    </div>
                    <span class="badge-{pri}" style="white-space:nowrap;">
                        {PRIORITY_EMOJI[pri]} {pri.capitalize()}
                    </span>
                </div>
                <div style="font-size:12px; color:#6b7280; margin:14px 0 6px 0; font-weight:500;">
                    Completion Progress — <span style="color:{pcolor}; font-weight:700;">{pct}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(comp)

            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
            with btn_col1:
                if st.button("🔁 Rescheduled", key=f"miss_{i}"):
                    updated = reschedule_missed(
                        generate_schedule(subjects), subj["name"]
                    )
                    subjects[i]["priority"] = updated[
                        updated["subject"] == subj["name"]
                    ]["priority"].values[0]
                    st.session_state.subjects = subjects
                    st.success(f"'{subj['name']}' rescheduled!")
                    st.rerun()
            with btn_col2:
                if st.button("🗑️ Remove", key=f"del_{i}"):
                    st.session_state.subjects.pop(i)
                    st.rerun()

            st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE 2 — AI Planner
# ══════════════════════════════════════════════════════════

def show_planner():
    st.markdown('<div class="section-header">🤖 AI Planner</div>', unsafe_allow_html=True)

    models = load_models()
    

    # ── Form header ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#4f46e5,#7c3aed); border-radius:16px;
                padding:20px 24px; margin-bottom:20px; color:white;">
        <div style="font-size:18px; font-weight:700; margin-bottom:4px;">➕ Add new subject</div>
        <div style="font-size:13px; opacity:0.8;">
            AI will predict your subject study time and prioritized it.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_subject_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📘 Subject Details**")
            name = st.selectbox("Subject", SUBJECTS + ["Other (Custom)"],
                                label_visibility="collapsed")
            if name == "Other (Custom)":
                name = st.text_input("Custom subject naam likho",
                                     placeholder="e.g. Artificial Intelligence")
            difficulty = st.selectbox(
                "Difficulty Level",
                DIFFICULTY_LEVELS,
                format_func=lambda x: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}.get(x, x),
                label_visibility="visible"
            )
            days_until_exam = st.number_input(
                "📅 How many days are left in exams?",
                min_value=1, max_value=180, value=14
            )

        with col2:
            st.markdown("**📖 Progress & Schedule**")
            total_chapters = st.number_input(
                "Total Chapters", min_value=1, max_value=30, value=10
            )
            chapters_done = st.number_input(
                "Chapters Done ✅", min_value=0,
                max_value=int(total_chapters), value=5
            )
            daily_free_hours = st.slider(
                "⏰ How many hours can give study daily?",
                min_value=0.5, max_value=10.0, value=3.0, step=0.5,
                format="%.1f hrs"
            )
            mid_score = st.number_input(
                "📝 Mid Term Score (0–100)",
                min_value=0, max_value=100, value=70
            )

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🤖 Generate schedule with AI",
            use_container_width=True
        )

        if submitted:
            input_data = {
                "name":             name,
                "difficulty":       difficulty,
                "days_until_exam":  days_until_exam,
                "total_chapters":   total_chapters,
                "chapters_done":    chapters_done,
                "daily_free_hours": daily_free_hours,
                "mid_score":        mid_score,
            }

            is_valid, err = validate_subject_input(input_data)
            if not is_valid:
                st.error(f"❌ {err}")
            else:
                if models["loaded"]:
                    preds = predict_with_ml(models, input_data)
                    input_data.update(preds)
                    pri = preds['priority']
                    pcolor = PRIORITY_COLOR.get(pri, "#6b7280")
                    st.success(
                        f"🤖 AI Prediction: **{format_hours(preds['study_hours_needed'])}** study time · "
                        f"Priority: **{preds['priority'].upper()}**"
                    )
                else:
                    remaining  = total_chapters - chapters_done
                    comp_ratio = chapters_done / max(total_chapters, 1)
                    diff_mult  = {"easy": 1.2, "medium": 1.8, "hard": 2.5}.get(difficulty, 1.5)
                    hours      = round(remaining * diff_mult, 1)
                    priority   = "high" if days_until_exam <= 3 else "medium" if days_until_exam <= 7 else "low"
                    input_data.update({
                        "study_hours_needed": hours,
                        "priority":           priority,
                        "completion_ratio":   comp_ratio,
                        "remaining_chapters": remaining,
                    })

                existing_names = [s["name"] for s in st.session_state.subjects]
                if name in existing_names:
                    st.warning(f"⚠️ '{name}' Already exist.")
                else:
                    st.session_state.subjects.append(input_data)
                    st.success(f"✅ '{name}' successfully added!")
                    st.rerun()

    # ── Current Schedule ──
    subjects = st.session_state.get("subjects", [])
    if subjects:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 Generated Schedule</div>', unsafe_allow_html=True)

        schedule_df = generate_schedule(subjects)

        for _, row in schedule_df.iterrows():
            pri    = row["priority"]
            pcolor = PRIORITY_COLOR.get(pri, "#6b7280")
            pbg    = PRIORITY_BG.get(pri, "#f9fafb")
            pborder= PRIORITY_BORDER.get(pri, "#e5e7eb")

            st.markdown(f"""
            <div style="background:{pbg}; border:1px solid {pborder}; border-left:4px solid {pcolor};
                        border-radius:14px; padding:18px 20px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:16px; font-weight:700; color:#1e1b4b; margin-bottom:6px;">
                            {PRIORITY_EMOJI[pri]} {row['subject']}
                        </div>
                        <div style="font-size:12px; color:#6b7280; display:flex; gap:16px; flex-wrap:wrap;">
                            <span>📅 Exam: <b style="color:#374151;">{row['exam_date']}</b></span>
                            <span>⏱️ Daily: <b style="color:#374151;">{format_hours(row['daily_study_hrs'])}</b></span>
                            <span>📊 Done: <b style="color:#374151;">{row['completion_pct']}%</b></span>
                        </div>
                    </div>
                    <div style="text-align:right; flex-shrink:0; margin-left:16px;">
                        <div style="font-size:26px; font-weight:800; color:{pcolor}; line-height:1;">
                            {format_hours(row['hours_needed'])}
                        </div>
                        <div style="font-size:11px; color:#9ca3af; margin-top:2px;">total needed</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Action buttons ──
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            csv = schedule_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV Schedule",
                data=csv,
                file_name="my_study_schedule.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with col2:
            if st.button("🗑️ Clear all", use_container_width=True):
                st.session_state.subjects = []
                st.session_state.schedule = None
                st.rerun()