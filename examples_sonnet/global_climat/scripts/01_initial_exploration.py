import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

print("\n=== DATASET SHAPE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\n=== COLUMN NAMES AND TYPES ===")
print(df.dtypes)

print("\n=== FIRST FEW ROWS ===")
print(df.head(20))

print("\n=== BASIC INFO ===")
print(df.info())

print("\n=== MISSING VALUES ===")
missing = df.isnull().sum()
missing_pct = 100 * missing / len(df)
missing_df = pd.DataFrame({
    'Missing_Count': missing,
    'Missing_Percentage': missing_pct
})
print(missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False))

print("\n=== UNIQUE VALUES PER COLUMN ===")
for col in df.columns:
    print(f"{col}: {df[col].nunique():,} unique values")

print("\n=== SAMPLE VALUES FROM EACH COLUMN ===")
for col in df.columns:
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))

print("\n=== DUPLICATE ROWS ===")
duplicates = df.duplicated().sum()
print(f"Total duplicate rows: {duplicates:,} ({100*duplicates/len(df):.2f}%)")

# Check for exact duplicates in key columns
dup_subset = df.duplicated(subset=['station_id', 'date', 'element']).sum()
print(f"Duplicates in (station_id, date, element): {dup_subset:,}")

