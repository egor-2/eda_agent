import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')

# 1. Crimes by area
fig, ax = plt.subplots(figsize=(12, 8))
area_counts = df['AREA NAME'].value_counts()
y_pos = np.arange(len(area_counts))
ax.barh(y_pos, area_counts.values, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(area_counts.index, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Distribution by LAPD Area', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(area_counts.values):
    ax.text(v, i, f' {v:,}', va='center', fontsize=8)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/16_crimes_by_area.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Top 15 premises
fig, ax = plt.subplots(figsize=(12, 8))
premise_counts = df['Premis Desc'].value_counts().head(15)
y_pos = np.arange(len(premise_counts))
ax.barh(y_pos, premise_counts.values, color='coral', edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(premise_counts.index, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Number of Crimes', fontsize=12)
ax.set_title('Top 15 Crime Premises', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(premise_counts.values):
    ax.text(v, i, f' {v:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/17_top_premises.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Top 12 weapons
weapon_counts = df[df['Weapon Desc'] != 'Unknown']['Weapon Desc'].value_counts().head(12)
fig, ax = plt.subplots(figsize=(12, 7))
y_pos = np.arange(len(weapon_counts))
ax.barh(y_pos, weapon_counts.values, color='darkred', edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(weapon_counts.index, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Number of Crimes', fontsize=12)
ax.set_title('Top 12 Weapons Used (Excluding "Unknown")', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(weapon_counts.values):
    ax.text(v, i, f' {v:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/18_top_weapons.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Geographic scatter plot (valid coordinates only)
df_geo = df[(df['LAT'] != 0) & (df['LON'] != 0)]
zero_coords = (df['LAT'] == 0).sum()

fig, ax = plt.subplots(figsize=(12, 10))
scatter = ax.scatter(df_geo['LON'], df_geo['LAT'], alpha=0.1, s=1, c='darkblue')
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.set_title(f'Geographic Distribution of Crimes\n({len(df_geo):,} crimes plotted, {zero_coords:,} with missing coordinates)', 
             fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/19_geographic_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Crime density heatmap by area (2D histogram)
fig, ax = plt.subplots(figsize=(12, 10))
h = ax.hist2d(df_geo['LON'], df_geo['LAT'], bins=100, cmap='hot', cmin=1)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.set_title('Crime Density Heatmap (Los Angeles)', fontsize=14, fontweight='bold')
plt.colorbar(h[3], ax=ax, label='Number of Crimes')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/20_crime_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("Location analysis plots completed!")
print(f"\nRecords with zero/missing coordinates: {zero_coords:,} ({zero_coords/len(df)*100:.2f}%)")
