import pandas as pd
import os

# Path to your stocks folder
STOCKS_DIR = "data/stocks"

# Get list of all CSV files
files = os.listdir(STOCKS_DIR)
print(f"Total companies: {len(files)}")
print("First 5 files:", files[:5])

# Read one file to understand structure
sample = pd.read_csv(f"{STOCKS_DIR}/{files[0]}")
print(f"\nFile: {files[0]}")
print("Shape:", sample.shape)
print("Columns:", sample.columns.tolist())
print("Dtypes:\n", sample.dtypes)
print("\nFirst 5 rows:")
print(sample.head())
print("\nMissing values:")
print(sample.isnull().sum())