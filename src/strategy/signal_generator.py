import pandas as pd

def generate_signals(df, sentiment_thresh=0.3):
    """
    Generate signals:
    1 if sentiment > threshold, else 0.
    """
    df = df.copy()
    df['signal'] = (df['avg_sentiment'] > sentiment_thresh).astype(int)
    return df
