import requests
import pandas as pd
import time

# Top 5 districts from our mandi dataset
districts = [
    "Salem",
    "Coimbatore",
    "Tiruvannamalai",
    "Madurai",
    "Vellore"
]

state = "Tamil Nadu"

weather_url = "https://archive-api.open-meteo.com/v1/archive"
geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

weather_variables = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "relative_humidity_2m_mean",
    "wind_speed_10m_max"
]

all_weather = []

for district in districts:

    print(f"\nFetching weather for {district}...")

    # Step 1: Find district coordinates
    geo_params = {
        "name": district,
        "count": 10,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geocoding_url,
        params=geo_params,
        timeout=30
    )
    geo_response.raise_for_status()

    geo_data = geo_response.json()

    results = geo_data.get("results", [])

    location = next(
        (
            place for place in results
            if place.get("country_code") == "IN"
            and place.get("admin1") == state
        ),
        None
    )

    if location is None:
        print(f"Coordinates not found for {district}. Skipping.")
        continue

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Fetch historical weather
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "daily": weather_variables,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        weather_url,
        params=params,
        timeout=60
    )
    response.raise_for_status()

    data = response.json()

    # Step 3: Convert response into a DataFrame
    df = pd.DataFrame(data["daily"])

    df["District"] = district
    df["State"] = state
    df["Latitude"] = latitude
    df["Longitude"] = longitude

    all_weather.append(df)

    print(f"Downloaded {len(df)} records for {district}")

    time.sleep(1)

# Step 4: Combine all districts
if all_weather:

    final_df = pd.concat(all_weather, ignore_index=True)

    output_path = "data/raw/weather_tamil_nadu_2025.csv"

    import os
    os.makedirs("data/raw", exist_ok=True)

    final_df.to_csv(output_path, index=False)

    print("\nWEATHER COLLECTION COMPLETED")
    print("--------------------------------")
    print("Total records:", len(final_df))
    print("Districts collected:", final_df["District"].nunique())
    print("Missing values:\n", final_df.isnull().sum())
    print("Saved to:", output_path)

else:
    print("No weather data was collected.")