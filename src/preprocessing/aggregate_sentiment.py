import pandas as pd

def aggregate_daily_sentiment(df, timestamp_col='created_utc', sentiment_col='vader_score'):
    """
    Groups sentiment by date (UTC) and computes mean sentiment score.
    """
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df['date'] = df[timestamp_col].dt.date
    daily_sentiment = df.groupby('date')[sentiment_col].mean().reset_index()
    daily_sentiment.columns = ['date', 'avg_sentiment']
    return daily_sentiment
