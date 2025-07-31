
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = yf.download("MSFT", start="2020-01-01", end="2025-01-01")
print(data.head())
print(data.info())


close = data[("Close", "MSFT")]
print(close)
print(f"\n")

close_volume = data[[("Close", "MSFT"), ("Volume", "MSFT")]]
print(close_volume.head())
print(f"\n")

close_v = data[("Close", "MSFT")]
print(close_v.head())
print(f"\n")

data.columns = [f"{price}_{ticker}" for price, ticker in data.columns]
data = data.reset_index()
print(data.head())

high_volume = data[data["Volume_MSFT"] > data["Volume_MSFT"].mean()]
print(high_volume[["Close_MSFT", "Volume_MSFT"]].head())

data["return"] = data["Close_MSFT"].pct_change()
print(data.head())

data["price_change"] = data["Close_MSFT"] - data["Close_MSFT"].shift(1)
print(data[["Close_MSFT", "price_change"]].head())

sorted_data = data.sort_values("Close_MSFT", ascending=False)
print(sorted_data.head())
print(f"\n")


print(data.isna().sum())
print(f"\n")

import seaborn as sns

# sns.lineplot(x="Date", y="Close_MSFT", data=data)
# plt.title("yeah")
# plt.show()



data["Year"] = data["Date"].dt.year
print(data.head())




print(f"\n")
import math
print(dir(math))
from math import e as e
print(e)

