
import pandas as pd
import json

file_path = "data/raw/crop_arrivals_wheat_2025.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)

print("\n--- DATASET OVERVIEW ---")
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("\nColumns:", list(df.columns))

print("\n--- MONTHLY COVERAGE ---")
print(sorted(df["t"].unique()))

print("\n--- GEOGRAPHICAL COVERAGE ---")
print("States:", df["state"].nunique())
print("Districts:", df["district"].nunique())

print("\n--- DATA QUALITY ---")
print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

print("\n--- QUANTITY STATISTICS ---")
print(df["qty"].describe())

print("\n--- SAMPLE RECORDS ---")
print(df.head())