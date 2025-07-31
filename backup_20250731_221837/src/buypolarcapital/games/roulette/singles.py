import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

# --- Setup ---
n_simulations = 10000
n_spins = 500
initial_bankroll = 100
bet_amount = 1
os.makedirs("plots", exist_ok=True)

# --- Define Bets ---
bets = [
    {"name": "Single Number", "win_prob": 1/37, "payout": 35},
    {"name": "Red", "win_prob": 18/37, "payout": 1},
    {"name": "Black", "win_prob": 18/37, "payout": 1},
    {"name": "Even", "win_prob": 18/37, "payout": 1},
    {"name": "Odd", "win_prob": 18/37, "payout": 1},
    {"name": "Low (1–18)", "win_prob": 18/37, "payout": 1},
    {"name": "High (19–36)", "win_prob": 18/37, "payout": 1},
    {"name": "Dozen (1–12)", "win_prob": 12/37, "payout": 2},
    {"name": "Dozen (13–24)", "win_prob": 12/37, "payout": 2},
    {"name": "Dozen (25–36)", "win_prob": 12/37, "payout": 2},
    {"name": "Column 1", "win_prob": 12/37, "payout": 2},
    {"name": "Column 2", "win_prob": 12/37, "payout": 2},
    {"name": "Column 3", "win_prob": 12/37, "payout": 2},
]

# --- Helper Function ---
def simulate_bet(win_prob, payout):
    final_bankrolls = np.zeros(n_simulations)
    busts = 0
    for i in range(n_simulations):
        bankroll = initial_bankroll
        for _ in range(n_spins):
            if bankroll <= 0:
                busts += 1
                break
            outcome = np.random.rand()
            if outcome < win_prob:
                bankroll += payout * bet_amount
            else:
                bankroll -= bet_amount
        final_bankrolls[i] = bankroll
    return final_bankrolls, busts / n_simulations

# --- Simulation & Plotting ---
pdf_path = "plots/roulette_bet_comparison.pdf"
with PdfPages(pdf_path) as pdf:
    for bet in bets:
        final_bankrolls, bust_rate = simulate_bet(bet["win_prob"], bet["payout"])
        mean_final = final_bankrolls.mean()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(final_bankrolls, bins=50, edgecolor='black', alpha=0.75)
        ax.axvline(initial_bankroll, color='red', linestyle='--', label='Starting Bankroll')
        ax.set_title(f"{bet['name']} | Payout {bet['payout']}:1 | Win Prob {bet['win_prob']:.2%}\nBust Rate = {bust_rate:.2%}, Mean Final = {mean_final:.2f}")
        ax.set_xlabel("Final Bankroll")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

print(f"✔️ Merged PDF saved to {pdf_path}")
