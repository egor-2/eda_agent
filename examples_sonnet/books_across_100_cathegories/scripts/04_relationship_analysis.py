import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv')
df['published_year'] = pd.to_datetime(df['published_date'], errors='coerce').dt.year

output_dir = '/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/eda_sonnet/figures'

# 1. Relationship between page count and price
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Filter for books with both page count and price
books_with_both = df[(df['page_count'] > 0) & (df['list_price'] > 0)]

axes[0].scatter(books_with_both['page_count'], books_with_both['list_price'], alpha=0.3, s=10)
axes[0].set_xlabel('Page Count')
axes[0].set_ylabel('Price (USD)')
axes[0].set_title(f'Page Count vs Price (n={len(books_with_both)})')
axes[0].grid(True, alpha=0.3)

# Log-log scale for better visualization
axes[1].scatter(books_with_both['page_count'], books_with_both['list_price'], alpha=0.3, s=10)
axes[1].set_xlabel('Page Count')
axes[1].set_ylabel('Price (USD)')
axes[1].set_xscale('log')
axes[1].set_yscale('log')
axes[1].set_title('Page Count vs Price (Log-Log Scale)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/09_page_count_vs_price.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Box plot: Price by page count bins
fig, ax = plt.subplots(figsize=(12, 6))

# Create bins for page count
books_with_both['page_bin'] = pd.cut(books_with_both['page_count'], 
                                       bins=[0, 100, 200, 300, 500, 1000, 10000],
                                       labels=['0-100', '100-200', '200-300', '300-500', '500-1000', '1000+'])

# Remove bins with too few samples
bin_counts = books_with_both['page_bin'].value_counts()
valid_bins = bin_counts[bin_counts >= 10].index
books_filtered = books_with_both[books_with_both['page_bin'].isin(valid_bins)]

if len(books_filtered) > 0:
    books_filtered.boxplot(column='list_price', by='page_bin', ax=ax)
    ax.set_xlabel('Page Count Range')
    ax.set_ylabel('Price (USD)')
    ax.set_title('Price Distribution by Page Count Range')
    plt.suptitle('')  # Remove default title
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/10_price_by_page_bins.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Ratings count vs average rating
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

rated_books = df[(df['ratings_count'] > 0) & (df['average_rating'].notna())]

axes[0].scatter(rated_books['ratings_count'], rated_books['average_rating'], alpha=0.4, s=20)
axes[0].set_xlabel('Ratings Count')
axes[0].set_ylabel('Average Rating')
axes[0].set_title(f'Ratings Count vs Average Rating (n={len(rated_books)})')
axes[0].grid(True, alpha=0.3)

# Log scale for ratings count
axes[1].scatter(rated_books['ratings_count'], rated_books['average_rating'], alpha=0.4, s=20)
axes[1].set_xlabel('Ratings Count (Log Scale)')
axes[1].set_ylabel('Average Rating')
axes[1].set_xscale('log')
axes[1].set_title('Ratings Count vs Average Rating (Log Scale)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/11_ratings_count_vs_average.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Average rating by ratings count bins
fig, ax = plt.subplots(figsize=(10, 6))

# Create bins for ratings count
rated_books['rating_count_bin'] = pd.cut(rated_books['ratings_count'],
                                           bins=[0, 1, 5, 10, 50, 1000],
                                           labels=['1', '2-5', '6-10', '11-50', '50+'])

rated_books.boxplot(column='average_rating', by='rating_count_bin', ax=ax)
ax.set_xlabel('Number of Ratings')
ax.set_ylabel('Average Rating')
ax.set_title('Average Rating Distribution by Ratings Count')
plt.suptitle('')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/12_rating_by_count_bins.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Publication year trends
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Books per year (recent years)
recent_years = df[(df['published_year'] >= 2000) & (df['published_year'] <= 2025)]
year_counts = recent_years['published_year'].value_counts().sort_index()

axes[0].plot(year_counts.index, year_counts.values, marker='o', linewidth=2)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Books')
axes[0].set_title('Books Published per Year (2000-2025)')
axes[0].grid(True, alpha=0.3)

# Average page count over time
year_page_avg = recent_years.groupby('published_year')['page_count'].mean()
year_page_median = recent_years.groupby('published_year')['page_count'].median()

axes[1].plot(year_page_avg.index, year_page_avg.values, marker='o', label='Mean', linewidth=2)
axes[1].plot(year_page_median.index, year_page_median.values, marker='s', label='Median', linewidth=2)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Page Count')
axes[1].set_title('Average Page Count Over Time (2000-2025)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/13_publication_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Missing data heatmap
fig, ax = plt.subplots(figsize=(10, 8))

# Calculate missing data percentage for each column
missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)
missing_data = pd.DataFrame({'Missing %': missing_pct})

# Create horizontal bar chart
ax.barh(range(len(missing_data)), missing_data['Missing %'].values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(missing_data)))
ax.set_yticklabels(missing_data.index)
ax.set_xlabel('Missing Data (%)')
ax.set_title('Missing Data Analysis by Column')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

# Add percentage labels
for i, v in enumerate(missing_data['Missing %'].values):
    if v > 0:
        ax.text(v, i, f' {v:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(f'{output_dir}/14_missing_data_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Language distribution
fig, ax = plt.subplots(figsize=(10, 6))

top_languages = df['language'].value_counts().head(15)
ax.bar(range(len(top_languages)), top_languages.values, edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(top_languages)))
ax.set_xticklabels(top_languages.index, rotation=45, ha='right')
ax.set_xlabel('Language Code')
ax.set_ylabel('Number of Books')
ax.set_title('Top 15 Languages')
ax.grid(True, alpha=0.3, axis='y')

# Add count labels
for i, v in enumerate(top_languages.values):
    ax.text(i, v, f'{v}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(f'{output_dir}/15_language_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Books by top authors
fig, ax = plt.subplots(figsize=(10, 8))

all_authors = df['authors'].dropna().str.split(',').explode().str.strip()
top_authors = all_authors.value_counts().head(20)

ax.barh(range(len(top_authors)), top_authors.values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_authors)))
ax.set_yticklabels(top_authors.index)
ax.set_xlabel('Number of Books')
ax.set_title('Top 20 Most Prolific Authors')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(f'{output_dir}/16_top_authors.png', dpi=300, bbox_inches='tight')
plt.close()

print("Relationship analysis visualizations created successfully!")
