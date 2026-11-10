Mandi Price Intelligence



A Big Data engineering project that integrates agricultural mandi prices, wheat arrivals, and historical weather data to create a unified dataset for agricultural market analysis.



1\. Project Overview



Agricultural commodity prices are influenced by several factors, including market demand, crop arrivals, and weather conditions.



This project collects data from multiple sources, processes and integrates the datasets using Python, and stores the resulting datasets in AWS S3 in CSV and Parquet formats.



The objective is to build a reliable data pipeline that can support agricultural market analysis and future predictive modelling.



2\. Data Sources



The project uses three primary data sources:



Dataset



Source



Coverage



Historical Mandi Prices



Hugging Face dataset sourced from AGMARKNET



January–December 2025



Historical Weather



Open-Meteo API



Five districts in Tamil Nadu, 2025



Wheat Arrivals



CEDA Agri-Market API



January–October 2025



Dataset details



Mandi prices: Approximately 5.83 million records covering 30 states, 572 districts, 5,423 markets, and 338 commodities.



Weather: 1,825 daily records covering five Tamil Nadu districts.



Wheat arrivals: 2,370 monthly records covering 14 states and 288 districts.



3\. Technology Stack



Component



Technology



Programming Language



Python



Data Processing



Pandas



Data Formats



CSV, Parquet, JSON



Data Extraction



APIs and dataset downloads



Cloud Storage



AWS S3



Cloud CLI



AWS CLI



Version Control



Git and GitHub



4\. Data Processing Pipeline



The project follows these major stages:



Data Extraction: Collect mandi prices, weather observations, and wheat arrival quantities.



Raw Storage: Store original datasets locally and in AWS S3.



Data Cleaning: Standardize State and District names and prepare datasets for integration.



Aggregation: Aggregate the datasets at the monthly State-District level.



Data Integration: Combine the datasets using a full outer join on State, District, and Month.



Processed Storage: Export the resulting datasets in CSV and Parquet formats.



Cloud Storage: Upload processed datasets to AWS S3.



5\. Processed Datasets



The project generates four primary processed datasets:



Dataset



Description



Records



monthly\_mandi\_wheat\_prices



Monthly wheat price statistics



2,996



monthly\_weather



Monthly district-level weather statistics



60



monthly\_wheat\_arrivals



Monthly wheat arrival quantities



2,370



monthly\_combined\_intelligence



Integrated dataset containing all available source records



3,799



Each processed dataset is available in CSV and Parquet formats.



The combined dataset includes source-presence indicators:



\_mandi\_present



\_weather\_present



\_arrival\_present



It also contains a match\_type field describing which sources contributed to each record.



6\. Data Integration Results



The combined dataset contains:



Match Type



Records



Mandi + Arrivals



1,627



Mandi Only



1,369



Arrivals Only



743



Weather Only



60



All Three Sources



0



Total



3,799



Integration limitation



The three datasets have different geographic coverage. The available weather data covers five Tamil Nadu districts, while the wheat arrivals dataset does not contain matching Tamil Nadu wheat districts.



Consequently, there are currently no records matching all three sources simultaneously.



A full outer join is used to preserve all available records without creating incorrect geographic matches.



7\. AWS S3 Storage



Raw and processed datasets are stored in Amazon S3.



Bucket name:



mandi-price-intelligence-2026-584310482678-ap-south-1-an



AWS Region: Asia Pacific (Mumbai) – ap-south-1



Storage structure:



mandi-price-intelligence/

│

├── raw/

│   ├── Mandi price data

│   ├── Weather data

│   └── Wheat arrivals data

│

└── processed/

&#x20;   ├── monthly\_mandi\_wheat\_prices.csv

&#x20;   ├── monthly\_mandi\_wheat\_prices.parquet

&#x20;   ├── monthly\_weather.csv

&#x20;   ├── monthly\_weather.parquet

&#x20;   ├── monthly\_wheat\_arrivals.csv

&#x20;   ├── monthly\_wheat\_arrivals.parquet

&#x20;   ├── monthly\_combined\_intelligence.csv

&#x20;   └── monthly\_combined\_intelligence.parquet



AWS credentials are configured locally and are not included in this repository.



8\. Project Documentation



Detailed project documentation is available in the documentation/ directory:



dataset\_sources.md – Dataset sources, coverage, and references.



data\_dictionary.md – Dataset columns, definitions, and data quality details.



problem\_statement.md – Problem definition and project objectives.



project\_scope.md – Project scope, deliverables, and limitations.



architecture.md – Project architecture and data pipeline diagram.



9\. Repository Structure



Mandi-Price-Intelligence/

│

├── data/

│   ├── raw/

│   └── processed/

│

├── documentation/

│   ├── architecture.md

│   ├── dataset\_sources.md

│   ├── data\_dictionary.md

│   ├── problem\_statement.md

│   └── project\_scope.md

│

├── scripts/

│   ├── data\_integration.py

│   └── convert\_to\_parquet.py

│

├── .gitignore

├── README.md

└── requirements.txt



10\. Running the Processing Scripts



Create and activate a Python virtual environment, then install the project dependencies.



python -m venv .venv

.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt



Run the data integration script:



python scripts/data\_integration.py



Convert the processed CSV datasets to Parquet:



python scripts/convert\_to\_parquet.py



These commands assume the required raw datasets are available in the expected local directories.



11\. Future Enhancements



Expand weather coverage to additional agricultural districts.



Improve geographic matching across all data sources.



Develop interactive agricultural market dashboards.



Implement wheat price trend analysis.



Explore machine learning models for price forecasting.



12\. Project Goal



The ultimate goal of Mandi Price Intelligence is to create a structured and scalable agricultural data pipeline that brings together market prices, crop arrivals, and weather information to support data-driven agricultural insights.

