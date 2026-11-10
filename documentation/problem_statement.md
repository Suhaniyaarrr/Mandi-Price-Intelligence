# Problem Statement

## 1. Background

Agricultural commodity prices in India are influenced by several factors, including market demand and supply, crop arrivals, seasonal patterns, and weather conditions. Farmers, traders, and other agricultural stakeholders need reliable information about market prices and related conditions to make informed decisions.

However, information about mandi prices, crop arrivals, and weather is available through different sources and in different formats. This makes it difficult to analyse these datasets together and identify useful patterns.

## 2. Problem Definition

The Mandi Price Intelligence project aims to develop a data-driven system that collects, stores, processes, and integrates agricultural mandi price data with crop arrival quantities and historical weather information.

The project addresses the challenge of working with large, heterogeneous datasets from multiple sources and creating a structured dataset suitable for agricultural market analysis.

## 3. Key Problems Addressed

- Agricultural price, crop arrival, and weather information is distributed across different data sources.
- Raw datasets have different structures, formats, geographical coverage, and levels of detail.
- Data requires cleaning, standardisation, and aggregation before meaningful analysis.
- Geographical and temporal matching across datasets is challenging.
- Missing or unmatched information must be retained and represented accurately rather than discarded or incorrectly matched.
- A scalable and organised storage approach is required for raw and processed data.

## 4. Proposed Solution

The project uses Python-based data extraction and processing to collect information from multiple agricultural and weather data sources.

The collected datasets are stored in raw form, processed into structured monthly datasets, and integrated using State, District, and month as matching keys.

The processed outputs are maintained in CSV and Parquet formats, with Amazon S3 used for cloud-based object storage.

## 5. Expected Outcomes

- A consolidated collection of agricultural market, crop arrival, and weather datasets.
- Standardised and documented raw and processed data.
- Monthly district-level datasets for wheat prices, arrivals, and weather.
- An integrated dataset that retains unmatched source records.
- A foundation for further analysis, visualisation, and predictive modelling by the project team.
