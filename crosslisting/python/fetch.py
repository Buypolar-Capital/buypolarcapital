import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the tickers and labels
PAIRS = [
    {"name": "schibsted_vs_aapl", "eu_ticker": "SCHA.OL", "us_ticker": "AAPL"},
    {"name": "sap_vs_sap", "eu_ticker": "SAP.DE", "us_ticker": "SAP"},
    {"name": "astrazeneca_vs_azn", "eu_ticker": "AZN.L", "us_ticker": "AZN"},
    {"name": "siemens_vs_siegy", "eu_ticker": "SIE.DE", "us_ticker": "SIEGY"},
    {"name": "nestle_vs_nsgry", "eu_ticker": "NESN.SW", "us_ticker": "NSRGY"},
    {"name": "novartis_vs_nvs", "eu_ticker": "NOVN.SW", "us_ticker": "NVS"},
    {"name": "unilever_vs_ul", "eu_ticker": "ULVR.L", "us_ticker": "UL"},
]

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_and_save_data(pair):
    try:
        print(f"Downloading data for {pair['name']}...")

        # Download price data for one full day
        df_eu = yf.download(
            pair["eu_ticker"], 
            interval="5m", 
            period="1d", 
            auto_adjust=False, 
            progress=False
        )
        df_us = yf.download(
            pair["us_ticker"], 
            interval="5m", 
            period="1d", 
            auto_adjust=False, 
            progress=False
        )

        # Validate data
        if df_eu.empty or df_us.empty:
            raise ValueError("One or both tickers returned no data")

        # Ensure UTC timezone
        df_eu.index = df_eu.index.tz_localize("UTC") if df_eu.index.tzinfo is None else df_eu.index.tz_convert("UTC")
        df_us.index = df_us.index.tz_localize("UTC") if df_us.index.tzinfo is None else df_us.index.tz_convert("UTC")

        # Define full day range from 00:01 to 23:59 UTC based on today’s date
        today = datetime.now().date()  # Use current date
        full_day = pd.date_range(
            start=f"{today} 00:01",
            end=f"{today} 23:59",
            freq="5min",
            tz="UTC"
        )
        df_eu = df_eu.reindex(full_day, method="ffill").fillna(method="ffill")
        df_us = df_us.reindex(full_day, method="ffill").fillna(method="ffill")

        # Concatenate the data
        df = pd.concat([df_eu["Close"], df_us["Close"]], axis=1)
        df.columns = ["eu", "us"]

        # Save to CSV
        data_path = os.path.join(DATA_DIR, f"{pair['name']}_intraday.csv")
        df.to_csv(data_path)
        print(f"✅ Saved data to {data_path}")
        return data_path

    except Exception as e:
        print(f"❌ Failed to fetch data for {pair['name']}: {str(e)}")
        return None

if __name__ == "__main__":
    for pair in PAIRS:
        fetch_and_save_data(pair)