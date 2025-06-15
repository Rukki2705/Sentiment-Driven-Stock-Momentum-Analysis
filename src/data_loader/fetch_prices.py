import yfinance as yf
import pandas as pd

def get_stock_prices(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date, group_by="ticker", auto_adjust=False)

    # If multi-index (due to group_by), flatten it
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[1] for col in data.columns]

    data = data[['Adj Close']].copy()
    data['return'] = data['Adj Close'].pct_change()
    data = data.reset_index()
    data['date'] = data['Date'].dt.date

    return data[['date', 'Adj Close', 'return']]
