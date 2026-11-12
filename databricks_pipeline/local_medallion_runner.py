#!/usr/bin/env python3
"""
Local / Databricks execution script for Member 2's Medallion Pipeline.
Supports both PySpark/Delta (if installed) and Pandas/DuckDB fallback for local verification.
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")
DELTA_DIR = os.path.join(ROOT_DIR, "data", "delta")
BRONZE_DIR = os.path.join(DELTA_DIR, "bronze")
SILVER_DIR = os.path.join(DELTA_DIR, "silver")
GOLD_DIR = os.path.join(DELTA_DIR, "gold")

for d in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(d, exist_ok=True)


def clean_str(series):
    return series.astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)


def run_medallion_pipeline():
    print("=" * 60)
    print("MANDI PRICE INTELLIGENCE - MEDALLION ETL PIPELINE (MEMBER 2)")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)


    # 1. BRONZE LAYER (RAW INGESTION WITH AUDIT TRAIL)

    print("\n[BRONZE LAYER] Ingesting raw source files...")
    
    mandi_raw = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "monthly_mandi_wheat_prices.csv"))
    mandi_raw["_ingested_at"] = datetime.utcnow()
    mandi_raw["_source_file"] = "monthly_mandi_wheat_prices.csv"
    mandi_raw.to_parquet(os.path.join(BRONZE_DIR, "bronze_mandi_prices.parquet"), index=False)
    print(f"  ✓ Bronze Mandi Prices: {len(mandi_raw):,} records")

    weather_raw = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "monthly_weather.csv"))
    weather_raw["_ingested_at"] = datetime.utcnow()
    weather_raw["_source_file"] = "monthly_weather.csv"
    weather_raw.to_parquet(os.path.join(BRONZE_DIR, "bronze_weather.parquet"), index=False)
    print(f"  ✓ Bronze Weather: {len(weather_raw):,} records")

    arrivals_raw = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "monthly_wheat_arrivals.csv"))
    arrivals_raw["_ingested_at"] = datetime.utcnow()
    arrivals_raw["_source_file"] = "monthly_wheat_arrivals.csv"
    arrivals_raw.to_parquet(os.path.join(BRONZE_DIR, "bronze_arrivals.parquet"), index=False)
    print(f"  ✓ Bronze Arrivals: {len(arrivals_raw):,} records")


    # 2. SILVER LAYER (CLEANING, STANDARDIZATION & VALIDATION)

    print("\n[SILVER LAYER] Cleaning, validating, and conforming schemas...")
    
    # Mandi Prices Silver
    mandi_silver = mandi_raw.copy()
    mandi_silver["State"] = clean_str(mandi_silver["State"])
    mandi_silver["District"] = clean_str(mandi_silver["District"])
    mandi_silver["month"] = mandi_silver["month"].str.strip()
    mandi_silver = mandi_silver[mandi_silver["average_modal_price"] > 0]
    mandi_silver = mandi_silver.drop_duplicates(subset=["State", "District", "month"])
    mandi_silver["_silver_processed_at"] = datetime.utcnow()
    mandi_silver.to_parquet(os.path.join(SILVER_DIR, "silver_mandi_prices.parquet"), index=False)
    print(f"  ✓ Silver Mandi Prices: {len(mandi_silver):,} clean records")

    # Weather Silver
    weather_silver = weather_raw.copy()
    weather_silver["State"] = clean_str(weather_silver["State"])
    weather_silver["District"] = clean_str(weather_silver["District"])
    weather_silver["month"] = weather_silver["month"].str.strip()
    weather_silver = weather_silver.drop_duplicates(subset=["State", "District", "month"])
    weather_silver["_silver_processed_at"] = datetime.utcnow()
    weather_silver.to_parquet(os.path.join(SILVER_DIR, "silver_weather.parquet"), index=False)
    print(f"  ✓ Silver Weather: {len(weather_silver):,} clean records")

    # Arrivals Silver
    arrivals_silver = arrivals_raw.copy()
    arrivals_silver["State"] = clean_str(arrivals_silver["State"])
    arrivals_silver["District"] = clean_str(arrivals_silver["District"])
    arrivals_silver["month"] = arrivals_silver["month"].str.strip()
    arrivals_silver = arrivals_silver[arrivals_silver["arrival_quantity_tonnes"] >= 0]
    arrivals_silver = arrivals_silver.drop_duplicates(subset=["State", "District", "month"])
    arrivals_silver["_silver_processed_at"] = datetime.utcnow()
    arrivals_silver.to_parquet(os.path.join(SILVER_DIR, "silver_arrivals.parquet"), index=False)
    print(f"  ✓ Silver Arrivals: {len(arrivals_silver):,} clean records")


    # 3. GOLD LAYER (INTEGRATION, MARTS & POWER BI READY TABLES)

    print("\n[GOLD LAYER] Integrating multi-source lakehouse tables...")

    # Select operational columns
    mandi_cols = ["State", "District", "month", "average_min_price", "average_max_price", "average_modal_price", "price_record_count"]
    weather_cols = ["State", "District", "month", "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "relative_humidity_2m_mean", "wind_speed_10m_max"]
    arrivals_cols = ["State", "District", "month", "arrival_quantity_tonnes"]

    mandi_part = mandi_silver[mandi_cols].copy()
    mandi_part["_mandi_present"] = True

    weather_part = weather_silver[weather_cols].copy()
    weather_part["_weather_present"] = True

    arrivals_part = arrivals_silver[arrivals_cols].copy()
    arrivals_part["_arrival_present"] = True

    # Full Outer Join
    gold_df = pd.merge(mandi_part, weather_part, on=["State", "District", "month"], how="outer")
    gold_df = pd.merge(gold_df, arrivals_part, on=["State", "District", "month"], how="outer")

    gold_df["_mandi_present"] = gold_df["_mandi_present"].fillna(False)
    gold_df["_weather_present"] = gold_df["_weather_present"].fillna(False)
    gold_df["_arrival_present"] = gold_df["_arrival_present"].fillna(False)

    gold_df["match_type"] = np.select(
        [
            gold_df["_mandi_present"] & gold_df["_weather_present"] & gold_df["_arrival_present"],
            gold_df["_mandi_present"] & gold_df["_weather_present"],
            gold_df["_mandi_present"] & gold_df["_arrival_present"],
            gold_df["_weather_present"] & gold_df["_arrival_present"],
            gold_df["_mandi_present"],
            gold_df["_weather_present"],
            gold_df["_arrival_present"],
        ],
        [
            "All three datasets",
            "Mandi + Weather",
            "Mandi + Arrivals",
            "Weather + Arrivals",
            "Mandi only",
            "Weather only",
            "Arrivals only",
        ],
        default="Unknown"
    )

    gold_df["price_spread"] = gold_df["average_max_price"] - gold_df["average_min_price"]
    gold_df["_gold_generated_at"] = datetime.utcnow()

    # Save Master Gold Table
    gold_master_path = os.path.join(GOLD_DIR, "gold_mandi_price_intelligence.parquet")
    gold_master_csv = os.path.join(GOLD_DIR, "gold_mandi_price_intelligence.csv")
    gold_df.to_parquet(gold_master_path, index=False)
    gold_df.to_csv(gold_master_csv, index=False)
    print(f"  ✓ Gold Master Intelligence Table: {len(gold_df):,} rows")
    print(f"    -> Saved to: {gold_master_path}")
    print(f"    -> Exported CSV for Power BI: {gold_master_csv}")


    # 4. POWER BI ANALYTICAL MARTS (FOR MEMBER 1 / VANSH)

    print("\n[GOLD MARTS] Generating curated analytical marts for Power BI...")

    # Mart 1: State Monthly Trends
    mart_state = gold_df.groupby(["State", "month"], as_index=False).agg(
        state_avg_modal_price=("average_modal_price", "mean"),
        state_total_arrivals=("arrival_quantity_tonnes", "sum"),
        total_mandi_records=("price_record_count", "sum"),
        avg_temperature=("temperature_2m_mean", "mean"),
        total_precipitation=("precipitation_sum", "sum")
    )
    mart_state_csv = os.path.join(GOLD_DIR, "mart_state_monthly_trends.csv")
    mart_state.to_csv(mart_state_csv, index=False)
    print(f"  ✓ Mart 1 (State Monthly Trends): {len(mart_state):,} rows -> {mart_state_csv}")

    # Mart 2: District Summary KPIs
    mart_district = gold_df.groupby(["State", "District"], as_index=False).agg(
        overall_avg_modal_price=("average_modal_price", "mean"),
        min_observed_price=("average_min_price", "min"),
        max_observed_price=("average_max_price", "max"),
        total_arrivals_tonnes=("arrival_quantity_tonnes", "sum"),
        active_months=("month", "nunique")
    ).sort_values(by="total_arrivals_tonnes", ascending=False)
    mart_district_csv = os.path.join(GOLD_DIR, "mart_district_summary.csv")
    mart_district.to_csv(mart_district_csv, index=False)
    print(f"  ✓ Mart 2 (District Summary KPIs): {len(mart_district):,} rows -> {mart_district_csv}")

    # Mart 3: Price vs Arrivals Correlation Mart (Mandi + Arrivals overlap)
    mart_corr = gold_df[gold_df["match_type"] == "Mandi + Arrivals"][[
        "State", "District", "month", "average_modal_price", "arrival_quantity_tonnes", "price_spread"
    ]].dropna()
    mart_corr_csv = os.path.join(GOLD_DIR, "mart_price_arrival_correlation.csv")
    mart_corr.to_csv(mart_corr_csv, index=False)
    print(f"  ✓ Mart 3 (Price-Arrival Correlation): {len(mart_corr):,} rows -> {mart_corr_csv}")


    # 5. EXECUTION & VALIDATION SUMMARY

    print("\n" + "=" * 60)
    print("PIPELINE AUDIT & VALIDATION SUMMARY")
    print("=" * 60)
    print(gold_df["match_type"].value_counts().to_string())
    print("\nMissing Values Count in Gold Master:")
    print(gold_df[["State", "District", "month", "average_modal_price", "arrival_quantity_tonnes", "temperature_2m_mean"]].isnull().sum().to_string())
    print("\nPIPELINE EXECUTION FINISHED SUCCESSFULLY!")


if __name__ == "__main__":
    run_medallion_pipeline()
