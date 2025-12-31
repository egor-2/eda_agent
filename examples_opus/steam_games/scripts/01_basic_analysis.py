"""
Basic exploratory data analysis of Steam Games dataset (2021-2025)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/steam_games/a_steam_data_2021_2025.csv')

# Basic info
print("=== Dataset Overview ===")
print(f"Shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nNull counts:\n{df.isnull().sum()}")

# Release year distribution
print("\n=== Release Year Distribution ===")
print(df['release_year'].value_counts().sort_index())

# Price statistics
print("\n=== Price Statistics ===")
print(df['price'].describe())

# Recommendations statistics
print("\n=== Recommendations Statistics ===")
print(df['recommendations'].describe())
print(f"\nGames with 0 recommendations: {(df['recommendations'] == 0).sum()}")
print(f"Games with 101+ recommendations: {(df['recommendations'] > 0).sum()}")
print(f"Min non-zero recommendations: {df[df['recommendations'] > 0]['recommendations'].min()}")

# Genre analysis
print("\n=== Top Genres ===")
all_genres = df['genres'].dropna().str.split(';').explode()
print(all_genres.value_counts().head(15))

# Duplicates check
print("\n=== Duplicate Check ===")
print(f"Total rows: {len(df)}")
print(f"Unique appids: {df['appid'].nunique()}")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
