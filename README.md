# Mandi Price Intelligence

A Big Data engineering project that integrates agricultural mandi prices, wheat arrivals, and historical weather data to create a unified dataset for agricultural market analysis.

## 1. Project Overview

Agricultural commodity prices are influenced by several factors, including market demand, crop arrivals, and weather conditions.

This project collects real-world agricultural datasets from multiple sources and processes them using **Databricks and PySpark**. The datasets are cleaned, standardized, aggregated, and integrated to create a unified monthly dataset.

The project aims to build a scalable data pipeline that supports agricultural market analysis and provides a foundation for future predictive modelling.

## 2. Data Sources

The project uses three primary data sources:

| Dataset | Source | Coverage |
|---|---|---|
| Historical Mandi Prices | Hugging Face dataset sourced from AGMARKNET | January–December 2025 |
| Historical Weather | Open-Meteo Historical Weather API | Five districts in Tamil Nadu, 2025 |
| Wheat Arrivals | CEDA Agri-Market API | January–October 2025 |

### Dataset Details

- **Mandi prices:** 5,827,604 daily records covering 30 states, 572 districts, 5,423 markets, and 338 commodities.
- **Weather:** 1,825 daily records covering five districts in Tamil Nadu.
- **Wheat arrivals:** 2,370 monthly records covering 14 states and 288 districts.

Detailed source information is available in [`documentation/dataset_sources.md`](documentation/dataset_sources.md).

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Big Data Processing | Apache Spark (PySpark) |
| Development Platform | Databricks |
| Data Extraction | Python Requests and dataset downloads |
| Data Formats | CSV, JSON, Parquet |
| Cloud Object Storage | AWS S3 |
| Databricks Storage | Unity Catalog Volumes |
| Version Control | Git and GitHub |

## 4. Data Processing Pipeline

The project follows these major stages:

1. **Data Collection:** Collect mandi prices, weather observations, and wheat arrival quantities from external sources.
2. **Raw Storage:** Store the original datasets in Databricks Unity Catalog Volumes.
3. **Data Exploration:** Inspect schemas, record counts, missing values, duplicates, and data coverage.
4. **Data Cleaning:** Standardize state, district, and commodity names using PySpark.
5. **Aggregation:** Aggregate the datasets at the monthly State-District level.
6. **Data Integration:** Combine the datasets using a full outer join on State, District, and Month.
7. **Validation:** Check record counts, duplicate keys, missing values, and integration results.
8. **Processed Storage:** Save the processed datasets in Parquet format.
9. **Analysis:** Perform exploratory analysis to identify wheat price trends, arrival patterns, state-level differences, and district-level price volatility.

## 5. Processed Datasets

The project generates four primary processed datasets:

| Dataset | Description | Records |
|---|---|---:|
| `monthly_mandi_wheat_prices` | Monthly wheat price statistics | 2,995 |
| `monthly_wheat_arrivals` | Monthly wheat arrival quantities | 2,370 |
| `monthly_weather` | Monthly district-level weather statistics | 60 |
| `monthly_combined_intelligence` | Integrated dataset containing available source records | 3,798 |

The current Databricks processing workflow saves the processed datasets in Parquet format.

### Combined Dataset Fields

The integrated dataset contains:

- Mandi price metrics
- Wheat arrival quantities
- Weather metrics
- `Mandi_Present`
- `Arrivals_Present`
- `Weather_Present`
- `Match_Type`

The presence indicators identify which source datasets contributed information to each record.

## 6. Data Integration Results

The combined dataset contains the following records:

| Match Type | Records |
|---|---:|
| Mandi + Arrivals | 1,627 |
| Mandi Only | 1,368 |
| Arrivals Only | 743 |
| Weather Only | 60 |
| All Three Sources | 0 |
| **Total** | **3,798** |

### Integration Limitation

The three datasets have different geographical coverage.

The weather dataset covers five districts in Tamil Nadu, but there are no matching State-District keys between the weather data and the selected mandi price and wheat arrival datasets.

Consequently, no records match all three sources simultaneously.

A full outer join is used to preserve all available records without creating incorrect geographical matches.

Duplicate State-District-Month keys in the combined dataset: **0**.

## 7. Databricks Implementation

The project uses Databricks as its primary development and data processing environment.

### Workspace Organisation

The project workspace contains the following notebooks:

| Notebook | Purpose |
|---|---|
| `01_Data_Ingestion_and_Exploration` | Data loading, exploration, cleaning, standardization, aggregation, and integration |
| `02_Data_Analysis_and_Insights` | Exploratory data analysis and agricultural market insights |
| `03_Visualizations_and_Dashboard` | Planned visualization and dashboard development |

### Databricks Storage

Raw and processed datasets are maintained in a Unity Catalog Volume.

**Volume path:**

`/Volumes/workspace/default/mandi_project_data/`

**Processed data path:**

`/Volumes/workspace/default/mandi_project_data/processed/`

## 8. AWS S3 Storage

The project has an AWS S3 bucket configured for cloud object storage.

**Bucket name:**

`mandi-price-intelligence-2026-584310482678-ap-south-1-an`

**AWS Region:** Asia Pacific (Mumbai) – `ap-south-1`

Planned storage organisation:

```text
mandi-price-intelligence/
│
├── raw/
│   ├── Mandi price data
│   ├── Weather data
│   └── Wheat arrivals data
│
└── processed/
    ├── monthly_mandi_wheat_prices
    ├── monthly_weather
    ├── monthly_wheat_arrivals
    └── monthly_combined_intelligence
```

AWS credentials and secret access keys must never be committed to this repository.

## 9. Project Documentation

Detailed project documentation is available in the `documentation/` directory.

| File | Description |
|---|---|
| `dataset_sources.md` | Dataset sources, coverage, and references |
| `data_dictionary.md` | Dataset columns, definitions, and data quality details |
| `methodology.md` | Data collection, processing, and integration methodology |
| `problem_statement.md` | Problem definition and project objectives |
| `project_scope.md` | Project scope, deliverables, and limitations |
| `architecture.md` | Project architecture and data pipeline diagram |

## 10. Repository Structure

```text
Mandi-Price-Intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── documentation/
│   ├── architecture.md
│   ├── dataset_sources.md
│   ├── data_dictionary.md
│   ├── methodology.md
│   ├── problem_statement.md
│   └── project_scope.md
│
├── scripts/
│   ├── arrival_extraction.py
│   ├── arrival_validation.py
│   ├── convert_to_parquet.py
│   ├── data_integration.py
│   ├── mandi_extraction.py
│   └── weather_extraction.py
│
├── notebooks/
│   ├── 01_Data_Ingestion_and_Exploration
│   ├── 02_Data_Analysis_and_Insights
│   └── 03_Visualizations_and_Dashboard
│
├── .gitignore
├── README.md
└── requirements.txt
```

The `scripts/` directory contains the earlier Python extraction and processing scripts. The current primary processing workflow is maintained in Databricks notebooks.

## 11. Running the Project

The main processing workflow is executed through Databricks.

1. Open the Databricks workspace.
2. Open the `Mandi-Price-Intelligence` project folder.
3. Run `01_Data_Ingestion_and_Exploration` to load, clean, aggregate, and integrate the datasets.
4. Run `02_Data_Analysis_and_Insights` to perform exploratory analysis.
5. Use the processed Parquet datasets stored in the Unity Catalog Volume for further analysis.

The earlier local Python scripts can be executed separately when their required dependencies and input files are available.

## 12. Key Analytical Findings

Initial exploratory analysis produced the following observations:

- Average monthly wheat prices were highest in January 2025, at approximately ₹2,902.
- Average monthly wheat prices were lowest in May 2025, at approximately ₹2,520.
- Wheat arrivals peaked in April 2025, at approximately 14.34 million recorded quantity units.
- The monthly wheat price and arrival series showed a Pearson correlation of approximately -0.374 across ten months.
- District-level analysis identified differences in average prices and price volatility.

These are exploratory findings and do not establish causal relationships. The unit of crop arrival quantity is not confirmed in the available source metadata.

## 13. Future Enhancements

- Expand weather coverage to additional agricultural districts.
- Improve geographical matching across data sources.
- Develop interactive agricultural market dashboards.
- Explore machine learning models for wheat price forecasting.
- Automate periodic data extraction and processing.
- Improve cloud storage integration and pipeline orchestration.

## 14. Project Goal

The ultimate goal of Mandi Price Intelligence is to create a structured and scalable agricultural data pipeline that brings together market prices, crop arrivals, and weather information to support data-driven agricultural insights.
