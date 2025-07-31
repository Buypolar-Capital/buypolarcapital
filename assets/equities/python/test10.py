import sys
from pathlib import Path
import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.data.fetch_data import get_data_yf
from src.plotting.plotting import plot_prices

# Define tickers and date range
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA",
           "NVDA", "META", "JPM", "UNH", "NFLX"]

start = "2023-01-01"
end = "2023-10-01"

# Output path
plots_dir = os.path.join(os.getcwd(), "plots")
os.makedirs(plots_dir, exist_ok=True)
pdf_path = os.path.join(plots_dir, "buypolar_10_ticker_report.pdf")

with PdfPages(pdf_path) as pdf:
    for ticker in tickers:
        print(f"📈 Plotting {ticker}...")
        df = get_data_yf(ticker, start=start, end=end)
        
        plot_prices(
            df,
            title=f"{ticker} Stock Price Jan–Oct 2023",
            save_pdf=False,
            export_png=False,
            show=False,  # Don't render live
        )
        
        # Get the actual figure that plot_prices just created
        fig = plt.gcf()
        pdf.savefig(fig)
        plt.close(fig)


print(f"✅ Multi-page PDF saved to: {pdf_path}")
