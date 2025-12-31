"""
Exploratory Data Analysis Script for Tokopedia Product Reviews Dataset
Author: Claude Opus 4.5
Date: 2025-12-31
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Setup
plt.style.use('seaborn-v0_8-whitegrid')
DATA_PATH = '/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv'
OUTPUT_DIR = '/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_opus/figures'

def load_and_preprocess_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv(DATA_PATH)
    df['review_date'] = pd.to_datetime(df['review_date'])
    df['review_length'] = df['review_text'].str.len()
    df['year'] = df['review_date'].dt.year
    return df

def generate_basic_statistics(df):
    """Print basic statistics about the dataset"""
    print("="*60)
    print("BASIC DATASET INFO")
    print("="*60)
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nDate range: {df['review_date'].min()} to {df['review_date'].max()}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"Duplicate review_ids: {df['review_id'].duplicated().sum()}")
    
def plot_rating_distribution(df, output_dir):
    """Plot rating distribution"""
    fig, ax = plt.subplots(figsize=(8, 5))
    rating_counts = df['rating'].value_counts().sort_index()
    bars = ax.bar(rating_counts.index, rating_counts.values, color='steelblue', edgecolor='black')
    ax.set_xlabel('Rating', fontsize=12)
    ax.set_ylabel('Number of Reviews', fontsize=12)
    ax.set_title('Distribution of Product Ratings', fontsize=14)
    ax.set_xticks([1, 2, 3, 4, 5])
    
    total = len(df)
    for bar, count in zip(bars, rating_counts.values):
        height = bar.get_height()
        ax.annotate(f'{count:,}\n({count/total*100:.1f}%)',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    ha='center', va='bottom', fontsize=10)
    ax.set_ylim(0, max(rating_counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_rating_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_sentiment_distribution(df, output_dir):
    """Plot sentiment distribution"""
    fig, ax = plt.subplots(figsize=(8, 5))
    sentiment_counts = df['sentiment_label'].value_counts()
    colors = {'positive': 'green', 'neutral': 'orange', 'negative': 'red'}
    bars = ax.bar(sentiment_counts.index, sentiment_counts.values, 
                  color=[colors[s] for s in sentiment_counts.index], edgecolor='black')
    ax.set_xlabel('Sentiment Label', fontsize=12)
    ax.set_ylabel('Number of Reviews', fontsize=12)
    ax.set_title('Distribution of Sentiment Labels', fontsize=14)
    
    total = len(df)
    for bar, count in zip(bars, sentiment_counts.values):
        height = bar.get_height()
        ax.annotate(f'{count:,}\n({count/total*100:.1f}%)',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    ha='center', va='bottom', fontsize=10)
    ax.set_ylim(0, max(sentiment_counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_sentiment_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_price_distribution(df, output_dir):
    """Plot price distribution with log transform"""
    fig, ax = plt.subplots(figsize=(10, 5))
    prices = df['product_price'][df['product_price'] > 0]
    log_prices = np.log10(prices)
    ax.hist(log_prices, bins=40, color='steelblue', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Product Price (IDR)', fontsize=12)
    ax.set_ylabel('Number of Products', fontsize=12)
    ax.set_title('Distribution of Product Prices (Log Scale)', fontsize=14)
    
    tick_locs = ax.get_xticks()
    tick_labels = [f'{10**x:,.0f}' if x >= 0 else '' for x in tick_locs]
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_price_distribution.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_wordclouds(df, output_dir):
    """Generate wordclouds by sentiment"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sentiments = ['positive', 'negative', 'neutral']
    for i, sentiment in enumerate(sentiments):
        ax = axes[i]
        text = ' '.join(df[df['sentiment_label'] == sentiment]['review_text'].astype(str))
        if len(text) > 0:
            wc = WordCloud(width=600, height=400, background_color='white', 
                          max_words=100, colormap='viridis' if sentiment == 'positive' else ('Reds' if sentiment == 'negative' else 'Oranges')).generate(text)
            ax.imshow(wc, interpolation='bilinear')
            ax.set_title(f'{sentiment.capitalize()} Reviews', fontsize=14)
        ax.axis('off')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/16_wordclouds_by_sentiment.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    df = load_and_preprocess_data()
    generate_basic_statistics(df)
    plot_rating_distribution(df, OUTPUT_DIR)
    plot_sentiment_distribution(df, OUTPUT_DIR)
    plot_price_distribution(df, OUTPUT_DIR)
    plot_wordclouds(df, OUTPUT_DIR)
    print("All plots generated successfully!")
