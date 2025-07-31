import yfinance as yf 
import matplotlib.pyplot as plt
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

try: 
    ticker_a = yf.Ticker('VOW3.DE')  # Preference shares
    ticker_b = yf.Ticker('VOW.DE')   # Ordinary shares
    data_a = ticker_a.history(start="2000-01-01", end="2024-12-31")
    data_b = ticker_b.history(start="2000-01-01", end="2024-12-31")

    if data_a.empty or data_b.empty:
        print('No data found')
    else: 
        # Plot 1: Closing Prices
        plt.figure(figsize=(12, 6))
        plt.plot(data_a['Close'], label='VOW3.DE')
        plt.plot(data_b['Close'], label='VOW.DE')
        plt.title('Volkswagen A vs B Stocks')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        price_file = os.path.join(script_dir, 'volkswagen_prices.pdf')
        plt.savefig(price_file, format='pdf', bbox_inches='tight')
        print(f"Saved closing prices plot to: {price_file}")
        plt.show()  # Optional

        # Plot 2: Relative Value (VOW.DE / VOW3.DE)
        relative_value = data_b['Close'] / data_a['Close']
        plt.figure(figsize=(12, 6))
        plt.plot(relative_value, label='VOW.DE / VOW3.DE')
        plt.title('Relative Value: VOW.DE / VOW3.DE')
        plt.xlabel('Date')
        plt.ylabel('Relative Value')
        plt.legend()
        rel_file = os.path.join(script_dir, 'volkswagen_relative_value.pdf')
        plt.savefig(rel_file, format='pdf', bbox_inches='tight')
        print(f"Saved relative value plot to: {rel_file}")
        plt.show()  # Optional

except Exception as e:
    print(f"An error occurred: {e}")

    