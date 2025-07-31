
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

tsla = yf.download("TSLA", start="2020-01-01", end="2025-01-01", period="1d")
print(tsla.head())

tsla["SMA20"] = tsla["Close"].rolling(window=20).mean()
print(tsla.head())

plt.figure(figsize=(10,5))
plt.plot(tsla.index, tsla["Close"], label="Close", color="black", alpha=.7)
plt.plot(tsla.index, tsla["SMA20"], label="SMA20", color="red")
plt.xlabel("date")
plt.ylabel("price")
plt.title("moving average")
plt.show()
