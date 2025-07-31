import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import xgboost as xgb
from pathlib import Path
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Paths
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgboost_osebx_model.json"
PLOT_PATH = Path(__file__).resolve().parent.parent / "plots"
PLOT_PATH.mkdir(parents=True, exist_ok=True)

# Load and prepare data
df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
features = ["return_60d", "volatility_60d", "turnover_60d", "trading_days_ratio"]
X = df[features]

# Load model and predict
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)
df["prediction"] = model.predict(X)

# Compute log return
df["log_return"] = (1 + df["return_60d"]).apply(lambda x: np.nan if x <= 0 else np.log(x))

# Long: predicted 1 (added), Short: predicted 0 (removed)
long_returns = df[df["prediction"] == 1].groupby("Date")["log_return"].mean()
short_returns = df[df["prediction"] == 0].groupby("Date")["log_return"].mean()
ls_returns = (long_returns - short_returns).dropna()
ls_cum = ls_returns.cumsum().apply(np.exp)

# Benchmark: OSEBX
osebx = yf.download("^OSEAX", start="2010-01-01", end="2022-12-31", progress=False)
osebx["log_return"] = np.log(osebx["Close"] / osebx["Close"].shift(1))
osebx["cum_return"] = osebx["log_return"].cumsum().apply(np.exp)

# Combine strategy and benchmark
combined = pd.DataFrame({
    "Long-Short Strategy": ls_cum,
    "OSEBX Benchmark": osebx["cum_return"]
}).dropna()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
combined.plot(ax=ax, linewidth=2)
ax.set_title("📈 Long-Short Index Effect Strategy vs OSEBX Benchmark")
ax.set_ylabel("Cumulative Return")
ax.set_xlabel("Date")
ax.grid(True)
ax.legend()
plt.tight_layout()

# Save to PDF
plot_file = PLOT_PATH / "index_effect_vs_osebx.pdf"
plt.savefig(plot_file)
print(f"📊 Comparison plot saved to: {plot_file}")
