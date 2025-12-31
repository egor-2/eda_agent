import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

# Pivot to get TMAX and TMIN in the same row
temp_df = df[df['element'].isin(['TMAX', 'TMIN'])].copy()
temp_pivot = temp_df.pivot_table(index=['station_id', 'date'], columns='element', values='value', aggfunc='first').reset_index()
temp_pivot = temp_pivot.dropna()

# Convert to Celsius and filter reasonable values
temp_pivot['TMAX_C'] = temp_pivot['TMAX'] / 10.0
temp_pivot['TMIN_C'] = temp_pivot['TMIN'] / 10.0
temp_pivot = temp_pivot[(temp_pivot['TMAX_C'] >= -60) & (temp_pivot['TMAX_C'] <= 60) & 
                         (temp_pivot['TMIN_C'] >= -60) & (temp_pivot['TMIN_C'] <= 60)]

# Calculate temperature range
temp_pivot['TEMP_RANGE'] = temp_pivot['TMAX_C'] - temp_pivot['TMIN_C']

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. TMAX vs TMIN scatter plot
ax = axes[0, 0]
# Sample for visibility
sample = temp_pivot.sample(min(50000, len(temp_pivot)), random_state=42)
ax.scatter(sample['TMIN_C'], sample['TMAX_C'], alpha=0.1, s=1)
ax.plot([-60, 60], [-60, 60], 'r--', linewidth=2, label='TMAX = TMIN')
ax.set_xlabel('TMIN (°C)', fontsize=12)
ax.set_ylabel('TMAX (°C)', fontsize=12)
ax.set_title('TMAX vs TMIN Correlation', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_xlim(-60, 60)
ax.set_ylim(-60, 60)

# Calculate correlation
corr = temp_pivot[['TMAX_C', 'TMIN_C']].corr().iloc[0, 1]
ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=ax.transAxes, 
        fontsize=12, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 2. Temperature range distribution
ax = axes[0, 1]
ax.hist(temp_pivot['TEMP_RANGE'], bins=100, edgecolor='black', alpha=0.7, color='orange')
ax.set_xlabel('Daily Temperature Range (°C)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Distribution of Daily Temperature Range (TMAX - TMIN)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.axvline(temp_pivot['TEMP_RANGE'].mean(), color='red', linestyle='--', linewidth=2,
           label=f'Mean: {temp_pivot["TEMP_RANGE"].mean():.1f}°C')
ax.legend()

# 3. Check for invalid TMAX < TMIN
ax = axes[1, 0]
invalid = temp_pivot[temp_pivot['TMAX_C'] < temp_pivot['TMIN_C']]
print(f"\nInvalid measurements (TMAX < TMIN): {len(invalid):,} ({100*len(invalid)/len(temp_pivot):.2f}%)")

if len(invalid) > 0:
    ax.scatter(invalid['TMIN_C'], invalid['TMAX_C'], alpha=0.3, s=10, color='red')
    ax.plot([-60, 60], [-60, 60], 'k--', linewidth=2, label='TMAX = TMIN')
    ax.set_xlabel('TMIN (°C)', fontsize=12)
    ax.set_ylabel('TMAX (°C)', fontsize=12)
    ax.set_title(f'Invalid Cases: TMAX < TMIN ({len(invalid):,} cases)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend()
else:
    ax.text(0.5, 0.5, 'No invalid cases found', ha='center', va='center', transform=ax.transAxes, fontsize=14)
    ax.set_title('Invalid Cases: TMAX < TMIN', fontsize=14, fontweight='bold')

# 4. Temperature range by TMIN bins
ax = axes[1, 1]
temp_pivot['TMIN_bin'] = pd.cut(temp_pivot['TMIN_C'], bins=np.arange(-60, 61, 10))
temp_pivot.boxplot(column='TEMP_RANGE', by='TMIN_bin', ax=ax)
ax.set_xlabel('TMIN Bin (°C)', fontsize=12)
ax.set_ylabel('Temperature Range (°C)', fontsize=12)
ax.set_title('Temperature Range vs TMIN', fontsize=14, fontweight='bold')
ax.get_figure().suptitle('')  # Remove auto title
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/07_temperature_correlation.png', dpi=300, bbox_inches='tight')
print("Saved: 07_temperature_correlation.png")
plt.close()

# Statistics
print("\n=== TEMPERATURE STATISTICS ===")
print(f"Total days with both TMAX and TMIN: {len(temp_pivot):,}")
print(f"\nTemperature range:")
print(f"  Min: {temp_pivot['TEMP_RANGE'].min():.1f}°C")
print(f"  Max: {temp_pivot['TEMP_RANGE'].max():.1f}°C")
print(f"  Mean: {temp_pivot['TEMP_RANGE'].mean():.1f}°C")
print(f"  Median: {temp_pivot['TEMP_RANGE'].median():.1f}°C")

print(f"\nNegative temperature range (TMAX < TMIN): {(temp_pivot['TEMP_RANGE'] < 0).sum():,}")
print(f"Zero temperature range (TMAX = TMIN): {(temp_pivot['TEMP_RANGE'] == 0).sum():,}")
print(f"Large temperature range (>40°C): {(temp_pivot['TEMP_RANGE'] > 40).sum():,}")

