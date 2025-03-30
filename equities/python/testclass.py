import sys
from pathlib import Path

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.data.fetch_data import get_data_yf
from src.plotting.plotting import plot_prices


df = get_data_yf("AAPL", start="2023-01-01", end="2023-10-01")

plot_prices(
    df,
    title="AAPL Stock Price Jan–Oct 2023",
    save_pdf=True,
    filename="aapl_2023_buyPolar_plot.pdf",
    source="Yahoo Finance"
)
