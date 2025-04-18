import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import norm
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

# === Binomial Model ===
def binomial_price(S, K, T, r, sigma, option_type="call", steps=100):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    disc = np.exp(-r * dt)

    prices = np.asarray([S * u**j * d**(steps - j) for j in range(steps + 1)])
    if option_type == "call":
        values = np.maximum(0, prices - K)
    else:
        values = np.maximum(0, K - prices)

    for i in range(steps - 1, -1, -1):
        values = disc * (p * values[1:i+2] + (1 - p) * values[0:i+1])
    return values[0]

# === Heston Model Approximation (simplified) ===
def heston_approx_price(S, K, T, r, sigma, option_type="call"):
    v0 = sigma**2
    return black_scholes_price(S, K, T, r, np.sqrt(v0), option_type)

# === GARCH-vol Black-Scholes Approximation ===
def garch_vol_price(S, K, T, r, sigma, option_type="call"):
    garch_vol = sigma * 1.2  # placeholder for actual GARCH forecast
    return black_scholes_price(S, K, T, r, garch_vol, option_type)

# === Mispricing P&L function ===
def option_pnl(S0, K, r, T, option_type, model_price, market_price):
    if option_type == "call":
        payoff = max(S0 - K, 0)
    else:
        payoff = max(K - S0, 0)
    return payoff - market_price

# === BuyPolar Plot Style ===
def set_bpc_style():
    plt.rcParams.update({
        "axes.edgecolor": "#cccccc",
        "axes.grid": True,
        "grid.color": "#cccccc",
        "grid.linestyle": "-",
        "grid.linewidth": 0.25,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
    })

set_bpc_style()

# === Tickers ===
stocks = {
    "AAPL": "USA", "EQNR": "Norway", "SHEL": "UK", "SONY": "Japan", "SAP": "Germany",
    "LVMUY": "France", "SHOP": "Canada", "TCEHY": "China", "INFY": "India", "PBR": "Brazil"
}

# === Model Map ===
models = {
    "Black-Scholes": black_scholes_price,
    "Binomial": binomial_price,
    "Heston": heston_approx_price,
    "GARCH": garch_vol_price
}

r = 0.05
output_dir = os.path.join(os.getcwd(), "plots")
os.makedirs(output_dir, exist_ok=True)

for model_name, model_func in models.items():
    pdf_path = os.path.join(output_dir, f"global_{model_name.lower().replace('-', '').replace(' ', '')}_market_pnl.pdf")
    leaderboard = []

    with PdfPages(pdf_path) as pdf:
        for ticker, country in stocks.items():
            try:
                yf_ticker = yf.Ticker(ticker)
                options = yf_ticker.options
                if not options:
                    raise Exception("No options available")

                spot = yf_ticker.history(period="1d")["Close"].iloc[-1]
                expiry = options[0]
                T = (pd.to_datetime(expiry) - datetime.today()).days / 365
                chain = yf_ticker.option_chain(expiry)
                history = yf_ticker.history(period="1mo").reset_index()

                for option_type, df in zip(["call", "put"], [chain.calls, chain.puts]):
                    df["impliedVolatility"] = df["impliedVolatility"].fillna(0.25)
                    df["Market_Price"] = (df["bid"] + df["ask"]) / 2

                    df["Model_Price"] = df.apply(
                        lambda row: model_func(
                            spot, row["strike"], T, r, row["impliedVolatility"], option_type
                        ), axis=1
                    )
                    df["PnL"] = df.apply(
                        lambda row: option_pnl(spot, row["strike"], r, T, option_type,
                                               row["Model_Price"], row["Market_Price"]), axis=1
                    )

                    avg_pnl = df["PnL"].mean()
                    total_pnl = df["PnL"].sum()
                    leaderboard.append({
                        "Ticker": ticker,
                        "Country": country,
                        "Type": option_type,
                        "Model": model_name,
                        "AvgPnL": avg_pnl,
                        "TotalPnL": total_pnl
                    })

                    fig, axes = plt.subplots(3, 1, figsize=(12, 10),
                                             gridspec_kw={"height_ratios": [1, 1.2, 1.1]})
                    fig.suptitle(f"{ticker} ({country}) — {option_type.upper()}S\nExpiry: {expiry} — Model: {model_name}",
                                 fontsize=15, fontweight="bold")

                    axes[0].plot(history["Date"], history["Close"], color="blue", label="Price")
                    axes[0].axhline(spot, linestyle="--", color="gray", label=f"Spot = ${spot:.2f}")
                    axes[0].set_ylabel("Stock Price ($)")
                    axes[0].legend()
                    axes[0].grid(True)

                    axes[1].plot(df["strike"], df["Market_Price"], label="Market", marker="o")
                    axes[1].plot(df["strike"], df["Model_Price"], label=f"{model_name}", marker="x")
                    axes[1].axvline(spot, color="gray", linestyle="--", linewidth=1)
                    axes[1].set_xlabel("Strike")
                    axes[1].set_ylabel("Option Price ($)")
                    axes[1].set_title("Market vs Model Pricing")
                    axes[1].legend()
                    axes[1].grid(True)

                    axes[2].bar(df["strike"], df["PnL"], color="green" if option_type == "call" else "purple")
                    axes[2].axhline(0, color="black", linewidth=0.7)
                    axes[2].set_xlabel("Strike")
                    axes[2].set_ylabel("PnL ($)")
                    axes[2].set_title("PnL if Held to Expiry (Model-Based Strategy)")
                    axes[2].grid(True)

                    fig.text(0.01, 0.01, f"Source: Yahoo Finance | Strategy: BuyPolar Capital",
                             fontsize=9, style="italic", color="#333333")

                    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
                    pdf.savefig(fig)
                    plt.close()

                    print(f"✅ [{model_name}] Added {ticker} ({country}) {option_type}s to report.")

            except Exception as e:
                print(f"❌ [{model_name}] Skipped {ticker} ({country}): {e}")

    print(f"\n📊 {model_name} PnL Leaderboard:")
    leader_df = pd.DataFrame(leaderboard)
    leader_df = leader_df.sort_values(by="TotalPnL", ascending=False)
    print(leader_df[["Ticker", "Country", "Type", "Model", "AvgPnL", "TotalPnL"]].round(2).to_string(index=False))

    print(f"\n📄 {model_name} PDF saved to: {pdf_path}")
