import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')

# 1. Top 15 crime types
fig, ax = plt.subplots(figsize=(12, 8))
top_crimes = df['Crm Cd Desc'].value_counts().head(15)
y_pos = np.arange(len(top_crimes))
ax.barh(y_pos, top_crimes.values, color='steelblue', edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(top_crimes.index, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Number of Incidents', fontsize=12)
ax.set_title('Top 15 Crime Types', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(top_crimes.values):
    ax.text(v, i, f' {v:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/07_top_crimes.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Crime concentration analysis
crime_counts = df['Crm Cd Desc'].value_counts()
total_crimes = len(df)
crime_types = len(crime_counts)

cumsum = crime_counts.cumsum() / total_crimes * 100
pct_1 = (cumsum <= 50).sum()
pct_5 = (cumsum <= 80).sum()
pct_10 = (cumsum <= 90).sum()

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(1, len(cumsum) + 1)
ax.plot(x, cumsum.values, linewidth=2, color='darkred')
ax.axhline(y=50, color='green', linestyle='--', linewidth=1, label='50% of crimes')
ax.axhline(y=80, color='orange', linestyle='--', linewidth=1, label='80% of crimes')
ax.axhline(y=90, color='red', linestyle='--', linewidth=1, label='90% of crimes')
ax.set_xlabel('Number of Crime Types (ranked by frequency)', fontsize=12)
ax.set_ylabel('Cumulative Percentage of All Crimes', fontsize=12)
ax.set_title('Crime Type Concentration Curve', fontsize=14, fontweight='bold')
ax.grid(alpha=0.3)
ax.legend()
ax.text(pct_1, 52, f'{pct_1} types', fontsize=10, ha='left')
ax.text(pct_5, 82, f'{pct_5} types', fontsize=10, ha='left')
ax.text(pct_10, 92, f'{pct_10} types', fontsize=10, ha='left')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/08_crime_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Part 1-2 distribution
fig, ax = plt.subplots(figsize=(8, 6))
part_counts = df['Part 1-2'].value_counts().sort_index()
labels = ['Part 1 (Serious)', 'Part 2 (Less Serious)']
ax.bar([1, 2], part_counts.values, color=['darkred', 'steelblue'], edgecolor='black', alpha=0.7, width=0.6)
ax.set_xticks([1, 2])
ax.set_xticklabels(labels)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Crime Severity Distribution', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, (part, count) in enumerate(part_counts.items()):
    ax.text(part, count, f'{count:,}\n({count/total_crimes*100:.1f}%)', ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/09_crime_severity.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Status distribution
fig, ax = plt.subplots(figsize=(10, 6))
status_counts = df['Status Desc'].value_counts()
colors = plt.cm.Set3(range(len(status_counts)))
wedges, texts, autotexts = ax.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%',
                                    colors=colors, startangle=90, textprops={'fontsize': 10})
ax.set_title('Case Status Distribution', fontsize=14, fontweight='bold')
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/10_status_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("Crime type analysis plots completed!")
print(f"\nConcentration stats:")
print(f"Top {pct_1} crime types account for 50% of all crimes")
print(f"Top {pct_5} crime types account for 80% of all crimes")
print(f"Total crime types: {crime_types}")
