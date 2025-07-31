import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
import sys

# === BPC PLOTTING STYLE ===
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root / 'src'))
from plotting.plotting import set_bpc_style
set_bpc_style()

# === CONFIG ===
tickers = ['SAP.DE', 'SIE.DE', 'DTE.DE']
start_price_target_pct = 1.10  # 10% up-move target
num_simulations = 500
max_days = 500
start_price_method = 'last_close'  # or 'mean'

# === DATA FETCH ===
data = {
    ticker: yf.download(ticker, start='2020-01-01', end='2025-01-01')
    for ticker in tickers
}
returns = {
    ticker: data[ticker]['Close'].pct_change().dropna()
    for ticker in tickers
}

# === OUTPUT PATH ===
pdf_dir = Path(__file__).parent / "plots"
pdf_dir.mkdir(exist_ok=True)
pdf_path = pdf_dir / "bpc_hitting_times_report.pdf"
pdf = PdfPages(pdf_path)

# === PAGE 1: RETURN PLOTS (not overlapping) ===
for ticker in tickers:
    fig, ax = plt.subplots()
    ax.plot(returns[ticker], color='black')
    ax.set_title(f'Daily Returns: {ticker}')
    ax.set_ylabel('Return')
    ax.set_xlabel('Date')
    pdf.savefig(fig)
    plt.close(fig)

# === FUNCTION: GBM hitting time sim ===
def simulate_hitting_time(S0, mu, sigma, S_target, max_days, n_sim=1000):
    dt = 1 / 252
    hitting_times = []

    for _ in range(n_sim):
        S = float(S0)  # ensure float
        for t in range(1, max_days + 1):
            Z = np.random.normal()
            S *= np.exp((mu - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)
            if S >= S_target:  # S and S_target are now floats
                hitting_times.append(t)
                break
        else:
            hitting_times.append(np.nan)  # did not hit

    return np.array(hitting_times)

# === PAGE 2+: HITTING TIME HISTOGRAMS ===
for ticker in tickers:
    prices = data[ticker]['Close'].dropna()
    log_returns = np.log(prices / prices.shift(1)).dropna()
    mu = float((log_returns.mean() * 252).iloc[0])  # use iloc[0] to get scalar
    sigma = float((log_returns.std() * np.sqrt(252)).iloc[0])  # use iloc[0] to get scalar

    if start_price_method == 'last_close':
        S0 = float(prices.iloc[-1])  # iloc[-1] is already a scalar
    else:
        S0 = float(prices.mean().iloc[0])  # use iloc[0] for mean
    S_target = float(S0 * start_price_target_pct)  # ensure S_target is a float

    hitting_times = simulate_hitting_time(S0, mu, sigma, S_target, max_days, num_simulations)
    theo_hitting_time = np.log(S_target / S0) / mu if mu > 0 else np.nan

    fig, ax = plt.subplots()
    ax.hist(hitting_times[~np.isnan(hitting_times)], bins=30, color='black', alpha=0.8)
    if mu > 0:
        ax.axvline(theo_hitting_time, color='red', linestyle='--',
                   label=f"Theoretical: {theo_hitting_time:.1f} days")
    ax.set_title(f"Hitting Time Distribution: {ticker}")
    ax.set_xlabel("Days to hit 10% gain")
    ax.set_ylabel("Frequency")
    ax.legend()
    pdf.savefig(fig)
    plt.close(fig)

# === SAVE PDF ===
pdf.close()
print(f"✅ Saved hitting time report to: {pdf_path}")