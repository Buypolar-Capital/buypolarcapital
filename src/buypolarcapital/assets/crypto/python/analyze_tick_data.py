import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import timedelta

# === 🧪 Load + Explore Parquet ===
FILE = "tick_data/BTCUSDT_2024-03-01_max10000.parquet"
df = pd.read_parquet(FILE)

# Convert data types
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df["q"] = df["q"].astype(float)

print("\n--- BASIC SUMMARY ---")
print(f"Num trades: {len(df)}")
print(f"Time range: {df['T'].min()} to {df['T'].max()}")
print(f"Price range: {df['p'].min():.2f} to {df['p'].max():.2f}")
print(f"Total volume traded: {df['q'].sum():,.2f}")

# === 📊 Plot price over time ===
plt.figure(figsize=(12, 5))
plt.plot(df["T"], df["p"], lw=0.5)
plt.title("BTCUSDT Trade Prices Over Time")
plt.xlabel("Time")
plt.ylabel("Price")
plt.grid(True)
plt.tight_layout()
plt.show()

# === 🔁 Resample to 1-Minute OHLCV ===
df.set_index("T", inplace=True)
ohlcv = df.resample("1min").agg({
    "p": ["first", "max", "min", "last"],
    "q": "sum"
})
ohlcv.columns = ["open", "high", "low", "close", "volume"]
ohlcv.dropna(inplace=True)

print("\n--- OHLCV SAMPLE ---")
print(ohlcv.head())

# === 🤖 LLM Summary Prompt ===
vol = ohlcv["volume"]
summary_prompt = f"""
Generate a summary of BTCUSDT market activity for 2024-03-01 using the first 10,000 trades.

- Price started at ${ohlcv['open'].iloc[0]:.2f} and ended at ${ohlcv['close'].iloc[-1]:.2f}.
- Intraday high was ${ohlcv['high'].max():.2f}, and the low was ${ohlcv['low'].min():.2f}.
- The period saw a total volume of {vol.sum():,.2f} BTC traded across {len(ohlcv)} minutes.
- Average volume per minute: {vol.mean():.2f}, with peak at {vol.max():.2f}.

Highlight volatility, price trends, and periods of high volume.
"""

print("\n--- LLM PROMPT ---")
print(summary_prompt.strip())
