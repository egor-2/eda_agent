import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

# 1. Price distributions
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Open Price
axes[0, 0].hist(df['Open_Price'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 0].set_xlabel('Open Price')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Distribution of Open Price')
axes[0, 0].grid(True, alpha=0.3)

# Close Price
axes[0, 1].hist(df['Close_Price'], bins=50, edgecolor='black', alpha=0.7)
axes[0, 1].set_xlabel('Close Price')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Distribution of Close Price')
axes[0, 1].grid(True, alpha=0.3)

# High Price
axes[1, 0].hist(df['High_Price'], bins=50, edgecolor='black', alpha=0.7)
axes[1, 0].set_xlabel('High Price')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Distribution of High Price')
axes[1, 0].grid(True, alpha=0.3)

# Low Price
axes[1, 1].hist(df['Low_Price'], bins=50, edgecolor='black', alpha=0.7)
axes[1, 1].set_xlabel('Low Price')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Distribution of Low Price')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/eda_sonnet/figures/01_price_distributions.png', dpi=300, bbox_inches='tight')
plt.close()

print("Created: 01_price_distributions.png")
