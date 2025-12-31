import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

print("=== DATA FORMAT ANALYSIS ===")
print("\nThis is a LONG-format dataset where each row represents a single measurement.")
print("Key identifier: (station_id, date, element)")
print("\nThe 'element' column indicates what was measured:")
print(df['element'].value_counts())

print("\n=== ELEMENT DESCRIPTIONS ===")
print("\nMost common elements:")
print("- PRCP: Precipitation (mm)")
print("- TMIN: Minimum temperature (tenths of °C)")
print("- TMAX: Maximum temperature (tenths of °C)")
print("- TOBS: Temperature at observation time (tenths of °C)")
print("- SNOW: Snowfall (mm)")
print("- SNWD: Snow depth (mm)")

print("\n=== UNIT ANALYSIS ===")
unit_by_element = df.groupby('element')['unit'].value_counts()
print(unit_by_element)

print("\n=== DATE RANGE ===")
print(f"Start date: {df['date'].min()}")
print(f"End date: {df['date'].max()}")
print(f"Time span: {(df['date'].max() - df['date'].min()).days} days")

print("\n=== STATION ANALYSIS ===")
print(f"Total unique stations: {df['station_id'].nunique():,}")
print(f"\nStation ID format examples:")
print(df['station_id'].head(20).unique())

# Station country codes (first 2-3 characters)
df['country_code'] = df['station_id'].str[:2]
print("\n=== TOP COUNTRIES BY STATION COUNT ===")
print(df.groupby('country_code')['station_id'].nunique().sort_values(ascending=False).head(20))

print("\n=== TOP COUNTRIES BY MEASUREMENT COUNT ===")
print(df['country_code'].value_counts().head(20))

print("\n=== FLAG MEANINGS ===")
print("\nmflag (Measurement flag):")
print(df['mflag'].value_counts())
print("\nqflag (Quality flag):")
print(df['qflag'].value_counts())
print("\nsflag (Source flag):")
print(df['sflag'].value_counts())

