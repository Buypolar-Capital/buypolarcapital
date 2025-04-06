# File: train_nn.py
# Purpose: Train a simple neural net to predict execution slippage

import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from models import SimpleMLP

DATA_PATH = Path("data/simulated/exec_dataset.parquet")
MODEL_PATH = Path("model/simple_mlp.pt")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_data():
    df = pd.read_parquet(DATA_PATH)
    print(df["slippage"].describe())

    # Drop NaNs/Infs
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    print(f"{df['slippage'].isna().sum()} NaNs")
    print(f"{np.isinf(df['slippage']).sum()} Infs")

    # Feature engineering
    df["log_order_size"] = np.log1p(df["order_size"])
    features = df[["order_size", "duration", "minutes_since_open", "volume_ratio", "log_order_size", "price_volatility"]]  # Added price_volatility
    target = df["slippage"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, target.values, test_size=0.2, random_state=42
    )

    return (
        torch.tensor(X_train, dtype=torch.float32),
        torch.tensor(y_train, dtype=torch.float32).view(-1, 1),
        torch.tensor(X_test, dtype=torch.float32),
        torch.tensor(y_test, dtype=torch.float32).view(-1, 1),
        scaler,
    )

def train_model():
    if MODEL_PATH.exists():
        os.remove(MODEL_PATH)
        print(f"🧹 Removed existing model: {MODEL_PATH}")

    X_train, y_train, X_test, y_test, scaler = load_data()
    model = SimpleMLP(input_dim=X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    best_test_loss = float('inf')
    patience = 10
    patience_counter = 0

    for epoch in range(100):  # Increased to 100
        model.train()
        y_pred = model(X_train)
        loss = criterion(y_pred, y_train)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            test_loss = criterion(model(X_test), y_test)
        print(f"Epoch {epoch+1}/100 | Train Loss: {loss.item():.5f} | Test Loss: {test_loss.item():.5f}")

        if test_loss < best_test_loss:
            best_test_loss = test_loss
            patience_counter = 0
            torch.save(model.state_dict(), MODEL_PATH)
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break

    print(f"✅ Model saved to {MODEL_PATH} with best test loss: {best_test_loss:.5f}")

if __name__ == "__main__":
    train_model()
