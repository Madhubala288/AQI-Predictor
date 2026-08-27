# Step 2 — Import Libraries
import os
import pandas as pd

# Step 3 — Read Dataset
data_path = "data/historical/historical_data.csv"

if not os.path.exists(data_path):
    print(f"Error: {data_path} not found!")
    exit()

df = pd.read_csv(data_path)
print("Dataset Loaded Successfully")

# Step 4 — Check Dataset Shape
print("\nDataset Shape")
print(df.shape)

# Step 5 — Check Column Names
expected_columns = [
    "Date",
    "City",
    "PM2.5",
    "PM10",
    "NO2",
    "SO2",
    "CO",
    "O3",
]

# Step 6 — Missing Columns Check
missing_columns = []
for column in expected_columns:
    if column not in df.columns:
        missing_columns.append(column)

print("\nColumn Verification:")
if len(missing_columns) == 0:
    print("All required columns exist.")
else:
    print("Missing Columns:", missing_columns)

# Step 7 — Check Data Types
print("\nData Types\n")
print(df.dtypes)

# Step 8 — Convert Date
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Step 9 — Check Missing Values
print("\nMissing Values\n")
print(df.isnull().sum())

# Step 10 — Check Duplicate Rows
duplicates = df.duplicated().sum()
print("\nDuplicate Records")
print(duplicates)

# Step 11 — Check Numeric Columns
pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]

print("\nPollutant Statistics:")
for column in pollutants:
    if column in df.columns:
        print(f"\n--- {column} ---")
        print(df[column].describe())

# Step 12 — Check Negative Values
print("\nNegative Values Check:")
for column in pollutants:
    if column in df.columns:
        negative = (df[column] < 0).sum()
        print(f"{column} Negative Values = {negative}")

# Step 13 — Check Date Range
print("\nDate Range")
if "Date" in df.columns:
    print("Start:", df["Date"].min())
    print("End:", df["Date"].max())

# Step 14 — Create Validation Report
# Make sure reports directory exists
os.makedirs("reports", exist_ok=True)

start_date = df["Date"].min() if "Date" in df.columns else "N/A"
end_date = df["Date"].max() if "Date" in df.columns else "N/A"

report = f"""==================================
Historical Data Validation
==================================

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Duplicate Records: {df.duplicated().sum()}

Missing Values:
{df.isnull().sum().to_string()}

Date Range:
{start_date} to {end_date}
"""

with open("reports/validation_report.txt", "w") as file:
    file.write(report)

print("\nValidation report saved.")