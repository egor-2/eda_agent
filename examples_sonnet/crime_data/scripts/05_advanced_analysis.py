import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')
df['hour'] = df['TIME OCC'].apply(lambda x: x.hour)

# 1. Crime types by hour - heatmap of top crimes
top_crimes = df['Crm Cd Desc'].value_counts().head(10).index
hourly_crime_data = []
for crime in top_crimes:
    hourly_counts = df[df['Crm Cd Desc'] == crime].groupby('hour').size()
    hourly_crime_data.append([hourly_counts.get(h, 0) for h in range(24)])

fig, ax = plt.subplots(figsize=(16, 8))
im = ax.imshow(hourly_crime_data, aspect='auto', cmap='YlOrRd', interpolation='nearest')
ax.set_yticks(range(len(top_crimes)))
ax.set_yticklabels([c[:40] + '...' if len(c) > 40 else c for c in top_crimes], fontsize=9)
ax.set_xticks(range(24))
ax.set_xticklabels(range(24))
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_title('Crime Type Distribution by Hour of Day (Top 10 Crimes)', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='Number of Crimes')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/21_crime_hour_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Arrest rate by crime type (top 15)
top_crimes_list = df['Crm Cd Desc'].value_counts().head(15).index
arrest_rates = []
crime_labels = []
for crime in top_crimes_list:
    subset = df[df['Crm Cd Desc'] == crime]
    arrests = subset[subset['Status Desc'].str.contains('Arrest', na=False)]
    rate = len(arrests) / len(subset) * 100
    arrest_rates.append(rate)
    crime_labels.append(crime[:35] + '...' if len(crime) > 35 else crime)

fig, ax = plt.subplots(figsize=(12, 8))
y_pos = np.arange(len(arrest_rates))
colors = ['darkgreen' if r > 20 else 'orange' if r > 10 else 'red' for r in arrest_rates]
ax.barh(y_pos, arrest_rates, color=colors, edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(crime_labels, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Arrest Rate (%)', fontsize=12)
ax.set_title('Arrest Rate by Crime Type (Top 15 Crimes)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(arrest_rates):
    ax.text(v, i, f' {v:.1f}%', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/22_arrest_rate_by_crime.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Crimes by day of week and hour
day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
day_hour_data = []
for day in day_order:
    hourly_counts = df[df['occ_day'] == day].groupby('hour').size()
    day_hour_data.append([hourly_counts.get(h, 0) for h in range(24)])

fig, ax = plt.subplots(figsize=(16, 6))
im = ax.imshow(day_hour_data, aspect='auto', cmap='viridis', interpolation='nearest')
ax.set_yticks(range(7))
ax.set_yticklabels(day_order)
ax.set_xticks(range(24))
ax.set_xticklabels(range(24))
ax.set_xlabel('Hour of Day', fontsize=12)
ax.set_ylabel('Day of Week', fontsize=12)
ax.set_title('Crime Distribution by Day of Week and Hour', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='Number of Crimes')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/23_day_hour_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Age distribution by crime type (top 5 crimes, excluding age=0)
top5_crimes = df['Crm Cd Desc'].value_counts().head(5).index
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

for i, crime in enumerate(top5_crimes):
    subset = df[(df['Crm Cd Desc'] == crime) & (df['Vict Age'] > 0)]
    axes[i].hist(subset['Vict Age'], bins=40, color='teal', edgecolor='black', alpha=0.7)
    axes[i].set_xlabel('Victim Age', fontsize=10)
    axes[i].set_ylabel('Count', fontsize=10)
    axes[i].set_title(crime[:40] + ('...' if len(crime) > 40 else ''), fontsize=10)
    axes[i].grid(alpha=0.3)
    axes[i].axvline(x=subset['Vict Age'].median(), color='red', linestyle='--', 
                    label=f'Median: {subset["Vict Age"].median():.0f}')
    axes[i].legend(fontsize=8)

# Remove extra subplot
axes[5].axis('off')

plt.suptitle('Victim Age Distribution by Crime Type (Top 5 Crimes)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/24_age_by_crime_type.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Violent vs Property crimes over time
violent_keywords = ['ASSAULT', 'BATTERY', 'ROBBERY', 'RAPE', 'HOMICIDE', 'KIDNAPPING', 'SHOTS']
property_keywords = ['THEFT', 'BURGLARY', 'STOLEN', 'VANDALISM', 'SHOPLIFTING']

df['crime_category'] = 'Other'
for keyword in violent_keywords:
    df.loc[df['Crm Cd Desc'].str.contains(keyword, case=False, na=False), 'crime_category'] = 'Violent'
for keyword in property_keywords:
    df.loc[df['Crm Cd Desc'].str.contains(keyword, case=False, na=False) & 
           (df['crime_category'] == 'Other'), 'crime_category'] = 'Property'

df['year_month'] = pd.to_datetime(df['DATE OCC']).dt.to_period('M')
monthly_by_category = df.groupby(['year_month', 'crime_category']).size().unstack(fill_value=0)
monthly_by_category.index = monthly_by_category.index.to_timestamp()

fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(monthly_by_category.index, monthly_by_category['Violent'], 
        linewidth=2, label='Violent Crimes', marker='o', markersize=3)
ax.plot(monthly_by_category.index, monthly_by_category['Property'], 
        linewidth=2, label='Property Crimes', marker='s', markersize=3)
ax.plot(monthly_by_category.index, monthly_by_category['Other'], 
        linewidth=2, label='Other Crimes', marker='^', markersize=3)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Trends by Category (Monthly)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/25_crime_trends_by_category.png', dpi=300, bbox_inches='tight')
plt.close()

print("Advanced analysis plots completed!")

# Print category distribution
print("\nCrime category distribution:")
print(df['crime_category'].value_counts())
