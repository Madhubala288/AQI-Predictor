import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

LAT = 24.8607
LON = 67.0011

url = (
    "https://api.openweathermap.org/data/2.5/"
    "air_pollution/forecast"
)

params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY
}

print("Requesting future air pollution forecast...")

response = requests.get(url, params=params, timeout=30)

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("API request failed.")
    print(response.text)
    raise SystemExit

data = response.json()

print("Forecast data received successfully.")
print("Number of forecast records:", len(data["list"]))

print("\nFirst forecast record:")
print(data["list"][0])