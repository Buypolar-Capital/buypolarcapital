import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define the stocks and parameters
stocks = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]
initial_cash = 10000  # $10,000 starting capital
shares_per_trade = 10  # Smaller trades
window = 5  # 5-day rolling VWAP

# Create 'plots' directory if it doesn't exist
Path("plots").mkdir(exist_ok=True)

# Download data for 2023
data = {}
for stock in stocks:
    try:
        df = yf.download(stock, start="2023-01-01", end="2023-12-31", interval="1d")
        if df.empty:
            raise ValueError(f"No data returned for {stock}")
        df = df.rename(columns={
            'Open': 'Open', 'High': 'High', 'Low': 'Low', 
            'Close': 'Close', 'Adj Close': 'Adj Close', 'Volume': 'Volume'
        })
        data[stock] = df[['High', 'Low', 'Close', 'Volume']]
    except Exception as e:
        print(f"Error downloading {stock}: {e}")
        exit(1)

# Function to calculate rolling 5-day VWAP with debugging
def calculate_rolling_vwap(df, window=5):
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    price_volume = typical_price * df['Volume']
    cum_price_volume = price_volume.cumsum()
    cum_volume = df['Volume'].cumsum()
    rolling_price_volume = cum_price_volume - cum_price_volume.shift(window, fill_value=0)
    rolling_volume = cum_volume - cum_volume.shift(window, fill_value=0)
    vwap = rolling_price_volume / rolling_volume
    
    # Debug prints
    print(f"Stock: {stocks[0 if 'AAPL' not in df else stocks.index('AAPL')]}")  # Hack to get stock name
    print(f"Close shape: {df['Close'].shape}, VWAP shape: {vwap.shape}")
    print(f"Close index: {df['Close'].index.equals(vwap.index)}")
    
    # Build DataFrame column-by-column
    result = pd.DataFrame(index=df.index)
    result['Close'] = df['Close']
    result['VWAP'] = vwap
    return result.dropna()

# VWAP Strategy Simulation (daily with 5-day rolling VWAP)
vwap_portfolio = pd.DataFrame(index=data["AAPL"].index)
vwap_cash = initial_cash
vwap_holdings = {stock: 0 for stock in stocks}

for stock in stocks:
    daily_data = calculate_rolling_vwap(data[stock], window=window)
    vwap_portfolio[f"{stock}_Value"] = 0.0
    
    for date in daily_data.index:
        price = daily_data.loc[date, 'Close']
        vwap = daily_data.loc[date, 'VWAP']
        
        # Buy if price < VWAP, sell if price > VWAP
        if price < vwap and vwap_cash >= price * shares_per_trade:
            vwap_holdings[stock] += shares_per_trade
            vwap_cash -= price * shares_per_trade
        elif price > vwap and vwap_holdings[stock] >= shares_per_trade:
            vwap_holdings[stock] -= shares_per_trade
            vwap_cash += price * shares_per_trade
        
        # Update portfolio value
        vwap_portfolio.loc[date, f"{stock}_Value"] = vwap_holdings[stock] * price

# Total VWAP portfolio value
vwap_portfolio['Total'] = vwap_portfolio[[f"{stock}_Value" for stock in stocks]].sum(axis=1) + vwap_cash

# Equal-Weighted Portfolio Simulation (weekly for comparison)
equal_portfolio = pd.DataFrame(index=data["AAPL"].resample('W').last().index)
equal_cash = initial_cash
equal_holdings = {}

for stock in stocks:
    weekly_data = data[stock][['Close']].resample('W').last().dropna()
    first_price = weekly_data['Close'].iloc[0]
    shares = (equal_cash * 0.2) // first_price
    equal_holdings[stock] = shares
    equal_portfolio[f"{stock}_Value"] = weekly_data['Close'] * shares

# Total equal-weighted portfolio value
equal_portfolio['Total'] = equal_portfolio[[f"{stock}_Value" for stock in stocks]].sum(axis=1)

# Resample VWAP portfolio to weekly for plotting
vwap_portfolio_weekly = vwap_portfolio.resample('W').last()

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(vwap_portfolio_weekly.index, vwap_portfolio_weekly['Total'], label="VWAP Strategy (5-Day Rolling)", color="blue")
plt.plot(equal_portfolio.index, equal_portfolio['Total'], label="Equal-Weighted (20%)", color="orange")
plt.title("Portfolio Performance: VWAP Strategy vs. Equal-Weighted (2023)")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)

# Save plot to PDF
plt.savefig("plots/portfolio_comparison.pdf", format="pdf")
plt.close()

print("Simulation complete! Plot saved as 'portfolio_comparison.pdf' in the 'plots' folder.")
print(f"Final VWAP Portfolio Value: ${vwap_portfolio['Total'].iloc[-1]:.2f}")
print(f"Final Equal-Weighted Portfolio Value: ${equal_portfolio['Total'].iloc[-1]:.2f}")