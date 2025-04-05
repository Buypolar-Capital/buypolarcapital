import sys
import os
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
    plot_daily_execution_overlay
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
            nn.Sigmoid()  # outputs execution aggressiveness: 0 to 1
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

    def train_model(self, epochs=5):
        print("Training VWAP model...")
        self.model.train()
        self.losses = []

        for epoch in range(epochs):
            losses = []
            for session in self.train_sessions:
                X = torch.tensor(session["features"].values, dtype=torch.float32)
                target = torch.ones(X.size(0), 1)  # uniform participation
                output = self.model(X)

                loss = self.criterion(output, target)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                losses.append(loss.item())

            avg_loss = np.mean(losses)
            self.losses.append(avg_loss)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.5f}")

    def test_model(self):
        print("Testing VWAP model...")
        self.model.eval()

        slippages = []
        for session in self.test_sessions:
            features = session["features"].values
            price_data = session["price_series"].flatten()[:len(features)]  # Double flatten
            volume_data = session["volume"].flatten()[:len(features)]      # Double flatten

            X = torch.tensor(features, dtype=torch.float32)
            with torch.no_grad():
                aggressiveness = self.model(X).squeeze().numpy()

            if len(price_data) != len(aggressiveness) or len(volume_data) != len(aggressiveness):
                print(f"Skipping {session['date']}: price_data ({len(price_data)}) != aggressiveness ({len(aggressiveness)}) or volume_data ({len(volume_data)})")
                continue

            side = session["side"]
            vwap = session["vwap"]

            exec_price, trade_volumes = compute_execution_price(price_data, volume_data, aggressiveness, self.notional)
            slippage = compute_slippage(exec_price, vwap, side)

            twap = compute_twap(price_data)
            twap_slippage = compute_slippage(twap, vwap, side)

            slippage_entry = {
                "date": session["date"],
                "side": side,
                "exec_price": exec_price,
                "vwap": vwap,
                "twap": twap,
                "slippage": slippage,
                "twap_slippage": twap_slippage,
                "aggressiveness": aggressiveness.copy(),
                "prices": price_data.copy(),  # Already 1D
                "features": features.copy()
            }
            print(f"Added {session['date']}: price_data ({len(price_data)}), aggressiveness ({len(aggressiveness)})")
            slippages.append(slippage_entry)

        return slippages

    def plot_results(self, slippages, prefix="", file_ext=".pdf"):
        print("\nGenerating result plots...")
        out_slippage = f"plots/{prefix}slippage_vs_vwap{file_ext}"
        out_cumsum   = f"plots/{prefix}cumulative_slippage{file_ext}"
        out_csv      = f"results/{prefix}slippage_results.csv"
        out_loss     = f"plots/{prefix}loss_curve{file_ext}"
        out_overlay  = f"plots/{prefix}daily_exec_overlay{file_ext}"

        summarize_slippages(slippages)
        plot_slippage_series(slippages, save_path=out_slippage)
        plot_cumulative_slippage(slippages, save_path=out_cumsum)
        save_results_csv(slippages, path=out_csv)
        print_leaderboard(slippages)
        plot_loss_curve(self.losses, save_path=out_loss)
        plot_daily_execution_overlay(slippages, model=self.model, save_path=out_overlay)