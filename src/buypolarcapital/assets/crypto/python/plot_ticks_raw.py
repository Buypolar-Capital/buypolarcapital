
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# === CONFIG ===
SYMBOL = "BTCUSDT"
DATE = "2024-03-01"
FILE = f"tick_data/{SYMBOL}_{DATE}_max10000.parquet"
REPORT_DIR = Path("report")
REPORT_PATH = REPORT_DIR / f"{SYMBOL}_{DATE}_ticks.pdf"
TICKS_PER_PAGE = 2000  # Adjust to control how dense each page is

# === LOAD TICK DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df["q"] = df["q"].astype(float)  # volume

# === Add chunking for pagination ===
df["chunk"] = df.index // TICKS_PER_PAGE
REPORT_DIR.mkdir(exist_ok=True)

# === Plot raw ticks ===
with PdfPages(REPORT_PATH) as pdf:
    for chunk_id, chunk_df in df.groupby("chunk"):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.scatter(chunk_df["T"], chunk_df["p"], s=chunk_df["q"]*2, alpha=0.6, c="blue", edgecolor="none")

        ax.set_title(f"{SYMBOL} Raw Tick Plot | {DATE} | Page {chunk_id + 1}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")
        ax.grid(True)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

print(f"\n✅ Tick-by-tick PDF saved to: {REPORT_PATH.resolve()}")
