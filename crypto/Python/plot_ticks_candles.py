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
TICKS_PER_PAGE = 10000

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

# === PLOT "TICK CANDLES" PER PAGE ===
with PdfPages(REPORT_PATH) as pdf:
    for chunk_id, chunk_df in df.groupby("chunk"):
        fig, ax = plt.subplots(figsize=(10, 5))

        for i, row in chunk_df.iterrows():
            t = row["T"]
            open_p = row["prev_p"]
            close_p = row["p"]
            color = row["color"]
            ax.plot([t, t], [open_p, close_p], color=color, linewidth=2 + row["q"] * 0.2, alpha=0.8)

        ax.set_title(f"{SYMBOL} One-Tick Candles | {DATE} | Page {chunk_id + 1}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.grid(True)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"\n✅ Tick-candle PDF saved to: {REPORT_PATH.resolve()}")
