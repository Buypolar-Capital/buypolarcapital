# File: simulate_exec_dataset.py
# Purpose: Generate simulated execution samples from minute-level stock data

import pandas as pd
import numpy as np
from pathlib import Path
from glob import glob
import pandas_market_calendars as mcal
import sys

# Set up folders
RAW_PATH = Path("data/raw/minute")
SAVE_PATH = Path("data/simulated")
SAVE_PATH.mkdir(parents=True, exist_ok=True)

# Check if today is a valid trading day
nyse = mcal.get_calendar("NYSE")
today = pd.Timestamp.today(tz='US/Eastern').normalize()
valid_days = nyse.valid_days(start_date=today - pd.Timedelta(days=7), end_date=today)
latest_valid_day = valid_days.max().normalize()
print(f"Latest valid trading day: {latest_valid_day}")

# Show fallback warning if needed
if today.date() != latest_valid_day.date():
    if "--force" not in sys.argv:
        print(f"⚠️ Market is closed today — using last valid trading day: {latest_valid_day.date()}")
    else:
        print(f"📅 Using last valid trading day (forced): {latest_valid_day.date()}")

# Simulation config
np.random.seed(42)
NUM_SIMS_PER_TICKER = 50
MIN_DURATION = 30  # in minutes
MAX_DURATION = 90
ORDER_SIZE_RANGE = (500, 10000)

def simulate_sample(df, ticker):
    samples = []

    if not isinstance(df.index, pd.DatetimeIndex):
        print(f"⚠️ {ticker}: Index is not a DatetimeIndex")
        return []

    df = df.copy()
    df.index = pd.to_datetime(df.index, utc=True).tz_convert('US/Eastern')
    df = df.sort_index()

    try:
        df = df.between_time("09:30", "15:30")
        print(f"{ticker}: Rows after time filter: {len(df)}")
    except Exception as e:
        print(f"⚠️ Could not filter trading hours for {ticker}: {e}")
        return []

    df = df[df["Volume"] > 0]
    print(f"{ticker}: Rows after volume filter: {len(df)}")

    if df.empty or len(df) < MIN_DURATION:
        print(f"⚠️ Insufficient data for {ticker}: {len(df)} rows")
        return []

    print(f"{ticker}: Entering simulation loop")
    for i in range(NUM_SIMS_PER_TICKER):
        print(f"{ticker}: Iteration {i} - Selecting slice")
        start_idx = np.random.randint(0, len(df) - MAX_DURATION + 1)
        duration = np.random.randint(MIN_DURATION, MAX_DURATION + 1)
        slice_df = df.iloc[start_idx:start_idx + duration].copy()

        if slice_df.empty:
            print(f"⚠️ {ticker}: Empty slice at iteration {i}")
            continue

        print(f"{ticker}: Iteration {i} - Extracting price and volume")
        order_size = np.random.randint(*ORDER_SIZE_RANGE)
        price = slice_df["Close"].to_numpy()
        volume = slice_df["Volume"].to_numpy()

        if len(price) == 0 or len(volume) == 0 or np.sum(volume) == 0:
            print(f"⚠️ {ticker}: Zero length or volume at iteration {i}")
            continue

        print(f"{ticker}: Iteration {i} - Calculating VWAP")
        vwap = np.sum(price * volume) / np.sum(volume)
        avg_exec_price = np.mean(price)
        slippage = avg_exec_price - vwap

        print(f"{ticker}: Iteration {i} - Calculating time metrics")
        first_idx = slice_df.index[0]
        minutes_since_open = (first_idx - first_idx.normalize().replace(hour=9, minute=30)).total_seconds() / 60

        print(f"{ticker}: Iteration {i} - Calculating volume metrics")
        cum_volume_before = float(df.loc[df.index < first_idx, "Volume"].sum())
        total_volume_day = float(df["Volume"].sum())
        print(f"{ticker}: Iteration {i} - Cum volume: {cum_volume_before}, Total volume: {total_volume_day}, Type: {type(total_volume_day)}")
        if total_volume_day > 0:
            volume_ratio = cum_volume_before / total_volume_day
        else:
            volume_ratio = 0.0

        print(f"{ticker}: Iteration {i} - Appending sample")
        samples.append({
            "ticker": ticker,
            "date": first_idx.date().isoformat(),
            "start_time": first_idx.time().isoformat(),
            "duration": duration,
            "order_size": order_size,
            "vwap": vwap,
            "exec_price": avg_exec_price,
            "slippage": slippage,
            "minutes_since_open": minutes_since_open,
            "volume_ratio": volume_ratio
        })
    return samples

def main():
    all_samples = []
    for path in glob(str(RAW_PATH / "*.parquet")):
        ticker = Path(path).stem
        try:
            df = pd.read_parquet(path)
            print(f"\nProcessing {ticker}:")
            print(f"Raw data index range: {df.index.min()} to {df.index.max()}")
            print(f"Unique dates in raw data: {sorted(set(df.index.date))}")

            # Filter only data for the last valid trading day
            df.index = pd.to_datetime(df.index, utc=True).tz_convert('US/Eastern')
            df = df[df.index.date == latest_valid_day.date()]
            print(f"Filtered data rows for {latest_valid_day.date()}: {len(df)}")

            samples = simulate_sample(df, ticker)
            if samples:
                all_samples.extend(samples)
                print(f"✅ Simulated {len(samples)} samples for {ticker}")
            else:
                print(f"⚠️ No samples generated for {ticker}")
        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")

    df_all = pd.DataFrame(all_samples)
    df_all.to_parquet(SAVE_PATH / "exec_dataset.parquet", index=False)
    print(f"📦 Saved {len(df_all)} total samples to {SAVE_PATH}/exec_dataset.parquet")

if __name__ == "__main__":
    main()