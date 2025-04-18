# download_batch_threaded.py

from binance_data import download_binance_trades
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path  # ← THIS IS THE FIX

TICKERS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT"
]

OUTPUT_DIR = "tick_data"
DATE = "2024-03-01"
MAX_TRADES = 10_000
MAX_WORKERS = 5

def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_binance_trades, symbol, DATE, OUTPUT_DIR, MAX_TRADES): symbol
            for symbol in TICKERS
        }
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"❌ Failed to download {symbol}: {e}")

if __name__ == "__main__":
    main()
