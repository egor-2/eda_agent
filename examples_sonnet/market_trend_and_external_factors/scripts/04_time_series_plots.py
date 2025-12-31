import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
df['Date'] = pd.to_datetime(df['Date'])

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

fig, axes = plt.subplots(3, 1, figsize=(16, 12))

axes[0].plot(df['Date'], df['Close_Price'], linewidth=0.5, alpha=0.7)
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Close Price')
axes[0].set_title('Close Price Over Time')
axes[0].grid(True, alpha=0.3)

axes[1].plot(df['Date'], df['Volume'], linewidth=0.5, alpha=0.7)
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Volume')
axes[1].set_title('Trading Volume Over Time')
axes[1].grid(True, alpha=0.3)

axes[2].plot(df['Date'], df['Daily_Return_Pct'], linewidth=0.5, alpha=0.7)
axes[2].axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[2].set_xlabel('Date')
axes[2].set_ylabel('Daily Return (%)')
axes[2].set_title('Daily Returns Over Time')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/eda_sonnet/figures/05_time_series.png', dpi=300, bbox_inches='tight')
plt.close()
