import pandas as pd
import os

# ============================================
# 1. File paths
# ============================================

aqi_file = "data/historical/karachi_historical_aqi.csv"
weather_file = "data/historical/karachi_historical_weather.csv"

# ============================================
# 2. Load datasets
# ============================================

print("Loading AQI data...")
aqi_df = pd.read_csv(aqi_file)

print("Loading weather data...")
weather_df = pd.read_csv(weather_file)

# ============================================
# 3. Convert Timestamp
# ============================================

aqi_df["Timestamp"] = pd.to_datetime(
    aqi_df["Timestamp"],
    utc=True
)

weather_df["Timestamp"] = pd.to_datetime(
    weather_df["Timestamp"],
    utc=True
)

# ============================================
# 4. Remove duplicate timestamps
# ============================================

aqi_df = aqi_df.drop_duplicates(
    subset=["Timestamp"]
)

weather_df = weather_df.drop_duplicates(
    subset=["Timestamp"]
)

# ============================================
# 5. Merge AQI + Weather
# ============================================

merged_df = pd.merge(
    weather_df,
    aqi_df,
    on=["Timestamp", "City"],
    how="inner"
)

# ============================================
# 6. Sort by Timestamp
# ============================================

merged_df = merged_df.sort_values(
    "Timestamp"
)

merged_df = merged_df.reset_index(
    drop=True
)

# ============================================
# 7. Check missing values
# ============================================

print("\nMissing Values:")
print(merged_df.isnull().sum())

# ============================================
# 8. Dataset information
# ============================================

print("\nDataset Shape:")
print(merged_df.shape)

print("\nColumns:")
print(merged_df.columns.tolist())

print("\nFirst 5 Records:")
print(merged_df.head())

print("\nLast 5 Records:")
print(merged_df.tail())

# ============================================
# 9. Save final historical dataset
# ============================================

output_file = (
    "data/historical/"
    "karachi_historical_dataset.csv"
)

os.makedirs(
    "data/historical",
    exist_ok=True
)

merged_df.to_csv(
    output_file,
    index=False
)

print("\n============================================")
print("MERGE COMPLETED SUCCESSFULLY!")
print("============================================")

print("\nFinal records:", len(merged_df))

print("\nFile saved at:")
print(output_file)