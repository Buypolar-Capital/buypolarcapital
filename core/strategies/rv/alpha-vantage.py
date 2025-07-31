from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import pytz

# Initialize the Alpha Vantage client with your API key
api_key = "U67RUCI71EEJTEXQ"
ts = TimeSeries(key=api_key, output_format='pandas')

# Fetch 1-minute intraday data for AAPL
data, meta = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')

# Rename columns to match your previous setup
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

# Filter for March 20, 2025, and regular market hours (09:30 to 16:00 Eastern Time)
data = data[data.index.date == pd.to_datetime('2025-03-20').date()]
data = data.between_time('09:30', '16:00')

# Check if data is empty
if data.empty:
    print("No data available for the specified date. Try a different date or check API availability.")
    exit()

# Print the first few rows
print(data[['Close']].head())

# Plot the closing price
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'])

# Format x-axis as HH:MM
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

# Add titles and labels
plt.title('AAPL Intraday Stock Prices (Alpha Vantage)')
plt.xlabel('Time (HH:MM, Eastern Time)')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)

# Save the plot as a PDF in the plots folder
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, '..', 'plots')
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
pdf_path = os.path.join(plots_dir, 'aapl_intraday_alphavantage.pdf')
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')

# Show the plot
plt.show()