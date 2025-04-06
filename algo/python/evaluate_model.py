# File: evaluate_model.py
# Purpose: Load model and compute evaluation metrics on test data

import torch
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from models import SimpleMLP

# Paths
DATA_PATH = Path("data/simulated/exec_dataset.parquet")
MODEL_PATH = Path("model/simple_mlp.pt")
SAVE_PATH = Path("results/eval_predictions.csv")

def load_data():
    df = pd.read_parquet(DATA_PATH)
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    # Features and target
    df["log_order_size"] = np.log1p(df["order_size"])
    features = df[["order_size", "duration", "minutes_since_open", "volume_ratio", "log_order_size"]]
    target = df["slippage"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    return torch.tensor(X_scaled, dtype=torch.float32), target.values, df[["ticker", "date", "start_time"]]

def main():
    print(f"📦 Loading model from: {MODEL_PATH.resolve()}")
    X, y_true, meta = load_data()

    # Init + load model
    model = SimpleMLP(input_dim=X.shape[1])
    model.load_state_dict(torch.load(MODEL_PATH), strict=True)
    model.eval()

    # Predict
    with torch.no_grad():
        y_pred = model(X).squeeze().numpy()

    # Metrics
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    # TWAP baseline
    twap_mae = mean_absolute_error(y_true, np.zeros_like(y_true))  # baseline = 0 slippage

    print(f"📊 Model MAE: {mae:.4f}")
    print(f"📈 R^2 Score: {r2:.4f}")
    print(f"🪵 TWAP MAE: {twap_mae:.4f}")
    print(f"\n🔍 Summary:\nModel improvement over TWAP: {twap_mae - mae:.4f} points of slippage")

    # Save predictions
    results = meta.copy()
    results["true_slippage"] = y_true
    results["predicted_slippage"] = y_pred
    SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(SAVE_PATH, index=False)
    print(f"✅ Saved predictions to {SAVE_PATH}")

if __name__ == "__main__":
    main()
