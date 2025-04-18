import numpy as np
import pandas as pd
from scipy.stats import norm

# Black-Scholes model
def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Binomial tree pricing (Cox-Ross-Rubinstein)
def binomial_option_price(S, K, T, r, sigma, steps=100, option_type="call"):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    discount = np.exp(-r * dt)

    prices = S * u ** np.arange(steps, -1, -1) * d ** np.arange(0, steps + 1)
    if option_type == "call":
        values = np.maximum(prices - K, 0)
    else:
        values = np.maximum(K - prices, 0)

    for _ in range(steps):
        values = discount * (p * values[:-1] + (1 - p) * values[1:])
    return values[0]

# GARCH(1,1) volatility estimator
def estimate_garch_vol(returns, omega=0.000001, alpha=0.05, beta=0.94):
    T = len(returns)
    var = np.var(returns)
    sigma2 = np.zeros(T)
    sigma2[0] = var
    for t in range(1, T):
        sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]
    return np.sqrt(sigma2[-1])

# Dummy return series for GARCH
np.random.seed(0)
returns = np.random.normal(0, 0.01, size=500)
garch_vol = estimate_garch_vol(returns)

# Example values
S, K, T, r, sigma = 100, 105, 0.5, 0.01, 0.2
bs = black_scholes_price(S, K, T, r, sigma, "call")
binom = binomial_option_price(S, K, T, r, sigma, option_type="call")
garch_bs = black_scholes_price(S, K, T, r, garch_vol, "call")

# Results
bs, binom, garch_bs


