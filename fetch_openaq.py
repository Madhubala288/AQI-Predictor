import os
import requests
import pandas as pd

def fetch_historical_aqi(lat=28.61, lon=77.23, city_name="Delhi"):
    # Output directory create karein
    os.makedirs("data/historical", exist_ok=True)
    
    print(f"Fetching historical AQI data for {city_name} via Open-Meteo...")
    
    # Open-Meteo Historical Air Quality API Endpoint
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&hourly=pm2_5,pm10,nitrogen_dioxide,ozone,sulphur_dioxide,carbon_monoxide&start_date=2024-01-01&end_date=2024-01-30"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        hourly_data = response.json().get('hourly', {})
        
        # DataFrame mein convert karein
        df = pd.DataFrame(hourly_data)
        
        # Columns ko required format mein rename karein
        df.rename(columns={
            'time': 'Date',
            'pm2_5': 'PM2.5',
            'pm10': 'PM10',
            'nitrogen_dioxide': 'NO2',
            'ozone': 'O3',
            'sulphur_dioxide': 'SO2',
            'carbon_monoxide': 'CO'
        }, inplace=True)
        
        df['City'] = city_name
        
        # Columns ki sequence set karein
        cols = ['Date', 'City', 'PM2.5', 'PM10', 'NO2', 'O3', 'SO2', 'CO']
        df = df[cols]
        
        # File save karein
        output_path = "data/historical/historical_aqi.csv"
        df.to_csv(output_path, index=False)
        
        print(f"SUCCESS: Data saved successfully to {output_path}")
        print("\n--- Processed Data Preview ---")
        print(df.head())
    else:
        print(f"API Error: Status Code {response.status_code}")

if __name__ == "__main__":
    fetch_historical_aqi(lat=28.61, lon=77.23, city_name="Delhi")