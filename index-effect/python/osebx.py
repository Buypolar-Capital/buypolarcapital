import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# Download OSEBX data using the Yahoo Finance ticker
ticker = "^OSEAX"  # OSEBX alternative on Yahoo (OSEAX = All Share Index)
start_date = "2020-01-01"

data = yf.download(ticker, start=start_date)

# Debug: Check what the data looks like
print("Columns:", data.columns)
print("Last rows:\n", data.tail())

# Ensure we have data
if data.empty:
    print("No data retrieved.")
    exit()

# Fix: Sometimes 'Close' isn't there or is multilevel
if 'Close' not in data.columns:
    raise ValueError("No 'Close' column found!")

# Get latest date and price (make sure it's a scalar)
latest_date = data.index[-1].strftime('%Y-%m-%d')
latest_price = data['Close'].iloc[-1]

# Debug print to confirm
print("Latest Date:", latest_date)
print("Latest Price Raw:", latest_price)
print("Latest Price Type:", type(latest_price))

# Make sure latest_price is a float
latest_price = float(latest_price)

# Plot
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Close'], label="OSEBX Index Level", linewidth=2)
plt.title("OSEBX Index Level since 2020", fontsize=16)
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

# Save as PDF
output_path = "osebx_monitor.pdf"
with PdfPages(output_path) as pdf:
    pdf.savefig()
    plt.close()

print(f"✅ Saved plot to {output_path}")
