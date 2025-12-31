import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

# Calculate text lengths
df['review_length'] = df['review_text'].str.len()
df['word_count'] = df['review_text'].str.split().str.len()

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Review length distribution (characters)
review_lengths = df['review_length'].values
review_lengths_log = np.log10(review_lengths[review_lengths > 0])
axes[0, 0].hist(review_lengths_log, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
tick_locs = axes[0, 0].get_xticks()
axes[0, 0].set_xticklabels([f'{10**x:.0f}' for x in tick_locs])
axes[0, 0].set_xlabel('Review Length (characters)', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Distribution of Review Lengths (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)

# 2. Word count distribution
word_counts = df['word_count'].values
word_counts_log = np.log10(word_counts[word_counts > 0])
axes[0, 1].hist(word_counts_log, bins=50, color='lightgreen', edgecolor='black', alpha=0.7)
tick_locs = axes[0, 1].get_xticks()
axes[0, 1].set_xticklabels([f'{10**x:.0f}' for x in tick_locs])
axes[0, 1].set_xlabel('Word Count', fontsize=11)
axes[0, 1].set_ylabel('Frequency', fontsize=11)
axes[0, 1].set_title('Distribution of Word Counts (Log Scale)', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)

# 3. Review length by rating (box plot)
rating_order = sorted(df['rating'].unique())
data_for_box = [df[df['rating'] == r]['review_length'].values for r in rating_order]
bp = axes[1, 0].boxplot(data_for_box, labels=rating_order, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightcoral')
    patch.set_alpha(0.7)
axes[1, 0].set_xlabel('Rating', fontsize=11)
axes[1, 0].set_ylabel('Review Length (characters)', fontsize=11)
axes[1, 0].set_title('Review Length Distribution by Rating', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)

# 4. Statistics table
stats_data = []
for rating in rating_order:
    subset = df[df['rating'] == rating]['review_length']
    stats_data.append([
        rating,
        f"{subset.mean():.0f}",
        f"{subset.median():.0f}",
        f"{subset.std():.0f}"
    ])

axes[1, 1].axis('off')
table = axes[1, 1].table(cellText=stats_data,
                         colLabels=['Rating', 'Mean Length', 'Median Length', 'Std Dev'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0.2, 1, 0.6])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)
axes[1, 1].set_title('Review Length Statistics by Rating', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/04_text_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Text analysis completed!")
