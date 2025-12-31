"""
Los Angeles Crime Data EDA Analysis Script
Dataset: Crime_Data_from_2020_to_Present.parquet
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load data
df = pd.read_parquet('../Crime_Data_from_2020_to_Present.parquet')
figures_path = '../figures/'

# Helper to extract hour from TIME OCC
df['hour'] = df['TIME OCC'].apply(lambda x: x.hour)
df['minute'] = df['TIME OCC'].apply(lambda x: x.minute)
df['delay_days'] = (df['Date Rptd'] - df['DATE OCC']).dt.days

# 1. Crime counts by area
fig, ax = plt.subplots(figsize=(12, 8))
area_counts = df['AREA NAME'].value_counts()
ax.barh(area_counts.index[::-1], area_counts.values[::-1], color='steelblue')
ax.set_xlabel('Number of Crimes')
ax.set_ylabel('Area')
ax.set_title('Total Crime Count by Area (2020-Present)')
for i, v in enumerate(area_counts.values[::-1]):
    ax.text(v + 500, i, f'{v:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(figures_path + '01_crimes_by_area.png', dpi=150)
plt.close()

# 2. Top crime types
fig, ax = plt.subplots(figsize=(14, 10))
crime_counts = df['Crm Cd Desc'].value_counts().head(20)
ax.barh(crime_counts.index[::-1], crime_counts.values[::-1], color='coral')
ax.set_xlabel('Number of Crimes')
ax.set_ylabel('Crime Type')
ax.set_title('Top 20 Crime Types (2020-Present)')
for i, v in enumerate(crime_counts.values[::-1]):
    ax.text(v + 500, i, f'{v:,}', va='center', fontsize=8)
plt.tight_layout()
plt.savefig(figures_path + '02_top_crime_types.png', dpi=150)
plt.close()

# 3. Crimes over time
fig, ax = plt.subplots(figsize=(14, 6))
daily_counts = df.groupby('DATE OCC').size()
rolling = daily_counts.rolling(window=30).mean()
ax.plot(daily_counts.index, daily_counts.values, alpha=0.3, color='steelblue', label='Daily')
ax.plot(rolling.index, rolling.values, color='darkblue', linewidth=2, label='30-day rolling avg')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Crimes')
ax.set_title('Daily Crime Count Over Time')
ax.legend()
ax.set_xlim(pd.Timestamp('2020-01-01'), pd.Timestamp('2024-12-31'))
plt.tight_layout()
plt.savefig(figures_path + '03_crimes_over_time.png', dpi=150)
plt.close()

# 4. Crimes by hour of day
fig, ax = plt.subplots(figsize=(12, 5))
hourly_counts = df.groupby('hour').size()
ax.bar(hourly_counts.index, hourly_counts.values, color='teal')
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Number of Crimes')
ax.set_title('Crime Distribution by Hour of Day')
ax.set_xticks(range(0, 24))
plt.tight_layout()
plt.savefig(figures_path + '04_crimes_by_hour.png', dpi=150)
plt.close()

# 5. Victim age distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
valid_ages = df[df['Vict Age'] > 0]['Vict Age']
axes[0].hist(valid_ages, bins=50, color='steelblue', edgecolor='white')
axes[0].set_xlabel('Victim Age')
axes[0].set_ylabel('Count')
axes[0].set_title(f'Victim Age Distribution (Age > 0, n={len(valid_ages):,})')
axes[0].axvline(valid_ages.median(), color='red', linestyle='--', label=f'Median: {valid_ages.median():.0f}')
axes[0].legend()

zero_neg = df[df['Vict Age'] <= 0]['Vict Age'].value_counts().sort_index()
axes[1].bar([str(x) for x in zero_neg.index], zero_neg.values, color='coral')
axes[1].set_xlabel('Age Value')
axes[1].set_ylabel('Count')
axes[1].set_title(f'Problematic Age Values (Total: {len(df[df["Vict Age"] <= 0]):,})')
plt.tight_layout()
plt.savefig(figures_path + '05_victim_age_distribution.png', dpi=150)
plt.close()

print("Analysis complete. Figures saved to", figures_path)
