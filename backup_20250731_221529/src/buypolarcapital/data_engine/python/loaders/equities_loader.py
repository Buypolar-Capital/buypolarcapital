import yfinance as yf
import pandas as pd
from pathlib import Path
from ..utils.config import DATA_PATH

def load_equities(tickers, start="2010-01-01", end=None):
    all_data = []
    for ticker in tickers:
        df = yf.download(ticker, start=start, end=end)
        df['ticker'] = ticker
        all_data.append(df.reset_index())

    df_all = pd.concat(all_data, axis=0)
    df_all.to_parquet(DATA_PATH / "equities" / "ohlcv.parquet", index=False)
    print("[✔] Saved equities data")