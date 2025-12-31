import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/books_across_100_cathegories/google_books_dataset.csv')

print("Dataset shape:", df.shape)
print("\nColumn names and types:")
print(df.dtypes)
print("\nFirst few rows:")
print(df.head(10))
print("\nBasic info:")
print(df.info())
print("\nSample of actual values to understand column types:")
for col in df.columns:
    print(f"\n{col}: {df[col].dropna().head(3).tolist()}")
