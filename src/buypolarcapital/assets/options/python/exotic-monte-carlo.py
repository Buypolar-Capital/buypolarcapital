import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import multiprocessing as mp
import seaborn as sns
from scipy import stats
import pandas as pd
import os

# Create plots/ folder
if not os.path.exists('plots'):
    os.makedirs('plots')

# Parameters
S0 = 100
K = 100
r = 0.05
sigma = 0.2
T = 1.0
n_steps = 252
n_sims = 10000

def simulate_paths(seed):
    np.random.seed(seed)
    n_per_core = n_sims // mp.cpu_count()
    paths = np.zeros((n_per_core, n_steps + 1))
    paths_anti = np.zeros((n_per_core, n_steps + 1))
    paths[:, 0] = paths_anti[:, 0] = S0
    dt = T / n_steps
    for t in range(n_steps):
        dW = np.random.normal(0, np.sqrt(dt), n_per_core)
        paths[:, t + 1] = paths[:, t] * np.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
        paths_anti[:, t + 1] = paths_anti[:, t] * np.exp((r - 0.5 * sigma**2) * dt - sigma * dW)
    return paths, paths_anti

if __name__ == '__main__':
    n_cores = mp.cpu_count()
    pool = mp.Pool(n_cores)
    seeds = range(n_cores)
    results = pool.map(simulate_paths, seeds)
    pool.close()
    pool.join()

    # Combine paths
    paths = np.vstack([res[0] for res in results])
    paths_anti = np.vstack([res[1] for res in results])
    
    # Asian option payoff
    avg_prices = np.mean(paths[:, 1:], axis=1)
    avg_prices_anti = np.mean(paths_anti[:, 1:], axis=1)
    payoffs = np.maximum(avg_prices - K, 0)
    payoffs_anti = np.maximum(avg_prices_anti - K, 0)
    all_payoffs = np.concatenate([payoffs, payoffs_anti])
    option_price = np.exp(-r * T) * np.mean(all_payoffs)
    price_std = np.std(all_payoffs) / np.sqrt(2 * n_sims)

    # Summary stats
    stats_table = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std', 'Min', 'Max', 'Skew', 'Kurtosis'],
        'Payoff': [all_payoffs.mean(), np.median(all_payoffs), all_payoffs.std(), 
                   all_payoffs.min(), all_payoffs.max(), stats.skew(all_payoffs), stats.kurtosis(all_payoffs)],
        'Avg Price': [avg_prices.mean(), np.median(avg_prices), avg_prices.std(), 
                      avg_prices.min(), avg_prices.max(), stats.skew(avg_prices), stats.kurtosis(avg_prices)],
        'Avg Price Anti': [avg_prices_anti.mean(), np.median(avg_prices_anti), avg_prices_anti.std(), 
                           avg_prices_anti.min(), avg_prices_anti.max(), stats.skew(avg_prices_anti), stats.kurtosis(avg_prices_anti)]
    })

    print(f"Asian Call Price (with Antithetic): {option_price:.4f}, Std Error: {price_std:.4f}")

    # Save to PDF with stats
    with PdfPages('plots/asian_option_antithetic_stats.pdf') as pdf:
        # Page 1: Sample Paths
        plt.figure(figsize=(12, 6))
        for i in range(5):
            plt.plot(paths[i], label=f"Path {i+1}")
            plt.plot(paths_anti[i], linestyle='--', label=f"Anti Path {i+1}")
        plt.title("Sample GBM Paths with Antithetic Variates")
        plt.xlabel("Time Step")
        plt.ylabel("Price")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 2: Payoff Histogram
        plt.figure(figsize=(12, 6))
        plt.hist(all_payoffs, bins=50, color='blue', alpha=0.7)
        plt.title("Asian Call Payoff Distribution")
        plt.xlabel("Payoff")
        plt.ylabel("Frequency")
        plt.axvline(option_price, color='red', linestyle='--', label=f"Price = {option_price:.2f}")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 3: Payoff Density
        plt.figure(figsize=(12, 6))
        sns.kdeplot(all_payoffs, color='blue', label='Payoff Density')
        plt.title("Payoff Density")
        plt.xlabel("Payoff")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 4: Avg Price Density (Regular vs. Anti)
        plt.figure(figsize=(12, 6))
        sns.kdeplot(avg_prices, color='green', label='Regular')
        sns.kdeplot(avg_prices_anti, color='orange', label='Antithetic')
        plt.title("Average Price Density (Regular vs. Antithetic)")
        plt.xlabel("Average Price")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 5: Payoff Q-Q Plot
        plt.figure(figsize=(12, 6))
        stats.probplot(all_payoffs, dist="norm", plot=plt)
        plt.title("Payoff Q-Q Plot")
        pdf.savefig()
        plt.close()

        # Page 6: Avg Price Q-Q Plot
        plt.figure(figsize=(12, 6))
        stats.probplot(avg_prices, dist="norm", plot=plt)
        plt.title("Average Price Q-Q Plot (Regular)")
        pdf.savefig()
        plt.close()

        # Page 7: Payoff vs. Avg Price Scatter
        plt.figure(figsize=(12, 6))
        plt.scatter(avg_prices, payoffs, color='teal', alpha=0.5, label='Regular')
        plt.scatter(avg_prices_anti, payoffs_anti, color='purple', alpha=0.5, label='Antithetic')
        plt.title("Payoff vs. Average Price")
        plt.xlabel("Average Price")
        plt.ylabel("Payoff")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 8: Cumulative Payoff
        plt.figure(figsize=(12, 6))
        plt.plot(np.cumsum(all_payoffs) / np.arange(1, len(all_payoffs) + 1), color='blue')
        plt.title("Cumulative Average Payoff")
        plt.xlabel("Simulation")
        plt.ylabel("Cumulative Mean Payoff")
        pdf.savefig()
        plt.close()

        # Page 9: Box Plot of Payoffs
        plt.figure(figsize=(12, 6))
        plt.boxplot([payoffs, payoffs_anti], labels=['Regular', 'Antithetic'])
        plt.title("Payoff Box Plot")
        plt.ylabel("Payoff")
        pdf.savefig()
        plt.close()

        # Page 10: Summary Stats Table
        plt.figure(figsize=(12, 6))
        plt.table(cellText=stats_table.values, colLabels=stats_table.columns, loc='center', cellLoc='center')
        plt.axis('off')
        plt.title("Summary Statistics")
        pdf.savefig()
        plt.close()

    print("PDF saved with 10 pages!")