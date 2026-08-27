import os
import requests
import pandas as pd

def fetch_weather_and_merge():
    # 1. Historical AQI Data Load Karein
    aqi_path = "data/historical/historical_aqi.csv"
    if not os.path.exists(aqi_path):
        print(f"Error: {aqi_path} nahi mili!")
        return

    print("AQI Data load ho raha hai...")
    df_aqi = pd.read_csv(aqi_path)

    # 2. Open-Meteo Weather API se Delhi ka Weather Data Fetch Karein
    lat, lon = 28.61, 77.23
    start_date = "2024-01-01"
    end_date = "2024-01-30"

    print("Weather Data fetch ho raha hai...")
    weather_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

    response = requests.get(weather_url)

    if response.status_code == 200:
        weather_json = response.json().get('hourly', {})
        df_weather = pd.DataFrame(weather_json)

        # Columns Rename Karein
        df_weather.rename(columns={
            'time': 'Date',
            'temperature_2m': 'Temperature',
            'relative_humidity_2m': 'Humidity',
            'wind_speed_10m': 'Wind_Speed'
        }, inplace=True)

        # 3. AQI aur Weather Data ko Date ke base par Merge Karein
        print("AQI aur Weather Data merge ho raha hai...")
        final_df = pd.merge(df_aqi, df_weather, on='Date', how='inner')

        # 4. Final Clean File Save Karein
        output_path = "data/historical/final_historical_dataset.csv"
        final_df.to_csv(output_path, index=False)

        print(f"\nSUCCESS: Merged Dataset Saved: {output_path}")
        print("\n--- Final Dataset Preview ---")
        print(final_df.head())

    else:
        print(f"Weather API Error: Status Code {response.status_code}")

if __name__ == "__main__":
    fetch_weather_and_merge()