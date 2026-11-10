@'
# Data Dictionary - Mandi Price Intelligence

## 1. Introduction

This document describes the raw and processed datasets used in the Mandi Price Intelligence project. It covers dataset attributes, column definitions, data types, geographical and temporal coverage, data quality, integration methodology, and limitations.

The project uses three primary data sources:

1. Historical Mandi Daily Prices
2. Historical Weather Data
3. Monthly Crop Arrival Quantities

The datasets are cleaned, aggregated, and integrated to create monthly agricultural market intelligence datasets.

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
| Storage Location | `data/raw/` |
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
| `Arrival_Date` | Date of the recorded market price | Date/String |
| `Min_Price` | Minimum recorded commodity price | Numeric |
| `Max_Price` | Maximum recorded commodity price | Numeric |
| `Modal_Price` | Modal or most frequently reported market price | Numeric |
| `Commodity_Code` | Identifier assigned to the commodity | Integer |

### 2.3 Data Quality Summary

- Total records: 5,827,604
- Missing values in `Min_Price`: 4,418
- Missing values in `Max_Price`: 4,718
- Duplicate records: 0
- Missing price values are retained for appropriate handling during analysis.

### 2.4 Limitations

- The downloaded and validated dataset covers 2025 only.
- Some minimum and maximum price values are missing.
- Market and commodity names may require standardisation before analysis and integration.
- The dataset contains multiple commodities; the current wheat price analysis filters records to Wheat.

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
| Storage Location | `data/raw/` |
| File Format | CSV |
| Total Records | 1,825 |
| Total Columns | 11 |
| Time Coverage | 2025-01-01 to 2025-12-31 |
| Geographical Coverage | 5 districts of Tamil Nadu |
| API Authentication | No API key required |

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
- Districts covered: 5
- Daily weather observations are available throughout 2025.

### 3.5 Limitations

- Weather data covers only five districts of Tamil Nadu.
- Coordinates represent district-level locations, not individual mandi locations.
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
| Extraction Method | Python Requests library using POST |
| JSON File | `crop_arrivals_wheat_2025.json` |
| CSV File | `crop_arrivals.csv` |
| Storage Location | `data/raw/` |
| Total Records | 2,370 |
| Total Columns | 7 |
| Actual Time Coverage | January to October 2025 |
| States | 14 |
| Districts | 288 |
| Data Granularity | Monthly, district-level |
| Quantity Unit | Tonnes |

### 4.2 Column Definitions

| Column Name | Description | Data Type |
|---|---|---|
| `t` | Month of the crop-arrival record in YYYY-MM format | String |
| `cmdty` | Name of the agricultural commodity | String |
| `district_id` | District identifier provided by CEDA | Integer |
| `district` | Name of the district | String |
| `state_id` | State identifier provided by CEDA | Integer |
| `state` | Name of the state | String |
| `qty` | Recorded crop-arrival quantity in tonnes | Numeric |

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

---

## 5. Processed Datasets

The raw datasets are cleaned, standardised, aggregated, and integrated using Python scripts. All four processed datasets are available in CSV and Parquet formats.

### 5.1 Monthly Mandi Wheat Prices

| Attribute | Details |
|---|---|
| File Names | `monthly_mandi_wheat_prices.csv` and `monthly_mandi_wheat_prices.parquet` |
| Records | 2,996 |
| Columns | 8 |
| Granularity | Monthly, State-District level |
| Source | Historical Mandi Daily Prices |
| Filter | Wheat |

The dataset contains monthly aggregated wheat price information.

| Column Name | Description |
|---|---|
| `State` | State name |
| `District` | District name |
| `month` | Month in YYYY-MM format |
| `average_min_price` | Monthly average of minimum prices |
| `average_max_price` | Monthly average of maximum prices |
| `average_modal_price` | Monthly average of modal prices |
| `price_record_count` | Number of daily mandi price records used in aggregation |
| `_mandi_present` | Boolean flag indicating the presence of mandi price data |

### 5.2 Monthly Weather

| Attribute | Details |
|---|---|
| File Names | `monthly_weather.csv` and `monthly_weather.parquet` |
| Records | 60 |
| Columns | 10 |
| Granularity | Monthly, State-District level |
| Source | Open-Meteo Historical Weather API |

Daily weather observations are aggregated to monthly district-level values.

| Column Name | Description |
|---|---|
| `State` | State name |
| `District` | District name |
| `month` | Month in YYYY-MM format |
| `temperature_2m_mean` | Monthly mean of daily mean temperatures |
| `temperature_2m_max` | Monthly mean of daily maximum temperatures |
| `temperature_2m_min` | Monthly mean of daily minimum temperatures |
| `precipitation_sum` | Monthly precipitation total |
| `relative_humidity_2m_mean` | Monthly mean relative humidity |
| `wind_speed_10m_max` | Monthly mean of daily maximum wind speeds |
| `_weather_present` | Boolean flag indicating the presence of weather data |

### 5.3 Monthly Wheat Arrivals

| Attribute | Details |
|---|---|
| File Names | `monthly_wheat_arrivals.csv` and `monthly_wheat_arrivals.parquet` |
| Records | 2,370 |
| Columns | 5 |
| Granularity | Monthly, State-District level |
| Source | CEDA Agri-Market |
| Commodity | Wheat |

The dataset contains monthly aggregated wheat arrival quantities in tonnes.

| Column Name | Description |
|---|---|
| `State` | State name |
| `District` | District name |
| `month` | Month in YYYY-MM format |
| `arrival_quantity_tonnes` | Total wheat arrival quantity in tonnes |
| `_arrival_present` | Boolean flag indicating the presence of arrival data |

### 5.4 Monthly Combined Intelligence

| Attribute | Details |
|---|---|
| File Names | `monthly_combined_intelligence.csv` and `monthly_combined_intelligence.parquet` |
| Records | 3,799 |
| Columns | 18 |
| Granularity | Monthly, State-District level |
| Integration Method | Full outer join |

This is the main integrated dataset. It combines monthly mandi wheat prices, crop arrivals, and weather information wherever geographical and temporal matching is possible. A full outer join retains records even when information from one or more sources is unavailable.

| Column Name | Description |
|---|---|
| `State` | State name |
| `District` | District name |
| `month` | Month in YYYY-MM format |
| `average_min_price` | Monthly average minimum wheat price |
| `average_max_price` | Monthly average maximum wheat price |
| `average_modal_price` | Monthly average modal wheat price |
| `price_record_count` | Number of mandi price records |
| `_mandi_present` | Boolean flag indicating mandi data availability |
| `temperature_2m_mean` | Monthly mean temperature |
| `temperature_2m_max` | Monthly mean of daily maximum temperatures |
| `temperature_2m_min` | Monthly mean of daily minimum temperatures |
| `precipitation_sum` | Monthly precipitation total |
| `relative_humidity_2m_mean` | Monthly mean relative humidity |
| `wind_speed_10m_max` | Monthly mean of daily maximum wind speeds |
| `_weather_present` | Boolean flag indicating weather data availability |
| `arrival_quantity_tonnes` | Monthly wheat arrival quantity in tonnes |
| `_arrival_present` | Boolean flag indicating arrival data availability |
| `match_type` | Identifies which source datasets are available for a record |

### 5.5 Integration Results

The integration was performed using State, District, and month as matching keys after standardising State and District names.

| Match Type | Records |
|---|---:|
| Mandi + Arrivals | 1,627 |
| Mandi only | 1,369 |
| Arrivals only | 743 |
| Weather only | 60 |
| All three sources | 0 |
| **Total** | **3,799** |

No records matched across all three sources. This is a source-coverage limitation: the available weather dataset covers five Tamil Nadu districts, while the wheat arrivals dataset does not provide matching Tamil Nadu wheat districts. The integration therefore retains unmatched records instead of forcing incorrect geographical matches.


## 6. Data Integration Methodology

The integration process follows these steps:

1. Load the raw datasets using Python and Pandas.
2. Standardise state and district names by converting them to lowercase, trimming whitespace, and normalising spacing.
3. Filter the mandi price dataset to Wheat.
4. Aggregate daily mandi price observations by State, District, and month.
5. Aggregate daily weather observations by District, State, and month.
6. Prepare monthly wheat arrival quantities using State, District, and month.
7. Combine the processed datasets using an outer merge.
8. Add source-presence indicators and a `match_type` field.
9. Export the processed datasets as CSV and Parquet files.

### Integration Keys

- `State`
- `District`
- `month`

The original raw datasets are retained separately from processed datasets.

---

## 7. Data Quality and General Limitations

- Raw datasets originate from different sources and have different levels of geographical and temporal detail.
- District and state names may differ in spelling or formatting.
- Weather observations are limited to five Tamil Nadu districts.
- Crop-arrival records cover January to October 2025.
- Missing mandi minimum and maximum prices require appropriate handling during analysis.
- No three-way geographical matches currently exist between the selected datasets.
- The integrated dataset retains unmatched records, so missing values in source-specific fields are expected.

---

## 8. Storage and File Organisation

The project maintains separate directories for raw and processed data.

| Directory | Purpose |
|---|---|
| `data/raw/` | Original datasets collected from external sources |
| `data/processed/` | Cleaned, aggregated, and integrated datasets |
| `scripts/` | Python extraction, integration, and conversion scripts |
| `documentation/` | Dataset metadata and project documentation |

### AWS Cloud Storage

Raw and processed datasets are also stored in Amazon S3.

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
- CSV files provide convenient access for inspection and analysis.
- Parquet files provide columnar storage suitable for analytical workloads.
- Dataset metadata should be updated whenever new data is extracted or processed.
- AWS credentials and secret access keys must never be committed to the GitHub repository.
'@ | Set-Content -Path documentation\data_dictionary.md -Encoding UTF8

