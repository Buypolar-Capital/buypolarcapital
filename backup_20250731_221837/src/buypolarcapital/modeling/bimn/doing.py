
# def finance(ticker):
#     data = yf.download(ticker, start="2010-01-01", end="2024-01-01")
#     plt.figure(figsize=(10,5))
#     plt.plot(data.index, data["Close"])
#     plt.ylabel("price")
#     plt.xlabel("date")
#     plt.title(f"{ticker}")
#     plt.show()

# finance("MSFT")

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

class StockData:
    def __init__(self, ticker, start="2020-01-01", end="2024-01-01"):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = None

    def download_data(self):
        self.data = yf.download(self.ticker, start=self.start, end=self.end)
        return self.data

    def plot_close(self):
        if self.data is None:
            self.download_data()
        plt.figure(figsize=(10,5))
        plt.plot(self.data.index, self.data["Close"])
        plt.xlabel("Date")
        plt.ylabel("Close")
        plt.title(f"{self.ticker} Closing Prices")
        plt.show()

    def calculate_returns(self):
        if self.data is None:
            self.download_data()
        self.data["Returns"] = self.data["Close"].pct_change()
        return self.data["Returns"]


msft = StockData("MSFT")
msft.download_data()
# msft.plot_close()
returns = msft.calculate_returns()
print(returns.head())

