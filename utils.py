# ============================================================
#  Smart Study Planner — src/utils.py
#  Reusable helper functions
# ============================================================

import pandas as pd
import numpy as np
from datetime import date, timedelta
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HIGH_PRIORITY_DAYS, MEDIUM_PRIORITY_DAYS


def priority_color(priority: str) -> str:
    """Streamlit mein color badge ke liye."""
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")


def days_left_badge(days: int) -> str:
    """Days remaining ka short label."""
    if days <= 1:
        return "⚠️ Tomorrow!"
    elif days <= HIGH_PRIORITY_DAYS:
        return f"🔴 {days} days"
    elif days <= MEDIUM_PRIORITY_DAYS:
        return f"🟡 {days} days"
    else:
        return f"🟢 {days} days"


def completion_bar(ratio: float, width: int = 20) -> str:
    """Terminal mein simple progress bar."""
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {ratio * 100:.0f}%"


def validate_subject_input(data: dict) -> tuple[bool, str]:
    """
    User input validate karo before schedule generation.
    Returns (is_valid, error_message).
    """
    required = ["name", "days_until_exam", "daily_free_hours",
                 "total_chapters", "chapters_done"]

    for field in required:
        if field not in data or data[field] is None:
            return False, f"'{field}' field required hai."

    if data["days_until_exam"] < 1:
        return False, "Exam abhi ya kal nahi ho sakta — kam se kam 1 din chahiye."
    if data["daily_free_hours"] < 0.5:
        return False, "Roz kam se kam 30 minute free hone chahiye."
    if data["chapters_done"] > data["total_chapters"]:
        return False, "Chapters done, total chapters se zyada nahi ho sakti."
    if data["total_chapters"] < 1:
        return False, "Total chapters kam se kam 1 hona chahiye."

    return True, ""


def compute_urgency_score(remaining_chapters: int,
                           days_until_exam: int) -> float:
    """Urgency score: jitna zyada utna zyada urgent."""
    return round(remaining_chapters / (days_until_exam + 1), 3)


def format_hours(hours: float) -> str:
    """1.5 → '1h 30m' format mein."""
    h = int(hours)
    m = int((hours - h) * 60)
    if h == 0:
        return f"{m}m"
    elif m == 0:
        return f"{h}h"
    return f"{h}h {m}m"


def get_study_tip(priority: str, completion_ratio: float) -> str:
    """Motivational tip based on priority aur progress."""
    if priority == "high" and completion_ratio < 0.5:
        return "Abhi focus karo — exam nazdik hai aur bohot kuch bacha hai!"
    elif priority == "high":
        return "Acha progress hai, lekin exam nazdik hai. Revision shuru karo!"
    elif priority == "medium" and completion_ratio < 0.4:
        return "Thoda tez chalo — completion ratio low hai."
    elif completion_ratio >= 0.8:
        return "Bohot acha! Sirf revision bacha hai."
    else:
        return "Consistent raho — daily target miss mat karo."


def summarize_schedule(schedule_df: pd.DataFrame) -> dict:
    """Schedule ka quick summary return karo."""
    return {
        "total_subjects":    len(schedule_df),
        "high_priority":     len(schedule_df[schedule_df["priority"] == "high"]),
        "medium_priority":   len(schedule_df[schedule_df["priority"] == "medium"]),
        "low_priority":      len(schedule_df[schedule_df["priority"] == "low"]),
        "total_hours_daily": round(schedule_df["daily_study_hrs"].sum(), 1),
        "avg_completion":    round(schedule_df["completion_pct"].mean(), 1),
        "nearest_exam_days": int(schedule_df["days_remaining"].min()),
    }


if __name__ == "__main__":
    print(format_hours(1.5))       # 1h 30m
    print(format_hours(0.75))      # 45m
    print(completion_bar(0.6))     # progress bar
    print(days_left_badge(2))      # red badge
    print(get_study_tip("high", 0.3))