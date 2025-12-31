import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Paths
data_path = Path('/Users/yegorklochkov/repos/eda_agent/test/steam_games/a_steam_data_2021_2025.csv')
fig_path = Path('/Users/yegorklochkov/repos/eda_agent/test/steam_games/eda_sonnet/figures')

# Load data
print("Loading data...")
df = pd.read_csv(data_path)

print(f"Dataset shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nBasic statistics:\n{df.describe()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nMissing values percentage:\n{df.isnull().sum() / len(df) * 100}")

# Check for duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")
print(f"Duplicate appids: {df['appid'].duplicated().sum()}")

# Save summary
with open(fig_path.parent / 'data_summary.txt', 'w') as f:
    f.write(f"Dataset shape: {df.shape}\n\n")
    f.write(f"Column dtypes:\n{df.dtypes}\n\n")
    f.write(f"Missing values:\n{df.isnull().sum()}\n\n")
    f.write(f"Missing values percentage:\n{df.isnull().sum() / len(df) * 100}\n\n")
    f.write(f"Duplicate rows: {df.duplicated().sum()}\n")
    f.write(f"Duplicate appids: {df['appid'].duplicated().sum()}\n")

print("\nInitial exploration completed!")
