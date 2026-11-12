
import os
import json
import pandas as pd

# Create output directory
os.makedirs("data/processed", exist_ok=True)

OUTPUT_DIR = "data/processed"


# Standardise geographical names for matching
def clean_name(series):
    return (
        series.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )


# Save processed datasets
def save_csv(data, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    data.to_csv(path, index=False)
    print(f"Saved: {path} | Records: {len(data)}")


# --------------------------------------------------
# 1. PROCESS WEATHER DATA
# --------------------------------------------------

print("\nLoading weather data...")

weather = pd.read_csv("data/raw/weather_tamil_nadu_2025.csv")

weather["State"] = clean_name(weather["State"])
weather["District"] = clean_name(weather["District"])

weather["month"] = (
    pd.to_datetime(weather["time"], errors="coerce")
    .dt.to_period("M")
    .astype(str)
)

weather_monthly = weather.groupby(
    ["State", "District", "month"], as_index=False
).agg(
    temperature_2m_mean=("temperature_2m_mean", "mean"),
    temperature_2m_max=("temperature_2m_max", "mean"),
    temperature_2m_min=("temperature_2m_min", "mean"),
    precipitation_sum=("precipitation_sum", "sum"),
    relative_humidity_2m_mean=("relative_humidity_2m_mean", "mean"),
    wind_speed_10m_max=("wind_speed_10m_max", "mean")
)

weather_monthly["_weather_present"] = True

save_csv(weather_monthly, "monthly_weather.csv")


# --------------------------------------------------
# 2. PROCESS WHEAT ARRIVAL DATA
# --------------------------------------------------

print("\nLoading wheat arrival data...")

with open(
    "data/raw/crop_arrivals_wheat_2025.json",
    "r",
    encoding="utf-8"
) as f:
    arrivals = pd.DataFrame(json.load(f))

arrivals["State"] = clean_name(arrivals["state"])
arrivals["District"] = clean_name(arrivals["district"])
arrivals["month"] = arrivals["t"].astype(str).str.strip()

arrivals["qty"] = pd.to_numeric(
    arrivals["qty"], errors="coerce"
)

arrivals = arrivals[
    arrivals["cmdty"].str.contains(
        "wheat", case=False, na=False
    )
].copy()

arrivals_monthly = arrivals.groupby(
    ["State", "District", "month"], as_index=False
).agg(
    arrival_quantity_tonnes=(
        "qty",
        lambda x: x.sum(min_count=1)
    )
)

arrivals_monthly["_arrival_present"] = True

save_csv(
    arrivals_monthly,
    "monthly_wheat_arrivals.csv"
)


# --------------------------------------------------
# 3. PROCESS MANDI WHEAT PRICE DATA
# --------------------------------------------------

print("\nLoading mandi price data...")

mandi = pd.read_parquet(
    "data/raw/mandi_daily_2025.parquet",
    columns=[
        "State",
        "District",
        "Commodity",
        "Arrival_Date",
        "Min_Price",
        "Max_Price",
        "Modal_Price"
    ]
)

mandi["State"] = clean_name(mandi["State"])
mandi["District"] = clean_name(mandi["District"])

mandi = mandi[
    mandi["Commodity"].str.contains(
        "wheat", case=False, na=False
    )
].copy()

mandi["Arrival_Date"] = pd.to_datetime(
    mandi["Arrival_Date"], errors="coerce"
)

mandi = mandi.dropna(subset=["Arrival_Date"])

mandi["month"] = (
    mandi["Arrival_Date"]
    .dt.to_period("M")
    .astype(str)
)

prices_monthly = mandi.groupby(
    ["State", "District", "month"], as_index=False
).agg(
    average_min_price=("Min_Price", "mean"),
    average_max_price=("Max_Price", "mean"),
    average_modal_price=("Modal_Price", "mean"),
    price_record_count=("Modal_Price", "count")
)

prices_monthly["_mandi_present"] = True

save_csv(
    prices_monthly,
    "monthly_mandi_wheat_prices.csv"
)


# --------------------------------------------------
# 4. COMBINE ALL THREE DATASETS
# --------------------------------------------------

print("\nCombining datasets...")

combined = prices_monthly.merge(
    weather_monthly,
    on=["State", "District", "month"],
    how="outer"
)

combined = combined.merge(
    arrivals_monthly,
    on=["State", "District", "month"],
    how="outer"
)

# Identify which datasets contributed to each row
for column in [
    "_mandi_present",
    "_weather_present",
    "_arrival_present"
]:
    combined[column] = combined[column].fillna(False)

combined["match_type"] = combined.apply(
    lambda row: (
        "All three datasets"
        if row["_mandi_present"]
        and row["_weather_present"]
        and row["_arrival_present"]
        else "Mandi + Weather"
        if row["_mandi_present"]
        and row["_weather_present"]
        else "Mandi + Arrivals"
        if row["_mandi_present"]
        and row["_arrival_present"]
        else "Weather + Arrivals"
        if row["_weather_present"]
        and row["_arrival_present"]
        else "Mandi only"
        if row["_mandi_present"]
        else "Weather only"
        if row["_weather_present"]
        else "Arrivals only"
    ),
    axis=1
)

# Save combined dataset
save_csv(
    combined,
    "monthly_combined_intelligence.csv"
)


# --------------------------------------------------
# 5. VALIDATION SUMMARY
# --------------------------------------------------

print("\n========== INTEGRATION SUMMARY ==========")

print("Mandi records:", len(prices_monthly))
print("Weather records:", len(weather_monthly))
print("Arrival records:", len(arrivals_monthly))
print("Combined records:", len(combined))

print("\nMatch type distribution:")
print(combined["match_type"].value_counts())

print("\nMissing values in combined dataset:")
print(combined.isnull().sum())

print("\nDuplicate records:", combined.duplicated(
    subset=["State", "District", "month"]
).sum())

print("\nINTEGRATION COMPLETED!")