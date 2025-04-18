import os
import yfinance as yf
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

# ========== SETUP ==========
os.makedirs("plots", exist_ok=True)
torch.manual_seed(42)

# ========== DOWNLOAD DATA ==========
ticker = "AAPL"
df = yf.download(ticker, start="2018-01-01", end="2023-12-31")
df["Return"] = df["Close"].pct_change().fillna(0)

# ========== FEATURE ENGINEERING ==========
df["Target"] = (df["Return"].shift(-1) > 0).astype(int)
df["Volatility"] = df["Return"].rolling(10).std()
df["RSI"] = 100 - (100 / (1 + df["Return"].rolling(14).apply(lambda x: (x[x > 0].mean() / abs(x[x < 0].mean() + 1e-6)) if len(x[x < 0]) > 0 else 0, raw=False)))
df["MA_5"] = df["Close"].rolling(5).mean()
df["MA_10"] = df["Close"].rolling(10).mean()
df["MA_ratio"] = df["MA_5"] / df["MA_10"] - 1

for lag in range(1, 6):
    df[f"lag_{lag}"] = df["Return"].shift(lag)

df.dropna(inplace=True)

features = [f"lag_{i}" for i in range(1, 6)] + ["Volatility", "RSI", "MA_ratio"]
target = "Target"

X = df[features].values
y = df[target].values

# ========== DATASET ==========
class FinanceDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

split = int(0.8 * len(X))
train_ds = FinanceDataset(X[:split], y[:split])
test_ds = FinanceDataset(X[split:], y[split:])
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)

# ========== MODEL ==========
class ImprovedNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(len(features), 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

model = ImprovedNN()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

# ========== TRAIN ==========
for epoch in range(30):
    model.train()
    total_loss = 0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        preds = model(xb)
        loss = criterion(preds, yb)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: Loss = {total_loss:.4f}")

# ========== STRATEGY SIM ==========
model.eval()
with torch.no_grad():
    X_test_tensor = torch.tensor(X[split:], dtype=torch.float32)
    probs = model(X_test_tensor).squeeze().numpy()

df_test = df.iloc[split:].copy()
df_test["Prob"] = probs

# Strategy simulation loop
thresholds = [0.45, 0.48, 0.50, 0.52, 0.55]
results = []

def sharpe_ratio(returns):
    return np.mean(returns) / (np.std(returns) + 1e-8) * np.sqrt(252)

def max_drawdown(cum_returns):
    peak = np.maximum.accumulate(cum_returns)
    drawdown = (cum_returns - peak) / peak
    return drawdown.min()

for threshold in thresholds:
    df_test["Signal"] = np.where(df_test["Prob"] > threshold, 1, -1)  # Long/short
    df_test["Trade"] = df_test["Signal"].diff().fillna(0).abs()
    cost = 0.001
    df_test["TransactionCost"] = df_test["Trade"] * cost
    df_test["StrategyReturn"] = df_test["Signal"] * df_test["Return"] - df_test["TransactionCost"]
    df_test["Cumulative"] = (1 + df_test["StrategyReturn"]).cumprod()
    sr = sharpe_ratio(df_test["StrategyReturn"])
    dd = max_drawdown(df_test["Cumulative"].values)
    results.append((threshold, sr, dd, df_test["Cumulative"].copy()))

# ========== BEST RESULT ==========
best = max(results, key=lambda x: x[1])  # Max Sharpe
best_threshold, best_sr, best_dd, best_cum = best
df_test["Cumulative"] = best_cum
df_test["BuyHold"] = (1 + df_test["Return"]).cumprod()

print(f"\n🏆 Best Threshold: {best_threshold}")
print(f"📈 Sharpe Ratio: {best_sr:.2f}")
print(f"📉 Max Drawdown: {best_dd:.2%}")

# ========== VISUALIZE ==========
plt.figure(figsize=(10, 6))
plt.plot(df_test.index, df_test["Cumulative"], label=f"Strategy (thresh={best_threshold})", linewidth=2)
plt.plot(df_test.index, df_test["BuyHold"], label="Buy & Hold", linestyle="--")

gap = df_test["Cumulative"] - df_test["BuyHold"]
max_gap_idx = gap.abs().idxmax()
plt.axvline(x=max_gap_idx, color="gray", linestyle=":")
plt.text(max_gap_idx, df_test["Cumulative"].loc[max_gap_idx], "Max gap", fontsize=9)

plt.title(f"{ticker} Strategy vs Buy & Hold\nSharpe: {best_sr:.2f}, Max DD: {best_dd:.1%}")
plt.ylabel("Cumulative Return")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("plots/pt_trading_strategy.pdf")
plt.close()

print("✅ Strategy plot saved to plots/pt_trading_strategy.pdf")
