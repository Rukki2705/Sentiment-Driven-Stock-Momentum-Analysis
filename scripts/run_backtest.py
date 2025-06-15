import pandas as pd
import os
from src.strategy.signal_generator import generate_signals
from src.strategy.backtester import apply_backtest

input_dir = "data/merged"
output_dir = "data/backtests"
os.makedirs(output_dir, exist_ok=True)

tickers = ["QQQ", "SMH", "PLTR"]

for ticker in tickers:
    file_path = os.path.join(input_dir, f"sentiment_price_{ticker}.csv")
    if not os.path.exists(file_path):
        print(f"❌ No data for {ticker}")
        continue

    df = pd.read_csv(file_path)
    df = generate_signals(df, sentiment_thresh=0.3)
    df = apply_backtest(df)

    out_path = os.path.join(output_dir, f"{ticker}_strategy.csv")
    df.to_csv(out_path, index=False)
    print(f"✅ Backtest complete: {out_path}")
