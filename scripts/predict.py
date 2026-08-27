"""AQI Prediction System."""

from pathlib import Path
import json
import joblib
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model_registry" / "v1" / "best_model.pkl"
FEATURE_PATH = BASE_DIR / "feature_store" / "features_v1.csv"

PREDICTION_DIR = BASE_DIR / "predictions"

PREDICTION_FILE = PREDICTION_DIR / "predictions.csv"
SUMMARY_FILE = PREDICTION_DIR / "prediction_summary.json"


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
    "AQI_Lag_3",
]


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading registered model...")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")
print(f"Model type: {type(model).__name__}")


# ============================================================
# LOAD FEATURES
# ============================================================

print("\nLoading feature dataset...")

if not FEATURE_PATH.exists():
    raise FileNotFoundError(
        f"Feature dataset not found: {FEATURE_PATH}"
    )

df = pd.read_csv(FEATURE_PATH)

print("Feature dataset loaded successfully.")
print(f"Dataset Shape: {df.shape}")


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

print("\n========== FEATURE VALIDATION ==========")

missing_columns = [
    col for col in FEATURE_COLUMNS
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required features: {missing_columns}"
    )

print("All required features are available.")


# ============================================================
# SORT DATA
# ============================================================

if "Timestamp" in df.columns:

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df = df.sort_values("Timestamp").reset_index(drop=True)

print("Dataset sorted chronologically.")


# ============================================================
# CHECK MISSING VALUES
# ============================================================

print("\n========== MISSING VALUE CHECK ==========")

missing_values = df[FEATURE_COLUMNS].isnull().sum()

if missing_values.sum() > 0:

    print(missing_values[missing_values > 0])

    raise ValueError(
        "Missing values detected in prediction features."
    )

print("No missing values found.")


# ============================================================
# SELECT LATEST 3 RECORDS
# ============================================================

print("\n========== GENERATING PREDICTIONS ==========")

latest_data = df.tail(3).copy()

X_prediction = latest_data[FEATURE_COLUMNS]


# ============================================================
# GENERATE PREDICTIONS
# ============================================================

predictions = model.predict(X_prediction)


# ============================================================
# CREATE OUTPUT
# ============================================================

prediction_output = pd.DataFrame()

if "Timestamp" in latest_data.columns:

    prediction_output["Timestamp"] = (
        latest_data["Timestamp"].values
    )

prediction_output["Predicted_AQI"] = predictions


# ============================================================
# SAVE PREDICTIONS
# ============================================================

PREDICTION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

prediction_output.to_csv(
    PREDICTION_FILE,
    index=False
)

print("\nPredictions saved to:")
print(PREDICTION_FILE)


# ============================================================
# CREATE SUMMARY
# ============================================================

summary = {
    "model_version": "v1",
    "model_type": type(model).__name__,
    "prediction_records": len(prediction_output),
    "features_used": FEATURE_COLUMNS,
    "prediction_file": str(PREDICTION_FILE),
}


with open(
    SUMMARY_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        summary,
        file,
        indent=4
    )


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========== PREDICTIONS ==========")

print(prediction_output.to_string(index=False))

print("\nPrediction summary saved to:")
print(SUMMARY_FILE)

print("\n=======================================================")
print("PHASE 11A COMPLETED SUCCESSFULLY!")
print("=======================================================")