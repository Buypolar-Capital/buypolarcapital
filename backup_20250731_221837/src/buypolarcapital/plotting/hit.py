

import yfinance as yf

# Define stock tickers
tickers = ['SAP.DE', 'SIE.DE', 'DTE.DE']

# Fetch data
data = {ticker: yf.download(ticker, start='2020-01-01', end='2025-01-01') for ticker in tickers}


import matplotlib.pyplot as plt

# Calculate daily returns
returns = {ticker: data[ticker]['Adj Close'].pct_change().dropna() for ticker in tickers}

# Plot returns
plt.figure(figsize=(14, 7))
for ticker in tickers:
    plt.plot(returns[ticker], label=ticker)
plt.title('Daily Returns of SAP, Siemens, and Deutsche Telekom')
plt.legend()
plt.show()


import numpy as np

params = {}
for ticker in tickers:
    mu = returns[ticker].mean()
    sigma = returns[ticker].std()
    params[ticker] = {'mu': mu, 'sigma': sigma}


import numpy as np

def simulate_hitting_time(S0, mu, sigma, target_price, dt=1/252, num_simulations=1000):
    hitting_times = []
    for _ in range(num_simulations):
        S = S0
        time = 0
        while S < target_price:
            S *= np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * np.random.normal())
            time += dt
        hitting_times.append(time)
    return np.mean(hitting_times)

# Define target prices (e.g., 10% above current price)
target_prices = {ticker: data[ticker]['Adj Close'][-1] * 1.1 for ticker in tickers}

# Simulate hitting times
simulated_hitting_times = {}
for ticker in tickers:
    S0 = data[ticker]['Adj Close'][-1]
    mu = params[ticker]['mu']
    sigma = params[ticker]['sigma']
    target_price = target_prices[ticker]
    simulated_hitting_times[ticker] = simulate_hitting_time(S0, mu, sigma, target_price)


import pandas as pd

# Compile results
results = pd.DataFrame({
    'Stock': tickers,
    'Simulated Hitting Time (days)': [simulated_hitting_times[ticker] for ticker in tickers]
})

print(results)


