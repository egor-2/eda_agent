import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')
prcp_data = df[df['element'] == 'PRCP']['value'].values

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Full distribution histogram
ax = axes[0, 0]
ax.hist(prcp_data, bins=100, edgecolor='black', alpha=0.7)
ax.set_xlabel('Precipitation (mm)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('PRCP Distribution (All Values)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(prcp_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {prcp_data.mean():.1f} mm')
ax.axvline(np.median(prcp_data), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(prcp_data):.1f} mm')
ax.legend()

# 2. Non-zero precipitation only
ax = axes[0, 1]
nonzero_prcp = prcp_data[prcp_data > 0]
ax.hist(nonzero_prcp, bins=100, edgecolor='black', alpha=0.7)
ax.set_xlabel('Precipitation (mm)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('PRCP Distribution (Non-zero only)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(nonzero_prcp.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {nonzero_prcp.mean():.1f} mm')
ax.axvline(np.median(nonzero_prcp), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(nonzero_prcp):.1f} mm')
ax.legend()

# 3. Log-transformed (non-zero values)
ax = axes[1, 0]
log_prcp = np.log10(nonzero_prcp)
ax.hist(log_prcp, bins=50, edgecolor='black', alpha=0.7)
tick_locations = ax.get_xticks()
ax.set_xticklabels([f'{10**x:.1f}' for x in tick_locations])
ax.set_xlabel('Precipitation (mm, log scale)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('PRCP Distribution (Log-transformed, non-zero)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# 4. Most common values bar chart
ax = axes[1, 1]
top_values = pd.Series(prcp_data).value_counts().head(20)
ax.bar(range(len(top_values)), top_values.values, edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(top_values)))
ax.set_xticklabels([f'{v}' for v in top_values.index], rotation=45, ha='right')
ax.set_xlabel('PRCP Value (mm)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Top 20 Most Common PRCP Values', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (val, count) in enumerate(top_values.items()):
    pct = 100 * count / len(prcp_data)
    if i < 5:  # Only label top 5
        ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/02_precipitation_distributions.png', dpi=300, bbox_inches='tight')
print("Saved: 02_precipitation_distributions.png")
plt.close()

# Analysis of negative precipitation
negative_prcp = prcp_data[prcp_data < 0]
print(f"\nNegative precipitation values: {len(negative_prcp):,} ({100*len(negative_prcp)/len(prcp_data):.3f}%)")
if len(negative_prcp) > 0:
    print(f"  Min: {negative_prcp.min()} mm")
    print(f"  Unique negative values: {np.unique(negative_prcp)}")

