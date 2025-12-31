import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/global_climat/ghcn_daily_1901_kaggle.csv')

# Create figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Source flags
ax = axes[0, 0]
sflag_counts = df['sflag'].value_counts()
ax.bar(range(len(sflag_counts)), sflag_counts.values, edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(sflag_counts)))
ax.set_xticklabels(sflag_counts.index, rotation=45, ha='right')
ax.set_xlabel('Source Flag', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Distribution of Source Flags (sflag)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add percentage labels for top flags
for i, (flag, count) in enumerate(sflag_counts.items()):
    pct = 100 * count / len(df)
    if pct > 5:  # Only label flags with >5%
        ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)

# 2. Quality flags (for non-null only)
ax = axes[0, 1]
qflag_counts = df['qflag'].value_counts()
ax.bar(range(len(qflag_counts)), qflag_counts.values, edgecolor='black', alpha=0.7, color='orange')
ax.set_xticks(range(len(qflag_counts)))
ax.set_xticklabels(qflag_counts.index, rotation=45, ha='right')
ax.set_xlabel('Quality Flag', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Distribution of Quality Flags (qflag, non-null)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# 3. Measurement flags (for non-null only)
ax = axes[1, 0]
mflag_counts = df['mflag'].value_counts()
ax.bar(range(len(mflag_counts)), mflag_counts.values, edgecolor='black', alpha=0.7, color='green')
ax.set_xticks(range(len(mflag_counts)))
ax.set_xticklabels(mflag_counts.index, rotation=45, ha='right')
ax.set_xlabel('Measurement Flag', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Distribution of Measurement Flags (mflag, non-null)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# 4. Missing data pattern
ax = axes[1, 1]
missing_data = {
    'qflag': df['qflag'].isnull().sum(),
    'obstime': df['obstime'].isnull().sum(),
    'mflag': df['mflag'].isnull().sum()
}
colors = ['red' if v > len(df) * 0.5 else 'orange' if v > len(df) * 0.1 else 'green' for v in missing_data.values()]
ax.bar(range(len(missing_data)), list(missing_data.values()), edgecolor='black', alpha=0.7, color=colors)
ax.set_xticks(range(len(missing_data)))
ax.set_xticklabels(list(missing_data.keys()))
ax.set_xlabel('Column', fontsize=12)
ax.set_ylabel('Missing Count', fontsize=12)
ax.set_title('Missing Values by Column', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (col, count) in enumerate(missing_data.items()):
    pct = 100 * count / len(df)
    ax.text(i, count, f'{pct:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/global_climat/eda_sonnet/figures/05_data_quality_flags.png', dpi=300, bbox_inches='tight')
print("Saved: 05_data_quality_flags.png")
plt.close()

# Print statistics
print("\n=== DATA QUALITY FLAG ANALYSIS ===")
print(f"\nTotal measurements: {len(df):,}")
print(f"\nMeasurements with quality flag (qflag): {df['qflag'].notna().sum():,} ({100*df['qflag'].notna().sum()/len(df):.2f}%)")
print(f"Measurements with measurement flag (mflag): {df['mflag'].notna().sum():,} ({100*df['mflag'].notna().sum()/len(df):.2f}%)")
print(f"Measurements with observation time: {df['obstime'].notna().sum():,} ({100*df['obstime'].notna().sum()/len(df):.2f}%)")

print("\n=== QUALITY FLAG MEANINGS (qflag) ===")
print("I: Failed internal consistency check")
print("D: Failed duplicate check")
print("Other flags indicate various quality issues")
print(f"\nMeasurements failing quality checks: {df['qflag'].notna().sum():,}")

