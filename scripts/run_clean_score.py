# run_clean_score.py

import pandas as pd
import os
from src.preprocessing.clean_text import prepare_text_columns
from src.preprocessing.sentiment_score import compute_vader_sentiment

input_file = "data/reddit/reddit_posts.csv"
output_file = "data/reddit/reddit_sentiment.csv"

# Ensure input exists
if not os.path.exists(input_file):
    raise FileNotFoundError(f"{input_file} not found.")

# Load
df = pd.read_csv(input_file)
original_count = len(df)

# Optional: drop duplicates (title + text)
df.drop_duplicates(subset=['title', 'text'], inplace=True)

# Clean text
df = prepare_text_columns(df)

# Remove empty or whitespace-only posts
df = df[df['full_text'].str.strip().astype(bool)]
after_clean_count = len(df)

# Apply sentiment scoring
df = compute_vader_sentiment(df)

# Sort chronologically
df = df.sort_values(by='created_utc')

# Save
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)

print(f"Original posts: {original_count}")
print(f"After cleaning and filtering: {after_clean_count}")
print(f"Saved to {output_file}")
