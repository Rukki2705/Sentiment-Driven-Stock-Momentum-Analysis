# run_fetch_reddit.py

import os
from src.data_loader.fetch_reddit import init_reddit, fetch_recent_posts

if __name__ == "__main__":
    subreddits = [
    'stocks', 'wallstreetbets', 'StockMarket', 'pennystocks',
    'Superstonk', 'Options', 'TechStocks'
]

    reddit = init_reddit()
    df = fetch_recent_posts(
    reddit,
    subreddits,
    days=90,
    limit=1000,
    min_score=30,
    min_comments=10
)

    # Ensure directory exists
    output_dir = "data/reddit"
    os.makedirs(output_dir, exist_ok=True)

    # Save file
    output_path = os.path.join(output_dir, "reddit_posts.csv")
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df)} Reddit posts to {output_path}.")
