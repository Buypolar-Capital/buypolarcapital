import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import os
from pathlib import Path
from itertools import product

# === BuyPolar Plot Style ===
def set_bpc_style():
    plt.rcParams.update({
        "axes.edgecolor": "#cccccc",
        "axes.grid": True,
        "grid.color": "#cccccc",
        "grid.linestyle": "-",
        "grid.linewidth": 0.25,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
    })

set_bpc_style()

# === Params ===
initial_capital = 1_000_000
days = 500
simulations_per_setting = 100

leverage_grid = [3, 5, 10]
mu_grid = [0.0002, 0.0, -0.0002]
sigma_grid = [0.02, 0.04, 0.06]

# === Track summary stats ===
heatmaps = {
    "bankrupt_pct": {},
    "avg_days_to_bust": {},
    "mean_final_equity": {},
    "std_final_equity": {},
    "avg_max_drawdown": {}
}

pdf_pages = []

def compute_drawdown(equity_curve):
    peak = equity_curve[0]
    max_dd = 0
    for val in equity_curve:
        if val > peak:
            peak = val
        dd = (peak - val) / peak
        max_dd = max(max_dd, dd)
    return max_dd

# === Simulation Loop ===
for leverage, mu, sigma in product(leverage_grid, mu_grid, sigma_grid):
    label = f"L{leverage}_mu{mu:.4f}_sigma{sigma:.2f}"
    all_curves = []
    days_to_bust = []
    final_equities = []
    drawdowns = []

    for _ in range(simulations_per_setting):
        returns = np.random.normal(mu, sigma, size=days)
        equity = initial_capital
        curve = []

        for i, r in enumerate(returns):
            exposure = equity * leverage
            pnl = exposure * r
            equity += pnl
            curve.append(equity)
            if equity <= 0:
                days_to_bust.append(i)
                break

        all_curves.append(curve)
        if equity > 0:
            final_equities.append(equity)
        drawdowns.append(compute_drawdown(curve))

    # Summary stats
    busts = len(days_to_bust)
    survivors = simulations_per_setting - busts
    heatmaps["bankrupt_pct"][label] = 100 * busts / simulations_per_setting
    heatmaps["avg_days_to_bust"][label] = np.mean(days_to_bust) if busts > 0 else 0
    heatmaps["mean_final_equity"][label] = np.mean(final_equities) if survivors > 0 else 0
    heatmaps["std_final_equity"][label] = np.std(final_equities) if survivors > 0 else 0
    heatmaps["avg_max_drawdown"][label] = np.mean(drawdowns)

    # === Pages 1-3 for each setting ===
    fig1, ax = plt.subplots(figsize=(10, 4))
    for curve in all_curves:
        ax.plot(curve, alpha=0.1, color="gray")
    ax.set_title(f"[{label}] Equity Curves ({simulations_per_setting} sims)")
    ax.axhline(initial_capital, linestyle="--", color="black", linewidth=0.8)
    pdf_pages.append(fig1)

    fig2, ax = plt.subplots(figsize=(6, 4))
    if busts > 0:
        ax.hist(days_to_bust, bins=30, color="red", edgecolor="black")
        ax.set_title("Days to Bust")
    else:
        ax.text(0.5, 0.5, "No bankruptcies", ha="center", va="center")
        ax.axis("off")
    pdf_pages.append(fig2)

    fig3, ax = plt.subplots(figsize=(6, 4))
    if survivors > 0:
        ax.hist(final_equities, bins=30, color="green", edgecolor="black")
        ax.set_title("Final Equity (Survivors)")
    else:
        ax.text(0.5, 0.5, "No survivors", ha="center", va="center")
        ax.axis("off")
    pdf_pages.append(fig3)

# === Heatmap Helper ===
def plot_heatmap(data, title, cmap="viridis"):
    fig, ax = plt.subplots(figsize=(9, 6))
    matrix = np.zeros((len(leverage_grid), len(mu_grid) * len(sigma_grid)))
    xticklabels = []
    for i, lev in enumerate(leverage_grid):
        for j, mu in enumerate(mu_grid):
            for k, sigma in enumerate(sigma_grid):
                col = j * len(sigma_grid) + k
                key = f"L{lev}_mu{mu:.4f}_sigma{sigma:.2f}"
                val = data.get(key, 0)
                matrix[i, col] = val
                xticklabels.append(f"μ={mu:.4f}\nσ={sigma:.2f}") if i == 0 else None

    sns.heatmap(matrix, annot=True, fmt=".1f", cmap=cmap, xticklabels=xticklabels[:len(mu_grid)*len(sigma_grid)],
                yticklabels=[f"L={l}" for l in leverage_grid], ax=ax)
    ax.set_title(title)
    plt.tight_layout()
    return fig

# === Heatmap Pages (4-8) ===
pdf_pages.append(plot_heatmap(heatmaps["bankrupt_pct"], "🔥 % Bankruptcies", cmap="Reds"))
pdf_pages.append(plot_heatmap(heatmaps["avg_days_to_bust"], "⏳ Avg Days to Bust", cmap="Oranges"))
pdf_pages.append(plot_heatmap(heatmaps["mean_final_equity"], "💰 Mean Final Equity (Survivors)", cmap="Greens"))
pdf_pages.append(plot_heatmap(heatmaps["std_final_equity"], "📈 Std Dev of Final Equity", cmap="Blues"))
pdf_pages.append(plot_heatmap(heatmaps["avg_max_drawdown"], "📉 Avg Max Drawdown", cmap="Purples"))

# === Save as Multi-Page PDF ===
output_dir = Path.cwd() / "plots"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "grid_montecarlo_report.pdf"

with PdfPages(output_path) as pdf:
    for fig in pdf_pages:
        pdf.savefig(fig)
        plt.close(fig)

print(f"✅ Full PDF report saved to: {output_path}")
