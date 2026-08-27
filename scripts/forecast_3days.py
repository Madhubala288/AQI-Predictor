"""Real 3-Day AQI Forecasting using OpenWeather Forecast APIs."""

import os
import json
from pathlib import Path
from datetime import datetime, timezone

import requests
import joblib
import pandas as pd
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model_registry"
    / "v1"
    / "best_model.pkl"
)

FEATURE_PATH = (
    BASE_DIR
    / "feature_store"
    / "features_v1.csv"
)

PREDICTION_DIR = BASE_DIR / "predictions"

PREDICTION_FILE = (
    PREDICTION_DIR / "predictions.csv"
)

SUMMARY_FILE = (
    PREDICTION_DIR / "prediction_summary.json"
)


# ============================================================
# OPENWEATHER SETTINGS
# ============================================================

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY not found in .env file."
    )

# Karachi coordinates
LAT = 24.8607
LON = 67.0011


# ============================================================
# MODEL FEATURES
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

print("\n========== LOADING MODEL ==========")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)

print("Registered model loaded successfully.")
print(f"Model type: {type(model).__name__}")


# ============================================================
# WEATHER FORECAST API
# ============================================================

print("\n========== WEATHER FORECAST ==========")

weather_url = (
    "https://api.openweathermap.org/data/2.5/forecast"
)

weather_params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
    "units": "metric",
}

weather_response = requests.get(
    weather_url,
    params=weather_params,
    timeout=30,
)

print("Weather API Status:", weather_response.status_code)

if weather_response.status_code != 200:
    raise RuntimeError(
        f"Weather API failed: {weather_response.text}"
    )

weather_data = weather_response.json()

weather_rows = []

for item in weather_data["list"]:

    timestamp = pd.to_datetime(
        item["dt"],
        unit="s",
        utc=True
    )

    weather_rows.append(
        {
            "Timestamp": timestamp,
            "Temperature": item["main"]["temp"],
            "Humidity": item["main"]["humidity"],
            "Pressure": item["main"]["pressure"],
            "Wind_Speed": item["wind"]["speed"],
        }
    )

weather_df = pd.DataFrame(weather_rows)

print(
    f"Weather records received: {len(weather_df)}"
)


# ============================================================
# AIR POLLUTION FORECAST API
# ============================================================

print("\n========== AIR POLLUTION FORECAST ==========")

pollution_url = (
    "https://api.openweathermap.org/data/2.5/"
    "air_pollution/forecast"
)

pollution_params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY,
}

pollution_response = requests.get(
    pollution_url,
    params=pollution_params,
    timeout=30,
)

print(
    "Pollution API Status:",
    pollution_response.status_code
)

if pollution_response.status_code != 200:
    raise RuntimeError(
        f"Pollution API failed: {pollution_response.text}"
    )

pollution_data = pollution_response.json()

pollution_rows = []

for item in pollution_data["list"]:

    timestamp = pd.to_datetime(
        item["dt"],
        unit="s",
        utc=True
    )

    components = item["components"]

    pollution_rows.append(
        {
            "Timestamp": timestamp,
            "PM2.5": components["pm2_5"],
            "PM10": components["pm10"],
            "CO": components["co"],
            "NO2": components["no2"],
            "SO2": components["so2"],
            "O3": components["o3"],
            "NH3": components["nh3"],
        }
    )

pollution_df = pd.DataFrame(pollution_rows)

print(
    f"Pollution records received: {len(pollution_df)}"
)


# ============================================================
# ALIGN WEATHER AND POLLUTION
# ============================================================

print("\n========== ALIGNING FORECAST DATA ==========")

weather_df = weather_df.sort_values("Timestamp")
pollution_df = pollution_df.sort_values("Timestamp")

# Convert weather 3-hour forecast into hourly values
weather_df = (
    weather_df
    .set_index("Timestamp")
    .resample("1h")
    .interpolate(method="linear")
    .reset_index()
)

# Merge using nearest timestamp
future_df = pd.merge_asof(
    pollution_df.sort_values("Timestamp"),
    weather_df.sort_values("Timestamp"),
    on="Timestamp",
    direction="nearest",
)

print(
    f"Combined forecast records: {len(future_df)}"
)


# ============================================================
# KEEP NEXT 72 HOURS
# ============================================================

future_df = future_df.head(72).copy()

print(
    f"Using forecast records: {len(future_df)}"
)


# ============================================================
# TIME FEATURES
# ============================================================

future_df["Hour"] = future_df["Timestamp"].dt.hour
future_df["Day"] = future_df["Timestamp"].dt.day
future_df["Month"] = future_df["Timestamp"].dt.month
future_df["Weekday"] = future_df["Timestamp"].dt.weekday


# ============================================================
# LOAD HISTORICAL AQI
# ============================================================

print("\n========== LOADING HISTORICAL AQI ==========")

if not FEATURE_PATH.exists():
    raise FileNotFoundError(
        f"Feature dataset not found: {FEATURE_PATH}"
    )

historical_df = pd.read_csv(FEATURE_PATH)

historical_df["Timestamp"] = pd.to_datetime(
    historical_df["Timestamp"],
    utc=True,
    errors="coerce"
)

historical_df = historical_df.sort_values(
    "Timestamp"
).reset_index(drop=True)

historical_aqi = historical_df["AQI"].dropna().tolist()

if len(historical_aqi) < 3:
    raise ValueError(
        "At least 3 historical AQI values are required."
    )

# Last three known AQI values
lag_values = historical_aqi[-3:]

print("Initial AQI lag values:")
print(f"Lag 3: {lag_values[0]}")
print(f"Lag 2: {lag_values[1]}")
print(f"Lag 1: {lag_values[2]}")


# ============================================================
# RECURSIVE AQI FORECAST
# ============================================================

print("\n========== GENERATING 72-HOUR AQI FORECAST ==========")

predictions = []

for _, row in future_df.iterrows():

    row_data = row.copy()

    # Recursive lag features
    row_data["AQI_Lag_1"] = lag_values[-1]
    row_data["AQI_Lag_2"] = lag_values[-2]
    row_data["AQI_Lag_3"] = lag_values[-3]

    # Create model input
    X = pd.DataFrame(
        [[row_data[col] for col in FEATURE_COLUMNS]],
        columns=FEATURE_COLUMNS
    )

    # Validate missing values
    if X.isnull().any().any():
        raise ValueError(
            "Missing value detected in future features."
        )

    # Predict
    prediction = float(model.predict(X)[0])

    # Keep prediction in OpenWeather AQI range
    prediction = max(1.0, min(5.0, prediction))

    predictions.append(prediction)

    # Update lag values
    lag_values.append(prediction)


# ============================================================
# CREATE OUTPUT
# ============================================================

future_df["Predicted_AQI"] = predictions

output_df = future_df[
    [
        "Timestamp",
        "Predicted_AQI",
    ]
].copy()


# ============================================================
# SAVE PREDICTIONS
# ============================================================

PREDICTION_DIR.mkdir(
    parents=True,
    exist_ok=True
)

output_df.to_csv(
    PREDICTION_FILE,
    index=False
)

print("\nPredictions saved to:")
print(PREDICTION_FILE)


# ============================================================
# DAILY SUMMARY
# ============================================================

output_df["Date"] = (
    output_df["Timestamp"]
    .dt.date
)

daily_summary = (
    output_df
    .groupby("Date")["Predicted_AQI"]
    .agg(
        Average_AQI="mean",
        Minimum_AQI="min",
        Maximum_AQI="max",
    )
    .reset_index()
)

daily_summary["Date"] = (
    daily_summary["Date"]
    .astype(str)
)


# ============================================================
# SUMMARY JSON
# ============================================================

summary = {
    "model_version": "v1",
    "model_type": type(model).__name__,
    "forecast_hours": len(output_df),
    "forecast_days": 3,
    "location": "Karachi",
    "generated_on": datetime.now(
        timezone.utc
    ).isoformat(),
    "prediction_file": str(PREDICTION_FILE),
    "daily_summary": daily_summary.to_dict(
        orient="records"
    ),
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

print("\n========== 3-DAY AQI FORECAST ==========")

print(
    output_df.to_string(index=False)
)

print("\n========== DAILY SUMMARY ==========")

print(
    daily_summary.to_string(index=False)
)

print("\nPrediction summary saved to:")
print(SUMMARY_FILE)

print("\n=======================================================")
print("PHASE 11B COMPLETED SUCCESSFULLY!")
print("=======================================================")