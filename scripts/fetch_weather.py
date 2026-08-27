import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
city_name = "Karachi"

# Step 1: Weather Data Fetch Karna
weather_url = (
    f"https://api.openweathermap.org/data/2.5/weather"
    f"?q={city_name}&appid={API_KEY}&units=metric"
)

try:
    response = requests.get(weather_url)
    response.raise_for_status()
    w_data = response.json()

    # Weather details
    city = w_data["name"]
    lat = w_data["coord"]["lat"]
    lon = w_data["coord"]["lon"]
    temp = w_data["main"]["temp"]
    humidity = w_data["main"]["humidity"]
    pressure = w_data["main"]["pressure"]
    wind_speed = w_data["wind"]["speed"]
    timestamp = datetime.now()

    # Step 2: Air Pollution Data Fetch Karna (using lat & lon)
    pollution_url = (
        f"https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )
    
    p_response = requests.get(pollution_url)
    p_response.raise_for_status()
    p_data = p_response.json()

    aqi = p_data["list"][0]["main"]["aqi"]
    components = p_data["list"][0]["components"]

    # Step 3: Weather + AQI Data Merge Karna
    combined_data = {
        "Timestamp": timestamp,
        "City": city,
        "Temperature": temp,
        "Humidity": humidity,
        "Pressure": pressure,
        "Wind Speed": wind_speed,
        "AQI": aqi,
        "PM2.5": components.get("pm2_5"),
        "PM10": components.get("pm10"),
        "CO": components.get("co"),
        "NO2": components.get("no2"),
        "SO2": components.get("so2"),
        "O3": components.get("o3"),
        "NH3": components.get("nh3")
    }

    df = pd.DataFrame([combined_data])

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/raw_aqi_data.csv", index=False)
    print("Weather + Pollution Data Saved Successfully!")

except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)