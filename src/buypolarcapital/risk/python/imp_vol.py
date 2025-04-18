import sys
import os
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PyPDF2 import PdfMerger

# === Setup project root and centralized plots dir ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Save plots in bpc/risk-management/python/plots/
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

# === Percentage formatter ===
def format_percent(x, pos):
    return f"{x:.1f}%"

# === Adapted stats text for volatility ===
def get_vol_stats_text(df, column="realized_vol"):
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

# === Volatility plot function ===
def plot_volatility(df, title="Volatility over Time", y_label="Volatility (%)",
                   save_pdf=True, filename=None, source="Yahoo Finance",
                   export_png=True):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot realized volatility
    ax.plot(df.index, df["realized_vol"], label="Realized Volatility", linewidth=1.5, color="blue")
    
    # Plot implied volatility if available
    if "implied_vol" in df.columns:
        ax.plot(df.index, df["implied_vol"], label="Implied Volatility", linewidth=1.5, color="red", alpha=0.5)

    # Styling (BPC style)
    ax.set_title(title, fontsize=16, fontweight="bold", loc="center")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel(y_label, fontsize=11)
    ax.grid(True, which="major", linestyle="-", linewidth=0.25, color="#cccccc")
    ax.legend(loc="upper right", fontsize=10, frameon=False)
    ax.yaxis.set_major_formatter(FuncFormatter(format_percent))
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#cccccc")

    # Caption
    fig.text(0.01, 0.01, f"Source: {source} | Strategy: BuyPolar Capital",
             fontsize=9, style="italic", color="#333333")

    # Metrics box
    stats_text = get_vol_stats_text(df, column="realized_vol")
    props = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.9)
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=9, fontfamily="monospace", verticalalignment='top', bbox=props)

    plt.tight_layout()

    # Export
    if filename is None:
        filename = "volatility_plot.pdf"
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
window = 21
annualization_factor = np.sqrt(252)
pdf_files = []

# === Style Setup ===
set_bpc_style()

# === Main Loop ===
for ticker, info in indices.items():
    print(f"📈 Processing {info['name']} ({ticker})...")

    try:
        index_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    except Exception as e:
        print(f"❌ Failed to download {ticker}: {e}")
        continue

    if index_data.empty:
        print(f"⚠️ No data for {ticker}. Skipping...")
        continue

    # Compute realized volatility
    index_data['log_ret'] = np.log(index_data['Close'] / index_data['Close'].shift(1))
    index_data['realized_vol'] = index_data['log_ret'].rolling(window).std() * annualization_factor * 100
    index_data = index_data.dropna()

    # Join implied vol
    if info['vol_index']:
        try:
            vol_data = yf.download(info['vol_index'], start=start_date, end=end_date, progress=False)
            if not vol_data.empty:
                vol_data = vol_data[['Close']].rename(columns={'Close': 'implied_vol'})
                vol_df = index_data[['realized_vol']].join(vol_data, how='inner').dropna()
            else:
                print(f"⚠️ No implied vol for {info['vol_index']}.")
                vol_df = index_data[['realized_vol']]
        except Exception as e:
            print(f"❌ Error downloading {info['vol_index']}: {e}")
            vol_df = index_data[['realized_vol']]
    else:
        print(f"⚠️ No implied volatility index for {info['name']}. Plotting realized volatility only.")
        vol_df = index_data[['realized_vol']]

    # Plot and save
    filename = f"{ticker.replace('.', '_')}_volatility.pdf"
    plot_volatility(
        df=vol_df,
        title=f"Realized vs Implied Volatility: {info['name']}",
        filename=filename
    )
    pdf_files.append(os.path.join(PLOTS_DIR, filename))

# === Merge PDFs ===
if pdf_files:
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    output_pdf = os.path.join(PLOTS_DIR, 'realized_vs_implied_volatility_merged.pdf')
    merger.write(output_pdf)
    merger.close()
    print(f"\n✅ Merged PDF saved to: {output_pdf}")

    # Optional cleanup
    for pdf in pdf_files:
        os.remove(pdf)
else:
    print("⚠️ No plots generated.")