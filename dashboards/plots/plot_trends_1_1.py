import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def format_dollar(x, pos):
    return f"${x:,.0f}"

def get_stats_text(df):
    prices = df["price"]
    total_return = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
    return (
        f"BuyPolar Metrics\n\n"
        f"Return:     {total_return:+.1f}%\n"
        f"Max:        ${prices.max():.2f}\n"
        f"Min:        ${prices.min():.2f}\n"
        f"Avg:        ${prices.mean():.2f}\n"
        f"Volatility: {prices.std():.2f}\n"
        f"Days:       {len(prices)}"
    )

def plot_prices(df, title="Price over Time", y_label="Price",
                save_pdf=False, filename=None, source="Yahoo Finance",
                export_png=True, show=True):
    tickers = df["ticker"].unique()
    fig, ax = plt.subplots(figsize=(12, 6))

    for ticker in tickers:
        sub = df[df["ticker"] == ticker]
        ax.plot(sub["date"], sub["price"], label=ticker, linewidth=1.5)

    ax.set_title(title, fontsize=16, fontweight="bold", loc="center")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(format_dollar))
    ax.set_facecolor("white")

    fig.patch.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")

    fig.text(0.01, 0.01, f"Source: {source} | Strategy: BuyPolar Capital",
             fontsize=9, style="italic", color="#333333")

    stats_text = get_stats_text(df)
    props = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.9)
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, fontfamily="monospace", verticalalignment='top',
            bbox=props)

    plt.tight_layout()

    plots_dir = os.path.join(os.getcwd(), "plots")
    os.makedirs(plots_dir, exist_ok=True)

    if filename is None:
        tickers_str = "-".join(tickers)
        filename = f"{tickers_str}_price_plot.pdf"

    pdf_path = os.path.join(plots_dir, filename)
    if save_pdf:
        fig.savefig(pdf_path, bbox_inches="tight")
        print(f"✅ Saved PDF to: {pdf_path}")

    if export_png:
        png_path = pdf_path.replace(".pdf", ".png")
        fig.savefig(png_path, bbox_inches="tight", dpi=300)
        print(f"✅ Saved PNG to: {png_path}")

    if show:
        plt.show()

def set_bpc_style():
    plt.rcParams.update({
        "axes.edgecolor": "#cccccc",
        "axes.grid": True,
        "grid.color": "#cccccc",
        "grid.linestyle": "-",
        "grid.linewidth": 0.25,
        "axes.titlesize": 16,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": "sans-serif",
    })

# Run the plots
set_bpc_style()

ticker_groups = {
    "indices": {"S&P 500": "^GSPC", "NASDAQ": "^IXIC", "OSEBX": "^OSEAX"},
    "commodities": {"Gold": "GC=F", "Brent": "BZ=F"},
    "fixed_income": {"10Y US": "^TNX", "10Y Norway": "^IRX"},
    "crypto": {"BTC": "BTC-USD", "ETH": "ETH-USD"}
}

end_date = datetime.today()
start_date = end_date - timedelta(days=60)

for group, tickers in ticker_groups.items():
    all_data = []
    for name, symbol in tickers.items():
        try:
            df = yf.download(symbol, start=start_date, end=end_date)
            df = df[["Close"]].dropna().reset_index()
            df.columns = ["date", "price"]
            df["ticker"] = name
            all_data.append(df)
        except Exception as e:
            print(f"Error fetching {name}: {e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        plot_prices(
            combined_df,
            title=f"{group.title()} Price Trends",
            filename=f"{group}_trend.png",
            save_pdf=True,
            export_png=True,
            show=False
        )
