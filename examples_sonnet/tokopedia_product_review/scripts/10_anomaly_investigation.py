import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])
df['review_length'] = df['review_text'].str.len()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Check sold_count vs actual review count
product_stats = df.groupby('product_id').agg({
    'sold_count': 'first',
    'review_id': 'count'
}).rename(columns={'review_id': 'actual_reviews'})

axes[0, 0].scatter(product_stats['sold_count'], product_stats['actual_reviews'], 
                   alpha=0.4, s=20, color='purple')
axes[0, 0].set_xlabel('Sold Count (from data)', fontsize=11)
axes[0, 0].set_ylabel('Actual Number of Reviews', fontsize=11)
axes[0, 0].set_title('Sold Count vs Actual Review Count', fontsize=12, fontweight='bold')
axes[0, 0].set_xscale('log')
axes[0, 0].set_yscale('log')
axes[0, 0].grid(True, alpha=0.3)

# Add diagonal reference line
max_val = max(product_stats['sold_count'].max(), product_stats['actual_reviews'].max())
axes[0, 0].plot([1, max_val], [1, max_val], 'r--', linewidth=1, alpha=0.5, label='x=y line')
axes[0, 0].legend()

# 2. Extremely short reviews
short_threshold = 10
very_short = df[df['review_length'] < short_threshold]
short_rating_dist = very_short['rating'].value_counts().sort_index()

axes[0, 1].bar(short_rating_dist.index, short_rating_dist.values, color='orange', edgecolor='black')
axes[0, 1].set_xlabel('Rating', fontsize=11)
axes[0, 1].set_ylabel('Count', fontsize=11)
axes[0, 1].set_title(f'Rating Distribution for Very Short Reviews (<{short_threshold} chars)', 
                     fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)

for rating, count in short_rating_dist.items():
    pct = count / len(very_short) * 100
    axes[0, 1].text(rating, count, f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=8)

# 3. Sentiment-rating mismatch
# Low rating but positive sentiment
mismatch_pos = df[(df['rating'] <= 2) & (df['sentiment_label'] == 'positive')]
# High rating but negative sentiment
mismatch_neg = df[(df['rating'] >= 4) & (df['sentiment_label'] == 'negative')]

mismatch_data = [len(mismatch_pos), len(mismatch_neg), len(df) - len(mismatch_pos) - len(mismatch_neg)]
labels = [f'Low rating +\nPositive sentiment\n({len(mismatch_pos)})', 
          f'High rating +\nNegative sentiment\n({len(mismatch_neg)})',
          f'Consistent\n({len(df) - len(mismatch_pos) - len(mismatch_neg)})']
colors = ['yellow', 'pink', 'lightgreen']

axes[1, 0].pie(mismatch_data, labels=labels, colors=colors, autopct=lambda p: f'{p:.1f}%' if p > 1 else '', 
               startangle=90)
axes[1, 0].set_title('Sentiment-Rating Consistency', fontsize=12, fontweight='bold')

# 4. Products with suspiciously uniform ratings
product_rating_stats = df.groupby('product_id').agg({
    'rating': ['std', 'count', 'mean']
})
product_rating_stats.columns = ['rating_std', 'review_count', 'rating_mean']
# Filter to products with at least 10 reviews
products_10plus = product_rating_stats[product_rating_stats['review_count'] >= 10]
# Find products with very low std (all ratings similar)
uniform_products = products_10plus[products_10plus['rating_std'] < 0.5]

axes[1, 1].hist(products_10plus['rating_std'], bins=30, color='steelblue', 
                edgecolor='black', alpha=0.7, label='All products (10+ reviews)')
axes[1, 1].axvline(x=0.5, color='red', linestyle='--', linewidth=2, 
                   label=f'Uniform threshold (0.5)\n{len(uniform_products)} products')
axes[1, 1].set_xlabel('Rating Standard Deviation', fontsize=11)
axes[1, 1].set_ylabel('Number of Products', fontsize=11)
axes[1, 1].set_title('Rating Variability (Products with 10+ Reviews)', fontsize=12, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/09_anomaly_investigation.png', dpi=300, bbox_inches='tight')
plt.close()

# Save anomaly statistics
with open('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/anomaly_stats.txt', 'w') as f:
    f.write("ANOMALY AND DATA QUALITY INVESTIGATION\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"Very short reviews (<{short_threshold} characters):\n")
    f.write(f"  Count: {len(very_short)} ({len(very_short)/len(df)*100:.2f}%)\n")
    f.write(f"  Average rating: {very_short['rating'].mean():.2f}\n")
    
    f.write(f"\nSentiment-Rating mismatches:\n")
    f.write(f"  Low rating (1-2) but positive sentiment: {len(mismatch_pos)} ({len(mismatch_pos)/len(df)*100:.2f}%)\n")
    f.write(f"  High rating (4-5) but negative sentiment: {len(mismatch_neg)} ({len(mismatch_neg)/len(df)*100:.2f}%)\n")
    
    f.write(f"\nProducts with uniform ratings (std < 0.5, 10+ reviews):\n")
    f.write(f"  Count: {len(uniform_products)} out of {len(products_10plus)} ({len(uniform_products)/len(products_10plus)*100:.1f}%)\n")
    if len(uniform_products) > 0:
        f.write(f"  Most uniform: std = {uniform_products['rating_std'].min():.3f}\n")

print("Anomaly investigation completed!")
