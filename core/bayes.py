import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import invgamma, norm
from datetime import datetime, timedelta
import os
import sys
import pandas as pd
import seaborn as sns

# Load BuyPolar Capital plotting theme
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/plotting')))
from plotting import set_bpc_style
set_bpc_style()

# Assets: (ticker, asset type, fallback strike)
assets = [
    ("BTC-USD", "Crypto", 50000),
    ("SPY", "ETF", 450),
    ("TSLA", "Stock", 200),
    ("GLD", "Commodity ETF", 190),
    ("MSFT", "Tech Stock", 300),  # Optional fallback
]

# Parameters
end = datetime.today()
start = end - timedelta(days=365)
r = 0.02
T = 0.5
n_samples = 1000
alpha_0 = 2.0
beta_0 = 0.0005

# Output
os.makedirs("plots", exist_ok=True)
pdf = PdfPages("plots/bayesian_volatility_report.pdf")

def bs_call_price(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

summary_data = []
posterior_samples_dict = {}

for ticker, asset_type, fallback_strike in assets:
    try:
        df = yf.download(ticker, start=start, end=end)
        print(f"✅ {ticker} — downloaded {len(df)} rows")
        if df.empty or 'Close' not in df:
            raise ValueError(f"No data for {ticker}")

        prices = df['Close'].dropna()
        returns = np.log(prices / prices.shift(1)).dropna()

        # Posterior
        n = len(returns)
        alpha_n = alpha_0 + n / 2
        beta_n = beta_0 + 0.5 * np.sum(returns ** 2, axis=0)
        sigma2_samples = invgamma.rvs(a=alpha_n, scale=beta_n, size=n_samples)
        sigma_samples = np.sqrt(sigma2_samples)
        posterior_samples_dict[ticker] = sigma_samples

        # Summary stats
        summary_data.append({
            "Ticker": ticker,
            "Asset Type": asset_type,
            "Mean Vol": np.mean(sigma_samples),
            "Std Dev": np.std(sigma_samples),
            "Median": np.median(sigma_samples),
            "5th %ile": np.percentile(sigma_samples, 5),
            "95th %ile": np.percentile(sigma_samples, 95)
        })

        # Black-Scholes
        S = prices.iloc[-1]
        K = S if asset_type != "Option" else fallback_strike
        bs_prices = [bs_call_price(S, K, T, r, sigma) for sigma in sigma_samples]

        # Plot
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        ax[0].hist(sigma_samples, bins=40, color="#a6cee3", edgecolor="#333333")
        ax[0].set_title("Posterior Volatility Distribution")
        ax[0].set_xlabel("Volatility (σ)")
        ax[0].set_ylabel("Frequency")

        ax[1].hist(bs_prices, bins=40, color="#fb9a99", edgecolor="#333333")
        ax[1].set_title("Bayesian Black-Scholes Price Distribution")
        ax[1].set_xlabel("Call Option Price")
        ax[1].set_ylabel("Frequency")

        fig.suptitle(f"{ticker} — {asset_type}\nPeriod: {start.date()} to {end.date()}", fontsize=16)
        fig.text(0.01, 0.01, "Source: Yahoo Finance | Strategy: BuyPolar Capital",
                 fontsize=9, style="italic", color="#333333")
        fig.tight_layout(rect=[0, 0.02, 1, 0.95])

        pdf.savefig(fig)
        plt.close(fig)

    except Exception as e:
        print(f"⚠️ Error with {ticker}: {e}")

# === Summary Table ===
if summary_data:
    df_summary = pd.DataFrame(summary_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")
    table = ax.table(
        cellText=np.round(df_summary.iloc[:, 2:].values, 4),
        colLabels=df_summary.columns[2:],
        rowLabels=[f"{row['Ticker']} ({row['Asset Type']})" for _, row in df_summary.iterrows()],
        loc="center",
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.5)
    ax.set_title("Summary of Posterior Volatility Statistics", fontsize=16, pad=20)
    pdf.savefig(fig)
    plt.close(fig)

# === Posterior KDE Plot ===
fig, ax = plt.subplots(figsize=(12, 6))
for ticker, samples in posterior_samples_dict.items():
    sns.kdeplot(samples, label=ticker, linewidth=2)
ax.set_title("Posterior Volatility KDEs (per asset)", fontsize=14)
ax.set_xlabel("Volatility (σ)")
ax.set_ylabel("Density")
ax.legend()
fig.text(0.01, 0.01, "Source: Posterior KDE | Strategy: BuyPolar Capital",
         fontsize=9, style="italic", color="#333333")
fig.tight_layout(rect=[0, 0.02, 1, 0.95])
pdf.savefig(fig)
plt.close(fig)

pdf.close()
print("✅ Bayesian volatility report saved to: plots/bayesian_volatility_report.pdf")
