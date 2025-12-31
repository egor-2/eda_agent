"""
Initial data exploration script for Market Trend and External Factors dataset.
"""
import pandas as pd
import numpy as np

def main():
    # Load data
    df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
    
    print("=== Basic Info ===")
    print(f"Shape: {df.shape}")
    print(f"\nColumn dtypes:\n{df.dtypes}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    print(f"\nLast 5 rows:\n{df.tail()}")
    print(f"\nDate range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"\n=== Missing Values ===\n{df.isnull().sum()}")
    print(f"\n=== Duplicates ===")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"\n=== Basic Statistics ===\n{df.describe()}")
    
    # Column details
    print("\n=== Column Details ===")
    for col in df.columns:
        print(f"\n--- {col} ---")
        print(f"Unique values: {df[col].nunique()}")
        if df[col].dtype in ['int64', 'float64']:
            print(f"Range: [{df[col].min():.2f}, {df[col].max():.2f}]")
            print(f"Mean: {df[col].mean():.4f}, Std: {df[col].std():.4f}")
        else:
            print(f"Sample values: {df[col].head(5).tolist()}")
    
    # Check price consistency
    print("\n=== Price Consistency Check ===")
    issues = (df['Low_Price'] > df['High_Price']).sum()
    print(f"Low > High violations: {issues}")
    issues = (df['Open_Price'] < df['Low_Price']).sum()
    print(f"Open < Low violations: {issues}")
    issues = (df['Close_Price'] < df['Low_Price']).sum()
    print(f"Close < Low violations: {issues}")

if __name__ == "__main__":
    main()
