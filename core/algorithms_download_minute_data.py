# download_minute_data.py
import os
import yfinance as yf
import pandas as pd
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import pandas_market_calendars as mcal

# NYSE market open check (Eastern time)
nyse = mcal.get_calendar("NYSE")
today = pd.Timestamp.now(tz="US/Eastern").normalize()
schedule = nyse.valid_days(start_date=today - pd.Timedelta(days=1), end_date=today)

if len(schedule) == 0:
    print("⚠️ Market is closed today — try again on a trading day.")
    exit()

# Tickers to download (US, China, Europe, Norway)
TICKERS = [
    # US Tech
    "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NVDA", "AMD", "INTC", "NFLX",
    # US Finance & Health
    "JPM", "BAC", "GS", "WFC", "UNH", "PFE", "MRK", "CVS", "T", "VZ",
    # US Industrial + Retail
    "XOM", "CVX", "BA", "NKE", "MCD", "WMT", "HD", "DIS", "PEP", "KO",
    # China
    "BABA", "TCEHY", "JD", "NIO", "PDD",
    # Europe
    "ASML", "SAP", "RDS.A", "BP", "RIO", "UL", "AZN", "SIEGY",
    # Norway (OSEBX)
    "EQNR.OL", "NHY.OL", "DNB.OL", "MOWI.OL", "YAR.OL", "TEL.OL", "ORK.OL", "SALM.OL", "AKERBP.OL", "TGS.OL"
]

# Create save path relative to script
SAVE_DIR = Path("data/raw/minute")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

# Download + save minute data
def fetch_and_save(ticker):
    try:
        df = yf.download(ticker, period="7d", interval="1m", progress=False)
        if not df.empty:
            save_path = SAVE_DIR / f"{ticker}.parquet"
            df.to_parquet(save_path)
            print(f"✅ Saved {ticker}")
        else:
            print(f"⚠️ No data for {ticker}")
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")

# Run parallel download
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch_and_save, TICKERS)
