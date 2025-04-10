import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
SYMBOL = "BTCUSDT"
DATE = "2024-03-01"
FILE = f"tick_data/{SYMBOL}_{DATE}_max10000.parquet"
REPORT_DIR = Path("report")
REPORT_PATH = REPORT_DIR / f"{SYMBOL}_{DATE}_microcandles.pdf"
CANDLE_INTERVAL = "0.01s"
CHUNK_SIZE = 1000  # how many candles per page (5s * 120 = 10 minutes)

# === LOAD TICK DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df.set_index("T", inplace=True)

# === RESAMPLE TO MICRO CANDLES ===
ohlc = df["p"].resample(CANDLE_INTERVAL).ohlc().dropna()
ohlc.reset_index(inplace=True)
ohlc["group"] = ohlc.index // CHUNK_SIZE

# === PLOT MULTI-PAGE MICRO CANDLESTICKS ===
REPORT_DIR.mkdir(exist_ok=True)
with PdfPages(REPORT_PATH) as pdf:
    for group_id, chunk in ohlc.groupby("group"):
        fig, ax = plt.subplots(figsize=(10, 5))
        for _, row in chunk.iterrows():
            t = row["T"]
            color = "green" if row["close"] >= row["open"] else "red"
            ax.plot([t, t], [row["low"], row["high"]], color=color, linewidth=1)  # wick
            ax.plot([t, t], [row["open"], row["close"]], color=color, linewidth=4)  # body

        ax.set_title(f"{SYMBOL} Micro-Candles (5s) | {DATE} | Page {group_id + 1}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
        ax.grid(True)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"\n✅ Micro-candle PDF saved to: {REPORT_PATH.resolve()}")
