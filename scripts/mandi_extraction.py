
import pandas as pd

file_path = "data/raw/mandi_daily_2025.parquet"

df = pd.read_parquet(file_path)

print("\n--- DATASET OVERVIEW ---")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 RECORDS:")
print(df.head().to_string())

print("\nDATA TYPES:")
print(df.dtypes)

print("\nMISSING VALUES:")
print(df.isnull().sum())

print("\nDATE COVERAGE:")
df["Arrival_Date"] = pd.to_datetime(
    df["Arrival_Date"], errors="coerce"
)

print("Start Date:", df["Arrival_Date"].min())
print("End Date:", df["Arrival_Date"].max())
print("Unique Dates:", df["Arrival_Date"].nunique())

print("\nGEOGRAPHICAL COVERAGE:")
print("States:", df["State"].nunique())
print("Districts:", df["District"].nunique())
print("Markets:", df["Market"].nunique())

print("\nCOMMODITY COVERAGE:")
print("Commodities:", df["Commodity"].nunique())

print("\nDUPLICATES:", df.duplicated().sum())

print("\nINSPECTION COMPLETED!")