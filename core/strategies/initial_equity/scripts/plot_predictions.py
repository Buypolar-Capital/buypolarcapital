import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import joblib

# Paths
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgboost_osebx_model.json"
PLOT_PATH = Path(__file__).resolve().parent.parent / "plots"
PLOT_PATH.mkdir(parents=True, exist_ok=True)

# Load data and model
df = pd.read_csv(DATA_PATH)
X = df[["return_60d", "volatility_60d", "turnover_60d", "trading_days_ratio"]]

# Load the trained model
model = joblib.load(MODEL_PATH)

# Make predictions
df["prediction"] = model.predict(X)

# Plotting
plt.figure(figsize=(10, 6))
df.groupby("Date")["prediction"].sum().plot()
plt.title("Predicted Inclusions Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Inclusions")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plot_path = PLOT_PATH / "index_addition_predictions.pdf"
plt.savefig(plot_path)
plt.close()

print(f"Prediction plot saved to: {plot_path}")
