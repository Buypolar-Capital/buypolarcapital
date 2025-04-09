import os
import pandas as pd
import yfinance as yf
from datetime import datetime

def download_stock_data():
    try:
        # Debug: Verify __file__ is working
        print("Debug: Script path:", __file__)
        
        # Define paths and constants
        BASE_DIR = os.path.dirname(__file__)
        print("Debug: BASE_DIR:", BASE_DIR)
        
        DATA_PATH = os.path.join(BASE_DIR, "data", "crosspair_intraday.csv")
        print("Debug: DATA_PATH:", DATA_PATH)
        
        # Stock pair configuration
        PAIR_CONFIG = {
            "name": "schibsted_vs_aapl",
            "eu_ticker": "SCHA.OL",  # Oslo Børs: Schibsted A
            "us_ticker": "AAPL"      # NASDAQ
        }

        print(f"📥 Downloading 5m data for: {PAIR_CONFIG['eu_ticker']} and {PAIR_CONFIG['us_ticker']}")
        
        # Download data
        df_eu = yf.download(
            PAIR_CONFIG["eu_ticker"], 
            interval="5m", 
            period="30d",
            auto_adjust=False,
            progress=False
        )
        print("Debug: EU data downloaded, shape:", df_eu.shape)
        
        df_us = yf.download(
            PAIR_CONFIG["us_ticker"], 
            interval="5m", 
            period="30d",
            prepost=True,
            auto_adjust=False,
            progress=False
        )
        print("Debug: US data downloaded, shape:", df_us.shape)

        # Validate data
        if df_eu.empty or df_us.empty:
            raise ValueError(f"❌ Data download failed for one or both tickers: {PAIR_CONFIG['eu_ticker']}, {PAIR_CONFIG['us_ticker']}")

        # Handle timezones with explicit checks
        print("Debug: Processing EU timezone...")
        if df_eu.index.tzinfo is None:
            df_eu.index = df_eu.index.tz_localize("UTC")
        else:
            df_eu.index = df_eu.index.tz_convert("UTC")
            
        print("Debug: Processing US timezone...")
        if df_us.index.tzinfo is None:
            df_us.index = df_us.index.tz_localize("UTC")
        else:
            df_us.index = df_us.index.tz_convert("UTC")

        # Extract and combine closing prices - simplified approach
        print("Debug: Combining data...")
        eu_series = df_eu["Close"]
        eu_series.name = "eu"  # Set name directly instead of using rename()
        us_series = df_us["Close"]
        us_series.name = "us"  # Set name directly instead of using rename()
        
        df = pd.concat([eu_series, us_series], axis=1).dropna()
        print("Debug: Combined data shape:", df.shape)

        # Save data
        print("Debug: Creating directory...")
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        print("Debug: Saving to CSV...")
        df.to_csv(DATA_PATH)
        print(f"✅ Saved aligned data to {DATA_PATH}")
        
        return df

    except Exception as e:
        print(f"Error: Failed to download or process data: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    download_stock_data()