import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_crosspair_leapfrog(name, data_path, output_path, eu_label, us_label):
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)

    if df.empty or df.shape[1] != 2:
        raise ValueError(f"❌ Invalid data format for {name}")

    df.columns = ["eu", "us"]
    df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")

    # Normalize
    def normalize_day(x):
        x_clean = x.dropna()
        return x / x_clean.iloc[0] if not x_clean.empty else pd.Series(index=x.index, dtype=float)

    df["eu_norm"] = df.groupby(df.index.date)["eu"].transform(normalize_day)
    df["us_norm"] = df.groupby(df.index.date)["us"].transform(normalize_day)

    MARKET_HOURS = {
        "eu": {"start": "07:00", "end": "15:25"},
        "us": {"start": "14:30", "end": "21:00"}
    }

    with PdfPages(output_path) as pdf:
        for date in sorted(set(df.index.date)):
            try:
                day = df[df.index.date == date]
                if day.empty:
                    continue

                full_range = pd.date_range(
                    start=f"{date} 00:00",
                    end=f"{date} 23:55",
                    freq="5min",
                    tz="UTC"
                )

                # Absolute prices
                eu_abs = day.between_time(MARKET_HOURS["eu"]["start"], MARKET_HOURS["eu"]["end"])["eu"].reindex(full_range, method="ffill")
                us_abs = day.between_time(MARKET_HOURS["us"]["start"], MARKET_HOURS["us"]["end"])["us"].reindex(full_range, method="ffill")

                # Normalized
                eu_norm = day.between_time(MARKET_HOURS["eu"]["start"], MARKET_HOURS["eu"]["end"])["eu_norm"].reindex(full_range, method="ffill")
                us_norm = day.between_time(MARKET_HOURS["us"]["start"], MARKET_HOURS["us"]["end"])["us_norm"].reindex(full_range, method="ffill")

                fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 10), sharex=True)

                # Absolute price plot
                axes[0].plot(eu_abs.index, eu_abs, label=eu_label, linewidth=2, color="#2ecc71")
                axes[0].plot(us_abs.index, us_abs, label=us_label, linewidth=2, color="#e74c3c", alpha=0.8)
                axes[0].set_ylabel("Absolute Price")
                axes[0].legend()
                axes[0].set_title(f"{name} — {date}", fontsize=14)
                axes[0].grid(True, linestyle="--", alpha=0.3)

                # Normalized plot
                axes[1].plot(eu_norm.index, eu_norm, label=eu_label + " (norm)", linewidth=2, color="#2ecc71")
                axes[1].plot(us_norm.index, us_norm, label=us_label + " (norm)", linewidth=2, color="#e74c3c", alpha=0.8)
                axes[1].set_ylabel("Normalized (start = 1.0)")
                axes[1].legend()
                axes[1].grid(True, linestyle="--", alpha=0.3)

                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close(fig)
                print(f"✅ Plotted {name} — {date}")
            except Exception as e:
                print(f"⚠️ Skipped {name} — {date}: {e}")
                continue

    print(f"✅ Saved PDF to {output_path}")

# Optional: example manual run (comment out or delete if unused)
# if __name__ == "__main__":
#     BASE_DIR = os.path.dirname(__file__)
#     plot_crosspair_leapfrog(
#         name="schibsted_vs_aapl",
#         data_path=os.path.join(BASE_DIR, "data", "schibsted_vs_aapl_intraday.csv"),
#         output_path=os.path.join(BASE_DIR, "plots", "schibsted_vs_aapl_leapfrog.pdf"),
#         eu_label="Schibsted (SCHA.OL)",
#         us_label="Apple (AAPL)"
#     )
