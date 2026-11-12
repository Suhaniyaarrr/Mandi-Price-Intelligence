# Project Scope

## 1. Project Overview

Mandi Price Intelligence is a Big Data engineering project that brings together historical mandi prices, wheat arrival quantities, and weather information.

The project focuses on collecting data from multiple sources, storing it systematically, processing it using Databricks and PySpark, and integrating available information at a monthly State-District level.

The resulting datasets provide a foundation for agricultural market analysis and future predictive modelling.

## 2. Objectives

1. Collect historical mandi price data from a reliable agricultural data source.
2. Retrieve historical weather information using a weather API.
3. Collect wheat arrival quantity data from an agricultural market data source.
4. Develop data extraction workflows using Python and APIs.
5. Store original datasets in an organised raw-data structure.
6. Clean and standardise geographical and temporal fields using PySpark.
7. Aggregate observations into monthly datasets.
8. Integrate datasets using State, District, and Month as matching keys.
9. Retain unmatched records and identify source availability using presence flags.
10. Store processed datasets in Parquet format.
11. Use Databricks Unity Catalog Volumes and configured Amazon S3 storage.
12. Maintain technical documentation to support reproducibility and future development.

## 3. Data Sources and Coverage

| Dataset | Source | Coverage |
|---|---|---|
| Historical Mandi Daily Prices | Hugging Face dataset based on AGMARKNET | India, January–December 2025; Wheat selected for processing |
| Historical Weather | Open-Meteo Historical Weather API | Five districts of Tamil Nadu, January–December 2025 |
| Wheat Crop Arrivals | CEDA Agri-Market API | 14 states and 288 districts, January–October 2025 |

The datasets have different geographical and temporal coverage. Integration is performed using matching State-District-Month combinations.

## 4. Functional Scope

### 4.1 Data Collection

- Obtain mandi price data in Parquet format.
- Retrieve historical weather observations through the Open-Meteo API.
- Extract wheat arrival quantities through the CEDA Agri-Market API.
- Load the collected datasets into the Databricks processing environment.

### 4.2 Data Storage

- Organise raw and processed datasets separately.
- Maintain raw datasets in a Databricks Unity Catalog Volume.
- Store processed datasets in Parquet format.
- Use the configured Amazon S3 bucket for cloud object storage.

### 4.3 Data Processing

- Explore schemas, record counts, missing values, and duplicates.
- Standardise State, District, and Commodity names.
- Convert observations to a consistent monthly time identifier.
- Filter mandi records for Wheat.
- Aggregate mandi prices, weather observations, and wheat arrivals.
- Integrate datasets using State, District, and Month.
- Retain unmatched records using a full outer join.
- Add source-presence flags and a `Match_Type` classification.
- Validate the resulting datasets for duplicate keys and data quality issues.

### 4.4 Data Analysis

- Analyse monthly wheat price trends.
- Examine monthly wheat arrival patterns.
- Compare average prices across states and districts.
- Identify district-level price volatility.
- Explore relationships between prices and arrivals, while considering data coverage limitations.

### 4.5 Documentation and Project Organisation

- Document dataset sources, collection methods, schemas, and limitations.
- Maintain the problem statement and project scope.
- Prepare an architecture diagram.
- Maintain a README and organised GitHub repository.
- Contribute to the final project report and presentation.

## 5. Current Dataset Coverage

The current processed outputs contain:

| Processed Dataset | Records |
|---|---:|
| Monthly Mandi Wheat Prices | 2,995 |
| Monthly Weather | 60 |
| Monthly Wheat Arrivals | 2,370 |
| Monthly Combined Intelligence | 3,798 |

The integrated dataset contains:

| Match Type | Records |
|---|---:|
| Mandi + Arrivals | 1,627 |
| Mandi Only | 1,368 |
| Arrivals Only | 743 |
| Weather Only | 60 |
| All Three Sources | 0 |
| **Total** | **3,798** |

There are currently no records matching all three sources. This is a source-coverage limitation and is documented rather than hidden through forced matching.

## 6. Storage Locations

**Databricks Unity Catalog Volume:**

`/Volumes/workspace/default/mandi_project_data/`

**Processed datasets:**

`/Volumes/workspace/default/mandi_project_data/processed/`

**Configured AWS S3 bucket:**

`mandi-price-intelligence-2026-584310482678-ap-south-1-an`

**AWS Region:** `ap-south-1`

## 7. Out of Scope and Limitations

- The current datasets do not provide complete geographical coverage across all three sources.
- The current integration does not establish causal relationships between weather, crop arrivals, and prices.
- The project does not guarantee real-time mandi prices or weather updates.
- The unit of the wheat arrival quantity field has not been confirmed.
- Predictive modelling and dashboard implementation are downstream activities and should only be described as completed after implementation and validation.
- Data quality and analytical conclusions are limited by the coverage, accuracy, and availability of the source datasets.

## 8. Expected Deliverables

- Raw datasets from the three sources.
- Python-based data extraction workflows.
- Databricks notebooks for ingestion, exploration, processing, integration, and analysis.
- Monthly processed Parquet datasets.
- Integrated monthly intelligence dataset.
- Databricks Unity Catalog storage structure.
- Configured Amazon S3 cloud storage.
- Dataset source documentation and data dictionary.
- Problem statement and project scope documentation.
- Project architecture diagram.
- GitHub repository and README.
- Final project report and presentation.

## 9. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Big Data Processing | Apache Spark (PySpark) |
| Development Environment | Databricks |
| Data Formats | CSV, Parquet, JSON |
| Data Sources | Hugging Face, Open-Meteo, CEDA Agri-Market |
| Databricks Storage | Unity Catalog Volumes |
| Cloud Object Storage | Amazon S3 |
| Version Control | Git and GitHub |