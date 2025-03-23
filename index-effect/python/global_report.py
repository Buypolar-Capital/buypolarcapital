

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

# Ensure plots directory exists
os.makedirs("plots", exist_ok=True)

# Indexes to include
indexes = {
    "OSEBX": "^OSEAX",
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI"
}

start_date = "2020-01-01"

# Create the PDF writer
with PdfPages("plots/global_index_report.pdf") as pdf:
    for name, ticker in indexes.items():
        print(f"Fetching data for {name} ({ticker})...")
        data = yf.download(ticker, start=start_date)

        if data.empty or 'Close' not in data.columns:
            print(f"⚠️ No data or missing 'Close' for {ticker}")
            continue

        latest_date = data.index[-1].strftime('%Y-%m-%d')
        latest_price = float(data['Close'].iloc[-1])

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label=f"{name} Index Level", linewidth=2)
        plt.title(f"{name} Index Level since 2020", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Index Level")
        plt.grid(True)
        plt.tight_layout()

        # Annotate last point
        plt.annotate(f"{latest_date}\n{latest_price:.2f}",
                     xy=(data.index[-1], latest_price),
                     xytext=(-100, -100),
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

        plt.legend()
        pdf.savefig()
        plt.close()

print("✅ Global index report saved to: plots/global_index_report.pdf")
