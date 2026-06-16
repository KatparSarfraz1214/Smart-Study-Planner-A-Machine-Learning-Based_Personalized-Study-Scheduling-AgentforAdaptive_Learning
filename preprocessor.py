# ============================================================
#  Smart Study Planner — src/preprocessor.py
#  Raw data clean karta hai aur ML ke liye ready karta hai
# ============================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    RAW_DATA_PATH, CLEANED_DATA_PATH, FEATURES_PATH, DATA_DIR
)


def load_raw_data(path: str = RAW_DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Loaded: {path}  shape={df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Null values handle karo, duplicates drop karo."""
    original_len = len(df)
    df = df.drop_duplicates()
    df = df.dropna()

    # chapters_done kabhi total_chapters se zyada nahi honi chahiye
    df = df[df["chapters_done"] <= df["total_chapters"]]

    # study_hours_needed positive hona chahiye
    df = df[df["study_hours_needed"] > 0]

    print(f"Cleaned: {original_len} → {len(df)} rows")
    return df.reset_index(drop=True)


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorical columns ko numbers mein convert karo.
        difficulty : easy=0, medium=1, hard=2
        priority   : low=0, medium=1, high=2
        subject    : LabelEncoder
    """
    df = df.copy()

    difficulty_map = {"easy": 0, "medium": 1, "hard": 2}
    priority_map   = {"low": 0, "medium": 1, "high": 2}

    df["difficulty_enc"] = df["difficulty"].map(difficulty_map)
    df["priority_enc"]   = df["priority"].map(priority_map)

    le = LabelEncoder()
    df["subject_enc"] = le.fit_transform(df["subject"])

    # Feature engineering — kuch extra useful columns
    df["remaining_chapters"] = df["total_chapters"] - df["chapters_done"]
    df["completion_ratio"]   = df["chapters_done"] / df["total_chapters"]
    df["urgency_score"]      = df["remaining_chapters"] / (df["days_until_exam"] + 1)

    return df


def get_feature_matrix(df: pd.DataFrame):
    """
    ML ke liye X (features) aur y targets return karta hai.
    Returns:
        X_reg   - regression features (study hours predict karne ke liye)
        y_reg   - regression target (study_hours_needed)
        X_clf   - classification features (priority predict karne ke liye)
        y_clf   - classification target (priority_enc)
    """
    regression_features = [
        "difficulty_enc", "total_chapters", "remaining_chapters",
        "completion_ratio", "days_until_exam", "daily_free_hours",
        "mid_score", "urgency_score"
    ]

    classification_features = [
        "difficulty_enc", "remaining_chapters", "completion_ratio",
        "days_until_exam", "daily_free_hours", "mid_score",
        "urgency_score", "study_hours_needed"
    ]

    X_reg = df[regression_features]
    y_reg = df["study_hours_needed"]

    X_clf = df[classification_features]
    y_clf = df["priority_enc"]

    return X_reg, y_reg, X_clf, y_clf


def scale_features(X_train, X_test):
    """StandardScaler apply karo — mean=0, std=1."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def run_preprocessing() -> pd.DataFrame:
    """Full pipeline: load → clean → encode → save."""
    os.makedirs(DATA_DIR, exist_ok=True)

    df = load_raw_data()
    df = clean_data(df)
    df = encode_features(df)

    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Cleaned data saved: {CLEANED_DATA_PATH}")

    feature_cols = [c for c in df.columns if c.endswith("_enc") or c in [
        "remaining_chapters", "completion_ratio", "urgency_score"
    ]]
    df[feature_cols].to_csv(FEATURES_PATH, index=False)
    print(f"Feature matrix saved: {FEATURES_PATH}")

    return df


if __name__ == "__main__":
    df = run_preprocessing()
    print("\nProcessed sample:")
    print(df[["subject", "difficulty", "difficulty_enc",
              "priority", "priority_enc", "urgency_score"]].head(8))