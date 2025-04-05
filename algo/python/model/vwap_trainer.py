import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from utils.execution_helpers import (
    compute_execution_price,
    compute_slippage,
    compute_twap,
    summarize_slippages,
    plot_slippage_series,
    plot_cumulative_slippage,
    save_results_csv,
    print_leaderboard,
    plot_loss_curve,
    compute_metrics
)

class SimpleVWAPModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

class VWAPExecutionTrainer:
    def __init__(self, train_sessions, test_sessions, notional=100000):
        self.train_sessions = train_sessions
        self.test_sessions = test_sessions
        self.notional = notional

        input_dim = self.train_sessions[0]["features"].shape[1]
        self.model = SimpleVWAPModel(input_dim)
        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.losses = []

    def train_model(self, epochs=10):
        self.model.train()
        self.losses = []
        for epoch in range(epochs):
            losses = []
            for session in self.train_sessions:
                X = torch.tensor(session["features"].values, dtype=torch.float32)
                target = torch.ones(X.size(0), 1)
                output = self.model(X)
                loss = self.criterion(output, target)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                losses.append(loss.item())
            avg_loss = np.mean(losses)
            self.losses.append(avg_loss)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.5f}")

    def test_model(self, strategy="vwap"):
        self.model.eval()
        slippages = []

        for session in self.test_sessions:
            features = session["features"].values
            price_data = session["price_series"].flatten()[:len(features)]
            volume_data = session["volume"].flatten()[:len(features)]

            if strategy == "vwap":
                X = torch.tensor(features, dtype=torch.float32)
                with torch.no_grad():
                    aggressiveness = self.model(X).squeeze().numpy()
            elif strategy == "twap":
                aggressiveness = np.ones(len(price_data))
            elif strategy == "random":
                aggressiveness = np.random.rand(len(price_data))
            else:
                raise ValueError(f"Unknown strategy: {strategy}")

            if len(price_data) != len(aggressiveness):
                print(f"⚠️ Skipping {session['date']}: price/agg mismatch")
                continue

            side = session["side"]
            vwap = session["vwap"]

            exec_price, _ = compute_execution_price(price_data, volume_data, aggressiveness, self.notional)
            slippage = compute_slippage(exec_price, vwap, side)
            twap_price = compute_twap(price_data)
            twap_slippage = compute_slippage(twap_price, vwap, side)

            slippages.append({
                "date": session["date"],
                "side": side,
                "exec_price": exec_price,
                "vwap": vwap,
                "twap": twap_price,
                "slippage": slippage,
                "twap_slippage": twap_slippage
            })

        return slippages

    def test_twap_baseline(self):
        return self.test_model(strategy="twap")

    def test_random_baseline(self):
        return self.test_model(strategy="random")

    def plot_results(self, slippages, prefix=""):
        summarize_slippages(slippages)
        plot_slippage_series(slippages, save_path=f"plots/{prefix}slippage_vs_vwap.pdf")
        plot_cumulative_slippage(slippages, save_path=f"plots/{prefix}cumulative_slippage.pdf")
        save_results_csv(slippages, path=f"results/{prefix}slippage_results.csv")
        plot_loss_curve(self.losses, save_path=f"plots/{prefix}loss_curve.pdf")
        print_leaderboard(slippages)

    def get_metrics(self, slippages, label="model"):
        return compute_metrics(slippages, label=label)
