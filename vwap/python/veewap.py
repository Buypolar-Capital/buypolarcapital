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

# Fetch 1-min data for March 26-27, 2025 (past date since today is March 30, 2025)
start = '2025-03-26'
end = '2025-03-27'
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
        df['SMA5'] = df['Close'].rolling(window=5).mean()
        df['VWAP20'] = (df['Close'] * df['Volume']).rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
        data[stock] = df[['Open', 'High', 'Low', 'Close', 'Volume', 'VWAP', 'SMA5', 'VWAP20']]
    except Exception as e:
        print(f"Error fetching data for {stock}: {e}")
        continue

# VWAP Strategies
def static_vwap(df, n_shares):
    trades = np.full(len(df), n_shares / len(df))
    exec_prices = df['Close'].values
    return trades, exec_prices

def dynamic_vwap(df, n_shares):
    vol_profile = df['Volume'] / df['Volume'].sum()
    trades = n_shares * vol_profile
    exec_prices = df['Close'].values
    return trades, exec_prices

def aggressive_vwap(df, n_shares):
    trades = np.where(df['Close'] < df['VWAP'], 50, 10)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)
    exec_prices = df['Close'].values
    return trades, exec_prices

def passive_vwap(df, n_shares):
    band = 0.005
    trades = np.where((df['Close'] > df['VWAP'] * (1 - band)) & (df['Close'] < df['VWAP'] * (1 + band)), 30, 0)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded if total_traded > 0 else 1)
    exec_prices = df['Close'].values
    return trades, exec_prices

def momentum_vwap(df, n_shares):
    trades = np.where(df['Close'] > df['SMA5'], 40, 10)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)
    exec_prices = df['Close'].values
    return trades, exec_prices

def twap_hybrid_vwap(df, n_shares):
    base_rate = n_shares / len(df)
    trades = base_rate * (1 + (df['VWAP'] - df['Close']) / df['VWAP'])
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)
    exec_prices = df['Close'].values
    return trades, exec_prices

def mean_reversion_vwap(df, n_shares):
    deviation = np.abs(df['Close'] - df['VWAP20']).fillna(0)
    trades = 10 + 40 * (deviation / deviation.max())
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded)
    exec_prices = df['Close'].values
    return trades, exec_prices

def liquidity_vwap(df, n_shares):
    vol_threshold = df['Volume'].quantile(0.8)
    trades = np.where(df['Volume'] > vol_threshold, 50, 0)
    total_traded = trades.sum()
    trades = trades * (n_shares / total_traded if total_traded > 0 else 1)
    exec_prices = df['Close'].values
    return trades, exec_prices

# Simulate trades
strategies = {
    'Static': static_vwap,
    'Dynamic': dynamic_vwap,
    'Aggressive': aggressive_vwap,
    'Passive': passive_vwap,
    'Momentum': momentum_vwap,
    'TWAP Hybrid': twap_hybrid_vwap,
    'Mean Reversion': mean_reversion_vwap,
    'Liquidity': liquidity_vwap
}
results = {}
for stock in data:
    df = data[stock]
    results[stock] = {}
    for strat_name, strat_func in strategies.items():
        trades, exec_prices = strat_func(df, n_shares)
        avg_price = np.average(exec_prices, weights=trades)
        slippage = avg_price - df['VWAP'].iloc[-1]
        results[stock][strat_name] = {'trades': trades, 'exec_prices': exec_prices, 'avg_price': avg_price, 'slippage': slippage}

# Plotting and Analysis - Single PDF
with PdfPages('plots/vwap_strats.pdf') as pdf:
    for stock in results:
        df = data[stock]

        # Page 1: Trade Volume vs. Price/VWAP
        plt.figure(figsize=(12, 6))
        for strat_name in strategies:
            plt.plot(df.index, results[stock][strat_name]['trades'], label=f'{strat_name}', alpha=0.7)
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
            plt.plot(df.index, cum_trades, label=f'{strat_name}', alpha=0.7)
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
        plt.xticks(rotation=45)
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

    # Overall Summary Stats - 5 Pages
    # Page 21: Slippage Distribution Box Plot
    plt.figure(figsize=(12, 6))
    slippage_data = [np.array([results[stock][strat]['slippage'] for stock in results]) for strat in strategies]
    sns.boxplot(data=slippage_data, palette='viridis')
    plt.xticks(np.arange(len(strategies)), list(strategies.keys()), rotation=45)
    plt.axhline(0, color='k', linestyle='--')
    plt.title('Slippage Distribution Across All Stocks')
    plt.ylabel('Slippage ($)')
    plt.xlabel('Strategy')
    plt.text(0.5, -0.2, 'Shows range and variability of slippage. Lower median and tighter spread = better consistency.', 
             transform=plt.gca().transAxes, fontsize=10, ha='center')
    pdf.savefig()
    plt.close()

    # Page 22: Avg Price vs. VWAP Bar Plot
    plt.figure(figsize=(12, 6))
    avg_prices = [np.mean([results[stock][strat]['avg_price'] - data[stock]['VWAP'].iloc[-1] for stock in results]) 
                  for strat in strategies]
    sns.barplot(x=list(strategies.keys()), y=avg_prices, hue=list(strategies.keys()), palette='viridis', legend=False)
    plt.axhline(0, color='k', linestyle='--')
    plt.title('Average Price Deviation from VWAP Across All Stocks')
    plt.ylabel('Price Deviation ($)')
    plt.xlabel('Strategy')
    plt.xticks(rotation=45)
    plt.text(0.5, -0.2, 'Measures how close avg execution price is to VWAP. Negative = cheaper than VWAP.', 
             transform=plt.gca().transAxes, fontsize=10, ha='center')
    pdf.savefig()
    plt.close()

    # Page 23: Risk (Slippage Std) Bar Plot
    plt.figure(figsize=(12, 6))
    std_slippages = [np.std([results[stock][strat]['slippage'] for stock in results]) for strat in strategies]
    sns.barplot(x=list(strategies.keys()), y=std_slippages, hue=list(strategies.keys()), palette='viridis', legend=False)
    plt.title('Slippage Risk (Standard Deviation) Across All Stocks')
    plt.ylabel('Slippage Std Dev ($)')
    plt.xlabel('Strategy')
    plt.xticks(rotation=45)
    plt.text(0.5, -0.2, 'Higher std = more risk/variability in execution price vs. VWAP.', 
             transform=plt.gca().transAxes, fontsize=10, ha='center')
    pdf.savefig()
    plt.close()

    # Page 24: Trade Volume Heatmap
    plt.figure(figsize=(12, 6))
    trade_volumes = np.array([np.mean([results[stock][strat]['trades'] for stock in results], axis=0) 
                              for strat in strategies])
    sns.heatmap(trade_volumes, cmap='viridis', xticklabels=50, yticklabels=list(strategies.keys()))
    plt.title('Average Trade Volume Heatmap Across Time')
    plt.xlabel('Time (Minutes)')
    plt.ylabel('Strategy')
    plt.text(0.5, -0.2, 'Shows trading intensity over time. Darker = more shares traded.', 
             transform=plt.gca().transAxes, fontsize=10, ha='center')
    pdf.savefig()
    plt.close()

    # Page 25: Detailed Tradeoff Table
    overall_stats = pd.DataFrame({
        'Strategy': list(strategies.keys()),
        'Avg Slippage': [np.mean([results[stock][strat]['slippage'] for stock in results]) for strat in strategies],
        'Std Slippage': std_slippages,
        'Avg Price Dev': avg_prices,
        'Tradeoffs': [
            'Stable, low risk, but no price advantage.',
            'Volume-driven, good in stable markets, risks missing dips.',
            'Exploits dips, high reward, higher risk.',
            'Low impact, waits for stability, may miss volume.',
            'Chases trends, good in momentum, risky in choppy markets.',
            'Balanced, adaptive, moderate risk/reward.',
            'Reversion-focused, high activity, sensitive to VWAP20.',
            'Liquidity-focused, low impact, misses low-volume opps.'
        ]
    }).sort_values('Avg Slippage')
    
    plt.figure(figsize=(12, 8))
    plt.table(cellText=overall_stats.values, colLabels=overall_stats.columns, loc='center', cellLoc='center', 
              colWidths=[0.15, 0.15, 0.15, 0.15, 0.4])
    plt.axis('off')
    plt.title('Strategy Tradeoffs Across All Stocks')
    plt.text(0.5, -0.1, 'Ranks by Avg Slippage. Tradeoffs: Price (Slippage), Risk (Std), Execution Style.', 
             transform=plt.gca().transAxes, fontsize=10, ha='center')
    pdf.savefig()
    plt.close()

    print("Single PDF 'vwap_strats.pdf' saved with 25 pages!")

print("All VWAP strategy analysis completed!")