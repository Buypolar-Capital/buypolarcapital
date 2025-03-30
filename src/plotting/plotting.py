import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
from matplotlib.ticker import FuncFormatter
from datetime import datetime

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
                export_png=True, show=True):  # ← new param


    tickers = df["ticker"].unique()
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot lines
    for ticker in tickers:
        sub = df[df["ticker"] == ticker]
        ax.plot(sub["date"], sub["price"], label=ticker, linewidth=1.5)

    # Style the chart
    ax.set_title(title, fontsize=16, fontweight="bold", loc="center")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(format_dollar))
    ax.set_facecolor("white")

    # Set background & borders
    fig.patch.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")

    # Add caption
    fig.text(0.01, 0.01, f"Source: {source} | Strategy: BuyPolar Capital",
             fontsize=9, style="italic", color="#333333")

    # Add stats box (top-left inside panel)
    stats_text = get_stats_text(df)
    props = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.9)
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, fontfamily="monospace", verticalalignment='top',
            bbox=props)

    plt.tight_layout()

    # Export
    if save_pdf or export_png:
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

