# ============================================================
#  Smart Study Planner — app/dashboard.py
#  Dashboard page — charts, progress, schedule overview
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import format_hours, days_left_badge, get_study_tip, summarize_schedule
from src.scheduler import generate_schedule, generate_weekly_timetable


# ── Color map ──
PRIORITY_COLOR = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
PRIORITY_BG    = {"high": "#fef2f2", "medium": "#fffbeb", "low": "#f0fdf4"}
PRIORITY_BORDER= {"high": "#fecaca", "medium": "#fde68a", "low": "#bbf7d0"}
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}

CHART_COLORS = ["#4f46e5","#7c3aed","#06b6d4","#10b981","#f59e0b","#ef4444","#ec4899","#8b5cf6"]


def show_dashboard():
    subjects = st.session_state.get("subjects", [])

    st.markdown('<div class="section-header">🏠 Dashboard</div>', unsafe_allow_html=True)

    if not subjects:
        st.markdown("""
        <div class="card" style="text-align:center; padding:48px 24px; border:2px dashed #ddd6fe;">
            <div style="font-size:56px; margin-bottom:16px;">📚</div>
            <h3 style="color:#1e1b4b; font-size:20px; margin:0 0 8px 0;">NO subject is found!</h3>
            <p style="color:#6b7280; margin:0 0 24px 0; font-size:14px;">
                Add subjects in AI planner to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Add Subjects ", use_container_width=True):
            st.session_state.page = "Planner"
            st.rerun()
        return

    # ── Generate schedule ──
    schedule_df = generate_schedule(subjects)
    st.session_state.schedule = schedule_df
    summary = summarize_schedule(schedule_df)

    # ── Top metric cards ──
    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        (summary['total_subjects'], "📚 Total Subjects", "#4f46e5"),
        (summary['high_priority'],  "🔴 High Priority",  "#ef4444"),
        (format_hours(summary['total_hours_daily']), "⏱️ Daily Study", "#06b6d4"),
        (summary['nearest_exam_days'], "📅 Days to Exam", "#f59e0b"),
    ]

    for col, (val, label, color) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-num" style="color:{color};">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two column layout ──
    left, right = st.columns([2, 1])

    with left:
        st.markdown('<div class="section-header">📖 My Subjects</div>', unsafe_allow_html=True)

        for subj in subjects:
            comp  = float(subj.get("completion_ratio", 0.5))
            pct   = int(comp * 100)
            pri   = subj.get("priority", "low")
            days  = int(subj.get("days_until_exam", 14))
            hrs   = float(subj.get("study_hours_needed", 5))
            tip   = get_study_tip(pri, comp)
            diff  = subj.get("difficulty", "medium").capitalize()

            bg     = PRIORITY_BG.get(pri, "#f9fafb")
            border = PRIORITY_BORDER.get(pri, "#e5e7eb")
            pcolor = PRIORITY_COLOR.get(pri, "#6b7280")

            # Exam date
            exam_date = (date.today() + timedelta(days=days)).strftime("%b %d")

            st.markdown(f"""
            <div style="background:{bg}; border:1px solid {border}; border-left:4px solid {pcolor};
                        border-radius:14px; padding:18px 20px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                    <div>
                        <div style="font-size:17px; font-weight:700; color:#1e1b4b;">
                            📘 {subj['name']}
                        </div>
                        <div style="font-size:12px; color:#6b7280; margin-top:4px;">
                            🎯 {diff} &nbsp;|&nbsp; 📅 Exam: {exam_date} ({days}d) &nbsp;|&nbsp; ⏱️ {format_hours(hrs)}
                        </div>
                    </div>
                    <span class="badge-{pri}">{PRIORITY_EMOJI[pri]} {pri.capitalize()}</span>
                </div>
                <div style="font-size:12px; color:#6b7280; margin-bottom:6px; font-weight:500;">
                    Progress: <span style="color:{pcolor}; font-weight:700;">{pct}%</span>
                    &nbsp;·&nbsp; {subj.get('chapters_done',0)}/{subj.get('total_chapters',10)} chapters
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.progress(comp)

            st.markdown(f"""
            <div style="background:#f5f3ff; border-radius:8px; padding:8px 14px;
                        font-size:12px; color:#6d28d9; margin-top:-10px; margin-bottom:18px;
                        border-left:3px solid #8b5cf6;">
                💡 {tip}
            </div>
            """, unsafe_allow_html=True)

    with right:
        # ── Upcoming deadlines ──
        st.markdown('<div class="section-header">⏰ Upcoming Exams</div>', unsafe_allow_html=True)
        sorted_subj = sorted(subjects, key=lambda x: x.get("days_until_exam", 99))

        for subj in sorted_subj:
            days = int(subj.get("days_until_exam", 14))
            pri  = subj.get("priority", "low")
            exam_date = (date.today() + timedelta(days=days)).strftime("%b %d")
            pcolor = PRIORITY_COLOR.get(pri, "#6b7280")
            pbg    = PRIORITY_BG.get(pri, "#f9fafb")

            urgency = "🔥 Urgent" if days <= 3 else f"📅 {exam_date}"

            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px;
                        background:{pbg}; border-radius:12px; padding:10px 14px;
                        margin-bottom:8px; border:1px solid {PRIORITY_BORDER.get(pri,'#e5e7eb')};">
                <div style="width:10px; height:10px; border-radius:50%;
                            background:{pcolor}; flex-shrink:0;"></div>
                <div style="flex:1;">
                    <div style="font-size:13px; font-weight:600; color:#1e1b4b;">{subj['name']}</div>
                    <div style="font-size:11px; color:#6b7280; margin-top:2px;">{urgency} · {days}d left</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Study streak ──
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">🔥 Study Streak</div>', unsafe_allow_html=True)
        streak = st.session_state.get("streak", 5)
        day_labels = ["M","T","W","T","F","S","S"]
        days_row = ""
        for i, d in enumerate(day_labels):
            done = i < streak % 7
            bg = "#4f46e5" if done else "#ede9fe"
            tc = "#ffffff" if done else "#a78bfa"
            days_row += f"""
            <div style="width:32px; height:32px; border-radius:50%; background:{bg};
                        color:{tc}; display:flex; align-items:center; justify-content:center;
                        font-size:11px; font-weight:700; border: 2px solid {'#6366f1' if done else '#ddd6fe'};">
                {d}
            </div>"""

        st.markdown(f"""
        <div style="background:#f5f3ff; border-radius:14px; padding:18px;
                    border: 1px solid #ddd6fe;">
            <div style="font-size:30px; font-weight:800; color:#4f46e5; line-height:1;">
                {streak} <span style="font-size:20px;">🔥</span>
            </div>
            <div style="font-size:12px; color:#6d28d9; font-weight:500; margin:6px 0 14px;">
                Day streak — Keep it up!
            </div>
            <div style="display:flex; gap:6px;">{days_row}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Weekly timetable chart ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📅 This Week\'s Study Plan</div>', unsafe_allow_html=True)

    timetable = generate_weekly_timetable(schedule_df)
    fig = go.Figure()

    for i, subj in enumerate(subjects):
        name     = subj["name"]
        hrs_list = [subj.get("study_hours_needed", 2) / max(subj.get("days_until_exam",1),1)
                    for _ in range(7)]
        fig.add_trace(go.Bar(
            name=name,
            x=timetable["day"].tolist(),
            y=[round(h, 1) for h in hrs_list],
            marker_color=CHART_COLORS[i % len(CHART_COLORS)],
            marker_line_width=0,
            text=[f"{h:.1f}h" for h in hrs_list],
            textposition="auto",
            textfont=dict(size=11, color="white"),
        ))

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Inter, sans-serif", size=12, color="#374151"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)", font=dict(size=12)
        ),
        margin=dict(l=10, r=10, t=48, b=10),
        height=340,
        yaxis=dict(title="Hours", gridcolor="#f3f4f6", zeroline=False),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        bargap=0.25,
        bargroupgap=0.05,
    )
    fig.update_traces(marker_line_color="rgba(0,0,0,0)")

    st.plotly_chart(fig, use_container_width=True)


def show_analytics():
    subjects = st.session_state.get("subjects", [])
    st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

    if not subjects:
        st.markdown("""
        <div class="card" style="text-align:center; padding:40px; border:2px dashed #ddd6fe;">
            <div style="font-size:48px; margin-bottom:12px;">📊</div>
            <p style="color:#6b7280; font-size:15px;">First, add subjects in AI planner.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    schedule_df = generate_schedule(subjects)
    col1, col2 = st.columns(2)

    with col1:
        pri_counts = schedule_df["priority"].value_counts().reset_index()
        pri_counts.columns = ["Priority", "Count"]
        color_map = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
        fig_pie = px.pie(
            pri_counts, values="Count", names="Priority",
            color="Priority",
            color_discrete_map=color_map,
            title="Priority Distribution",
            hole=0.5,
        )
        fig_pie.update_layout(
            paper_bgcolor="white", plot_bgcolor="white", height=320,
            margin=dict(l=10, r=10, t=48, b=10),
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=15, color="#1e1b4b"),
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_bar = px.bar(
            schedule_df,
            x="subject", y="completion_pct",
            color="priority",
            color_discrete_map=color_map,
            title="Completion % per Subject",
            labels={"completion_pct": "Completion %", "subject": ""},
            text="completion_pct",
        )
        fig_bar.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig_bar.update_layout(
            paper_bgcolor="white", plot_bgcolor="white", height=320,
            margin=dict(l=10, r=10, t=48, b=10),
            showlegend=False,
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=15, color="#1e1b4b"),
            yaxis=dict(gridcolor="#f3f4f6", zeroline=False, range=[0, 115]),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            bargap=0.35,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Summary table ──
    st.markdown('<div class="section-header">📋 Schedule Summary</div>', unsafe_allow_html=True)
    display_df = schedule_df[[
        "subject", "priority", "days_remaining",
        "completion_pct", "daily_study_hrs", "hours_needed"
    ]].copy()
    display_df.columns = ["Subject", "Priority", "Days Left", "Done %", "Daily Hrs", "Total Hrs"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)