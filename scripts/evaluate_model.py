"""
Phase 9 - Model Evaluation
Evaluates the best trained AQI prediction model.
"""

import json
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. FILE PATHS
# ============================================================

FEATURE_FILE = "feature_store/features_v1.csv"
MODEL_FILE = "models/best_model.pkl"
METADATA_FILE = "models/model_metadata.json"

REPORT_DIR = "reports"
CHART_DIR = os.path.join(REPORT_DIR, "evaluation_charts")
REPORT_FILE = os.path.join(REPORT_DIR, "evaluation_report.md")

os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# 2. REQUIRED FEATURES
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

TARGET_COLUMN = "AQI"


# ============================================================
# 3. LOAD DATA
# ============================================================

print("\nLoading feature dataset...")

df = pd.read_csv(FEATURE_FILE)

print("Dataset loaded successfully.")
print(f"Dataset Shape: {df.shape}")


# ============================================================
# 4. SORT CHRONOLOGICALLY
# ============================================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce",
    utc=True
)

df = df.sort_values("Timestamp").reset_index(drop=True)

print("Dataset sorted chronologically.")


# ============================================================
# 5. VALIDATE COLUMNS
# ============================================================

print("\n========== COLUMN VALIDATION ==========")

required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("All required columns are available.")


# ============================================================
# 6. REMOVE MISSING VALUES
# ============================================================

df = df.dropna(
    subset=FEATURE_COLUMNS + [TARGET_COLUMN]
).reset_index(drop=True)

print(f"Rows after cleaning: {len(df)}")


# ============================================================
# 7. FEATURES AND TARGET
# ============================================================

X = df[FEATURE_COLUMNS]
y = df[TARGET_COLUMN]


# ============================================================
# 8. SAME CHRONOLOGICAL 80/20 TEST SPLIT
# ============================================================

split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\n========== TEST DATA ==========")

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

print("\nTest period:")
print(f"From: {df.iloc[split_index]['Timestamp']}")
print(f"To  : {df.iloc[-1]['Timestamp']}")


# ============================================================
# 9. LOAD BEST MODEL
# ============================================================

print("\nLoading best model...")

model = joblib.load(MODEL_FILE)

print("Best model loaded successfully.")
print(f"Model type: {type(model).__name__}")


# ============================================================
# 10. GENERATE PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

predictions = model.predict(X_test)

print("Predictions generated successfully.")


# ============================================================
# 11. EVALUATION METRICS
# ============================================================

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

mae = mean_absolute_error(y_test, predictions)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

r2 = r2_score(y_test, predictions)


print("\n========== EVALUATION METRICS ==========")

print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2  : {r2:.4f}")


# ============================================================
# 12. ERROR ANALYSIS
# ============================================================

errors = y_test.values - predictions

absolute_errors = np.abs(errors)

max_error = absolute_errors.max()
mean_error = absolute_errors.mean()

max_error_index = absolute_errors.argmax()

high_error_threshold = np.percentile(
    absolute_errors,
    95
)

high_error_count = np.sum(
    absolute_errors >= high_error_threshold
)


print("\n========== ERROR ANALYSIS ==========")

print(f"Mean Absolute Error : {mean_error:.4f}")
print(f"Maximum Error       : {max_error:.4f}")
print(
    f"95th Percentile Error: "
    f"{high_error_threshold:.4f}"
)

print(
    f"High-error observations: "
    f"{high_error_count}"
)


# ============================================================
# 13. ACTUAL VS PREDICTED DATAFRAME
# ============================================================

results = pd.DataFrame({
    "Timestamp": df.iloc[split_index:]["Timestamp"].values,
    "Actual_AQI": y_test.values,
    "Predicted_AQI": predictions,
    "Error": errors,
    "Absolute_Error": absolute_errors
})

results = results.sort_values(
    "Absolute_Error",
    ascending=False
)

print("\n========== HIGHEST ERROR OBSERVATIONS ==========")

print(
    results.head(10).to_string(index=False)
)


# ============================================================
# 14. ACTUAL VS PREDICTED PLOT
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    y_test.values,
    label="Actual AQI"
)

plt.plot(
    predictions,
    label="Predicted AQI"
)

plt.title("Actual vs Predicted AQI")

plt.xlabel("Test Sample")

plt.ylabel("AQI")

plt.legend()

plt.tight_layout()

actual_predicted_path = os.path.join(
    CHART_DIR,
    "actual_vs_predicted.png"
)

plt.savefig(actual_predicted_path)

plt.close()

print(
    "\nActual vs Predicted chart saved."
)


# ============================================================
# 15. RESIDUAL PLOT
# ============================================================

plt.figure(figsize=(10, 6))

plt.scatter(
    predictions,
    errors,
    alpha=0.6
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.title("Residual Plot")

plt.xlabel("Predicted AQI")

plt.ylabel("Residual")

plt.tight_layout()

residual_path = os.path.join(
    CHART_DIR,
    "residual_plot.png"
)

plt.savefig(residual_path)

plt.close()

print("Residual plot saved.")


# ============================================================
# 16. FEATURE IMPORTANCE
# ============================================================

feature_importance_path = None

if hasattr(model, "feature_importances_"):

    importance = model.feature_importances_

    importance_df = pd.DataFrame({
        "Feature": FEATURE_COLUMNS,
        "Importance": importance
    })

    importance_df = importance_df.sort_values(
        "Importance",
        ascending=True
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    plt.title("Random Forest Feature Importance")

    plt.xlabel("Importance")

    plt.ylabel("Feature")

    plt.tight_layout()

    feature_importance_path = os.path.join(
        CHART_DIR,
        "feature_importance.png"
    )

    plt.savefig(feature_importance_path)

    plt.close()

    print("Feature importance chart saved.")


# ============================================================
# 17. SAVE EVALUATION REPORT
# ============================================================

top_features_text = ""

if hasattr(model, "feature_importances_"):

    top_features = (
        importance_df
        .sort_values("Importance", ascending=False)
        .head(5)
    )

    for _, row in top_features.iterrows():

        top_features_text += (
            f"- **{row['Feature']}**: "
            f"{row['Importance']:.4f}\n"
        )


report = f"""# Phase 9 — Model Evaluation Report

## 1. Model Information

- Model: `{type(model).__name__}`
- Dataset: `features_v1.csv`
- Total Samples: {len(df)}
- Training Samples: {len(X_train)}
- Testing Samples: {len(X_test)}

## 2. Evaluation Metrics

| Metric | Value |
|---|---:|
| MAE | {mae:.4f} |
| RMSE | {rmse:.4f} |
| R² | {r2:.4f} |

## 3. Error Analysis

- Mean Absolute Error: **{mean_error:.4f}**
- Maximum Error: **{max_error:.4f}**
- 95th Percentile Error: **{high_error_threshold:.4f}**
- High-error observations: **{high_error_count}**

## 4. Test Period

- Start: `{df.iloc[split_index]['Timestamp']}`
- End: `{df.iloc[-1]['Timestamp']}`

## 5. Feature Importance

{top_features_text}

## 6. Generated Charts

- `evaluation_charts/actual_vs_predicted.png`
- `evaluation_charts/residual_plot.png`
- `evaluation_charts/feature_importance.png`

## 7. Conclusion

The trained model was evaluated on the final 20% of the chronological dataset.

The evaluation uses MAE, RMSE and R² to measure prediction performance.

Because this project uses time-series data, the evaluation was performed without random shuffling.

The model's performance should be interpreted in the context of the OpenWeather AQI index used in the dataset.
"""


with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(report)


print("\nEvaluation report saved:")
print(REPORT_FILE)


# ============================================================
# 18. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 55)

print("PHASE 9 COMPLETED SUCCESSFULLY!")

print("=" * 55)

print("\nGenerated files:")

print("1. reports/evaluation_report.md")

print(
    "2. reports/evaluation_charts/"
    "actual_vs_predicted.png"
)

print(
    "3. reports/evaluation_charts/"
    "residual_plot.png"
)

if feature_importance_path:

    print(
        "4. reports/evaluation_charts/"
        "feature_importance.png"
    )

print("\nModel evaluation is ready.")