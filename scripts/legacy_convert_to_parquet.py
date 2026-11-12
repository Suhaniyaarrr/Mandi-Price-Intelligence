from pathlib import Path
import pandas as pd

folder = Path("data/processed")

files = [
    "monthly_weather.csv",
    "monthly_wheat_arrivals.csv",
    "monthly_mandi_wheat_prices.csv",
    "monthly_combined_intelligence.csv"
]

for filename in files:
    source = folder / filename
    df = pd.read_csv(source)

    output = source.with_suffix(".parquet")
    df.to_parquet(output, index=False)

    print(f"Converted: {filename} -> {output.name} | Rows: {len(df)}")

print("\nAll conversions completed!")
