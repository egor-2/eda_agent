import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv')

output_dir = '/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/eda_sonnet/figures'

print("="*80)
print("DETAILED RATINGS INVESTIGATION")
print("="*80)

# Focus on rated books
rated_books = df[(df['ratings_count'] > 0) & (df['average_rating'].notna())]

print(f"\nTotal rated books: {len(rated_books)}")
print(f"\nRating distribution:")
print(rated_books['average_rating'].value_counts().sort_index())

# Check if rating=5 books have lower ratings_count
rating_5 = rated_books[rated_books['average_rating'] == 5.0]
rating_not_5 = rated_books[rated_books['average_rating'] < 5.0]

print(f"\n5.0 rating books: {len(rating_5)} ({len(rating_5)/len(rated_books)*100:.1f}%)")
print(f"  Mean ratings_count: {rating_5['ratings_count'].mean():.2f}")
print(f"  Median ratings_count: {rating_5['ratings_count'].median():.0f}")
print(f"  Max ratings_count: {rating_5['ratings_count'].max():.0f}")

print(f"\n<5.0 rating books: {len(rating_not_5)} ({len(rating_not_5)/len(rated_books)*100:.1f}%)")
print(f"  Mean ratings_count: {rating_not_5['ratings_count'].mean():.2f}")
print(f"  Median ratings_count: {rating_not_5['ratings_count'].median():.0f}")
print(f"  Max ratings_count: {rating_not_5['ratings_count'].max():.0f}")

# Distribution of ratings_count for rating=5 vs rating<5
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Histogram comparison
bins = np.logspace(0, np.log10(rated_books['ratings_count'].max()), 30)
axes[0].hist(rating_5['ratings_count'], bins=bins, alpha=0.5, label='Rating = 5.0', edgecolor='black')
axes[0].hist(rating_not_5['ratings_count'], bins=bins, alpha=0.5, label='Rating < 5.0', edgecolor='black')
axes[0].set_xscale('log')
axes[0].set_xlabel('Ratings Count (Log Scale)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Ratings Count Distribution: 5.0 vs <5.0')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Box plot comparison
data_to_plot = [rating_5['ratings_count'], rating_not_5['ratings_count']]
axes[1].boxplot(data_to_plot, labels=['Rating = 5.0', 'Rating < 5.0'])
axes[1].set_ylabel('Ratings Count')
axes[1].set_title('Ratings Count Comparison')
axes[1].set_yscale('log')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/20_rating_5_vs_not5.png', dpi=300, bbox_inches='tight')
plt.close()

# Check books with high ratings_count
print(f"\nBooks with >10 ratings:")
high_rating_count = rated_books[rated_books['ratings_count'] > 10]
print(f"  Total: {len(high_rating_count)}")
print(f"  Rating distribution:")
print(high_rating_count['average_rating'].value_counts().sort_index())

print(f"\nBooks with >50 ratings:")
very_high_rating_count = rated_books[rated_books['ratings_count'] > 50]
print(f"  Total: {len(very_high_rating_count)}")
print(f"  Rating distribution:")
print(very_high_rating_count['average_rating'].value_counts().sort_index())

# Sample some 5.0 rated books with only 1 rating
low_count_5_rating = rating_5[rating_5['ratings_count'] <= 2]
print(f"\n5.0 rated books with <=2 ratings: {len(low_count_5_rating)}")
print("\nSample of such books:")
print(low_count_5_rating[['title', 'authors', 'ratings_count', 'average_rating']].head(10))

# Scatter plot with density
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(rated_books['ratings_count'], rated_books['average_rating'], 
                     alpha=0.3, s=30, c=rated_books['ratings_count'], 
                     cmap='viridis', norm=plt.matplotlib.colors.LogNorm())
ax.set_xlabel('Ratings Count')
ax.set_ylabel('Average Rating')
ax.set_xscale('log')
ax.set_title('Ratings Count vs Average Rating (Colored by Count)')
ax.grid(True, alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Ratings Count (Log Scale)')
plt.tight_layout()
plt.savefig(f'{output_dir}/21_ratings_scatter_colored.png', dpi=300, bbox_inches='tight')
plt.close()

# Create bins for ratings_count and show average rating
bins_edges = [0, 1, 2, 5, 10, 20, 50, 1000]
rated_books['count_bin'] = pd.cut(rated_books['ratings_count'], bins=bins_edges)

print("\n" + "="*80)
print("Average rating by ratings_count bins:")
print("="*80)
for bin_label in rated_books['count_bin'].cat.categories:
    subset = rated_books[rated_books['count_bin'] == bin_label]
    if len(subset) > 0:
        print(f"{bin_label}: n={len(subset)}, mean_rating={subset['average_rating'].mean():.2f}, median_rating={subset['average_rating'].median():.1f}")

print("\n" + "="*80)
print("INTERPRETATION")
print("="*80)
print("The negative correlation between ratings_count and average_rating appears to be")
print("driven by the large number of books with very few ratings (often just 1) that")
print("happen to have a perfect 5.0 score. Books with more ratings show more variation")
print("and tend to regress toward lower average values.")
print("="*80)
