import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')
df['country_code'] = df['station_id'].str[:2]

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Top countries by measurement count
ax = axes[0, 0]
top_countries = df['country_code'].value_counts().head(15)
ax.barh(range(len(top_countries)), top_countries.values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_countries)))
ax.set_yticklabels(top_countries.index)
ax.set_xlabel('Number of Measurements', fontsize=12)
ax.set_ylabel('Country Code', fontsize=12)
ax.set_title('Top 15 Countries by Measurement Count', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

# 2. Top countries by station count
ax = axes[0, 1]
top_countries_stations = df.groupby('country_code')['station_id'].nunique().sort_values(ascending=False).head(15)
ax.barh(range(len(top_countries_stations)), top_countries_stations.values, edgecolor='black', alpha=0.7, color='orange')
ax.set_yticks(range(len(top_countries_stations)))
ax.set_yticklabels(top_countries_stations.index)
ax.set_xlabel('Number of Stations', fontsize=12)
ax.set_ylabel('Country Code', fontsize=12)
ax.set_title('Top 15 Countries by Station Count', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

# 3. Element distribution by top countries
ax = axes[1, 0]
top_5_countries = df['country_code'].value_counts().head(5).index
element_by_country = df[df['country_code'].isin(top_5_countries)].groupby(['country_code', 'element']).size().unstack(fill_value=0)
element_by_country = element_by_country[['PRCP', 'TMAX', 'TMIN', 'TOBS', 'SNOW', 'SNWD']]
element_by_country.plot(kind='bar', ax=ax, edgecolor='black', alpha=0.7)
ax.set_xlabel('Country Code', fontsize=12)
ax.set_ylabel('Number of Measurements', fontsize=12)
ax.set_title('Element Distribution for Top 5 Countries', fontsize=14, fontweight='bold')
ax.legend(title='Element', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True, alpha=0.3, axis='y')
ax.tick_params(axis='x', rotation=45)

# 4. Average measurements per station by country
ax = axes[1, 1]
measurements_per_station = df.groupby('country_code').size() / df.groupby('country_code')['station_id'].nunique()
top_mps = measurements_per_station.sort_values(ascending=False).head(15)
ax.barh(range(len(top_mps)), top_mps.values, edgecolor='black', alpha=0.7, color='green')
ax.set_yticks(range(len(top_mps)))
ax.set_yticklabels(top_mps.index)
ax.set_xlabel('Avg Measurements per Station', fontsize=12)
ax.set_ylabel('Country Code', fontsize=12)
ax.set_title('Top 15 Countries by Avg Measurements per Station', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/04_geographic_patterns.png', dpi=300, bbox_inches='tight')
print("Saved: 04_geographic_patterns.png")
plt.close()

# Print statistics
print("\n=== GEOGRAPHIC COVERAGE ===")
print(f"Total unique countries: {df['country_code'].nunique()}")
print(f"\nCountries with > 100,000 measurements:")
big_countries = df['country_code'].value_counts()
print(big_countries[big_countries > 100000])

