import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "best_model.pkl"
)

FEATURE_FILE = (
    BASE_DIR
    / "feature_store"
    / "features_v1.csv"
)

REPORT_DIR = BASE_DIR / "reports"

XAI_DIR = (
    REPORT_DIR
    / "explainability"
)

XAI_DIR.mkdir(
    parents=True,
    exist_ok=True
)

XAI_REPORT = REPORT_DIR / "xai_report.md"


# ============================================================
# FEATURES USED DURING TRAINING
# ============================================================

FEATURE_COLUMNS = [
    "Temperature",
    "Humidity",
    "Pressure",
    "Wind_Speed",
    "PM2.5",
    "PM10",
    "CO",
    "NO2",
    "SO2",
    "O3",
    "NH3",
    "Hour",
    "Day",
    "Month",
    "Weekday",
    "AQI_Lag_1",
    "AQI_Lag_2",
    "AQI_Lag_3"
]


# ============================================================
# STEP 1 — LOAD REGISTERED MODEL
# ============================================================

print("=" * 55)
print("PHASE 13 — EXPLAINABLE AI")
print("=" * 55)

print("\n========== LOADING REGISTERED MODEL ==========")

if not MODEL_FILE.exists():

    print("ERROR: Registered model not found.")
    print(f"Expected path: {MODEL_FILE}")

    sys.exit(1)


try:

    model = joblib.load(MODEL_FILE)

except Exception as e:

    print(f"ERROR loading model: {e}")

    sys.exit(1)


print("Registered model loaded successfully.")
print(f"Model type: {type(model).__name__}")


# ============================================================
# STEP 2 — LOAD FEATURE DATASET
# ============================================================

print("\n========== LOADING FEATURE DATASET ==========")

if not FEATURE_FILE.exists():

    print("ERROR: Feature dataset not found.")
    print(f"Expected path: {FEATURE_FILE}")

    sys.exit(1)


try:

    df = pd.read_csv(FEATURE_FILE)

except Exception as e:

    print(f"ERROR loading feature dataset: {e}")

    sys.exit(1)


print("Feature dataset loaded successfully.")
print(f"Dataset Shape: {df.shape}")


# ============================================================
# STEP 3 — VALIDATE FEATURES
# ============================================================

print("\n========== FEATURE VALIDATION ==========")

missing_features = [
    feature
    for feature in FEATURE_COLUMNS
    if feature not in df.columns
]

if missing_features:

    print("ERROR: Missing features:")

    for feature in missing_features:
        print(f"- {feature}")

    sys.exit(1)


print("All training features are available.")


# ============================================================
# STEP 4 — PREPARE DATA
# ============================================================

X = df[FEATURE_COLUMNS].copy()

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

missing_before = X.isna().sum().sum()

if missing_before > 0:

    print(
        f"Missing values found: {missing_before}"
    )

    X = X.fillna(
        X.median()
    )

else:

    print("No missing values found.")


print(f"Final explanation dataset shape: {X.shape}")


# ============================================================
# STEP 5 — DETECT MODEL TYPE
# ============================================================

print("\n========== MODEL DETECTION ==========")

model_type = type(model).__name__

print(f"Detected model: {model_type}")


# ============================================================
# STEP 6 — RANDOM FOREST / TREE MODEL
# ============================================================

if hasattr(model, "feature_importances_"):

    print(
        "\nTree-based model detected."
    )

    print(
        "Using SHAP TreeExplainer..."
    )

    try:

        explainer = shap.TreeExplainer(model)

        shap_result = explainer(X)

    except Exception as e:

        print(
            f"ERROR generating SHAP values: {e}"
        )

        sys.exit(1)


    # ========================================================
    # HANDLE SHAP VALUE FORMAT
    # ========================================================

    if hasattr(shap_result, "values"):

        shap_values = shap_result.values

        base_values = shap_result.base_values

    else:

        shap_values = shap_result

        base_values = explainer.expected_value


    # ========================================================
    # STEP 7 — SHAP SUMMARY PLOT
    # ========================================================

    print(
        "\n========== SHAP SUMMARY =========="
    )

    summary_file = (
        XAI_DIR
        / "shap_summary.png"
    )

    plt.figure(
        figsize=(10, 7)
    )

    shap.summary_plot(
        shap_values,
        X,
        show=False
    )

    plt.title(
        "SHAP Summary — AQI Prediction Model"
    )

    plt.tight_layout()

    plt.savefig(
        summary_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"SHAP summary saved to:\n{summary_file}"
    )


    # ========================================================
    # STEP 8 — SHAP WATERFALL PLOT
    # ========================================================

    print(
        "\n========== SHAP WATERFALL =========="
    )

    waterfall_file = (
        XAI_DIR
        / "shap_waterfall.png"
    )

    # Select first observation
    sample_index = 0

    sample_values = shap_values[
        sample_index
    ]

    if np.ndim(base_values) == 0:

        base_value = base_values

    else:

        base_value = base_values[
            sample_index
        ]


    explanation = shap.Explanation(
        values=sample_values,
        base_values=base_value,
        data=X.iloc[
            sample_index
        ].values,
        feature_names=FEATURE_COLUMNS
    )

    plt.figure(
        figsize=(10, 8)
    )

    shap.plots.waterfall(
        explanation,
        show=False,
        max_display=18
    )

    plt.title(
        "SHAP Waterfall — Individual AQI Prediction"
    )

    plt.tight_layout()

    plt.savefig(
        waterfall_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"SHAP waterfall saved to:\n{waterfall_file}"
    )


    # ========================================================
    # STEP 9 — FEATURE IMPORTANCE
    # ========================================================

    print(
        "\n========== FEATURE IMPORTANCE =========="
    )

    importance_file = (
        XAI_DIR
        / "feature_importance.png"
    )


    importance_df = pd.DataFrame({

        "Feature": FEATURE_COLUMNS,

        "Importance":
            model.feature_importances_

    })

    importance_df = (
        importance_df
        .sort_values(
            "Importance",
            ascending=True
        )
    )


    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    plt.xlabel(
        "Feature Importance"
    )

    plt.ylabel(
        "Feature"
    )

    plt.title(
        "Random Forest Feature Importance"
    )

    plt.tight_layout()

    plt.savefig(
        importance_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    print(
        f"Feature importance saved to:\n"
        f"{importance_file}"
    )


    # ========================================================
    # STEP 10 — TOP FEATURES
    # ========================================================

    top_features = (
        importance_df
        .sort_values(
            "Importance",
            ascending=False
        )
        .head(10)
    )


    print(
        "\n========== TOP FEATURES =========="
    )

    for _, row in top_features.iterrows():

        print(
            f"{row['Feature']}: "
            f"{row['Importance']:.6f}"
        )


    # ========================================================
    # STEP 11 — GENERATE REPORT
    # ========================================================

    print(
        "\n========== GENERATING XAI REPORT =========="
    )


    report_lines = [

        "# Explainable AI Report",

        "",

        "## Model Information",

        "",

        f"- **Model:** {model_type}",

        "- **Model Version:** v1",

        "- **Explanation Method:** SHAP TreeExplainer",

        "- **Model Type:** Tree-based Random Forest",

        f"- **Number of Features:** {len(FEATURE_COLUMNS)}",

        f"- **Explanation Dataset Size:** {len(X)} rows",

        "",

        "## Explainability Methods",

        "",

        "### SHAP Summary Plot",

        "",

        "The SHAP summary plot shows the global "
        "importance and impact of features across "
        "the dataset.",

        "",

        "### SHAP Waterfall Plot",

        "",

        "The SHAP waterfall plot explains how individual "
        "features contributed to one specific AQI prediction.",

        "",

        "### Random Forest Feature Importance",

        "",

        "The feature importance chart shows the relative "
        "importance of each feature used by the Random "
        "Forest model.",

        "",

        "## Top Features",

        ""

    ]


    for _, row in top_features.iterrows():

        report_lines.append(
            f"- **{row['Feature']}**: "
            f"{row['Importance']:.6f}"
        )


    report_lines.extend([

        "",

        "## Generated Files",

        "",

        "- `explainability/shap_summary.png`",

        "- `explainability/shap_waterfall.png`",

        "- `explainability/feature_importance.png`",

        "",

        "## Conclusion",

        "",

        "The Explainable AI analysis provides both "
        "global and local explanations of the AQI "
        "forecasting model. SHAP identifies how "
        "individual features influence predictions, "
        "while Random Forest feature importance "
        "provides an overall ranking of feature influence.",

        "",

        "The explanations are generated directly from "
        "the registered production model (v1), ensuring "
        "that the XAI results correspond to the model "
        "used by the forecasting system."

    ])


    with open(
        XAI_REPORT,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report_lines)
        )


    print(
        f"XAI report saved to:\n{XAI_REPORT}"
    )


else:

    print(
        "\nThis model does not expose "
        "tree-based feature_importances_."
    )

    print(
        "Linear-model coefficient analysis "
        "should be implemented for this model."
    )


# ============================================================
# FINAL VERIFICATION
# ============================================================

print(
    "\n========== XAI VERIFICATION =========="
)


expected_files = [

    XAI_REPORT,

    XAI_DIR
    / "shap_summary.png",

    XAI_DIR
    / "shap_waterfall.png",

    XAI_DIR
    / "feature_importance.png"

]


all_files_exist = True


for file_path in expected_files:

    if file_path.exists():

        print(
            f"✓ {file_path.relative_to(BASE_DIR)}"
        )

    else:

        print(
            f"✗ Missing: "
            f"{file_path.relative_to(BASE_DIR)}"
        )

        all_files_exist = False


if all_files_exist:

    print(
        "\n======================================================="
    )

    print(
        "PHASE 13 COMPLETED SUCCESSFULLY!"
    )

    print(
        "======================================================="

    )

else:

    print(
        "\nPhase 13 completed with missing outputs."
    )