# ============================================================
#  Smart Study Planner — src/ml_models.py
#  Regression, Classification, aur Clustering sab yahan hai
# ============================================================

import numpy as np
import pandas as pd
import joblib
import os
import sys

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error, r2_score,
    accuracy_score, classification_report
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    REGRESSION_MODEL_PATH, CLASSIFIER_MODEL_PATH, KMEANS_MODEL_PATH,
    MODELS_DIR, TEST_SIZE, RANDOM_SEED, N_CLUSTERS, KNN_NEIGHBORS
)


# ──────────────────────────────────────────────
#  1. REGRESSION — study hours predict karna
# ──────────────────────────────────────────────

def train_regression(X, y):
    """
    Linear Regression: kitne hours study karne padenge?
    Input  : feature matrix X, target y (study_hours_needed)
    Output : trained model, RMSE, R² score
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
    r2     = r2_score(y_test, y_pred)

    print(f"\n[Regression]  RMSE={rmse:.3f}  R²={r2:.3f}")

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, REGRESSION_MODEL_PATH)
    print(f"  Saved → {REGRESSION_MODEL_PATH}")

    return model, rmse, r2


def predict_study_hours(model, features: dict) -> float:
    """
    Ek subject ke liye study hours predict karo.
    features dict mein wahi keys honi chahiye jo training mein thi.
    """
    df = pd.DataFrame([features])
    hours = model.predict(df)[0]
    return round(max(0.5, hours), 1)


# ──────────────────────────────────────────────
#  2. CLASSIFICATION — priority predict karna
# ──────────────────────────────────────────────

def train_classifier(X, y, method: str = "decision_tree"):
    """
    Classification: subject ki priority kya hai? (low/medium/high)
    method: 'decision_tree' ya 'knn'
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )

    if method == "knn":
        model = KNeighborsClassifier(n_neighbors=KNN_NEIGHBORS)
    else:
        model = DecisionTreeClassifier(max_depth=6, random_state=RANDOM_SEED)

    model.fit(X_train, y_train)

    y_pred   = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n[Classifier — {method}]  Accuracy={accuracy:.3f}")
    print(classification_report(y_test, y_pred,
                                 target_names=["low", "medium", "high"],
                                 zero_division=0))

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, CLASSIFIER_MODEL_PATH)
    print(f"  Saved → {CLASSIFIER_MODEL_PATH}")

    return model, accuracy


def predict_priority(model, features: dict) -> str:
    """0=low, 1=medium, 2=high string mein return karo."""
    df    = pd.DataFrame([features])
    label = model.predict(df)[0]
    return {0: "low", 1: "medium", 2: "high"}.get(label, "medium")


# ──────────────────────────────────────────────
#  3. CLUSTERING — subjects group karna
# ──────────────────────────────────────────────

def train_kmeans(X, n_clusters: int = N_CLUSTERS):
    """
    K-Means: subjects ko difficulty groups mein cluster karo.
    Unsupervised — koi labels nahi chahiye.
    """
    model = KMeans(n_clusters=n_clusters, random_state=RANDOM_SEED, n_init=10)
    labels = model.fit_predict(X)

    inertia = model.inertia_
    print(f"\n[K-Means]  clusters={n_clusters}  inertia={inertia:.1f}")

    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(model, KMEANS_MODEL_PATH)
    print(f"  Saved → {KMEANS_MODEL_PATH}")

    return model, labels


def get_cluster_label(cluster_id: int, cluster_centers) -> str:
    """
    Cluster ID ko human-readable name deta hai
    based on center ka urgency_score (last feature).
    """
    scores = [center[-1] for center in cluster_centers]
    sorted_ids = np.argsort(scores)
    rank = list(sorted_ids).index(cluster_id)
    return ["Low load", "Medium load", "High load"][rank]


# ──────────────────────────────────────────────
#  4. Model load karne ke helpers
# ──────────────────────────────────────────────

def load_regression_model():
    return joblib.load(REGRESSION_MODEL_PATH)

def load_classifier_model():
    return joblib.load(CLASSIFIER_MODEL_PATH)

def load_kmeans_model():
    return joblib.load(KMEANS_MODEL_PATH)


if __name__ == "__main__":
    # Quick test — dummy data se
    print("ML Models module loaded successfully.")
    print("Train karne ke liye notebooks/02_models.ipynb use karo.")