import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import os

# Define the simulation parameters
START_DATE = '2024-01-01'
END_DATE = '2024-12-31'
THRESHOLDS = [0.01, 0.02, 0.03, 0.04, 0.05]  # Minimum thresholds: 1%, 2%, 3%, 4%, 5%
INITIAL_CASH = 10000.0  # Starting cash for the portfolio

# Get a list of S&P 500 tickers (we'll use a subset for simplicity)
sp500_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT',
    'PG', 'KO', 'DIS', 'NFLX', 'CSCO', 'INTC', 'AMD', 'QCOM', 'ORCL', 'IBM'
]  # 20 stocks for this example; expand as needed

def fetch_stock_data(tickers, start_date, end_date):
    """
    Fetch historical stock data for the given tickers
    """
    data = {}
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        if not df.empty:
            data[ticker] = df['Close']
        else:
            print(f"No data for {ticker}")
    return pd.DataFrame(data)

def simulate_portfolio(tickers, start_date, end_date, min_threshold):
    """
    Simulate the portfolio using the dynamic percentage change strategy
    If a stock drops X% (X >= min_threshold), buy $X worth; if it rises X% (X >= min_threshold), sell $X worth
    """
    # Fetch stock data
    stock_prices = fetch_stock_data(tickers, start_date, end_date)
    
    # Initialize portfolio
    cash = INITIAL_CASH
    holdings = {ticker: 0.0 for ticker in tickers}  # Shares owned
    portfolio_values = []
    dates = stock_prices.index
    
    # Iterate through each trading day
    for i in range(1, len(dates)):
        date = dates[i]
        prev_date = dates[i-1]
        
        # Calculate portfolio value at the start of the day
        portfolio_value = cash
        for ticker in tickers:
            if ticker in stock_prices.columns:
                price = stock_prices.loc[date, ticker]
                if not np.isnan(price):
                    portfolio_value += holdings[ticker] * price
        
        portfolio_values.append(portfolio_value)
        
        # Apply the trading strategy
        for ticker in tickers:
            if ticker not in stock_prices.columns:
                continue
            
            # Get current and previous day's closing prices
            current_price = stock_prices.loc[date, ticker]
            prev_price = stock_prices.loc[prev_date, ticker]
            
            if np.isnan(current_price) or np.isnan(prev_price):
                continue
            
            # Calculate price change percentage
            price_change = (current_price - prev_price) / prev_price
            trade_amount = abs(price_change) * 100  # Convert percentage to dollars (e.g., 8% = $8)
            
            # Only trade if the absolute price change exceeds the minimum threshold
            if abs(price_change) < min_threshold:
                continue
            
            # Buy if price drops
            if price_change < 0:  # Price dropped
                shares_to_buy = trade_amount / current_price
                if cash >= trade_amount:
                    holdings[ticker] += shares_to_buy
                    cash -= trade_amount
                    print(f"Threshold {min_threshold*100}% - {date.date()}: Bought {shares_to_buy:.4f} shares of {ticker} at ${current_price:.2f} (drop of {abs(price_change)*100:.2f}%)")
            
            # Sell if price rises
            elif price_change > 0:  # Price rose
                shares_to_sell = trade_amount / current_price
                if holdings[ticker] >= shares_to_sell:
                    holdings[ticker] -= shares_to_sell
                    cash += trade_amount
                    print(f"Threshold {min_threshold*100}% - {date.date()}: Sold {shares_to_sell:.4f} shares of {ticker} at ${current_price:.2f} (rise of {price_change*100:.2f}%)")
    
    # Final portfolio value
    final_value = cash
    for ticker in tickers:
        if ticker in stock_prices.columns:
            final_price = stock_prices.loc[dates[-1], ticker]
            if not np.isnan(final_price):
                final_value += holdings[ticker] * final_price
    
    return dates, portfolio_values, final_value

def simulate_equally_weighted_portfolio(tickers, start_date, end_date):
    """
    Simulate an equally weighted portfolio (buy and hold)
    Invest an equal amount in each stock at the start and hold until the end
    """
    # Fetch stock data
    stock_prices = fetch_stock_data(tickers, start_date, end_date)
    
    # Initialize portfolio
    num_stocks = len(tickers)
    cash_per_stock = INITIAL_CASH / num_stocks  # Equal allocation
    holdings = {ticker: 0.0 for ticker in tickers}  # Shares owned
    portfolio_values = []
    dates = stock_prices.index
    
    # Invest equally on the first day
    for ticker in tickers:
        if ticker in stock_prices.columns:
            first_price = stock_prices.loc[dates[0], ticker]
            if not np.isnan(first_price):
                shares_to_buy = cash_per_stock / first_price
                holdings[ticker] = shares_to_buy
                print(f"Equally Weighted - {dates[0].date()}: Bought {shares_to_buy:.4f} shares of {ticker} at ${first_price:.2f}")
    
    # Track portfolio value over time
    for i in range(len(dates)):
        date = dates[i]
        portfolio_value = 0.0
        for ticker in tickers:
            if ticker in stock_prices.columns:
                price = stock_prices.loc[date, ticker]
                if not np.isnan(price):
                    portfolio_value += holdings[ticker] * price
        portfolio_values.append(portfolio_value)
    
    final_value = portfolio_values[-1]
    return dates, portfolio_values, final_value

def plot_portfolios(dates, threshold_results, equally_weighted_result):
    """
    Plot the portfolio values for different thresholds and the equally weighted portfolio
    """
    plt.figure(figsize=(12, 8))
    
    # Plot each threshold strategy
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, (min_threshold, (portfolio_values, final_value)) in enumerate(threshold_results.items()):
        plt.plot(dates[1:], portfolio_values, label=f'Threshold {min_threshold*100}% (Final: ${final_value:.2f})', color=colors[i])
    
    # Plot the equally weighted portfolio
    dates_eq, portfolio_values_eq, final_value_eq = equally_weighted_result
    plt.plot(dates_eq, portfolio_values_eq, label=f'Equally Weighted (Final: ${final_value_eq:.2f})', color='black', linestyle='--')
    
    plt.title('Portfolio Performance: Dynamic Strategy vs. Equally Weighted (2024)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot as PDF
    plots_dir = 'c:/Users/ofurn/Dokumenter/Github/buypolarcapital/hft/Python/plots'
    os.makedirs(plots_dir, exist_ok=True)
    save_path = os.path.join(plots_dir, 'portfolio_simulation_2024.pdf')
    plt.savefig(save_path, format='pdf')
    print(f"Portfolio plot saved as '{save_path}'")
    plt.show()

# Run the simulation
if __name__ == "__main__":
    # Install required libraries if not already installed:
    # pip install yfinance pandas matplotlib numpy
    
    # Simulate for each threshold
    threshold_results = {}
    for min_threshold in THRESHOLDS:
        print(f"\nSimulating with minimum threshold: {min_threshold*100}%")
        dates, portfolio_values, final_value = simulate_portfolio(sp500_tickers, START_DATE, END_DATE, min_threshold)
        threshold_results[min_threshold] = (portfolio_values, final_value)
        print(f"Threshold {min_threshold*100}% - Initial Portfolio Value: ${INITIAL_CASH:.2f}")
        print(f"Threshold {min_threshold*100}% - Final Portfolio Value: ${final_value:.2f}")
        print(f"Threshold {min_threshold*100}% - Total Return: {((final_value - INITIAL_CASH) / INITIAL_CASH) * 100:.2f}%")
    
    # Simulate the equally weighted portfolio
    print("\nSimulating equally weighted portfolio...")
    dates_eq, portfolio_values_eq, final_value_eq = simulate_equally_weighted_portfolio(sp500_tickers, START_DATE, END_DATE)
    print(f"Equally Weighted - Initial Portfolio Value: ${INITIAL_CASH:.2f}")
    print(f"Equally Weighted - Final Portfolio Value: ${final_value_eq:.2f}")
    print(f"Equally Weighted - Total Return: {((final_value_eq - INITIAL_CASH) / INITIAL_CASH) * 100:.2f}%")
    
    # Plot the results
    plot_portfolios(dates, threshold_results, (dates_eq, portfolio_values_eq, final_value_eq))