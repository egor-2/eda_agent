import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Price by rating (box plot with binned approach)
# Bin prices for better visualization
df['price_bin'] = pd.cut(df['product_price'], 
                          bins=[0, 50000, 100000, 200000, 500000, df['product_price'].max()],
                          labels=['<50K', '50K-100K', '100K-200K', '200K-500K', '>500K'])

rating_order = sorted(df['rating'].unique())
data_for_box = [df[df['rating'] == r]['product_price'].values for r in rating_order]
bp = axes[0, 0].boxplot(data_for_box, tick_labels=rating_order, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
    patch.set_alpha(0.7)
axes[0, 0].set_xlabel('Rating', fontsize=11)
axes[0, 0].set_ylabel('Price (IDR)', fontsize=11)
axes[0, 0].set_title('Price Distribution by Rating', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)
axes[0, 0].set_yscale('log')

# 2. Rating distribution by price bin
rating_by_price = df.groupby(['price_bin', 'rating']).size().unstack(fill_value=0)
rating_by_price_pct = rating_by_price.div(rating_by_price.sum(axis=1), axis=0) * 100
rating_by_price_pct.plot(kind='bar', stacked=True, ax=axes[0, 1], 
                          colormap='RdYlGn', width=0.8)
axes[0, 1].set_xlabel('Price Range', fontsize=11)
axes[0, 1].set_ylabel('Percentage', fontsize=11)
axes[0, 1].set_title('Rating Distribution by Price Range', fontsize=12, fontweight='bold')
axes[0, 1].legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[0, 1].grid(axis='y', alpha=0.3)
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha='right')

# 3. Average rating by price bin
avg_rating_by_price = df.groupby('price_bin')['rating'].agg(['mean', 'count'])
x_pos = range(len(avg_rating_by_price))
bars = axes[1, 0].bar(x_pos, avg_rating_by_price['mean'], color='coral', edgecolor='black')
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(avg_rating_by_price.index, rotation=45, ha='right')
axes[1, 0].set_xlabel('Price Range', fontsize=11)
axes[1, 0].set_ylabel('Average Rating', fontsize=11)
axes[1, 0].set_title('Average Rating by Price Range', fontsize=12, fontweight='bold')
axes[1, 0].set_ylim([0, 5.5])
axes[1, 0].axhline(y=df['rating'].mean(), color='red', linestyle='--', linewidth=1, 
                   label=f'Overall: {df["rating"].mean():.2f}')
axes[1, 0].grid(axis='y', alpha=0.3)
axes[1, 0].legend()

# Add counts on bars
for i, (idx, row) in enumerate(avg_rating_by_price.iterrows()):
    axes[1, 0].text(i, row['mean'], f'{row["mean"]:.2f}\n(n={int(row["count"])})', 
                    ha='center', va='bottom', fontsize=8)

# 4. Statistics table
stats_data = []
for rating in rating_order:
    subset = df[df['rating'] == rating]['product_price']
    stats_data.append([
        rating,
        f'{subset.mean():,.0f}',
        f'{subset.median():,.0f}',
        f'{len(subset):,}'
    ])

axes[1, 1].axis('off')
table = axes[1, 1].table(cellText=stats_data,
                         colLabels=['Rating', 'Mean Price', 'Median Price', 'Count'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0.2, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)
axes[1, 1].set_title('Price Statistics by Rating', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/07_price_rating_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Price-rating analysis completed!")
