import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import joblib

# Paths
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "features_2010_2022.csv"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgboost_osebx_model.json"
FEATURES_PATH = Path(__file__).resolve().parent.parent / "models" / "features.txt"
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
X = df[["return_60d", "volatility_60d", "turnover_60d", "trading_days_ratio"]]
y = df["included"]

# Save the features used
with open(FEATURES_PATH, "w") as f:
    f.write("\n".join(X.columns.tolist()))

# Split and train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
print("Classification Report:\n", report)

# Save model
model.save_model(MODEL_PATH)
print(f"Model saved to: {MODEL_PATH}")
print(f"Feature list saved to: {FEATURES_PATH}")
