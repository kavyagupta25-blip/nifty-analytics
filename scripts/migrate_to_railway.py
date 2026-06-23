import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Local database — handles special characters in password
local_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Aanyagupta@1", 
    host="localhost",
    port=5432,
    database="nifty_analytics"
)
local_engine = create_engine(local_url)

# Railway database
railway_engine = create_engine(
    "postgresql://postgres:nYdlcXkaJADDUPjPDpnqdaQVVgbSHQzZ@reseau.proxy.rlwy.net:50401/railway"
)

print("Reading from local PostgreSQL...")
df = pd.read_sql("SELECT * FROM stocks", local_engine)
print(f"Read {len(df)} rows")

print("Writing to Railway PostgreSQL...")
df.to_sql("stocks", railway_engine, if_exists="replace", index=False)
print(f"Migrated {len(df)} rows to Railway!")