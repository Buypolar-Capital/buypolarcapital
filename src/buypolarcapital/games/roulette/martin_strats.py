import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_pdf import PdfPages

# --- Parameters ---
n_simulations = 10000
n_spins = 300
initial_bankroll = 100
base_bet = 1
fraction = 0.05  # For fixed fraction strategy
p_red = 18 / 37
os.makedirs("plots", exist_ok=True)

# --- Define Strategies ---
def simulate_strategy(strategy_func, name):
    results = []
    busts = 0
    for _ in range(n_simulations):
        bankroll = initial_bankroll
        bet = base_bet
        for _ in range(n_spins):
            if bankroll < 1e-6 or bankroll < bet:
                busts += 1
                bankroll = 0
                break
            win = np.random.rand() < p_red
            bankroll, bet = strategy_func(bankroll, bet, win)
        results.append(bankroll)
    return np.array(results), busts / n_simulations

# --- Strategies ---
def martingale(bankroll, bet, win):
    if win:
        bankroll += bet
        bet = base_bet
    else:
        bankroll -= bet
        bet *= 2
    return bankroll, bet

def anti_martingale(bankroll, bet, win):
    if win:
        bankroll += bet
        bet *= 2
    else:
        bankroll -= bet
        bet = base_bet
    return bankroll, bet

def dalembert(bankroll, bet, win):
    if win:
        bankroll += bet
        bet = max(base_bet, bet - 1)
    else:
        bankroll -= bet
        bet += 1
    return bankroll, bet

def reverse_dalembert(bankroll, bet, win):
    if win:
        bankroll += bet
        bet += 1
    else:
        bankroll -= bet
        bet = max(base_bet, bet - 1)
    return bankroll, bet

def fixed_fraction(bankroll, bet, win):
    bet = max(1, int(fraction * bankroll))
    if win:
        bankroll += bet
    else:
        bankroll -= bet
    return bankroll, bet

def flat_bet(bankroll, bet, win):
    if win:
        bankroll += bet
    else:
        bankroll -= bet
    return bankroll, base_bet

# --- Strategy List ---
strategies = [
    ("Martingale", martingale),
    ("Anti-Martingale", anti_martingale),
    ("D’Alembert", dalembert),
    ("Reverse D’Alembert", reverse_dalembert),
    ("Fixed Fraction", fixed_fraction),
    ("Flat Bet", flat_bet),
]

# --- Plot and Save ---
pdf_path = "plots/roulette_advanced_strategies.pdf"
with PdfPages(pdf_path) as pdf:
    for name, func in strategies:
        results, bust_rate = simulate_strategy(func, name)
        mean_final = results.mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(results, bins=50, edgecolor='black', alpha=0.75)
        ax.axvline(initial_bankroll, color='red', linestyle='--', label='Initial')
        ax.set_title(f"{name} Strategy\nBust Rate: {bust_rate:.2%}, Mean Final: {mean_final:.2f}")
        ax.set_xlabel("Final Bankroll")
        ax.set_ylabel("Frequency")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

print(f"✅ Saved to {pdf_path}")
