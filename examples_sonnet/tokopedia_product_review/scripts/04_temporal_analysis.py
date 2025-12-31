import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# 1. Reviews over time (monthly aggregation)
df_sorted = df.sort_values('review_date')
df_sorted['year_month'] = df_sorted['review_date'].dt.to_period('M')
monthly_counts = df_sorted.groupby('year_month').size()
monthly_dates = [period.to_timestamp() for period in monthly_counts.index]

axes[0].plot(monthly_dates, monthly_counts.values, linewidth=1.5, color='steelblue')
axes[0].fill_between(monthly_dates, monthly_counts.values, alpha=0.3, color='steelblue')
axes[0].set_xlabel('Date', fontsize=11)
axes[0].set_ylabel('Number of Reviews', fontsize=11)
axes[0].set_title('Review Volume Over Time (Monthly)', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# 2. Cumulative reviews over time
cumsum = monthly_counts.cumsum()
axes[1].plot(monthly_dates, cumsum.values, linewidth=2, color='darkgreen')
axes[1].set_xlabel('Date', fontsize=11)
axes[1].set_ylabel('Cumulative Review Count', fontsize=11)
axes[1].set_title('Cumulative Reviews Over Time', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

# 3. Average rating over time
monthly_rating = df_sorted.groupby('year_month')['rating'].mean()
monthly_rating_dates = [period.to_timestamp() for period in monthly_rating.index]

axes[2].plot(monthly_rating_dates, monthly_rating.values, linewidth=1.5, color='coral', marker='o', markersize=2)
axes[2].axhline(y=df['rating'].mean(), color='red', linestyle='--', linewidth=1, label=f'Overall mean: {df["rating"].mean():.2f}')
axes[2].set_xlabel('Date', fontsize=11)
axes[2].set_ylabel('Average Rating', fontsize=11)
axes[2].set_title('Average Rating Over Time (Monthly)', fontsize=12, fontweight='bold')
axes[2].set_ylim([0, 5.5])
axes[2].grid(True, alpha=0.3)
axes[2].legend()

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/03_temporal_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Temporal analysis completed!")
