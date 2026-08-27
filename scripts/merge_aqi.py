import os
import pandas as pd

# Files load karein
cleaned_file = "data/processed/cleaned_data.csv"
aqi_file = "data/raw/historical_aqi.csv"

if not os.path.exists(cleaned_file) or not os.path.exists(aqi_file):
    print("Error: Required files not found!")
    exit()

df_cleaned = pd.read_csv(cleaned_file)
df_aqi = pd.read_csv(aqi_file)

# Date column ko datetime format mein convert karein
df_cleaned["Date"] = pd.to_datetime(df_cleaned["Date"]).dt.strftime("%Y-%m-%d")
df_aqi["Date"] = pd.to_datetime(df_aqi["Date"]).dt.strftime("%Y-%m-%d")

# Merge on Date column
df_final = pd.merge(df_cleaned, df_aqi, on="Date", how="inner")

# Final merged dataset save karein
df_final.to_csv("data/processed/final_historical_dataset.csv", index=False)
df_final.to_csv("data/processed/cleaned_data.csv", index=False)

print("\n========== DATASET MERGED SUCCESSFULLY ==========")
print(f"Total Rows: {len(df_final)}")
print("\nColumns in final dataset:")
print(df_final.columns.tolist())
print("\nFirst 5 rows:")
print(df_final.head())