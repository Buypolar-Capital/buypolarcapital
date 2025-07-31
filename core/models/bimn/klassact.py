
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Finans:
    def __init__(self, ticker, start='2020-01-01', end='2025-01-01'):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.data = None

    def fetch_data(self):
        stock = yf.Ticker(self.ticker)
        self.data = stock.history(start=self.start, end=self.end)
        if self.data.empty:
            print(f'no data found for {self.ticker} between {self.start} and {self.end}')
        else:
            print(f'data fetched succesfully!')

    def plot_close(self):
        if self.data is None or self.data.empty:
            print(f'no data to plot pls run fetch_data() first')
            return
        plt.figure(figsize=(10,5))
        plt.plot(self.data.index, self.data['Close'], label=f'{self.ticker} Close')
        plt.title(f'{self.ticker} Closing Price')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    stock = Finans('IBM', start='2023-01-01', end='2023-12-31')
    stock.fetch_data()
    stock.plot_close()







    