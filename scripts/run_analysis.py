import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import json
from statsmodels.tsa.stattools import grangercausalitytests

# Configuration
merged_dir = "data/merged"
tickers = ["QQQ", "SMH", "PLTR"]
max_lag = 3

results = []

def plot_cross_correlation(sentiment, returns, ticker, max_lag=5):
    sentiment = (sentiment - np.mean(sentiment)) / np.std(sentiment)
    returns = (returns - np.mean(returns)) / np.std(returns)

    corr = [np.corrcoef(sentiment[:-lag or None], returns[lag:])[0, 1] for lag in range(max_lag + 1)]

    plt.figure(figsize=(6, 3))
    plt.bar(range(max_lag + 1), corr)
    plt.title(f"Cross-Correlation: {ticker}")
    plt.xlabel("Lag (days)")
    plt.ylabel("Correlation")
    plt.xticks(range(max_lag + 1))
    plt.grid(True)
    plt.tight_layout()

    os.makedirs("reports/correlation", exist_ok=True)
    plt.savefig(f"reports/correlation/cross_correlation_{ticker}.png")
    plt.close()
    return corr

def run_granger(df, maxlag=3):
    df_test = df[['return', 'avg_sentiment']].dropna()
    result = grangercausalitytests(df_test, maxlag=maxlag, verbose=False)
    p_values = {int(lag): round(result[lag][0]['ssr_ftest'][1], 4) for lag in result}
    return p_values

# Loop through each ticker
for ticker in tickers:
    file_path = os.path.join(merged_dir, f"sentiment_price_{ticker}.csv")
    if not os.path.exists(file_path):
        print(f"❌ Missing data for {ticker}")
        continue

    df = pd.read_csv(file_path)
    if len(df) < max_lag + 5:
        print(f"⚠️ Not enough data for {ticker} (only {len(df)} records)")
        continue

    print(f"\n📈 Analyzing {ticker}...")

    # Cross-Correlation
    correlations = plot_cross_correlation(df['avg_sentiment'], df['return'], ticker, max_lag=5)

    # Granger Test
    granger_p = run_granger(df, maxlag=max_lag)

    # Save summary
    best_lag = min(granger_p, key=granger_p.get)
    results.append({
        "ticker": ticker,
        "best_lag": best_lag,
        "best_p_value": granger_p[best_lag],
        "all_p_values": json.dumps(granger_p),                    # ✅ cleaned to JSON
        "cross_correlation": json.dumps([float(c) for c in correlations])  # ✅ converted np.float64 to float
    })

# Summary Report
summary_df = pd.DataFrame(results).sort_values(by="best_p_value")
summary_path = "reports/granger_summary.csv"
os.makedirs("reports", exist_ok=True)
summary_df.to_csv(summary_path, index=False)

print(f"\n📊 Granger test summary saved to {summary_path}")
print(summary_df[['ticker', 'best_lag', 'best_p_value']])

