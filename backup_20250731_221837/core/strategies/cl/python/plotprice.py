import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

def plot_price_data(name, eu_label, us_label, data_path, output_path):
    try:
        # Load data
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)
        if df.empty:
            raise ValueError("Data file is empty")

        # Debug column names
        print(f"Debug: Columns in {name}: {df.columns.tolist()}")

        # Ensure UTC timezone
        df.index = df.index.tz_localize("UTC") if df.index.tzinfo is None else df.index.tz_convert("UTC")

        # Handle missing or non-numeric data
        if df["eu"].isnull().all() or df["us"].isnull().all():
            raise ValueError("All data is missing")
        df = df.dropna()

        if not (pd.api.types.is_numeric_dtype(df["eu"]) and pd.api.types.is_numeric_dtype(df["us"])):
            raise ValueError("Non-numeric data detected")

        # Normalize prices
        df["eu_norm"] = df["eu"] / df["eu"].iloc[0]
        df["us_norm"] = df["us"] / df["us"].iloc[0]

        # Calculate returns
        df["eu_return"] = df["eu"].pct_change().fillna(0)
        df["us_return"] = df["us"].pct_change().fillna(0)
        first_eu_ret = df["eu_return"][df["eu_return"] != 0].iloc[0] if any(df["eu_return"] != 0) else 1
        first_us_ret = df["us_return"][df["us_return"] != 0].iloc[0] if any(df["us_return"] != 0) else 1
        df["eu_return_norm"] = df["eu_return"] / first_eu_ret
        df["us_return_norm"] = df["us_return"] / first_us_ret

        # Ensure full day range from 00:01 to 23:59 UTC
        day_start = df.index[0].date()  # Use date from data
        full_day = pd.date_range(
            start=f"{day_start} 00:01",
            end=f"{day_start} 23:59",
            freq="5min",
            tz="UTC"
        )
        df = df.reindex(full_day, method="ffill")

        # Plot
        with PdfPages(output_path) as pdf:
            fig, axs = plt.subplots(2, 1, figsize=(15, 12), sharex=True, height_ratios=[1, 1])

            # Top: Absolute prices
            axs[0].plot(df.index, df["eu"], label=eu_label, linewidth=2, color="#2ecc71")
            axs[0].plot(df.index, df["us"], label=us_label, linewidth=2, color="#e74c3c", alpha=0.8)
            axs[0].set_title(f"{name} — Absolute Prices", fontsize=16, pad=15)
            axs[0].set_ylabel("Price (Local Currency)", fontsize=12)
            axs[0].legend(loc="best", fontsize=10)
            axs[0].grid(True, linestyle="--", alpha=0.4, which="both")

            # Bottom: Normalized returns
            axs[1].plot(df.index, df["eu_return_norm"], label=eu_label, linewidth=2, color="#2ecc71")
            axs[1].plot(df.index, df["us_return_norm"], label=us_label, linewidth=2, color="#e74c3c", alpha=0.8)
            axs[1].set_title(f"{name} — Normalized Returns", fontsize=16, pad=15)
            axs[1].set_xlabel("Time (UTC)", fontsize=12)
            axs[1].set_ylabel("Normalized Return", fontsize=12)
            axs[1].legend(loc="best", fontsize=10)
            axs[1].grid(True, linestyle="--", alpha=0.4, which="both")

            # Format x-axis
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()

            pdf.savefig(dpi=150)
            plt.close()
            print(f"✅ Plotted {name} data to {output_path}")

    except Exception as e:
        print(f"❌ Failed to plot {name}: {str(e)}")

if __name__ == "__main__":
    # Example usage for testing
    plot_price_data(
        "test_pair",
        "EU Test",
        "US Test",
        os.path.join(os.path.dirname(__file__), "data", "schibsted_vs_aapl_intraday.csv"),
        os.path.join(os.path.dirname(__file__), "plots", "test_output.pdf")
    )