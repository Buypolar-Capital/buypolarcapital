import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend suitable for headless environments

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
import os

# Ensure 'plots' directory exists
os.makedirs("plots", exist_ok=True)

# Force overwrite of existing report
pdf_path = "plots/global_index_report.pdf"
if os.path.exists(pdf_path):
    os.remove(pdf_path)

# Index tickers
indexes = {
    "OSEBX": "^OSEAX",
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC",
    "MSCI World": "URTH",
    "Emerging Markets": "EEM",
    "China": "MCHI",
    "Bitcoin": "BTC-USD"
}

start_date = "2020-01-01"
today = datetime.utcnow().date()

# Create the PDF report
with PdfPages(pdf_path) as pdf:
    for name, ticker in indexes.items():
        print(f"Fetching data for {name} ({ticker})...")
        data = yf.download(ticker, start=start_date, interval="1d", progress=False, threads=True)

        if data.empty or 'Close' not in data.columns:
            print(f"⚠️ No data or missing 'Close' for {ticker}")
            continue

        # Drop any missing values
        data = data[data['Close'].notna()]
        data.index = data.index.tz_localize(None)  # Remove timezone info

        # Get latest available date
        max_date = data.index.max().date()
        if (today - max_date).days > 1:
            print(f"⚠️ {name} data might be outdated — last available: {max_date}")

        latest_date = max_date.strftime('%Y-%m-%d')
        latest_price = data.loc[data.index.max(), 'Close'].iloc[0]

        # Plot index data
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close'], label=f"{name} Index Level", linewidth=2)
        plt.title(f"{name} Index Level since 2020", fontsize=16)
        plt.xlabel("Date")
        plt.ylabel("Index Level")
        plt.grid(True)
        plt.tight_layout()

        # Annotate latest point
        plt.annotate(f"{latest_date}\n{latest_price:.2f}",
                     xy=(data.index[-1], latest_price),
                     xytext=(-100, -100),
                     textcoords='offset points',
                     arrowprops=dict(arrowstyle='->', lw=1.5),
                     bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

        # Add generation timestamp (to force Git diff)
        timestamp = datetime.utcnow().strftime("Generated: %Y-%m-%d %H:%M UTC")
        plt.figtext(0.99, 0.01, timestamp, ha='right', fontsize=8)

        plt.legend()
        pdf.savefig()
        plt.close()

print("✅ Global index report saved to: plots/global_index_report.pdf")
