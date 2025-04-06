import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
import seaborn as sns

# Set up paths
RAW_PATH = Path("data/raw/minute")
SIM_PATH = Path("data/simulated/exec_dataset.parquet")
PRED_PATH = Path("results/eval_predictions.csv")
PLOT_DIR = Path("plots")
PLOT_DIR.mkdir(exist_ok=True)

# Load data
raw_files = list(RAW_PATH.glob("*.parquet"))
sim_df = pd.read_parquet(SIM_PATH)
pred_df = pd.read_csv(PRED_PATH)

# Merge pred_df with sim_df to get order_size and vwap
pred_df = pred_df.merge(sim_df[["ticker", "date", "start_time", "order_size", "vwap"]], 
                        on=["ticker", "date", "start_time"], 
                        how="left")

# Example tickers for detailed plots
example_tickers = ["AAPL", "TSLA", "BABA", "ASML", "YAR.OL"]

# Initialize PDF
with PdfPages(PLOT_DIR / "model_performance.pdf") as pdf:
    # 1. Slippage Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(pred_df["true_slippage"], bins=50, label="True", alpha=0.5)
    sns.histplot(pred_df["predicted_slippage"], bins=50, label="Predicted", alpha=0.5)
    plt.title("Slippage Distribution")
    plt.xlabel("Slippage")
    plt.legend()
    pdf.savefig()
    plt.close()

    # 2. Prediction Error Distribution
    pred_df["error"] = pred_df["true_slippage"] - pred_df["predicted_slippage"]
    plt.figure(figsize=(10, 6))
    sns.histplot(pred_df["error"], bins=50)
    plt.title("Prediction Error Distribution")
    plt.xlabel("Error (True - Predicted)")
    pdf.savefig()
    plt.close()

    # 3. True vs. Predicted Slippage
    plt.figure(figsize=(10, 6))
    plt.scatter(pred_df["true_slippage"], pred_df["predicted_slippage"], alpha=0.3)
    plt.plot([-2, 1], [-2, 1], 'r--')  # 45-degree line
    plt.title("True vs. Predicted Slippage")
    plt.xlabel("True Slippage")
    plt.ylabel("Predicted Slippage")
    pdf.savefig()
    plt.close()

    # 4. MAE Over Time
    pred_df["minutes_since_open"] = pd.to_numeric(pred_df["start_time"].str.split(":").str[0]) * 60 + pd.to_numeric(pred_df["start_time"].str.split(":").str[1])
    mae_by_time = pred_df.groupby("minutes_since_open", as_index=False).apply(
        lambda x: np.mean(np.abs(x["true_slippage"] - x["predicted_slippage"])), include_groups=False
    )
    plt.figure(figsize=(10, 6))
    plt.plot(pred_df["minutes_since_open"].unique(), mae_by_time)
    plt.title("MAE Over Time of Day")
    plt.xlabel("Minutes Since Open")
    plt.ylabel("MAE")
    pdf.savefig()
    plt.close()

    # 5. R² Per Ticker
    r2_by_ticker = pred_df.groupby("ticker").apply(
        lambda x: 1 - np.sum((x["true_slippage"] - x["predicted_slippage"])**2) / np.sum((x["true_slippage"] - x["true_slippage"].mean())**2), include_groups=False
    )
    plt.figure(figsize=(12, 6))
    plt.bar(r2_by_ticker.index, r2_by_ticker.values)
    plt.title("R² Score Per Ticker")
    plt.xlabel("Ticker")
    plt.ylabel("R²")
    plt.xticks(rotation=45)
    pdf.savefig()
    plt.close()

    # 6-10. VWAP Through the Day (5 Tickers)
    for ticker in example_tickers:
        ticker_df = sim_df[sim_df["ticker"] == ticker]
        plt.figure(figsize=(10, 6))
        plt.plot(ticker_df["minutes_since_open"], ticker_df["vwap"], label="VWAP")
        plt.twinx()
        plt.bar(ticker_df["minutes_since_open"], ticker_df["order_size"], alpha=0.3, color="gray", label="Order Size")
        plt.title(f"VWAP Through the Day - {ticker}")
        plt.xlabel("Minutes Since Open")
        plt.ylabel("VWAP")
        plt.legend(loc="upper left")
        pdf.savefig()
        plt.close()

    # 11-15. Price and Volume (5 Tickers)
    for ticker in example_tickers:
        raw_df = pd.read_parquet(RAW_PATH / f"{ticker}.parquet")
        raw_df = raw_df[raw_df.index.date == pd.Timestamp("2025-04-04").date()]
        if isinstance(raw_df.columns, pd.MultiIndex):
            raw_df.columns = raw_df.columns.get_level_values(0)  # Flatten MultiIndex
        plt.figure(figsize=(10, 6))
        plt.plot(raw_df.index, raw_df["Close"], label="Close")
        plt.twinx()
        plt.bar(raw_df.index, raw_df["Volume"].values, alpha=0.3, color="gray", label="Volume")
        plt.title(f"Price and Volume - {ticker}")
        plt.xlabel("Time")
        plt.ylabel("Close Price")
        plt.legend(loc="upper left")
        plt.xticks(rotation=45)
        pdf.savefig()
        plt.close()

    # 16. Cumulative Volume Ratio
    plt.figure(figsize=(10, 6))
    plt.scatter(sim_df["minutes_since_open"], sim_df["volume_ratio"], alpha=0.3)
    plt.title("Cumulative Volume Ratio vs. Time")
    plt.xlabel("Minutes Since Open")
    plt.ylabel("Volume Ratio")
    pdf.savefig()
    plt.close()

    # 17. Slippage vs. Volatility
    plt.figure(figsize=(10, 6))
    plt.scatter(sim_df["price_volatility"], sim_df["slippage"], alpha=0.3)
    plt.title("Slippage vs. Price Volatility")
    plt.xlabel("Price Volatility")
    plt.ylabel("Slippage")
    pdf.savefig()
    plt.close()

    # 18. Portfolio Simulation (Simple Example)
    portfolio = pred_df.groupby("ticker").apply(
        lambda x: np.cumsum(x["order_size"] * (x["vwap"] - x["predicted_slippage"])), include_groups=False
    )
    twap_portfolio = pred_df.groupby("ticker").apply(
        lambda x: np.cumsum(x["order_size"] * x["vwap"]), include_groups=False
    )
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio.mean(), label="Model-Based")
    plt.plot(twap_portfolio.mean(), label="TWAP")
    plt.title("Portfolio Value Simulation")
    plt.xlabel("Trade Index")
    plt.ylabel("Cumulative Value")
    plt.legend()
    pdf.savefig()
    plt.close()

print("PDF generated at plots/model_performance.pdf")