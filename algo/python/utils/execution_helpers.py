import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.backends.backend_pdf import PdfPages
import torch

def compute_slippage(executed_price, vwap, side):
    if side == "buy":
        return executed_price - vwap
    elif side == "sell":
        return vwap - executed_price
    else:
        raise ValueError("Side must be 'buy' or 'sell'")

def compute_execution_price(price_data, volume_data, aggressiveness, notional):
    weights = aggressiveness / (aggressiveness.sum() + 1e-8)
    total_shares = notional / price_data.mean()
    trade_volumes = weights * total_shares
    exec_price = np.sum(price_data * trade_volumes) / total_shares
    return exec_price, trade_volumes

def compute_twap(price_data):
    return np.mean(price_data)

def summarize_slippages(slippages):
    df = pd.DataFrame(slippages)
    print("\n--- Slippage Summary ---")
    print(f"Avg Slippage: {df['slippage'].mean():.4f}")
    print(f"Median Slippage: {df['slippage'].median():.4f}")
    print(f"VWAP or better: {(df['slippage'] <= 0).mean() * 100:.1f}% of days")
    return df

def compute_metrics(slippages, label="Model"):
    df = pd.DataFrame(slippages)
    sharpe = df["slippage"].mean() / (df["slippage"].std() + 1e-8)
    hit_ratio = (df["slippage"] < df["twap_slippage"]).mean()
    max_dd = (df["slippage"].cumsum().cummax() - df["slippage"].cumsum()).max()
    summary = {
        "model": label,
        "avg_slip": df["slippage"].mean(),
        "std_slip": df["slippage"].std(),
        "sharpe": sharpe,
        "hit_ratio": hit_ratio,
        "max_drawdown": max_dd
    }
    return summary

def print_leaderboard(slippages, top_n=5):
    df = pd.DataFrame(slippages).copy()
    df_sorted = df.sort_values("slippage")
    print("\n--- VWAP Execution Leaderboard ---")
    print(df_sorted[["date", "side", "slippage", "twap_slippage"]].head(top_n))
    print("\n--- Worst Execution Days ---")
    print(df_sorted[["date", "side", "slippage", "twap_slippage"]].tail(top_n))
    return df_sorted

def plot_slippage_series(slippages, save_path=None):
    dates = [s["date"] for s in slippages]
    model_slip = [s["slippage"] for s in slippages]
    twap_slip = [s["twap_slippage"] for s in slippages if "twap_slippage" in s]

    plt.figure(figsize=(12, 4))
    plt.plot(dates, model_slip, marker="o", label="Model Slippage")
    if twap_slip:
        plt.plot(dates, twap_slip, marker="x", linestyle="--", label="TWAP Slippage")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Slippage vs VWAP")
    plt.ylabel("Slippage")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Saved plot to {save_path}")
    plt.close()

def plot_cumulative_slippage(slippages, save_path=None):
    dates = [s["date"] for s in slippages]
    cumsum = np.cumsum([s["slippage"] for s in slippages])

    plt.figure(figsize=(10, 4))
    plt.plot(dates, cumsum, marker="o")
    plt.title("Cumulative Slippage Over Time")
    plt.ylabel("Cumulative Slippage")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Saved cumulative plot to {save_path}")
    plt.close()

def save_results_csv(slippages, path="results/slippage_results.csv"):
    df = pd.DataFrame(slippages)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved results to {path}")

def plot_loss_curve(losses, save_path="plots/loss_curve.pdf"):
    plt.figure(figsize=(8, 4))
    plt.plot(losses, marker="o", label="Training Loss")
    plt.title("Training Loss Over Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    print(f"Saved loss curve to {save_path}")
    plt.close()


def plot_daily_execution_overlay(slippages, model, save_path="plots/daily_exec_analytics.pdf"):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with PdfPages(save_path) as pdf:
        for session in slippages:
            day_prices = np.array(session["prices"]).flatten()
            day_aggr = np.array(session["aggressiveness"]).flatten()
            day_side = session["side"]
            day_date = session["date"]
            day_vwap = session["vwap"]
            day_exec_price = session["exec_price"]
            day_twap = session["twap"]

            _, day_trade_volumes = compute_execution_price(day_prices, None, day_aggr, 100000)
            day_shares = day_trade_volumes  # Already shares per minute
            day_shares = np.nan_to_num(day_shares, nan=0.0, posinf=0.0, neginf=0.0)
            cum_shares = np.cumsum(day_shares)

            print(f"{day_date}: prices ({len(day_prices)}), aggr ({len(day_aggr)}), trade_volumes ({len(day_trade_volumes)}), shares ({len(day_shares)}), max_shares ({np.max(day_shares):.2f}), total_shares ({cum_shares[-1]:.2f})")
            print(f"Trade volumes sample: {day_trade_volumes[:5]}")
            print(f"Shares sample: {day_shares[:5]}")

            if len(day_prices) != len(day_aggr) or len(day_shares) != len(day_prices):
                print(f"⚠️ Skipping {day_date}: length mismatch - prices ({len(day_prices)}), aggr ({len(day_aggr)}), shares ({len(day_shares)})")
                continue

            # Plot 1: Cumulative Shares Traded
            plt.figure(figsize=(10, 6))
            plt.plot(cum_shares, label="Cumulative Shares", color="purple")
            plt.title(f"{day_date} ({day_side}) - Cumulative Shares Traded")
            plt.xlabel("Minute of Day")
            plt.ylabel("Cumulative Shares")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plot 2: Price Overlay
            plt.figure(figsize=(10, 6))
            plt.plot(day_prices, label="Price", color="gray", alpha=0.6)
            plt.axhline(day_vwap, color="blue", linestyle="--", label=f"VWAP ({day_vwap:.2f})")
            plt.axhline(day_exec_price, color="green", linestyle="-.", label=f"Exec Price ({day_exec_price:.2f})")
            plt.axhline(day_twap, color="orange", linestyle=":", label=f"TWAP ({day_twap:.2f})")
            plt.title(f"{day_date} ({day_side}) - Price Overlay")
            plt.xlabel("Minute of Day")
            plt.ylabel("Price ($)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plot 3: Aggressiveness Profile
            plt.figure(figsize=(10, 6))
            plt.plot(day_aggr, label="Aggressiveness", color="red")
            plt.title(f"{day_date} ({day_side}) - Aggressiveness Profile")
            plt.xlabel("Minute of Day")
            plt.ylabel("Aggressiveness (0-1)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # Plot 4: Shares Traded vs. Price
            fig, ax1 = plt.subplots(figsize=(10, 6))
            ax1.plot(day_prices, color="gray", alpha=0.6, label="Price")
            ax1.set_xlabel("Minute of Day")
            ax1.set_ylabel("Price ($)", color="gray")
            ax1.tick_params(axis="y", labelcolor="gray")
            ax2 = ax1.twinx()
            ax2.bar(range(len(day_shares)), day_shares, alpha=0.5, color="blue", label="Shares Traded", width=1.0)
            ax2.set_ylabel("Shares Traded", color="blue")
            ax2.tick_params(axis="y", labelcolor="blue")
            plt.title(f"{day_date} ({day_side}) - Shares Traded vs. Price")
            fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)
            plt.grid(True)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

    print(f"✅ Saved daily execution analytics PDF to {save_path}")