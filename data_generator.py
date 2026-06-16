# ============================================================
#  Smart Study Planner — src/data_generator.py
#  Synthetic dataset generate karta hai ML training ke liye
# ============================================================

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    SUBJECTS, DIFFICULTY_LEVELS, NUM_SAMPLES,
    RANDOM_SEED, RAW_DATA_PATH, DATA_DIR
)


def generate_dataset(num_samples: int = NUM_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """
    Synthetic study planner dataset banata hai.

    Columns:
        subject          - subject ka naam
        difficulty       - easy / medium / hard
        total_chapters   - kitne chapters hain
        chapters_done    - kitne complete ho gaye
        days_until_exam  - exam mein kitne din baaki hain
        daily_free_hours - roz kitne ghante available hain
        mid_score        - mid term marks (0-100)
        study_hours_needed - target variable (regression ke liye)
        priority         - high / medium / low (classification ke liye)
    """
    np.random.seed(seed)
    n = num_samples

    subjects        = np.random.choice(SUBJECTS, n)
    difficulties    = np.random.choice(DIFFICULTY_LEVELS, n, p=[0.3, 0.45, 0.25])
    total_chapters  = np.random.randint(6, 16, n)
    chapters_done   = np.array([np.random.randint(0, tc + 1) for tc in total_chapters])
    days_until_exam = np.random.randint(1, 31, n)
    daily_free_hours = np.round(np.random.uniform(1.0, 7.0, n), 1)
    mid_score       = np.random.randint(40, 101, n)

    # Remaining chapters ratio
    remaining_ratio = (total_chapters - chapters_done) / total_chapters

    # study_hours_needed — difficulty + remaining work se calculate
    diff_multiplier = np.where(difficulties == "hard", 2.5,
                      np.where(difficulties == "medium", 1.8, 1.2))
    base_hours = remaining_ratio * total_chapters * diff_multiplier
    noise = np.random.normal(0, 0.5, n)
    study_hours_needed = np.clip(np.round(base_hours + noise, 1), 0.5, 40.0)

    # Priority — days_until_exam pe based rule
    priority = np.where(days_until_exam <= 3, "high",
               np.where(days_until_exam <= 7, "medium", "low"))

    df = pd.DataFrame({
        "subject":             subjects,
        "difficulty":          difficulties,
        "total_chapters":      total_chapters,
        "chapters_done":       chapters_done,
        "days_until_exam":     days_until_exam,
        "daily_free_hours":    daily_free_hours,
        "mid_score":           mid_score,
        "study_hours_needed":  study_hours_needed,
        "priority":            priority,
    })

    return df


def save_dataset(df: pd.DataFrame, path: str = RAW_DATA_PATH) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Dataset saved: {path}  ({len(df)} rows)")


if __name__ == "__main__":
    df = generate_dataset()
    save_dataset(df)
    print("\nSample rows:")
    print(df.head())
    print("\nColumn info:")
    print(df.dtypes)
    print("\nPriority distribution:")
    print(df["priority"].value_counts())
    print("\nDifficulty distribution:")
    print(df["difficulty"].value_counts())