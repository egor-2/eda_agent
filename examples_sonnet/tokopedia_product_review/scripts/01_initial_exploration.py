import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')

# Convert review_date to datetime
df['review_date'] = pd.to_datetime(df['review_date'])

# Save basic statistics
with open('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/basic_stats.txt', 'w') as f:
    f.write("TOKOPEDIA PRODUCT REVIEWS - BASIC STATISTICS\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"Dataset shape: {df.shape[0]} reviews, {df.shape[1]} columns\n\n")
    
    f.write("Columns:\n")
    for col in df.columns:
        f.write(f"  - {col}: {df[col].dtype}\n")
    
    f.write("\n" + "=" * 60 + "\n")
    f.write("MISSING VALUES\n")
    f.write("=" * 60 + "\n")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    for col in df.columns:
        if missing[col] > 0:
            f.write(f"{col}: {missing[col]} ({missing_pct[col]:.2f}%)\n")
    
    f.write("\n" + "=" * 60 + "\n")
    f.write("UNIQUE VALUES COUNT\n")
    f.write("=" * 60 + "\n")
    for col in df.columns:
        if col not in ['review_text', 'product_url']:
            f.write(f"{col}: {df[col].nunique()}\n")
    
    f.write("\n" + "=" * 60 + "\n")
    f.write("DATE RANGE\n")
    f.write("=" * 60 + "\n")
    f.write(f"From: {df['review_date'].min()}\n")
    f.write(f"To: {df['review_date'].max()}\n")
    f.write(f"Range: {(df['review_date'].max() - df['review_date'].min()).days} days\n")
    
    f.write("\n" + "=" * 60 + "\n")
    f.write("DUPLICATE ROWS\n")
    f.write("=" * 60 + "\n")
    duplicates = df.duplicated().sum()
    f.write(f"Exact duplicate rows: {duplicates}\n")
    
    # Check for duplicate review_ids
    dup_ids = df['review_id'].duplicated().sum()
    f.write(f"Duplicate review_ids: {dup_ids}\n")

print("Basic statistics saved!")
