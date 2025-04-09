import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_price_data(name, eu_label, us_label, data_path, output_path):
    df = pd.read_csv(data_path, index_col=0, parse_dates=True)

    # Plot the absolute prices
    with PdfPages(output_path) as pdf:
        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(df.index, df["eu"], label=eu_label, linewidth=1.5)
        ax.plot(df.index, df["us"], label=us_label, linewidth=1.5)

        ax.set_title(f"Price Data — {name}")
        ax.set_xlabel("Time (GMT)")
        ax.set_ylabel("Price")
        ax.legend()
        ax.grid(True)

        # Format x-axis for better readability
        fig.autofmt_xdate()

        # Save the plot to PDF
        pdf.savefig(fig)
        plt.close()
        print(f"✅ Plotted {name} data to {output_path}")

# Example usage for a single pair:
# plot_price_data('schibsted_vs_aapl', 'Schibsted (SCHA.OL)', 'Apple (AAPL)', 'data/schibsted_vs_aapl_intraday.csv', 'plots/schibsted_vs_aapl.pdf')
