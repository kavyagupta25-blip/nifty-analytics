# Nifty 50 Stock Market Analytics

End-to-end data engineering project analyzing 21 years of Nifty 50 stock market data.

## What this project does
- Processes 235,192 rows of historical stock data from 65 companies
- Cleans and combines 50 individual CSV files into a unified dataset
- Stores data in PostgreSQL for production-grade querying
- Serves data via a REST API with 9 endpoints built with FastAPI
- Interactive Power BI dashboard with cross-filtering
- Deployed on Railway cloud platform

## Tech Stack
- Python, Pandas — data cleaning and ETL pipeline
- PostgreSQL — production database
- FastAPI — REST API with automatic documentation
- Power BI — interactive dashboard
- Railway — cloud deployment
- Git, GitHub — version control

## Key Findings
- TATAMOTORS and SBIN are the most traded stocks over 21 years
- 2008 financial crisis clearly visible as market low point
- Market showed strongest recovery in 2009-2010
- Average Nifty 50 stock price grew from ~₹500 to ~₹2500 over 21 years

## API Endpoints
- GET /stocks — all available companies
- GET /stocks/{symbol} — price history for one stock
- GET /stocks/{symbol}/summary — complete stats for one stock
- GET /stocks/{symbol}/yearly-returns — year by year performance
- GET /stocks/top-performers — best performing stocks
- GET /stocks/compare?s1=TCS&s2=INFY — compare two stocks
- GET /market/best-year — best years for overall market
- GET /market/worst-crash — worst single day crashes

## How to run locally
1. pip install -r requirements.txt
2. Set up PostgreSQL and run scripts/build_db.py
3. uvicorn api.main:app --reload
4. Open http://localhost:8000/docs

## Project Structure
nifty-analytics/
├── data/stocks/       # Raw CSV files (50 companies)
├── scripts/
│   └── build_db.py    # ETL pipeline
├── api/
│   └── main.py        # FastAPI application
├── Dockerfile         # Container configuration
└── README.md
