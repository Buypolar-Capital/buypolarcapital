
import numpy as np
import matplotlib.pyplot as plt
import os

# --- Parameters ---
n_spins = 100000       # number of roulette spins
n_slots = 37            # European roulette: numbers 0-36
n_bootstrap = 100       # how many times to bootstrap the whole simulation

# --- Simulate ---
all_counts = np.zeros((n_bootstrap, n_slots))
for b in range(n_bootstrap):
    spins = np.random.randint(0, n_slots, size=n_spins)
    counts = np.bincount(spins, minlength=n_slots)
    all_counts[b] = counts

# --- Average hits across bootstrap samples ---
mean_hits = all_counts.mean(axis=0)
std_hits = all_counts.std(axis=0)

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(n_slots)
ax.bar(x, mean_hits, yerr=std_hits, capsize=2, edgecolor='black', alpha=0.75)
ax.set_title(f"Distribution of Roulette Hits (European, {n_spins} spins bootstrapped {n_bootstrap}x)")
ax.set_xlabel("Roulette Number")
ax.set_ylabel("Average Hit Count")
ax.set_xticks(x)
ax.set_xticklabels([str(i) for i in range(n_slots)])
ax.grid(True, linestyle='--', alpha=0.5)

# --- Save as PDF ---
os.makedirs("plots", exist_ok=True)
plt.tight_layout()
plt.savefig("plots/roulette_hits.pdf")
plt.close()
