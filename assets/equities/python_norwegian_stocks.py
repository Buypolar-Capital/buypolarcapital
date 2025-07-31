import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
import os

# Create plots directory if it doesn't exist
plots_dir = os.path.join(os.path.dirname(__file__), 'plots')
os.makedirs(plots_dir, exist_ok=True)

# Define Norwegian stock symbols (Oslo Børs)
# Note: Adding .OL suffix for Oslo Stock Exchange
symbols = [
    # Energy & Oil
    'EQNR.OL',    # Equinor
    'AKRBP.OL',   # Aker BP
    'VAR.OL',     # Vår Energi
    'AKSO.OL',    # Aker Solutions
    'TGS.OL',     # TGS
    
    # Seafood
    'MOWI.OL',    # Mowi
    'SALM.OL',    # SalMar
    'AUSS.OL',    # Austevoll Seafood
    'LSG.OL',     # Lerøy Seafood
    'BAKKA.OL',   # Bakkafrost
    
    # Finance
    'DNB.OL',     # DNB
    'GJFS.OL',    # Gjensidige
    'SBANK.OL',   # Sparebank 1 SR-Bank
    'NDA.OL',     # Nordea
    'SBVG.OL',    # Sparebanken Vest
    
    # Industry & Tech
    'YAR.OL',     # Yara International
    'TEL.OL',     # Telenor
    'KAHOT.OL',   # Kahoot
    'KOG.OL',     # Kongsberg Gruppen
    'ORCA.OL',    # Orca
    
    # Other sectors
    'GOGL.OL',    # Golden Ocean Group
    'ODF.OL',     # Orkla
    'NONG.OL',    # Norwegian
    'AKVA.OL',    # AKVA Group
    'RECSI.OL'    # REC Silicon
]

# Set the date range
end_date = datetime.now()
start_date = '2010-01-01'

# Create an empty DataFrame to store all stock data
all_stocks_data = pd.DataFrame()

print("Downloading Norwegian stock data...")
for symbol in symbols:
    try:
        # Download the data
        stock_data = yf.download(symbol, start=start_date, end=end_date, progress=False)
        
        if len(stock_data) > 0:  # Check if we got any data
            # Calculate returns relative to 2010 or first available data point
            initial_price = stock_data['Close'].iloc[0]
            returns = (stock_data['Close'] / initial_price - 1) * 100
            
            # Add to the main DataFrame
            all_stocks_data[symbol.replace('.OL', '')] = returns  # Remove .OL for cleaner labels
            print(f"Successfully downloaded {symbol}")
        else:
            print(f"No data available for {symbol}")
    except Exception as e:
        print(f"Error downloading {symbol}: {e}")

# Remove any columns with all NaN values
all_stocks_data = all_stocks_data.dropna(axis=1, how='all')

if not all_stocks_data.empty:
    # Create the plot
    plt.figure(figsize=(15, 8))

    # Plot each stock
    for column in all_stocks_data.columns:
        plt.plot(all_stocks_data.index, all_stocks_data[column], label=column, alpha=0.7, linewidth=1)

    plt.title('Norwegian Stock Returns Since 2010 (Normalized)')
    plt.xlabel('Date')
    plt.ylabel('Return (%)')
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save plot to PDF
    pdf_path = os.path.join(plots_dir, f'norwegian_stocks_returns_{datetime.now().strftime("%Y%m%d")}.pdf')
    plt.savefig(pdf_path, bbox_inches='tight', dpi=300)
    print(f"\nPlot saved to: {pdf_path}")

    # Add some statistics
    print("\nPerformance Statistics (in %):")
    stats_df = pd.DataFrame({
        'Final Return': all_stocks_data.iloc[-1],
        'Max Return': all_stocks_data.max(),
        'Min Return': all_stocks_data.min(),
        'Volatility': all_stocks_data.std()
    }).round(2)

    print("\nTop Performers:")
    print(stats_df.sort_values('Final Return', ascending=False))

    # Show the plot
    plt.show()
else:
    print("No data was successfully downloaded for any of the stocks.") 