"""
Comprehensive EDA Script for Steam Games Dataset (2021-2025)
This script performs all analyses and generates all visualizations for the EDA report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
data_path = Path('/Users/yegorklochkov/repos/eda_agent/test/steam_games/a_steam_data_2021_2025.csv')
fig_path = Path('/Users/yegorklochkov/repos/eda_agent/test/steam_games/eda_sonnet/figures')

# Load data
print("Loading data...")
df = pd.read_csv(data_path)
print(f"Loaded {len(df)} games\n")

# ============================================================================
# FIGURE 1: Release Year Distribution
# ============================================================================
print("Creating Figure 1: Release Year Distribution...")
fig, ax = plt.subplots(figsize=(10, 6))
year_counts = df['release_year'].value_counts().sort_index()
ax.bar(year_counts.index, year_counts.values, color='steelblue', edgecolor='black')
ax.set_xlabel('Release Year', fontsize=12)
ax.set_ylabel('Number of Games', fontsize=12)
ax.set_title('Steam Games Release Distribution (2021-2025)', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(year_counts.values):
    ax.text(year_counts.index[i], v + 100, str(v), ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig(fig_path / '01_release_year_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 2: Price Distribution
# ============================================================================
print("Creating Figure 2: Price Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['price'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Price (USD)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Price Distribution (Original Scale)', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

prices_positive = df[df['price'] > 0]['price']
log_prices = np.log10(prices_positive)
counts, bins, patches = axes[1].hist(log_prices, bins=40, color='coral', edgecolor='black', alpha=0.7)
tick_locations = axes[1].get_xticks()
axes[1].set_xticklabels([f'{10**x:.1f}' if x >= 0 else '0' for x in tick_locations])
axes[1].set_xlabel('Price (USD)', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('Price Distribution (Log-Transformed Data, prices > 0)', fontsize=12, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '02_price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 3: Common Price Points
# ============================================================================
print("Creating Figure 3: Common Price Points...")
price_counts = df['price'].value_counts().head(15)
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(range(len(price_counts)), price_counts.values, color='steelblue', edgecolor='black')
ax.set_xticks(range(len(price_counts)))
ax.set_xticklabels([f'${x:.2f}' for x in price_counts.index], rotation=45, ha='right')
ax.set_xlabel('Price Point (USD)', fontsize=12)
ax.set_ylabel('Number of Games', fontsize=12)
ax.set_title('Top 15 Most Common Price Points', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(price_counts.values):
    ax.text(i, v + 50, str(v), ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig(fig_path / '03_common_price_points.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 4: Recommendations Distribution
# ============================================================================
print("Creating Figure 4: Recommendations Distribution...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['recommendations'], bins=50, color='green', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Recommendations', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].set_title('Recommendations Distribution (Original Scale)', fontsize=12, fontweight='bold')
axes[0].grid(axis='y', alpha=0.3)

recs_positive = df[df['recommendations'] > 0]['recommendations']
log_recs = np.log10(recs_positive)
counts, bins, patches = axes[1].hist(log_recs, bins=40, color='orange', edgecolor='black', alpha=0.7)
tick_vals = [0, 1, 10, 100, 1000, 10000, 100000, 1000000]
tick_locs = [np.log10(x) if x > 0 else 0 for x in tick_vals]
axes[1].set_xticks(tick_locs)
axes[1].set_xticklabels([str(x) for x in tick_vals], rotation=45)
axes[1].set_xlabel('Recommendations', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('Recommendations Distribution (Log-Transformed Data, recs > 0)', fontsize=12, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '04_recommendations_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 5: Top Genres
# ============================================================================
print("Creating Figure 5: Top Genres...")
genre_list = []
for genres in df['genres'].dropna():
    genre_list.extend(genres.split(';'))
genre_counts = Counter(genre_list)
top_genres = dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:15])

fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(list(top_genres.keys())[::-1], list(top_genres.values())[::-1], color='steelblue', edgecolor='black')
ax.set_xlabel('Number of Games', fontsize=12)
ax.set_ylabel('Genre', fontsize=12)
ax.set_title('Top 15 Most Common Genres', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(list(top_genres.values())[::-1]):
    ax.text(v + 200, i, str(v), ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(fig_path / '05_top_genres.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 6: Top Categories
# ============================================================================
print("Creating Figure 6: Top Categories...")
category_list = []
for categories in df['categories'].dropna():
    category_list.extend(categories.split(';'))
category_counts = Counter(category_list)
top_categories = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:15])

fig, ax = plt.subplots(figsize=(12, 7))
ax.barh(list(top_categories.keys())[::-1], list(top_categories.values())[::-1], color='coral', edgecolor='black')
ax.set_xlabel('Number of Games', fontsize=12)
ax.set_ylabel('Category', fontsize=12)
ax.set_title('Top 15 Most Common Categories', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, v in enumerate(list(top_categories.values())[::-1]):
    ax.text(v + 300, i, str(v), ha='left', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(fig_path / '06_top_categories.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 7: Price vs Recommendations Scatter
# ============================================================================
print("Creating Figure 7: Price vs Recommendations Scatter...")
fig, ax = plt.subplots(figsize=(10, 6))
df_filtered = df[(df['price'] > 0) & (df['recommendations'] > 0)]
ax.scatter(df_filtered['price'], df_filtered['recommendations'], alpha=0.3, s=20, color='purple')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Price (USD, log scale)', fontsize=12)
ax.set_ylabel('Recommendations (log scale)', fontsize=12)
ax.set_title('Price vs Recommendations (Both > 0)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, which='both')
plt.tight_layout()
plt.savefig(fig_path / '07_price_vs_recommendations_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 8: Recommendations by Price Boxplot
# ============================================================================
print("Creating Figure 8: Recommendations by Price Boxplot...")
df_with_recs = df[df['recommendations'] > 0].copy()
price_bins = [0, 0.99, 4.99, 9.99, 19.99, 49.99, 1000]
bin_labels = ['Free', '$0.99-4.99', '$5-9.99', '$10-19.99', '$20-49.99', '$50+']
df_with_recs['price_bin'] = pd.cut(df_with_recs['price'], bins=price_bins, labels=bin_labels, include_lowest=True)

fig, ax = plt.subplots(figsize=(12, 6))
df_with_recs.boxplot(column='recommendations', by='price_bin', ax=ax, patch_artist=True)
ax.set_yscale('log')
ax.set_xlabel('Price Range', fontsize=12)
ax.set_ylabel('Recommendations (log scale)', fontsize=12)
ax.set_title('Recommendations Distribution by Price Range', fontsize=14, fontweight='bold')
plt.suptitle('')
ax.grid(True, alpha=0.3, which='both')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(fig_path / '08_recommendations_by_price_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 9: Price and Recommendations by Year
# ============================================================================
print("Creating Figure 9: Price and Recommendations by Year...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

year_price_mean = df.groupby('release_year')['price'].mean()
year_price_median = df.groupby('release_year')['price'].median()

axes[0].plot(year_price_mean.index, year_price_mean.values, marker='o', linewidth=2, markersize=8, label='Mean', color='steelblue')
axes[0].plot(year_price_median.index, year_price_median.values, marker='s', linewidth=2, markersize=8, label='Median', color='coral')
axes[0].set_xlabel('Release Year', fontsize=12)
axes[0].set_ylabel('Price (USD)', fontsize=12)
axes[0].set_title('Average Price by Release Year', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

df_with_recs_year = df[df['recommendations'] > 0]
year_recs_mean = df_with_recs_year.groupby('release_year')['recommendations'].mean()
year_recs_median = df_with_recs_year.groupby('release_year')['recommendations'].median()

axes[1].plot(year_recs_mean.index, year_recs_mean.values, marker='o', linewidth=2, markersize=8, label='Mean', color='green')
axes[1].plot(year_recs_median.index, year_recs_median.values, marker='s', linewidth=2, markersize=8, label='Median', color='orange')
axes[1].set_xlabel('Release Year', fontsize=12)
axes[1].set_ylabel('Recommendations', fontsize=12)
axes[1].set_title('Average Recommendations by Release Year (recs > 0)', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '09_price_recommendations_by_year.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 10: Genre Statistics
# ============================================================================
print("Creating Figure 10: Genre Statistics...")
top_genre_names = ['Indie', 'Casual', 'Adventure', 'Action', 'Simulation', 'Strategy', 'RPG']
for genre in top_genre_names:
    df[f'is_{genre}'] = df['genres'].fillna('').str.contains(genre)

genre_stats = []
for genre in top_genre_names:
    genre_df = df[df[f'is_{genre}']]
    stats = {
        'Genre': genre,
        'Avg_Price': genre_df['price'].mean(),
        'Pct_With_Recommendations': (genre_df['recommendations'] > 0).sum() / len(genre_df) * 100
    }
    genre_stats.append(stats)

genre_stats_df = pd.DataFrame(genre_stats)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].barh(genre_stats_df['Genre'], genre_stats_df['Avg_Price'], color='steelblue', edgecolor='black')
axes[0].set_xlabel('Average Price (USD)', fontsize=12)
axes[0].set_ylabel('Genre', fontsize=12)
axes[0].set_title('Average Price by Genre', fontsize=12, fontweight='bold')
axes[0].grid(axis='x', alpha=0.3)

axes[1].barh(genre_stats_df['Genre'], genre_stats_df['Pct_With_Recommendations'], color='coral', edgecolor='black')
axes[1].set_xlabel('% of Games with Recommendations > 0', fontsize=12)
axes[1].set_ylabel('Genre', fontsize=12)
axes[1].set_title('Percentage of Games with Recommendations by Genre', fontsize=12, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '10_genre_statistics.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 11: Recommendations Concentration
# ============================================================================
print("Creating Figure 11: Recommendations Concentration...")
df_sorted = df.sort_values('recommendations', ascending=False).reset_index(drop=True)
df_sorted['cumulative_recommendations'] = df_sorted['recommendations'].cumsum()
total_recommendations = df_sorted['recommendations'].sum()
df_sorted['cumulative_pct'] = df_sorted['cumulative_recommendations'] / total_recommendations * 100

fig, ax = plt.subplots(figsize=(10, 6))
pct_to_show = 0.2
n_games_to_show = int(len(df_sorted) * pct_to_show)
x_values = np.arange(n_games_to_show) / len(df) * 100
ax.plot(x_values, df_sorted['cumulative_pct'][:n_games_to_show], linewidth=2, color='darkblue')
ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% of recommendations')
ax.axhline(y=80, color='orange', linestyle='--', alpha=0.5, label='80% of recommendations')
ax.set_xlabel('Percentage of Games (sorted by recommendations)', fontsize=12)
ax.set_ylabel('Cumulative % of Total Recommendations', fontsize=12)
ax.set_title('Concentration of Recommendations (Pareto Distribution)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(fig_path / '11_recommendations_concentration.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 12: Free vs Paid Comparison
# ============================================================================
print("Creating Figure 12: Free vs Paid Comparison...")
df['is_free'] = df['price'] == 0

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

df_with_recs_free = df[df['recommendations'] > 0].copy()
df_with_recs_free['Game_Type'] = df_with_recs_free['is_free'].map({True: 'Free', False: 'Paid'})

df_with_recs_free.boxplot(column='recommendations', by='Game_Type', ax=axes[0], patch_artist=True)
axes[0].set_yscale('log')
axes[0].set_xlabel('Game Type', fontsize=12)
axes[0].set_ylabel('Recommendations (log scale)', fontsize=12)
axes[0].set_title('Recommendations Distribution: Free vs Paid Games', fontsize=12, fontweight='bold')
plt.suptitle('')
axes[0].grid(True, alpha=0.3, which='both')

categories = ['Free', 'Paid']
pct_with_recs = [
    (df[df['is_free']]['recommendations'] > 0).sum() / df['is_free'].sum() * 100,
    (df[~df['is_free']]['recommendations'] > 0).sum() / (~df['is_free']).sum() * 100
]
axes[1].bar(categories, pct_with_recs, color=['coral', 'steelblue'], edgecolor='black')
axes[1].set_ylabel('% of Games with Recommendations > 0', fontsize=12)
axes[1].set_xlabel('Game Type', fontsize=12)
axes[1].set_title('Percentage of Games with Recommendations', fontsize=12, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)
for i, v in enumerate(pct_with_recs):
    axes[1].text(i, v + 0.5, f'{v:.2f}%', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(fig_path / '12_free_vs_paid_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 13: Developer Distribution
# ============================================================================
print("Creating Figure 13: Developer Distribution...")
dev_counts = df['developer'].value_counts()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

games_per_dev = dev_counts.values
axes[0].hist(games_per_dev, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Number of Games', fontsize=12)
axes[0].set_ylabel('Number of Developers', fontsize=12)
axes[0].set_title('Distribution of Games per Developer', fontsize=12, fontweight='bold')
axes[0].set_xlim(0, 50)
axes[0].grid(axis='y', alpha=0.3)

top_devs = dev_counts.head(15)
axes[1].barh(range(len(top_devs)), top_devs.values, color='coral', edgecolor='black')
axes[1].set_yticks(range(len(top_devs)))
axes[1].set_yticklabels([name[:30] + '...' if len(name) > 30 else name for name in top_devs.index], fontsize=9)
axes[1].set_xlabel('Number of Games', fontsize=12)
axes[1].set_ylabel('Developer', fontsize=12)
axes[1].set_title('Top 15 Developers by Game Count', fontsize=12, fontweight='bold')
axes[1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '13_developer_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 14: Genres/Categories vs Recommendations
# ============================================================================
print("Creating Figure 14: Genres/Categories vs Recommendations...")
df['num_genres'] = df['genres'].fillna('').apply(lambda x: len(x.split(';')) if x else 0)
df['num_categories'] = df['categories'].fillna('').apply(lambda x: len(x.split(';')) if x else 0)

df_with_recs_complex = df[df['recommendations'] > 0].copy()
genre_count_stats = df_with_recs_complex.groupby('num_genres')['recommendations'].agg(['mean', 'median', 'count'])
category_count_stats = df_with_recs_complex.groupby('num_categories')['recommendations'].agg(['mean', 'median', 'count'])

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].plot(genre_count_stats.index, genre_count_stats['mean'], marker='o', linewidth=2, markersize=8, label='Mean', color='steelblue')
axes[0].plot(genre_count_stats.index, genre_count_stats['median'], marker='s', linewidth=2, markersize=8, label='Median', color='coral')
axes[0].set_xlabel('Number of Genres', fontsize=12)
axes[0].set_ylabel('Recommendations', fontsize=12)
axes[0].set_title('Recommendations vs Number of Genres', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_yscale('log')

axes[1].plot(category_count_stats.index[:20], category_count_stats['mean'][:20], marker='o', linewidth=2, markersize=8, label='Mean', color='green')
axes[1].plot(category_count_stats.index[:20], category_count_stats['median'][:20], marker='s', linewidth=2, markersize=8, label='Median', color='orange')
axes[1].set_xlabel('Number of Categories', fontsize=12)
axes[1].set_ylabel('Recommendations', fontsize=12)
axes[1].set_title('Recommendations vs Number of Categories', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_yscale('log')

plt.tight_layout()
plt.savefig(fig_path / '14_genres_categories_vs_recommendations.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# FIGURE 15: Early Access Analysis
# ============================================================================
print("Creating Figure 15: Early Access Analysis...")
df['is_early_access'] = df['genres'].fillna('').str.contains('Early Access')
ea_games = df[df['is_early_access']]
non_ea_games = df[~df['is_early_access']]

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

price_data = [ea_games['price'], non_ea_games['price']]
bp1 = axes[0, 0].boxplot(price_data, tick_labels=['Early Access', 'Non-Early Access'], patch_artist=True)
axes[0, 0].set_ylabel('Price (USD)', fontsize=12)
axes[0, 0].set_title('Price Distribution: Early Access vs Non-Early Access', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)

ea_recs = ea_games[ea_games['recommendations'] > 0]['recommendations']
non_ea_recs = non_ea_games[non_ea_games['recommendations'] > 0]['recommendations']
recs_data = [ea_recs, non_ea_recs]
bp2 = axes[0, 1].boxplot(recs_data, tick_labels=['Early Access', 'Non-Early Access'], patch_artist=True)
axes[0, 1].set_yscale('log')
axes[0, 1].set_ylabel('Recommendations (log scale)', fontsize=12)
axes[0, 1].set_title('Recommendations: Early Access vs Non-Early Access (recs > 0)', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3, which='both')

ea_by_year = df[df['is_early_access']].groupby('release_year').size()
total_by_year = df.groupby('release_year').size()
ea_pct_by_year = (ea_by_year / total_by_year * 100)

axes[1, 0].bar(ea_pct_by_year.index, ea_pct_by_year.values, color='steelblue', edgecolor='black')
axes[1, 0].set_xlabel('Release Year', fontsize=12)
axes[1, 0].set_ylabel('% of Games in Early Access', fontsize=12)
axes[1, 0].set_title('Percentage of Early Access Games by Year', fontsize=12, fontweight='bold')
axes[1, 0].grid(axis='y', alpha=0.3)

axes[1, 1].bar(ea_by_year.index, ea_by_year.values, color='coral', edgecolor='black')
axes[1, 1].set_xlabel('Release Year', fontsize=12)
axes[1, 1].set_ylabel('Number of Early Access Games', fontsize=12)
axes[1, 1].set_title('Early Access Games Count by Year', fontsize=12, fontweight='bold')
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig(fig_path / '15_early_access_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*80)
print("All visualizations completed successfully!")
print("="*80)
print(f"\nFigures saved to: {fig_path}")
print("Total figures created: 15")
