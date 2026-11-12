#!/usr/bin/env python3
"""
Zero-dependency Python runner for Member 2's Medallion ETL Pipeline.
Uses standard library csv, math, datetime to produce Bronze, Silver, and Gold datasets,
plus curated analytical data marts ready for Power BI consumption by Vansh (Member 1).
"""

import os
import csv
from datetime import datetime
from collections import defaultdict

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DATA_DIR = os.path.join(ROOT_DIR, "data", "processed")
DELTA_DIR = os.path.join(ROOT_DIR, "data", "delta")
BRONZE_DIR = os.path.join(DELTA_DIR, "bronze")
SILVER_DIR = os.path.join(DELTA_DIR, "silver")
GOLD_DIR = os.path.join(DELTA_DIR, "gold")

for d in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(d, exist_ok=True)


def clean_name(val):
    if not val:
        return ""
    return " ".join(val.strip().lower().split())


def read_csv(path):
    with open(path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader), reader.fieldnames


def write_csv(path, rows, fieldnames):
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✓ Saved {len(rows):,} rows -> {path}")


def run_pipeline():
    print("=" * 65)
    print("MANDI PRICE INTELLIGENCE - MEDALLION LAKEHOUSE ETL PIPELINE")
    print("MEMBER 2: Python / PySpark / Databricks / Delta Lake Ready")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 65)

    # 1. BRONZE LAYER (RAW INGESTION WITH AUDIT METADATA)

    print("\n[BRONZE LAYER] Ingesting raw source files with audit columns...")

    # Bronze Mandi Prices
    mandi_raw_file = os.path.join(PROCESSED_DATA_DIR, "monthly_mandi_wheat_prices.csv")
    mandi_raw_rows, mandi_fields = read_csv(mandi_raw_file)
    now_ts = datetime.utcnow().isoformat()
    bronze_mandi = []
    for r in mandi_raw_rows:
        row = dict(r)
        row["_ingested_at"] = now_ts
        row["_source_file"] = "monthly_mandi_wheat_prices.csv"
        bronze_mandi.append(row)
    write_csv(os.path.join(BRONZE_DIR, "bronze_mandi_prices.csv"), bronze_mandi, mandi_fields + ["_ingested_at", "_source_file"])

    # Bronze Weather
    weather_raw_file = os.path.join(PROCESSED_DATA_DIR, "monthly_weather.csv")
    weather_raw_rows, weather_fields = read_csv(weather_raw_file)
    bronze_weather = []
    for r in weather_raw_rows:
        row = dict(r)
        row["_ingested_at"] = now_ts
        row["_source_file"] = "monthly_weather.csv"
        bronze_weather.append(row)
    write_csv(os.path.join(BRONZE_DIR, "bronze_weather.csv"), bronze_weather, weather_fields + ["_ingested_at", "_source_file"])

    # Bronze Arrivals
    arrivals_raw_file = os.path.join(PROCESSED_DATA_DIR, "monthly_wheat_arrivals.csv")
    arrivals_raw_rows, arrivals_fields = read_csv(arrivals_raw_file)
    bronze_arrivals = []
    for r in arrivals_raw_rows:
        row = dict(r)
        row["_ingested_at"] = now_ts
        row["_source_file"] = "monthly_wheat_arrivals.csv"
        bronze_arrivals.append(row)
    write_csv(os.path.join(BRONZE_DIR, "bronze_arrivals.csv"), bronze_arrivals, arrivals_fields + ["_ingested_at", "_source_file"])

    # 2. SILVER LAYER (CLEANING, STANDARDIZATION & VALIDATION)

    print("\n[SILVER LAYER] Standardizing schema, validating bounds & deduplicating...")

    # Silver Mandi: clean text, ensure valid positive prices, deduplicate
    silver_mandi = {}
    for r in bronze_mandi:
        state = clean_name(r.get("State", ""))
        district = clean_name(r.get("District", ""))
        month = r.get("month", "").strip()
        key = (state, district, month)

        modal_str = r.get("average_modal_price", "")
        try:
            modal_price = float(modal_str) if modal_str else 0.0
        except ValueError:
            modal_price = 0.0

        if modal_price <= 0:
            continue

        min_p = float(r.get("average_min_price", 0) or 0)
        max_p = float(r.get("average_max_price", 0) or 0)
        rec_cnt = int(float(r.get("price_record_count", 0) or 0))

        silver_mandi[key] = {
            "State": state,
            "District": district,
            "month": month,
            "average_min_price": round(min_p, 2),
            "average_max_price": round(max_p, 2),
            "average_modal_price": round(modal_price, 2),
            "price_record_count": rec_cnt,
            "_silver_processed_at": now_ts
        }
    silver_mandi_list = list(silver_mandi.values())
    write_csv(
        os.path.join(SILVER_DIR, "silver_mandi_prices.csv"),
        silver_mandi_list,
        ["State", "District", "month", "average_min_price", "average_max_price", "average_modal_price", "price_record_count", "_silver_processed_at"]
    )

    # Silver Weather: clean keys & round metrics
    silver_weather = {}
    for r in bronze_weather:
        state = clean_name(r.get("State", ""))
        district = clean_name(r.get("District", ""))
        month = r.get("month", "").strip()
        key = (state, district, month)

        silver_weather[key] = {
            "State": state,
            "District": district,
            "month": month,
            "temperature_2m_mean": round(float(r.get("temperature_2m_mean", 0) or 0), 2),
            "temperature_2m_max": round(float(r.get("temperature_2m_max", 0) or 0), 2),
            "temperature_2m_min": round(float(r.get("temperature_2m_min", 0) or 0), 2),
            "precipitation_sum": round(float(r.get("precipitation_sum", 0) or 0), 2),
            "relative_humidity_2m_mean": round(float(r.get("relative_humidity_2m_mean", 0) or 0), 2),
            "wind_speed_10m_max": round(float(r.get("wind_speed_10m_max", 0) or 0), 2),
            "_silver_processed_at": now_ts
        }
    silver_weather_list = list(silver_weather.values())
    write_csv(
        os.path.join(SILVER_DIR, "silver_weather.csv"),
        silver_weather_list,
        ["State", "District", "month", "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "relative_humidity_2m_mean", "wind_speed_10m_max", "_silver_processed_at"]
    )

    # Silver Arrivals: filter >= 0, deduplicate
    silver_arrivals = {}
    for r in bronze_arrivals:
        state = clean_name(r.get("State", ""))
        district = clean_name(r.get("District", ""))
        month = r.get("month", "").strip()
        key = (state, district, month)

        qty_str = r.get("arrival_quantity_tonnes", "")
        try:
            qty = float(qty_str) if qty_str else 0.0
        except ValueError:
            qty = 0.0

        if qty < 0:
            continue

        silver_arrivals[key] = {
            "State": state,
            "District": district,
            "month": month,
            "arrival_quantity_tonnes": round(qty, 2),
            "_silver_processed_at": now_ts
        }
    silver_arrivals_list = list(silver_arrivals.values())
    write_csv(
        os.path.join(SILVER_DIR, "silver_arrivals.csv"),
        silver_arrivals_list,
        ["State", "District", "month", "arrival_quantity_tonnes", "_silver_processed_at"]
    )
    # 3. GOLD LAYER (DIMENSIONAL INTEGRATION & MATCH TYPES)

    print("\n[GOLD LAYER] Integrating multi-source lakehouse tables...")

    all_keys = set(silver_mandi.keys()) | set(silver_weather.keys()) | set(silver_arrivals.keys())
    gold_rows = []
    match_counts = defaultdict(int)

    for key in sorted(all_keys):
        state, district, month = key
        m_item = silver_mandi.get(key)
        w_item = silver_weather.get(key)
        a_item = silver_arrivals.get(key)

        m_present = m_item is not None
        w_present = w_item is not None
        a_present = a_item is not None

        if m_present and w_present and a_present:
            match_type = "All three datasets"
        elif m_present and w_present:
            match_type = "Mandi + Weather"
        elif m_present and a_present:
            match_type = "Mandi + Arrivals"
        elif w_present and a_present:
            match_type = "Weather + Arrivals"
        elif m_present:
            match_type = "Mandi only"
        elif w_present:
            match_type = "Weather only"
        else:
            match_type = "Arrivals only"

        match_counts[match_type] += 1

        price_spread = ""
        if m_present:
            min_p = m_item["average_min_price"]
            max_p = m_item["average_max_price"]
            price_spread = round(max_p - min_p, 2)

        row = {
            "State": state,
            "District": district,
            "month": month,
            # Mandi metrics
            "average_min_price": m_item["average_min_price"] if m_present else "",
            "average_max_price": m_item["average_max_price"] if m_present else "",
            "average_modal_price": m_item["average_modal_price"] if m_present else "",
            "price_spread": price_spread,
            "price_record_count": m_item["price_record_count"] if m_present else "",
            "_mandi_present": m_present,
            # Weather metrics
            "temperature_2m_mean": w_item["temperature_2m_mean"] if w_present else "",
            "temperature_2m_max": w_item["temperature_2m_max"] if w_present else "",
            "temperature_2m_min": w_item["temperature_2m_min"] if w_present else "",
            "precipitation_sum": w_item["precipitation_sum"] if w_present else "",
            "relative_humidity_2m_mean": w_item["relative_humidity_2m_mean"] if w_present else "",
            "wind_speed_10m_max": w_item["wind_speed_10m_max"] if w_present else "",
            "_weather_present": w_present,
            # Arrival metrics
            "arrival_quantity_tonnes": a_item["arrival_quantity_tonnes"] if a_present else "",
            "_arrival_present": a_present,
            # Dimension tags
            "match_type": match_type,
            "_gold_generated_at": now_ts
        }
        gold_rows.append(row)

    gold_fields = [
        "State", "District", "month",
        "average_min_price", "average_max_price", "average_modal_price", "price_spread", "price_record_count", "_mandi_present",
        "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min", "precipitation_sum", "relative_humidity_2m_mean", "wind_speed_10m_max", "_weather_present",
        "arrival_quantity_tonnes", "_arrival_present",
        "match_type", "_gold_generated_at"
    ]
    gold_master_csv = os.path.join(GOLD_DIR, "gold_mandi_price_intelligence.csv")
    write_csv(gold_master_csv, gold_rows, gold_fields)

    # 4. GOLD ANALTICAL MARTS (FOR VANSH - POWER BI DASHBOARD)

    print("\n[GOLD MARTS] Creating specialized analytical marts for Power BI...")

    # Mart 1: State-level Monthly Aggregation
    state_groups = defaultdict(lambda: {"prices": [], "arrivals": 0.0, "obs_count": 0, "temps": [], "precip": 0.0})
    for r in gold_rows:
        s_key = (r["State"], r["month"])
        if r["average_modal_price"] != "":
            state_groups[s_key]["prices"].append(float(r["average_modal_price"]))
        if r["arrival_quantity_tonnes"] != "":
            state_groups[s_key]["arrivals"] += float(r["arrival_quantity_tonnes"])
        if r["price_record_count"] != "":
            state_groups[s_key]["obs_count"] += int(r["price_record_count"])
        if r["temperature_2m_mean"] != "":
            state_groups[s_key]["temps"].append(float(r["temperature_2m_mean"]))
        if r["precipitation_sum"] != "":
            state_groups[s_key]["precip"] += float(r["precipitation_sum"])

    mart_state_rows = []
    for (st, mo), data in sorted(state_groups.items()):
        avg_price = round(sum(data["prices"]) / len(data["prices"]), 2) if data["prices"] else ""
        avg_temp = round(sum(data["temps"]) / len(data["temps"]), 2) if data["temps"] else ""
        mart_state_rows.append({
            "State": st,
            "month": mo,
            "state_avg_modal_price": avg_price,
            "state_total_arrivals_tonnes": round(data["arrivals"], 2),
            "state_mandi_observations": data["obs_count"],
            "state_avg_temperature": avg_temp,
            "state_total_precipitation": round(data["precip"], 2)
        })
    write_csv(
        os.path.join(GOLD_DIR, "mart_state_monthly_trends.csv"),
        mart_state_rows,
        ["State", "month", "state_avg_modal_price", "state_total_arrivals_tonnes", "state_mandi_observations", "state_avg_temperature", "state_total_precipitation"]
    )

    # Mart 2: District Summary KPIs
    district_groups = defaultdict(lambda: {"prices": [], "min_prices": [], "max_prices": [], "arrivals": 0.0, "months": set()})
    for r in gold_rows:
        d_key = (r["State"], r["District"])
        district_groups[d_key]["months"].add(r["month"])
        if r["average_modal_price"] != "":
            district_groups[d_key]["prices"].append(float(r["average_modal_price"]))
        if r["average_min_price"] != "":
            district_groups[d_key]["min_prices"].append(float(r["average_min_price"]))
        if r["average_max_price"] != "":
            district_groups[d_key]["max_prices"].append(float(r["average_max_price"]))
        if r["arrival_quantity_tonnes"] != "":
            district_groups[d_key]["arrivals"] += float(r["arrival_quantity_tonnes"])

    mart_district_rows = []
    for (st, dist), data in district_groups.items():
        avg_price = round(sum(data["prices"]) / len(data["prices"]), 2) if data["prices"] else ""
        min_p = min(data["min_prices"]) if data["min_prices"] else ""
        max_p = max(data["max_prices"]) if data["max_prices"] else ""
        mart_district_rows.append({
            "State": st,
            "District": dist,
            "annual_avg_modal_price": avg_price,
            "min_observed_price": min_p,
            "max_observed_price": max_p,
            "annual_total_arrivals_tonnes": round(data["arrivals"], 2),
            "active_months_count": len(data["months"])
        })
    mart_district_rows.sort(key=lambda x: (x["annual_total_arrivals_tonnes"] or 0), reverse=True)
    write_csv(
        os.path.join(GOLD_DIR, "mart_district_summary.csv"),
        mart_district_rows,
        ["State", "District", "annual_avg_modal_price", "min_observed_price", "max_observed_price", "annual_total_arrivals_tonnes", "active_months_count"]
    )

    # Mart 3: Price vs Arrival Correlation Table (Mandi + Arrivals overlap)
    mart_corr_rows = []
    for r in gold_rows:
        if r["match_type"] == "Mandi + Arrivals":
            mart_corr_rows.append({
                "State": r["State"],
                "District": r["District"],
                "month": r["month"],
                "average_modal_price": r["average_modal_price"],
                "price_spread": r["price_spread"],
                "arrival_quantity_tonnes": r["arrival_quantity_tonnes"]
            })
    write_csv(
        os.path.join(GOLD_DIR, "mart_price_arrival_correlation.csv"),
        mart_corr_rows,
        ["State", "District", "month", "average_modal_price", "price_spread", "arrival_quantity_tonnes"])
    

    # 5. SUMMARY

    print("\n" + "=" * 65)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 65)
    for mtype, cnt in sorted(match_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {mtype:<20}: {cnt:>5} records")
    print(f"  {'TOTAL GOLD RECORDS':<20}: {len(gold_rows):>5} records")
    print("\n[SUCCESS] Medallion Pipeline executed. Ready for Databricks and Power BI!")


if __name__ == "__main__":
    run_pipeline()
