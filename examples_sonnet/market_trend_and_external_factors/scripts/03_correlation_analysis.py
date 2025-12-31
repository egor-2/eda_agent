import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
df['Date'] = pd.to_datetime(df['Date'])

sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100

numeric_cols = ['Open_Price', 'Close_Price', 'High_Price', 'Low_Price', 'Volume', 
                'Daily_Return_Pct', 'Volatility_Range', 'VIX_Close', 'Sentiment_Score',
                'GeoPolitical_Risk_Score', 'Currency_Index']

corr_matrix = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title('Correlation Matrix of Numeric Variables', fontsize=14, pad=20)
plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/eda_sonnet/figures/06_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
