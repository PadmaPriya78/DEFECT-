"""
DefectGuard AI — model training script
Compares Logistic Regression, Random Forest, XGBoost on software defect dataset.
Selects best model by F1 score (recall-weighted), saves to disk.

BEFORE RUN: set CSV_PATH and TARGET_COL below (from dataset inspection step).
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)

# ── CONFIG — EDIT THESE ──────────────────────────────
CSV_PATH = "path/to/defect.csv"       # from os.walk output
TARGET_COL = "defects"                 # actual target column name, e.g. "Defective" / "bug" / "target"
# ──────────────────────────────────────────────────────

def load_and_prepare(csv_path, target_col):
    df = pd.read_csv(csv_path)
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Nulls:\n", df.isnull().sum())
    print("Duplicates:", df.duplicated().sum())

    df = df.drop_duplicates()
    df = df.dropna()  # simple strategy; swap for imputation if needed

    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found. Available: {list(df.columns)}")

    # binarize target if bool/text (true/false, yes/no, T/F)
    if df[target_col].dtype == object or df[target_col].dtype == bool:
        df[target_col] = df[target_col].astype(str).str.lower().map(
            {"true": 1, "false": 0, "yes": 1, "no": 0, "1": 1, "0": 0}
        ).fillna(df[target_col])

    print("Class distribution:\n", df[target_col].value_counts(normalize=True))

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)

    # keep numeric features only (extend later for categorical handling)
    X = X.select_dtypes(include=[np.number])

    return X, y


def train_and_evaluate(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "RandomForest": RandomForestClassifier(
            n_estimators=300, class_weight="balanced", random_state=42
        ),
        "XGBoost": XGBClassifier(
            n_estimators=300, eval_metric="logloss",
            scale_pos_weight=(y_train == 0).sum() / max((y_train == 1).sum(), 1),
            random_state=42
        ),
    }

    results = {}
    fitted = {}

    for name, model in models.items():
        Xtr = X_train_s if name == "LogisticRegression" else X_train
        Xte = X_test_s if name == "LogisticRegression" else X_test

        model.fit(Xtr, y_train)
        preds = model.predict(Xte)
        proba = model.predict_proba(Xte)[:, 1]

        metrics = {
            "accuracy": accuracy_score(y_test, preds),
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0),
            "f1": f1_score(y_test, preds, zero_division=0),
            "roc_auc": roc_auc_score(y_test, proba),
        }
        results[name] = metrics
        fitted[name] = model

        print(f"\n=== {name} ===")
        for k, v in metrics.items():
            print(f"{k}: {v:.4f}")
        print(confusion_matrix(y_test, preds))
        print(classification_report(y_test, preds, zero_division=0))

    best_name = max(results, key=lambda n: results[n]["f1"])
    print(f"\nBest model by F1: {best_name}")

    joblib.dump(fitted[best_name], "best_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(list(X.columns), "feature_columns.pkl")
    print("Saved: best_model.pkl, scaler.pkl, feature_columns.pkl")

    return results, fitted[best_name]


if __name__ == "__main__":
    X, y = load_and_prepare(CSV_PATH, TARGET_COL)
    train_and_evaluate(X, y)
