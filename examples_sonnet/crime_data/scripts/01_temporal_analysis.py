import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')

# Convert TIME OCC to hour
df['hour'] = df['TIME OCC'].apply(lambda x: x.hour)

# 1. Crimes by year
fig, ax = plt.subplots(figsize=(10, 6))
yearly_counts = df['occ_year'].value_counts().sort_index()
ax.bar(yearly_counts.index, yearly_counts.values, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Reports by Year', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, (year, count) in enumerate(yearly_counts.items()):
    ax.text(year, count, f'{count:,}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/01_crimes_by_year.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Crimes by month
fig, ax = plt.subplots(figsize=(12, 6))
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_counts = df['occ_month'].value_counts().reindex(month_order)
ax.bar(range(12), monthly_counts.values, color='coral', edgecolor='black', alpha=0.7)
ax.set_xticks(range(12))
ax.set_xticklabels(month_order)
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Reports by Month (2020-2025)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/02_crimes_by_month.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Crimes by day of week
fig, ax = plt.subplots(figsize=(10, 6))
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
day_counts = df['occ_day'].value_counts().reindex(day_order)
ax.bar(range(7), day_counts.values, color='seagreen', edgecolor='black', alpha=0.7)
ax.set_xticks(range(7))
ax.set_xticklabels(day_order)
ax.set_xlabel('Day of Week', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Reports by Day of Week', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/03_crimes_by_day.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Crimes by hour of day
fig, ax = plt.subplots(figsize=(14, 6))
hourly_counts = df['hour'].value_counts().sort_index()
ax.bar(hourly_counts.index, hourly_counts.values, color='purple', edgecolor='black', alpha=0.7)
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Reports by Hour of Day', fontsize=14, fontweight='bold')
ax.set_xticks(range(0, 24))
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/04_crimes_by_hour.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Time series - monthly aggregation
df['year_month'] = pd.to_datetime(df['DATE OCC']).dt.to_period('M')
monthly_series = df.groupby('year_month').size()
monthly_series.index = monthly_series.index.to_timestamp()

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(monthly_series.index, monthly_series.values, linewidth=2, color='darkblue', marker='o', markersize=3)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Monthly Crime Count Time Series (2020-2025)', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/05_monthly_timeseries.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Reporting delay
df['report_delay_days'] = (df['Date Rptd'] - df['DATE OCC']).dt.days
delay_valid = df[df['report_delay_days'] >= 0]['report_delay_days']

fig, ax = plt.subplots(figsize=(12, 6))
# Use log bins for better visualization
bins = np.logspace(0, np.log10(delay_valid.max() + 1), 50)
ax.hist(delay_valid, bins=bins, color='orange', edgecolor='black', alpha=0.7)
ax.set_xscale('log')
ax.set_xlabel('Reporting Delay (Days, log scale)', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Distribution of Crime Reporting Delay', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/06_reporting_delay.png', dpi=300, bbox_inches='tight')
plt.close()

print("Temporal analysis plots completed!")
