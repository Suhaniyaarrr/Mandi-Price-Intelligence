# Problem Statement

## 1. Background

Agricultural commodity prices in India are influenced by several factors, including market demand and supply, crop arrivals, seasonal patterns, and weather conditions. Farmers, traders, and other agricultural stakeholders need reliable information about market prices and related conditions to make informed decisions.

However, mandi prices, crop arrivals, and weather information are available through different sources and in different formats. This makes it difficult to analyse these datasets together and identify meaningful patterns.

A structured Big Data engineering approach is required to collect, process, integrate, and analyse information from these diverse sources.

## 2. Problem Definition

The Mandi Price Intelligence project aims to develop a data engineering pipeline that collects, stores, processes, and integrates agricultural mandi price data with wheat arrival quantities and historical weather information.

The project addresses the challenge of handling large and heterogeneous datasets from multiple sources and transforming them into structured monthly datasets suitable for agricultural market analysis.

The pipeline uses Databricks and Apache Spark (PySpark) to perform data cleaning, standardisation, aggregation, integration, and validation.

## 3. Key Problems Addressed

- Agricultural price, crop arrival, and weather information is distributed across different data sources.
- Raw datasets have different structures, formats, geographical coverage, and levels of detail.
- Large datasets require efficient processing and organised storage.
- Data requires cleaning, standardisation, and aggregation before meaningful analysis.
- Geographical and temporal matching across datasets is challenging.
- Missing or unmatched information must be retained and represented accurately rather than discarded or incorrectly matched.
- A scalable storage and processing approach is required for raw and processed data.

## 4. Proposed Solution

The project develops a multi-source agricultural data pipeline using Python, Databricks, and PySpark.

The proposed solution includes:

1. Collecting mandi prices, wheat arrivals, and historical weather data from external sources.
2. Loading and maintaining raw datasets in Databricks Unity Catalog Volumes.
3. Exploring and validating the datasets for missing values, duplicates, and data coverage.
4. Standardising State, District, and Commodity names using PySpark.
5. Aggregating each dataset at the monthly State-District level.
6. Integrating the aggregated datasets using a full outer join on State, District, and Month.
7. Creating source-presence indicators and a match classification to identify the contribution of each dataset.
8. Storing processed datasets in Parquet format for further analysis.

AWS S3 is configured as the project's cloud object storage.

## 5. Expected Outcomes

- A consolidated collection of agricultural market, wheat arrival, and weather datasets.
- Standardised and documented raw and processed data.
- Monthly district-level datasets for wheat prices, arrivals, and weather.
- An integrated dataset that preserves unmatched records from all available sources.
- Data quality validation and source-presence indicators.
- A foundation for further agricultural market analysis, visualisation, dashboard development, and predictive modelling.

## 6. Project Limitations

- Mandi price data covers January to December 2025.
- Wheat arrivals data is available from January to October 2025.
- Weather data covers only five selected districts in Tamil Nadu.
- The available weather records do not geographically match the mandi price and wheat arrival datasets at the State-District-Month level.
- The unit of the wheat arrival quantity field has not been confirmed.

These limitations are documented to ensure that analytical results are interpreted accurately and that unsupported relationships are not assumed.