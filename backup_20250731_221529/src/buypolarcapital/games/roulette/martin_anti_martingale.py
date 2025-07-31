
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Parameters ---
n_simulations = 10000
n_spins = 300
initial_bankroll = 100
base_bet = 1
p_red = 18 / 37

# --- Martingale Strategy ---
def simulate_martingale():
    results = []
    busts = 0
    for _ in range(n_simulations):
        bankroll = initial_bankroll
        bet = base_bet
        for _ in range(n_spins):
            if bankroll < bet:
                busts += 1
                bankroll = 0
                break
            win = np.random.rand() < p_red
            if win:
                bankroll += bet
                bet = base_bet
            else:
                bankroll -= bet
                bet *= 2
        results.append(bankroll)
    return np.array(results), busts / n_simulations

# --- Anti-Martingale Strategy ---
def simulate_anti_martingale():
    results = []
    busts = 0
    for _ in range(n_simulations):
        bankroll = initial_bankroll
        bet = base_bet
        for _ in range(n_spins):
            if bankroll < bet:
                busts += 1
                bankroll = 0
                break
            win = np.random.rand() < p_red
            if win:
                bankroll += bet
                bet *= 2
            else:
                bankroll -= bet
                bet = base_bet
        results.append(bankroll)
    return np.array(results), busts / n_simulations

# --- Run Simulations ---
martingale_results, martingale_bust = simulate_martingale()
anti_results, anti_bust = simulate_anti_martingale()

# --- Plot ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Martingale
axes[0].hist(martingale_results, bins=50, color='skyblue', edgecolor='black')
axes[0].axvline(initial_bankroll, color='red', linestyle='--', label='Initial')
axes[0].set_title(f"Martingale Strategy\nBust Rate: {martingale_bust:.2%}")
axes[0].set_xlabel("Final Bankroll")
axes[0].set_ylabel("Frequency")
axes[0].grid(True, linestyle='--', alpha=0.5)
axes[0].legend()

# Anti-Martingale
axes[1].hist(anti_results, bins=50, color='lightgreen', edgecolor='black')
axes[1].axvline(initial_bankroll, color='red', linestyle='--', label='Initial')
axes[1].set_title(f"Anti-Martingale Strategy\nBust Rate: {anti_bust:.2%}")
axes[1].set_xlabel("Final Bankroll")
axes[1].grid(True, linestyle='--', alpha=0.5)
axes[1].legend()

# --- Save ---
os.makedirs("plots", exist_ok=True)
plt.tight_layout()
plt.savefig("plots/roulette_martingale_vs_antimartingale.pdf")
plt.close()
