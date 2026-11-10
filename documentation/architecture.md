\# Mandi Price Intelligence – Project Architecture



\## 1. Architecture Overview



The project follows a data engineering pipeline that collects agricultural market prices, crop arrivals, and weather information from multiple external sources. The collected data is stored locally and in AWS S3, processed using Python and Pandas, and transformed into monthly datasets for further analysis.



\## 2. Architecture Diagram



```mermaid

flowchart TD

&#x20;   A\[Hugging Face / AGMARKNET<br/>Mandi Daily Prices]

&#x20;   B\[Open-Meteo<br/>Historical Weather]

&#x20;   C\[CEDA Agri-Market<br/>Wheat Arrivals]



&#x20;   A --> D\[Python Data Extraction]

&#x20;   B --> D

&#x20;   C --> D



&#x20;   D --> E\[Raw Data Storage<br/>data/raw/]

&#x20;   E --> F\[AWS S3 Raw Storage]



&#x20;   E --> G\[Python Data Integration<br/>Pandas]



&#x20;   G --> H\[Data Cleaning<br/>Standardization]

&#x20;   H --> I\[Monthly Aggregation]

&#x20;   I --> J\[Full Outer Join<br/>State + District + Month]

&#x20;   J --> K\[Source Presence Flags<br/>and Match Type]



&#x20;   K --> L\[Processed CSV and Parquet Files]

&#x20;   L --> M\[AWS S3 Processed Storage]



&#x20;   M --> N\[Further Analysis]

&#x20;   N --> O\[Visualization and Dashboard]

&#x20;   N --> P\[Future Predictive Modelling]

```



\## 3. External Data Sources



The project integrates three agricultural and environmental datasets:



1\. \*\*Mandi Daily Prices:\*\* Historical agricultural market prices obtained from a Hugging Face dataset sourced from AGMARKNET.

2\. \*\*Weather Data:\*\* Historical weather observations collected using the Open-Meteo API.

3\. \*\*Crop Arrivals:\*\* Monthly wheat arrival quantities obtained from the CEDA Agri-Market API.



\## 4. Data Extraction Layer



Python scripts are used to retrieve and organize data from the external sources.



The extracted datasets are initially stored in the `data/raw/` directory.



\## 5. Raw Data Storage Layer



Raw datasets are stored locally and uploaded to an AWS S3 bucket.



\*\*AWS S3 bucket:\*\*



`mandi-price-intelligence-2026-584310482678-ap-south-1-an`



Storage organization:



\- `raw/` – Original extracted datasets.

\- `processed/` – Cleaned and aggregated datasets.



AWS S3 provides centralized cloud-based object storage for the project.



\## 6. Data Processing and Integration Layer



Python and Pandas are used for data processing.



The major operations include:



\- Standardizing State and District names.

\- Filtering mandi records for wheat.

\- Aggregating mandi prices by State, District, and Month.

\- Aggregating weather observations by district and month.

\- Aggregating wheat arrivals by State, District, and Month.

\- Combining datasets using a full outer join.

\- Creating source-presence indicators and a `match\_type` column.



The integration uses State, District, and Month as common keys.



\## 7. Processed Data Storage Layer



The processed datasets are stored in both CSV and Parquet formats.



The main outputs are:



\- `monthly\_mandi\_wheat\_prices`

\- `monthly\_weather`

\- `monthly\_wheat\_arrivals`

\- `monthly\_combined\_intelligence`



Parquet is used as a columnar storage format for efficient analytical processing, while CSV provides convenient access and inspection.



\## 8. Cloud Storage Layer



All raw and processed datasets are uploaded to AWS S3.



The cloud storage structure is:



```text

AWS S3 Bucket

│

├── raw/

│   ├── Mandi price data

│   ├── Weather data

│   └── Crop arrivals data

│

└── processed/

&#x20;   ├── Monthly mandi prices

&#x20;   ├── Monthly weather

&#x20;   ├── Monthly wheat arrivals

&#x20;   └── Combined intelligence

```



\## 9. Downstream Usage



The processed datasets can support:



\- Agricultural price trend analysis.

\- Wheat arrival and market activity analysis.

\- Weather and agricultural market analysis where geographic coverage overlaps.

\- Future dashboard development.

\- Future predictive modelling.



\## 10. Data Integration Limitation



The three datasets have different geographic coverage. The weather dataset covers five districts in Tamil Nadu, while the wheat arrivals dataset does not provide matching Tamil Nadu wheat districts in the available data.



Therefore, the current integration does not contain records matching all three sources simultaneously.



A full outer join preserves records from each source instead of forcing incorrect geographic matches.



\## 11. Technology Stack



| Component | Technology |

|---|---|

| Programming | Python |

| Data Processing | Pandas |

| Data Formats | CSV, Parquet |

| Extraction | APIs and dataset downloads |

| Cloud Storage | AWS S3 |

| Cloud CLI | AWS CLI |

| Development Environment | Python Virtual Environment |

| Version Control | Git and GitHub |

