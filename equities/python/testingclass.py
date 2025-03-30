import sys
from pathlib import Path

# Add root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Import reusable utilities
from src.data.fetch_data import get_data_yf
from src.plotting.plotting import plot_prices

# Fetch price data
df1 = get_data_yf("AAPL", start="2023-01-01", end="2023-10-01")
print(df1.head())

# Plot it and save to PDF in /plots
plot_prices(
    df1,
    title="AAPL Stock Price Jan–Oct 2023",
    save_pdf=True,
    filename="aapl_2023_price.pdf"
)
