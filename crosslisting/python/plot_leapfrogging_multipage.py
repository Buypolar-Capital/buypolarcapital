import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")
PLOT_PATH = os.path.join(BASE_DIR, "plots", "shel_leapfrog_multipage.pdf")

# Load data
df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index

# Normalize to each day's open price
df["shel_us_norm"] = df.groupby(df.index.date)["shel_us"].transform(lambda x: x / x.dropna().iloc[0])
df["shel_eu_norm"] = df.groupby(df.index.date)["shel_eu"].transform(lambda x: x / x.dropna().iloc[0])

# Generate multipage PDF
with PdfPages(PLOT_PATH) as pdf:
    for date in sorted(set(df.index.date)):
        day_data = df[df.index.date == date]

        # Reindex both series to full 00:00–23:59
        full_range = pd.date_range(start=f"{date} 00:00", end=f"{date} 23:59", freq="5min", tz="UTC")
        lse_segment = day_data.between_time("08:00", "16:30")["shel_eu_norm"].reindex(full_range)
        nyse_segment = day_data.between_time("14:30", "21:00")["shel_us_norm"].reindex(full_range)

        plt.figure(figsize=(14, 6))
        plt.plot(lse_segment.index, lse_segment, label="LSE (08:00–16:30 UTC)", linewidth=2)
        plt.plot(nyse_segment.index, nyse_segment, label="NYSE (14:30–21:00 UTC)", linewidth=2, alpha=0.8)

        plt.title(f"SHELL Leapfrogging — {date}", fontsize=14)
        plt.xlabel("Time (UTC)")
        plt.ylabel("Normalized Price (Start-of-Day = 1.0)")
        plt.ylim(0.97, 1.03)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.legend()
        plt.tight_layout()
        pdf.savefig()
        plt.close()

print(f"📄 Saved multi-day leapfrog report to {PLOT_PATH}")
