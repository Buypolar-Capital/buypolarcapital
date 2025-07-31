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
REPORT_PATH = REPORT_DIR / f"{SYMBOL}_{DATE}_candlesticks.pdf"
CHUNK_SIZE = 60  # minutes per page

# === LOAD TICK DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)

# Resample to 1-minute OHLC
df.set_index("T", inplace=True)
ohlc = df["p"].resample("1min").ohlc().dropna()
ohlc.reset_index(inplace=True)

# Split into chunks
ohlc["group"] = ohlc.index // CHUNK_SIZE

# === PLOT MULTI-PAGE CANDLESTICKS ===
REPORT_DIR.mkdir(exist_ok=True)
with PdfPages(REPORT_PATH) as pdf:
    for group, chunk in ohlc.groupby("group"):
        fig, ax = plt.subplots(figsize=(10, 5))
        for idx, row in chunk.iterrows():
            t = row["T"]
            color = "green" if row["close"] >= row["open"] else "red"
            ax.plot([t, t], [row["low"], row["high"]], color=color, linewidth=1)  # wick
            ax.plot([t, t], [row["open"], row["close"]], color=color, linewidth=4)  # body

        ax.set_title(f"{SYMBOL} Candlestick Chart | {DATE} | Page {group + 1}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator())
        ax.grid(True)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"\n✅ Multi-page candlestick PDF saved to: {REPORT_PATH.resolve()}")
