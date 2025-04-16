import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from PyPDF2 import PdfMerger
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
import sys

# Check for required dependencies
required_packages = ['yfinance', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy', 'PyPDF2']
missing_packages = []
for pkg in required_packages:
    try:
        __import__(pkg)
    except ImportError:
        missing_packages.append(pkg)

if missing_packages:
    print(f"Error: Missing required packages: {', '.join(missing_packages)}")
    print("Install them using: pip install " + " ".join(missing_packages))
    sys.exit(1)

# Set style for professional plots
try:
    plt.style.use('seaborn-v0_8')
except OSError:
    plt.style.use('default')
sns.set_palette("deep")

# Create directories
os.makedirs("plots", exist_ok=True)
os.makedirs("data", exist_ok=True)

# IPOs
ipos = [
    ("ABNB", "2020-12-10"), ("SNOW", "2020-09-16"), ("RIVN", "2021-11-10"),
    ("COIN", "2021-04-14"), ("UBER", "2019-05-10"), ("LYFT", "2019-03-29"),
    ("PLTR", "2020-09-30"), ("TSLA", "2010-06-29"), ("BABA", "2014-09-19"),
    ("META", "2012-05-18"), ("SPOT", "2018-04-03"), ("DBX", "2018-03-23")
]

# Benchmark and parameters
benchmark_ticker = "^GSPC"
event_window_days = 21  # Number of trading days post-IPO
estimation_window_days = 60
pdf_paths = []
all_car_data = []
all_ar_data = []

def calculate_rolling_beta(stock_returns, benchmark_returns, window=30):
    """Calculate rolling beta using past window days"""
    cov = stock_returns.rolling(window).cov(benchmark_returns)
    var = benchmark_returns.rolling(window).var()
    beta = cov / var
    return beta.bfill()  # Handle NaNs

def create_cover_page():
    """Create a cover page for the PDF report"""
    fig = plt.figure(figsize=(8.5, 11))
    plt.text(0.5, 0.8, 'IPO Event Study Analysis', ha='center', va='center', fontsize=24, fontweight='bold')
    plt.text(0.5, 0.65, 'Advanced Analytics of IPO Abnormal Returns', ha='center', va='center', fontsize=16)
    plt.text(0.5, 0.5, f'Generated on: {datetime.now().strftime("%Y-%m-%d")}', ha='center', va='center', fontsize=12)
    plt.text(0.5, 0.35, 'Prepared by: Grok Analysis', ha='center', va='center', fontsize=12)
    plt.axis('off')
    return fig

# Main analysis loop
for ticker, ipo_date in ipos:
    try:
        ipo_date = pd.to_datetime(ipo_date)
        start_date = ipo_date - pd.Timedelta(days=estimation_window_days)
        end_date = ipo_date + pd.Timedelta(days=event_window_days * 2)  # Buffer for trading days

        # Download data
        stock_data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
        benchmark_data = yf.download(benchmark_ticker, start=start_date, end=end_date, auto_adjust=True)

        if stock_data.empty or benchmark_data.empty:
            print(f"Data missing for {ticker}, skipping...")
            continue

        # Calculate returns
        stock_returns = stock_data['Close'].pct_change()
        benchmark_returns = benchmark_data['Close'].pct_change()
        stock_volume = stock_data['Volume']

        # Align data
        returns = pd.concat([stock_returns, benchmark_returns, stock_volume], axis=1)
        returns.columns = ['Stock', 'Benchmark', 'Volume']
        returns = returns.dropna()

        # Calculate abnormal returns and beta
        returns['Abnormal'] = returns['Stock'] - returns['Benchmark']
        returns['Beta'] = calculate_rolling_beta(returns['Stock'], returns['Benchmark'])
        returns['Volatility'] = returns['Stock'].rolling(20).std() * np.sqrt(252)

        # Event window data (select first 21 trading days after IPO)
        event_returns = returns.loc[ipo_date:].head(event_window_days).copy()
        if len(event_returns) < 10:  # Require at least 10 trading days
            print(f"Insufficient event window data for {ticker} ({len(event_returns)} trading days), skipping...")
            continue
        event_returns.reset_index(inplace=True)
        event_returns['EventDay'] = range(len(event_returns))  # Match length of data
        event_returns['CAR'] = event_returns['Abnormal'].cumsum()

        # Statistical tests
        t_stat, p_value = stats.ttest_1samp(event_returns['Abnormal'].dropna(), 0)
        stats_summary = {
            'Ticker': ticker,
            'Mean_AR': event_returns['Abnormal'].mean(),
            'T_Stat': t_stat,
            'P_Value': p_value,
            'Mean_CAR': event_returns['CAR'].mean(),
            'Volatility': event_returns['Volatility'].mean()
        }

        # Save data
        csv_path = f"data/ipo_returns_{ticker}.csv"
        event_returns.to_csv(csv_path, index=False)

        # Store for comparative analysis
        all_car_data.append(event_returns[['EventDay', 'CAR']].set_index('EventDay').rename(columns={'CAR': ticker}))
        all_ar_data.append(event_returns[['EventDay', 'Abnormal']].set_index('EventDay').rename(columns={'Abnormal': ticker}))

        # Create PDF for this ticker
        pdf_path = f"plots/ipo_analysis_{ticker}.pdf"
        with PdfPages(pdf_path) as pdf:
            # Plot 1: CAR and AR
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            ax1.plot(event_returns['EventDay'], event_returns['CAR'], marker='o', label='CAR')
            ax1.axhline(0, color='gray', linestyle='--')
            ax1.axvline(0, color='red', linestyle=':', label='IPO Day')
            ax1.set_title(f'{ticker}: Cumulative Abnormal Returns')
            ax1.set_ylabel('CAR')
            ax1.grid(True)
            ax1.legend()

            ax2.bar(event_returns['EventDay'], event_returns['Abnormal'], color='skyblue')
            ax2.axhline(0, color='gray', linestyle='--')
            ax2.axvline(0, color='red', linestyle=':')
            ax2.set_title(f'{ticker}: Daily Abnormal Returns')
            ax2.set_xlabel('Days since IPO')
            ax2.set_ylabel('AR')
            ax2.grid(True)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plot 2: Volume and Volatility
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
            ax1.plot(event_returns['EventDay'], event_returns['Volume'], marker='o', color='purple')
            ax1.set_title(f'{ticker}: Trading Volume')
            ax1.set_ylabel('Volume')
            ax1.grid(True)

            ax2.plot(event_returns['EventDay'], event_returns['Volatility'], marker='o', color='orange')
            ax2.set_title(f'{ticker}: Volatility')
            ax2.set_xlabel('Days since IPO')
            ax2.set_ylabel('Annualized Volatility')
            ax2.grid(True)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plot 3: Beta Evolution
            plt.figure(figsize=(10, 4))
            plt.plot(event_returns['EventDay'], event_returns['Beta'], marker='o', color='green')
            plt.axhline(1, color='gray', linestyle='--')
            plt.axvline(0, color='red', linestyle=':', label='IPO Day')
            plt.title(f'{ticker}: Rolling Beta')
            plt.xlabel('Days since IPO')
            plt.ylabel('Beta')
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            pdf.savefig()
            plt.close()

        pdf_paths.append(pdf_path)
        print(f"Successfully processed {ticker}")

    except Exception as e:
        print(f"Error processing {ticker}: {str(e)}")
        continue

# Comparative Analysis
if all_car_data and all_ar_data:
    # Align data for comparison
    max_days = min(max(len(df) for df in all_car_data), event_window_days)
    all_car_df = pd.concat([df.iloc[:max_days] for df in all_car_data], axis=1)
    all_ar_df = pd.concat([df.iloc[:max_days] for df in all_ar_data], axis=1)

    # Create comparative PDF
    comp_pdf_path = "plots/ipo_comparative_analysis.pdf"
    with PdfPages(comp_pdf_path) as pdf:
        # Plot 1: All CARs
        plt.figure(figsize=(12, 6))
        for ticker in all_car_df.columns:
            plt.plot(all_car_df.index, all_car_df[ticker], marker='o', label=ticker)
        plt.axhline(0, color='gray', linestyle='--')
        plt.axvline(0, color='red', linestyle=':', label='IPO Day')
        plt.title('Comparative Cumulative Abnormal Returns')
        plt.xlabel('Trading Days since IPO')
        plt.ylabel('CAR')
        plt.grid(True)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

        # Plot 2: AR Heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(all_ar_df.T, cmap='RdBu', center=0, annot=True, fmt='.3f')
        plt.title('Abnormal Returns Heatmap Across IPOs')
        plt.xlabel('Trading Days since IPO')
        plt.ylabel('Company')
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    pdf_paths.append(comp_pdf_path)
    print("Generated comparative analysis PDF")

# Create final merged PDF with cover page
final_pdf_path = "plots/ipo_event_study_advanced.pdf"
merger = PdfMerger()

# Add cover page
cover_pdf = "plots/cover_page.pdf"
try:
    with PdfPages(cover_pdf) as pdf:
        pdf.savefig(create_cover_page())
        plt.close()
    merger.append(cover_pdf)
except Exception as e:
    print(f"Error creating cover page: {str(e)}")

# Add all individual and comparative PDFs
for path in pdf_paths:
    try:
        merger.append(path)
    except Exception as e:
        print(f"Error merging {path}: {str(e)}")

try:
    merger.write(final_pdf_path)
    print(f"Advanced IPO event study PDF saved as: {final_pdf_path}")
except Exception as e:
    print(f"Error saving final PDF: {str(e)}")
finally:
    merger.close()

# Clean up temporary cover page
if os.path.exists(cover_pdf):
    try:
        os.remove(cover_pdf)
    except Exception as e:
        print(f"Error removing temporary cover page: {str(e)}")
