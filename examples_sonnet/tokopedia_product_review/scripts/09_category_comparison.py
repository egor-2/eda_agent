import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

# Get top categories
top_categories = df['product_category'].value_counts().head(6).index

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Average rating by category
cat_stats = df[df['product_category'].isin(top_categories)].groupby('product_category').agg({
    'rating': ['mean', 'std', 'count']
}).reset_index()
cat_stats.columns = ['category', 'mean_rating', 'std_rating', 'count']
cat_stats = cat_stats.sort_values('mean_rating', ascending=False)

x_pos = range(len(cat_stats))
bars = axes[0, 0].bar(x_pos, cat_stats['mean_rating'], yerr=cat_stats['std_rating'], 
                      color='skyblue', edgecolor='black', capsize=5)
axes[0, 0].set_xticks(x_pos)
axes[0, 0].set_xticklabels(cat_stats['category'], rotation=45, ha='right', fontsize=9)
axes[0, 0].set_ylabel('Average Rating', fontsize=11)
axes[0, 0].set_title('Average Rating by Category (with Std Dev)', fontsize=12, fontweight='bold')
axes[0, 0].set_ylim([0, 5.5])
axes[0, 0].axhline(y=df['rating'].mean(), color='red', linestyle='--', linewidth=1)
axes[0, 0].grid(axis='y', alpha=0.3)

for i, row in cat_stats.iterrows():
    axes[0, 0].text(x_pos[i], row['mean_rating'], f'{row["mean_rating"]:.2f}', 
                    ha='center', va='bottom', fontsize=8)

# 2. Price distribution by category
cat_price_data = [df[df['product_category'] == cat]['product_price'].values 
                  for cat in top_categories]
bp = axes[0, 1].boxplot(cat_price_data, tick_labels=[cat[:15] for cat in top_categories], 
                        patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightcoral')
    patch.set_alpha(0.7)
axes[0, 1].set_xticklabels([cat[:15] for cat in top_categories], rotation=45, ha='right', fontsize=8)
axes[0, 1].set_ylabel('Price (IDR)', fontsize=11)
axes[0, 1].set_title('Price Distribution by Category', fontsize=12, fontweight='bold')
axes[0, 1].set_yscale('log')
axes[0, 1].grid(axis='y', alpha=0.3)

# 3. Review length by category
df['review_length'] = df['review_text'].str.len()
cat_length = df[df['product_category'].isin(top_categories)].groupby('product_category')['review_length'].mean().sort_values()
axes[1, 0].barh(range(len(cat_length)), cat_length.values, color='lightgreen', edgecolor='black')
axes[1, 0].set_yticks(range(len(cat_length)))
axes[1, 0].set_yticklabels([cat[:20] for cat in cat_length.index], fontsize=9)
axes[1, 0].set_xlabel('Average Review Length (characters)', fontsize=11)
axes[1, 0].set_title('Average Review Length by Category', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='x', alpha=0.3)

for i, (cat, length) in enumerate(cat_length.items()):
    axes[1, 0].text(length, i, f' {length:.0f}', va='center', fontsize=8)

# 4. Category statistics table
stats_data = []
for cat in top_categories[:6]:
    subset = df[df['product_category'] == cat]
    stats_data.append([
        cat[:20],
        f'{subset["rating"].mean():.2f}',
        f'{subset["product_price"].median():,.0f}',
        f'{len(subset):,}'
    ])

axes[1, 1].axis('off')
table = axes[1, 1].table(cellText=stats_data,
                         colLabels=['Category', 'Avg Rating', 'Med Price', 'Reviews'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0.2, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 2.5)
axes[1, 1].set_title('Category Statistics Summary', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/08_category_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("Category comparison completed!")
