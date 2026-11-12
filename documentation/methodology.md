# Project Methodology - Mandi Price Intelligence

## 1. Overview

The Mandi Price Intelligence project uses multiple agricultural datasets to study wheat price trends, crop arrivals, and weather conditions.

The project uses Databricks and PySpark for large-scale data processing, cleaning, aggregation, integration, and analysis.

The methodology is divided into the following stages:

1. Data collection
2. Raw data storage
3. Data exploration and validation
4. Data cleaning and standardization
5. Monthly aggregation
6. Data integration
7. Data quality validation
8. Data analysis and insights
9. Processed data storage

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data extraction and processing |
| PySpark | Distributed data processing |
| Databricks | Cloud-based development and execution |
| AWS S3 | Cloud object storage |
| Unity Catalog Volumes | Raw and processed data storage |
| Parquet | Efficient analytical data storage |
| GitHub | Version control and collaboration |

## 3. Data Collection

Three datasets were selected from external sources.

### 3.1 Mandi Price Data

Historical daily mandi prices were obtained from the Hugging Face dataset, which originates from AGMARKNET.

The 2025 Parquet dataset contains approximately 5.83 million records covering 30 states, 572 districts, and 338 commodities.

### 3.2 Crop Arrival Data

Monthly wheat arrival quantities were collected from the CEDA Agri-Market API.

The returned dataset contains 2,370 records covering January to October 2025, across 14 states and 288 districts.

### 3.3 Weather Data

Historical weather observations were collected using the Open-Meteo Historical Weather API.

Daily observations were obtained for five districts of Tamil Nadu for the full year 2025.

## 4. Raw Data Storage

The collected datasets were uploaded to a Databricks Unity Catalog Volume.

**Volume location:**

`/Volumes/workspace/default/mandi_project_data/`

The raw datasets were stored in their original formats:

- `mandi_daily_2025.parquet`
- `crop_arrivals_wheat_2025.json`
- `weather_tamil_nadu_2025.csv`

Original datasets were retained separately from processed outputs.

## 5. Data Exploration and Validation

The first Databricks notebook, `01_Data_Ingestion_and_Exploration`, performs the initial data processing workflow.

The following checks were performed:

- Loaded the raw datasets using PySpark.
- Inspected dataset schemas and column names.
- Counted records and columns.
- Examined missing values.
- Checked for duplicate records.
- Identified date coverage and geographical coverage.
- Examined commodity and district information.

The initial data quality checks identified missing minimum and maximum prices in the mandi dataset. The weather and crop arrival datasets contained no missing values in the validated raw records.

## 6. Data Cleaning and Standardization

The datasets originated from different sources and used different naming conventions.

PySpark transformations were applied to standardize the data.

The following operations were performed:

- Removed leading and trailing whitespace from text fields.
- Standardized state, district, and commodity names using consistent capitalization.
- Renamed crop arrival columns to match the common naming convention.
- Converted date information into a common monthly format.
- Corrected identified state spelling variations in the mandi data.

The common integration fields were:

- `State`
- `District`
- `Month`

## 7. Monthly Aggregation

The datasets were aggregated to monthly State-District level observations.

### 7.1 Mandi Price Aggregation

The raw mandi dataset was filtered to include Wheat records only.

Daily price records were grouped by State, District, and Month.

The following metrics were calculated:

- Average minimum price
- Average maximum price
- Average modal price
- Number of price records

**Output:** `monthly_mandi_prices`

**Records:** 2,995

### 7.2 Crop Arrival Aggregation

Wheat arrival records were grouped by State, District, and Month.

The arrival quantities were summed for each group.

**Output:** `monthly_wheat_arrivals`

**Records:** 2,370

The quantity unit was not confirmed in the available source metadata.

### 7.3 Weather Aggregation

Daily weather observations were grouped by State, District, and Month.

The following metrics were calculated:

- Average temperature
- Average maximum temperature
- Average minimum temperature
- Total precipitation
- Average relative humidity
- Average wind speed

**Output:** `monthly_weather`

**Records:** 60

## 8. Data Integration

The three monthly datasets were integrated using PySpark joins.

The integration keys were:

- `State`
- `District`
- `Month`

A full outer join was used to retain records from all datasets, including records without matching geographical or temporal information.

The combined dataset contains:

- Monthly mandi wheat prices
- Monthly wheat arrival quantities
- Monthly weather observations
- Source-presence indicators
- Match classification

Three presence indicators were included:

- `Mandi_Present`
- `Arrivals_Present`
- `Weather_Present`

A `Match_Type` field was also created to identify the source datasets available for each record.

### 8.1 Integration Results

| Match Type | Records |
|---|---:|
| Mandi + Arrivals | 1,627 |
| Mandi only | 1,368 |
| Arrivals only | 743 |
| Weather only | 60 |
| **Total** | **3,798** |

No three-way geographical matches were found.

The weather dataset has no matching State-District keys with the selected mandi price and crop arrival datasets. Therefore, weather records were retained separately in the combined output rather than being treated as matched observations.

**Output:** `monthly_combined_intelligence`

**Records:** 3,798

## 9. Data Quality Validation

After processing and integration, additional validation checks were performed.

The following conditions were verified:

- No duplicate State-District-Month keys in the processed datasets.
- No duplicate integration keys in the combined dataset.
- Expected record counts were obtained.
- Dataset coverage was checked.
- Missing values in important fields were examined.
- Source-presence indicators and match classifications were validated.

The combined dataset contains 3,798 records and 18 columns.

## 10. Processed Data Storage

The processed datasets were saved in Parquet format in the Databricks Unity Catalog Volume.

**Output location:**

`/Volumes/workspace/default/mandi_project_data/processed/`

The four processed outputs are:

| Dataset | Records |
|---|---:|
| `monthly_mandi_prices` | 2,995 |
| `monthly_wheat_arrivals` | 2,370 |
| `monthly_weather` | 60 |
| `monthly_combined_intelligence` | 3,798 |

Parquet was selected for efficient storage and analytical processing.

## 11. Data Analysis

The second Databricks notebook, `02_Data_Analysis_and_Insights`, uses the processed datasets to perform exploratory analysis.

The analysis includes:

- Monthly wheat price trends.
- Monthly wheat arrival trends.
- Comparison of wheat prices and arrivals.
- State-level average wheat prices.
- District-level price comparisons.
- District-level price volatility.
- Comparison of price stability across selected districts.

The analysis also examines data coverage and limitations before interpreting results.

Correlation analysis is used to identify possible statistical relationships, not to establish causation.

## 12. Limitations

The project has the following limitations:

1. Mandi prices cover 2025 only in the selected dataset.
2. Crop arrival data is available only from January to October 2025.
3. The crop arrival quantity unit is not confirmed.
4. Weather data covers only five districts of Tamil Nadu.
5. The selected weather dataset has no geographical matches with the mandi and arrival datasets.
6. Different datasets have different geographical coverage and levels of detail.
7. Monthly averages are based on available observations and may have different district coverage.

These limitations are considered while interpreting the analytical results.

## 13. Reproducibility and Collaboration

The project uses Databricks notebooks to maintain an organized and reproducible processing workflow.

The notebooks are intended to document:

- Data loading and exploration.
- Cleaning and standardization.
- Aggregation and integration.
- Data validation.
- Analysis and visualization.

GitHub is used for version control, documentation, and collaboration among project members.

AWS credentials and other sensitive information must not be committed to the repository.

## 14. Conclusion

The methodology establishes a structured pipeline for collecting, validating, processing, and integrating agricultural datasets.

By combining mandi prices, crop arrivals, and weather observations where geographical matching is possible, the project creates a monthly agricultural intelligence dataset.

The resulting datasets support further analysis of wheat price trends, crop arrival patterns, geographical price differences, and price volatility.