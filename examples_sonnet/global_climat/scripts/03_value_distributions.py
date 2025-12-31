import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')
df['date'] = pd.to_datetime(df['date'])

# Analyze value distribution by element
print("=== VALUE STATISTICS BY ELEMENT ===\n")
for element in df['element'].value_counts().head(10).index:
    element_data = df[df['element'] == element]['value']
    print(f"\n{element}:")
    print(f"  Count: {len(element_data):,}")
    print(f"  Min: {element_data.min()}")
    print(f"  Max: {element_data.max()}")
    print(f"  Mean: {element_data.mean():.2f}")
    print(f"  Median: {element_data.median():.2f}")
    print(f"  Std: {element_data.std():.2f}")
    
    # Check for zeros
    zero_count = (element_data == 0).sum()
    print(f"  Zero values: {zero_count:,} ({100*zero_count/len(element_data):.1f}%)")
    
    # Most common values
    print(f"  Top 5 values: {element_data.value_counts().head().to_dict()}")

# Specifically for PRCP - check default/placeholder values
print("\n\n=== PRECIPITATION (PRCP) VALUE ANALYSIS ===")
prcp_data = df[df['element'] == 'PRCP']['value']
print(f"\nTotal PRCP measurements: {len(prcp_data):,}")
print(f"Zero precipitation: {(prcp_data == 0).sum():,} ({100*(prcp_data == 0).sum()/len(prcp_data):.1f}%)")

# Top 20 most common values
print("\nTop 20 most common PRCP values:")
top_prcp = prcp_data.value_counts().head(20)
for val, count in top_prcp.items():
    print(f"  {val} mm: {count:,} ({100*count/len(prcp_data):.2f}%)")

# Check if common values are round numbers
common_vals = [0, 5, 10, 15, 20, 25, 50, 100]
count_at_common = sum((prcp_data == v).sum() for v in common_vals)
print(f"\nPRCP values at common round numbers {common_vals}:")
print(f"  {count_at_common:,} ({100*count_at_common/len(prcp_data):.1f}%)")

# Temperature analysis
print("\n\n=== TEMPERATURE VALUE ANALYSIS ===")
for temp_elem in ['TMAX', 'TMIN', 'TOBS']:
    if temp_elem in df['element'].values:
        temp_data = df[df['element'] == temp_elem]['value']
        print(f"\n{temp_elem} (tenths of °C):")
        print(f"  Range: {temp_data.min()} to {temp_data.max()} ({temp_data.min()/10}°C to {temp_data.max()/10}°C)")
        print(f"  Mean: {temp_data.mean():.1f} ({temp_data.mean()/10:.1f}°C)")
        
        # Check for round numbers in tenths
        round_vals = temp_data[temp_data % 10 == 0]
        print(f"  Round values (multiples of 10): {len(round_vals):,} ({100*len(round_vals)/len(temp_data):.1f}%)")

