import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv')

# Convert published_date to datetime
df['published_year'] = pd.to_datetime(df['published_date'], errors='coerce').dt.year

print("="*80)
print("COMPREHENSIVE DATA ANALYSIS")
print("="*80)

# Basic statistics
print("\n1. DATASET OVERVIEW")
print(f"Total books: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Missing data analysis
print("\n2. MISSING DATA ANALYSIS")
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Count': missing,
    'Percentage': missing_pct
}).sort_values('Percentage', ascending=False)
print(missing_df[missing_df['Percentage'] > 0])

# Duplicate analysis
print("\n3. DUPLICATE ANALYSIS")
dup_books = df.duplicated(subset='book_id').sum()
dup_all = df.duplicated().sum()
print(f"Duplicate book_ids: {dup_books}")
print(f"Fully duplicate rows: {dup_all}")

# Numerical columns analysis
print("\n4. NUMERICAL VARIABLES STATISTICS")
numerical_cols = ['page_count', 'average_rating', 'ratings_count', 'list_price']
print(df[numerical_cols].describe())

# Check for zeros in ratings_count
print(f"\nBooks with 0 ratings: {(df['ratings_count'] == 0).sum()} ({(df['ratings_count'] == 0).sum()/len(df)*100:.1f}%)")
print(f"Books with ratings > 0: {(df['ratings_count'] > 0).sum()} ({(df['ratings_count'] > 0).sum()/len(df)*100:.1f}%)")

# Average rating analysis (only for rated books)
rated_books = df[df['average_rating'].notna()]
print(f"\nBooks with average_rating: {len(rated_books)} ({len(rated_books)/len(df)*100:.1f}%)")
if len(rated_books) > 0:
    print(f"Average rating stats:\n{rated_books['average_rating'].describe()}")

# Language distribution
print("\n5. LANGUAGE DISTRIBUTION")
print(df['language'].value_counts().head(10))

# Categories analysis
print("\n6. CATEGORIES ANALYSIS")
print(f"Books with categories: {df['categories'].notna().sum()} ({df['categories'].notna().sum()/len(df)*100:.1f}%)")
print(f"Unique categories: {df['categories'].nunique()}")
print("\nTop 20 categories:")
print(df['categories'].value_counts().head(20))

# Search category analysis  
print("\n7. SEARCH CATEGORY ANALYSIS")
print(f"Unique search categories: {df['search_category'].nunique()}")
print("\nTop 20 search categories:")
print(df['search_category'].value_counts().head(20))

# Buyable analysis
print("\n8. BUYABILITY ANALYSIS")
print(df['buyable'].value_counts())
print(f"\nBuyable books with list_price: {df[df['buyable'] == True]['list_price'].notna().sum()}")
print(f"Buyable books without list_price: {df[df['buyable'] == True]['list_price'].isna().sum()}")

# Currency analysis
print("\n9. CURRENCY ANALYSIS")
if df['currency'].notna().sum() > 0:
    print(df['currency'].value_counts())

# Published year analysis
print("\n10. PUBLISHED YEAR ANALYSIS")
valid_years = df[df['published_year'].notna() & (df['published_year'] >= 1800) & (df['published_year'] <= 2025)]
print(f"Valid years: {len(valid_years)}")
print(f"Year range: {valid_years['published_year'].min():.0f} to {valid_years['published_year'].max():.0f}")
print(f"\nYear statistics:\n{valid_years['published_year'].describe()}")

# Page count analysis - check for default values
print("\n11. PAGE COUNT ANALYSIS - DEFAULT VALUES")
page_counts = df['page_count'].dropna()
value_counts = page_counts.value_counts().head(20)
print("Top 20 most frequent page counts:")
print(value_counts)

# Check for concentration at round numbers
round_numbers = [10, 20, 50, 100, 200, 300, 400, 500, 1000]
round_count = sum([sum(page_counts == n) for n in round_numbers])
print(f"\nBooks with round page counts ({round_numbers}): {round_count} ({round_count/len(page_counts)*100:.1f}%)")

# Title and subtitle length
print("\n12. TEXT LENGTH ANALYSIS")
df['title_length'] = df['title'].fillna('').str.len()
df['subtitle_length'] = df['subtitle'].fillna('').str.len()
df['description_length'] = df['description'].fillna('').str.len()
print(f"Title length: mean={df['title_length'].mean():.1f}, median={df['title_length'].median():.1f}")
print(f"Subtitle length: mean={df['subtitle_length'].mean():.1f}, median={df['subtitle_length'].median():.1f}")
print(f"Description length: mean={df['description_length'].mean():.1f}, median={df['description_length'].median():.1f}")

# Author analysis
print("\n13. AUTHOR ANALYSIS")
print(f"Books with authors: {df['authors'].notna().sum()} ({df['authors'].notna().sum()/len(df)*100:.1f}%)")
# Count number of authors per book
df['num_authors'] = df['authors'].fillna('').apply(lambda x: len(x.split(',')) if x else 0)
print(f"Books with multiple authors: {(df['num_authors'] > 1).sum()}")
print(f"\nMost prolific authors:")
all_authors = df['authors'].dropna().str.split(',').explode().str.strip()
print(all_authors.value_counts().head(15))

print("\n" + "="*80)
print("Analysis complete. Generating visualizations...")
print("="*80)
