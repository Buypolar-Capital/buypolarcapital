import pandas as pd
import xgboost as xgb
from pathlib import Path

# Paths
FEATURES_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgboost_osebx_model.json"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "data" / "processed" / "predictions.csv"

# Load data
df = pd.read_csv(FEATURES_FILE)
features = ['return_60d', 'volatility_60d', 'turnover_60d', 'trading_days_ratio']
X = df[features]

# Load model
model = xgb.XGBClassifier()
model.load_model(MODEL_PATH)

# Predict probabilities
df['predicted_prob'] = model.predict_proba(X)[:, 1]

# Show top predictions
top_preds = df[['Date', 'ticker', 'predicted_prob']].sort_values('predicted_prob', ascending=False).drop_duplicates('ticker')
top_preds.to_csv(OUTPUT_FILE, index=False)

print(f"Top predictions saved to: {OUTPUT_FILE}")
print(top_preds.head(10))
