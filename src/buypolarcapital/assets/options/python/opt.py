
import yfinance as yf

ticker = yf.Ticker("AAPL")
options_dates = ticker.options

for i in options_dates:
    print(i)

expiry = options_dates[0]
opt = ticker.option_chain(expiry)

print("\nCalls:")
print(opt.calls.head())

print("\nPuts:")
print(opt.puts.head())

