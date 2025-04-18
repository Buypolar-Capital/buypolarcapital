
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os
import pytz

def fetch_intraday_data(symbol, interval='1min', outputsize='full', api_key="U67RUCI71EEJTEXQ", data_dir=None):
    """
    Fetch intraday data from Alpha Vantage and save it to a CSV.
    Args:
        symbol (str): Stock ticker (e.g., 'AAPL').
        interval (str): Time interval (e.g., '1min').
        outputsize (str): 'compact' or 'full'.
        api_key (str): Alpha Vantage API key.
        data_dir (str): Directory to save the CSV.
    Returns:
        pd.DataFrame: Intraday data.
    """
    # Define the CSV path
    csv_path = os.path.join(data_dir, f'{symbol}_intraday_alphavantage.csv')

    # Check if data exists locally
    if os.path.exists(csv_path):
        print("Loading data from local CSV...")
        data = pd.read_csv(csv_path, index_col='timestamp', parse_dates=True)
    else:
        print("Fetching data from Alpha Vantage...")
        # Initialize the Alpha Vantage client
        ts = TimeSeries(key=api_key, output_format='pandas')

        # Fetch data
        data, meta = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)

        # Rename columns
        data = data.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })

        # Convert index to datetime and set to Eastern Time
        data.index = pd.to_datetime(data.index)
        eastern = pytz.timezone('US/Eastern')
        data.index = data.index.tz_localize('UTC').tz_convert(eastern)

        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Save to CSV
        data.to_csv(csv_path)
        print(f"Data saved to {csv_path}")

    return data