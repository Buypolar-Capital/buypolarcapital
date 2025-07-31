

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ticker = "^DJI"  # Dow Jones Industrial Average
start_date = "2020-01-01"

data = yf.download(ticker, start=start_date)

if data.empty:
    print("No data retrieved.")
    exit()

if 'Close' not in data.columns:
    raise ValueError("No 'Close' column found!")

latest_date = data.index[-1].strftime('%Y-%m-%d')
latest_price = float(data['Close'].iloc[-1])

plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label="Dow Jones Index Level", linewidth=2)
plt.title("Dow Jones Index Level since 2020", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Index Level")
plt.grid(True)
plt.tight_layout()

plt.annotate(f"{latest_date}\n{latest_price:.2f}",
             xy=(data.index[-1], latest_price),
             xytext=(-100, -100),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', lw=1.5),
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))

plt.legend()

output_path = "plots/dowjones_monitor.pdf"
with PdfPages(output_path) as pdf:
    pdf.savefig()
    plt.close()

print(f"✅ Saved plot to {output_path}")
