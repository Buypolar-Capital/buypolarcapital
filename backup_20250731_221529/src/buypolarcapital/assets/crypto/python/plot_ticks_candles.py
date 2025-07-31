import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
SYMBOL = "BTCUSDT"
DATE = "2024-03-01"
FILE = f"tick_data/{SYMBOL}_{DATE}_max10000.parquet"
REPORT_DIR = Path("report")
REPORT_PATH = REPORT_DIR / f"{SYMBOL}_{DATE}_tickcandles.pdf"
TICKS_PER_PAGE = 2000  # ultra zoom mode

# === LOAD RAW TICK DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df["q"] = df["q"].astype(float)
df["prev_p"] = df["p"].shift(1)
df = df.dropna().reset_index(drop=True)
df["color"] = df.apply(lambda row: "green" if row["p"] >= row["prev_p"] else "red", axis=1)
df["chunk"] = df.index // TICKS_PER_PAGE

REPORT_DIR.mkdir(exist_ok=True)

# === PLOT TICK CANDLES + VOLUME BARS ===
with PdfPages(REPORT_PATH) as pdf:
    for chunk_id, chunk_df in df.groupby("chunk"):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True,
                                        gridspec_kw={'height_ratios': [3, 1]})

        # Tick Candles
        for i, row in chunk_df.iterrows():
            t = row["T"]
            open_p = row["prev_p"]
            close_p = row["p"]
            color = row["color"]
            ax1.plot([t, t], [open_p, close_p], color=color, linewidth=2 + row["q"] * 0.2, alpha=0.8)

        ax1.set_title(f"{SYMBOL} One-Tick Candles + Volume | {DATE} | Page {chunk_id + 1}")
        ax1.set_ylabel("Price")
        ax1.grid(True)

        # Volume Bars
        ax2.bar(chunk_df["T"], chunk_df["q"], color=chunk_df["color"], width=0.0005)
        ax2.set_ylabel("Volume")
        ax2.grid(True)

        plt.xlabel("Time")
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"\n✅ Tick-candle + volume PDF saved to: {REPORT_PATH.resolve()}")
