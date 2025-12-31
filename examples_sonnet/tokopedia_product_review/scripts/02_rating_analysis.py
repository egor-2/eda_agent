import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/tokopedia_product_reviews_2025.csv')
df['review_date'] = pd.to_datetime(df['review_date'])

# Rating distribution
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Rating distribution bar plot
rating_counts = df['rating'].value_counts().sort_index()
axes[0, 0].bar(rating_counts.index, rating_counts.values, color='steelblue', edgecolor='black')
axes[0, 0].set_xlabel('Rating', fontsize=11)
axes[0, 0].set_ylabel('Count', fontsize=11)
axes[0, 0].set_title('Distribution of Ratings', fontsize=12, fontweight='bold')
axes[0, 0].grid(axis='y', alpha=0.3)
for i, (rating, count) in enumerate(rating_counts.items()):
    pct = count / len(df) * 100
    axes[0, 0].text(rating, count, f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

# 2. Sentiment distribution
sentiment_counts = df['sentiment_label'].value_counts()
axes[0, 1].bar(sentiment_counts.index, sentiment_counts.values, 
               color=['green', 'gray', 'red'], edgecolor='black')
axes[0, 1].set_xlabel('Sentiment', fontsize=11)
axes[0, 1].set_ylabel('Count', fontsize=11)
axes[0, 1].set_title('Distribution of Sentiment Labels', fontsize=12, fontweight='bold')
axes[0, 1].grid(axis='y', alpha=0.3)
for i, (sent, count) in enumerate(sentiment_counts.items()):
    pct = count / len(df) * 100
    axes[0, 1].text(i, count, f'{count}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9)

# 3. Rating vs Sentiment
rating_sentiment = pd.crosstab(df['rating'], df['sentiment_label'], normalize='index') * 100
rating_sentiment.plot(kind='bar', stacked=True, ax=axes[1, 0], 
                      color=['green', 'gray', 'red'])
axes[1, 0].set_xlabel('Rating', fontsize=11)
axes[1, 0].set_ylabel('Percentage', fontsize=11)
axes[1, 0].set_title('Sentiment Distribution by Rating', fontsize=12, fontweight='bold')
axes[1, 0].legend(title='Sentiment', bbox_to_anchor=(1.05, 1), loc='upper left')
axes[1, 0].grid(axis='y', alpha=0.3)
axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=0)

# 4. Rating statistics by sentiment
sentiment_stats = df.groupby('sentiment_label')['rating'].agg(['mean', 'median', 'count'])
axes[1, 1].axis('off')
table_data = []
for sent in sentiment_stats.index:
    table_data.append([
        sent,
        f"{sentiment_stats.loc[sent, 'mean']:.2f}",
        f"{sentiment_stats.loc[sent, 'median']:.0f}",
        f"{sentiment_stats.loc[sent, 'count']:.0f}"
    ])
table = axes[1, 1].table(cellText=table_data,
                         colLabels=['Sentiment', 'Mean Rating', 'Median Rating', 'Count'],
                         cellLoc='center',
                         loc='center',
                         bbox=[0, 0.3, 1, 0.5])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
axes[1, 1].set_title('Rating Statistics by Sentiment', fontsize=12, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/yegorklochkov/repos/eda_agent/test/tokopedia_product_review/eda_sonnet/figures/01_rating_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print("Rating analysis completed!")
