import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pytz
import os

# Get intraday data for AAPL
ticker = "AAPL"
stock = yf.Ticker(ticker)
intraday_data = stock.history(period="1d", interval="1m")

# Ensure the index is in US Eastern Time
eastern = pytz.timezone('US/Eastern')
intraday_data.index = intraday_data.index.tz_convert(eastern)

# Filter for regular market hours (09:30 to 16:00 Eastern Time)
intraday_data = intraday_data.between_time('09:30', '16:00')

# Plot the closing price
plt.figure(figsize=(10, 5))
plt.plot(intraday_data['Close'])

# Format x-axis as HH:MM
plt.gca().xaxis.set_major_formatter(DateFormatter('%H:%M', tz=eastern))

# Add titles and labels
plt.title('AAPL Intraday Stock Prices')
plt.xlabel('Time (HH:MM, Eastern Time)')
plt.ylabel('Price (USD)')
plt.grid(True)
plt.xticks(rotation=45)

# Save the plot as a PDF in the plots folder (one directory up, then into plots)
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script (python folder)
plots_dir = os.path.join(script_dir, '..', 'plots')  # Go up one level and into plots folder
pdf_path = os.path.join(plots_dir, 'aapl_intraday_plot.pdf')  # Define the PDF file path
plt.savefig(pdf_path, format='pdf', bbox_inches='tight')  # Save as PDF

# Show the plot
plt.show()