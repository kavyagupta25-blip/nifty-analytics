import pandas as pd
import os
import sqlite3

STOCKS_DIR = "data/stocks"

# ── EXTRACT ───────────────────────────────────────────────
print("Reading files...")
all_dfs = []

for filename in os.listdir(STOCKS_DIR):
    if filename.endswith(".csv") and filename not in [
        "NIFTY50_all.csv", "stock_metadata.csv", "INFRATEL.csv"
    ]:
        filepath = os.path.join(STOCKS_DIR, filename)
        df = pd.read_csv(filepath)
        all_dfs.append(df)

combined = pd.concat(all_dfs, ignore_index=True)
print(f"Raw shape: {combined.shape}")

# ── TRANSFORM ─────────────────────────────────────────────

# 1. Fix dates
combined["Date"] = pd.to_datetime(combined["Date"], errors="coerce")
combined = combined.dropna(subset=["Date"])

# 2. Keep only useful columns
# Series, Last, VWAP, Turnover are less useful for analysis
combined = combined[[
    "Date", "Symbol", "Open", "High", 
    "Low", "Close", "Volume", "Trades",
    "Deliverable Volume", "%Deliverble"
]]

# 3. Rename columns — cleaner names
combined.columns = [
    "date", "symbol", "open", "high",
    "low", "close", "volume", "trades",
    "deliverable_volume", "pct_deliverable"
]

# 4. Handle missing values
# Fill Trades with median per company
combined["trades"] = combined.groupby("symbol")["trades"].transform(
    lambda x: x.fillna(x.median())
)

# Fill deliverable columns with 0 — old data didn't track this
combined["deliverable_volume"] = combined["deliverable_volume"].fillna(0)
combined["pct_deliverable"]    = combined["pct_deliverable"].fillna(0)

# 5. Add useful derived columns
combined["year"]        = combined["date"].dt.year
combined["month"]       = combined["date"].dt.month
combined["month_name"]  = combined["date"].dt.strftime("%B")
combined["day_of_week"] = combined["date"].dt.strftime("%A")

# 6. Add daily return column
# Daily return = how much % the stock moved today
# (close - prev_close) / prev_close * 100
combined = combined.sort_values(["symbol", "date"])
combined["daily_return"] = combined.groupby("symbol")["close"].pct_change() * 100

# ── VALIDATE ──────────────────────────────────────────────
print(f"Clean shape: {combined.shape}")
print(f"Companies: {combined['symbol'].nunique()}")
print(f"Date range: {combined['date'].min()} to {combined['date'].max()}")
print(f"Null values:\n{combined.isnull().sum()}")
print(f"\nSample data:")
print(combined.head())

# ── LOAD ──────────────────────────────────────────────────
print("\nSaving to database...")
conn = sqlite3.connect("data/stocks.db")
combined.to_sql("stocks", conn, if_exists="replace", index=False)
print(f"✅ Saved {len(combined)} rows to stocks.db")
conn.close()

# Save CSV for deployment
combined.to_csv("data/stocks_cleaned.csv", index=False)
print("✅ CSV saved!")

# ── LOAD TO POSTGRESQL ────────────────────────────────────
from sqlalchemy import create_engine

# Create connection to PostgreSQL
# Format: postgresql://username:password@host:port/database_name
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Aanyagupta@1",  # paste your actual password here
    host="localhost",
    port=5432,
    database="nifty_analytics"
)

engine = create_engine(connection_url)
print("\nLoading to PostgreSQL...")
combined.to_sql("stocks", engine, if_exists="replace", index=False)
print(f"✅ Saved {len(combined)} rows to PostgreSQL!")