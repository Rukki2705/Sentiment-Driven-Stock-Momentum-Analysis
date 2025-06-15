# src/processing/clean_text.py

import re
import pandas as pd

def clean_text(text):
    """
    Basic text cleaning: lowercasing, removing URLs, symbols, and extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)  # remove links
    text = re.sub(r"[^a-zA-Z0-9\s]", '', text)  # remove punctuation/special chars
    text = re.sub(r"\s+", ' ', text).strip()  # remove extra spaces
    return text

def prepare_text_columns(df):
    """
    Clean title and body, and create a merged text column.
    """
    df['title_clean'] = df['title'].apply(clean_text)
    df['text_clean'] = df['text'].apply(clean_text)
    df['full_text'] = (df['title_clean'] + " " + df['text_clean']).str.strip()
    return df
