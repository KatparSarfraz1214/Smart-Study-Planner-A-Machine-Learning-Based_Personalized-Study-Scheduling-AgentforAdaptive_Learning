# ============================================================
#  Smart Study Planner — src/scheduler.py
#  Rule-based + ML combined schedule generator (Classical AI)
# ============================================================

import pandas as pd
import numpy as np
from datetime import date, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    HIGH_PRIORITY_DAYS, MEDIUM_PRIORITY_DAYS,
    MIN_STUDY_HOURS_PER_DAY, MAX_STUDY_HOURS_PER_DAY
)


# ──────────────────────────────────────────────
#  Rule-Based Priority Engine (Classical AI)
# ──────────────────────────────────────────────

def assign_priority_rule(days_until_exam: int, completion_ratio: float) -> str:
    """
    Simple rule-based agent:
      - Agar exam nazdik hai ya completion kam hai → high
      - Agar thoda waqt hai → medium
      - Agar kaafi waqt hai → low
    """
    if days_until_exam <= HIGH_PRIORITY_DAYS:
        return "high"
    elif days_until_exam <= MEDIUM_PRIORITY_DAYS or completion_ratio < 0.4:
        return "medium"
    else:
        return "low"


def calculate_daily_hours(study_hours_needed: float,
                           days_until_exam: int,
                           daily_free_hours: float) -> float:
    """
    Roz kitne ghante padhne chahiye yeh calculate karo.
    Total needed hours ko remaining days mein divide karo.
    """
    if days_until_exam <= 0:
        return 0.0
    raw = study_hours_needed / days_until_exam
    # Daily free hours se zyada nahi kar sakte
    capped = min(raw, daily_free_hours, MAX_STUDY_HOURS_PER_DAY)
    return round(max(capped, MIN_STUDY_HOURS_PER_DAY), 1)


# ──────────────────────────────────────────────
#  Schedule Generator
# ──────────────────────────────────────────────

def generate_schedule(subjects_data: list[dict],
                      start_date: date = None) -> pd.DataFrame:
    """
    Subjects ki list se weekly schedule banata hai.

    subjects_data — list of dicts, har dict mein:
        name               : subject ka naam
        days_until_exam    : int
        daily_free_hours   : float
        study_hours_needed : float  (ML se predicted ya manually entered)
        completion_ratio   : float  (0.0 to 1.0)

    Returns:
        schedule_df — har subject ke liye daily time slots
    """
    if start_date is None:
        start_date = date.today()

    rows = []

    for subj in subjects_data:
        name          = subj["name"]
        days_left     = int(subj["days_until_exam"])
        free_hours    = float(subj["daily_free_hours"])
        hours_needed  = float(subj["study_hours_needed"])
        comp_ratio    = float(subj.get("completion_ratio", 0.5))

        priority      = assign_priority_rule(days_left, comp_ratio)
        daily_hrs     = calculate_daily_hours(hours_needed, days_left, free_hours)
        exam_date     = start_date + timedelta(days=days_left)

        rows.append({
            "subject":          name,
            "exam_date":        exam_date.strftime("%Y-%m-%d"),
            "days_remaining":   days_left,
            "priority":         priority,
            "hours_needed":     hours_needed,
            "daily_study_hrs":  daily_hrs,
            "completion_pct":   round(comp_ratio * 100, 1),
        })

    df = pd.DataFrame(rows)

    # Sort by priority (high first), phir days_remaining
    priority_order = {"high": 0, "medium": 1, "low": 2}
    df["priority_rank"] = df["priority"].map(priority_order)
    df = df.sort_values(["priority_rank", "days_remaining"]).drop("priority_rank", axis=1)

    return df.reset_index(drop=True)


def generate_weekly_timetable(schedule_df: pd.DataFrame,
                               start_date: date = None) -> pd.DataFrame:
    """
    7-day timetable banata hai — kaunse din kaunsa subject padhna hai.
    Greedy algorithm: high priority subjects ko pehle allocate karo.
    """
    if start_date is None:
        start_date = date.today()

    days = [start_date + timedelta(days=i) for i in range(7)]
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    timetable = {d.strftime("%Y-%m-%d"): [] for d in days}

    # Greedy: har din subjects allocate karo by priority
    for _, row in schedule_df.iterrows():
        subj_name = row["subject"]
        hrs_per_day = row["daily_study_hrs"]
        priority = row["priority"]

        for day in days:
            day_str = day.strftime("%Y-%m-%d")
            timetable[day_str].append({
                "subject":  subj_name,
                "hours":    hrs_per_day,
                "priority": priority
            })

    # Flatten into DataFrame
    rows = []
    for i, day in enumerate(days):
        day_str = day.strftime("%Y-%m-%d")
        slots = timetable[day_str]
        total_hrs = sum(s["hours"] for s in slots)
        subjects_today = ", ".join(s["subject"].split()[0] for s in slots)
        rows.append({
            "day":        day_names[i],
            "date":       day_str,
            "subjects":   subjects_today,
            "total_hours": round(total_hrs, 1),
            "slots":       slots,
        })

    return pd.DataFrame(rows)


def reschedule_missed(schedule_df: pd.DataFrame,
                      missed_subject: str) -> pd.DataFrame:
    """
    Agar koi subject miss ho jaye toh uski priority boost karo.
    Classical AI adaptive behavior.
    """
    df = schedule_df.copy()
    mask = df["subject"] == missed_subject

    if not mask.any():
        print(f"Subject '{missed_subject}' nahi mila.")
        return df

    # Priority upgrade
    current = df.loc[mask, "priority"].values[0]
    upgraded = {"low": "medium", "medium": "high", "high": "high"}[current]
    df.loc[mask, "priority"] = upgraded

    # Daily hours bhi thodi barha do (max 8 se nahi zyada)
    df.loc[mask, "daily_study_hrs"] = df.loc[mask, "daily_study_hrs"].apply(
        lambda x: min(x + 0.5, MAX_STUDY_HOURS_PER_DAY)
    )

    print(f"'{missed_subject}' rescheduled: {current} → {upgraded}")
    return df


if __name__ == "__main__":
    sample_subjects = [
        {"name": "AI",       "days_until_exam": 14, "daily_free_hours": 4, "study_hours_needed": 18, "completion_ratio": 0.75},
        {"name": "Database", "days_until_exam": 14, "daily_free_hours": 3, "study_hours_needed": 12, "completion_ratio": 0.60},
        {"name": "OS",       "days_until_exam": 14, "daily_free_hours": 3, "study_hours_needed": 20, "completion_ratio": 0.45},
    ]
    schedule = generate_schedule(sample_subjects)
    print("\nGenerated Schedule:")
    print(schedule.to_string(index=False))

    timetable = generate_weekly_timetable(schedule)
    print("\nWeekly Timetable:")
    print(timetable[["day", "date", "subjects", "total_hours"]].to_string(index=False))