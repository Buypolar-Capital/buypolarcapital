import pandas as pd
import numpy as np
import asyncio
import time
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from scipy import stats
import os

# Create plots/ folder
if not os.path.exists('plots'):
    os.makedirs('plots')

# Fake tick data
data = pd.DataFrame({
    'timestamp': pd.date_range(start='2025-03-29', periods=10000, freq='1ms'),
    'price': np.random.normal(50000, 100, 10000),
    'volume': np.random.exponential(0.1, 10000)
})

# Order book and log
lob = {'bids': [], 'asks': []}
order_log = []

async def place_order(side, price, volume, latency_ms):
    await asyncio.sleep(latency_ms / 1000)
    order = {'side': side, 'price': price, 'volume': volume, 'time': time.time(), 'latency': latency_ms}
    lob[side].append({'price': price, 'volume': volume})
    order_log.append(order)
    print(f"Order placed: {side} @ {price}, vol: {volume}")

async def simulate_orders():
    for i in range(100):  # 100 trades
        latency = np.random.exponential(0.1)
        price = data['price'].iloc[i]
        volume = data['volume'].iloc[i]
        await place_order('bids', price - 0.1, volume, latency * 1000)
        await place_order('asks', price + 0.1, volume, latency * 1000)
        await asyncio.sleep(np.random.poisson(0.2))

# Run sim
asyncio.run(simulate_orders())

# Convert log to DataFrame
orders_df = pd.DataFrame(order_log)
orders_df['time'] = pd.to_datetime(orders_df['time'], unit='s')

# Calculate spreads
bids = pd.DataFrame(lob['bids'])
asks = pd.DataFrame(lob['asks'])
spreads = asks['price'].values[:len(bids)] - bids['price'].values[:len(asks)]

# Summary stats
stats_table = pd.DataFrame({
    'Metric': ['Mean', 'Median', 'Std', 'Min', 'Max', 'Skew', 'Kurtosis'],
    'Price': [orders_df['price'].mean(), orders_df['price'].median(), orders_df['price'].std(), 
              orders_df['price'].min(), orders_df['price'].max(), orders_df['price'].skew(), orders_df['price'].kurtosis()],
    'Volume': [orders_df['volume'].mean(), orders_df['volume'].median(), orders_df['volume'].std(), 
               orders_df['volume'].min(), orders_df['volume'].max(), orders_df['volume'].skew(), orders_df['volume'].kurtosis()],
    'Latency': [orders_df['latency'].mean(), orders_df['latency'].median(), orders_df['latency'].std(), 
                orders_df['latency'].min(), orders_df['latency'].max(), orders_df['latency'].skew(), orders_df['latency'].kurtosis()],
    'Spread': [spreads.mean(), np.median(spreads), spreads.std(), spreads.min(), spreads.max(), 
               pd.Series(spreads).skew(), pd.Series(spreads).kurtosis()]
})

# Multi-page PDF
with PdfPages('plots/hft_plots.pdf') as pdf:
    # Page 1: Order Book
    plt.figure(figsize=(12, 6))
    if not bids.empty:
        plt.bar(bids['price'], bids['volume'], color='green', alpha=0.5, label='Bids')
    if not asks.empty:
        plt.bar(asks['price'], asks['volume'], color='red', alpha=0.5, label='Asks')
    plt.title('Order Book')
    plt.xlabel('Price')
    plt.ylabel('Volume')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Page 2: Latency Histogram
    plt.figure(figsize=(12, 6))
    plt.hist(orders_df['latency'], bins=20, color='blue', alpha=0.7)
    plt.title('Order Latencies')
    plt.xlabel('Latency (ms)')
    plt.ylabel('Frequency')
    pdf.savefig()
    plt.close()

    # Page 3: Price + Orders Over Time
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'][:100], data['price'][:100], label='Price', color='black')
    plt.scatter(orders_df[orders_df['side'] == 'bids']['time'], orders_df[orders_df['side'] == 'bids']['price'], 
                color='green', label='Bids', alpha=0.6)
    plt.scatter(orders_df[orders_df['side'] == 'asks']['time'], orders_df[orders_df['side'] == 'asks']['price'], 
                color='red', label='Asks', alpha=0.6)
    plt.title('Order Execution Over Time')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Page 4: Bid/Ask Price Density
    plt.figure(figsize=(12, 6))
    sns.kdeplot(bids['price'], color='green', label='Bids')
    sns.kdeplot(asks['price'], color='red', label='Asks')
    plt.title('Bid/Ask Price Density')
    plt.xlabel('Price')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Page 5: Volume Density
    plt.figure(figsize=(12, 6))
    sns.kdeplot(orders_df['volume'], color='purple')
    plt.title('Volume Density')
    plt.xlabel('Volume')
    pdf.savefig()
    plt.close()

    # Page 6: Latency Density
    plt.figure(figsize=(12, 6))
    sns.kdeplot(orders_df['latency'], color='blue')
    plt.title('Latency Density')
    plt.xlabel('Latency (ms)')
    pdf.savefig()
    plt.close()

    # Page 7: Price Q-Q Plot
    plt.figure(figsize=(12, 6))
    stats.probplot(orders_df['price'], dist="norm", plot=plt)
    plt.title('Price Q-Q Plot')
    pdf.savefig()
    plt.close()

    # Page 8: Volume Q-Q Plot
    plt.figure(figsize=(12, 6))
    stats.probplot(orders_df['volume'], dist="norm", plot=plt)
    plt.title('Volume Q-Q Plot')
    pdf.savefig()
    plt.close()

    # Page 9: Bid/Ask Spread Histogram
    plt.figure(figsize=(12, 6))
    plt.hist(spreads, bins=20, color='orange', alpha=0.7)
    plt.title('Bid/Ask Spread Distribution')
    plt.xlabel('Spread')
    pdf.savefig()
    plt.close()

    # Page 10: Volume vs. Latency Scatter
    plt.figure(figsize=(12, 6))
    plt.scatter(orders_df['latency'], orders_df['volume'], color='teal', alpha=0.5)
    plt.title('Volume vs. Latency')
    plt.xlabel('Latency (ms)')
    plt.ylabel('Volume')
    pdf.savefig()
    plt.close()

    # Page 11: Summary Stats Table
    plt.figure(figsize=(12, 6))
    plt.table(cellText=stats_table.values, colLabels=stats_table.columns, loc='center')
    plt.axis('off')
    plt.title('Summary Statistics')
    pdf.savefig()
    plt.close()

print("PDF saved with 11 pages!")