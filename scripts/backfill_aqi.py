# ============================================
# Karachi Historical AQI Backfill
# ============================================

import os
import requests
import pandas as pd
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    print("ERROR: OPENWEATHER_API_KEY not found in .env file.")
    exit()

# 2. Karachi coordinates
LAT = 24.8607
LON = 67.0011
CITY = "Karachi"

# 3. Historical period
# 30 days = approximately 720 hourly records
START_DATE = datetime(2024, 1, 1, tzinfo=timezone.utc)
END_DATE = datetime(2024, 1, 31, tzinfo=timezone.utc)

print("============================================")
print("Karachi Historical AQI Backfill")
print("============================================")

print("City:", CITY)
print("Start:", START_DATE)
print("End:", END_DATE)

all_rows = []

current_start = START_DATE

# 4. Fetch data day-by-day
while current_start < END_DATE:

    current_end = current_start + timedelta(days=1)

    # Do not go beyond final date
    if current_end > END_DATE:
        current_end = END_DATE

    start_timestamp = int(current_start.timestamp())
    end_timestamp = int(current_end.timestamp())

    print(
        f"\nFetching: "
        f"{current_start.date()} "
        f"to "
        f"{current_end.date()}"
    )

    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution/history"
        f"?lat={LAT}"
        f"&lon={LON}"
        f"&start={start_timestamp}"
        f"&end={end_timestamp}"
        f"&appid={API_KEY}"
    )

    try:

        response = requests.get(url, timeout=30)

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        records = data.get("list", [])

        print("Records received:", len(records))

        # 5. Process records
        for item in records:

            timestamp = datetime.fromtimestamp(
                item["dt"],
                tz=timezone.utc
            )

            components = item.get("components", {})

            row = {
                "Timestamp": timestamp,
                "City": CITY,
                "AQI": item["main"]["aqi"],
                "PM2.5": components.get("pm2_5"),
                "PM10": components.get("pm10"),
                "CO": components.get("co"),
                "NO2": components.get("no2"),
                "SO2": components.get("so2"),
                "O3": components.get("o3"),
                "NH3": components.get("nh3")
            }

            all_rows.append(row)

    except requests.exceptions.RequestException as e:

        print("API ERROR:", e)

    current_start = current_end


# 6. Create DataFrame
df = pd.DataFrame(all_rows)

if df.empty:
    print("\nERROR: No historical AQI data collected.")
    exit()

# 7. Remove duplicate timestamps
df = df.drop_duplicates(subset=["Timestamp"])

# 8. Sort by timestamp
df = df.sort_values("Timestamp")

# 9. Reset index
df = df.reset_index(drop=True)

# 10. Save final AQI dataset
os.makedirs("data/historical", exist_ok=True)

output_file = "data/historical/karachi_historical_aqi.csv"

df.to_csv(output_file, index=False)

# 11. Display summary
print("\n============================================")
print("BACKFILL COMPLETED")
print("============================================")

print("\nTotal records:", len(df))

print("\nFirst 5 records:")
print(df.head())

print("\nLast 5 records:")
print(df.tail())

print("\nAQI Distribution:")
print(df["AQI"].value_counts().sort_index())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDate Range:")
print(df["Timestamp"].min())
print(df["Timestamp"].max())

print("\nFile saved at:")
print(output_file)