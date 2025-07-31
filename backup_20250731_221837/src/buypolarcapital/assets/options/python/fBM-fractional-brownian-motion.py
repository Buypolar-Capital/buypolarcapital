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
r = 0.05
sigma = 0.2
H = 0.3
eta = 1.5
rho = -0.7
T = 1.0
n_steps = 252
n_sims = 10000

def generate_fbm(n_steps, H, seed):
    np.random.seed(seed)
    t = np.linspace(0, T, n_steps + 1)
    cov = np.zeros((n_steps + 1, n_steps + 1))
    for i in range(n_steps + 1):
        for j in range(n_steps + 1):
            cov[i, j] = 0.5 * (t[i]**(2*H) + t[j]**(2*H) - np.abs(t[i] - t[j])**(2*H))
    L = np.linalg.cholesky(cov + 1e-10 * np.eye(n_steps + 1))
    z = np.random.normal(0, 1, (n_steps + 1, n_sims // mp.cpu_count()))
    return L @ z

def simulate_paths(seed):
    np.random.seed(seed)
    n_per_core = n_sims // mp.cpu_count()
    dt = T / n_steps
    S = np.zeros((n_per_core, n_steps + 1))
    S_anti = np.zeros((n_per_core, n_steps + 1))
    v = np.zeros((n_per_core, n_steps + 1))
    S[:, 0] = S_anti[:, 0] = S0
    v[:, 0] = sigma**2

    B_H = generate_fbm(n_steps, H, seed)
    W = np.random.normal(0, np.sqrt(dt), (n_per_core, n_steps))
    W_vol = rho * W + np.sqrt(1 - rho**2) * np.random.normal(0, np.sqrt(dt), (n_per_core, n_steps))

    for t in range(n_steps):
        v[:, t + 1] = np.exp(eta * B_H[t + 1, :] - 0.5 * eta**2 * (t * dt)**(2 * H))
        S[:, t + 1] = S[:, t] * np.exp((r - 0.5 * v[:, t]) * dt + np.sqrt(v[:, t]) * W[:, t])
        S_anti[:, t + 1] = S_anti[:, t] * np.exp((r - 0.5 * v[:, t]) * dt - np.sqrt(v[:, t]) * W[:, t])

    return S, S_anti, v

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
    vols = np.vstack([res[2] for res in results])

    # Lookback option payoff
    min_prices = np.min(paths[:, 1:], axis=1)
    min_prices_anti = np.min(paths_anti[:, 1:], axis=1)
    payoffs = np.maximum(paths[:, -1] - min_prices, 0)
    payoffs_anti = np.maximum(paths_anti[:, -1] - min_prices_anti, 0)
    all_payoffs = np.concatenate([payoffs, payoffs_anti])
    option_price = np.exp(-r * T) * np.mean(all_payoffs)
    price_std = np.std(all_payoffs) / np.sqrt(2 * n_sims)

    # Control variate (GBM) - Match size with all_payoffs
    gbm_sims = 2 * n_sims  # Double to match antithetic
    gbm_paths = np.zeros((gbm_sims, n_steps + 1))
    gbm_paths[:, 0] = S0
    for t in range(n_steps):
        dW = np.random.normal(0, np.sqrt(T/n_steps), gbm_sims)
        gbm_paths[:, t + 1] = gbm_paths[:, t] * np.exp((r - 0.5 * sigma**2) * (T/n_steps) + sigma * dW)
    gbm_min = np.min(gbm_paths[:, 1:], axis=1)
    gbm_payoffs = np.maximum(gbm_paths[:, -1] - gbm_min, 0)
    gbm_price = np.exp(-r * T) * np.mean(gbm_payoffs)
    cov = np.cov(all_payoffs, gbm_payoffs)[0, 1]
    var_gbm = np.var(gbm_payoffs)
    b = cov / var_gbm
    option_price_cv = option_price + b * (gbm_price - option_price)

    # Summary stats
    stats_table = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std', 'Min', 'Max', 'Skew', 'Kurtosis'],
        'Payoff': [all_payoffs.mean(), np.median(all_payoffs), all_payoffs.std(), 
                   all_payoffs.min(), all_payoffs.max(), stats.skew(all_payoffs), stats.kurtosis(all_payoffs)],
        'Min Price': [min_prices.mean(), np.median(min_prices), min_prices.std(), 
                      min_prices.min(), min_prices.max(), stats.skew(min_prices), stats.kurtosis(min_prices)],
        'Volatility': [vols.mean(), np.median(vols), vols.std(), 
                       vols.min(), vols.max(), stats.skew(vols.flatten()), stats.kurtosis(vols.flatten())]
    })

    print(f"Lookback Call Price (Rough Vol): {option_price:.4f}, Std Error: {price_std:.4f}")
    print(f"Lookback Call Price (Control Variate): {option_price_cv:.4f}")

    # Save to PDF with stats
    with PdfPages('plots/lookback_rough_stats.pdf') as pdf:
        # Page 1: Sample Paths
        plt.figure(figsize=(12, 6))
        for i in range(5):
            plt.plot(paths[i], label=f"Path {i+1}")
            plt.plot(paths_anti[i], linestyle='--', label=f"Anti Path {i+1}")
        plt.title(f"Sample Rough Volatility Paths (H={H})")
        plt.xlabel("Time Step")
        plt.ylabel("Price")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 2: Payoff Histogram
        plt.figure(figsize=(12, 6))
        plt.hist(all_payoffs, bins=50, color='blue', alpha=0.7)
        plt.title("Lookback Call Payoff Distribution")
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

        # Page 4: Min Price Density
        plt.figure(figsize=(12, 6))
        sns.kdeplot(min_prices, color='green', label='Regular')
        sns.kdeplot(min_prices_anti, color='orange', label='Antithetic')
        plt.title("Minimum Price Density (Regular vs. Antithetic)")
        plt.xlabel("Minimum Price")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 5: Volatility Density
        plt.figure(figsize=(12, 6))
        sns.kdeplot(vols.flatten(), color='purple', label='Volatility')
        plt.title("Volatility Density")
        plt.xlabel("Volatility")
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 6: Payoff Q-Q Plot
        plt.figure(figsize=(12, 6))
        stats.probplot(all_payoffs, dist="norm", plot=plt)
        plt.title("Payoff Q-Q Plot")
        pdf.savefig()
        plt.close()

        # Page 7: Volatility vs. Payoff Scatter
        plt.figure(figsize=(12, 6))
        plt.scatter(vols.mean(axis=1), payoffs, color='teal', alpha=0.5, label='Regular')
        plt.scatter(vols.mean(axis=1), payoffs_anti, color='purple', alpha=0.5, label='Antithetic')
        plt.title("Volatility vs. Payoff")
        plt.xlabel("Average Volatility")
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