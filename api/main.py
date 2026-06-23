from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import pandas as pd

# ── App setup ──────────────────────────────────────────────
app = FastAPI(
    title="Nifty 50 Analytics API",
    description="REST API for Nifty 50 stock market data",
    version="1.0.0"
)

# ── Database connection ────────────────────────────────────
connection_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Aanyagupta@1", 
    host="localhost",
    port=5432,
    database="nifty_analytics"
)
engine = create_engine(connection_url)

# ── Routes ─────────────────────────────────────────────────

# Route 1 — Health check
@app.get("/")
def root():
    return {
        "message": "Nifty 50 Analytics API is running!",
        "version": "1.0.0",
        "endpoints": [
            "/stocks",
            "/stocks/{symbol}",
            "/stocks/top-performers",
            "/stocks/{symbol}/yearly-returns"
        ]
    }

# Route 2 — Get all available stock symbols
@app.get("/stocks")
def get_all_stocks():
    query = """
        SELECT DISTINCT symbol, 
               MIN(date) as first_date,
               MAX(date) as last_date,
               COUNT(*) as trading_days
        FROM stocks
        GROUP BY symbol
        ORDER BY symbol
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# Route 3 — Get data for a specific stock
@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    query = f"""
        SELECT date, open, high, low, close, volume, daily_return
        FROM stocks
        WHERE symbol = '{symbol.upper()}'
        ORDER BY date DESC
        LIMIT 100
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return {"error": f"Stock {symbol} not found"}
    return df.to_dict(orient="records")

# Route 4 — Top performing stocks
@app.get("/stocks/top-performers")
def get_top_performers():
    query = """
        SELECT 
            symbol,
            ROUND(AVG(daily_return)::numeric, 4) as avg_daily_return,
            ROUND(STDDEV(daily_return)::numeric, 4) as volatility,
            COUNT(*) as trading_days
        FROM stocks
        WHERE daily_return IS NOT NULL
        GROUP BY symbol
        ORDER BY avg_daily_return DESC
        LIMIT 10
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# Route 5 — Yearly returns for a specific stock
@app.get("/stocks/{symbol}/yearly-returns")
def get_yearly_returns(symbol: str):
    query = f"""
        SELECT 
            year,
            ROUND(AVG(daily_return)::numeric, 4) as avg_return,
            ROUND(AVG(close)::numeric, 2) as avg_close,
            SUM(volume) as total_volume
        FROM stocks
        WHERE symbol = '{symbol.upper()}'
        AND daily_return IS NOT NULL
        GROUP BY year
        ORDER BY year
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return {"error": f"Stock {symbol} not found"}
    return df.to_dict(orient="records")
    # Route 6 — Compare two stocks
@app.get("/stocks/compare")
def compare_stocks(s1: str, s2: str):
    query = f"""
        SELECT 
            symbol,
            year,
            ROUND(AVG(daily_return)::numeric, 4) as avg_return,
            ROUND(AVG(close)::numeric, 2) as avg_close,
            SUM(volume) as total_volume
        FROM stocks
        WHERE symbol IN ('{s1.upper()}', '{s2.upper()}')
        AND daily_return IS NOT NULL
        GROUP BY symbol, year
        ORDER BY symbol, year
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return {"error": "One or both stocks not found"}
    return df.to_dict(orient="records")

# Route 7 — Quick summary for one stock
@app.get("/stocks/{symbol}/summary")
def get_stock_summary(symbol: str):
    query = f"""
        SELECT 
            symbol,
            MIN(date) as first_traded,
            MAX(date) as last_traded,
            COUNT(*) as total_trading_days,
            ROUND(MIN(close)::numeric, 2) as all_time_low,
            ROUND(MAX(close)::numeric, 2) as all_time_high,
            ROUND(AVG(close)::numeric, 2) as avg_close,
            ROUND(AVG(daily_return)::numeric, 4) as avg_daily_return,
            ROUND(STDDEV(daily_return)::numeric, 4) as volatility,
            SUM(volume) as total_volume_traded
        FROM stocks
        WHERE symbol = '{symbol.upper()}'
        AND daily_return IS NOT NULL
        GROUP BY symbol
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        return {"error": f"Stock {symbol} not found"}
    return df.to_dict(orient="records")[0]

# Route 8 — Best year for overall market
@app.get("/market/best-year")
def get_best_year():
    query = """
        SELECT 
            year,
            ROUND(AVG(daily_return)::numeric, 4) as avg_market_return,
            COUNT(DISTINCT symbol) as stocks_tracked,
            SUM(volume) as total_volume
        FROM stocks
        WHERE daily_return IS NOT NULL
        GROUP BY year
        ORDER BY avg_market_return DESC
        LIMIT 5
    """
    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")

# Route 9 — Worst single day crashes
@app.get("/market/worst-crash")
def get_worst_crashes():
    query = """
        SELECT 
            date,
            symbol,
            ROUND(daily_return::numeric, 4) as daily_return,
            ROUND(close::numeric, 2) as close_price,
            volume
        FROM stocks
        WHERE daily_return IS NOT NULL
        ORDER BY daily_return ASC
        LIMIT 10
    """
    df = pd.read_sql(query, engine)
    df["date"] = df["date"].astype(str)
    return df.to_dict(orient="records")