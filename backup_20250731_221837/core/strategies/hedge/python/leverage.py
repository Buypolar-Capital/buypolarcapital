import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
from matplotlib import font_manager

# --- SETUP FONT TO SUPPORT EMOJIS (Windows-friendly) ---
emoji_font_path = "C:/Windows/Fonts/seguisym.ttf"  # Segoe UI Symbol
if os.path.exists(emoji_font_path):
    emoji_font = font_manager.FontProperties(fname=emoji_font_path)
    plt.rcParams['font.family'] = emoji_font.get_name()

# --- ADD BUYPOLAR PLOTTING STYLE ---
root = Path(__file__).resolve().parents[2]
sys.path.append(str(root / 'src' / 'plotting'))
from plotting import set_bpc_style
set_bpc_style()

# --- SIMULATION SETTINGS ---
initial_capital = 1_000_000
leverage = 5.0
days = 1000
np.random.seed(42)

mu_values = [0.0003, 0.0005, 0.0007, 0.0009]
sigma_values = [0.01, 0.015, 0.02, 0.025]

fig, axes = plt.subplots(4, 4, figsize=(16, 12))
axes = axes.flatten()

for i, mu in enumerate(mu_values):
    for j, sigma in enumerate(sigma_values):
        ax = axes[i * 4 + j]
        returns = np.random.normal(mu, sigma, size=days)
        equity = initial_capital
        equity_curve = []
        bust_day = None

        for day, r in enumerate(returns):
            exposure = equity * leverage
            pnl = exposure * r
            equity += pnl
            equity_curve.append(equity)
            if equity <= 0:
                bust_day = day
                break

        ax.plot(equity_curve, label=f'μ={mu:.4f}, σ={sigma:.3f}', zorder=1)
        if bust_day is not None:
            ax.scatter(bust_day, 0, color='red', s=30, zorder=2)

        ax.axhline(y=initial_capital, color='gray', linestyle='--', linewidth=0.5)
        ax.set_title(f'μ={mu:.4f}, σ={sigma:.3f}')
        ax.set_xticks([])
        ax.set_yticks([])

plt.suptitle('💼 Hedge Fund Equity Simulations with Varying μ and σ', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# --- EXPORT TO PLOTS FOLDER ---
output_dir = Path.cwd() / 'plots'
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / 'leverage_sim_grid.pdf'

plt.savefig(output_path, bbox_inches='tight')
print(f"✅ Saved 4×4 grid plot to: {output_path}")
