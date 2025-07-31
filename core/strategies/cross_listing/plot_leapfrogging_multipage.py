import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")
PLOT_PATH = os.path.join(BASE_DIR, "plots", "shel_leapfrog_fullrange.pdf")

# Load data
df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index

# Normalize each day's prices from their first valid value
df["shel_us_norm"] = df.groupby(df.index.date)["shel_us"].transform(lambda x: x / x.dropna().iloc[0])
df["shel_eu_norm"] = df.groupby(df.index.date)["shel_eu"].transform(lambda x: x / x.dropna().iloc[0])

# Generate multipage PDF with full 00:00–23:59 x-axis
with PdfPages(PLOT_PATH) as pdf:
    for date in sorted(set(df.index.date)):
        day_df = df[df.index.date == date]

        # Full timeline even where data is missing
        full_range = pd.date_range(start=f"{date} 00:00", end=f"{date} 23:55", freq="5min", tz="UTC")
        lse_plot = day_df["shel_eu_norm"].reindex(full_range)
        nyse_plot = day_df["shel_us_norm"].reindex(full_range)

        # Plot
        plt.figure(figsize=(14, 6))
        plt.plot(lse_plot.index, lse_plot, label="LSE (08:00–16:30 UTC)", linewidth=2)
        plt.plot(nyse_plot.index, nyse_plot, label="NYSE (14:30–21:00 UTC)", linewidth=2, alpha=0.8)

        # Styling
        plt.title(f"SHELL Intraday Leapfrogging — {date}", fontsize=14)
        plt.xlabel("Time (UTC)")
        plt.ylabel("Normalized Price (Start-of-Day = 1.0)")
        plt.ylim(0.97, 1.03)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"✅ Saved full-range leapfrog PDF to {PLOT_PATH}")
