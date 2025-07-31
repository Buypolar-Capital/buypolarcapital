
import pandas as pd 
import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt 

aapl = yf.download("AAPL", start="2010-01-01", end="2020-01-02")
print(aapl.head(3))


def ticker_reader(ticker):
    data = yf.download(ticker, start="2020-01-01", end="2025-04-01")
    print(data)

ticker_reader("TSLA")


df = pd.DataFrame(aapl)
print(df)


