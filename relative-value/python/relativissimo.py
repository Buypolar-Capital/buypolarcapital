import sys
import os
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib
# Set backend to Agg to avoid tkinter issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PyPDF2 import PdfMerger

# === Setup project root and centralized plots dir ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Save plots in bpc/relative-value/python/plots/
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

# Debug: Print paths to diagnose
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"PLOTS_DIR: {PLOTS_DIR}")
print(f"Adding to sys.path: {os.path.join(PROJECT_ROOT, 'src')}")

# === Add src/ to path ===
sys.path.append(os.path.join(PROJECT_ROOT, "src"))

# Debug: Print sys.path before import
print(f"sys.path: {sys.path}")

# === Import from plotting ===
try:
    from plotting.plotting import set_bpc_style, get_stats_text
except ModuleNotFoundError as e:
    print(f"Import error: {e}")
    print("Ensure plotting.py is in bpc/src/plotting/ and contains set_bpc_style, get_stats_text")
    sys.exit(1)

# === Formatters ===
def format_dollar(x, pos):
    return f"${x:,.0f}"

def format_ratio(x, pos):
    return f"{x:.2f}"

# === Adapted stats text for ratio ===
def get_ratio_stats_text(df, column="ratio"):
    values = pd.to_numeric(df[column], errors="coerce").dropna()
    if len(values) == 0:
        return "No valid ratio data."

    return (
        f"BuyPolar Metrics\n\n"
        f"Max:        {values.max():.2f}\n"
        f"Min:        {values.min():.2f}\n"
        f"Avg:        {values.mean():.2f}\n"
        f"Volatility: {values.std():.2f}\n"
        f"Days:       {len(values)}"
    )

# === Plot function for dually listed stocks ===
def plot_dual_stocks(df, title="Stock Prices and Ratio", ticker_a="", ticker_b="", source="Yahoo Finance",
                     save_pdf=True, filename=None, export_png=True):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # Top chart: Stock prices
    ax1.plot(df.index, df['price_a'], label=f"{ticker_a} Price", linewidth=1.5, color="blue")
    ax1.plot(df.index, df['price_b'], label=f"{ticker_b} Price", linewidth=1.5, color="red", alpha=0.5)
    ax1.set_title(title, fontsize=16, fontweight="bold", loc="center")
    ax1.set_ylabel("Price ($)", fontsize=11)
    ax1.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax1.legend(loc="upper right", fontsize=10, frameon=False)
    ax1.yaxis.set_major_formatter(FuncFormatter(format_dollar))
    ax1.set_facecolor("white")

    # Bottom chart: A/B ratio
    ax2.plot(df.index, df['ratio'], label=f"{ticker_a}/{ticker_b} Ratio", linewidth=1.5, color="green")
    ax2.set_xlabel("Date", fontsize=11)
    ax2.set_ylabel("Ratio", fontsize=11)
    ax2.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax2.legend(loc="upper right", fontsize=10, frameon=False)
    ax2.yaxis.set_major_formatter(FuncFormatter(format_ratio))
    ax2.set_facecolor("white")

    # Set background & borders
    fig.patch.set_facecolor("white")
    for ax in [ax1, ax2]:
        for spine in ax.spines.values():
            spine.set_edgecolor("#cccccc")

    # Caption
    fig.text(0.01, 0.01, f"Source: {source} | Strategy: BuyPolar Capital",
             fontsize=9, style="italic", color="#333333")

    # Metrics box (for ratio) on bottom chart
    stats_text = get_ratio_stats_text(df, column="ratio")
    props = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.9)
    ax2.text(0.02, 0.98, stats_text, transform=ax2.transAxes,
             fontsize=9, fontfamily="monospace", verticalalignment='top', bbox=props)

    plt.tight_layout()

    # Export
    if filename is None:
        filename = "dual_stock_plot.pdf"
    pdf_path = os.path.join(PLOTS_DIR, filename)

    if save_pdf:
        fig.savefig(pdf_path, bbox_inches="tight")
        print(f"✅ Saved PDF to: {pdf_path}")
    if export_png:
        png_path = pdf_path.replace(".pdf", ".png")
        fig.savefig(png_path, bbox_inches="tight", dpi=300)
        print(f"✅ Saved PNG to: {png_path}")
    plt.close(fig)

# === Configs ===
stocks = [
    {'name': 'Acciona', 'ticker_a': 'ANA.MC', 'ticker_b': 'ANE.MC'},
    {'name': 'Alphabet', 'ticker_a': 'GOOGL', 'ticker_b': 'GOOG'},
    {'name': 'Atlas Copco', 'ticker_a': 'ATCO-A.ST', 'ticker_b': 'ATCO-B.ST'},
    {'name': 'BMW', 'ticker_a': 'BMW.DE', 'ticker_b': 'BMW3.DE'},
    {'name': 'CK Hutchison Holdings Ltd', 'ticker_a': '0001.HK', 'ticker_b': '1038.HK'},
    {'name': 'EDP', 'ticker_a': 'EDP.LS', 'ticker_b': 'EDPR.LS'},
    {'name': 'Epiroc', 'ticker_a': 'EPI-A.ST', 'ticker_b': 'EPI-B.ST'},
    {'name': 'Fox Corp', 'ticker_a': 'FOXA', 'ticker_b': 'FOX'},
    {'name': 'Grifols', 'ticker_a': 'GRF.MC', 'ticker_b': 'GRF-P.MC'},
    {'name': 'Heico', 'ticker_a': 'HEI', 'ticker_b': 'HEI-A'},
    {'name': 'Heineken', 'ticker_a': 'HEIO.AS', 'ticker_b': 'HEIA.AS'},
    {'name': 'Henkel', 'ticker_a': 'HEN.DE', 'ticker_b': 'HEN3.DE'},
    {'name': 'Industrivärden', 'ticker_a': 'INDU-A.ST', 'ticker_b': 'INDU-C.ST'},
    {'name': 'Investor AB', 'ticker_a': 'INVE-A.ST', 'ticker_b': 'INVE-B.ST'},
    {'name': 'Japan Post', 'ticker_a': '6178.T', 'ticker_b': '6178.T'},  # Note: 7128 invalid, using 6178.T
    {'name': 'Las Vegas Sands', 'ticker_a': 'LVS', 'ticker_b': '1928.HK'},
    {'name': 'Liberty Global', 'ticker_a': 'LBTYA', 'ticker_b': 'LBTYK'},
    {'name': 'Lindt', 'ticker_a': 'LISN.SW', 'ticker_b': 'LISP.SW'},
    {'name': 'Møller-Maersk', 'ticker_a': 'MAERSK-A.CO', 'ticker_b': 'MAERSK-B.CO'},
    {'name': 'NTT', 'ticker_a': '9432.T', 'ticker_b': '9613.T'},
    {'name': 'Porsche', 'ticker_a': 'PAH3.DE', 'ticker_b': 'P911.DE'},
    {'name': 'Rio Tinto', 'ticker_a': 'RIO.AX', 'ticker_b': 'RIO.L'},
    {'name': 'Roche', 'ticker_a': 'ROG.SW', 'ticker_b': 'RO.SW'},
    {'name': 'Sartorius', 'ticker_a': 'SRT.DE', 'ticker_b': 'SRT3.DE'},
    {'name': 'Schindler', 'ticker_a': 'SCHN.SW', 'ticker_b': 'SCHP.SW'},
    {'name': 'Swatch', 'ticker_a': 'UHR.SW', 'ticker_b': 'UHRN.SW'},
    {'name': 'Swire', 'ticker_a': '0019.HK', 'ticker_b': '1972.HK'},
    {'name': 'Volkswagen', 'ticker_a': 'VOW.DE', 'ticker_b': 'VOW3.DE'},
    {'name': 'Volvo', 'ticker_a': 'VOLV-A.ST', 'ticker_b': 'VOLV-B.ST'},
    {'name': 'Rockwool', 'ticker_a': 'ROCK-A.CO', 'ticker_b': 'ROCK-B.CO'},
    {'name': 'Berkshire Hathaway', 'ticker_a': 'BRK-A', 'ticker_b': 'BRK-B'},
    {'name': 'Schibsted', 'ticker_a': 'SCHA.OL', 'ticker_b': 'SCHB.OL'},
    {'name': 'Essity', 'ticker_a': 'ESSITY-A.ST', 'ticker_b': 'ESSITY-B.ST'},
    {'name': 'Electrolux', 'ticker_a': 'ELUX-A.ST', 'ticker_b': 'ELUX-B.ST'}
]

start_date = '1990-01-01'
end_date = '2025-01-01'
pdf_files = []

# === Style Setup ===
set_bpc_style()

# === Batch Download All Tickers ===
# Collect all unique tickers
all_tickers = set()
for stock in stocks:
    all_tickers.add(stock['ticker_a'])
    all_tickers.add(stock['ticker_b'])
all_tickers = list(all_tickers)

print(f"Downloading data for {len(all_tickers)} tickers...")
try:
    # Download all tickers in one request
    data = yf.download(all_tickers, start=start_date, end=end_date, progress=True, group_by='ticker')
except Exception as e:
    print(f"❌ Failed to download ticker data: {e}")
    sys.exit(1)

# === Main Loop ===
for stock in stocks:
    name = stock['name']
    ticker_a = stock['ticker_a']
    ticker_b = stock['ticker_b']
    print(f"📈 Processing {name} ({ticker_a} vs {ticker_b})...")

    # Skip if tickers are identical (e.g., Japan Post)
    if ticker_a == ticker_b:
        print(f"⚠️ Tickers are identical ({ticker_a} vs {ticker_b}). Skipping...")
        continue

    # Extract closing prices for both tickers
    try:
        if ticker_a in data and ticker_b in data:
            price_a = data[ticker_a]['Close']
            price_b = data[ticker_b]['Close']
        else:
            print(f"⚠️ Data not available for {ticker_a} or {ticker_b}. Skipping...")
            continue
    except KeyError as e:
        print(f"⚠️ Error accessing data for {ticker_a} or {ticker_b}: {e}. Skipping...")
        continue

    # Prepare DataFrame
    df = pd.DataFrame()
    df['price_a'] = price_a
    df['price_b'] = price_b
    df = df.dropna()

    if df.empty:
        print(f"⚠️ No overlapping data for {ticker_a} and {ticker_b}. Skipping...")
        continue

    # Compute A/B ratio
    df['ratio'] = df['price_a'] / df['price_b']

    # Plot and save
    filename = f"{ticker_a.replace('.', '_')}_vs_{ticker_b.replace('.', '_')}_relative.pdf"
    plot_dual_stocks(
        df=df,
        title=f"Dually Listed Stocks: {name}",
        ticker_a=ticker_a,
        ticker_b=ticker_b,
        filename=filename
    )
    pdf_files.append(os.path.join(PLOTS_DIR, filename))

# === Merge PDFs ===
if pdf_files:
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    output_pdf = os.path.join(PLOTS_DIR, 'dually_listed_stocks_merged.pdf')
    merger.write(output_pdf)
    merger.close()
    print(f"\n✅ Merged PDF saved to: {output_pdf}")

    # Optional cleanup
    for pdf in pdf_files:
        os.remove(pdf)
else:
    print("⚠️ No plots generated.")