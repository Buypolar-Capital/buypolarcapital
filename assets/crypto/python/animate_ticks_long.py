import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pathlib import Path

# === CONFIG ===
SYMBOL = "BTCUSDT"
DATE = "2024-03-01"
FILE = f"tick_data/{SYMBOL}_{DATE}_max10000.parquet"  # use more ticks
OUT_PATH = Path(f"report/{SYMBOL}_{DATE}_tick_animation_cumulative_long.gif")
FPS = 24
FRAME_SIZE = 250  # smaller = more frames, more granularity

# === LOAD DATA ===
df = pd.read_parquet(FILE)
df["T"] = pd.to_datetime(df["T"])
df["p"] = df["p"].astype(float)
df["q"] = df["q"].astype(float)
df["prev_p"] = df["p"].shift(1)
df = df.dropna().reset_index(drop=True)
df["color"] = df.apply(lambda row: "green" if row["p"] >= row["prev_p"] else "red", axis=1)

# === FIXED AXIS RANGE ===
ymin, ymax = df["p"].min() - 5, df["p"].max() + 5
xmin, xmax = df["T"].min(), df["T"].max()

# === ANIMATION SETUP ===
fig, ax = plt.subplots(figsize=(10, 5))

def update(frame_idx):
    ax.clear()
    window = df.iloc[: (frame_idx + 1) * FRAME_SIZE]
    for _, row in window.iterrows():
        t = row["T"]
        open_p = row["prev_p"]
        close_p = row["p"]
        color = row["color"]
        ax.plot([t, t], [open_p, close_p], color=color, linewidth=2 + row["q"] * 0.2, alpha=0.8)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_title(f"{SYMBOL} Cumulative Tick Candles | {DATE} | Frame {frame_idx + 1}")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True)

frame_count = len(df) // FRAME_SIZE

ani = animation.FuncAnimation(fig, update, frames=frame_count, interval=1000 // FPS)
ani.save(OUT_PATH, writer='pillow', dpi=120)

print(f"\n✅ Expanded cumulative tick animation saved to: {OUT_PATH.resolve()}")
