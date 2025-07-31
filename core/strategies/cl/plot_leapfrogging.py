import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")
PLOT_PATH = os.path.join(BASE_DIR, "plots", "shel_leapfrog_segments.pdf")

# Load and convert index to datetime
df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)

# Ensure UTC timezone on index
df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index

# Normalize both to start-of-day value
df["shel_us_norm"] = df["shel_us"] / df["shel_us"].dropna().iloc[0]
df["shel_eu_norm"] = df["shel_eu"] / df["shel_eu"].dropna().iloc[0]

# Build new columns that ONLY show values during market hours
lse_open = "08:00"
lse_close = "16:30"
nyse_open = "14:30"
nyse_close = "21:00"

lse_segment = df.between_time(lse_open, lse_close)["shel_eu_norm"]
nyse_segment = df.between_time(nyse_open, nyse_close)["shel_us_norm"]

# Reindex to full 00:00–23:59 range to show gaps where no trading happens
all_times = pd.date_range(start=df.index[0].normalize(), periods=1440, freq="T", tz="UTC")
lse_segment_full = lse_segment.reindex(all_times)
nyse_segment_full = nyse_segment.reindex(all_times)

# Plot
plt.figure(figsize=(14, 6))
plt.plot(lse_segment_full.index, lse_segment_full, label="LSE (09:00–16:30)", linewidth=2)
plt.plot(nyse_segment_full.index, nyse_segment_full, label="NYSE (14:30–21:00)", linewidth=2, alpha=0.8)

# Styling
plt.title("Shell: Intraday Leapfrogging Price Segments (UTC)", fontsize=14)
plt.xlabel("Time (UTC)")
plt.ylabel("Normalized Price (Start-of-Day = 1.0)")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# Save
os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)
plt.savefig(PLOT_PATH)
print(f"📊 Saved segmented leapfrogging plot to {PLOT_PATH}")
