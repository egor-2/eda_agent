import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

# Temperature distributions
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

for idx, element in enumerate(['TMAX', 'TMIN', 'TOBS']):
    temp_data = df[df['element'] == element]['value'].values / 10.0  # Convert to °C
    
    # Histogram
    ax = axes[0, idx]
    ax.hist(temp_data, bins=100, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Temperature (°C)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(f'{element} Distribution (All Values)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axvline(temp_data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {temp_data.mean():.1f}°C')
    ax.axvline(np.median(temp_data), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(temp_data):.1f}°C')
    ax.legend()
    
    # Histogram with reasonable range
    ax = axes[1, idx]
    reasonable_temp = temp_data[(temp_data >= -60) & (temp_data <= 60)]
    ax.hist(reasonable_temp, bins=100, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Temperature (°C)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title(f'{element} Distribution (Filtered: -60 to 60°C)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axvline(reasonable_temp.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {reasonable_temp.mean():.1f}°C')
    ax.axvline(np.median(reasonable_temp), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(reasonable_temp):.1f}°C')
    ax.legend()
    
    # Report outliers
    outliers = len(temp_data) - len(reasonable_temp)
    print(f"{element}: {outliers:,} outliers beyond [-60, 60]°C ({100*outliers/len(temp_data):.2f}%)")

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/01_temperature_distributions.png', dpi=300, bbox_inches='tight')
print("Saved: 01_temperature_distributions.png")
plt.close()

# Extreme values investigation
print("\n=== EXTREME TEMPERATURE VALUES ===")
for element in ['TMAX', 'TMIN', 'TOBS']:
    temp_df = df[df['element'] == element].copy()
    temp_df['temp_celsius'] = temp_df['value'] / 10.0
    
    print(f"\n{element}:")
    # Physically impossible high values
    extreme_high = temp_df[temp_df['temp_celsius'] > 60]
    if len(extreme_high) > 0:
        print(f"  Values > 60°C: {len(extreme_high)}")
        print(f"  Max: {extreme_high['temp_celsius'].max():.1f}°C")
        print(f"  Sample stations: {extreme_high['station_id'].value_counts().head()}")
    
    # Physically impossible low values
    extreme_low = temp_df[temp_df['temp_celsius'] < -90]
    if len(extreme_low) > 0:
        print(f"  Values < -90°C: {len(extreme_low)}")
        print(f"  Min: {extreme_low['temp_celsius'].min():.1f}°C")

