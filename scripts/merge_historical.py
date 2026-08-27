# 1. Import libraries
import os
import glob
import pandas as pd

# 2. Find all CSV files
files = glob.glob("data/historical/*.csv")
print("Files Found:")
print(files)

# 3. Read all CSV files
df_list = []
for file in files:
    print(f"Reading: {file}")
    df = pd.read_csv(file)
    df_list.append(df)

if df_list:
    # 4. Merge datasets
    historical_df = pd.concat(df_list, ignore_index=True)
    print("\nMerged Successfully!")
    print(historical_df.head())

    # 5. Remove duplicates
    historical_df = historical_df.drop_duplicates()
    print("\nDuplicates removed successfully.")
    print("Dataset Shape:", historical_df.shape)

    # 6. Check missing values
    print("\nMissing Values:")
    print(historical_df.isnull().sum())

    # 7. Remove missing values
    historical_df = historical_df.dropna()
    print("Missing values removed.")

    # 8. Clean column names
    historical_df.columns = historical_df.columns.str.strip()

    # 9. Convert Date column
    if "Date" in historical_df.columns:
        historical_df["Date"] = pd.to_datetime(
            historical_df["Date"], errors="coerce"
        )

    # 10. Remove invalid dates
    historical_df = historical_df.dropna(subset=["Date"])

    # 11. Sort by Date
    historical_df = historical_df.sort_values("Date")

    # 12. Reset index
    historical_df = historical_df.reset_index(drop=True)

    # 13. Display info & statistics
    print("\nDataset Information:\n")
    print(historical_df.info())

    print("\nStatistical Summary:\n")
    print(historical_df.describe())

    # 14. Save historical_data.csv
    output_path = "data/historical/historical_data.csv"
    historical_df.to_csv(output_path, index=False)
    print("\nHistorical dataset saved successfully to:", output_path)

else:
    print("\nNo CSV files found in data/historical/")