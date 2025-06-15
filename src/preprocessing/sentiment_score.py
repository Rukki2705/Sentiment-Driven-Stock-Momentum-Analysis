# src/processing/sentiment_score.py

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def compute_vader_sentiment(df, text_col='full_text'):
    analyzer = SentimentIntensityAnalyzer()
    df['vader_score'] = df[text_col].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    return df
