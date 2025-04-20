import numpy as np
import matplotlib.pyplot as plt
import os

# --- Parameters ---
n_simulations = 100000         # number of gamblers
n_spins = 500                 # how long each tries
initial_bankroll = 100        # starting capital
bet_amount = 1                # fixed bet per round

# Red wins with prob 18/37 (European wheel)
p_red = 18 / 37
p_loss = 1 - p_red

# --- Simulation ---
final_bankrolls = np.zeros(n_simulations)
busts = 0

for i in range(n_simulations):
    bankroll = initial_bankroll
    for _ in range(n_spins):
        if bankroll <= 0:
            busts += 1
            break
        outcome = np.random.rand()
        if outcome < p_red:
            bankroll += bet_amount
        else:
            bankroll -= bet_amount
    final_bankrolls[i] = bankroll

# --- Stats ---
bust_rate = busts / n_simulations
mean_final = final_bankrolls.mean()

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(final_bankrolls, bins=50, edgecolor='black', alpha=0.75)
ax.axvline(initial_bankroll, color='red', linestyle='--', label='Starting Bankroll')
ax.set_title(f"Flat Bet on Red ({n_simulations} Sims, {n_spins} Spins, Init = {initial_bankroll})\nBust Rate = {bust_rate:.2%}, Mean Final = {mean_final:.2f}")
ax.set_xlabel("Final Bankroll")
ax.set_ylabel("Frequency")
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)

# --- Save ---
os.makedirs("plots", exist_ok=True)
plt.tight_layout()
plt.savefig("plots/roulette_betting_red.pdf")
plt.close()
