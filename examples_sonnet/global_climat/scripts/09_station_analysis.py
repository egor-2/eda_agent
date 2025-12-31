import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Measurements per station distribution
ax = axes[0, 0]
measurements_per_station = df.groupby('station_id').size()
ax.hist(measurements_per_station.values, bins=50, edgecolor='black', alpha=0.7)
ax.set_xlabel('Measurements per Station', fontsize=12)
ax.set_ylabel('Number of Stations', fontsize=12)
ax.set_title('Distribution of Measurements per Station', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(measurements_per_station.mean(), color='red', linestyle='--', linewidth=2, 
           label=f'Mean: {measurements_per_station.mean():.0f}')
ax.axvline(measurements_per_station.median(), color='green', linestyle='--', linewidth=2,
           label=f'Median: {measurements_per_station.median():.0f}')
ax.legend()

# 2. Elements per station
ax = axes[0, 1]
elements_per_station = df.groupby('station_id')['element'].nunique()
ax.hist(elements_per_station.values, bins=30, edgecolor='black', alpha=0.7, color='orange')
ax.set_xlabel('Number of Different Elements Measured', fontsize=12)
ax.set_ylabel('Number of Stations', fontsize=12)
ax.set_title('Distribution of Elements per Station', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(elements_per_station.mean(), color='red', linestyle='--', linewidth=2,
           label=f'Mean: {elements_per_station.mean():.1f}')
ax.legend()

# 3. Days of data per station
ax = axes[1, 0]
days_per_station = df.groupby('station_id')['date'].nunique()
ax.hist(days_per_station.values, bins=50, edgecolor='black', alpha=0.7, color='green')
ax.set_xlabel('Days with Data', fontsize=12)
ax.set_ylabel('Number of Stations', fontsize=12)
ax.set_title('Distribution of Days with Data per Station', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(days_per_station.mean(), color='red', linestyle='--', linewidth=2,
           label=f'Mean: {days_per_station.mean():.0f}')
ax.axvline(365, color='blue', linestyle=':', linewidth=2, label='365 days (full year)')
ax.legend()

# 4. Station data completeness
ax = axes[1, 1]
completeness = (days_per_station / 365) * 100
ax.hist(completeness.values, bins=50, edgecolor='black', alpha=0.7, color='purple')
ax.set_xlabel('Data Completeness (%)', fontsize=12)
ax.set_ylabel('Number of Stations', fontsize=12)
ax.set_title('Station Data Completeness (% of days in 1901)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(completeness.mean(), color='red', linestyle='--', linewidth=2,
           label=f'Mean: {completeness.mean():.1f}%')
ax.legend()

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/06_station_analysis.png', dpi=300, bbox_inches='tight')
print("Saved: 06_station_analysis.png")
plt.close()

# Print statistics
print("\n=== STATION STATISTICS ===")
print(f"Total stations: {df['station_id'].nunique():,}")
print(f"\nMeasurements per station:")
print(f"  Min: {measurements_per_station.min()}")
print(f"  Max: {measurements_per_station.max()}")
print(f"  Mean: {measurements_per_station.mean():.1f}")
print(f"  Median: {measurements_per_station.median():.1f}")

print(f"\nDays per station:")
print(f"  Min: {days_per_station.min()}")
print(f"  Max: {days_per_station.max()}")
print(f"  Mean: {days_per_station.mean():.1f}")
print(f"  Stations with full year (365 days): {(days_per_station == 365).sum():,} ({100*(days_per_station == 365).sum()/len(days_per_station):.1f}%)")

print(f"\nElements per station:")
print(f"  Min: {elements_per_station.min()}")
print(f"  Max: {elements_per_station.max()}")
print(f"  Mean: {elements_per_station.mean():.1f}")

# Top stations
print("\n=== TOP 10 STATIONS BY MEASUREMENT COUNT ===")
top_stations = df.groupby('station_id').size().sort_values(ascending=False).head(10)
for station, count in top_stations.items():
    country = station[:2]
    print(f"{station} ({country}): {count:,} measurements")

