import os
import pandas as pd
import yfinance as yf
from pathlib import Path


# Constants
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw"
CSV_PATH = DATA_PATH / "osebx_changes.csv"
PRICE_FOLDER = DATA_PATH / "prices"
START_DATE = "2010-01-01"
END_DATE = "2022-12-31"


def read_tickers(csv_path):
    """Read the tickers from the CSV file and print the columns."""
    df = pd.read_csv(csv_path)
    print("CSV columns detected:", df.columns.tolist())
    tickers = df['ticker'].dropna().unique().tolist()
    print("Tickers parsed:", tickers)
    return tickers


def download_price_data(ticker, start, end):
    """Download historical price data from Yahoo Finance."""
    print(f"Downloading {ticker}...")
    try:
        df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
        if not df.empty:
            df.reset_index(inplace=True)  # Reset index to make the date a column
            return df
        else:
            print(f"No data found for {ticker}")
    except Exception as e:
        print(f"Error downloading {ticker}: {e}")
    return None


def save_all_prices(tickers):
    """Download and save price data for each ticker."""
    PRICE_FOLDER.mkdir(parents=True, exist_ok=True)
    for ticker in tickers:
        filename = PRICE_FOLDER / f"{ticker}.csv"
        # Check if the file already exists, and if so, skip downloading
        if filename.exists():
            print(f"Already downloaded: {ticker}")
            continue
        # Download data
        df = download_price_data(ticker, START_DATE, END_DATE)
        if df is not None:
            df.to_csv(filename, index=False)  # Save to CSV if data is available


if __name__ == "__main__":
    tickers = read_tickers(CSV_PATH)  # Read the tickers from the CSV
    save_all_prices(tickers)  # Save all the price data
