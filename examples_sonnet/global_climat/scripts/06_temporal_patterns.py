import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['day_of_year'] = df['date'].dt.dayofyear

# Create figure for temporal patterns
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Measurements per day
ax = axes[0, 0]
daily_counts = df.groupby('date').size().sort_index()
ax.plot(daily_counts.index, daily_counts.values, linewidth=1, alpha=0.7)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Measurements', fontsize=12)
ax.set_title('Total Measurements per Day in 1901', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 2. Measurements per element over time
ax = axes[0, 1]
for element in ['PRCP', 'TMAX', 'TMIN', 'TOBS', 'SNOW']:
    element_daily = df[df['element'] == element].groupby('date').size().sort_index()
    ax.plot(element_daily.index, element_daily.values, label=element, linewidth=1.5, alpha=0.7)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Measurements', fontsize=12)
ax.set_title('Measurements by Element Over Time', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

# 3. Average temperature by day of year
ax = axes[1, 0]
for element in ['TMAX', 'TMIN']:
    temp_daily = df[df['element'] == element].groupby('day_of_year')['value'].mean() / 10.0  # Convert to °C
    ax.plot(temp_daily.index, temp_daily.values, label=element, linewidth=2, alpha=0.7)
ax.set_xlabel('Day of Year', fontsize=12)
ax.set_ylabel('Average Temperature (°C)', fontsize=12)
ax.set_title('Average Daily Temperature Throughout 1901', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

# 4. Average precipitation by day of year
ax = axes[1, 1]
prcp_daily = df[df['element'] == 'PRCP'].groupby('day_of_year')['value'].mean()
ax.plot(prcp_daily.index, prcp_daily.values, linewidth=2, alpha=0.7, color='blue')
ax.set_xlabel('Day of Year', fontsize=12)
ax.set_ylabel('Average Precipitation (mm)', fontsize=12)
ax.set_title('Average Daily Precipitation Throughout 1901', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/03_temporal_patterns.png', dpi=300, bbox_inches='tight')
print("Saved: 03_temporal_patterns.png")
plt.close()

# Station coverage over time
print("\n=== STATION COVERAGE OVER TIME ===")
stations_per_day = df.groupby('date')['station_id'].nunique()
print(f"Min stations per day: {stations_per_day.min():,}")
print(f"Max stations per day: {stations_per_day.max():,}")
print(f"Mean stations per day: {stations_per_day.mean():.0f}")

