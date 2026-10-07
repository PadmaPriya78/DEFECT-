"""
DefectGuard AI
---------------
1. Downloads software-defect dataset from Kaggle
2. Inspects the dataset
3. Cleans the data
4. Automatically identifies/uses the target column
5. Trains:
      - Logistic Regression
      - Random Forest
      - XGBoost
6. Compares models
7. Selects the best model using F1 score
8. Saves the trained model and preprocessing files
"""

# ============================================================
# INSTALL DEPENDENCIES
# ============================================================
#
# pip install "kagglehub[pandas-datasets]"
# pip install pandas numpy scikit-learn xgboost joblib
#
# ============================================================

import pandas as pd
import numpy as np
import joblib
import kagglehub

from kagglehub import KaggleDatasetAdapter

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_NAME = "radowanulhaque/software-defect"

# Change this ONLY if inspection shows another target column.
TARGET_COL = "defects"


# ============================================================
# LOAD KAGGLE DATASET
# ============================================================

def load_dataset():

    print("\n==========================================")
    print("LOADING KAGGLE DATASET")
    print("==========================================")

    file_path = "jm1.csv"

    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        DATASET_NAME,
        file_path,
    )

    print("\nDataset loaded successfully!")

    return df


# ============================================================
# INSPECT DATASET
# ============================================================

def inspect_dataset(df):

    print("\n==========================================")
    print("DATASET INFORMATION")
    print("==========================================")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\n==========================================")
    print("UNIQUE VALUES")
    print("==========================================")

    for column in df.columns:

        print(f"\n{column}")
        print("Type:", df[column].dtype)
        print("Unique values:", df[column].nunique())

        values = df[column].dropna().unique()

        if len(values) > 10:
            print("Sample values:", values[:10])
        else:
            print("Values:", values)


# ============================================================
# PREPARE DATA
# ============================================================

def prepare_data(df):

    print("\n==========================================")
    print("PREPARING DATA")
    print("==========================================")

    # --------------------------------------------------------
    # Check target column
    # --------------------------------------------------------

    if TARGET_COL not in df.columns:

        raise ValueError(
            f"\nTarget column '{TARGET_COL}' was not found.\n\n"
            f"Available columns:\n{df.columns.tolist()}"
        )

    print("\nTarget column:", TARGET_COL)

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    duplicate_count = df.duplicated().sum()

    print(
        f"\nRemoving {duplicate_count} duplicate rows..."
    )

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # Convert target column
    # --------------------------------------------------------

    print("\nTarget values before conversion:")

    print(
        df[TARGET_COL].value_counts()
    )

    # Handle text / boolean targets

    if (
        df[TARGET_COL].dtype == object
        or df[TARGET_COL].dtype == bool
    ):

        df[TARGET_COL] = (
            df[TARGET_COL]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({
                "true": 1,
                "false": 0,
                "yes": 1,
                "no": 0,
                "1": 1,
                "0": 0,
                "t": 1,
                "f": 0
            })
        )

    # --------------------------------------------------------
    # Remove rows where target could not be converted
    # --------------------------------------------------------

    if df[TARGET_COL].isnull().any():

        print(
            "\nWarning: Some target values could not "
            "be converted to 0/1."
        )

        df = df.dropna(
            subset=[TARGET_COL]
        )

    # --------------------------------------------------------
    # Convert target to integer
    # --------------------------------------------------------

    df[TARGET_COL] = df[TARGET_COL].astype(int)

    # --------------------------------------------------------
    # Remove missing values
    # --------------------------------------------------------

    missing_before = df.isnull().sum().sum()

    print(
        f"\nMissing values before cleaning: "
        f"{missing_before}"
    )

    df = df.dropna()

    missing_after = df.isnull().sum().sum()

    print(
        f"Missing values after cleaning: "
        f"{missing_after}"
    )

    # --------------------------------------------------------
    # Class distribution
    # --------------------------------------------------------

    print("\n==========================================")
    print("CLASS DISTRIBUTION")
    print("==========================================")

    print(
        df[TARGET_COL].value_counts()
    )

    print("\nPercentage:")

    print(
        df[TARGET_COL]
        .value_counts(normalize=True)
        .mul(100)
        .round(2)
    )

    # --------------------------------------------------------
    # Separate X and y
    # --------------------------------------------------------

    X = df.drop(
        columns=[TARGET_COL]
    )

    y = df[TARGET_COL]

    # --------------------------------------------------------
    # Keep numeric columns
    # --------------------------------------------------------

    numeric_columns = X.select_dtypes(
        include=[np.number]
    ).columns

    X = X[numeric_columns]

    print("\n==========================================")
    print("FEATURE INFORMATION")
    print("==========================================")

    print(
        "Number of features:",
        X.shape[1]
    )

    print("\nFeatures:")

    for column in X.columns:
        print("-", column)

    return X, y


# ============================================================
# TRAIN MODELS
# ============================================================

def train_and_evaluate(X, y):

    print("\n==========================================")
    print("TRAINING MODELS")
    print("==========================================")

    # --------------------------------------------------------
    # Train/Test split
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nTraining samples:", len(X_train))
    print("Testing samples :", len(X_test))

    # --------------------------------------------------------
    # Scaling
    # --------------------------------------------------------

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    # --------------------------------------------------------
    # XGBoost class imbalance
    # --------------------------------------------------------

    negative_count = (y_train == 0).sum()

    positive_count = (y_train == 1).sum()

    scale_pos_weight = (
        negative_count /
        max(positive_count, 1)
    )

    print(
        "\nXGBoost scale_pos_weight:",
        round(scale_pos_weight, 4)
    )

    # --------------------------------------------------------
    # Models
    # --------------------------------------------------------

    models = {

        "LogisticRegression":

            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            ),

        "RandomForest":

            RandomForestClassifier(
                n_estimators=300,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            ),

        "XGBoost":

            XGBClassifier(
                n_estimators=300,
                eval_metric="logloss",
                scale_pos_weight=scale_pos_weight,
                random_state=42,
                n_jobs=-1
            )
    }

    results = {}

    fitted_models = {}

    # ========================================================
    # TRAIN EACH MODEL
    # ========================================================

    for name, model in models.items():

        print("\n")
        print("==========================================")
        print("MODEL:", name)
        print("==========================================")

        # Logistic Regression needs scaled data

        if name == "LogisticRegression":

            Xtr = X_train_scaled
            Xte = X_test_scaled

        else:

            Xtr = X_train
            Xte = X_test

        # ----------------------------------------------------
        # Train
        # ----------------------------------------------------

        model.fit(
            Xtr,
            y_train
        )

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        predictions = model.predict(
            Xte
        )

        probabilities = model.predict_proba(
            Xte
        )[:, 1]

        # ----------------------------------------------------
        # Metrics
        # ----------------------------------------------------

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        try:

            roc_auc = roc_auc_score(
                y_test,
                probabilities
            )

        except ValueError:

            roc_auc = 0.0

        metrics = {

            "accuracy": accuracy,

            "precision": precision,

            "recall": recall,

            "f1": f1,

            "roc_auc": roc_auc
        }

        results[name] = metrics

        fitted_models[name] = model

        # ----------------------------------------------------
        # Print results
        # ----------------------------------------------------

        print("\nMetrics:")

        for metric, value in metrics.items():

            print(
                f"{metric:<10}: {value:.4f}"
            )

        # ----------------------------------------------------
        # Confusion Matrix
        # ----------------------------------------------------

        print("\nConfusion Matrix:")

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        # ----------------------------------------------------
        # Classification Report
        # ----------------------------------------------------

        print("\nClassification Report:")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

    # ========================================================
    # MODEL COMPARISON
    # ========================================================

    print("\n")
    print("==========================================")
    print("MODEL COMPARISON")
    print("==========================================")

    results_df = pd.DataFrame(
        results
    ).T

    print(
        results_df.round(4)
    )

    # ========================================================
    # SELECT BEST MODEL
    # ========================================================

    best_name = max(
        results,
        key=lambda name:
        results[name]["f1"]
    )

    best_model = fitted_models[
        best_name
    ]

    print("\n==========================================")
    print("BEST MODEL")
    print("==========================================")

    print(
        "Best model:",
        best_name
    )

    print(
        "F1 Score:",
        f"{results[best_name]['f1']:.4f}"
    )

    print(
        "Recall:",
        f"{results[best_name]['recall']:.4f}"
    )

    print(
        "Precision:",
        f"{results[best_name]['precision']:.4f}"
    )

    # ========================================================
    # SAVE MODEL
    # ========================================================

    joblib.dump(
        best_model,
        "best_model.pkl"
    )

    joblib.dump(
        scaler,
        "scaler.pkl"
    )

    joblib.dump(
        list(X.columns),
        "feature_columns.pkl"
    )

    results_df.to_csv(
        "model_results.csv"
    )

    # ========================================================
    # SAVE DATASET
    # ========================================================

    df_path = "processed_defect_dataset.csv"

    processed_df = pd.concat(
        [X, y],
        axis=1
    )

    processed_df.to_csv(
        df_path,
        index=False
    )

    # ========================================================
    # FINAL OUTPUT
    # ========================================================

    print("\n==========================================")
    print("FILES CREATED")
    print("==========================================")

    print("✓ best_model.pkl")
    print("✓ scaler.pkl")
    print("✓ feature_columns.pkl")
    print("✓ model_results.csv")
    print("✓ processed_defect_dataset.csv")

    return (
        results,
        best_model,
        scaler
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("==========================================")
    print("        DefectGuard AI")
    print(" Software Defect Prediction System")
    print("==========================================")

    # --------------------------------------------------------
    # Step 1: Load dataset from Kaggle
    # --------------------------------------------------------

    df = load_dataset()

    # --------------------------------------------------------
    # Step 2: Inspect dataset
    # --------------------------------------------------------

    inspect_dataset(df)

    # --------------------------------------------------------
    # Step 3: Prepare dataset
    # --------------------------------------------------------

    X, y = prepare_data(df)

    # --------------------------------------------------------
    # Step 4: Train and evaluate
    # --------------------------------------------------------

    results, best_model, scaler = train_and_evaluate(
        X,
        y
    )

    print("\n")
    print("==========================================")
    print("TRAINING COMPLETED SUCCESSFULLY")
    print("==========================================")
