# Data Dictionary - Mandi Price Intelligence

## 1. Introduction

This document describes the raw and processed datasets used in the Mandi Price Intelligence project. It covers dataset attributes, column definitions, data types, geographical and temporal coverage, data quality, integration methodology, and limitations.

The project uses three primary data sources:

1. Historical Mandi Daily Prices
2. Historical Weather Data
3. Monthly Crop Arrival Quantities

The datasets are cleaned, standardized, aggregated, and integrated using Databricks and PySpark to create monthly agricultural market intelligence datasets.

---

## 2. Dataset 1: Historical Mandi Daily Prices

### 2.1 Dataset Overview

| Attribute | Details |
|---|---|
| Dataset Name | India Mandi Daily Prices |
| Source | Hugging Face |
| Original Source | AGMARKNET |
| Dataset URL | https://huggingface.co/datasets/DHIVAKARNAIDUSUNKARI/mandi-india-daily-prices-2001-2026 |
| File Name | `mandi_daily_2025.parquet` |
| File Format | Parquet |
| Total Records | 5,827,604 |
| Total Columns | 11 |
| Time Coverage | 2025-01-01 to 2025-12-31 |
| States | 30 |
| Districts | 572 |
| Markets | 5,423 |
| Commodities | 338 |

### 2.2 Column Definitions

| Column Name | Description | Data Type |
|---|---|---|
| `State` | Name of the Indian state | String |
| `District` | Name of the district | String |
| `Market` | Agricultural wholesale market or mandi name | String |
| `Commodity` | Agricultural commodity name | String |
| `Variety` | Variety of the commodity | String |
| `Grade` | Quality grade of the commodity | String |
| `Arrival_Date` | Date of the recorded market price | Date |
| `Min_Price` | Minimum recorded commodity price | Numeric |
| `Max_Price` | Maximum recorded commodity price | Numeric |
| `Modal_Price` | Modal or most frequently reported market price | Numeric |
| `Commodity_Code` | Identifier assigned to the commodity | Integer |

### 2.3 Data Quality Summary

- Total records: 5,827,604
- Missing values in `Min_Price`: 4,418
- Missing values in `Max_Price`: 4,718
- Missing values in `Modal_Price`: 0
- Duplicate records: 0

Missing minimum and maximum prices are retained and handled appropriately during processing.

### 2.4 Limitations

- The downloaded dataset covers 2025 only.
- Some minimum and maximum price values are missing.
- Market and commodity names may require standardization.
- The raw dataset contains multiple commodities; the current price analysis filters records to Wheat.

---

## 3. Dataset 2: Historical Weather Data

### 3.1 Dataset Overview

| Attribute | Details |
|---|---|
| Dataset Name | Historical Weather Data |
| Source | Open-Meteo |
| API | Historical Weather API |
| API Endpoint | https://archive-api.open-meteo.com/v1/archive |
| Documentation | https://open-meteo.com/en/docs/historical-weather-api |
| File Name | `weather_tamil_nadu_2025.csv` |
| File Format | CSV |
| Total Records | 1,825 |
| Total Columns | 11 |
| Time Coverage | 2025-01-01 to 2025-12-31 |
| Geographical Coverage | 5 districts of Tamil Nadu |
| API Authentication | No API key required |
| Extraction Method | Python Requests library |

### 3.2 Districts Covered

- Salem
- Coimbatore
- Tiruvannamalai
- Madurai
- Vellore

### 3.3 Column Definitions

| Column Name | Description | Data Type |
|---|---|---|
| `time` | Date of the weather observation | Date |
| `temperature_2m_mean` | Mean daily temperature at 2 metres | Numeric |
| `temperature_2m_max` | Maximum daily temperature at 2 metres | Numeric |
| `temperature_2m_min` | Minimum daily temperature at 2 metres | Numeric |
| `precipitation_sum` | Total daily precipitation | Numeric |
| `relative_humidity_2m_mean` | Mean daily relative humidity | Numeric |
| `wind_speed_10m_max` | Maximum daily wind speed at 10 metres | Numeric |
| `District` | Name of the district | String |
| `State` | Name of the state | String |
| `Latitude` | Latitude coordinate used for data retrieval | Numeric |
| `Longitude` | Longitude coordinate used for data retrieval | Numeric |

### 3.4 Data Quality Summary

- Total records: 1,825
- Records per district: 365
- Missing values: 0
- Duplicate records: 0
- Districts covered: 5
- Daily weather observations are available throughout 2025.

### 3.5 Limitations

- Weather data covers only five districts of Tamil Nadu.
- Coordinates represent selected district-level locations, not individual mandi locations.
- Weather observations may not capture local variations within a district.
- The current weather dataset has no common State-District matches with the wheat mandi price and crop-arrival datasets.

---

## 4. Dataset 3: Monthly Crop Arrival Quantities

### 4.1 Dataset Overview

| Attribute | Details |
|---|---|
| Dataset Name | Monthly Crop Arrival Quantities |
| Source | CEDA Agri-Market, Ashoka University |
| Original Source | AGMARKNET |
| Portal | https://agmarknet.ceda.ashoka.edu.in/ |
| API Endpoint | https://agmarknet.ceda.ashoka.edu.in/api/quantities |
| Commodity | Wheat |
| Extraction Method | Python Requests library using an API request |
| JSON File | `crop_arrivals_wheat_2025.json` |
| Total Records | 2,370 |
| Total Columns | 7 |
| Actual Time Coverage | January to October 2025 |
| States | 14 |
| Districts | 288 |
| Data Granularity | Monthly, district-level |
| Quantity Unit | Not confirmed in available source metadata |

### 4.2 Column Definitions

| Column Name | Description | Data Type |
|---|---|---|
| `t` | Month of the crop-arrival record in YYYY-MM format | String |
| `cmdty` | Name of the agricultural commodity | String |
| `district_id` | District identifier provided by CEDA | Integer |
| `district` | Name of the district | String |
| `state_id` | State identifier provided by CEDA | Integer |
| `state` | Name of the state | String |
| `qty` | Recorded crop-arrival quantity; source unit unconfirmed | Numeric |

### 4.3 Data Quality Summary

- Total records: 2,370
- Total columns: 7
- Missing values: 0
- Duplicate records: 0
- States covered: 14
- Districts covered: 288
- Monthly coverage: January to October 2025

### 4.4 Limitations

- Data is aggregated monthly at district level, not daily or individual mandi level.
- Although the extraction request covered January to December 2025, returned records cover January to October only.
- The dataset is AGMARKNET-derived and is complementary to the mandi price dataset rather than a fully independent source.
- The quantity unit must be verified before interpreting absolute arrival quantities.

---

## 5. Processed Datasets

The raw datasets are processed using Databricks and PySpark. Processing includes data cleaning, standardization, filtering, monthly aggregation, and integration.

The authoritative processed datasets are stored in Parquet format in the Databricks Unity Catalog Volume.

**Storage path:**

`/Volumes/workspace/default/mandi_project_data/processed/`

### 5.1 Monthly Mandi Wheat Prices

| Attribute | Details |
|---|---|
| Dataset Name | Monthly Mandi Wheat Prices |
| Output Name | `monthly_mandi_wheat_prices` |
| Records | 2,995 |
| Granularity | Monthly, State-District level |
| Source | Historical Mandi Daily Prices |
| Filter | Wheat |
| Format | Parquet |

The dataset contains monthly aggregated wheat price information.

| Column Name | Description |
|---|---|
| `State` | Standardized state name |
| `District` | Standardized district name |
| `Month` | Month in YYYY-MM format |
| `Average_Min_Price` | Monthly average of minimum prices |
| `Average_Max_Price` | Monthly average of maximum prices |
| `Average_Modal_Price` | Monthly average of modal prices |
| `Price_Record_Count` | Number of mandi price records used in aggregation |

### 5.2 Monthly Weather

| Attribute | Details |
|---|---|
| Dataset Name | Monthly Weather |
| Output Name | `monthly_weather` |
| Records | 60 |
| Granularity | Monthly, State-District level |
| Source | Open-Meteo Historical Weather API |
| Format | Parquet |

Daily weather observations are aggregated to monthly district-level values.

| Column Name | Description |
|---|---|
| `State` | State name |
| `District` | District name |
| `Month` | Month in YYYY-MM format |
| `Average_Temperature` | Monthly average temperature |
| `Average_Max_Temperature` | Monthly average of daily maximum temperatures |
| `Average_Min_Temperature` | Monthly average of daily minimum temperatures |
| `Total_Precipitation` | Monthly precipitation total |
| `Average_Humidity` | Monthly average relative humidity |
| `Average_Wind_Speed` | Monthly average of daily maximum wind speeds |

### 5.3 Monthly Wheat Arrivals

| Attribute | Details |
|---|---|
| Dataset Name | Monthly Wheat Arrivals |
| Output Name | `monthly_wheat_arrivals` |
| Records | 2,370 |
| Granularity | Monthly, State-District level |
| Source | CEDA Agri-Market |
| Commodity | Wheat |
| Format | Parquet |

The dataset contains monthly aggregated wheat arrival quantities.

| Column Name | Description |
|---|---|
| `State` | Standardized state name |
| `District` | Standardized district name |
| `Month` | Month in YYYY-MM format |
| `Arrival_Quantity` | Total recorded wheat arrival quantity; source unit unconfirmed |

### 5.4 Monthly Combined Intelligence

| Attribute | Details |
|---|---|
| Dataset Name | Monthly Combined Intelligence |
| Output Name | `monthly_combined_intelligence` |
| Records | 3,798 |
| Columns | 18 |
| Granularity | Monthly, State-District level |
| Integration Method | Full outer join |
| Format | Parquet |

This is the main integrated dataset. It combines monthly mandi wheat prices, crop arrivals, and weather information wherever geographical and temporal matching is possible.

A full outer join retains records even when information from one or more sources is unavailable.

| Column Name | Description |
|---|---|
| `State` | Standardized state name |
| `District` | Standardized district name |
| `Month` | Month in YYYY-MM format |
| `Average_Min_Price` | Monthly average minimum wheat price |
| `Average_Max_Price` | Monthly average maximum wheat price |
| `Average_Modal_Price` | Monthly average modal wheat price |
| `Price_Record_Count` | Number of mandi price records |
| `Total_Arrival_Quantity` | Monthly wheat arrival quantity; source unit unconfirmed |
| `Average_Temperature` | Monthly average temperature |
| `Average_Max_Temperature` | Monthly average of daily maximum temperatures |
| `Average_Min_Temperature` | Monthly average of daily minimum temperatures |
| `Total_Precipitation` | Monthly precipitation total |
| `Average_Humidity` | Monthly average relative humidity |
| `Average_Wind_Speed` | Monthly average of daily maximum wind speeds |
| `Mandi_Present` | Boolean flag indicating mandi data availability |
| `Arrivals_Present` | Boolean flag indicating arrival data availability |
| `Weather_Present` | Boolean flag indicating weather data availability |
| `Match_Type` | Identifies which source datasets are available for a record |

### 5.5 Integration Results

The integration was performed using State, District, and Month as matching keys after standardizing state and district names.

| Match Type | Records |
|---|---:|
| Mandi + Arrivals | 1,627 |
| Mandi only | 1,368 |
| Arrivals only | 743 |
| Weather only | 60 |
| All three sources | 0 |
| **Total** | **3,798** |

No records matched across all three sources.

This is a source-coverage limitation. The available weather dataset covers five Tamil Nadu districts, while the selected wheat price and arrival datasets have no matching State-District keys with the weather dataset.

The full outer join retains unmatched records instead of forcing incorrect geographical matches.

Duplicate State-District-Month keys in the combined dataset: 0.

---

## 6. Data Integration Methodology

The integration process follows these steps:

1. Load the raw Parquet, JSON, and CSV datasets into Databricks.
2. Inspect schemas, record counts, missing values, and duplicate records using PySpark.
3. Standardize state, district, and commodity names.
4. Convert date information into a common monthly format.
5. Filter the mandi price dataset to Wheat.
6. Aggregate daily mandi price observations by State, District, and Month.
7. Aggregate daily weather observations by State, District, and Month.
8. Aggregate wheat arrival quantities by State, District, and Month.
9. Combine the processed datasets using a full outer join.
10. Add source-presence indicators and a `Match_Type` field.
11. Validate record counts and duplicate integration keys.
12. Save the processed datasets in Parquet format.

### Integration Keys

- `State`
- `District`
- `Month`

The original raw datasets are retained separately from processed datasets.

---

## 7. Data Quality and General Limitations

- Raw datasets originate from different sources and have different geographical and temporal coverage.
- State and district names may differ in spelling or formatting.
- Weather observations are limited to five Tamil Nadu districts.
- Crop-arrival records cover January to October 2025.
- Missing mandi minimum and maximum prices require appropriate handling during analysis.
- No three-way geographical matches currently exist between the selected datasets.
- The integrated dataset retains unmatched records, so missing values in source-specific fields are expected.
- The crop-arrival quantity unit is not confirmed in the available source metadata.
- Monthly averages are based on available observations and may have different district coverage across months.

---

## 8. Storage and File Organisation

The project maintains separate directories for raw and processed data.

| Directory | Purpose |
|---|---|
| `data/raw/` | Original datasets collected from external sources |
| `data/processed/` | Processed datasets maintained in the GitHub repository |
| `scripts/` | Python extraction and data-processing scripts |
| `documentation/` | Dataset metadata and project documentation |
| `notebooks/` | Databricks notebooks used for processing and analysis |

### Databricks Storage

Raw and processed datasets are stored in the project's Unity Catalog Volume.

| Attribute | Details |
|---|---|
| Platform | Databricks |
| Volume Path | `/Volumes/workspace/default/mandi_project_data/` |
| Raw Data Path | `/Volumes/workspace/default/mandi_project_data/` |
| Processed Data Path | `/Volumes/workspace/default/mandi_project_data/processed/` |

### AWS Cloud Storage

The project also has an AWS S3 bucket configured for cloud storage.

| Attribute | Details |
|---|---|
| Cloud Provider | Amazon Web Services |
| Service | Amazon S3 |
| Bucket | `mandi-price-intelligence-2026-584310482678-ap-south-1-an` |
| Region | `ap-south-1` (Asia Pacific - Mumbai) |
| Raw Prefix | `raw/` |
| Processed Prefix | `processed/` |

---

## 9. General Notes

- Original datasets should remain unchanged.
- Cleaning and transformation should be performed separately.
- Parquet files provide columnar storage suitable for analytical workloads.
- Dataset metadata should be updated whenever new data is extracted or processed.
- AWS credentials and secret access keys must never be committed to the GitHub repository.
- Databricks notebooks are the primary record of the current processing workflow.