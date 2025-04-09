import os
import pandas as pd
import matplotlib.pyplot as plt

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "shel_intraday_utc.csv")
PLOT_PATH = os.path.join(BASE_DIR, "plots", "shel_leapfrog.pdf")

# Load data
df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)

# Optional: Rescale shel_eu from GBp to GBP for visual comparison
df["shel_eu_gbp"] = df["shel_eu"] / 100

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df.index, df["shel_us"], label="SHEL (NYSE, USD)", linewidth=1.5)
plt.plot(df.index, df["shel_eu_gbp"], label="SHEL.L (LSE, GBP)", linewidth=1.5, alpha=0.8)

# Vertical lines for open hours (UTC)
date_str = df.index[0].strftime("%Y-%m-%d")
plt.axvline(pd.to_datetime(f"{date_str} 08:00"), color="gray", linestyle="--", label="London Open (08:00 UTC)")
plt.axvline(pd.to_datetime(f"{date_str} 14:30"), color="black", linestyle="--", label="NYSE Open (14:30 UTC)")

# Final touches
plt.title("Shell Intraday Movement: LSE → NYSE (Leapfrogging Effect)", fontsize=14)
plt.xlabel("Time (UTC)")
plt.ylabel("Price")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# Save
os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)
plt.savefig(PLOT_PATH)
print(f"📈 Plot saved to {PLOT_PATH}")
