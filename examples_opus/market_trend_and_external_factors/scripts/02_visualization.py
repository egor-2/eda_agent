"""
Visualization script for Market Trend and External Factors dataset.
Generates all figures for the EDA report.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

plt.style.use('seaborn-v0_8-whitegrid')

def load_data():
    df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/Market_Trend_External.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def plot_price_timeseries(df, output_dir):
    """Figure 1: Price and volume time series"""
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    axes[0].plot(df['Date'], df['Close_Price'], linewidth=0.5, alpha=0.8)
    axes[0].set_title('Close Price Over Time (1902-2017)', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Close Price')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(df['Date'], df['Volume'], linewidth=0.5, alpha=0.8, color='green')
    axes[1].set_title('Trading Volume Over Time', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel('Volume')
    axes[1].grid(True, alpha=0.3)
    axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_price_volume_timeseries.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_distributions(df, output_dir):
    """Figure 2-4: Various distributions"""
    # Price distributions
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0,0].hist(df['Close_Price'], bins=50, edgecolor='black', alpha=0.7)
    axes[0,0].set_title('Distribution of Close Price', fontsize=11, fontweight='bold')
    axes[0,0].set_xlabel('Close Price')
    axes[0,0].set_ylabel('Frequency')
    
    log_volume = np.log10(df['Volume'])
    axes[0,1].hist(log_volume, bins=50, edgecolor='black', alpha=0.7, color='green')
    axes[0,1].set_title('Distribution of Volume (Log Scale)', fontsize=11, fontweight='bold')
    axes[0,1].set_xlabel('Log10(Volume)')
    axes[0,1].set_ylabel('Frequency')
    
    axes[1,0].hist(df['VIX_Close'], bins=40, edgecolor='black', alpha=0.7, color='orange')
    axes[1,0].set_title('Distribution of VIX Close', fontsize=11, fontweight='bold')
    axes[1,0].set_xlabel('VIX Close')
    axes[1,0].set_ylabel('Frequency')
    
    axes[1,1].hist(df['Currency_Index'], bins=40, edgecolor='black', alpha=0.7, color='purple')
    axes[1,1].set_title('Distribution of Currency Index', fontsize=11, fontweight='bold')
    axes[1,1].set_xlabel('Currency Index')
    axes[1,1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_price_distributions.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_correlation_heatmap(df, output_dir):
    """Figure 5: Correlation heatmap"""
    numeric_cols = ['Open_Price', 'Close_Price', 'High_Price', 'Low_Price', 'Volume', 
                    'Daily_Return_Pct', 'Volatility_Range', 'VIX_Close', 
                    'Sentiment_Score', 'GeoPolitical_Risk_Score', 'Currency_Index']
    
    fig, ax = plt.subplots(figsize=(12, 10))
    corr_matrix = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
                center=0, vmin=-1, vmax=1, ax=ax, square=True)
    ax.set_title('Correlation Matrix', fontsize=12, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.close()

def main():
    output_dir = '/Users/yegorklochkov/repos/eda_agent/test/market_trend_and_external_factors/eda_opus/figures'
    df = load_data()
    
    plot_price_timeseries(df, output_dir)
    plot_distributions(df, output_dir)
    plot_correlation_heatmap(df, output_dir)
    
    print("All figures generated.")

if __name__ == "__main__":
    main()
