from fastapi import FastAPI, HTTPException
from pathlib import Path
from datetime import datetime
import json
import pandas as pd


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="AQI Predictor API",
    description=(
        "Production-style REST API for the Karachi AQI "
        "Forecasting System."
    ),
    version="1.0.0",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTION_FILE = (
    BASE_DIR
    / "predictions"
    / "predictions.csv"
)

REGISTRY_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "registry.json"
)

METRICS_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "metrics.json"
)

METADATA_FILE = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "metadata.json"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_json(file_path: Path):

    if not file_path.exists():
        return {}

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def load_predictions():

    if not PREDICTION_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="Prediction file not found."
        )

    try:

        df = pd.read_csv(
            PREDICTION_FILE
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load prediction data: {e}"
        )

    required_columns = [
        "Timestamp",
        "Predicted_AQI"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Missing prediction columns: "
                f"{missing_columns}"
            )
        )

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    df["Predicted_AQI"] = pd.to_numeric(
        df["Predicted_AQI"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Timestamp",
            "Predicted_AQI"
        ]
    )

    df = df.sort_values(
        "Timestamp"
    ).reset_index(
        drop=True
    )

    if df.empty:

        raise HTTPException(
            status_code=404,
            detail="No valid prediction data available."
        )

    return df


def get_aqi_category(aqi: float):

    if aqi < 1.5:
        return "Good"

    elif aqi < 2.5:
        return "Fair"

    elif aqi < 3.5:
        return "Moderate"

    elif aqi < 4.5:
        return "Poor"

    else:
        return "Very Poor"


def get_health_advisory(category: str):

    advisories = {

        "Good":
            "Air quality is good. "
            "Outdoor activities are generally safe.",

        "Fair":
            "Air quality is acceptable for most people.",

        "Moderate":
            "Sensitive individuals should consider "
            "reducing prolonged outdoor exposure.",

        "Poor":
            "Consider limiting prolonged outdoor activities.",

        "Very Poor":
            "Avoid prolonged outdoor exposure and "
            "take appropriate precautions."
    }

    return advisories.get(
        category,
        "No health advisory available."
    )


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def home():

    return {

        "name": "AQI Predictor API",

        "description":
            "Air Quality Forecasting System",

        "version": "1.0.0",

        "status": "online",

        "location": "Karachi",

        "documentation": "/docs"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    prediction_available = (
        PREDICTION_FILE.exists()
    )

    registry_available = (
        REGISTRY_FILE.exists()
    )

    return {

        "status": "healthy",

        "service":
            "AQI Predictor API",

        "prediction_data":
            "available"
            if prediction_available
            else "missing",

        "model_registry":
            "available"
            if registry_available
            else "missing",

        "timestamp":
            datetime.now().isoformat()
    }


# ============================================================
# LATEST PREDICTION
# ============================================================

@app.get("/latest")
def latest_prediction():

    df = load_predictions()

    latest = df.iloc[-1]

    aqi = float(
        latest["Predicted_AQI"]
    )

    category = get_aqi_category(
        aqi
    )

    return {

        "city": "Karachi",

        "timestamp":
            latest["Timestamp"].isoformat(),

        "predicted_aqi":
            round(aqi, 3),

        "category":
            category,

        "health_advisory":
            get_health_advisory(category)
    }


# ============================================================
# 72-HOUR FORECAST
# ============================================================

@app.get("/forecast")
def forecast():

    df = load_predictions()

    forecast_data = []

    for _, row in df.iterrows():

        aqi = float(
            row["Predicted_AQI"]
        )

        category = get_aqi_category(
            aqi
        )

        forecast_data.append({

            "timestamp":
                row["Timestamp"].isoformat(),

            "predicted_aqi":
                round(aqi, 3),

            "category":
                category
        })

    return {

        "city": "Karachi",

        "forecast_horizon_hours":
            len(forecast_data),

        "forecast": forecast_data
    }


# ============================================================
# PREDICTION HISTORY
# ============================================================

@app.get("/history")
def prediction_history():

    df = load_predictions()

    history = []

    for _, row in df.iterrows():

        aqi = float(
            row["Predicted_AQI"]
        )

        history.append({

            "timestamp":
                row["Timestamp"].isoformat(),

            "predicted_aqi":
                round(aqi, 3),

            "category":
                get_aqi_category(aqi)
        })

    return {

        "city": "Karachi",

        "total_predictions":
            len(history),

        "history": history
    }


# ============================================================
# MODEL INFORMATION
# ============================================================

@app.get("/model")
def model_information():

    registry = load_json(
        REGISTRY_FILE
    )

    metadata = load_json(
        METADATA_FILE
    )

    return {

        "model":
            registry.get(
                "current_best_model",
                "Unknown"
            ),

        "model_type":
            registry.get(
                "model_type",
                "Unknown"
            ),

        "version":
            registry.get(
                "model_version",
                "Unknown"
            ),

        "status":
            registry.get(
                "status",
                "Unknown"
            ),

        "metadata":
            metadata
    }


# ============================================================
# MODEL METRICS
# ============================================================

@app.get("/metrics")
def model_metrics():

    metrics = load_json(
        METRICS_FILE
    )

    if not metrics:

        raise HTTPException(
            status_code=404,
            detail="Model metrics not found."
        )

    return {

        "model_version": "v1",

        "metrics": metrics
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/info")
def api_information():

    return {

        "project":
            "AQI Forecasting System",

        "location":
            "Karachi",

        "forecast_horizon":
            "72 hours",

        "machine_learning":
            True,

        "explainable_ai":
            True,

        "model_registry":
            True,

        "prediction_history":
            True,

        "api_version":
            "1.0.0"
    }