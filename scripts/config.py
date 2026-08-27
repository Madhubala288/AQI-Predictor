"""Configuration settings and path management for the AQI Predictor project."""

from pathlib import Path

# Project Root Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = BASE_DIR / "data"
HISTORICAL_DIR = DATA_DIR / "historical"
PROCESSED_DIR = DATA_DIR / "processed"

# Input and Output Files
HISTORICAL_DATA = HISTORICAL_DIR / "karachi_historical_dataset.csv"
PROCESSED_DATA = PROCESSED_DIR / "cleaned_data.csv"

# Required Columns
REQUIRED_COLUMNS = [
    "Timestamp",
    "City",
    "Temperature",
    "Humidity",
    "Pressure",
    "Wind_Speed",
    "AQI",
    "PM2.5",
    "PM10",
    "CO",
    "NO2",
    "SO2",
    "O3",
    "NH3"
]