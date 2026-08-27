# ============================================
# Karachi Historical Weather Backfill
# Open-Meteo Historical Weather API
# ============================================

import requests
import pandas as pd
import os

# Karachi coordinates
LAT = 24.8607
LON = 67.0011
CITY = "Karachi"

# January 2024
START_DATE = "2024-01-01"
END_DATE = "2024-01-31"

# Open-Meteo Historical Weather API
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "surface_pressure,"
        "wind_speed_10m"
    ),
    "temperature_unit": "celsius",
    "wind_speed_unit": "ms",
    "timezone": "UTC"
}

print("============================================")
print("Karachi Historical Weather Backfill")
print("============================================")

print("City:", CITY)
print("Start:", START_DATE)
print("End:", END_DATE)

try:

    # Send API request
    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    print("\nStatus Code:", response.status_code)

    response.raise_for_status()

    data = response.json()

    # Get hourly data
    hourly = data["hourly"]

    # Create DataFrame
    df = pd.DataFrame({
        "Timestamp": hourly["time"],
        "City": CITY,
        "Temperature": hourly["temperature_2m"],
        "Humidity": hourly["relative_humidity_2m"],
        "Pressure": hourly["surface_pressure"],
        "Wind_Speed": hourly["wind_speed_10m"]
    })

    # Convert timestamp
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)

    # Remove duplicates
    df = df.drop_duplicates(subset=["Timestamp"])

    # Sort by timestamp
    df = df.sort_values("Timestamp")

    # Reset index
    df = df.reset_index(drop=True)

    # Create folder
    os.makedirs("data/historical", exist_ok=True)

    # Save file
    output_file = (
        "data/historical/"
        "karachi_historical_weather.csv"
    )

    df.to_csv(
        output_file,
        index=False
    )

    # Display results
    print("\n============================================")
    print("SUCCESS!")
    print("============================================")

    print("\nTotal records:", len(df))

    print("\nFirst 5 records:")
    print(df.head())

    print("\nLast 5 records:")
    print(df.tail())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDate Range:")
    print(df["Timestamp"].min())
    print(df["Timestamp"].max())

    print("\nFile saved at:")
    print(output_file)

except requests.exceptions.RequestException as e:

    print("\nAPI ERROR:")
    print(e)

except Exception as e:

    print("\nERROR:")
    print(e)