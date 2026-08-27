"""Phase 6 - Feature Engineering Pipeline."""

import os
import pandas as pd


# ============================================================
# 1. File Paths
# ============================================================

INPUT_FILE = "data/processed/cleaned_data.csv"
OUTPUT_FILE = "data/processed/processed_data.csv"


# ============================================================
# 2. Load Dataset
# ============================================================

print("Loading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print("Original Shape:", df.shape)


# ============================================================
# 3. Convert Timestamp to Datetime
# ============================================================

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce",
    utc=True
)

# Remove invalid timestamps
df = df.dropna(subset=["Timestamp"])

# Sort chronologically
df = df.sort_values("Timestamp").reset_index(drop=True)

print("Timestamp converted and dataset sorted.")


# ============================================================
# 4. Time-Based Features
# ============================================================

df["Hour"] = df["Timestamp"].dt.hour

df["Day"] = df["Timestamp"].dt.day

df["Month"] = df["Timestamp"].dt.month

df["Weekday"] = df["Timestamp"].dt.weekday


# ============================================================
# 5. AQI Change Rate
# ============================================================

df["AQI_Change"] = df["AQI"].diff()


# ============================================================
# 6. 3-Hour Moving Average
# ============================================================

df["AQI_Moving_Average_3H"] = (
    df["AQI"]
    .rolling(window=3)
    .mean()
)


# ============================================================
# 7. Lag Features
# ============================================================

df["AQI_Lag_1"] = df["AQI"].shift(1)

df["AQI_Lag_2"] = df["AQI"].shift(2)

df["AQI_Lag_3"] = df["AQI"].shift(3)


# ============================================================
# 8. Remove Rows Created with NaN
# ============================================================

df = df.dropna().reset_index(drop=True)


# ============================================================
# 9. Final Data Quality Check
# ============================================================

print("\n========== FEATURE ENGINEERING CHECK ==========")

print("Final Shape:", df.shape)

print("\nNew Columns:")

new_features = [
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

for feature in new_features:
    print(f"- {feature}")

print("\nMissing Values:")
print(df.isnull().sum())


# ============================================================
# 10. Save Processed Dataset
# ============================================================

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n============================================")
print("PHASE 6 COMPLETED SUCCESSFULLY!")
print("Processed dataset saved at:")
print(OUTPUT_FILE)
print("============================================")