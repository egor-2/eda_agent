import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Top product categories
category_counts = df['product_category'].value_counts().head(10)
axes[0, 0].barh(range(len(category_counts)), category_counts.values, color='coral', edgecolor='black')
axes[0, 0].set_yticks(range(len(category_counts)))
axes[0, 0].set_yticklabels(category_counts.index, fontsize=9)
axes[0, 0].set_xlabel('Number of Reviews', fontsize=11)
axes[0, 0].set_title('Top Product Categories by Review Count', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='x', alpha=0.3)
for i, (cat, count) in enumerate(category_counts.items()):
    pct = count / len(df) * 100
    axes[0, 0].text(count, i, f' {count} ({pct:.1f}%)', va='center', fontsize=9)

# 2. Price distribution (log scale)
prices = df['product_price'].values
prices_log = np.log10(prices[prices > 0])
axes[0, 1].hist(prices_log, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
tick_locs = axes[0, 1].get_xticks()
axes[0, 1].set_xticklabels([f'{10**x:.0f}' for x in tick_locs])
axes[0, 1].set_xlabel('Price (IDR)', fontsize=11)
axes[0, 1].set_ylabel('Frequency', fontsize=11)
axes[0, 1].set_title('Distribution of Product Prices (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)

# 3. Top products by review count
product_counts = df.groupby('product_name').size().sort_values(ascending=False).head(15)
axes[1, 0].barh(range(len(product_counts)), product_counts.values, color='lightgreen', edgecolor='black')
axes[1, 0].set_yticks(range(len(product_counts)))
# Truncate long names
truncated_names = [name[:40] + '...' if len(name) > 40 else name for name in product_counts.index]
axes[1, 0].set_yticklabels(truncated_names, fontsize=8)
axes[1, 0].set_xlabel('Number of Reviews', fontsize=11)
axes[1, 0].set_title('Top 15 Products by Review Count', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3)
axes[1, 0].invert_yaxis()

# 4. Sold count distribution
sold_counts = df['sold_count'].value_counts().sort_index()
# Get top 20 most common sold counts
top_sold = sold_counts.nlargest(20).sort_index()
axes[1, 1].bar(range(len(top_sold)), top_sold.values, color='plum', edgecolor='black')
axes[1, 1].set_xticks(range(len(top_sold)))
axes[1, 1].set_xticklabels([f'{x:,}' for x in top_sold.index], rotation=45, ha='right', fontsize=8)
axes[1, 1].set_xlabel('Sold Count', fontsize=11)
axes[1, 1].set_ylabel('Number of Products', fontsize=11)
axes[1, 1].set_title('Distribution of Top 20 Sold Count Values', fontsize=12, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/02_product_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Product analysis completed!")
