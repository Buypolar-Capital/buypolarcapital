import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from PyPDF2 import PdfMerger
import os
from datetime import datetime

# BPC Style Setup
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

# Formatter for percentage
def format_percent(x, pos):
    return f"{x:.1f}%"

# Stats text for volatility
def get_stats_text(df, column="realized_vol"):
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if len(values) == 0:
        return "No valid volatility data."

    return (
        f"BuyPolar Metrics\n\n"
        f"Max:        {values.max():.2f}%\n"
        f"Min:        {values.min():.2f}%\n"
        f"Avg:        {values.mean():.2f}%\n"
        f"Volatility: {values.std():.2f}%\n"
        f"Days:       {len(values)}"
    )

# Adapted plot function for volatility
def plot_volatility(df, title="Volatility over Time", y_label="Volatility (%)",
                   save_pdf=True, filename=None, source="Yahoo Finance",
                   export_png=True):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot realized volatility
    ax.plot(df.index, df["realized_vol"], label="Realized Volatility", linewidth=1.5, color="blue")
    
    # Plot implied volatility if available
    if "implied_vol" in df.columns:
        ax.plot(df.index, df["implied_vol"], label="Implied Volatility", linewidth=1.5, color="red", alpha=0.5)

    # Style the chart (BPC style)
    ax.set_title(title, fontsize=16, fontweight="bold", loc="center")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(format_percent))
    ax.set_facecolor("white")

    # Set background & borders
    fig.patch.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")

    # Add caption
    fig.text(0.01, 0.01, f"Source: {source} | Strategy: BuyPolar Capital",
             fontsize=9, style="italic", color="#333333")

    # Add stats box (top-left inside panel)
    stats_text = get_stats_text(df, column="realized_vol")
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
            filename = "volatility_plot.pdf"

        pdf_path = os.path.join(plots_dir, filename)
        if save_pdf:
            fig.savefig(pdf_path, bbox_inches="tight")
            print(f"✅ Saved PDF to: {pdf_path}")

        if export_png:
            png_path = pdf_path.replace(".pdf", ".png")
            fig.savefig(png_path, bbox_inches="tight", dpi=300)
            print(f"✅ Saved PNG to: {png_path}")

    plt.close(fig)

# Define indices and their corresponding implied volatility indices
indices = {
    '^GSPC': {'name': 'S&P 500', 'vol_index': '^VIX'},
    '^IXIC': {'name': 'NASDAQ', 'vol_index': '^VXN'},
    '^DJI': {'name': 'Dow Jones Industrial Average', 'vol_index': '^VXD'},
    '^GDAXI': {'name': 'DAX', 'vol_index': '^VDAX'},
    '^STOXX50E': {'name': 'EURO STOXX 50', 'vol_index': '^VSTOXX'},
    '000001.SS': {'name': 'SSE Composite', 'vol_index': '^VIXC'},
    '^AXJO': {'name': 'S&P/ASX 200', 'vol_index': None},
    '^IBEX': {'name': 'IBEX 35', 'vol_index': None},
    '^SSMI': {'name': 'Swiss Market Index', 'vol_index': None},
    '^GSPTSE': {'name': 'S&P/TSX', 'vol_index': None}
}

start_date = '1990-01-01'
end_date = '2025-01-01'
window = 21  # 21 trading days for rolling volatility
annualization_factor = np.sqrt(252)  # Annualize volatility
pdf_files = []

# Apply BPC style
set_bpc_style()

# Process each index
for ticker, info in indices.items():
    print(f"Processing {info['name']} ({ticker})...")
    
    # Download index data
    try:
        index_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(f"Failed to download data for {info['name']} ({ticker}): {e}")
        continue
    
    # Skip if no data is retrieved
    if index_data.empty:
        print(f"No data for {info['name']} ({ticker}). Skipping...")
        continue
    
    # Calculate log returns
    index_data['log_ret'] = np.log(index_data['Close'] / index_data['Close'].shift(1))
    
    # Calculate realized volatility (in percentage)
    index_data['realized_vol'] = index_data['log_ret'].rolling(window=window).std() * annualization_factor * 100
    
    # Drop NaN values
    index_data = index_data.dropna()
    
    # Prepare implied volatility data if available
    if info['vol_index']:
        try:
            vol_data = yf.download(info['vol_index'], start=start_date, end=end_date, progress=False)
            if not vol_data.empty:
                vol_data = vol_data[['Close']].rename(columns={'Close': 'implied_vol'})
                # Merge realized and implied volatility
                vol_df = index_data[['realized_vol']].join(vol_data, how='inner').dropna()
            else:
                print(f"No implied volatility data for {info['name']} ({info['vol_index']}). Plotting realized volatility only.")
                vol_df = index_data[['realized_vol']]
        except Exception as e:
            print(f"Failed to download implied volatility data for {info['name']} ({info['vol_index']}): {e}")
            vol_df = index_data[['realized_vol']]
    else:
        print(f"No implied volatility index for {info['name']}. Plotting realized volatility only.")
        vol_df = index_data[['realized_vol']]
    
    # Plot volatility with BPC style
    filename = f"{ticker.replace('.', '_')}_volatility.pdf"
    plot_volatility(
        df=vol_df,
        title=f"Realized vs Implied Volatility: {info['name']}",
        y_label="Volatility (%)",
        save_pdf=True,
        filename=filename,
        source="Yahoo Finance",
        export_png=True
    )
    pdf_files.append(os.path.join("plots", filename))

# Merge PDFs
if pdf_files:
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    output_pdf = 'plots/realized_vs_implied_volatility_merged.pdf'
    merger.write(output_pdf)
    merger.close()
    print(f"✅ Merged PDF saved as {output_pdf}")
    
    # Clean up individual PDF files
    for pdf in pdf_files:
        os.remove(pdf)
else:
    print("No plots generated. Check data availability.")