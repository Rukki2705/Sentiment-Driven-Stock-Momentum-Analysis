import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import ast
from src.strategy.signal_generator import generate_signals
from src.strategy.backtester import apply_backtest
from scripts.generate_post_attributions import get_top_reddit_posts

st.set_page_config(page_title="Reddit Sentiment vs Stock Returns", layout="wide")
st.title("\U0001F4C8 Reddit Sentiment Momentum Analysis")

# --- Load summary and available tickers ---
summary_path = "reports/granger_summary.csv"
data_dir = "data/merged"
reddit_data_path = "data/reddit/reddit_sentiment.csv"

@st.cache_data
def load_summary():
    if os.path.exists(summary_path):
        return pd.read_csv(summary_path)
    return pd.DataFrame()

@st.cache_data
def load_merged_data(ticker):
    file_path = os.path.join(data_dir, f"sentiment_price_{ticker}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

@st.cache_data
def load_reddit_data():
    if os.path.exists(reddit_data_path):
        return pd.read_csv(reddit_data_path)
    return pd.DataFrame()

# --- Sidebar: ticker selection ---
st.sidebar.header("\u2699\ufe0f Settings")
ticker_options = [f.replace("sentiment_price_", "").replace(".csv", "") for f in os.listdir(data_dir) if f.endswith(".csv")]
ticker = st.sidebar.selectbox("Select a Ticker", sorted(ticker_options))
threshold = st.sidebar.slider("Sentiment Threshold", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
top_n = st.sidebar.slider("Top Reddit Posts per Signal Day", min_value=1, max_value=5, value=1, step=1)

# --- Load Data ---
df = load_merged_data(ticker)
summary_df = load_summary()
reddit_df = load_reddit_data()

if df.empty:
    st.warning(f"No data found for {ticker}.")
    st.stop()

# --- Line Plot: Sentiment vs Price ---
st.subheader(f"\U0001F4CA Sentiment vs Adjusted Close Price: {ticker}")
fig, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(pd.to_datetime(df['date']), df['avg_sentiment'], color='tab:blue', label='Sentiment')
ax1.set_ylabel('Sentiment', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.plot(pd.to_datetime(df['date']), df['Adj Close'], color='tab:gray', label='Price')
ax2.set_ylabel('Adj Close Price', color='tab:gray')
ax2.tick_params(axis='y', labelcolor='tab:gray')

fig.tight_layout()
st.pyplot(fig)

# --- Show pre-generated cross-correlation chart ---
st.subheader(f"\U0001F501 Cross-Correlation Lag Analysis")
img_path = f"reports/correlation/cross_correlation_{ticker}.png"
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)
else:
    st.info("No correlation chart available. Run analysis script to generate it.")

# --- Show Granger Results ---
st.subheader("\U0001F52C Granger Causality Results")
if not summary_df.empty:
    granger_row = summary_df[summary_df['ticker'] == ticker].iloc[0].copy()

    st.markdown(f"**Best Lag:** {granger_row['best_lag']}")
    st.markdown(f"**Best p-value:** {granger_row['best_p_value']:.4f}")

    st.markdown("**All p-values:**")
    all_p_values = ast.literal_eval(granger_row['all_p_values'])
    pval_df = pd.DataFrame(list(all_p_values.items()), columns=['Lag', 'p-value'])
    st.dataframe(pval_df, use_container_width=True)

    st.markdown("**Cross-Correlation Coefficients:**")
    correlations = ast.literal_eval(granger_row['cross_correlation'])
    corr_df = pd.DataFrame({'Lag': list(range(len(correlations))), 'Correlation': correlations})
    st.dataframe(corr_df, use_container_width=True)
else:
    st.info("No Granger summary found. Run run_analysis_multi.py to generate.")

# --- Comparison Section ---
st.subheader("\U0001F4CB Ticker Ranking by Granger Predictiveness")
if not summary_df.empty:
    st.dataframe(summary_df[['ticker', 'best_lag', 'best_p_value']].sort_values(by='best_p_value'), use_container_width=True)

# --- Strategy Backtest Panel ---
st.subheader("\U0001F4C8 Strategy Backtest vs Market (Live Computed)")
df_bt = generate_signals(df.copy(), sentiment_thresh=threshold)
df_bt = apply_backtest(df_bt)

fig_bt, ax_bt = plt.subplots(figsize=(10, 4))
ax_bt.plot(pd.to_datetime(df_bt['date']), df_bt['cumulative_strategy_return'], label="Strategy", color="green")
ax_bt.plot(pd.to_datetime(df_bt['date']), df_bt['cumulative_market_return'], label="Market", color="black", linestyle="--")
ax_bt.set_ylabel("Cumulative Return")
ax_bt.set_xlabel("Date")
ax_bt.legend()
ax_bt.set_title(f"Strategy vs Market Returns: {ticker} (Threshold: {threshold})")
st.pyplot(fig_bt)

# --- Show performance metrics ---
st.markdown("### \U0001F4CA Backtest Metrics")
strat_return = df_bt['cumulative_strategy_return'].iloc[-1] - 1
market_return = df_bt['cumulative_market_return'].iloc[-1] - 1
strat_vol = df_bt['strategy_return'].std() * (252 ** 0.5)
sharpe = (df_bt['strategy_return'].mean() / strat_vol) * (252 ** 0.5) if strat_vol > 0 else 0

metrics_df = pd.DataFrame({
    "Metric": ["Strategy Return", "Market Return", "Sharpe Ratio"],
    ticker: [f"{strat_return:.2%}", f"{market_return:.2%}", f"{sharpe:.2f}"]
})
st.dataframe(metrics_df, use_container_width=True)

# --- Attributed Reddit Posts ---
st.markdown("### \U0001F4DD Attributed Reddit Posts Driving Signals")
post_df = get_top_reddit_posts(reddit_df, df_bt, top_n=top_n)
if not post_df.empty:
    st.dataframe(post_df[['date', 'subreddit', 'title', 'score', 'vader_score', 'signal_strength']], use_container_width=True)
else:
    st.info("No attributed posts found for this strategy.")
