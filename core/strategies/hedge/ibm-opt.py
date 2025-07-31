import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.backends.backend_pdf import PdfPages
import os

# === SETUP ===
os.makedirs("plots", exist_ok=True)

# === FETCH IBM DATA ===
stock = yf.Ticker("IBM")
hist = stock.history(period="3mo", interval="1d")  # More granular daily data over 3 months
hist = hist.reset_index()
hist = hist.tail(30)  # Use only the last 30 trading days

# === BLACK-SCHOLES PRICING ===
def black_scholes(S, K, T, r, sigma, option_type="call"):
    if T == 0 or sigma == 0:
        return max(S - K, 0) if option_type == "call" else max(K - S, 0)
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r*T) * norm.cdf(d2)
    else:
        return K * np.exp(-r*T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# === DEFINE PARAMETERS ===
r = 0.02
sigma = 0.25
T_total = 30 / 365  # 30-day maturity
K = round(hist['Close'].iloc[0])

# === INITIAL PRICES ===
S0 = hist['Close'].iloc[0]
call_price = black_scholes(S0, K, T_total, r, sigma, "call")
put_price = black_scholes(S0, K, T_total, r, sigma, "put")
synthetic_stock = call_price - put_price + K * np.exp(-r * T_total)

# === SIMULATE OVER 1 MONTH OF REAL DATA ===
stock_prices = []
call_values = []
put_values = []
portfolio_values = []

dates = hist['Date']

for i in range(len(hist)):
    S_t = hist['Close'].iloc[i]
    days_remaining = (len(hist) - i - 1)
    T_t = max(days_remaining / 365, 1e-5)

    call_t = black_scholes(S_t, K, T_t, r, sigma, "call")
    put_t = black_scholes(S_t, K, T_t, r, sigma, "put")
    bond_t = K * np.exp(-r * T_t)
    portfolio_value = S_t - call_t + put_t + bond_t

    stock_prices.append(S_t)
    call_values.append(call_t)
    put_values.append(put_t)
    portfolio_values.append(portfolio_value)

# === PLOT RESULTS ===
with PdfPages("plots/ibm_neutral_portfolio.pdf") as pdf:
    fig, axs = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    axs[0].plot(dates, stock_prices, label="IBM Stock", color='black')
    axs[0].set_ylabel("Stock Price")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(dates, call_values, label="Call Option (ATM)", color='blue')
    axs[1].set_ylabel("Call Value")
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(dates, put_values, label="Put Option (ATM)", color='green')
    axs[2].set_ylabel("Put Value")
    axs[2].legend()
    axs[2].grid(True)

    axs[3].plot(dates, portfolio_values, label="Portfolio Value", color='purple', linewidth=2)
    axs[3].axhline(y=portfolio_values[0], color='gray', linestyle='--', label=f"Initial ≈ {portfolio_values[0]:.2f} USD")
    axs[3].set_xlabel("Date")
    axs[3].set_ylabel("Portfolio Value")
    axs[3].legend()
    axs[3].grid(True)

    plt.suptitle("IBM Synthetic Delta-Neutral Portfolio (Real Data, 1 Month)", fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    pdf.savefig()
    plt.close()

    # Explanatory page
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    text = (
        f"IBM initial stock price: ${S0:.2f}\n"
        f"Strike price (K): ${K}\n"
        f"Call price: ${call_price:.2f}\n"
        f"Put price: ${put_price:.2f}\n"
        f"Synthetic stock (Call - Put + Bond): ${synthetic_stock:.2f}\n"
        f"\n"
        f"Portfolio Construction:\n"
        f"  +1 IBM Stock\n"
        f"  -1 Call Option (ATM)\n"
        f"  +1 Put Option (ATM)\n"
        f"  +1 Zero-Coupon Bond (value = K * exp(-rT))\n"
        f"\n"
        f"This creates a delta-neutral portfolio that maintains a stable value\n"
        f"even as the stock fluctuates, visualized over the last month of real prices."
    )
    plt.text(0, 0.5, text, fontsize=12, verticalalignment='center')
    pdf.savefig()
    plt.close()