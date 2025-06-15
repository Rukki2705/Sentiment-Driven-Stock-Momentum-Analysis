import pandas as pd
import os

def get_top_reddit_posts(reddit_df: pd.DataFrame, signal_df: pd.DataFrame, top_n=1) -> pd.DataFrame:
    """
    For each day a signal is triggered, attach the top Reddit posts (by score × sentiment).
    """
    reddit_df = reddit_df.copy()
    reddit_df['created_utc'] = pd.to_datetime(reddit_df['created_utc'])
    reddit_df['date'] = reddit_df['created_utc'].dt.date

    signal_df = signal_df.copy()
    signal_df['date'] = pd.to_datetime(signal_df['date']).dt.date
    signal_days = signal_df[signal_df['signal'] != 0]['date'].unique()

    result = []
    for day in signal_days:
        posts_on_day = reddit_df[reddit_df['date'] == day].copy()
        if posts_on_day.empty:
            continue

        # Compute post ranking by score * sentiment
        posts_on_day['signal_strength'] = posts_on_day['vader_score'] * posts_on_day['score']
        top_posts = posts_on_day.sort_values(by='signal_strength', ascending=False).head(top_n)
        for _, row in top_posts.iterrows():
            result.append({
                'date': day,
                'title': row['title'],
                'score': row['score'],
                'vader_score': row['vader_score'],
                'signal_strength': row['signal_strength'],
                'subreddit': row.get('subreddit', None),
                'permalink': row.get('permalink', None)
            })

    return pd.DataFrame(result)


if __name__ == "__main__":
    reddit_df = pd.read_csv("data/reddit/reddit_sentiment.csv")
    backtest_dir = "data/backtests"
    output_dir = "data/attributions"
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(backtest_dir):
        if file.endswith("_strategy.csv"):
            ticker = file.replace("_strategy.csv", "")
            signal_df = pd.read_csv(os.path.join(backtest_dir, file))
            top_posts = get_top_reddit_posts(reddit_df, signal_df, top_n=1)
            out_path = os.path.join(output_dir, f"{ticker}_attributed_posts.csv")
            top_posts.to_csv(out_path, index=False)
            print(f"✅ Saved {len(top_posts)} top posts for {ticker} to {out_path}")
