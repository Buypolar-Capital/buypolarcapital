import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import os

# Create plots/ folder
if not os.path.exists('plots'):
    os.makedirs('plots')

# Stocks and order size
stocks = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL']
n_shares = 10000  # Fixed order size

# Fetch 1-min data for March 27, 2025 (past date since today is March 30, 2025)
start = '2025-03-27'
end = '2025-03-28'
data = {}
for stock in stocks:
    try:
        ticker = yf.Ticker(stock)
        df = ticker.history(interval='1m', start=start, end=end)
        if df.empty:
            print(f"No data for {stock} - skipping.")
            continue
        df.index = pd.to_datetime(df.index).tz_convert('America/New_York')
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        df['SMA5'] = df['Close'].rolling(window=5).mean()  # For Momentum strat
        data[stock] = df[['Open', 'High', 'Low', 'Close', 'Volume', 'VWAP', 'SMA5']]
    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
        continue

# VWAP Strategies
def static_vwap(df, n_shares):
    trades = np.full(len(df), n_shares / len(df))  # Even split
    exec_prices = df['Close'].values
    return trades, exec_prices

def dynamic_vwap(df, n_shares):
    vol_profile = df['Volume'] / df['Volume'].sum()  # Volume fraction per minute
    trades = n_shares * vol_profile  # Scale by total shares
    exec_prices = df['Close'].values
    return trades, exec_prices

def aggressive_vwap(df, n_shares):
    trades = np.where(df['Close'] < df['VWAP'], 50, 10)  # More when below VWAP
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)  # Normalize to n_shares
    exec_prices = df['Close'].values
    return trades, exec_prices

def passive_vwap(df, n_shares):
    band = 0.005  # 0.5% band around VWAP
    trades = np.where((df['Close'] > df['VWAP'] * (1 - band)) & (df['Close'] < df['VWAP'] * (1 + band)), 30, 0)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded if total_traded > 0 else 1)  # Normalize or flat if no trades
    exec_prices = df['Close'].values
    return trades, exec_prices

def momentum_vwap(df, n_shares):
    trades = np.where(df['Close'] > df['SMA5'], 40, 10)  # More when price > SMA5 (uptrend)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)  # Normalize to n_shares
    exec_prices = df['Close'].values
    return trades, exec_prices

# Simulate trades
strategies = {
    'Static': static_vwap,
    'Dynamic': dynamic_vwap,
    'Aggressive': aggressive_vwap,
    'Passive': passive_vwap,
    'Momentum': momentum_vwap
}
results = {}
for stock in data:
    df = data[stock]
    results[stock] = {}
    for strat_name, strat_func in strategies.items():
        trades, exec_prices = strat_func(df, n_shares)
        avg_price = np.average(exec_prices, weights=trades)
        slippage = avg_price - df['VWAP'].iloc[-1]  # vs. day's VWAP
        results[stock][strat_name] = {'trades': trades, 'exec_prices': exec_prices, 'avg_price': avg_price, 'slippage': slippage}

# Plotting and Analysis - Single PDF
with PdfPages('plots/vwap_strats.pdf') as pdf:
    for stock in results:
        df = data[stock]

        # Page 1: Trade Volume vs. Price/VWAP
        plt.figure(figsize=(12, 6))
        for strat_name in strategies:
            plt.plot(df.index, results[stock][strat_name]['trades'], label=f'{strat_name} Trades', alpha=0.7)
        plt.plot(df.index, df['Close'], 'k-', label='Price', alpha=0.5)
        plt.plot(df.index, df['VWAP'], 'r--', label='VWAP', alpha=0.8)
        plt.title(f'{stock} - Trade Volume vs. Price/VWAP')
        plt.xlabel('Time')
        plt.ylabel('Shares Traded / Price')
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 2: Cumulative Execution
        plt.figure(figsize=(12, 6))
        for strat_name in strategies:
            cum_trades = np.cumsum(results[stock][strat_name]['trades'])
            plt.plot(df.index, cum_trades, label=f'{strat_name} Cumulative', alpha=0.7)
        plt.axhline(n_shares, color='k', linestyle='--', label='Target Shares')
        plt.title(f'{stock} - Cumulative Execution')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Shares')
        plt.legend()
        pdf.savefig()
        plt.close()

        # Page 3: Slippage Bar Plot
        plt.figure(figsize=(12, 6))
        slippages = [results[stock][strat]['slippage'] for strat in strategies]
        sns.barplot(x=list(strategies.keys()), y=slippages, hue=list(strategies.keys()), palette='viridis', legend=False)
        plt.axhline(0, color='k', linestyle='--')
        plt.title(f'{stock} - Slippage vs. VWAP')
        plt.ylabel('Slippage ($)')
        plt.xlabel('Strategy')
        pdf.savefig()
        plt.close()

        # Page 4: Summary Stats
        stats_table = pd.DataFrame({
            'Strategy': list(strategies.keys()),
            'Avg Price': [results[stock][strat]['avg_price'] for strat in strategies],
            'Slippage': slippages
        })
        plt.figure(figsize=(12, 6))
        plt.table(cellText=stats_table.values, colLabels=stats_table.columns, loc='center', cellLoc='center')
        plt.axis('off')
        plt.title(f'{stock} - Summary Stats')
        pdf.savefig()
        plt.close()

    print("Single PDF 'vwap_strats.pdf' saved with 20 pages!")

print("All VWAP strategy analysis completed!")