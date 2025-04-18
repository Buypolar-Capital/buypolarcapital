from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import os
import pytz
from datetime import datetime

# Define the simulation parameters
TRADING_DAY = '2025-03-20'  # Recent trading day within Alpha Vantage's data range
INTERVAL = '1min'  # 1-minute intervals
THRESHOLDS = [0.01, 0.02, 0.03, 0.04, 0.05]  # Minimum thresholds: 1%, 2%, 3%, 4%, 5%
INITIAL_CASH = 10000.0  # Starting cash for the portfolio
TRANSACTION_FEE = 0.01  # $0.01 per trade
API_KEY = "YI1MGLZJZOKNMP4W"  # Replace with a new API key if the current one is over the limit

# Get a list of S&P 500 tickers (subset for simplicity)
sp500_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT',
    'PG', 'KO', 'DIS', 'NFLX', 'CSCO', 'INTC', 'AMD', 'QCOM', 'ORCL', 'IBM'
]

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, '..', 'plots')

def fetch_intraday_data(tickers, trading_day, interval):
    """
    Fetch intraday stock data for the given tickers using Alpha Vantage
    """
    data = {}
    eastern = pytz.timezone('US/Eastern')
    
    for ticker in tickers:
        print(f"Fetching data for {ticker} from Alpha Vantage...")
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        df, meta = ts.get_intraday(symbol=ticker, interval=interval, outputsize='full')
        
        # Rename columns
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        
        # Convert index to Eastern Time
        df.index = pd.to_datetime(df.index).tz_localize('UTC').tz_convert(eastern)
        
        # Filter for the specific trading day and regular market hours (09:30 to 16:00)
        df = df[df.index.date == pd.to_datetime(trading_day).date()]
        df = df.between_time('09:30', '16:00')
        
        if df.empty:
            print(f"No data available for {ticker} on {trading_day} between 09:30 and 16:00.")
            continue
        
        data[ticker] = df['Close']
    
    return pd.DataFrame(data)

def simulate_intraday_portfolio(tickers, trading_day, interval, min_threshold):
    """
    Simulate the portfolio using the dynamic percentage change strategy on an intraday basis
    """
    stock_prices = fetch_intraday_data(tickers, trading_day, interval)
    
    if stock_prices.empty:
        print("No data available for the specified tickers and time range.")
        return None, None, None
    
    cash = INITIAL_CASH
    holdings = {ticker: 0.0 for ticker in tickers}
    portfolio_values = []
    timestamps = stock_prices.index
    
    for i in range(1, len(timestamps)):
        timestamp = timestamps[i]
        prev_timestamp = timestamps[i-1]
        
        portfolio_value = cash
        for ticker in tickers:
            if ticker in stock_prices.columns:
                price = stock_prices.loc[timestamp, ticker]
                if not np.isnan(price):
                    portfolio_value += holdings[ticker] * price
        
        portfolio_values.append(portfolio_value)
        
        for ticker in tickers:
            if ticker not in stock_prices.columns:
                continue
            
            current_price = stock_prices.loc[timestamp, ticker]
            prev_price = stock_prices.loc[prev_timestamp, ticker]
            
            if np.isnan(current_price) or np.isnan(prev_price):
                continue
            
            price_change = (current_price - prev_price) / prev_price
            trade_amount = abs(price_change) * 100
            
            if abs(price_change) < min_threshold:
                continue
            
            if price_change < 0:
                shares_to_buy = trade_amount / current_price
                total_cost = trade_amount + TRANSACTION_FEE
                if cash >= total_cost:
                    holdings[ticker] += shares_to_buy
                    cash -= total_cost
                    print(f"Threshold {min_threshold*100}% - {timestamp}: Bought {shares_to_buy:.4f} shares of {ticker} at ${current_price:.2f} (drop of {abs(price_change)*100:.2f}%)")
            
            elif price_change > 0:
                shares_to_sell = trade_amount / current_price
                if holdings[ticker] >= shares_to_sell:
                    holdings[ticker] -= shares_to_sell
                    cash += trade_amount - TRANSACTION_FEE
                    print(f"Threshold {min_threshold*100}% - {timestamp}: Sold {shares_to_sell:.4f} shares of {ticker} at ${current_price:.2f} (rise of {price_change*100:.2f}%)")
    
    final_value = cash
    for ticker in tickers:
        if ticker in stock_prices.columns:
            final_price = stock_prices.iloc[-1][ticker]
            if not np.isnan(final_price):
                final_value += holdings[ticker] * final_price
    
    return timestamps, portfolio_values, final_value

def simulate_equally_weighted_intraday(tickers, trading_day, interval):
    """
    Simulate an equally weighted portfolio (buy and hold) for a single day
    """
    stock_prices = fetch_intraday_data(tickers, trading_day, interval)
    
    if stock_prices.empty:
        print("No data available for the specified tickers and time range.")
        return None, None, None
    
    num_stocks = len(tickers)
    cash_per_stock = INITIAL_CASH / num_stocks
    holdings = {ticker: 0.0 for ticker in tickers}
    portfolio_values = []
    timestamps = stock_prices.index
    
    for ticker in tickers:
        if ticker in stock_prices.columns:
            first_price = stock_prices.iloc[0][ticker]
            if not np.isnan(first_price):
                shares_to_buy = cash_per_stock / first_price
                holdings[ticker] = shares_to_buy
                print(f"Equally Weighted - {timestamps[0]}: Bought {shares_to_buy:.4f} shares of {ticker} at ${first_price:.2f}")
    
    for i in range(len(timestamps)):
        timestamp = timestamps[i]
        portfolio_value = 0.0
        for ticker in tickers:
            if ticker in stock_prices.columns:
                price = stock_prices.loc[timestamp, ticker]
                if not np.isnan(price):
                    portfolio_value += holdings[ticker] * price
        portfolio_values.append(portfolio_value)
    
    final_value = portfolio_values[-1]
    return timestamps, portfolio_values, final_value

def plot_portfolios(timestamps, threshold_results, equally_weighted_result):
    """
    Plot the portfolio values for different thresholds and the equally weighted portfolio
    """
    plt.figure(figsize=(12, 8))
    
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, (min_threshold, (portfolio_values, final_value)) in enumerate(threshold_results.items()):
        plt.plot(timestamps[1:], portfolio_values, label=f'Threshold {min_threshold*100}% (Final: ${final_value:.2f})', color=colors[i])
    
    timestamps_eq, portfolio_values_eq, final_value_eq = equally_weighted_result
    plt.plot(timestamps_eq, portfolio_values_eq, label=f'Equally Weighted (Final: ${final_value_eq:.2f})', color='black', linestyle='--')
    
    plt.title(f'Intraday Portfolio Performance: Dynamic Strategy vs. Equally Weighted ({TRADING_DAY})', fontsize=14)
    plt.xlabel('Time (HH:MM, Eastern Time)', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format x-axis as HH:MM
    eastern = pytz.timezone('US/Eastern')
    plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M', tz=eastern))
    
    # Set x-axis limits to 09:30 to 16:00
    start_date = timestamps[0].date()
    start_time = datetime(start_date.year, start_date.month, start_date.day, 9, 30, tzinfo=eastern)
    end_time = datetime(start_date.year, start_date.month, start_date.day, 16, 0, tzinfo=eastern)
    plt.xlim(start_time, end_time)
    
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot as PDF
    os.makedirs(plots_dir, exist_ok=True)
    save_path = os.path.join(plots_dir, 'intraday_portfolio_simulation_2025.pdf')
    plt.savefig(save_path, format='pdf', bbox_inches='tight')
    print(f"Portfolio plot saved as '{save_path}'")
    plt.show()

# Run the simulation
if __name__ == "__main__":
    # Install required libraries if not already installed:
    # pip install alpha-vantage pandas matplotlib numpy
    
    # Simulate for each threshold
    threshold_results = {}
    for min_threshold in THRESHOLDS:
        print(f"\nSimulating intraday with minimum threshold: {min_threshold*100}%")
        timestamps, portfolio_values, final_value = simulate_intraday_portfolio(sp500_tickers, TRADING_DAY, INTERVAL, min_threshold)
        if timestamps is None:
            print(f"Skipping threshold {min_threshold*100}% due to lack of data.")
            continue
        threshold_results[min_threshold] = (portfolio_values, final_value)
        print(f"Threshold {min_threshold*100}% - Initial Portfolio Value: ${INITIAL_CASH:.2f}")
        print(f"Threshold {min_threshold*100}% - Final Portfolio Value: ${final_value:.2f}")
        print(f"Threshold {min_threshold*100}% - Total Return: {((final_value - INITIAL_CASH) / INITIAL_CASH) * 100:.2f}%")
    
    # Simulate the equally weighted portfolio
    print("\nSimulating intraday equally weighted portfolio...")
    timestamps_eq, portfolio_values_eq, final_value_eq = simulate_equally_weighted_intraday(sp500_tickers, TRADING_DAY, INTERVAL)
    if timestamps_eq is None:
        print("Exiting due to lack of data for equally weighted portfolio.")
        exit()
    
    print(f"Equally Weighted - Initial Portfolio Value: ${INITIAL_CASH:.2f}")
    print(f"Equally Weighted - Final Portfolio Value: ${final_value_eq:.2f}")
    print(f"Equally Weighted - Total Return: {((final_value_eq - INITIAL_CASH) / INITIAL_CASH) * 100:.2f}%")
    
    # Plot the results
    plot_portfolios(timestamps, threshold_results, (timestamps_eq, portfolio_values_eq, final_value_eq))