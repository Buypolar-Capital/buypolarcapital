import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from pathlib import Path
from matplotlib import font_manager

# Optional: Windows emoji font
emoji_font_path = "C:/Windows/Fonts/seguisym.ttf"
if os.path.exists(emoji_font_path):
    emoji_font = font_manager.FontProperties(fname=emoji_font_path)
    plt.rcParams['font.family'] = emoji_font.get_name()

# BuyPolar Capital plotting style
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

# --- Simulation Parameters ---
initial_capital = 1_000_000
leverage = 10.0
mu = -0.0002
sigma = 0.04
days = 1000
simulations = 500

# --- Data Containers ---
equity_curves = []
days_to_bust = []
final_equities = []

for _ in range(simulations):
    returns = np.random.normal(mu, sigma, size=days)
    equity = initial_capital
    equity_curve = []

    for i, r in enumerate(returns):
        exposure = equity * leverage
        pnl = exposure * r
        equity += pnl
        equity_curve.append(equity)
        if equity <= 0:
            days_to_bust.append(i)
            break

    equity_curves.append(equity_curve)
    if equity > 0:
        final_equities.append(equity)

# --- Plot 1: Equity curves ---
fig1, ax1 = plt.subplots(figsize=(12, 6))
for curve in equity_curves:
    ax1.plot(curve, color='gray', alpha=0.1)
ax1.set_title(f'💥 Monte Carlo: {simulations} Simulations (Leverage x{leverage})\nBankruptcies: {len(days_to_bust)}')
ax1.set_xlabel("Days")
ax1.set_ylabel("Equity ($)")
ax1.axhline(initial_capital, color='black', linestyle='--', linewidth=0.8, label="Initial Capital")
ax1.legend()
fig1.tight_layout()

# --- Plot 2: Days to Bust ---
fig2, ax2 = plt.subplots(figsize=(10, 5))
if days_to_bust:
    ax2.hist(days_to_bust, bins=30, color='red', edgecolor='black')
    ax2.set_title("📉 Histogram of Days to Bankruptcy")
    ax2.set_xlabel("Days until fund blows up")
    ax2.set_ylabel("Number of simulations")
else:
    ax2.text(0.5, 0.5, "No bankruptcies occurred", ha='center', va='center', fontsize=14)
    ax2.axis('off')
fig2.tight_layout()

# --- Plot 3: Final Equity of Survivors ---
fig3, ax3 = plt.subplots(figsize=(10, 5))
if final_equities:
    ax3.hist(final_equities, bins=30, color='green', edgecolor='black')
    ax3.set_title("💰 Final Equity of Survivors")
    ax3.set_xlabel("Final Equity ($)")
    ax3.set_ylabel("Number of surviving simulations")
else:
    ax3.text(0.5, 0.5, "No survivors", ha='center', va='center', fontsize=14)
    ax3.axis('off')
fig3.tight_layout()

# --- Export all to multi-page PDF ---
output_dir = Path.cwd() / "plots"
output_dir.mkdir(parents=True, exist_ok=True)
report_path = output_dir / "montecarlo_report.pdf"

with PdfPages(report_path) as pdf:
    pdf.savefig(fig1)
    pdf.savefig(fig2)
    pdf.savefig(fig3)

print(f"✅ Multi-page PDF saved to: {report_path}")
