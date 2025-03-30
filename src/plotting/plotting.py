import matplotlib.pyplot as plt
import os

def plot_prices(df, title="Price over Time", y_label="Price", save_pdf=False, filename=None):
    """
    Plots price data for one or more tickers.
    
    Args:
        df: DataFrame with columns [date, ticker, price]
        title: Plot title
        y_label: Y-axis label
        save_pdf: If True, saves the figure to ./plots/ (relative to working dir)
        filename: Optional filename (e.g., 'aapl_price.pdf')
    """
    plt.figure(figsize=(12, 6))
    for ticker in df["ticker"].unique():
        sub = df[df["ticker"] == ticker]
        plt.plot(sub["date"], sub["price"], label=ticker)
    
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    if save_pdf:
        plots_dir = os.path.join(os.getcwd(), "plots")
        os.makedirs(plots_dir, exist_ok=True)

        if filename is None:
            tickers = "-".join(df["ticker"].unique())
            filename = f"{tickers}_price_plot.pdf"

        full_path = os.path.join(plots_dir, filename)
        plt.savefig(full_path)
        print(f"✅ Saved plot to: {full_path}")

    plt.show()
