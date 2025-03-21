import yfinance as yf
import pandas as pd

ticker = "AAPL"
stock = yf.Ticker(ticker)
intraday_data = stock.history(period="1d", interval="1m")

# Shortened output: only Close price, 2 rows
print(intraday_data[['Close']].head(2))

