import os
import yfinance as yf
import pandas as pd

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
    print(f"Downloading data for {pair['name']}...")

    # Download price data for one full day (from 00:00 to 23:59)
    df_eu = yf.download(pair["eu_ticker"], interval="5m", period="1d", auto_adjust=False, progress=False)
    df_us = yf.download(pair["us_ticker"], interval="5m", period="1d", auto_adjust=False, progress=False)

    # Ensure timestamps are aligned to GMT
    df_eu.index = df_eu.index.tz_localize("UTC") if df_eu.index.tzinfo is None else df_eu.index.tz_convert("UTC")
    df_us.index = df_us.index.tz_localize("UTC") if df_us.index.tzinfo is None else df_us.index.tz_convert("UTC")

    # Concatenate the data
    df = pd.concat([df_eu['Close'], df_us['Close']], axis=1)
    df.columns = ['eu', 'us']  # Renaming the columns after concatenating

    # Save to CSV
    data_path = os.path.join(DATA_DIR, f"{pair['name']}_intraday.csv")
    df.to_csv(data_path)

    print(f"✅ Saved data to {data_path}")
    return data_path

for pair in PAIRS:
    fetch_and_save_data(pair)
