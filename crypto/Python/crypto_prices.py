import ccxt
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
import os

# Initialize the exchange (Binance as an example)
exchange = ccxt.binance({
    'enableRateLimit': True,
})

# List of the 5 most popular cryptos (based on current trends)
crypto_pairs = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT']

# Define absolute base path
BASE_PATH = 'c:/Users/ofurn/Dokumenter/Github/buypolarcapital'

def fetch_historical_prices(symbols, timeframe='1d', limit=90):
    """
    Fetch historical OHLCV data for 2025 up to March 23
    symbols: list of trading pairs
    timeframe: '1d' for daily data
    limit: number of data points (e.g., 90 days back from March 23, 2025)
    """
    all_data = {}
    
    try:
        exchange.load_markets()
        
        # Calculate timestamp for start of 2025 (Jan 1, 2025)
        since = exchange.parse8601('2025-01-01T00:00:00Z')
        
        for symbol in symbols:
            print(f"Fetching data for {symbol}...")
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            all_data[symbol] = df
            time.sleep(exchange.rateLimit / 1000)  # Avoid rate limits
            
        return all_data
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def plot_relative_profits(price_data, plot_all=True, btc_only=False):
    """
    Plot percentage change (relative profits) for cryptocurrencies
    plot_all: If True, plot all cryptos together
    btc_only: If True, plot only Bitcoin
    """
    plt.figure(figsize=(12, 8))
    
    for symbol, df in price_data.items():
        # Filter data up to March 23, 2025
        df = df[df['timestamp'] <= '2025-03-23']
        
        # Calculate percentage change relative to the first price
        initial_price = df['close'].iloc[0]
        df['pct_change'] = (df['close'] - initial_price) / initial_price * 100
        
        # Plot based on conditions
        if plot_all or (btc_only and symbol == 'BTC/USDT'):
            plt.plot(df['timestamp'], df['pct_change'], label=symbol, linewidth=1.5)
    
    if plot_all:
        plt.title('Top 5 Cryptocurrency Relative Profits (Jan 1 - March 23, 2025)', fontsize=14)
        save_path = os.path.join(BASE_PATH, 'crypto', 'Python', 'crypto_relative_profits_2025.png')
    elif btc_only:
        plt.title('Bitcoin Relative Profits (Jan 1 - March 23, 2025)', fontsize=14)
        plots_dir = os.path.join(BASE_PATH, 'crypto', 'plots')
        os.makedirs(plots_dir, exist_ok=True)
        save_path = os.path.join(plots_dir, 'bitcoin_relative_profits_2025.png')
    
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Percentage Change (%)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(save_path)
    print(f"Plot saved as '{save_path}'")
    plt.show()

# Fetch and plot the data
if __name__ == "__main__":
    price_data = fetch_historical_prices(crypto_pairs)
    
    if price_data:
        # Plot all cryptos together
        plot_relative_profits(price_data, plot_all=True, btc_only=False)
        
        # Plot only Bitcoin separately
        plot_relative_profits(price_data, plot_all=False, btc_only=True)
        
        # Ensure the masterdata directory exists
        masterdata_dir = os.path.join(BASE_PATH, 'masterdata')
        os.makedirs(masterdata_dir, exist_ok=True)
        
        # Save data to CSV with percentage change
        for symbol, df in price_data.items():
            # Recalculate pct_change for saving
            initial_price = df['close'].iloc[0]
            df['pct_change'] = (df['close'] - initial_price) / initial_price * 100
            
            if symbol == 'BTC/USDT':
                # Save BTC data to the masterdata folder
                filename = os.path.join(masterdata_dir, 'BTC_USDT_2025_profits.csv')
            else:
                # Save other cryptos to the Python directory
                filename = os.path.join(BASE_PATH, 'crypto', 'Python', f"{symbol.replace('/', '_')}_2025_profits.csv")
                
            df.to_csv(filename, index=False)
            print(f"Saved {symbol} data to {filename}")