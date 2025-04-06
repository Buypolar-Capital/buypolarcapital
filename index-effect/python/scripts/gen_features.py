import pandas as pd
from pathlib import Path
import numpy as np
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_PATH = Path(__file__).resolve().parent.parent
PRICE_DIR = BASE_PATH / "data" / "prices"
TICKER_CSV = BASE_PATH / "data" / "raw" / "osebx_changes.csv"  # Corrected file path
OUTPUT_CSV = BASE_PATH / "data" / "processed" / "features_2010_2022.csv"

# Debugging output
print("Loading tickers...")
try:
    tickers_df = pd.read_csv(TICKER_CSV, parse_dates=["add_dates", "remove_dates"], encoding="utf-8")
    print(f"✅ Loaded {len(tickers_df)} ticker entries.")
except Exception as e:
    print(f"❌ Error loading ticker CSV: {e}")
    sys.exit(1)

all_data = []

# Process each ticker
for idx, row in tickers_df.iterrows():
    ticker = row["ticker"]
    add_date = row["add_dates"]
    remove_date = row["remove_dates"]

    print(f"Processing ticker: {ticker} | Add Date: {add_date} | Remove Date: {remove_date}")  # Debugging line

    price_path = PRICE_DIR / f"{ticker}.csv"
    if not price_path.exists():
        print(f"⚠️  Missing data file for {ticker}")
        continue

    try:
        df = pd.read_csv(price_path, parse_dates=["Date"], encoding="utf-8")  # Use utf-8 encoding here too
        df = df.sort_values("Date")
    except Exception as e:
        print(f"❌ Error reading price data for {ticker}: {e}")
        continue

    # Filter between add/remove window
    df = df[df["Date"] >= pd.to_datetime(add_date)]
    if pd.notnull(remove_date):
        df = df[df["Date"] <= pd.to_datetime(remove_date)]

    if df.empty:
        print(f"⚠️  No data for {ticker} between {add_date} and {remove_date}")
        continue

    df["ticker"] = ticker
    df["included"] = 1  # Mark these as included during this period

    # Feature engineering
    df["return_60d"] = df["Close"].pct_change(60)
    df["volatility_60d"] = df["Close"].rolling(60).std()
    df["turnover_60d"] = df["Volume"].rolling(60).mean()
    df["trading_days_ratio"] = (
        df["Volume"].rolling(60).count() / 60
    )

    all_data.append(df)

if not all_data:
    raise ValueError("No data was processed for any ticker. Check CSV or price files.")

final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df.dropna(subset=["return_60d", "volatility_60d", "turnover_60d"])

# Debugging output to confirm data
print(f"✅ Processed data for {len(final_df)} rows. Saving features to {OUTPUT_CSV}")

final_df.to_csv(OUTPUT_CSV, index=False)
print("✅ Done.")
