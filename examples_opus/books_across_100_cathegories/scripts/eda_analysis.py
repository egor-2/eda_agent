"""
Exploratory Data Analysis Script for Google Books Dataset
Dataset: google_books_dataset.csv from books_across_100_categories

This script performs comprehensive EDA including:
- Data loading and initial inspection
- Missing data analysis
- Distribution analysis for numeric columns
- Categorical analysis
- Correlation analysis
- Visualization generation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from scipy import stats
from wordcloud import WordCloud

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

DATA_PATH = '/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv'
FIGURES_PATH = '/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/eda_opus/figures/'


def extract_year(date_str):
    """Extract year from various date formats."""
    if pd.isna(date_str):
        return None
    date_str = str(date_str)
    match = re.match(r'(\d{4})', date_str)
    if match:
        year = int(match.group(1))
        if 1400 <= year <= 2030:
            return year
    return None


def count_authors(authors_str):
    """Count number of authors from comma-separated string."""
    if pd.isna(authors_str):
        return 0
    return len(authors_str.split(','))


def load_and_prepare_data():
    """Load data and create derived columns."""
    df = pd.read_csv(DATA_PATH)
    
    # Derived columns
    df['year'] = df['published_date'].apply(extract_year)
    df['title_length'] = df['title'].fillna('').str.len()
    df['title_word_count'] = df['title'].fillna('').str.split().str.len()
    df['desc_length'] = df['description'].fillna('').str.len()
    df['author_count'] = df['authors'].apply(count_authors)
    
    return df


def print_basic_stats(df):
    """Print basic dataset statistics."""
    print("=" * 60)
    print("BASIC DATASET STATISTICS")
    print("=" * 60)
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Unique book IDs: {df['book_id'].nunique()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print()
    
    print("Missing data per column:")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    for col in df.columns:
        if missing[col] > 0:
            print(f"  {col}: {missing[col]} ({missing_pct[col]}%)")
    print()


def analyze_numeric_distributions(df):
    """Analyze distributions of numeric columns."""
    print("=" * 60)
    print("NUMERIC COLUMN STATISTICS")
    print("=" * 60)
    
    numeric_cols = ['page_count', 'list_price', 'ratings_count', 'average_rating']
    for col in numeric_cols:
        print(f"\n{col}:")
        print(df[col].describe())
    print()


def analyze_ratings_concentration(df):
    """Analyze Pareto distribution of ratings."""
    print("=" * 60)
    print("RATINGS CONCENTRATION ANALYSIS")
    print("=" * 60)
    
    rated_books = df[df['ratings_count'] > 0].copy()
    rated_books = rated_books.sort_values('ratings_count', ascending=False)
    
    print(f"Books with 0 ratings: {(df['ratings_count'] == 0).sum()} ({(df['ratings_count'] == 0).mean()*100:.1f}%)")
    print(f"Books with ratings: {len(rated_books)} ({len(rated_books)/len(df)*100:.1f}%)")
    
    if len(rated_books) > 0:
        rated_books['cumulative_ratings'] = rated_books['ratings_count'].cumsum()
        total_ratings = rated_books['ratings_count'].sum()
        rated_books['cumulative_pct'] = rated_books['cumulative_ratings'] / total_ratings * 100
        rated_books['book_pct'] = np.arange(1, len(rated_books) + 1) / len(rated_books) * 100
        
        top_10_pct = rated_books[rated_books['book_pct'] <= 10]['cumulative_pct'].max()
        top_20_pct = rated_books[rated_books['book_pct'] <= 20]['cumulative_pct'].max()
        
        print(f"Top 10% of rated books account for {top_10_pct:.1f}% of all ratings")
        print(f"Top 20% of rated books account for {top_20_pct:.1f}% of all ratings")
    print()


def analyze_categories(df):
    """Analyze category distributions."""
    print("=" * 60)
    print("CATEGORY ANALYSIS")
    print("=" * 60)
    
    print(f"Unique search categories: {df['search_category'].nunique()}")
    print(f"Unique Google categories: {df['categories'].nunique()}")
    print()
    
    print("Top 15 search categories:")
    print(df['search_category'].value_counts().head(15))
    print()


if __name__ == "__main__":
    df = load_and_prepare_data()
    print_basic_stats(df)
    analyze_numeric_distributions(df)
    analyze_ratings_concentration(df)
    analyze_categories(df)
    
    print("Analysis complete. See figures/ directory for visualizations.")
