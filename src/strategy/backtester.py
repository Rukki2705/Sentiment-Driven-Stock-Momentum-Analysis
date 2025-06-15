import pandas as pd

def apply_backtest(df):
    """
    Simulate strategy returns.
    If signal == 1, take next day's return.
    """
    df = df.copy()
    df['strategy_return'] = df['signal'].shift(1) * df['return']
    df['cumulative_strategy_return'] = (1 + df['strategy_return']).cumprod()
    df['cumulative_market_return'] = (1 + df['return']).cumprod()
    return df
