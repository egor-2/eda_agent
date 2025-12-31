import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
df['Date'] = pd.to_datetime(df['Date'])

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['Daily_Return_Pct'], bins=100, edgecolor='black', alpha=0.7)
axes[0].set_xlabel('Daily Return (%)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Daily Returns')
axes[0].grid(True, alpha=0.3)
axes[0].axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.5)

stats.probplot(df['Daily_Return_Pct'], dist="norm", plot=axes[1])
axes[1].set_title('Q-Q Plot: Daily Returns vs Normal Distribution')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/eda_sonnet/figures/02_daily_return_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
