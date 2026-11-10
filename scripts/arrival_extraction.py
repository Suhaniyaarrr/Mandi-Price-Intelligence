
import requests
import json
import os

url = "https://agmarknet.ceda.ashoka.edu.in/api/quantities"

payload = {
    "state_id": 0,
    "district_id": 0,
    "commodity_id": 1,
    "calculation_type": "m",
    "chart_type": "map",
    "start_date": "2025-01-01T00:00:00Z",
    "end_date": "2025-12-31T00:00:00Z"
}

try:
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    records = result.get("data", [])

    os.makedirs("data/raw", exist_ok=True)

    output_file = "data/raw/crop_arrivals_wheat_2025.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    print("Extraction successful!")
    print("Total records:", len(records))
    print("Saved to:", output_file)

except requests.exceptions.RequestException as error:
    print("API request failed:", error)
