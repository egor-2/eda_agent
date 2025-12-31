import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')

# Analyze sold_count
sold_count_dist = df['sold_count'].value_counts().sort_values(ascending=False)

# Calculate concentration on round numbers
round_numbers = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
on_round_numbers = df['sold_count'].isin(round_numbers).sum()
pct_round = on_round_numbers / len(df) * 100

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Top 30 most common sold_count values
top_sold = sold_count_dist.head(30)
axes[0, 0].bar(range(len(top_sold)), top_sold.values, color='steelblue', edgecolor='black')
axes[0, 0].set_xticks(range(len(top_sold)))
axes[0, 0].set_xticklabels([f'{x:,}' for x in top_sold.index], rotation=90, fontsize=7)
axes[0, 0].set_xlabel('Sold Count Value', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Top 30 Most Common Sold Count Values', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)

# 2. Highlight round numbers
is_round = df['sold_count'].isin(round_numbers)
fig2_data = [df[is_round].shape[0], df[~is_round].shape[0]]
labels = [f'Round numbers\n({pct_round:.1f}%)', f'Other values\n({100-pct_round:.1f}%)']
colors = ['coral', 'lightblue']
axes[0, 1].pie(fig2_data, labels=labels, colors=colors, autopct='%d', startangle=90)
axes[0, 1].set_title('Distribution: Round vs Other Sold Count Values', fontsize=12, fontweight='bold')

# 3. Sold count distribution (full range, log scale)
unique_sold = df['sold_count'].unique()
unique_sold_sorted = np.sort(unique_sold)
counts_per_value = [df[df['sold_count'] == v].shape[0] for v in unique_sold_sorted]

axes[1, 0].scatter(unique_sold_sorted, counts_per_value, alpha=0.6, s=30, color='purple')
axes[1, 0].set_xscale('log')
axes[1, 0].set_yscale('log')
axes[1, 0].set_xlabel('Sold Count (log scale)', fontsize=11)
axes[1, 0].set_ylabel('Number of Reviews (log scale)', fontsize=11)
axes[1, 0].set_title('Sold Count vs Number of Reviews', fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# 4. Statistics table
axes[1, 1].axis('off')
stats_text = f"""
Sold Count Statistics:

Total reviews: {len(df):,}
Unique sold_count values: {df['sold_count'].nunique()}

Most common values:
  {top_sold.index[0]:,}: {top_sold.values[0]:,} reviews ({top_sold.values[0]/len(df)*100:.1f}%)
  {top_sold.index[1]:,}: {top_sold.values[1]:,} reviews ({top_sold.values[1]/len(df)*100:.1f}%)
  {top_sold.index[2]:,}: {top_sold.values[2]:,} reviews ({top_sold.values[2]/len(df)*100:.1f}%)

Round number concentration:
  {on_round_numbers:,} reviews ({pct_round:.1f}%)
  on values: {', '.join([str(x) for x in round_numbers[:8]])}
  and others

Range: {df['sold_count'].min():,} to {df['sold_count'].max():,}
Median: {df['sold_count'].median():,.0f}
"""
axes[1, 1].text(0.1, 0.5, stats_text, fontsize=10, family='monospace', 
                verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/06_sold_count_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save detailed statistics
with open('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/sold_count_stats.txt', 'w') as f:
    f.write("SOLD COUNT ANALYSIS\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total reviews: {len(df):,}\n")
    f.write(f"Unique sold_count values: {df['sold_count'].nunique()}\n\n")
    
    f.write("Top 15 most common sold_count values:\n")
    for i, (val, count) in enumerate(sold_count_dist.head(15).items(), 1):
        pct = count / len(df) * 100
        f.write(f"  {i:2d}. {val:>10,}: {count:>6,} reviews ({pct:5.2f}%)\n")
    
    f.write(f"\nRound number concentration:\n")
    f.write(f"  Reviews with round sold_count: {on_round_numbers:,} ({pct_round:.2f}%)\n")
    f.write(f"  Round numbers checked: {round_numbers}\n")

print("Sold count investigation completed!")
