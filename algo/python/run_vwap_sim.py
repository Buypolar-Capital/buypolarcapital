# File: run_vwap_sim.py

import os
import argparse
from data.vwap_dataset import VWAPExecutionDataset
from model.vwap_trainer import VWAPExecutionTrainer
from utils.execution_helpers import summarize_slippages
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def run_for_ticker(ticker, train_days, test_days, epochs):
    dataset = VWAPExecutionDataset(ticker, days_back=train_days + test_days + 1)
    train, test = dataset.get_train_test_split(train_days=train_days, test_days=test_days)

    print(f"\n=== {ticker} ===")
    print(f"Training on {len(train)} days, Testing on {len(test)} days")

    trainer = VWAPExecutionTrainer(train, test)
    trainer.train_model(epochs=epochs)
    slippages = trainer.test_model()

    os.makedirs(f"results/{ticker}", exist_ok=True)
    os.makedirs(f"plots/{ticker}", exist_ok=True)

    trainer.plot_results(slippages, prefix=f"{ticker}/")
    return pd.DataFrame(slippages)

def generate_leaderboard(all_dfs, save_path="leaderboard.pdf"):
    all_stats = []
    for ticker, df in all_dfs.items():
        df = df.copy()
        win_rate = (df['slippage'] <= 0).mean() * 100
        avg_slip = df['slippage'].mean()
        median_slip = df['slippage'].median()
        cum_slip = df['slippage'].sum()
        all_stats.append({
            "Ticker": ticker,
            "VWAP Win %": win_rate,
            "Avg Slippage": avg_slip,
            "Median Slippage": median_slip,
            "Cumulative Slippage": cum_slip
        })

    leaderboard = pd.DataFrame(all_stats).sort_values("VWAP Win %", ascending=False)

    with PdfPages(save_path) as pdf:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        table = ax.table(cellText=leaderboard.values, colLabels=leaderboard.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title("VWAP Execution Leaderboard", fontsize=14)
        pdf.savefig()
        plt.close()

        # Add bar chart
        leaderboard.set_index("Ticker")["VWAP Win %"].plot(kind="bar", figsize=(10,6), color="skyblue")
        plt.title("VWAP Win Rate by Ticker")
        plt.ylabel("VWAP Win %")
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"\n✅ Saved leaderboard to {save_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tickers', nargs='+', default=['AAPL'])
    parser.add_argument('--train_days', type=int, default=24)
    parser.add_argument('--test_days', type=int, default=5)
    parser.add_argument('--epochs', type=int, default=10)
    args = parser.parse_args()

    all_results = {}
    for ticker in args.tickers:
        df = run_for_ticker(ticker, args.train_days, args.test_days, args.epochs)
        all_results[ticker] = df

    generate_leaderboard(all_results)

if __name__ == "__main__":
    main()
