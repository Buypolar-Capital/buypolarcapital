# src/data/fetch_data.py
import yfinance as yf
import pandas as pd

def get_data_yf(tickers, start=None, end=None, interval="1d", auto_adjust=True):
    """
    Fetch historical price data from Yahoo Finance.
    - Handles both single and multiple tickers
    - Supports auto_adjust flag (default: True)
    """
    if isinstance(tickers, str):
        tickers = [tickers]

    data = yf.download(tickers, start=start, end=end, interval=interval, auto_adjust=auto_adjust)

    # Determine which price column to use
    price_column = "Close" if auto_adjust else "Adj Close"

    if isinstance(data.columns, pd.MultiIndex):
        df = data[price_column].copy()
    else:
        df = data[[price_column]].copy()
        df.columns = [tickers[0]]

    df = df.reset_index().melt(id_vars="Date", var_name="ticker", value_name="price")
    df.columns = ["date", "ticker", "price"]
    return df.dropna()
