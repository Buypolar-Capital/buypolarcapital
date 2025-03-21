from polygon import RESTClient
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import os

# Initialize the client with your new API key
api_key = "gzVm12cSEvBEDEBiw_3aXEnTzjpZixul"
client = RESTClient(api_key=api_key)

# Fetch 1-minute bars for AAPL on March 21, 2025
ticker = "AAPL"
bars = client.get_aggs(
    ticker=ticker,
    multiplier=1,  # 1-minute intervals
    timespan="minute",
    from_="2025-03-21",
    to="2025-03-21",
    limit=50000  # Max number of results
)

# Convert to DataFrame
data = pd.DataFrame(bars)
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')  # Convert timestamp to datetime
data = data.rename(columns={
    'o': 'Open',
    'h': 'High',
    'l': 'Low',
    'c': 'Close',
    'v': 'Volume'
})

# Filter for regular market hours (09:30 to 16:00 Eastern Time)
data = data.set_index('timestamp')
data = data.between_time('09:30', '16:00')

# Print the first few rows
print(data[['Close']].head())

# Plot the closing price
plt.figure(figsize=(10, 5))
plt.plot(data.index, data['Close'])

# Format x-axis as HH:MM
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M'))

# Add titles and labels
plt.title('AAPL Intraday Stock Prices (Polygon.io)')
plt.xlabel('Time (HH:MM, Eastern Time)')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)

# Save the plot as a PDF in the plots folder
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, '..', 'plots')
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)
pdf_path = os.path.join(plots_dir, 'aapl_intraday_polygon.pdf')
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')

# Show the plot
plt.show()