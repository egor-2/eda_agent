"""
Exploratory Data Analysis for GHCN Daily Climate Data (1901)
This script performs comprehensive EDA on the Global Historical Climatology Network dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11

DATA_PATH = '/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv'
FIG_DIR = '/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_opus/figures'

def load_data():
    """Load and prepare the dataset."""
    df = pd.read_csv(DATA_PATH)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['country'] = df['station_id'].str[:2]
    return df

def basic_stats(df):
    """Print basic statistics."""
    print("=== BASIC STATISTICS ===")
    print(f"Total observations: {len(df):,}")
    print(f"Unique stations: {df['station_id'].nunique():,}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Unique elements: {df['element'].nunique()}")
    print(f"Unique countries: {df['country'].nunique()}")
    
    print("\n=== ELEMENT DISTRIBUTION ===")
    print(df['element'].value_counts())
    
    print("\n=== MISSING DATA ===")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    print(pd.DataFrame({'missing': missing, 'percent': missing_pct}))

def temperature_analysis(df):
    """Analyze temperature data."""
    df_tmax = df[df['element'] == 'TMAX'].copy()
    df_tmin = df[df['element'] == 'TMIN'].copy()
    df_tmax['value_c'] = df_tmax['value'] / 10
    df_tmin['value_c'] = df_tmin['value'] / 10
    
    # Filter unrealistic values
    df_tmax_clean = df_tmax[(df_tmax['value_c'] >= -60) & (df_tmax['value_c'] <= 60)]
    df_tmin_clean = df_tmin[(df_tmin['value_c'] >= -60) & (df_tmin['value_c'] <= 50)]
    
    print("\n=== TEMPERATURE STATISTICS (filtered) ===")
    print(f"TMAX: mean={df_tmax_clean['value_c'].mean():.1f}C, std={df_tmax_clean['value_c'].std():.1f}C")
    print(f"TMIN: mean={df_tmin_clean['value_c'].mean():.1f}C, std={df_tmin_clean['value_c'].std():.1f}C")
    
    return df_tmax_clean, df_tmin_clean

def precipitation_analysis(df):
    """Analyze precipitation data."""
    df_prcp = df[df['element'] == 'PRCP'].copy()
    
    zero_pct = (df_prcp['value'] == 0).sum() / len(df_prcp) * 100
    print(f"\n=== PRECIPITATION ===")
    print(f"Records: {len(df_prcp):,}")
    print(f"Zero precipitation: {zero_pct:.1f}%")
    print(f"Mean (all): {df_prcp['value'].mean():.2f}mm")
    print(f"Mean (non-zero): {df_prcp[df_prcp['value'] > 0]['value'].mean():.2f}mm")
    
    return df_prcp

def main():
    df = load_data()
    basic_stats(df)
    temperature_analysis(df)
    precipitation_analysis(df)

if __name__ == "__main__":
    main()
