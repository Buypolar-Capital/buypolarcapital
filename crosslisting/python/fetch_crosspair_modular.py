import os
import pandas as pd
import yfinance as yf

def fetch_crosspair_data(name, eu_ticker, us_ticker):
    try:
        print(f"📥 Downloading 5m data for: {eu_ticker} and {us_ticker}")
        
        BASE_DIR = os.path.dirname(__file__)
        DATA_PATH = os.path.join(BASE_DIR, "data", f"{name}_intraday.csv")

        # Download data
        df_eu = yf.download(eu_ticker, interval="5m", period="30d", auto_adjust=False, progress=False)
        df_us = yf.download(us_ticker, interval="5m", period="30d", prepost=True, auto_adjust=False, progress=False)

        if df_eu.empty or df_us.empty:
            raise ValueError("❌ One of the tickers returned empty data.")

        # Timezone conversion
        df_eu.index = df_eu.index.tz_localize("UTC") if df_eu.index.tzinfo is None else df_eu.index.tz_convert("UTC")
        df_us.index = df_us.index.tz_localize("UTC") if df_us.index.tzinfo is None else df_us.index.tz_convert("UTC")

        # Combine close prices
        eu_series = df_eu["Close"]
        eu_series.name = "eu"
        us_series = df_us["Close"]
        us_series.name = "us"

        df = pd.concat([eu_series, us_series], axis=1).dropna()

        # Save
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH)
        print(f"✅ Saved to {DATA_PATH}")
        return df

    except Exception as e:
        print(f"❌ Fetch error for {name}: {e}")
        return None
