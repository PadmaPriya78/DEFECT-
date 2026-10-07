"""
Loads the trained model (best_model.pkl / scaler.pkl / feature_columns.pkl)
produced by train_model.py. If those artifacts aren't present yet, falls back
to a transparent heuristic score so the app still runs end-to-end.
"""

import os
import joblib
import numpy as np

MODEL_DIR = os.getenv("MODEL_DIR", "./ml_artifacts")

_model = None
_scaler = None
_feature_columns = None
_model_loaded = False


def _try_load():
    global _model, _scaler, _feature_columns, _model_loaded
    if _model_loaded:
        return
    model_path = os.path.join(MODEL_DIR, "best_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    cols_path = os.path.join(MODEL_DIR, "feature_columns.pkl")

    if os.path.exists(model_path) and os.path.exists(cols_path):
        _model = joblib.load(model_path)
        _feature_columns = joblib.load(cols_path)
        _scaler = joblib.load(scaler_path) if os.path.exists(scaler_path) else None
    _model_loaded = True


def _heuristic_probability(features: dict) -> float:
    """Fallback scoring, used only until a trained model is dropped into MODEL_DIR."""
    complexity = features.get("complexity", 0)
    loc = features.get("loc", 0)
    comment_ratio = features.get("comment_ratio", 0)
    num_functions = max(features.get("num_functions", 1), 1)

    complexity_per_fn = complexity / num_functions
    size_penalty = min(loc / 1000, 1.0)
    complexity_penalty = min(complexity_per_fn / 15, 1.0)
    doc_bonus = min(comment_ratio * 2, 0.3)

    score = 0.5 * complexity_penalty + 0.4 * size_penalty - doc_bonus
    return float(max(0.0, min(1.0, score)))


def predict_probability(features: dict) -> float:
    _try_load()
    if _model is not None and _feature_columns is not None:
        row = np.array([[features.get(col, 0) for col in _feature_columns]])
        if _scaler is not None and _model.__class__.__name__ == "LogisticRegression":
            row = _scaler.transform(row)
        proba = _model.predict_proba(row)[0][1]
        return float(proba)
    return _heuristic_probability(features)


def probability_to_risk(prob: float) -> str:
    if prob >= 0.70:
        return "HIGH"
    if prob >= 0.40:
        return "MEDIUM"
    return "LOW"


def generate_flag_reason(features: dict, prob: float) -> str | None:
    risk = probability_to_risk(prob)
    if risk == "LOW":
        return None

    reasons = []
    loc = features.get("loc", 0)
    complexity = features.get("complexity", 0)
    comment_ratio = features.get("comment_ratio", 0)
    num_functions = max(features.get("num_functions", 1), 1)

    if loc > 500:
        reasons.append("File is excessively large (>500 lines).")
    elif loc > 200:
        reasons.append("File is quite large (>200 lines).")

    complexity_per_fn = complexity / num_functions
    if complexity_per_fn > 15:
        reasons.append("Average complexity per function is very high (>15).")
    elif complexity_per_fn > 10:
        reasons.append("Average complexity per function is moderately high (>10).")
    elif complexity > 50:
        reasons.append("Overall file complexity is high.")

    if comment_ratio < 0.05:
        reasons.append("Very few comments (<5% of code).")

    if not reasons:
        reasons.append("Model detected complex code patterns correlated with defects.")

    return " ".join(reasons)


def is_model_ready() -> bool:
    _try_load()
    return _model is not None
