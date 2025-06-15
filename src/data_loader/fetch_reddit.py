# src/data_loader/fetch_reddit.py

import praw
import pandas as pd
from datetime import datetime, timedelta

def init_reddit():
    return praw.Reddit(
        client_id="FP95WJXPIAmtkNkxDxRxrw",
        client_secret="LnLuhXyVs-vKrf5Xdvy4wHLCMe4I6Q",
        user_agent="East_Employee_8969"
    )

def fetch_recent_posts(reddit, subreddits, days=2, limit=500, min_score=30, min_comments=10):
    """
    Fetch recent Reddit posts with filtering based on score and comment count.
    """
    posts = []
    since = datetime.utcnow() - timedelta(days=days)

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        count = 0  # Track how many valid posts per sub
        for submission in subreddit.new(limit=limit):
            created = datetime.utcfromtimestamp(submission.created_utc)

            if (
                created >= since
                and submission.score >= min_score
                and submission.num_comments >= min_comments
            ):
                posts.append({
                    'subreddit': sub,
                    'title': submission.title,
                    'text': submission.selftext,
                    'created_utc': created,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'permalink': submission.permalink
                })
                count += 1
        print(f"[{sub}] → {count} posts collected")

    df = pd.DataFrame(posts)
    df['created_utc'] = pd.to_datetime(df['created_utc'])
    return df
