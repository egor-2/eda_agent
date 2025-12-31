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

# 1. Page count distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Remove 0 values for better visualization
page_counts_nonzero = df[df['page_count'] > 0]['page_count']

# Histogram with log-transformed data
log_pages = np.log10(page_counts_nonzero)
axes[0].hist(log_pages, bins=50, edgecolor='black', alpha=0.7)
tick_locations = axes[0].get_xticks()
axes[0].set_xticklabels([f'{10**x:.0f}' for x in tick_locations])
axes[0].set_xlabel('Page Count')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Page Counts (Log Scale)')
axes[0].grid(True, alpha=0.3)

# Box plot
axes[1].boxplot(page_counts_nonzero, vert=True)
axes[1].set_ylabel('Page Count')
axes[1].set_title('Page Count Distribution (Box Plot)')
axes[1].set_xticks([])
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/01_page_count_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Page count = 0 analysis
fig, ax = plt.subplots(figsize=(8, 6))
page_zero_counts = df['page_count'].value_counts().head(20)
ax.bar(range(len(page_zero_counts)), page_zero_counts.values, edgecolor='black')
ax.set_xticks(range(len(page_zero_counts)))
ax.set_xticklabels([f'{int(x)}' for x in page_zero_counts.index], rotation=45, ha='right')
ax.set_xlabel('Page Count Value')
ax.set_ylabel('Number of Books')
ax.set_title('Top 20 Most Frequent Page Count Values')
ax.grid(True, alpha=0.3, axis='y')
# Add percentage annotation for page_count=0
if page_zero_counts.index[0] == 0.0:
    pct = page_zero_counts.values[0] / df['page_count'].notna().sum() * 100
    ax.text(0, page_zero_counts.values[0], f'{pct:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{output_dir}/02_page_count_frequent_values.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Published year distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

valid_years = df[(df['published_year'] >= 1800) & (df['published_year'] <= 2025)]['published_year']
axes[0].hist(valid_years, bins=50, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Books')
axes[0].set_title('Distribution of Publication Years')
axes[0].grid(True, alpha=0.3)

# Focus on recent years
recent_years = df[(df['published_year'] >= 2000) & (df['published_year'] <= 2025)]['published_year']
axes[1].hist(recent_years, bins=26, edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Number of Books')
axes[1].set_title('Distribution of Publication Years (2000-2025)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}/03_publication_year_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Average rating distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

rated_books = df[df['average_rating'].notna()]
axes[0].hist(rated_books['average_rating'], bins=20, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Average Rating')
axes[0].set_ylabel('Number of Books')
axes[0].set_title(f'Distribution of Average Ratings (n={len(rated_books)})')
axes[0].grid(True, alpha=0.3)

# Rating distribution with counts
rating_counts = rated_books['average_rating'].value_counts().sort_index()
axes[1].bar(rating_counts.index, rating_counts.values, width=0.3, edgecolor='black', alpha=0.7)
axes[1].set_xlabel('Average Rating')
axes[1].set_ylabel('Number of Books')
axes[1].set_title('Rating Value Frequency')
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{output_dir}/04_average_rating_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Ratings count distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ratings_with_counts = df[df['ratings_count'] > 0]['ratings_count']
log_ratings = np.log10(ratings_with_counts)
axes[0].hist(log_ratings, bins=30, edgecolor='black', alpha=0.7)
tick_locations = axes[0].get_xticks()
axes[0].set_xticklabels([f'{10**x:.0f}' for x in tick_locations])
axes[0].set_xlabel('Ratings Count')
axes[0].set_ylabel('Frequency')
axes[0].set_title(f'Distribution of Ratings Count (Log Scale, n={len(ratings_with_counts)})')
axes[0].grid(True, alpha=0.3)

# Pie chart for rated vs unrated
rated_status = ['No ratings (0)', 'Has ratings (>0)']
rated_counts = [(df['ratings_count'] == 0).sum(), (df['ratings_count'] > 0).sum()]
axes[1].pie(rated_counts, labels=rated_status, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Books by Rating Status')

plt.tight_layout()
plt.savefig(f'{output_dir}/05_ratings_count_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. List price distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

prices = df[df['list_price'] > 0]['list_price']
log_prices = np.log10(prices)
axes[0].hist(log_prices, bins=40, edgecolor='black', alpha=0.7)
tick_locations = axes[0].get_xticks()
axes[0].set_xticklabels([f'{10**x:.1f}' for x in tick_locations])
axes[0].set_xlabel('Price (USD)')
axes[0].set_ylabel('Frequency')
axes[0].set_title(f'Distribution of List Prices (Log Scale, n={len(prices)})')
axes[0].grid(True, alpha=0.3)

# Buyable status
buyable_counts = df['buyable'].value_counts()
axes[1].bar(['Not Buyable', 'Buyable'], buyable_counts.values, edgecolor='black', alpha=0.7)
axes[1].set_ylabel('Number of Books')
axes[1].set_title('Buyability Status')
axes[1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(buyable_counts.values):
    axes[1].text(i, v, f'{v}\n({v/len(df)*100:.1f}%)', ha='center', va='bottom')

plt.tight_layout()
plt.savefig(f'{output_dir}/06_price_and_buyability.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Top categories
fig, ax = plt.subplots(figsize=(10, 8))
top_categories = df['categories'].value_counts().head(20)
ax.barh(range(len(top_categories)), top_categories.values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_categories)))
ax.set_yticklabels(top_categories.index)
ax.set_xlabel('Number of Books')
ax.set_title('Top 20 Book Categories')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/07_top_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Top search categories
fig, ax = plt.subplots(figsize=(10, 8))
top_search = df['search_category'].value_counts().head(20)
ax.barh(range(len(top_search)), top_search.values, edgecolor='black', alpha=0.7)
ax.set_yticks(range(len(top_search)))
ax.set_yticklabels(top_search.index)
ax.set_xlabel('Number of Books')
ax.set_title('Top 20 Search Categories')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f'{output_dir}/08_top_search_categories.png', dpi=300, bbox_inches='tight')
plt.close()

print("Distribution visualizations created successfully!")
