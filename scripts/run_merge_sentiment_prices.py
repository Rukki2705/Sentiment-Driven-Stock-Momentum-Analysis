import pandas as pd
from src.preprocessing.aggregate_sentiment import aggregate_daily_sentiment
from src.data_loader.fetch_prices import get_stock_prices
from datetime import timedelta
import os

# Configuration
tickers = ["QQQ", "SMH", "PLTR"]
sentiment_input = "data/reddit/reddit_sentiment.csv"
output_dir = "data/merged"
os.makedirs(output_dir, exist_ok=True)

# Load and aggregate sentiment
reddit_df = pd.read_csv(sentiment_input)
sentiment_df = aggregate_daily_sentiment(reddit_df)

# Loop through tickers
for ticker in tickers:
    print(f"\n📈 Processing ticker: {ticker}")
    
    # Determine stock price date range
    start_date = (pd.to_datetime(sentiment_df['date'].min()) - timedelta(days=3)).date().isoformat()
    end_date = (pd.to_datetime(sentiment_df['date'].max()) + timedelta(days=2)).date().isoformat()

    # Fetch stock price data
    price_df = get_stock_prices(ticker, start_date, end_date)
    
    if price_df.empty:
        print(f"⚠️ No price data for {ticker} — skipping.")
        continue

    # Merge with sentiment
    merged = pd.merge(sentiment_df, price_df, on='date', how='left')
    merged_clean = merged.dropna(subset=['avg_sentiment', 'return'])

    # Save
    out_path = os.path.join(output_dir, f"sentiment_price_{ticker}.csv")
    merged_clean.to_csv(out_path, index=False)
    print(f"✅ Saved {len(merged_clean)} merged records to {out_path}")
