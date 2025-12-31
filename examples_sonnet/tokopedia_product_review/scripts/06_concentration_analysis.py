import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

# Calculate review concentration
product_review_counts = df.groupby('product_id').size().sort_values(ascending=False)
total_reviews = len(df)

# Calculate cumulative percentages
cumsum = product_review_counts.cumsum()
cumsum_pct = (cumsum / total_reviews) * 100
product_pct = (np.arange(1, len(product_review_counts) + 1) / len(product_review_counts)) * 100

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Concentration curve
axes[0, 0].plot(product_pct, cumsum_pct.values, linewidth=2, color='darkblue')
axes[0, 0].plot([0, 100], [0, 100], 'r--', linewidth=1, label='Perfect equality')
axes[0, 0].set_xlabel('Percentage of Products', fontsize=11)
axes[0, 0].set_ylabel('Cumulative % of Reviews', fontsize=11)
axes[0, 0].set_title('Review Concentration Curve (Lorenz Curve)', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()

# Add annotations for key percentiles
for pct in [1, 5, 10, 20]:
    idx = int(len(product_review_counts) * pct / 100) - 1
    if idx < len(cumsum_pct):
        axes[0, 0].scatter([pct], [cumsum_pct.iloc[idx]], color='red', s=50, zorder=5)
        axes[0, 0].annotate(f'{pct}% → {cumsum_pct.iloc[idx]:.1f}%', 
                           xy=(pct, cumsum_pct.iloc[idx]),
                           xytext=(pct+5, cumsum_pct.iloc[idx]-5),
                           fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# 2. Reviews per product distribution
reviews_per_product = product_review_counts.values
reviews_per_product_log = np.log10(reviews_per_product)
axes[0, 1].hist(reviews_per_product_log, bins=50, color='purple', edgecolor='black', alpha=0.7)
tick_locs = axes[0, 1].get_xticks()
axes[0, 1].set_xticklabels([f'{10**x:.0f}' for x in tick_locs])
axes[0, 1].set_xlabel('Reviews per Product', fontsize=11)
axes[0, 1].set_ylabel('Number of Products', fontsize=11)
axes[0, 1].set_title('Distribution of Reviews per Product (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)

# 3. Shop concentration
shop_review_counts = df.groupby('shop_id').size().sort_values(ascending=False)
top_shops = shop_review_counts.head(20)
axes[1, 0].barh(range(len(top_shops)), top_shops.values, color='teal', edgecolor='black')
axes[1, 0].set_yticks(range(len(top_shops)))
axes[1, 0].set_yticklabels([f'Shop {shop_id}' for shop_id in top_shops.index], fontsize=8)
axes[1, 0].set_xlabel('Number of Reviews', fontsize=11)
axes[1, 0].set_title('Top 20 Shops by Review Count', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3)
axes[1, 0].invert_yaxis()

# Add percentages
for i, (shop, count) in enumerate(top_shops.items()):
    pct = count / total_reviews * 100
    axes[1, 0].text(count, i, f' {count} ({pct:.1f}%)', va='center', fontsize=7)

# 4. Concentration statistics table
stats_data = []
for pct in [1, 5, 10, 20, 50]:
    idx = int(len(product_review_counts) * pct / 100) - 1
    if idx < len(cumsum_pct):
        stats_data.append([
            f'{pct}%',
            f'{cumsum_pct.iloc[idx]:.1f}%',
            f'{product_review_counts.iloc[idx]:.0f}'
        ])

axes[1, 1].axis('off')
table = axes[1, 1].table(cellText=stats_data,
                         colLabels=['Top Products', '% of Total Reviews', 'Min Reviews in Group'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0.2, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)
axes[1, 1].set_title('Review Concentration Statistics', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/05_concentration_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# Save concentration statistics
with open('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/concentration_stats.txt', 'w') as f:
    f.write("REVIEW CONCENTRATION ANALYSIS\n")
    f.write("=" * 60 + "\n\n")
    
    for pct in [1, 5, 10, 20, 50]:
        idx = int(len(product_review_counts) * pct / 100) - 1
        if idx < len(cumsum_pct):
            f.write(f"Top {pct}% of products account for {cumsum_pct.iloc[idx]:.2f}% of all reviews\n")
    
    f.write(f"\nTotal unique products: {len(product_review_counts)}\n")
    f.write(f"Products with only 1 review: {(product_review_counts == 1).sum()} ({(product_review_counts == 1).sum() / len(product_review_counts) * 100:.1f}%)\n")
    f.write(f"Products with >100 reviews: {(product_review_counts > 100).sum()} ({(product_review_counts > 100).sum() / len(product_review_counts) * 100:.1f}%)\n")

print("Concentration analysis completed!")
