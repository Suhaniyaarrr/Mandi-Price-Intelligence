@'
# Dataset Sources and Collection Methodology

## Dataset 1: Historical India Mandi Daily Prices

- Source: Hugging Face
- Dataset: DHIVAKARNAIDUSUNKARI/mandi-india-daily-prices-2001-2026
- URL: https://huggingface.co/datasets/DHIVAKARNAIDUSUNKARI/mandi-india-daily-prices-2001-2026
- Original Data Source: AGMARKNET
- File Used: `data/raw/mandi_daily_2025.parquet`
- Records: 5,827,604
- Columns: 11
- Date Coverage: 01-01-2025 to 31-12-2025
- States: 30
- Districts: 572
- Markets: 5,423
- Commodities: 338
- Missing Values:
  - Min_Price: 4,418
  - Max_Price: 4,718
- Duplicate Records: 0
- Format: Parquet
- Purpose: Historical mandi price analysis, commodity price trends, and price fluctuation analysis.

### Main Fields

State, District, Market, Commodity, Variety, Grade, Arrival_Date, Min_Price, Max_Price, Modal_Price, Commodity_Code.

## Dataset 2: Historical Weather Data

- Source: Open-Meteo Historical Weather API
- Documentation: https://open-meteo.com/en/docs/historical-weather-api
- API Endpoint: https://archive-api.open-meteo.com/v1/archive
- State: Tamil Nadu
- Districts: Salem, Coimbatore, Tiruvannamalai, Madurai, Vellore
- File Used: `data/raw/weather_tamil_nadu_2025.csv`
- Records: 1,825
- Columns: 11
- Date Coverage: 01-01-2025 to 31-12-2025
- Missing Values: 0
- Format: CSV
- Extraction Method: Python Requests library
- API Key Required: No
- Purpose: Analyze weather conditions such as temperature, precipitation, humidity, and wind speed.

### Main Fields

- `time`: Observation date
- `temperature_2m_mean`: Mean temperature
- `temperature_2m_max`: Maximum temperature
- `temperature_2m_min`: Minimum temperature
- `precipitation_sum`: Total precipitation
- `relative_humidity_2m_mean`: Mean relative humidity
- `wind_speed_10m_max`: Maximum wind speed
- `District`: District name
- `State`: State name
- `Latitude`: Location latitude
- `Longitude`: Location longitude

## Dataset 3: Monthly Crop Arrival Quantities

- Source: CEDA Agri-Market, Ashoka University
- Portal: https://agmarknet.ceda.ashoka.edu.in/
- API Endpoint: https://agmarknet.ceda.ashoka.edu.in/api/quantities
- Original Data Source: AGMARKNET, Ministry of Agriculture and Farmers Welfare
- Extraction Method: Python Requests library using a POST API request
- Commodity: Wheat
- Period Requested: January to December 2025
- Actual Data Coverage: January to October 2025
- Geographical Coverage: 14 states and 288 districts
- Total Records: 2,370
- Storage Formats: JSON and CSV
- Files Used:
  - `data/raw/crop_arrivals_wheat_2025.json`
  - `data/raw/crop_arrivals.csv`
- Quantity Unit: Tonnes

### Main Fields

- `t`: Month of record (YYYY-MM)
- `cmdty`: Commodity name
- `district_id`: District identifier
- `district`: District name
- `state_id`: State identifier
- `state`: State name
- `qty`: Crop arrival quantity in tonnes

### Limitations

- Data is aggregated monthly at district level, rather than daily or mandi level.
- Available records cover January to October 2025 only.
- The dataset is AGMARKNET-derived, making it complementary to the mandi price dataset rather than a fully independent source.

## Data Integration Notes

- All three datasets cover the year 2025, although crop arrival data is available only through October.
- Data integration uses standardized state and district names and monthly aggregation.
- Mandi prices and wheat arrivals are integrated using State, District, and Month.
- Weather data is aggregated to monthly district-level observations.
- Weather coverage does not overlap with the wheat price and arrival records at the State-District level in the current datasets.
- Unmatched records are retained in the combined dataset instead of being discarded.
- The lack of common geographical coverage is documented as a limitation and is not treated as a successful three-source match.

## Cloud Storage

Raw and processed datasets are stored in an AWS S3 bucket in the Asia Pacific (Mumbai) region.

- Bucket: `mandi-price-intelligence-2026-584310482678-ap-south-1-an`
- Raw data prefix: `raw/`
- Processed data prefix: `processed/`
- Region: `ap-south-1`
'@ | Set-Content -Path documentation\dataset_sources.md -Encoding UTF8