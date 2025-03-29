import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import plotly.express as px

st.title("🔮 FX ML Signal Generator – Logistic Regression vs XGBoost")

# -------------------------------
# Load FX data
# -------------------------------
st.subheader("💱 Load FX Data")

fx_ticker = st.selectbox("Select FX Pair", ["USDNOK=X", "EURNOK=X", "JPYUSD=X"])
price_series = yf.download(fx_ticker, start="2020-01-01", auto_adjust=True)["Close"].dropna()

# Build DataFrame and assign the price column
df = pd.DataFrame()
df["price"] = price_series
df["return"] = df["price"].pct_change()

# -------------------------------
# Feature engineering
# -------------------------------
st.subheader("🧮 Feature Engineering")

df["return"] = df["price"].pct_change()
df["target"] = (df["return"].shift(-1) > 0).astype(int)

# Lagged features
for lag in range(1, 4):
    df[f"lag_{lag}"] = df["return"].shift(lag)

# Rolling stats
df["rolling_mean"] = df["price"].rolling(5).mean().pct_change()
df["rolling_std"] = df["price"].rolling(5).std()
df["momentum"] = df["price"] - df["price"].shift(5)

df.dropna(inplace=True)

features = ["lag_1", "lag_2", "lag_3", "rolling_mean", "rolling_std", "momentum"]
X = df[features]
y = df["target"]

# -------------------------------
# Train/test split
# -------------------------------
split_idx = int(len(df) * 0.7)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

# -------------------------------
# Train models
# -------------------------------
st.subheader("🧠 Training Models")

lr = LogisticRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
y_proba_lr = lr.predict_proba(X_test)[:, 1]

xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)
y_proba_xgb = xgb.predict_proba(X_test)[:, 1]

# -------------------------------
# Evaluation
# -------------------------------
st.subheader("📊 Model Performance")

metrics_df = pd.DataFrame({
    "Model": ["Logistic Regression", "XGBoost"],
    "Accuracy": [accuracy_score(y_test, y_pred_lr), accuracy_score(y_test, y_pred_xgb)],
    "AUC": [roc_auc_score(y_test, y_proba_lr), roc_auc_score(y_test, y_proba_xgb)]
})
st.dataframe(metrics_df.set_index("Model"))

# -------------------------------
# Signal chart
# -------------------------------
st.subheader("📈 Predicted Signals vs Actual")

signal_df = pd.DataFrame({
    "Actual": y_test,
    "LR Prob": y_proba_lr,
    "XGB Prob": y_proba_xgb
}, index=y_test.index)

signal_df["LR Signal"] = signal_df["LR Prob"].apply(lambda p: "Buy" if p > 0.5 else "Sell")
signal_df["XGB Signal"] = signal_df["XGB Prob"].apply(lambda p: "Buy" if p > 0.5 else "Sell")

plot_df = signal_df[["Actual", "LR Prob", "XGB Prob"]].copy()
plot_df["Date"] = plot_df.index

fig = px.line(plot_df, x="Date", y=["LR Prob", "XGB Prob"], title="📉 Model Signal Probabilities Over Time")
st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Latest signal
# -------------------------------
st.subheader("🔔 Latest Prediction")

latest_features = X.iloc[[-1]]
latest_lr = lr.predict_proba(latest_features)[0, 1]
latest_xgb = xgb.predict_proba(latest_features)[0, 1]

st.metric("Logistic Regression Signal", "Buy" if latest_lr > 0.5 else "Sell", f"{latest_lr:.2%}")
st.metric("XGBoost Signal", "Buy" if latest_xgb > 0.5 else "Sell", f"{latest_xgb:.2%}")

st.caption("🚨 Disclaimer: Signals are experimental and not investment advice.")
