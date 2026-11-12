# Databricks notebook source
# MAGIC %md
# MAGIC # Mandi Price Intelligence — Medallion Lakehouse Pipeline
# MAGIC ### Member 2: Data Engineering & ETL Pipeline (PySpark & Delta Lake)
# MAGIC 
# MAGIC **Architecture Overview:**
# MAGIC - **Bronze Layer:** Ingest raw feeds (Mandi Prices, Weather, Wheat Arrivals) preserving source fidelity with audit metadata (`ingestion_timestamp`, `source_file`).
# MAGIC - **Silver Layer:** Data quality enforcement, deduplication, schema conformation, geographic name standardisation (lowercase, trimmed whitespace), and domain range checks.
# MAGIC - **Gold Layer:** Business aggregation and multi-source dimensional joining (Mandi + Arrivals + Weather) partitioned and optimized for Power BI reporting and analytical modeling.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 0. Environment Setup & Configuration

# COMMAND ----------
import os
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, LongType, TimestampType, BooleanType
)

# Base Paths (configurable for DBFS / Unity Catalog Volumes / S3 / Local)
BASE_DIR = os.getenv("PIPELINE_BASE_DIR", "/FileStore/mandi-price-intelligence")
RAW_DIR = f"{BASE_DIR}/data/raw"
PROCESSED_DIR = f"{BASE_DIR}/data/processed"

DELTA_BASE = f"{BASE_DIR}/delta"
BRONZE_PATH = f"{DELTA_BASE}/bronze"
SILVER_PATH = f"{DELTA_BASE}/silver"
GOLD_PATH = f"{DELTA_BASE}/gold"

print(f"Bronze Path: {BRONZE_PATH}")
print(f"Silver Path: {SILVER_PATH}")
print(f"Gold Path:   {GOLD_PATH}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Bronze Layer: Raw Ingestion to Delta Lake
# MAGIC Ingest raw datasets as-is, attaching ingestion metadata (`_ingested_at`, `_source_file`).

# COMMAND ----------
# 1.1 Ingest Mandi Prices (Bronze)
# Can read either raw parquet/csv or pre-extracted records
try:
    df_raw_mandi = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{PROCESSED_DIR}/monthly_mandi_wheat_prices.csv")
    df_bronze_mandi = df_raw_mandi \
        .withColumn("_ingested_at", F.current_timestamp()) \
        .withColumn("_source_file", F.lit("monthly_mandi_wheat_prices.csv"))
    
    df_bronze_mandi.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{BRONZE_PATH}/mandi_prices")
    print(f"Bronze Mandi: {df_bronze_mandi.count()} rows ingested.")
except Exception as e:
    print(f"Bronze Mandi Ingestion Note: {e}")

# COMMAND ----------
# 1.2 Ingest Weather Data (Bronze)
try:
    df_raw_weather = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{PROCESSED_DIR}/monthly_weather.csv")
    df_bronze_weather = df_raw_weather \
        .withColumn("_ingested_at", F.current_timestamp()) \
        .withColumn("_source_file", F.lit("monthly_weather.csv"))
    
    df_bronze_weather.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{BRONZE_PATH}/weather")
    print(f"Bronze Weather: {df_bronze_weather.count()} rows ingested.")
except Exception as e:
    print(f"Bronze Weather Ingestion Note: {e}")

# COMMAND ----------
# 1.3 Ingest Wheat Arrivals (Bronze)
try:
    df_raw_arrivals = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{PROCESSED_DIR}/monthly_wheat_arrivals.csv")
    df_bronze_arrivals = df_raw_arrivals \
        .withColumn("_ingested_at", F.current_timestamp()) \
        .withColumn("_source_file", F.lit("monthly_wheat_arrivals.csv"))
    
    df_bronze_arrivals.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{BRONZE_PATH}/arrivals")
    print(f"Bronze Arrivals: {df_bronze_arrivals.count()} rows ingested.")
except Exception as e:
    print(f"Bronze Arrivals Ingestion Note: {e}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Silver Layer: Data Cleaning, Standardization & Validation
# MAGIC Standardize text keys (`State`, `District`), cast datatypes, validate boundaries (prices > 0, realistic temperatures), and deduplicate.

# COMMAND ----------
# Clean String Helper Function
def clean_spark_str(col_name):
    return F.lower(F.trim(F.regexp_replace(F.col(col_name), r"\s+", " ")))

# 2.1 Silver: Clean Mandi Prices
df_b_mandi = spark.read.format("delta").load(f"{BRONZE_PATH}/mandi_prices")

df_silver_mandi = df_b_mandi \
    .withColumn("State", clean_spark_str("State")) \
    .withColumn("District", clean_spark_str("District")) \
    .withColumn("month", F.trim(F.col("month"))) \
    .withColumn("average_min_price", F.col("average_min_price").cast(DoubleType())) \
    .withColumn("average_max_price", F.col("average_max_price").cast(DoubleType())) \
    .withColumn("average_modal_price", F.col("average_modal_price").cast(DoubleType())) \
    .withColumn("price_record_count", F.col("price_record_count").cast(LongType())) \
    .filter((F.col("average_modal_price").isNotNull()) & (F.col("average_modal_price") > 0)) \
    .dropDuplicates(["State", "District", "month"]) \
    .withColumn("_silver_processed_at", F.current_timestamp())

df_silver_mandi.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{SILVER_PATH}/mandi_prices")
print(f"Silver Mandi Prices written: {df_silver_mandi.count()} clean rows.")

# COMMAND ----------
# 2.2 Silver: Clean Weather Observations
df_b_weather = spark.read.format("delta").load(f"{BRONZE_PATH}/weather")

df_silver_weather = df_b_weather \
    .withColumn("State", clean_spark_str("State")) \
    .withColumn("District", clean_spark_str("District")) \
    .withColumn("month", F.trim(F.col("month"))) \
    .withColumn("temperature_2m_mean", F.col("temperature_2m_mean").cast(DoubleType())) \
    .withColumn("temperature_2m_max", F.col("temperature_2m_max").cast(DoubleType())) \
    .withColumn("temperature_2m_min", F.col("temperature_2m_min").cast(DoubleType())) \
    .withColumn("precipitation_sum", F.col("precipitation_sum").cast(DoubleType())) \
    .withColumn("relative_humidity_2m_mean", F.col("relative_humidity_2m_mean").cast(DoubleType())) \
    .withColumn("wind_speed_10m_max", F.col("wind_speed_10m_max").cast(DoubleType())) \
    .dropDuplicates(["State", "District", "month"]) \
    .withColumn("_silver_processed_at", F.current_timestamp())

df_silver_weather.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{SILVER_PATH}/weather")
print(f"Silver Weather written: {df_silver_weather.count()} clean rows.")

# COMMAND ----------
# 2.3 Silver: Clean Wheat Arrivals
df_b_arrivals = spark.read.format("delta").load(f"{BRONZE_PATH}/arrivals")

df_silver_arrivals = df_b_arrivals \
    .withColumn("State", clean_spark_str("State")) \
    .withColumn("District", clean_spark_str("District")) \
    .withColumn("month", F.trim(F.col("month"))) \
    .withColumn("arrival_quantity_tonnes", F.col("arrival_quantity_tonnes").cast(DoubleType())) \
    .filter((F.col("arrival_quantity_tonnes").isNotNull()) & (F.col("arrival_quantity_tonnes") >= 0)) \
    .dropDuplicates(["State", "District", "month"]) \
    .withColumn("_silver_processed_at", F.current_timestamp())

df_silver_arrivals.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{SILVER_PATH}/arrivals")
print(f"Silver Arrivals written: {df_silver_arrivals.count()} clean rows.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Gold Layer: Multi-Source Lakehouse Integration & Power BI Ready Tables
# MAGIC Perform outer join across the three silver domains by `State`, `District`, and `month`, assign lineage flags, and calculate key analytical metrics.

# COMMAND ----------
# 3.1 Load Silver Tables
s_mandi = spark.read.format("delta").load(f"{SILVER_PATH}/mandi_prices").select(
    "State", "District", "month", "average_min_price", "average_max_price", "average_modal_price", "price_record_count"
).withColumn("_mandi_present", F.lit(True))

s_weather = spark.read.format("delta").load(f"{SILVER_PATH}/weather").select(
    "State", "District", "month", "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
    "precipitation_sum", "relative_humidity_2m_mean", "wind_speed_10m_max"
).withColumn("_weather_present", F.lit(True))

s_arrivals = spark.read.format("delta").load(f"{SILVER_PATH}/arrivals").select(
    "State", "District", "month", "arrival_quantity_tonnes"
).withColumn("_arrival_present", F.lit(True))

# 3.2 Join Silver Tables (Full Outer Join across State, District, month)
gold_joined = s_mandi.join(s_weather, on=["State", "District", "month"], how="outer") \
                     .join(s_arrivals, on=["State", "District", "month"], how="outer")

# Fill presence boolean flags
gold_joined = gold_joined \
    .withColumn("_mandi_present", F.coalesce(F.col("_mandi_present"), F.lit(False))) \
    .withColumn("_weather_present", F.coalesce(F.col("_weather_present"), F.lit(False))) \
    .withColumn("_arrival_present", F.coalesce(F.col("_arrival_present"), F.lit(False)))

# Compute match_type category
gold_joined = gold_joined.withColumn(
    "match_type",
    F.when(F.col("_mandi_present") & F.col("_weather_present") & F.col("_arrival_present"), "All three datasets")
     .when(F.col("_mandi_present") & F.col("_weather_present"), "Mandi + Weather")
     .when(F.col("_mandi_present") & F.col("_arrival_present"), "Mandi + Arrivals")
     .when(F.col("_weather_present") & F.col("_arrival_present"), "Weather + Arrivals")
     .when(F.col("_mandi_present"), "Mandi only")
     .when(F.col("_weather_present"), "Weather only")
     .otherwise("Arrivals only")
)

# Price spread KPI
gold_joined = gold_joined.withColumn(
    "price_spread",
    F.when(F.col("average_max_price").isNotNull() & F.col("average_min_price").isNotNull(),
           F.col("average_max_price") - F.col("average_min_price")).otherwise(None)
)

# Add gold metadata timestamp
gold_final = gold_joined.withColumn("_gold_generated_at", F.current_timestamp())

# Write Gold table to Delta Lake partitioned by State
gold_final.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .partitionBy("State") \
    .save(f"{GOLD_PATH}/mandi_price_intelligence")

print(f"Gold table successfully created with {gold_final.count()} records.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Gold Data Marts for Vansh (Power BI Analytics)
# MAGIC Pre-calculate aggregated views that Power BI can consume directly for high-performance dashboarding.

# COMMAND ----------
# 4.1 State-Level Monthly Trend Mart
state_trends = gold_final.groupBy("State", "month").agg(
    F.avg("average_modal_price").alias("state_avg_modal_price"),
    F.sum("arrival_quantity_tonnes").alias("state_total_arrivals"),
    F.sum("price_record_count").alias("total_mandi_observations"),
    F.avg("temperature_2m_mean").alias("state_avg_temperature"),
    F.avg("precipitation_sum").alias("state_avg_precipitation")
).orderBy("State", "month")

state_trends.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/mart_state_monthly_trends")
print(f"State Monthly Trends Mart created: {state_trends.count()} rows.")

# 4.2 District Performance KPI Summary Mart
district_summary = gold_final.groupBy("State", "District").agg(
    F.avg("average_modal_price").alias("annual_avg_modal_price"),
    F.min("average_min_price").alias("min_observed_price"),
    F.max("average_max_price").alias("max_observed_price"),
    F.sum("arrival_quantity_tonnes").alias("annual_total_arrivals"),
    F.count("month").alias("active_months_count")
).orderBy(F.col("annual_total_arrivals").desc_nulls_last())

district_summary.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/mart_district_summary")
print(f"District Summary Mart created: {district_summary.count()} rows.")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Validation & Quality Audit

# COMMAND ----------
display(gold_final.groupBy("match_type").count().orderBy(F.col("count").desc()))

# COMMAND ----------
# Sample output for verification
display(gold_final.filter(F.col("match_type") == "Mandi + Arrivals").limit(10))
