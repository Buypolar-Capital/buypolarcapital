import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_crosspair_leapfrog(name, eu_label, us_label):
    BASE_DIR = os.path.dirname(__file__)
    DATA_PATH = os.path.join(BASE_DIR, "data", f"{name}_intraday.csv")
    PLOT_PATH = os.path.join(BASE_DIR, "plots", f"{name}_leapfrog.pdf")

    if not os.path.exists(DATA_PATH):
        print(f"❌ Data file not found for {name}")
        return

    df = pd.read_csv(DATA_PATH, index_col=0, parse_dates=True)
    if df.empty:
        print(f"❌ Data for {name} is empty")
        return

    df.columns = ["eu", "us"]
    df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")

    def normalize_day(x):
        x_clean = x.dropna()
        return x / x_clean.iloc[0] if not x_clean.empty else pd.Series(index=x.index, dtype=float)

    df["eu_norm"] = df.groupby(df.index.date)["eu"].transform(normalize_day)
    df["us_norm"] = df.groupby(df.index.date)["us"].transform(normalize_day)

    MARKET_HOURS = {
        "eu": {"start": "07:00", "end": "15:25", "label": eu_label},
        "us": {"start": "14:30", "end": "21:00", "label": us_label}
    }

    os.makedirs(os.path.dirname(PLOT_PATH), exist_ok=True)

    with PdfPages(PLOT_PATH) as pdf:
        for date in sorted(set(df.index.date)):
            day = df[df.index.date == date]
            if day.empty or day["eu_norm"].isna().all() or day["us_norm"].isna().all():
                continue

            full_range = pd.date_range(
                start=f"{date} 00:00",
                end=f"{date} 23:55",
                freq="5min",
                tz="UTC"
            )

            eu = day.between_time(MARKET_HOURS["eu"]["start"], MARKET_HOURS["eu"]["end"])["eu_norm"].reindex(full_range, method="ffill")
            us = day.between_time(MARKET_HOURS["us"]["start"], MARKET_HOURS["us"]["end"])["us_norm"].reindex(full_range, method="ffill")

            plt.figure(figsize=(15, 7))
            plt.plot(eu.index, eu, label=MARKET_HOURS["eu"]["label"], linewidth=2, color="#2ecc71")
            plt.plot(us.index, us, label=MARKET_HOURS["us"]["label"], linewidth=2, color="#e74c3c", alpha=0.8)

            plt.title(f"Cross-Market Leapfrogging — {date}", fontsize=16, pad=15)
            plt.xlabel("Time (UTC)", fontsize=12)
            plt.ylabel("Normalized Price (Day Start = 1.0)", fontsize=12)
            plt.ylim(0.95, 1.05)
            plt.xticks(rotation=45, ha="right")
            plt.grid(True, linestyle="--", alpha=0.4, which="both")

            plt.axvspan(
                pd.Timestamp(f"{date} {MARKET_HOURS['eu']['start']} UTC"),
                pd.Timestamp(f"{date} {MARKET_HOURS['eu']['end']} UTC"),
                color="green", alpha=0.1, label="EU Market Hours"
            )
            plt.axvspan(
                pd.Timestamp(f"{date} {MARKET_HOURS['us']['start']} UTC"),
                pd.Timestamp(f"{date} {MARKET_HOURS['us']['end']} UTC"),
                color="red", alpha=0.1, label="US Market Hours"
            )

            plt.legend(loc="best", fontsize=10)
            plt.tight_layout()
            pdf.savefig(dpi=150)
            plt.close()
            print(f"✅ Plotted {name} — {date}")

    print(f"✅ Saved PDF to {PLOT_PATH}")

# Testable manually
if __name__ == "__main__":
    plot_crosspair_leapfrog("schibsted_vs_aapl", "Schibsted (SCHA.OL)", "Apple (AAPL)")
