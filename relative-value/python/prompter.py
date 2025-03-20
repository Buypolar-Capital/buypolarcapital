import yfinance as yf 
import matplotlib.pyplot as plt
import os
import numpy as np
from scipy import stats

# List of ticker pairs (add as many as you want)
ticker_pairs = [
    # United States
    ('BRK-A', 'BRK-B', '1996-05-09', '2024-12-31'),  # Berkshire Hathaway: BRK-A ~1500x BRK-B since 1996 B-share split
    ('GOOGL', 'GOOG', '2004-08-19', '2024-12-31'),  # Alphabet: Class A (1 vote) vs Class C (no vote), IPO 2004
    ('META', 'METB', '2012-05-18', '2024-12-31'),   # Meta: Class A vs Class B (10 votes), IPO 2012 (METB not publicly traded, placeholder)
    ('F', 'F-B', '1956-01-01', '2024-12-31'),       # Ford: Class A vs Class B (family control), public since 1956 (F-B not listed)
    ('CMCSA', 'CMCSK', '1988-01-01', '2024-12-31'), # Comcast: Class A (1 vote) vs Class K (no vote), dual structure since 1980s
    ('NWS', 'NWSA', '2004-11-03', '2024-12-31'),   # News Corp: Class A (no vote) vs Class B (1 vote), split from parent 2004
    ('SNAP', 'SNAP-B', '2017-03-02', '2024-12-31'), # Snap: Class A (no vote) vs Class B (1 vote), IPO 2017 (SNAP-B not public)
    ('DIS', 'DIS-B', '1940-11-13', '2024-12-31'),  # Disney: Class A vs Class B (historical family control, B not traded widely)
    ('WMT', 'WMT-B', '1970-10-01', '2024-12-31'),  # Walmart: Class A vs Class B (Walton family), public since 1970 (B not listed)
    ('KO', 'KO-B', '1919-09-05', '2024-12-31'),    # Coca-Cola: Historical dual structure, B shares for control (B not traded)

    # Scandinavia
    ('HM-B.ST', 'HM-A.ST', '1974-10-04', '2024-12-31'), # H&M (Sweden): B (1/10 vote) vs A (1 vote), public since 1974
    ('VOLV-B.ST', 'VOLV-A.ST', '1935-01-01', '2024-12-31'), # Volvo (Sweden): B (1/10 vote) vs A (1 vote), long history
    ('TEL.OL', 'TEL-B.OL', '1998-10-26', '2024-12-31'), # Telenor (Norway): A vs B (state control), IPO 1998 (B less common)
    ('NDA-DK.CO', 'NDA-SE.ST', '1998-01-01', '2024-12-31'), # Nordea (Finland/Sweden): Dual listings, historical A/B split
    ('ATCO-A.ST', 'ATCO-B.ST', '2005-01-01', '2024-12-31'), # Atlas Copco (Sweden): A (1 vote) vs B (1/10 vote)
    ('ERIC-B.ST', 'ERIC-A.ST', '1876-01-01', '2024-12-31'), # Ericsson (Sweden): B (1/10 vote) vs A (1 vote), long history
    ('INVEB.ST', 'INVEA.ST', '1987-01-01', '2024-12-31'),  # Investor AB (Sweden): B (1/10 vote) vs A (1 vote), Wallenberg control
    ('SKF-B.ST', 'SKF-A.ST', '1935-01-01', '2024-12-31'),   # SKF (Sweden): B (1/10 vote) vs A (1 vote), industrial giant

    # Asia
    ('9988.HK', '9988-B.HK', '2019-11-26', '2024-12-31'), # Alibaba (China/HK): Ordinary vs B (founder control), HK listing 2019
    ('9618.HK', '9618-B.HK', '2020-11-05', '2024-12-31'), # JD.com (China/HK): Ordinary vs B (10 votes), HK dual listing 2020
    ('1810.HK', '1810-B.HK', '2018-07-09', '2024-12-31'), # Xiaomi (China/HK): Ordinary vs B (10 votes), IPO 2018
    ('700.HK', '700-B.HK', '2000-07-26', '2024-12-31'),   # Tencent (China/HK): Ordinary vs B (founder control), IPO 2004 (B not public)
    ('TM', 'TM-B', '1987-01-01', '2024-12-31'),          # Toyota (Japan): Common vs historical B (family influence), NYSE 1987
    ('005930.KS', '005935.KS', '1975-06-11', '2024-12-31'), # Samsung Electronics (South Korea): Common vs Preferred (no vote)
    ('SOFTBANK.JP', 'SOFTBANK-B.JP', '1994-07-29', '2024-12-31'), # SoftBank (Japan): Common vs B (Masayoshi Son control, B not public)
]

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Loop through each ticker pair
for ticker1, ticker2, start_date, end_date in ticker_pairs:
    print(f"\nProcessing {ticker1} vs {ticker2}")
    try:
        # Fetch data
        stock1 = yf.Ticker(ticker1)
        stock2 = yf.Ticker(ticker2)
        data1 = stock1.history(start=start_date, end=end_date)
        data2 = stock2.history(start=start_date, end=end_date)

        if data1.empty or data2.empty:
            print(f'No data found for {ticker1} or {ticker2}')
        else:
            # Plot 1: Closing Prices
            plt.figure(figsize=(12, 6))
            plt.plot(data1['Close'], label=ticker1)
            plt.plot(data2['Close'], label=ticker2)
            plt.title(f'{ticker1} vs {ticker2} Stock Prices')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            price_file = os.path.join(script_dir, f'{ticker1.lower()}_vs_{ticker2.lower()}_prices.pdf')
            plt.savefig(price_file, format='pdf', bbox_inches='tight')
            print(f"Saved prices plot to: {price_file}")
            plt.close()  # Close to free memory (replaces plt.show())

            # Plot 2: Relative Value (ticker1 / ticker2)
            relative_value = data1['Close'] / data2['Close']
            mode_value = round(stats.mode(relative_value.dropna())[0])  # Mode, rounded

            plt.figure(figsize=(12, 6))
            plt.plot(relative_value, label=f'{ticker1} / {ticker2}')
            plt.axhline(y=mode_value, color='r', linestyle='--', label=f'Mode ≈ {mode_value}')
            plt.title(f'Relative Value: {ticker1} / {ticker2}')
            plt.xlabel('Date')
            plt.ylabel('Relative Value')
            plt.legend()
            rel_file = os.path.join(script_dir, f'{ticker1.lower()}_vs_{ticker2.lower()}_relative_value.pdf')
            plt.savefig(rel_file, format='pdf', bbox_inches='tight')
            print(f"Saved relative value plot to: {rel_file}")
            plt.close()  # Close to free memory

    except Exception as e:
        print(f"An error occurred for {ticker1} vs {ticker2}: {e}")

print("\nAll pairs processed!")