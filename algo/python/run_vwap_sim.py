# File: buypolarcapital/algo/python/run_vwap_sim.py

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from data.vwap_dataset import VWAPExecutionDataset
from model.vwap_trainer import VWAPExecutionTrainer
from utils.execution_helpers import summarize_slippages
from utils.report_helpers import create_model_comparison_report


def run_for_ticker(ticker, train_days, test_days, epochs):
    dataset = VWAPExecutionDataset(ticker, days_back=train_days + test_days + 1)
    train, test = dataset.get_train_test_split(train_days=train_days, test_days=test_days)

    print(f"\n=== {ticker} ===")
    print(f"Training on {len(train)} days, Testing on {len(test)} days")

    trainer = VWAPExecutionTrainer(train, test)
    trainer.train_model(epochs=epochs)
    vwap_slippages = trainer.test_model()
    twap_slippages = trainer.test_twap_baseline()
    rand_slippages = trainer.test_random_baseline()

    # Save visualizations and metrics
    trainer.plot_results(vwap_slippages, prefix=f"{ticker}/")

    # Get metrics per model
    vwap_metrics = trainer.get_metrics(vwap_slippages, label="VWAP Model")
    twap_metrics = trainer.get_metrics(twap_slippages, label="TWAP Baseline")
    rand_metrics = trainer.get_metrics(rand_slippages, label="Random")

    return {
        "VWAP Model": vwap_metrics,
        "TWAP Baseline": twap_metrics,
        "Random": rand_metrics
    }


def generate_leaderboard(results_dict, save_path="reports/leaderboard.pdf"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df = pd.DataFrame(results_dict).T.reset_index()
    df.rename(columns={"index": "Strategy"}, inplace=True)
    df[["avg_slip", "sharpe", "hit_ratio"]] = df[["avg_slip", "sharpe", "hit_ratio"]].round(4)

    with PdfPages(save_path) as pdf:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title("Execution Strategy Leaderboard", fontsize=14)
        pdf.savefig()
        plt.close()

        df.set_index("Strategy")[["avg_slip", "sharpe"]].plot(kind="bar", figsize=(10,6))
        plt.title("Model Comparison: Avg Slippage & Sharpe Ratio")
        plt.grid(True)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"✅ Saved leaderboard to {save_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tickers', nargs='+', default=['AAPL'])
    parser.add_argument('--train_days', type=int, default=24)
    parser.add_argument('--test_days', type=int, default=5)
    parser.add_argument('--epochs', type=int, default=10)
    args = parser.parse_args()

    combined_results = {}

    for ticker in args.tickers:
        metrics = run_for_ticker(ticker, args.train_days, args.test_days, args.epochs)
        for model, result in metrics.items():
            key = f"{ticker} – {model}"
            combined_results[key] = result

    # Format combined_results to match expected structure
    results_list = []
    for key, metrics in combined_results.items():
        ticker, strategy = key.split(" – ")
        results_list.append({
            "ticker": ticker,
            "strategy": strategy,
            "metrics": metrics
        })

    create_model_comparison_report(results_list, save_path="reports/model_comparison.pdf")


if __name__ == "__main__":
    main()
