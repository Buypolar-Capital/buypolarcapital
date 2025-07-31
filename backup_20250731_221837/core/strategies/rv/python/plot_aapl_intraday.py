

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os
import pytz
from datetime import datetime
# Adjust the import path to point to utils/data_fetchers/
from ....utils.data_fetchers.alpha_vantage import fetch_intraday_data

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', '..', 'data')  # assets/stocks/relative-value/data/
plots_dir = os.path.join(script_dir, '..', '..', 'plots')  # assets/stocks/relative-value/plots/

# Fetch data using the utility function
data = fetch_intraday_data(symbol='AAPL', interval='1min', outputsize='full', data_dir=data_dir)

# Print the date range of the data before filtering
print("Data date range before filtering:", data.index.min(), "to", data.index.max())

# Filter for regular market hours (09:30 to 16:00 Eastern Time)
data = data.between_time('09:30', '16:00')

# Remove the date filter to use the most recent data
# If you want to filter for a specific date, uncomment and adjust the line below
# data = data[data.index.date == pd.to_datetime('2025-03-20').date()]

# Check if data is empty
if data.empty:
    print("No data available for the specified time range. Check API data availability.")
    print("Available dates in data:", data.index.date)
    exit()

# Print the date range after filtering
print("Data date range after filtering:", data.index.min(), "to", data.index.max())

# Print the first few rows
print(data[['Close']].head())

# Plot the closing price
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'])

# Format x-axis as HH:MM
eastern = pytz.timezone('US/Eastern')
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M', tz=eastern))

# Set x-axis limits to 09:30 to 16:00 on the date of the data
start_date = data.index.min().date()
start_time = datetime(start_date.year, start_date.month, start_date.day, 9, 30, tzinfo=eastern)
end_time = datetime(start_date.year, start_date.month, start_date.day, 16, 0, tzinfo=eastern)
plt.xlim(start_time, end_time)

# Add titles and labels
plt.title('AAPL Intraday Stock Prices (Alpha Vantage)')
plt.xlabel('Time (HH:MM, Eastern Time)')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)

# Save the plot as a PDF in the plots folder
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
pdf_path = os.path.join(plots_dir, 'aapl_intraday_alphavantage.pdf')
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')

# Show the plot
plt.show()