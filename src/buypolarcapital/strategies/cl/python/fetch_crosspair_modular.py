import builtins
str = builtins.str  # Restore built-in str function if overwritten
assert str is builtins.str, "You've overwritten the built-in 'str' function!"
import builtins
str = builtins.str
assert callable(str)


import os
import pandas as pd
import yfinance as yf
import builtins

def fetch_crosspair_data(name, eu_ticker, us_ticker):
    try:
        print(f"📥 Downloading 5m data for: {eu_ticker} and {us_ticker}")
        BASE_DIR = os.path.dirname(__file__)
        DATA_PATH = os.path.join(BASE_DIR, "data", f"{name}_intraday.csv")

        # Download data
        df_eu = yf.download(eu_ticker, interval="5m", period="30d", auto_adjust=False, progress=False)
        df_us = yf.download(us_ticker, interval="5m", period="30d", prepost=True, auto_adjust=False, progress=False)

        if df_eu.empty or df_us.empty:
            raise ValueError("One or both tickers returned empty data.")

        # Timezone alignment
        df_eu.index = df_eu.index.tz_localize("UTC") if df_eu.index.tzinfo is None else df_eu.index.tz_convert("UTC")
        df_us.index = df_us.index.tz_localize("UTC") if df_us.index.tzinfo is None else df_us.index.tz_convert("UTC")

        # Extract close prices
        df = pd.concat([df_eu["Close"].rename("eu"), df_us["Close"].rename("us")], axis=1).dropna()

        # Save to CSV
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH)
        print(f"✅ Saved to {DATA_PATH}")
        return DATA_PATH

    except Exception as e:
        print(f"❌ Failed {name}: {e}")
        return None
