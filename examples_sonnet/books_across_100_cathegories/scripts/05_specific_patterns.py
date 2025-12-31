import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv')
df['published_year'] = pd.to_datetime(df['published_date'], errors='coerce').dt.year

output_dir = '/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/eda_sonnet/figures'

print("="*80)
print("SPECIFIC PATTERN ANALYSIS")
print("="*80)

# 1. Investigate page_count = 0
print("\n1. PAGE COUNT = 0 INVESTIGATION")
page_zero = df[df['page_count'] == 0]
page_nonzero = df[df['page_count'] > 0]

print(f"Books with page_count=0: {len(page_zero)} ({len(page_zero)/len(df)*100:.1f}%)")
print(f"\nCategories of books with page_count=0:")
print(page_zero['categories'].value_counts().head(10))

print(f"\nSearch categories of books with page_count=0:")
print(page_zero['search_category'].value_counts().head(10))

# Compare missing data between page_count=0 and page_count>0
print(f"\nMissing data comparison:")
print(f"Books with page_count=0 missing description: {page_zero['description'].isna().sum()/len(page_zero)*100:.1f}%")
print(f"Books with page_count>0 missing description: {page_nonzero['description'].isna().sum()/len(page_nonzero)*100:.1f}%")

# 2. Correlation between ratings_count and average_rating
print("\n2. RATINGS COUNT vs AVERAGE RATING ANALYSIS")
rated_books = df[(df['ratings_count'] > 0) & (df['average_rating'].notna())]
if len(rated_books) > 10:
    corr, pval = stats.spearmanr(rated_books['ratings_count'], rated_books['average_rating'])
    print(f"Spearman correlation: {corr:.3f} (p-value: {pval:.4f})")
    
    # Group by rating and show average ratings_count
    print(f"\nAverage ratings_count by rating:")
    for rating in sorted(rated_books['average_rating'].unique()):
        subset = rated_books[rated_books['average_rating'] == rating]
        print(f"Rating {rating}: mean={subset['ratings_count'].mean():.1f}, median={subset['ratings_count'].median():.0f}, n={len(subset)}")

# 3. Price analysis by category
print("\n3. PRICE ANALYSIS BY CATEGORY")
books_with_price = df[df['list_price'] > 0]
category_prices = books_with_price.groupby('categories')['list_price'].agg(['mean', 'median', 'count'])
category_prices = category_prices[category_prices['count'] >= 10].sort_values('mean', ascending=False)
print("\nTop 10 most expensive categories (by mean price):")
print(category_prices.head(10))

print("\nTop 10 least expensive categories (by mean price):")
print(category_prices.tail(10))

# Visualize top expensive categories
fig, ax = plt.subplots(figsize=(10, 8))
top_expensive = category_prices.head(15)
ax.barh(range(len(top_expensive)), top_expensive['mean'].values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_expensive)))
ax.set_yticklabels(top_expensive.index)
ax.set_xlabel('Average Price (USD)')
ax.set_title('Top 15 Most Expensive Book Categories')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/17_expensive_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Check buyable vs not buyable characteristics
print("\n4. BUYABLE vs NOT BUYABLE ANALYSIS")
buyable = df[df['buyable'] == True]
not_buyable = df[df['buyable'] == False]

print(f"\nBuyable books: {len(buyable)} ({len(buyable)/len(df)*100:.1f}%)")
print(f"Not buyable books: {len(not_buyable)} ({len(not_buyable)/len(df)*100:.1f}%)")

print(f"\nPage count statistics:")
print(f"Buyable - mean: {buyable['page_count'].mean():.0f}, median: {buyable['page_count'].median():.0f}")
print(f"Not buyable - mean: {not_buyable['page_count'].mean():.0f}, median: {not_buyable['page_count'].median():.0f}")

print(f"\nTop categories for buyable books:")
print(buyable['categories'].value_counts().head(10))

print(f"\nTop categories for not buyable books:")
print(not_buyable['categories'].value_counts().head(10))

# 5. Search category concentration
print("\n5. SEARCH CATEGORY CONCENTRATION ANALYSIS")
search_cat_counts = df['search_category'].value_counts()
print(f"\nTotal search categories: {len(search_cat_counts)}")
print(f"Top 10 categories account for: {search_cat_counts.head(10).sum()/len(df)*100:.1f}% of books")
print(f"Top 20 categories account for: {search_cat_counts.head(20).sum()/len(df)*100:.1f}% of books")

# Cumulative distribution
cumsum_pct = (search_cat_counts.cumsum() / len(df) * 100).values
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(range(1, len(cumsum_pct)+1), cumsum_pct, linewidth=2)
ax.set_xlabel('Number of Search Categories (Ranked)')
ax.set_ylabel('Cumulative Percentage of Books (%)')
ax.set_title('Cumulative Distribution of Books Across Search Categories')
ax.grid(True, alpha=0.3)
ax.axhline(y=50, color='r', linestyle='--', alpha=0.5, label='50% threshold')
ax.axhline(y=80, color='orange', linestyle='--', alpha=0.5, label='80% threshold')
ax.legend()
plt.tight_layout()
plt.savefig(f'{output_dir}/18_search_category_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# Find how many categories cover 50% and 80%
n_for_50 = (cumsum_pct >= 50).argmax() + 1
n_for_80 = (cumsum_pct >= 80).argmax() + 1
print(f"\nTop {n_for_50} categories cover 50% of books")
print(f"Top {n_for_80} categories cover 80% of books")

# 6. Publisher analysis
print("\n6. PUBLISHER ANALYSIS")
print(f"Books with publisher: {df['publisher'].notna().sum()} ({df['publisher'].notna().sum()/len(df)*100:.1f}%)")
top_publishers = df['publisher'].value_counts().head(20)
print("\nTop 20 publishers:")
print(top_publishers)

# Visualize
fig, ax = plt.subplots(figsize=(10, 8))
ax.barh(range(len(top_publishers)), top_publishers.values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_publishers)))
ax.set_yticklabels(top_publishers.index)
ax.set_xlabel('Number of Books')
ax.set_title('Top 20 Publishers')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/19_top_publishers.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. ISBN coverage
print("\n7. ISBN ANALYSIS")
has_isbn13 = df['isbn_13'].notna().sum()
has_isbn10 = df['isbn_10'].notna().sum()
has_both = df[(df['isbn_13'].notna()) & (df['isbn_10'].notna())].shape[0]
has_either = df[(df['isbn_13'].notna()) | (df['isbn_10'].notna())].shape[0]

print(f"Books with ISBN-13: {has_isbn13} ({has_isbn13/len(df)*100:.1f}%)")
print(f"Books with ISBN-10: {has_isbn10} ({has_isbn10/len(df)*100:.1f}%)")
print(f"Books with both ISBNs: {has_both} ({has_both/len(df)*100:.1f}%)")
print(f"Books with at least one ISBN: {has_either} ({has_either/len(df)*100:.1f}%)")

print("\n" + "="*80)
print("Specific pattern analysis complete!")
print("="*80)
