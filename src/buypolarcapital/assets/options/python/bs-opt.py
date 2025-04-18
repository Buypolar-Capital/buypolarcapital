import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === Black-Scholes Formula ===
def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# === Setup ===
ticker_symbol = "AAPL"
ticker = yf.Ticker(ticker_symbol)
spot = ticker.history(period="1d")["Close"].iloc[-1]
options_dates = ticker.options
expiry = options_dates[0]
opt_chain = ticker.option_chain(expiry)
calls = opt_chain.calls.copy()

# === Fill missing IVs ===
calls["impliedVolatility"] = calls["impliedVolatility"].fillna(0.25)

# === Risk-free rate and T ===
r = 0.05
T = (pd.to_datetime(expiry) - datetime.today()).days / 365

# === Calculate BS prices ===
calls["BS_Price"] = calls.apply(
    lambda row: black_scholes_price(
        spot, row["strike"], T, r, row["impliedVolatility"], option_type="call"
    ),
    axis=1
)

# === Mid-market price ===
calls["Market_Price"] = (calls["bid"] + calls["ask"]) / 2
calls["Diff"] = calls["Market_Price"] - calls["BS_Price"]

# === Get AAPL price history ===
history = ticker.history(period="1mo")
history = history.reset_index()

# === PLOTTING ===
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=False, gridspec_kw={'height_ratios': [1, 1.2]})
fig.suptitle(f"{ticker_symbol} — Black-Scholes vs Market Pricing\nExpiry: {expiry}", fontsize=16, fontweight='bold')

# --- Top: AAPL Stock History ---
ax1.plot(history["Date"], history["Close"], label="AAPL Close", color="blue")
ax1.axhline(y=spot, color="gray", linestyle="--", label=f"Spot Price (${spot:.2f})")
ax1.set_ylabel("Stock Price ($)")
ax1.legend()
ax1.grid(True)

# --- Bottom: Option Prices ---
ax2.plot(calls["strike"], calls["Market_Price"], label="Market Price", marker="o")
ax2.plot(calls["strike"], calls["BS_Price"], label="BS Price", marker="x")

# Annotate spot price
ax2.axvline(spot, color="gray", linestyle="--", linewidth=1)
ax2.annotate(f"Spot = ${spot:.2f}", xy=(spot, ax2.get_ylim()[1]*0.95),
             xytext=(spot + 2, ax2.get_ylim()[1]*0.9),
             arrowprops=dict(arrowstyle="->", lw=1), fontsize=10)

# Shade ITM/OTM regions
ax2.axvspan(0, spot, alpha=0.08, color="green", label="In the Money (ITM)")
ax2.axvspan(spot, calls["strike"].max(), alpha=0.05, color="red", label="Out of the Money (OTM)")

ax2.set_xlabel("Strike Price ($)")
ax2.set_ylabel("Option Price ($)")
ax2.legend()
ax2.grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# === Save to PDF ===
os.makedirs("plots", exist_ok=True)
pdf_path = f"plots/bs-opt-{expiry}.pdf"
plt.savefig(pdf_path)
plt.show()

print(f"✅ Saved: {pdf_path}")
