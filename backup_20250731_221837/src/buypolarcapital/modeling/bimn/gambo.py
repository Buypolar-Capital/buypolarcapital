

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

data = yf.download("AAPL", start="2023-01-01", end="2025-04-01", interval="1d")
print(data)
data = data.reset_index()
print(data)
print(data["Date"])

X = data['Volume']
y = data['Close']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())

plt.figure(figsize=(10,5))
sns.regplot(data=data, x='Volume', y='Close', scatter_kws={'alpha':.5})
plt.tight_layout()
plt.show()

