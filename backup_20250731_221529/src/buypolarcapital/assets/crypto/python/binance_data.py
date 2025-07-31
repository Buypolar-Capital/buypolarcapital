# binance_data.py

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from pathlib import Path

BASE_URL = "https://api.binance.com"  

def get_agg_trades(symbol: str, start_time: int, end_time: int, limit=1000, max_trades=None):
    url = f"{BASE_URL}/api/v3/aggTrades"
    trades = []
    params = {
        "symbol": symbol.upper(),
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit
    }

    print(f"→ Fetching trades for {symbol}...")
    
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"✖ Error fetching data for {symbol}: {response.text}")
            break

        data = response.json()
        if not data:
            break

        trades.extend(data)
        last_ts = data[-1]['T']
        print(f"   ↳ Total trades: {len(trades)} | Last ts: {last_ts}")

        if last_ts >= end_time or (max_trades and len(trades) >= max_trades):
            break

        params['startTime'] = last_ts + 1
        time.sleep(0.1)

    return trades[:max_trades] if max_trades else trades


def save_to_parquet(data: list, symbol: str, output_dir: str, filename_part: str):
    df = pd.DataFrame(data)
    if df.empty:
        print(f"⚠ No data for {symbol}")
        return

    df['T'] = pd.to_datetime(df['T'], unit='ms')
    output_path = Path(output_dir) / f"{symbol}_{filename_part}.parquet"
    df.to_parquet(output_path, index=False)
    print(f"✅ Saved {symbol} data to {output_path}")


def download_binance_trades(symbol: str, date: str, output_dir: str, max_trades=10000):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(output_dir) / f"{symbol}_{date}_max{max_trades}.parquet"
    if file_path.exists():
        print(f"⏩ Skipping {symbol}, already exists: {file_path}")
        return

    start_dt = datetime.strptime(date, "%Y-%m-%d")
    end_dt = start_dt + timedelta(days=1)
    start_time = int(start_dt.timestamp() * 1000)
    end_time = int(end_dt.timestamp() * 1000)

    print(f"📦 Downloading {symbol} for {date}, capped at {max_trades} trades")
    data = get_agg_trades(symbol, start_time, end_time, max_trades=max_trades)
    save_to_parquet(data, symbol, output_dir, f"{date}_max{max_trades}")
