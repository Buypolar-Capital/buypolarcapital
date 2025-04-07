# run this once to generate a test plot
import matplotlib.pyplot as plt
import numpy as np

tickers = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'GOOG']
returns = [1.25, 0.85, 0.45, 0.35, 0.3]

plt.bar(tickers, returns)
plt.title("Daily Returns")
plt.ylabel("Return (%)")
plt.tight_layout()
plt.savefig("dashboard/plots/daily_returns.pdf")
