import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data
df = pd.read_parquet('/Users/yegorklochkov/repos/eda_agent/test/crime_data/Crime_Data_from_2020_to_Present.parquet')

# 1. Victim age distribution (excluding 0 and negative)
age_valid = df[df['Vict Age'] > 0]['Vict Age']
age_zero_count = (df['Vict Age'] == 0).sum()

fig, ax = plt.subplots(figsize=(14, 6))
ax.hist(age_valid, bins=60, color='teal', edgecolor='black', alpha=0.7)
ax.set_xlabel('Victim Age', fontsize=12)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title(f'Victim Age Distribution (Excluding {age_zero_count:,} records with age=0)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
ax.axvline(x=age_valid.median(), color='red', linestyle='--', linewidth=2, label=f'Median: {age_valid.median():.0f}')
ax.legend()
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/11_victim_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Age value frequency analysis (check for default values)
age_counts = df['Vict Age'].value_counts().sort_index()
top_ages = age_counts.nlargest(15)

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(range(len(top_ages)), top_ages.values, color='coral', edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(top_ages)))
ax.set_xticklabels(top_ages.index, fontsize=10)
ax.set_xlabel('Age Value', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Most Frequent Victim Age Values', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, (age, count) in enumerate(top_ages.items()):
    ax.text(i, count, f'{count:,}', ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/12_top_age_values.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Victim sex distribution
fig, ax = plt.subplots(figsize=(10, 6))
sex_counts = df['Vict Sex'].value_counts()
colors = ['steelblue', 'pink', 'gray', 'purple']
ax.bar(range(len(sex_counts)), sex_counts.values, color=colors[:len(sex_counts)], edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(sex_counts)))
ax.set_xticklabels(sex_counts.index, fontsize=11)
ax.set_ylabel('Number of Crimes', fontsize=12)
ax.set_title('Victim Sex Distribution', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, (sex, count) in enumerate(sex_counts.items()):
    ax.text(i, count, f'{count:,}\n({count/len(df)*100:.1f}%)', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/13_victim_sex.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Victim descent distribution
fig, ax = plt.subplots(figsize=(12, 8))
descent_counts = df['Vict Descent'].value_counts().head(12)
y_pos = np.arange(len(descent_counts))
ax.barh(y_pos, descent_counts.values, color='seagreen', edgecolor='black', alpha=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(descent_counts.index, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Number of Crimes', fontsize=12)
ax.set_title('Victim Descent/Ethnicity Distribution (Top 12)', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(descent_counts.values):
    ax.text(v, i, f' {v:,}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/14_victim_descent.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Age statistics by sex
age_by_sex = df[df['Vict Age'] > 0].groupby('Vict Sex')['Vict Age'].describe()

fig, ax = plt.subplots(figsize=(10, 6))
sex_groups = ['Male', 'Female', 'Unknown']
sex_groups = [s for s in sex_groups if s in age_by_sex.index]
positions = range(len(sex_groups))
bp = ax.boxplot([df[(df['Vict Sex'] == sex) & (df['Vict Age'] > 0)]['Vict Age'] for sex in sex_groups],
                 labels=sex_groups, patch_artist=True, showfliers=False)
for patch, color in zip(bp['boxes'], ['steelblue', 'pink', 'gray']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_ylabel('Victim Age', fontsize=12)
ax.set_title('Victim Age Distribution by Sex (outliers hidden)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/crime_data/eda_sonnet/figures/15_age_by_sex.png', dpi=300, bbox_inches='tight')
plt.close()

print("Victim analysis plots completed!")
print(f"\nAge=0 records: {age_zero_count:,} ({age_zero_count/len(df)*100:.1f}%)")
print(f"Negative age records: {(df['Vict Age'] < 0).sum()}")
