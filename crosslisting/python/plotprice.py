import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_price_data(name, eu_label, us_label, data_path, output_path):
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)

    # Normalize prices (set to 1 at the start of the day)
    df["eu_norm"] = df["eu"] / df["eu"].iloc[0]
    df["us_norm"] = df["us"] / df["us"].iloc[0]

    # Market hours (UTC)
    MARKET_HOURS = {
        "eu": {"start": "07:00", "end": "15:25", "label": eu_label},
        "us": {"start": "14:30", "end": "21:00", "label": us_label}
    }

    # Generate PDF
    with PdfPages(output_path) as pdf:
        fig, axs = plt.subplots(2, 1, figsize=(15, 10), sharex=True, height_ratios=[1.2, 1.2])

        # 1. Plot absolute prices (Top plot)
        axs[0].plot(df.index, df["eu"], label=eu_label, linewidth=2, color="#2ecc71")
        axs[0].plot(df.index, df["us"], label=us_label, linewidth=2, color="#e74c3c", alpha=0.8)
        axs[0].set_title(f"Price Data — {name} (Absolute)", fontsize=16, pad=15)
        axs[0].set_ylabel("Price", fontsize=12)
        axs[0].legend(loc="best", fontsize=10)
        axs[0].grid(True, linestyle="--", alpha=0.4, which="both")
        axs[0].axvspan(
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['eu']['start']} UTC"),
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['eu']['end']} UTC"),
            color="green", alpha=0.1, label="EU Market Hours"
        )
        axs[0].axvspan(
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['us']['start']} UTC"),
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['us']['end']} UTC"),
            color="red", alpha=0.1, label="US Market Hours"
        )

        # 2. Plot normalized prices (Bottom plot)
        axs[1].plot(df.index, df["eu_norm"], label=eu_label, linewidth=2, color="#2ecc71")
        axs[1].plot(df.index, df["us_norm"], label=us_label, linewidth=2, color="#e74c3c", alpha=0.8)
        axs[1].set_title(f"Price Data — {name} (Normalized to 1)", fontsize=16, pad=15)
        axs[1].set_xlabel("Time (GMT)", fontsize=12)
        axs[1].set_ylabel("Normalized Price", fontsize=12)
        axs[1].legend(loc="best", fontsize=10)
        axs[1].grid(True, linestyle="--", alpha=0.4, which="both")
        axs[1].axvspan(
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['eu']['start']} UTC"),
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['eu']['end']} UTC"),
            color="green", alpha=0.1
        )
        axs[1].axvspan(
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['us']['start']} UTC"),
            pd.Timestamp(f"{df.index.date[0]} {MARKET_HOURS['us']['end']} UTC"),
            color="red", alpha=0.1
        )

        # Format x-axis for better readability
        fig.autofmt_xdate()

        # Save the plot to PDF
        pdf.savefig(fig)
        plt.close()
        print(f"✅ Plotted {name} data to {output_path}")

# Example usage for a single pair:
# plot_price_data('schibsted_vs_aapl', 'Schibsted (SCHA.OL)', 'Apple (AAPL)', 'data/schibsted_vs_aapl_intraday.csv', 'plots/schibsted_vs_aapl.pdf')

