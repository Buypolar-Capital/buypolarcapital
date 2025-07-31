import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from pathlib import Path
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Paths
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgboost_osebx_model.json"
PLOT_PATH = Path(__file__).resolve().parent.parent / "plots"
PLOT_PATH.mkdir(parents=True, exist_ok=True)

# Load data and model
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

# Predict inclusion using only trained features
features = ["return_60d", "volatility_60d", "turnover_60d", "trading_days_ratio"]
X = df[features]
df["prediction"] = model.predict(X)

# Create log return column
df["log_return"] = np.log1p(df["return_60d"])

# Simulate strategy: average return of predicted stocks
daily_perf = df[df["prediction"] == 1].groupby("Date")["log_return"].mean().dropna()
cumulative_return = daily_perf.cumsum().apply(np.exp)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
cumulative_return.plot(ax=ax, color="tab:green", label="Predicted Index Inclusion Strategy")
ax.set_title("Naive Backtest: Cumulative Return from Predicted Inclusions")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.legend()
plt.tight_layout()

# Save to PDF
plot_file = PLOT_PATH / "backtest_predicted_inclusions.pdf"
plt.savefig(plot_file)
print(f"📉 Backtest plot saved to: {plot_file}")
