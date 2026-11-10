# Project Scope

## 1. Project Overview

Mandi Price Intelligence is a data-driven agricultural market intelligence project that brings together historical mandi prices, crop arrival quantities, and weather information.

The project focuses on collecting data from multiple sources, storing it systematically, preparing it for analysis, and integrating available information at a monthly State-District level.

## 2. Objectives

1. Collect historical mandi price data from a reliable agricultural data source.
2. Retrieve historical weather information using a weather API.
3. Collect crop arrival quantity data from an agricultural market data source.
4. Develop Python scripts for data extraction and processing.
5. Store original datasets in an organised raw-data structure.
6. Clean and standardise geographical and temporal fields.
7. Aggregate daily and source-level observations into monthly datasets.
8. Integrate datasets using State, District, and month as matching keys.
9. Retain unmatched records and identify source availability using presence flags.
10. Store processed datasets in CSV and Parquet formats.
11. Use Amazon S3 for cloud-based storage of raw and processed datasets.
12. Maintain technical documentation to support reproducibility and future development.

## 3. Data Sources and Coverage

| Dataset | Source | Coverage |
|---|---|---|
| Historical Mandi Daily Prices | Hugging Face dataset based on AGMARKNET | India, January-December 2025; wheat extracted for processing |
| Historical Weather | Open-Meteo Historical Weather API | Five districts of Tamil Nadu, January-December 2025 |
| Wheat Crop Arrivals | CEDA Agri-Market, based on AGMARKNET | 14 states and 288 districts, January-October 2025 |

The datasets have different geographical and temporal coverage. Their integration is therefore limited to matching State-District-month combinations.

## 4. Functional Scope

### 4.1 Data Collection

- Obtain mandi price data in Parquet format.
- Retrieve historical weather observations through the Open-Meteo API.
- Extract wheat arrival quantities through the CEDA Agri-Market API.
- Preserve original downloaded data in the raw-data directory.

### 4.2 Data Storage

- Organise raw and processed datasets separately.
- Maintain CSV and Parquet versions of processed datasets.
- Upload raw and processed data to the configured Amazon S3 bucket.

### 4.3 Data Processing

- Standardise State and District names.
- Convert observations to a consistent monthly time identifier.
- Aggregate mandi prices, weather observations, and wheat arrivals.
- Integrate datasets using State, District, and month.
- Retain unmatched records using an outer join.
- Add source-presence flags and a match-type classification.

### 4.4 Documentation and Project Organisation

- Document dataset sources, collection methods, schemas, and limitations.
- Maintain the problem statement and project scope.
- Prepare an architecture diagram.
- Maintain a README and organised GitHub repository.
- Contribute to the final project report and presentation.

## 5. Current Dataset Coverage

The current processed outputs contain:

| Processed Dataset | Records |
|---|---:|
| Monthly Mandi Wheat Prices | 2,996 |
| Monthly Weather | 60 |
| Monthly Wheat Arrivals | 2,370 |
| Monthly Combined Intelligence | 3,799 |

The integrated dataset contains 1,627 Mandi + Arrivals matches, 1,369 Mandi-only records, 743 Arrivals-only records, and 60 Weather-only records.

There are currently no records matching all three sources. This is a source-coverage limitation and is documented rather than hidden through forced matching.

## 6. Out of Scope and Limitations

- The current dataset does not provide complete geographical coverage across all three sources.
- The current integration does not establish causal relationships between weather, crop arrivals, and prices.
- The project does not guarantee real-time mandi prices or weather updates.
- Predictive modelling and dashboard implementation are downstream project activities and should only be described as completed when implemented and validated by the responsible team members.
- Data quality and analytical conclusions are limited by the coverage, accuracy, and availability of the source datasets.

## 7. Expected Deliverables

- Raw datasets from the three sources.
- Python extraction and processing scripts.
- Monthly processed CSV and Parquet datasets.
- Integrated monthly intelligence dataset.
- Amazon S3 storage structure containing raw and processed data.
- Dataset source documentation and data dictionary.
- Problem statement and project scope documentation.
- Project architecture diagram.
- GitHub repository and README.
- Final project report and presentation.

## 8. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Data Formats | CSV, Parquet, JSON |
| Parquet Support | PyArrow |
| Data Sources | Hugging Face, Open-Meteo, CEDA Agri-Market |
| Cloud Object Storage | Amazon S3 |
| Cloud CLI | AWS CLI |
| Version Control | Git and GitHub |
