# 📈 Reddit Sentiment-Driven Stock Momentum Analysis

This project analyzes Reddit-based sentiment signals to identify their predictive influence on stock price momentum. It performs correlation and causality testing on Reddit posts and historical stock returns, delivering insights through an interactive Streamlit dashboard with signal attribution and backtesting.

---

## 🧠 Project Overview

- **Goal**: Identify if Reddit sentiment leads stock movements using time series modeling, cross-correlation, and Granger causality.
- **Data Sources**:
  - Reddit posts from finance-related subreddits (`PRAW`)
  - Stock prices from Yahoo Finance (`yfinance`)
- **Assets Analyzed**: `QQQ`, `SMH`, and `PLTR`

---

## 🏗️ Features

- 🔄 **ETL Pipeline** to fetch and clean Reddit data
- 💬 **Sentiment Scoring** using VADER
- 📊 **Time Series Analysis**: Cross-correlation & Granger causality
- 🧪 **Backtestable Strategy Engine** with signal labeling
- 🧠 **Post Attribution** to explain buy/sell signals via Reddit posts
- 📈 **Interactive Streamlit Dashboard** for analysts and traders

---

## 📁 Project Structure
```
Sentiment Stock Analysis/
├── data/
│ ├── reddit/ # Raw and scored Reddit post data (CSV)
│ ├── merged/ # Sentiment + stock price merged time series
│ ├── backtests/ # Strategy backtest results (returns)
│ └── attributions/ # Reddit posts that contributed to signal days
│
├── reports/
│ ├── correlation/ # Cross-correlation PNG plots by ticker
│ └── granger_summary.csv # Granger p-values and best lag per ticker
│
├── scripts/
│ ├── run_fetch_reddit.py # Fetches Reddit posts using PRAW
│ ├── run_clean_score.py # Cleans, scores sentiment using VADER
│ ├── run_merge_sentiment_prices.py # Merges sentiment with stock returns
│ ├── run_analysis.py # Granger and cross-correlation analysis
│ └── generate_post_attributions.py # Maps signals to top Reddit posts
│
├── src/
│ ├── data_loader/
│ │ ├── fetch_reddit.py
│ │ └── fetch_prices.py
│ │
│ ├── preprocessing/
│ │ ├── clean_text.py
│ │ ├── sentiment_score.py
│ │ └── aggregate_sentiment.py
│ │
│ └── strategy/
│ ├── signal_generator.py # Label buy/sell based on sentiment
│ ├── backtester.py # Compare strategy vs market return
│ 
│
├── streamlit/
│ └── app.py # Streamlit dashboard for sentiment analysis
│
├── requirements.txt # Python dependencies
```
---
## ⚙️ How to Run

### 1. 🐍 Set up environment
```bash
python -m venv venv
source venv/bin/activate   # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```
### 2. 🔽 Fetch Reddit Posts
```bash
python scripts/run_fetch_reddit.py
```
### 🧼 Clean + Score Sentiment
```bash
python scripts/run_clean_score.py
```
### 4. 📈 Merge with Stock Prices
```bash
python scripts/run_merge_sentiment_prices.py
```
### 5. 📊 Run Time Series Analysis
```bash
python scripts/run_analysis.py
```
### 6. 🧪 Generate Post Attributions
```bash
python scripts/generate_post_attributions.py
```
### 7. 🚀 Launch Streamlit App
```bash
streamlit run streamlit/app.py
```
---
## 📸 Dashboard Features
- Ticker selector (QQQ, SMH, PLTR)
- Sentiment vs Adjusted Price over time
- Cross-correlation lag chart
- Granger causality p-values and best lag
- Strategy vs Market backtest panel
- Attributed Reddit posts behind signal days
---
## 🙌 Acknowledgements
- VADER Sentiment Analysis
- Reddit Dataset
- Yahoo Finance via yfinance
---

## 👤 Author

**Hrushikesh Attarde**  
[LinkedIn](https://www.linkedin.com/in/hrushikesh-attarde) · [GitHub](https://github.com/Rukki2705)
