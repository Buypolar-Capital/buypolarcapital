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
RISK_FREE_RATE = 0.0  # Risk-free rate (assumed 0% for simplicity)

# Get a list of S&P 500 tickers (we'll use a subset for simplicity)
sp500_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'WMT',
    'PG', 'KO', 'DIS', 'NFLX', 'CSCO', 'INTC', 'AMD', 'QCOM', 'ORCL', 'IBM'
]

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

def calculate_metrics(portfolio_values, dates):
    """
    Calculate return, risk (std dev of daily returns), and Sharpe ratio
    """
    # Calculate daily returns
    portfolio_values = np.array(portfolio_values)
    daily_returns = (portfolio_values[1:] - portfolio_values[:-1]) / portfolio_values[:-1]
    
    # Total return
    total_return = (portfolio_values[-1] - INITIAL_CASH) / INITIAL_CASH * 100
    
    # Risk (standard deviation of daily returns)
    risk = np.std(daily_returns) * 100  # In percentage
    
    # Sharpe ratio (annualized)
    mean_daily_return = np.mean(daily_returns)
    sharpe_ratio = (mean_daily_return - RISK_FREE_RATE) / np.std(daily_returns) * np.sqrt(252)
    
    return total_return, risk, sharpe_ratio

def simulate_portfolio(tickers, start_date, end_date, min_threshold):
    """
    Simulate the portfolio using the dynamic percentage change strategy
    """
    stock_prices = fetch_stock_data(tickers, start_date, end_date)
    
    cash = INITIAL_CASH
    holdings = {ticker: 0.0 for ticker in tickers}
    portfolio_values = []
    dates = stock_prices.index
    
    for i in range(1, len(dates)):
        date = dates[i]
        prev_date = dates[i-1]
        
        portfolio_value = cash
        for ticker in tickers:
            if ticker in stock_prices.columns:
                price = stock_prices.loc[date, ticker]
                if not np.isnan(price):
                    portfolio_value += holdings[ticker] * price
        
        portfolio_values.append(portfolio_value)
        
        for ticker in tickers:
            if ticker not in stock_prices.columns:
                continue
            
            current_price = stock_prices.loc[date, ticker]
            prev_price = stock_prices.loc[prev_date, ticker]
            
            if np.isnan(current_price) or np.isnan(prev_price):
                continue
            
            price_change = (current_price - prev_price) / prev_price
            trade_amount = abs(price_change) * 100
            
            if abs(price_change) < min_threshold:
                continue
            
            if price_change < 0:
                shares_to_buy = trade_amount / current_price
                if cash >= trade_amount:
                    holdings[ticker] += shares_to_buy
                    cash -= trade_amount
                    print(f"Threshold {min_threshold*100}% - {date.date()}: Bought {shares_to_buy:.4f} shares of {ticker} at ${current_price:.2f} (drop of {abs(price_change)*100:.2f}%)")
            
            elif price_change > 0:
                shares_to_sell = trade_amount / current_price
                if holdings[ticker] >= shares_to_sell:
                    holdings[ticker] -= shares_to_sell
                    cash += trade_amount
                    print(f"Threshold {min_threshold*100}% - {date.date()}: Sold {shares_to_sell:.4f} shares of {ticker} at ${current_price:.2f} (rise of {price_change*100:.2f}%)")
    
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
    """
    stock_prices = fetch_stock_data(tickers, start_date, end_date)
    
    num_stocks = len(tickers)
    cash_per_stock = INITIAL_CASH / num_stocks
    holdings = {ticker: 0.0 for ticker in tickers}
    portfolio_values = []
    dates = stock_prices.index
    
    for ticker in tickers:
        if ticker in stock_prices.columns:
            first_price = stock_prices.loc[dates[0], ticker]
            if not np.isnan(first_price):
                shares_to_buy = cash_per_stock / first_price
                holdings[ticker] = shares_to_buy
                print(f"Equally Weighted - {dates[0].date()}: Bought {shares_to_buy:.4f} shares of {ticker} at ${first_price:.2f}")
    
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

def plot_trading_strategies(dates, threshold_results):
    """
    Plot only the trading strategies
    """
    plt.figure(figsize=(12, 8))
    
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, (min_threshold, (portfolio_values, final_value)) in enumerate(threshold_results.items()):
        total_return, risk, sharpe = calculate_metrics(portfolio_values, dates[1:])
        plt.plot(dates[1:], portfolio_values, label=f'Threshold {min_threshold*100}% (Return: {total_return:.2f}%, Risk: {risk:.2f}%, Sharpe: {sharpe:.2f})', color=colors[i])
    
    plt.title('Portfolio Performance: Dynamic Trading Strategies (2024)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plots_dir = 'c:/Users/ofurn/Dokumenter/Github/buypolarcapital/hft/Python/plots'
    os.makedirs(plots_dir, exist_ok=True)
    save_path = os.path.join(plots_dir, 'trading_strategies_2024.pdf')
    plt.savefig(save_path, format='pdf')
    print(f"Trading strategies plot saved as '{save_path}'")
    plt.show()

def plot_basket(dates_eq, portfolio_values_eq, final_value_eq):
    """
    Plot only the equally weighted portfolio
    """
    plt.figure(figsize=(12, 8))
    
    total_return, risk, sharpe = calculate_metrics(portfolio_values_eq, dates_eq)
    plt.plot(dates_eq, portfolio_values_eq, label=f'Equally Weighted (Return: {total_return:.2f}%, Risk: {risk:.2f}%, Sharpe: {sharpe:.2f})', color='black', linestyle='--')
    
    plt.title('Portfolio Performance: Equally Weighted Portfolio (2024)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plots_dir = 'c:/Users/ofurn/Dokumenter/Github/buypolarcapital/hft/Python/plots'
    os.makedirs(plots_dir, exist_ok=True)
    save_path = os.path.join(plots_dir, 'equally_weighted_2024.pdf')
    plt.savefig(save_path, format='pdf')
    print(f"Equally weighted plot saved as '{save_path}'")
    plt.show()

def plot_combined(dates, threshold_results, equally_weighted_result):
    """
    Plot the combined portfolio values (trading strategies + equally weighted)
    """
    plt.figure(figsize=(12, 8))
    
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, (min_threshold, (portfolio_values, final_value)) in enumerate(threshold_results.items()):
        total_return, risk, sharpe = calculate_metrics(portfolio_values, dates[1:])
        plt.plot(dates[1:], portfolio_values, label=f'Threshold {min_threshold*100}% (Return: {total_return:.2f}%, Risk: {risk:.2f}%, Sharpe: {sharpe:.2f})', color=colors[i])
    
    dates_eq, portfolio_values_eq, final_value_eq = equally_weighted_result
    total_return_eq, risk_eq, sharpe_eq = calculate_metrics(portfolio_values_eq, dates_eq)
    plt.plot(dates_eq, portfolio_values_eq, label=f'Equally Weighted (Return: {total_return_eq:.2f}%, Risk: {risk_eq:.2f}%, Sharpe: {sharpe_eq:.2f})', color='black', linestyle='--')
    
    plt.title('Portfolio Performance: Dynamic Strategy vs. Equally Weighted (2024)', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    plots_dir = 'c:/Users/ofurn/Dokumenter/Github/buypolarcapital/hft/Python/plots'
    os.makedirs(plots_dir, exist_ok=True)
    save_path = os.path.join(plots_dir, 'combined_portfolio_simulation_2024.pdf')
    plt.savefig(save_path, format='pdf')
    print(f"Combined plot saved as '{save_path}'")
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
    plot_trading_strategies(dates, threshold_results)
    plot_basket(dates_eq, portfolio_values_eq, final_value_eq)
    plot_combined(dates, threshold_results, (dates_eq, portfolio_values_eq, final_value_eq))