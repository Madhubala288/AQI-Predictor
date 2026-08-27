"""Feature Store creation and validation pipeline."""

import json
from pathlib import Path
from datetime import datetime

import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "processed_data.csv"
FEATURE_STORE_DIR = BASE_DIR / "feature_store"

FEATURE_FILE = FEATURE_STORE_DIR / "features_v1.csv"
METADATA_FILE = FEATURE_STORE_DIR / "metadata.json"


# ============================================================
# 2. REQUIRED FEATURES
# ============================================================

FEATURE_COLUMNS = [
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
    "NH3",
    "Hour",
    "Day",
    "Month",
    "Weekday",
    "AQI_Change",
    "AQI_Moving_Average_3H",
    "AQI_Lag_1",
    "AQI_Lag_2",
    "AQI_Lag_3"
]


# ============================================================
# 3. LOAD PROCESSED DATA
# ============================================================

print("Loading processed dataset...")

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Processed dataset not found:\n{INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print(f"Input Shape: {df.shape}")


# ============================================================
# 4. VALIDATE REQUIRED COLUMNS
# ============================================================

print("\nValidating feature columns...")

missing_columns = [
    column for column in FEATURE_COLUMNS
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("All required feature columns are available.")


# ============================================================
# 5. SELECT FEATURES
# ============================================================

feature_df = df[FEATURE_COLUMNS].copy()

print("\nFeature dataset created.")
print(f"Feature Shape: {feature_df.shape}")


# ============================================================
# 6. CHECK MISSING VALUES
# ============================================================

print("\nChecking missing values...")

missing_values = feature_df.isnull().sum()

total_missing = missing_values.sum()

print(missing_values)

if total_missing > 0:
    raise ValueError(
        f"Feature Store contains {total_missing} missing values."
    )

print("No missing values found.")


# ============================================================
# 7. CREATE FEATURE STORE DIRECTORY
# ============================================================

FEATURE_STORE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 8. SAVE FEATURES
# ============================================================

feature_df.to_csv(
    FEATURE_FILE,
    index=False
)

print("\nFeatures saved successfully:")
print(FEATURE_FILE)


# ============================================================
# 9. CREATE METADATA
# ============================================================

metadata = {
    "version": "v1",
    "created_on": datetime.now().isoformat(),
    "source": "data/processed/processed_data.csv",
    "rows": int(len(feature_df)),
    "columns": int(len(feature_df.columns)),
    "features": FEATURE_COLUMNS
}


with open(
    METADATA_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        indent=4
    )


print("\nMetadata saved successfully:")
print(METADATA_FILE)


# ============================================================
# 10. FEATURE STORE RETRIEVAL TEST
# ============================================================

print("\nTesting Feature Store retrieval...")

test_df = pd.read_csv(FEATURE_FILE)

print(f"Retrieved Shape: {test_df.shape}")
print(f"Retrieved Columns: {len(test_df.columns)}")

if test_df.shape != feature_df.shape:
    raise ValueError(
        "Feature Store retrieval validation failed."
    )

print("Feature Store retrieval test passed.")


# ============================================================
# 11. FINAL STATUS
# ============================================================

print("\n" + "=" * 55)
print("PHASE 7 COMPLETED SUCCESSFULLY!")
print("=" * 55)

print("\nFeature Store:")
print(f"Features : {FEATURE_FILE}")
print(f"Metadata : {METADATA_FILE}")
print(f"Rows     : {len(feature_df)}")
print(f"Features : {len(feature_df.columns)}")