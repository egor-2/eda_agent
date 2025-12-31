# Steam Games EDA Results (2021-2025)

This folder contains the complete Exploratory Data Analysis (EDA) of the Steam games dataset.

## Contents

### Main Report
- **EDA_Report.md** - Comprehensive markdown report with all findings, statistics, and interpretations

### Folders
- **figures/** - All 15 visualization plots referenced in the report
- **scripts/** - Python scripts used to generate the analysis

## Key Findings Summary

1. **Dataset**: 65,521 Steam games released from 2021-2025
2. **Growth**: Game releases increased 140% from 2021 to 2025
3. **Engagement**: 87.78% of games have zero user recommendations
4. **Concentration**: Top 1% of games capture 79.74% of all recommendations
5. **Pricing**: 85.76% of games use round price points ($X.99 or $X.00)
6. **Free-to-Play**: 18.26% of games are free, but only 0.72% receive recommendations
7. **Genres**: 70% of games are tagged as "Indie"
8. **Developers**: 82.55% of developers have released only one game

## How to Reproduce

Run the complete analysis:
```bash
cd /Users/yegorklochkov/repos/eda_agent/test/steam_games/eda_sonnet/scripts
source ~/ml_env/bin/activate
python full_analysis.py
```

This will regenerate all 15 figures in the `figures/` directory.

## Visualization Index

1. Release Year Distribution
2. Price Distribution
3. Common Price Points
4. Recommendations Distribution
5. Top Genres
6. Top Categories
7. Price vs Recommendations Scatter
8. Recommendations by Price Boxplot
9. Price and Recommendations by Year
10. Genre Statistics
11. Recommendations Concentration (Pareto)
12. Free vs Paid Comparison
13. Developer Distribution
14. Genres/Categories vs Recommendations
15. Early Access Analysis

## Technical Details

- **Python**: 3.13.5
- **Libraries**: pandas, numpy, matplotlib, seaborn
- **Dataset**: a_steam_data_2021_2025.csv (11 MB)
- **Generated**: 2025-12-31
- **Agent**: Claude Sonnet 4.5
