"""
Full analysis pipeline – robust datetime parsing.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, f_oneway
import statsmodels.api as sm
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# -------------------------------
# 1. Setup paths
# -------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUT_DIR = PROJECT_ROOT / 'outputs'
REPORT_DIR = PROJECT_ROOT / 'reports'

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# -------------------------------
# 2. Helper: find date column
# -------------------------------
def find_date_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

# -------------------------------
# 3. Load datasets
# -------------------------------
print("Loading data...")
fear_greed = pd.read_csv(DATA_DIR / 'fear_greed_index.csv')
trades = pd.read_csv(DATA_DIR / 'historical_data.csv')

print("Fear & Greed columns:", fear_greed.columns.tolist())
print("Trades columns:", trades.columns.tolist())

# -------------------------------
# 4. Preprocess Fear & Greed
# -------------------------------
# Date column: use 'date' or 'timestamp'
fg_date_col = find_date_column(fear_greed, ['date', 'Date', 'timestamp', 'Timestamp'])
if fg_date_col is None:
    raise KeyError("No date column found in fear_greed file.")

# Try parsing with dayfirst if needed (fear_greed dates likely YYYY-MM-DD)
fear_greed[fg_date_col] = pd.to_datetime(fear_greed[fg_date_col], errors='coerce')
if fear_greed[fg_date_col].isna().all():
    # If all failed, try dayfirst
    fear_greed[fg_date_col] = pd.to_datetime(fear_greed[fg_date_col], dayfirst=True, errors='coerce')
fear_greed['date_only'] = fear_greed[fg_date_col].dt.date

# Sentiment column: 'classification'
if 'classification' not in fear_greed.columns:
    raise KeyError("Sentiment column 'classification' not found.")
sentiment_map = {
    'Extreme Fear': 1,
    'Fear': 2,
    'Neutral': 3,
    'Greed': 4,
    'Extreme Greed': 5
}
fear_greed['sentiment_score'] = fear_greed['classification'].map(sentiment_map)
fear_greed.rename(columns={'classification': 'Classification'}, inplace=True)

# -------------------------------
# 5. Preprocess Trades
# -------------------------------
# Timestamp column: 'Timestamp IST' or 'Timestamp'
trade_time_col = find_date_column(trades, ['Timestamp IST', 'Timestamp', 'timestamp'])
if trade_time_col is None:
    raise KeyError("No timestamp column found in trades.")

# Convert with dayfirst=True because format is DD-MM-YYYY HH:MM
trades[trade_time_col] = pd.to_datetime(trades[trade_time_col], dayfirst=True, errors='coerce')
# Drop rows where timestamp couldn't be parsed
initial_len = len(trades)
trades = trades.dropna(subset=[trade_time_col])
if len(trades) < initial_len:
    print(f"Dropped {initial_len - len(trades)} rows due to invalid timestamps.")
trades['trade_date'] = trades[trade_time_col].dt.date

# PnL column: 'Closed PnL'
if 'Closed PnL' not in trades.columns:
    raise KeyError("Column 'Closed PnL' not found.")
trades['closedPnL'] = pd.to_numeric(trades['Closed PnL'], errors='coerce')
trades = trades.dropna(subset=['closedPnL'])

# Leverage: not directly present. If not found, set to 1.
leverage_col = None
for col in trades.columns:
    if 'leverage' in col.lower():
        leverage_col = col
        break
if leverage_col is None:
    print("Warning: No leverage column found. Setting leverage = 1 for all trades.")
    trades['leverage'] = 1
else:
    trades['leverage'] = pd.to_numeric(trades[leverage_col], errors='coerce')

# Side column: 'Side'
if 'Side' in trades.columns:
    trades['side'] = trades['Side']
else:
    trades['side'] = None

# Event column? Not present in list
if 'event' in trades.columns:
    trades['event'] = trades['event']
else:
    trades['event'] = None

# -------------------------------
# 6. Merge datasets
# -------------------------------
# Ensure fear_greed has unique dates for merging (take first if duplicates)
fear_greed_unique = fear_greed.drop_duplicates(subset=['date_only'])
merged = trades.merge(fear_greed_unique, left_on='trade_date', right_on='date_only', how='left')
merged = merged.dropna(subset=['Classification', 'closedPnL', 'leverage'])
merged['is_profitable'] = merged['closedPnL'] > 0

print(f"Merged dataset shape: {merged.shape}")
if len(merged) == 0:
    raise ValueError("No rows after merging. Check date alignment.")
print(f"Date range: {merged['trade_date'].min()} to {merged['trade_date'].max()}")

# -------------------------------
# 7. Feature engineering: sentiment momentum
# -------------------------------
# Daily sentiment series (use fg_date_col)
daily_sentiment = fear_greed_unique.set_index(fg_date_col)['sentiment_score']
daily_sentiment = daily_sentiment.resample('D').ffill()
daily_sentiment_change = daily_sentiment.diff(1)
daily_sentiment_change_3d = daily_sentiment.diff(3)

# Map to trade dates
merged['sentiment_change_1d'] = merged['trade_date'].map(daily_sentiment_change)
merged['sentiment_change_3d'] = merged['trade_date'].map(daily_sentiment_change_3d)

def trend_category(change):
    if pd.isna(change):
        return 'Stable'
    elif change > 0.5:
        return 'Increasing'
    elif change < -0.5:
        return 'Decreasing'
    else:
        return 'Stable'

merged['sentiment_trend'] = merged['sentiment_change_3d'].apply(trend_category)
merged['leverage_sentiment'] = merged['leverage'] * merged['sentiment_score']

# -------------------------------
# 8. Analysis & Visualizations
# -------------------------------
order = ['Extreme Fear','Fear','Neutral','Greed','Extreme Greed']

# 8.1 Trade count
plt.figure(figsize=(8,5))
sns.countplot(data=merged, x='Classification', order=order)
plt.title('Number of Trades by Market Sentiment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'trade_count_by_sentiment.png')
plt.close()

# 8.2 Win rate
win_rate = merged.groupby('Classification')['is_profitable'].mean() * 100
win_rate = win_rate.reindex(order)
plt.figure(figsize=(8,5))
win_rate.plot(kind='bar', color=['darkred','red','gray','green','darkgreen'])
plt.ylabel('Win Rate (%)')
plt.title('Trader Win Rate by Market Sentiment')
plt.ylim(0,100)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'win_rate_by_sentiment.png')
plt.close()

# 8.3 Average PnL
avg_pnl = merged.groupby('Classification')['closedPnL'].mean().reindex(order)
plt.figure(figsize=(8,5))
avg_pnl.plot(kind='bar', color='steelblue')
plt.ylabel('Average Closed PnL ($)')
plt.title('Average Profit/Loss per Trade by Sentiment')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'avg_pnl_by_sentiment.png')
plt.close()

# 8.4 Leverage distribution (if leverage varies)
if leverage_col is not None and merged['leverage'].nunique() > 1:
    plt.figure(figsize=(10,6))
    sns.boxplot(data=merged, x='Classification', y='leverage', order=order)
    plt.title('Leverage Distribution by Market Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'leverage_by_sentiment.png')
    plt.close()

# 8.5 Trade direction
if 'side' in merged.columns and merged['side'].notna().any():
    direction = pd.crosstab(merged['Classification'], merged['side'], normalize='index') * 100
    direction = direction.reindex(order)
    direction.plot(kind='bar', stacked=True, figsize=(8,5), colormap='coolwarm')
    plt.title('Trade Direction (Long/Short) by Sentiment')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(title='Side')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'trade_direction_by_sentiment.png')
    plt.close()

# 8.6 PnL by sentiment trend
pnl_by_trend = merged.groupby('sentiment_trend')['closedPnL'].mean()
plt.figure(figsize=(6,4))
pnl_by_trend.plot(kind='bar', color=['red','gray','green'])
plt.title('Average PnL by Sentiment Trend (3-day change)')
plt.ylabel('Avg PnL ($)')
plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'pnl_by_sentiment_trend.png')
plt.close()

# 8.7 Liquidation rate – skip if no event column
if 'event' in merged.columns and merged['event'].notna().any():
    merged['is_liquidation'] = merged['event'].str.lower() == 'liquidation'
    liq_rate = merged.groupby('Classification')['is_liquidation'].mean() * 100
    liq_rate = liq_rate.reindex(order)
    plt.figure(figsize=(8,5))
    liq_rate.plot(kind='bar', color='orange')
    plt.ylabel('Liquidation Rate (%)')
    plt.title('Liquidation Rate by Market Sentiment')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'liquidation_rate_by_sentiment.png')
    plt.close()

# -------------------------------
# 9. Statistical Tests
# -------------------------------
corr, p_val = pearsonr(merged['sentiment_score'], merged['closedPnL'])
print(f"\nPearson correlation (sentiment score vs PnL): r={corr:.3f}, p={p_val:.4f}")

# Regression with interaction (only if leverage varies)
if leverage_col is not None and merged['leverage'].nunique() > 1:
    X = merged[['leverage', 'sentiment_score', 'leverage_sentiment']]
    X = sm.add_constant(X)
    y = merged['closedPnL']
    model = sm.OLS(y, X, missing='drop').fit()
    print("\n=== Regression Summary ===")
    print(model.summary())
else:
    print("\nLeverage is constant (or missing) – skipping interaction regression.")
    model = None

# ANOVA for sentiment trend
groups = [merged[merged['sentiment_trend'] == cat]['closedPnL'].dropna() for cat in ['Decreasing', 'Stable', 'Increasing']]
f_stat, p_anova = f_oneway(*groups)
print(f"\nANOVA (PnL by sentiment trend): F={f_stat:.3f}, p={p_anova:.4f}")

# -------------------------------
# 10. Export cleaned data and reports
# -------------------------------
merged.to_csv(OUTPUT_DIR / 'cleaned_trading_data.csv', index=False)

with open(REPORT_DIR / 'statistics.txt', 'w') as f:
    f.write("===== TRADER PERFORMANCE VS SENTIMENT ANALYSIS =====\n\n")
    f.write("1. Win Rate by Sentiment (%)\n")
    for sent, rate in win_rate.items():
        f.write(f"   {sent}: {rate:.2f}%\n")
    f.write("\n2. Average PnL by Sentiment ($)\n")
    for sent, pnl in avg_pnl.items():
        f.write(f"   {sent}: {pnl:.2f}\n")
    f.write(f"\n3. Pearson correlation (sentiment score vs PnL): r={corr:.3f}, p={p_val:.4f}\n")
    if model is not None:
        f.write("\n4. OLS Regression Results:\n")
        f.write(model.summary().as_text())
    f.write(f"\n5. ANOVA (PnL by sentiment trend): F={f_stat:.3f}, p={p_anova:.4f}\n")

print("\nAnalysis complete! Results saved to 'outputs/' and 'reports/'.")